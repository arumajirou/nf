#!/usr/bin/env python
"""
シンプルな特徴量生成スクリプト（修正版）
- パイプラインから生成した特徴量をDBスキーマに合わせて自動整形
- 既知の列名差異（Fourier周期の小数点表記など）をリネーム
- 余計な列は削除し、足りない列はNULLで補完してUPSERT
"""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Set

# src を import パスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import yaml
import pandas as pd
import logging
from tqdm import tqdm

from core.database_manager import DatabaseManager
from core.data_loader import DataLoader
from pipelines.basic_stats import BasicStatsPipeline
from pipelines.calendar_features import CalendarFeaturesPipeline

# ----------------------------------
# ロギング
# ----------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ----------------------------------
# ユーティリティ
# ----------------------------------
FOURIER_RENAME_MAP: Dict[str, str] = {
    # 30.44日（月相当） -> 30
    'futr_p30_44_k1_sin': 'futr_p30_k1_sin',
    'futr_p30_44_k1_cos': 'futr_p30_k1_cos',
    'futr_p30_44_k2_sin': 'futr_p30_k2_sin',
    'futr_p30_44_k2_cos': 'futr_p30_k2_cos',
    # 365.25日（年相当） -> 365
    'futr_p365_25_k1_sin': 'futr_p365_k1_sin',
    'futr_p365_25_k1_cos': 'futr_p365_k1_cos',
    'futr_p365_25_k2_sin': 'futr_p365_k2_sin',
    'futr_p365_25_k2_cos': 'futr_p365_k2_cos',
}


def _ensure_required_meta_columns(df: pd.DataFrame, base_df: pd.DataFrame, loto: str, uid: str) -> pd.DataFrame:
    """loto / unique_id / ds を安全に付与し、型も整える。
    base_df は元の系列データ（必ず 'ds' を持つ）。
    """
    out = df.copy()
    out['loto'] = loto
    out['unique_id'] = uid

    # ds はパイプラインが持っていない可能性があるため、元系列から移す
    out['ds'] = pd.to_datetime(base_df['ds']).dt.date

    # 型の安定化
    out['loto'] = out['loto'].astype(str)
    out['unique_id'] = out['unique_id'].astype(str)
    return out


def _rename_known_mismatches(df: pd.DataFrame) -> pd.DataFrame:
    """既知の列名ミスマッチ（小数点入り周期名など）をリネーム。"""
    cols = df.columns.tolist()
    rename_map = {c: FOURIER_RENAME_MAP[c] for c in cols if c in FOURIER_RENAME_MAP}
    if rename_map:
        logger.info(f"Fourier列のリネーム: {rename_map}")
        df = df.rename(columns=rename_map)
    return df


def _align_to_table_schema(df: pd.DataFrame, allowed_cols: Set[str]) -> pd.DataFrame:
    """テーブルに存在しない列を落とし、存在するが欠けている列はNULLで補完して整列する。"""
    # メタ列（DB側で自動）は扱わない
    meta_auto = {'created_at', 'updated_at'}

    present = set(df.columns)
    drop_cols = [c for c in df.columns if c not in allowed_cols]
    if drop_cols:
        logger.info(f"テーブル未定義列を削除: {drop_cols[:8]}{'...' if len(drop_cols) > 8 else ''}")
        df = df.drop(columns=drop_cols)

    missing = [c for c in allowed_cols if c not in present and c not in meta_auto]
    for c in missing:
        df[c] = pd.NA

    # 主キー順などに合わせて軽く整列（順序はUPSERTでは必須ではないが読みやすさのため）
    ordered = [c for c in allowed_cols if c in df.columns]  # 既存＋補完列のみ
    return df[ordered]


def main() -> int:
    # 設定読み込み
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'db_config.yaml')
    if not os.path.exists(config_path):
        logger.error(f"設定ファイルが見つかりません: {config_path}")
        return 1

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    logger.info("=== 宝くじ時系列特徴量生成 ===\n")

    # データ読み込み
    logger.info("データ読み込み中...")
    data_loader = DataLoader(config)
    try:
        df_dict = data_loader.load_by_series('nf_loto_final')
        logger.info(f"読み込み完了: {len(df_dict)}系列\n")
    except Exception as e:
        logger.error(f"データ読み込み失敗: {e}")
        logger.info("nf_loto_finalテーブルが存在することを確認してください")
        return 1

    # パイプライン初期化
    logger.info("パイプライン初期化中...")
    pipelines = {
        'basic_stats': BasicStatsPipeline(),
        'calendar': CalendarFeaturesPipeline(),
    }
    logger.info(f"パイプライン数: {len(pipelines)}\n")

    # 特徴量生成
    logger.info("特徴量生成中...")
    hist_features: List[pd.DataFrame] = []
    futr_features: List[pd.DataFrame] = []

    for (loto, unique_id), series_df in tqdm(df_dict.items(), desc="系列処理"):
        for pipeline_name, pipeline in pipelines.items():
            try:
                feats = pipeline.generate(series_df)
                if feats is None or len(feats) == 0:
                    logger.warning(f"{pipeline_name} で {loto}/{unique_id} の特徴量生成が空")
                    continue

                feats = _ensure_required_meta_columns(feats, series_df, loto, unique_id)

                # パイプライン種別で集約
                ftype = pipeline.get_feature_type()
                if ftype == 'hist':
                    hist_features.append(feats)
                elif ftype == 'futr':
                    # 既知のミスマッチ（Fourier名など）をここで修正
                    feats = _rename_known_mismatches(feats)
                    futr_features.append(feats)
                else:
                    # 今回のシンプル版では 'hist' と 'futr' のみ扱う
                    logger.debug(f"未対応feature_type={ftype} をスキップ")
            except Exception as e:
                logger.error(f"{pipeline_name} で {loto}/{unique_id} の処理中にエラー: {e}")
                continue

    # 統合
    logger.info("\n特徴量統合中...")
    if hist_features:
        hist_df = pd.concat(hist_features, ignore_index=True)
        logger.info(f"Historical特徴量: {len(hist_df)}行 × {len(hist_df.columns)}列")
    else:
        hist_df = pd.DataFrame()
        logger.warning("Historical特徴量が生成されませんでした")

    if futr_features:
        futr_df = pd.concat(futr_features, ignore_index=True)
        logger.info(f"Future特徴量: {len(futr_df)}行 × {len(futr_df.columns)}列")
    else:
        futr_df = pd.DataFrame()
        logger.warning("Future特徴量が生成されませんでした")

    # データベース保存
    logger.info("\nデータベース保存中...")
    db_manager = DatabaseManager(config)

    try:
        # スキーマ情報を取得し、列を整合
        if not hist_df.empty:
            hist_info = db_manager.get_table_info('features_hist')  # columns は dict を想定
            hist_allowed: Set[str] = set(hist_info['columns'].keys())
            hist_df = _align_to_table_schema(hist_df, hist_allowed)
            rows = db_manager.upsert_features(hist_df, 'features_hist')
            logger.info(f"features_hist へのUPSERT完了: {rows}行")

        if not futr_df.empty:
            futr_info = db_manager.get_table_info('features_futr')
            futr_allowed: Set[str] = set(futr_info['columns'].keys())
            futr_df = _align_to_table_schema(futr_df, futr_allowed)
            rows = db_manager.upsert_features(futr_df, 'features_futr')
            logger.info(f"features_futr へのUPSERT完了: {rows}行")

        logger.info("\n=== 完了 ===")
        return 0

    except Exception as e:
        logger.error(f"データベース保存失敗: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
