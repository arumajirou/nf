# =====================================================
# NeuralForecast モデル完全パラメータ抽出ツール（PostgreSQL統合版）
# - すべてのパラメータを網羅的に取得
# - PostgreSQLにカテゴリ別テーブルとして保存
# - 個別ファイルダウンロード機能
# - エラーハンドリング強化
# =====================================================
"""
NeuralForecastモデルの全パラメータを抽出し、PostgreSQLに保存するツール

【新機能】
1. PostgreSQL統合: Categoryごとにテーブル作成
2. 個別ファイル保存: 処理中断対策
3. 段階的実行: 各ステップごとに保存
4. 詳細ログ: 進捗と結果を明確に表示

【使用例】
# 基本的な使い方
extractor = NeuralForecastExtractor(MODEL_DIR)
results = extractor.run_full_extraction(save_to_postgres=True)

# 個別ステップ実行
extractor.extract_model_params()
extractor.extract_pkl_params()
extractor.save_all_to_files()
extractor.save_to_postgres()
"""

import os, sys, re, json, pickle, warnings, inspect
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set
from collections import defaultdict
from datetime import datetime
import pandas as pd
import traceback

# PostgreSQLマネージャーをインポート
try:
    from postgres_manager import PostgreSQLManager
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠ PostgreSQLマネージャーが利用できません（psycopg2をインストールしてください）")

# =====================================================
# ユーティリティ関数
# =====================================================

def safe_getattr(obj: Any, name: str, default: Any = None) -> Any:
    """安全に属性を取得"""
    try:
        return getattr(obj, name, default)
    except Exception:
        return default

def safe_repr(obj: Any, max_len: int = 100) -> str:
    """安全にオブジェクトを文字列化"""
    try:
        s = repr(obj)
        if len(s) > max_len:
            return s[:max_len] + "..."
        return s
    except:
        return f"<{type(obj).__name__}>"

def load_pickle_safe(path: Path) -> Optional[Any]:
    """PKLファイルを安全にロード"""
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        warnings.warn(f"PKL読込失敗 {path.name}: {e}")
        return None

