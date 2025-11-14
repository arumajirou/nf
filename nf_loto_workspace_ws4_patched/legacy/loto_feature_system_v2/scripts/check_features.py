#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
features_* テーブルの存在・行数・列数・簡易健全性をチェックするスクリプト。
- パッケージ名衝突（core 等）を避けるため、当プロジェクトの src を sys.path 先頭へ。
- DatabaseManager.get_table_info() の仕様差に耐えるようフェイルセーフ実装。
"""

import os
import sys
import logging
import yaml
import pandas as pd

# --- 自分の src を最優先に通す ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from core.database_manager import DatabaseManager  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger("check_features")


def load_config():
    cfg_path = os.path.join(PROJECT_ROOT, 'config', 'db_config.yaml')
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"設定ファイルが見つかりません: {cfg_path}")
    with open(cfg_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def to_list_safe(cols):
    """columns が set/dict/tuple/None/str でも安全にリスト化する。"""
    if cols is None:
        return []
    if isinstance(cols, dict):
        # information_schema の dict などが来た場合はキー名でそろえる（必要なら調整）
        cols = list(cols.keys())
    elif isinstance(cols, (set, tuple)):
        cols = list(cols)
    elif isinstance(cols, str):
        cols = [cols]
    elif isinstance(cols, list):
        pass
    else:
        # 想定外型は文字列化して単一要素に
        cols = [str(cols)]
    return cols


def get_table_info_safe(db: DatabaseManager, table: str):
    """
    DatabaseManager.get_table_info() があれば使い、
    足りない情報は engine 経由の SQL で補完する。
    返り値: dict(row_count, n_columns, columns)
    """
    info = {}
    # まずは既存 API を試す
    try:
        base = db.get_table_info(table)
        if isinstance(base, dict):
            info.update(base)
    except Exception:
        pass

    # 欠けているものを補う
    engine = getattr(db, "engine", None)
    if engine is not None:
        try:
            if "n_columns" not in info or not info.get("n_columns"):
                q = """
                    SELECT COUNT(*) AS n_columns
                    FROM information_schema.columns
                    WHERE table_schema='public' AND table_name=%(t)s
                """
                n = pd.read_sql(q, engine, params={"t": table}).iloc[0, 0]
                info["n_columns"] = int(n)

            if "columns" not in info or not info.get("columns"):
                q = """
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema='public' AND table_name=%(t)s
                    ORDER BY ordinal_position
                """
                cols = pd.read_sql(q, engine, params={"t": table})["column_name"].tolist()
                info["columns"] = cols

            if "row_count" not in info or info.get("row_count") in (None, -1):
                q = f"SELECT COUNT(*) AS cnt FROM {table}"
                info["row_count"] = int(pd.read_sql(q, engine).iloc[0, 0])
        except Exception as e:
            log.warning(f"{table}: 追加情報の取得に失敗: {e}")

    # 最低限形を整える
    info.setdefault("row_count", None)
    info.setdefault("n_columns", len(to_list_safe(info.get("columns"))))
    info["columns"] = to_list_safe(info.get("columns"))
    return info


def print_table_info(db: DatabaseManager, table: str):
    info = get_table_info_safe(db, table)
    row_count = info.get('row_count')
    n_columns = info.get('n_columns')
    sample_cols = info.get('columns')[:10]  # ここはすでに list 化済み

    log.info(f"[{table}] rows={row_count}, cols={n_columns}")
    if sample_cols:
        log.info(f"  columns(head): {', '.join(sample_cols)}")


def fetch_df(db: DatabaseManager, sql: str, params: dict | None = None) -> pd.DataFrame:
    engine = getattr(db, "engine", None)
    if engine is None:
        raise RuntimeError("DatabaseManager.engine が見つかりません。SQL 実行に必要です。")
    return pd.read_sql(sql, engine, params=params)


def print_basic_checks(db: DatabaseManager):
    """代表的な欠損と PK 重複の簡易チェック。"""
    try:
        nulls = fetch_df(db, """
            SELECT 
              SUM((hist_y_lag1 IS NULL)::int) AS null_lag1,
              SUM((hist_y_roll_mean_w7 IS NULL)::int) AS null_mean7
            FROM features_hist
        """)
        log.info(f"[features_hist nulls] {nulls.to_dict(orient='records')[0]}")
    except Exception as e:
        log.warning(f"NULL チェックをスキップ: {e}")

    try:
        dups = fetch_df(db, """
            SELECT COUNT(*) AS dup_cnt FROM (
              SELECT loto, unique_id, ds, COUNT(*) 
              FROM features_hist 
              GROUP BY 1,2,3 
              HAVING COUNT(*) > 1
            ) t
        """)
        log.info(f"[features_hist duplicates] count={int(dups.iloc[0,0])}")
    except Exception as e:
        log.warning(f"重複チェックをスキップ: {e}")


def print_head_sample(db: DatabaseManager):
    try:
        head = fetch_df(db, """
            SELECT * FROM features_hist 
            ORDER BY loto, unique_id, ds 
            LIMIT 5
        """)
        log.info("features_hist sample (top 5):\n" + head.to_string(index=False))
    except Exception as e:
        log.warning(f"サンプル取得をスキップ: {e}")


def main() -> int:
    try:
        cfg = load_config()
    except Exception as e:
        log.error(e)
        return 1

    db = DatabaseManager(cfg)

    for t in ['features_hist', 'features_futr', 'features_stat']:
        print_table_info(db, t)

    print_basic_checks(db)
    print_head_sample(db)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