def load_json_safe(path: Path) -> Optional[Any]:
    """JSONファイルを安全にロード"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        warnings.warn(f"JSON読込失敗 {path.name}: {e}")
        return None

# =====================================================
# メインクラス
# =====================================================

class NeuralForecastExtractor:
    """NeuralForecastパラメータ抽出クラス"""
    
    def __init__(self, model_dir: str):
        """
        初期化
        
        Args:
            model_dir: モデルディレクトリのパス
        """
        self.model_dir = Path(model_dir)
        self.output_dir = self.model_dir / "extracted_params"
        self.output_dir.mkdir(exist_ok=True)
        
        # パラメータ格納用
        self.all_params = {}
        self.all_sources = {}
        
        # ファイルパス格納用
        self.pkl_files = []
        self.ckpt_files = []
        self.json_files = []
        self.yaml_files = []
        
        # 結果格納用
        self.df_long = None
        self.df_wide_params = None
        self.df_wide_sources = None
        
        print(f"\n{'='*80}")
        print(f"NeuralForecast パラメータ抽出ツール（PostgreSQL統合版）")
        print(f"{'='*80}")
        print(f"モデルディレクトリ: {self.model_dir}")
        print(f"出力ディレクトリ: {self.output_dir}")
        print(f"{'='*80}\n")
    
    def scan_files(self):
        """ディレクトリをスキャンしてファイルを検出"""
        print("\n[INFO] ファイルスキャン中...")
        
        self.pkl_files = list(self.model_dir.glob("*.pkl"))
        self.ckpt_files = list(self.model_dir.glob("*.ckpt"))
        self.json_files = list(self.model_dir.glob("*.json"))
        self.yaml_files = list(self.model_dir.glob("*.yaml")) + list(self.model_dir.glob("*.yml"))
        
        print(f"  - PKL: {len(self.pkl_files)} files")
        print(f"  - CKPT: {len(self.ckpt_files)} files")
        print(f"  - JSON: {len(self.json_files)} files")
        print(f"  - YAML: {len(self.yaml_files)} files")
    
    def load_model(self):
        """NeuralForecastモデルをロード"""
        try:
            import torch
            from neuralforecast import NeuralForecast
            
            # モデルをロード
            nf = NeuralForecast.load(path=str(self.model_dir))
            self.model = nf.models[0] if nf.models else None
            
            if self.model:
                print(f"✓ モデルロード成功: {type(self.model).__name__}")
                return True
            else:
                print("✗ モデルが見つかりません")
                return False
                
        except Exception as e:
            print(f"✗ モデルロード失敗: {e}")
            traceback.print_exc()
            return False
    
    def extract_model_params(self) -> int:
        """モデルから全パラメータを抽出"""
        print("\n[1/5] NeuralForecastモデルから抽出中...")
        
        if not hasattr(self, 'model') or self.model is None:
            print("  ⚠ モデルがロードされていません")
            return 0
        
        count = 0
        
        try:
            # モデルの直接属性
            for attr_name in dir(self.model):
                if attr_name.startswith('_'):
                    continue
                
                try:
                    attr_value = getattr(self.model, attr_name)
                    
                    # メソッドやモジュールはスキップ
                    if callable(attr_value) and not isinstance(attr_value, type):
                        continue
                    if isinstance(attr_value, (type(torch.nn.Module), torch.nn.ModuleList)):
                        continue
                    
                    param_key = f"model.{attr_name}"
                    self.all_params[param_key] = safe_repr(attr_value, max_len=1000)
                    self.all_sources[param_key] = "model.getattr"
                    count += 1
                    
                except Exception:
                    continue
            
            # __dict__からも抽出
            if hasattr(self.model, '__dict__'):
                for key, value in self.model.__dict__.items():
                    if key.startswith('_'):
                        continue
                    
                    param_key = f"model.{key}"
                    if param_key not in self.all_params:
                        self.all_params[param_key] = safe_repr(value, max_len=1000)
                        self.all_sources[param_key] = "model.__dict__"
                        count += 1
            
            # hparamsから抽出
            if hasattr(self.model, 'hparams'):
                hparams = self.model.hparams
                if isinstance(hparams, dict):
                    for key, value in hparams.items():
                        param_key = f"model.hparams.{key}"
                        self.all_params[param_key] = safe_repr(value, max_len=1000)
                        self.all_sources[param_key] = "model.hparams"
                        count += 1
                elif hasattr(hparams, '__dict__'):
                    for key, value in hparams.__dict__.items():
                        if not key.startswith('_'):
                            param_key = f"model.hparams.{key}"
                            self.all_params[param_key] = safe_repr(value, max_len=1000)
                            self.all_sources[param_key] = "model.hparams"
                            count += 1
            
            print(f"  抽出: {count} parameters")
            
            # 即座に保存
            self._save_step_results("model", count)
            
        except Exception as e:
            print(f"  ✗ エラー: {e}")
            traceback.print_exc()
        
        return count
    
    def extract_pkl_params(self) -> int:
        """PKLファイルから全パラメータを抽出"""
        print("\n[2/5] PKLファイルから抽出中...")
        
        count = 0
        
        for pkl_file in self.pkl_files:
            try:
                data = load_pickle_safe(pkl_file)
                if data is None:
                    continue
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        param_key = f"pkl.{pkl_file.stem}.{key}"
                        self.all_params[param_key] = safe_repr(value, max_len=1000)
                        self.all_sources[param_key] = f"pkl.{pkl_file.name}"
                        count += 1
                else:
                    param_key = f"pkl.{pkl_file.stem}"
                    self.all_params[param_key] = safe_repr(data, max_len=1000)
                    self.all_sources[param_key] = f"pkl.{pkl_file.name}"
                    count += 1
                    
            except Exception as e:
                print(f"  ⚠ {pkl_file.name}: {e}")
                continue
        
        print(f"  抽出: {count} parameters")
        self._save_step_results("pkl", count)
        return count
    
    def extract_ckpt_params(self) -> int:
        """CKPTファイルから全パラメータを抽出"""
        print("\n[3/5] CKPTファイルから抽出中...")
        
        count = 0
        
        try:
            import torch
        except ImportError:
            print("  ⚠ PyTorchがインストールされていません")
            return count
        
        for ckpt_file in self.ckpt_files:
            try:
                checkpoint = torch.load(ckpt_file, map_location='cpu', weights_only=False)
                
                if isinstance(checkpoint, dict):
                    for key, value in checkpoint.items():
                        if key == 'state_dict':
                            continue  # 重みは除外
                        
                        param_key = f"ckpt.{ckpt_file.stem}.{key}"
                        self.all_params[param_key] = safe_repr(value, max_len=1000)
                        self.all_sources[param_key] = f"ckpt.{ckpt_file.name}"
                        count += 1
                        
            except Exception as e:
                print(f"  ⚠ {ckpt_file.name}: {e}")
                continue
        
        print(f"  抽出: {count} parameters")
        self._save_step_results("ckpt", count)
        return count
    
    def extract_json_params(self) -> int:
        """JSONファイルから全パラメータを抽出"""
        print("\n[4/5] JSONファイルから抽出中...")
        
        count = 0
        
        for json_file in self.json_files:
            try:
                data = load_json_safe(json_file)
                if data is None:
                    continue
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        param_key = f"json.{json_file.stem}.{key}"
                        self.all_params[param_key] = safe_repr(value, max_len=1000)
                        self.all_sources[param_key] = f"json.{json_file.name}"
                        count += 1
                else:
                    param_key = f"json.{json_file.stem}"
                    self.all_params[param_key] = safe_repr(data, max_len=1000)
                    self.all_sources[param_key] = f"json.{json_file.name}"
                    count += 1
                    
            except Exception as e:
                print(f"  ⚠ {json_file.name}: {e}")
                continue
        
        print(f"  抽出: {count} parameters")
        self._save_step_results("json", count)
        return count
    
    def extract_yaml_params(self) -> int:
        """YAMLファイルから全パラメータを抽出"""
        print("\n[5/5] YAMLファイルから抽出中...")
        
        count = 0
        
        try:
            import yaml
        except ImportError:
            print("  ⚠ PyYAMLがインストールされていません")
            return count
        
        for yaml_file in self.yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                if data is None:
                    continue
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        param_key = f"yaml.{yaml_file.stem}.{key}"
                        self.all_params[param_key] = safe_repr(value, max_len=1000)
                        self.all_sources[param_key] = f"yaml.{yaml_file.name}"
                        count += 1
                else:
                    param_key = f"yaml.{yaml_file.stem}"
                    self.all_params[param_key] = safe_repr(data, max_len=1000)
                    self.all_sources[param_key] = f"yaml.{yaml_file.name}"
                    count += 1
                    
            except Exception as e:
                print(f"  ⚠ {yaml_file.name}: {e}")
                continue
        
        print(f"  抽出: {count} parameters")
        self._save_step_results("yaml", count)
        return count
    
    def _categorize_parameters(self):
        """パラメータをカテゴリに分類"""
        categorized = defaultdict(dict)
        
        for key, value in self.all_params.items():
            # カテゴリを判定
            if key.startswith('model.hparams.'):
                category = 'D_hparams'
            elif key.startswith('model.'):
                category = 'A_model'
            elif key.startswith('pkl.configuration.'):
                category = 'C_config'
            elif key.startswith('pkl.'):
                category = 'F_pkl'
            elif key.startswith('ckpt.'):
                category = 'G_ckpt'
            elif key.startswith('json.'):
                category = 'H_json'
            elif key.startswith('yaml.'):
                category = 'I_yaml'
            else:
                category = 'Z_other'
            
            categorized[category][key] = value
        
        return categorized
    
    def create_dataframes(self):
        """DataFrameを作成"""
        print("\n[INFO] DataFrameを作成中...")
        
        # 縦持ち形式
        rows = []
        for key, value in self.all_params.items():
            # カテゴリを判定
            if key.startswith('model.hparams.'):
                category = 'D_hparams'
            elif key.startswith('model.'):
                category = 'A_model'
            elif key.startswith('pkl.configuration.'):
                category = 'C_config'
            elif key.startswith('pkl.'):
                category = 'F_pkl'
            elif key.startswith('ckpt.'):
                category = 'G_ckpt'
            elif key.startswith('json.'):
                category = 'H_json'
            elif key.startswith('yaml.'):
                category = 'I_yaml'
            else:
                category = 'Z_other'
            
            rows.append({
                'Category': category,
                'Parameter': key,
                'Value': value,
                'Source': self.all_sources.get(key, 'unknown')
            })
        
        self.df_long = pd.DataFrame(rows)
        
        # 横持ち形式（値）
        wide_params = {row['Parameter']: row['Value'] for row in rows}
        self.df_wide_params = pd.DataFrame([wide_params])
        
        # 横持ち形式（ソース）
        wide_sources = {row['Parameter']: row['Source'] for row in rows}
        self.df_wide_sources = pd.DataFrame([wide_sources])
        
        print(f"  ✓ 縦持ちDataFrame: {len(self.df_long)} rows")
        print(f"  ✓ 横持ちDataFrame: {len(wide_params)} columns")
    
    def save_all_to_files(self):
        """全データをファイルに保存"""
        print("\n[INFO] ファイルに保存中...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSVファイル
        csv_long = self.output_dir / f"params_long_{timestamp}.csv"
        csv_wide = self.output_dir / f"params_wide_{timestamp}.csv"
        csv_sources = self.output_dir / f"params_sources_{timestamp}.csv"
        
        self.df_long.to_csv(csv_long, index=False, encoding='utf-8-sig')
        self.df_wide_params.to_csv(csv_wide, index=False, encoding='utf-8-sig')
        self.df_wide_sources.to_csv(csv_sources, index=False, encoding='utf-8-sig')
        
        print(f"  ✓ CSV (縦持ち): {csv_long.name}")
        print(f"  ✓ CSV (横持ち値): {csv_wide.name}")
        print(f"  ✓ CSV (横持ちソース): {csv_sources.name}")
        
        # Excelファイル
        try:
            excel_file = self.output_dir / f"params_all_{timestamp}.xlsx"
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                self.df_long.to_excel(writer, sheet_name='All_Parameters', index=False)
                self.df_wide_params.T.to_excel(writer, sheet_name='Wide_Parameters')
                self.df_wide_sources.T.to_excel(writer, sheet_name='Wide_Sources')
            print(f"  ✓ Excel: {excel_file.name}")
        except Exception as e:
            print(f"  ⚠ Excel保存失敗: {e}")
        
        # JSONファイル（生データ）
        json_file = self.output_dir / f"params_raw_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'params': self.all_params,
                'sources': self.all_sources,
                'timestamp': timestamp
            }, f, ensure_ascii=False, indent=2)
        print(f"  ✓ JSON (生データ): {json_file.name}")
    
    def _save_step_results(self, step_name: str, count: int):
        """ステップごとの結果を個別ファイルに保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        step_file = self.output_dir / f"step_{step_name}_{timestamp}.json"
        
        step_params = {k: v for k, v in self.all_params.items() if step_name in k or k.startswith(step_name)}
        step_sources = {k: v for k, v in self.all_sources.items() if k in step_params}
        
        with open(step_file, 'w', encoding='utf-8') as f:
            json.dump({
                'step': step_name,
                'count': count,
                'params': step_params,
                'sources': step_sources,
                'timestamp': timestamp
            }, f, ensure_ascii=False, indent=2)
        
        print(f"    → 保存: {step_file.name}")
    
    def save_to_postgres(self, db_config: Dict[str, Any] = None) -> bool:
        """PostgreSQLにデータを保存"""
        if not POSTGRES_AVAILABLE:
            print("\n⚠ PostgreSQL機能が利用できません")
            return False
        
        if self.df_long is None:
            print("\n⚠ DataFrameが作成されていません")
            return False
        
        try:
            with PostgreSQLManager(db_config) as db:
                table_mapping = db.save_dataframe_to_postgres(self.df_long)
                
                # テーブルマッピングを保存
                mapping_file = self.output_dir / "postgres_table_mapping.json"
                with open(mapping_file, 'w', encoding='utf-8') as f:
                    json.dump(table_mapping, f, ensure_ascii=False, indent=2)
                print(f"\n✓ テーブルマッピング保存: {mapping_file.name}")
                
                return True
                
        except Exception as e:
            print(f"\n✗ PostgreSQL保存失敗: {e}")
            traceback.print_exc()
            return False
    
    def run_full_extraction(self, save_to_postgres: bool = False, db_config: Dict[str, Any] = None):
        """完全抽出を実行"""
        print("\n" + "="*80)
        print("完全抽出を開始")
        print("="*80)
        
        # ステップ1: ファイルスキャン
        self.scan_files()
        
        # ステップ2: モデルロード
        self.load_model()
        
        # ステップ3: 各種パラメータ抽出
        self.extract_model_params()
        self.extract_pkl_params()
        self.extract_ckpt_params()
        self.extract_json_params()
        self.extract_yaml_params()
        
        # ステップ4: DataFrame作成
        self.create_dataframes()
        
        # ステップ5: ファイル保存
        self.save_all_to_files()
        
        # ステップ6: PostgreSQL保存
        if save_to_postgres:
            self.save_to_postgres(db_config)
        
        print("\n" + "="*80)
        print(f"✓ 完全抽出完了: 総パラメータ数 {len(self.all_params)}")
        print(f"✓ 出力ディレクトリ: {self.output_dir}")
        print("="*80 + "\n")
        
        return {
            'df_long': self.df_long,
            'df_wide_params': self.df_wide_params,
            'df_wide_sources': self.df_wide_sources,
            'all_params': self.all_params,
            'all_sources': self.all_sources,
            'output_dir': self.output_dir
        }

# =====================================================
# ユーティリティ関数（DataFrameフィルタ等）
# =====================================================

def filter_params_by_category(df_long: pd.DataFrame, category_keyword: str) -> pd.DataFrame:
    """カテゴリでフィルタ"""
    mask = df_long['Category'].str.contains(category_keyword, case=False, na=False)
    return df_long[mask].copy()

def search_params(df_long: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """キーワードでパラメータを検索"""
    mask = df_long['Parameter'].str.contains(keyword, case=False, na=False)
    return df_long[mask].copy()

def get_param_value(df_long: pd.DataFrame, param_name: str) -> Any:
    """特定パラメータの値を取得"""
    matches = df_long[df_long['Parameter'] == param_name]
    if len(matches) > 0:
        return matches.iloc[0]['Value']
    
    # 部分一致で検索
    matches = df_long[df_long['Parameter'].str.contains(param_name, case=False, na=False)]
    if len(matches) > 0:
        return matches.iloc[0]['Value']
    
    return None

# =====================================================
# メイン実行
# =====================================================

if __name__ == "__main__":
    # モデルディレクトリを指定
    MODEL_DIR = r"C:\Users\hashimoto.ryohei\Downloads\zip\unzipped_model\model\dir(data_long)_parent_dir(N_features)_loto(bingo5)_model(AutoDilatedRNN)_N(1)_unique_id(N7)_h(1)_loss(HuberLoss())_local_scaler_type(robust-iqr)_num(10000)_freq(D)_num_samples(40)_backend(optuna)_val_rate(6)_cols(32)_rows(1000)"
    
    # 抽出実行
    extractor = NeuralForecastExtractor(MODEL_DIR)
    results = extractor.run_full_extraction(
        save_to_postgres=True  # PostgreSQLに保存する場合はTrue
    )
    
    # 結果を表示
    df_long = results['df_long']
    print("\n" + "="*80)
    print("抽出結果サマリー")
    print("="*80)
    print(f"総パラメータ数: {len(df_long)}")
    print(f"\nカテゴリ別パラメータ数:")
    for category, count in df_long['Category'].value_counts().sort_index().items():
        print(f"  {category}: {count}")
    print("="*80)
