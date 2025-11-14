"""
NeuralForecast Model Analyzer v2
4つの基本ファイルからモデルを完全分析

使用方法:
    python neuralforecast_analyzer_v2.py

または:
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
    analyzer = NeuralForecastAnalyzer("path/to/model")
    results = analyzer.run_full_analysis()
"""

import sys
from pathlib import Path
import hashlib
import pandas as pd
import pickle
import torch
import numpy as np
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# 既存モジュールのインポート
try:
    from postgres_manager import PostgreSQLManager
    from db_config import DB_CONFIG
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("⚠ PostgreSQL機能が無効です（psycopg2が見つかりません）")


class NeuralForecastAnalyzer:
    """
    NeuralForecastモデルの完全分析システム
    4つの基本ファイルのみを使用:
    - alias_to_model.pkl
    - configuration.pkl
    - dataset.pkl
    - *.ckpt
    """
    
    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)
        self.model_dir_hash = self._compute_dir_hash()
        
        # ファイルパス
        self.alias_path = None
        self.config_path = None
        self.dataset_path = None
        self.ckpt_path = None
        
        # ロードしたデータ
        self.alias_data = None
        self.config_data = None
        self.dataset_data = None
        self.ckpt_data = None
        
        # 分析結果
        self.results = {}
        
    def _compute_dir_hash(self) -> str:
        """ディレクトリパスのハッシュを計算"""
        return hashlib.sha256(str(self.model_dir.resolve()).encode()).hexdigest()
    
    def find_and_load_files(self) -> bool:
        """4つの基本ファイルを検索してロード"""
        print("\n" + "="*80)
        print("ファイル検索とロード")
        print("="*80)
        
        # alias_to_model.pkl
        alias_files = list(self.model_dir.glob("*alias*.pkl"))
        if not alias_files:
            print("✗ alias_to_model.pkl が見つかりません")
            return False
        self.alias_path = alias_files[0]
        print(f"✓ Alias file: {self.alias_path.name}")
        
        # configuration.pkl
        config_files = list(self.model_dir.glob("*config*.pkl"))
        if not config_files:
            print("✗ configuration.pkl が見つかりません")
            return False
        self.config_path = config_files[0]
        print(f"✓ Config file: {self.config_path.name}")
        
        # dataset.pkl
        dataset_files = list(self.model_dir.glob("dataset*.pkl"))
        if not dataset_files:
            print("✗ dataset.pkl が見つかりません")
            return False
        self.dataset_path = dataset_files[0]
        print(f"✓ Dataset file: {self.dataset_path.name}")
        
        # *.ckpt
        ckpt_files = list(self.model_dir.glob("*.ckpt"))
        if not ckpt_files:
            print("✗ *.ckpt が見つかりません")
            return False
        self.ckpt_path = ckpt_files[0]
        print(f"✓ Checkpoint file: {self.ckpt_path.name}")
        
        # ロード実行
        try:
            with open(self.alias_path, 'rb') as f:
                self.alias_data = pickle.load(f)
            print("  → Alias data loaded")
            
            with open(self.config_path, 'rb') as f:
                self.config_data = pickle.load(f)
            print("  → Config data loaded")
            
            with open(self.dataset_path, 'rb') as f:
                self.dataset_data = pickle.load(f)
            print("  → Dataset data loaded")
            
            self.ckpt_data = torch.load(self.ckpt_path, map_location='cpu', weights_only=False)
            print("  → Checkpoint data loaded")
            
            return True
            
        except Exception as e:
            print(f"✗ ファイルロードエラー: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def extract_model_profile(self) -> pd.DataFrame:
        """レイヤー1-1: モデルプロファイル抽出"""
        print("\n[1/8] モデルプロファイル抽出中...")
        
        # alias_dataから基本情報
        model_alias = list(self.alias_data.keys())[0] if self.alias_data else "Unknown"
        model_class = str(self.alias_data.get(model_alias, "Unknown"))
        
        # config_dataから詳細
        config = self.config_data.get(model_alias, {})
        
        # ハイパーパラメータを抽出
        hyperparams = {}
        for key, value in config.items():
            if not key.startswith('_') and not callable(value):
                try:
                    # JSON serializable チェック
                    json.dumps(value)
                    hyperparams[key] = value
                except:
                    hyperparams[key] = str(value)[:100]  # 長すぎる場合は切り詰め
        
        # モデルオブジェクトからパラメータ数を取得
        total_params = 0
        trainable_params = 0
        if 'model' in config and hasattr(config['model'], 'parameters'):
            for p in config['model'].parameters():
                params = p.numel()
                total_params += params
                if p.requires_grad:
                    trainable_params += params
        
        data = {
            'model_dir_hash': [self.model_dir_hash],
            'model_alias': [model_alias],
            'model_class': [model_class.split("'")[1] if "'" in model_class else model_class],
            'h': [hyperparams.get('h', None)],
            'input_size': [hyperparams.get('input_size', None)],
            'freq': [hyperparams.get('freq', None)],
            'total_params': [total_params],
            'trainable_params': [trainable_params],
            'hyperparameters': [json.dumps(hyperparams, ensure_ascii=False)]
        }
        
        df = pd.DataFrame(data)
        print(f"  ✓ モデル: {model_alias}, パラメータ数: {total_params:,}")
        
        self.results['model_profile'] = df
        return df
    
    # 既存の extract_dataset_profile を丸ごと置換
    def extract_dataset_profile(self):
        print("\n[2/8] データセットプロファイル抽出中.")
        ds = self._normalize_dataset(self.dataset_data)

        n_series   = ds.get('n_series')
        n_temporal = ds.get('n_temporal')
        stat       = ds.get('stat', {}) or {}
        Y_df       = ds.get('Y_df')

        mean_val = stat.get('mean')
        std_val  = stat.get('std')
        min_val  = stat.get('min')
        max_val  = stat.get('max')
        zero_rate = 0.0
        missing_rate = 0.0

        if isinstance(Y_df, pd.DataFrame):
            if n_series is None:
                n_series = int(Y_df['unique_id'].nunique()) if 'unique_id' in Y_df.columns else 1
            if n_temporal is None:
                n_temporal = int(len(Y_df))

            if 'y' in Y_df.columns:
                zero_rate    = float((Y_df['y'] == 0).mean())
                missing_rate = float(Y_df['y'].isna().mean())
                # stat が無い場合は最小限の統計をその場で補完
                if mean_val is None: mean_val = float(Y_df['y'].mean())
                if std_val  is None: std_val  = float(Y_df['y'].std(ddof=0))
                if min_val  is None: min_val  = float(Y_df['y'].min())
                if max_val  is None: max_val  = float(Y_df['y'].max())

        data = {
            'model_dir_hash': [self.model_dir_hash],
            'n_series': [n_series],
            'n_temporal': [n_temporal],
            'total_observations': [n_series * n_temporal if n_series and n_temporal else None],
            'mean_value': [mean_val],
            'std_value': [std_val],
            'min_value': [min_val],
            'max_value': [max_val],
            'zero_rate': [zero_rate],
            'missing_rate': [missing_rate],
            'statistics': [json.dumps(stat, ensure_ascii=False)]
        }
        df = pd.DataFrame(data)
        print(f"  ✓ 系列数: {n_series}, 観測数: {n_temporal}")
        self.results['dataset_profile'] = df
        return df

    # NeuralForecastAnalyzer クラス内に追記（クラスメソッドとして）
    def _normalize_dataset(self, ds_obj):
        """
        TimeSeriesDataset / DataFrame / dict を共通辞書に正規化して返す。
        返却キー:
        - 'Y_df'        : pd.DataFrame|None（unique_id, ds, y など）
        - 'stat'        : dict|{}
        - 'n_series'    : int|None
        - 'n_temporal'  : int|None（レコード数）
        """
        out = {}

        # 1) そのまま dict
        if isinstance(ds_obj, dict):
            out.update(ds_obj)

        # 2) まるごと DataFrame
        elif isinstance(ds_obj, pd.DataFrame):
            out['Y_df'] = ds_obj

        # 3) クラスオブジェクト（TimeSeriesDataset 等）
        else:
            for cand in ('Y_df', 'df', 'data'):
                if hasattr(ds_obj, cand):
                    val = getattr(ds_obj, cand)
                    if isinstance(val, pd.DataFrame):
                        out['Y_df'] = val
                        break
            if hasattr(ds_obj, 'stat') and isinstance(getattr(ds_obj, 'stat'), dict):
                out['stat'] = getattr(ds_obj, 'stat')

        # 推定補完
        Y_df = out.get('Y_df')
        if isinstance(Y_df, pd.DataFrame):
            out.setdefault('n_series', int(Y_df['unique_id'].nunique()) if 'unique_id' in Y_df.columns else 1)
            out.setdefault('n_temporal', int(len(Y_df)))

        # stat が dict 以外なら空dict
        if not isinstance(out.get('stat', {}), dict):
            out['stat'] = {}

        return out

    def extract_training_state(self) -> pd.DataFrame:
        """レイヤー1-3: 学習状態抽出"""
        print("\n[3/8] 学習状態抽出中...")
        
        epoch = self.ckpt_data.get('epoch', 0)
        global_step = self.ckpt_data.get('global_step', 0)
        
        # Early stopping判定
        early_stopped = False
        if 'callbacks' in self.ckpt_data:
            callbacks = self.ckpt_data['callbacks']
            if isinstance(callbacks, dict):
                for cb_name, cb_state in callbacks.items():
                    if 'early_stop' in cb_name.lower():
                        early_stopped = cb_state.get('stopped_epoch', 0) > 0
        
        # 最終学習率
        final_lr = None
        if 'optimizer_states' in self.ckpt_data:
            opt_states = self.ckpt_data['optimizer_states']
            if opt_states and len(opt_states) > 0:
                first_opt = opt_states[0]
                if 'param_groups' in first_opt:
                    final_lr = first_opt['param_groups'][0].get('lr')
        
        # チェックポイントサイズ
        ckpt_size_mb = self.ckpt_path.stat().st_size / (1024 * 1024)
        
        data = {
            'model_dir_hash': [self.model_dir_hash],
            'epoch': [epoch],
            'global_step': [global_step],
            'early_stopped': [early_stopped],
            'final_lr': [final_lr],
            'checkpoint_size_mb': [ckpt_size_mb],
            'optimizer_state': [json.dumps({})]  # 詳細は省略
        }
        
        df = pd.DataFrame(data)
        print(f"  ✓ エポック: {epoch}, ステップ: {global_step}, Early stop: {early_stopped}")
        
        self.results['training_state'] = df
        return df
    
    def analyze_weight_statistics(self) -> pd.DataFrame:
        """レイヤー2-2: 重み統計量分析"""
        print("\n[4/8] 重み統計量分析中...")
        
        state_dict = self.ckpt_data.get('state_dict', {})
        
        rows = []
        for layer_name, weights in state_dict.items():
            if not isinstance(weights, torch.Tensor):
                continue
            
            # 統計量計算
            weights_np = weights.detach().cpu().numpy().flatten()
            
            mean_val = float(weights_np.mean())
            std_val = float(weights_np.std())
            min_val = float(weights_np.min())
            max_val = float(weights_np.max())
            
            # ノルム
            l1_norm = float(np.abs(weights_np).sum())
            l2_norm = float(np.sqrt((weights_np ** 2).sum()))
            
            # スパース性
            sparsity = float((weights_np == 0).mean())
            
            # 外れ値比率 (|value| > 3*std)
            if std_val > 0:
                outlier_ratio = float((np.abs(weights_np) > 3 * std_val).mean())
            else:
                outlier_ratio = 0.0
            
            # 健全性スコア
            health_score = 10
            if outlier_ratio > 0.05:
                health_score -= 3
            if sparsity > 0.9:
                health_score -= 2
            if abs(mean_val) > 1.0:
                health_score -= 2
            if std_val < 0.01 or std_val > 10:
                health_score -= 2
            health_score = max(0, health_score)
            
            # 層タイプ推定
            layer_type = "Unknown"
            if 'conv' in layer_name.lower():
                layer_type = "Conv"
            elif 'linear' in layer_name.lower() or 'fc' in layer_name.lower():
                layer_type = "Linear"
            elif 'lstm' in layer_name.lower() or 'gru' in layer_name.lower():
                layer_type = "RNN"
            elif 'norm' in layer_name.lower():
                layer_type = "Normalization"
            elif 'bias' in layer_name.lower():
                layer_type = "Bias"
            
            rows.append({
                'model_dir_hash': self.model_dir_hash,
                'layer_name': layer_name,
                'layer_type': layer_type,
                'param_count': len(weights_np),
                'mean_val': mean_val,
                'std_val': std_val,
                'min_val': min_val,
                'max_val': max_val,
                'l1_norm': l1_norm,
                'l2_norm': l2_norm,
                'sparsity': sparsity,
                'outlier_ratio': outlier_ratio,
                'health_score': health_score
            })
        
        df = pd.DataFrame(rows)
        if len(df) > 0:
            avg_health = df['health_score'].mean()
            print(f"  ✓ 解析層数: {len(df)}, 平均健全性スコア: {avg_health:.1f}/10")
        else:
            print("  ⚠ 解析可能な層が見つかりませんでした")
        
        self.results['weight_statistics'] = df
        return df
    
    def analyze_model_complexity(self) -> pd.DataFrame:
        """レイヤー2-3: モデル複雑度分析"""
        print("\n[5/8] モデル複雑度分析中...")
        
        model_profile = self.results.get('model_profile')
        if model_profile is None or len(model_profile) == 0:
            return pd.DataFrame()
        
        total_params = model_profile['total_params'].iloc[0]
        h = model_profile['h'].iloc[0] or 1
        input_size = model_profile['input_size'].iloc[0] or 1
        
        # パラメータ効率
        param_efficiency = total_params / (h * input_size)
        
        # 深さ・幅（推定）
        weight_stats = self.results.get('weight_statistics')
        depth = len(weight_stats) if weight_stats is not None else 0
        width = int(total_params ** 0.5) if total_params > 0 else 0
        
        # メモリ推定 (4 bytes per float32 param)
        memory_mb = (total_params * 4) / (1024 * 1024)
        
        # 複雑度カテゴリ
        if total_params < 100000:
            complexity_category = 'light'
        elif total_params < 1000000:
            complexity_category = 'medium'
        else:
            complexity_category = 'heavy'
        
        data = {
            'model_dir_hash': [self.model_dir_hash],
            'param_efficiency': [param_efficiency],
            'depth': [depth],
            'width': [width],
            'memory_mb': [memory_mb],
            'complexity_category': [complexity_category]
        }
        
        df = pd.DataFrame(data)
        print(f"  ✓ 複雑度: {complexity_category}, メモリ: {memory_mb:.1f} MB, 効率: {param_efficiency:.1f}")
        
        self.results['model_complexity'] = df
        return df
    
    def analyze_parameter_sensitivity(self) -> pd.DataFrame:
        """レイヤー2-1: パラメータ感度分析"""
        print("\n[6/8] パラメータ感度分析中...")
        
        model_profile = self.results.get('model_profile')
        if model_profile is None or len(model_profile) == 0:
            return pd.DataFrame()
        
        hyperparams = json.loads(model_profile['hyperparameters'].iloc[0])
        
        # 重要度マッピング
        importance_map = {
            'h': (10, 'model'),
            'input_size': (9, 'model'),
            'hidden_size': (8, 'model'),
            'num_layers': (8, 'model'),
            'learning_rate': (7, 'training'),
            'batch_size': (6, 'training'),
            'max_steps': (5, 'training'),
            'max_epochs': (5, 'training'),
            'dropout': (6, 'model'),
            'scaler': (5, 'data'),
            'loss': (9, 'training'),
            'kernel_size': (7, 'model'),
            'dilations': (7, 'model')
        }
        
        rows = []
        for param_name, param_value in hyperparams.items():
            importance, category = importance_map.get(param_name, (3, 'other'))
            
            rows.append({
                'model_dir_hash': self.model_dir_hash,
                'parameter_name': param_name,
                'parameter_value': str(param_value)[:200],  # 長すぎる場合は切り詰め
                'importance_score': importance,
                'category': category
            })
        
        df = pd.DataFrame(rows)
        if len(df) > 0:
            high_importance = len(df[df['importance_score'] >= 8])
            print(f"  ✓ パラメータ数: {len(df)}, 高重要度(8+): {high_importance}")
        
        self.results['parameter_sensitivity'] = df
        return df
    
    def diagnose_model_health(self) -> Dict:
        """レイヤー4-1: モデル健全性診断"""
        print("\n[7/8] モデル健全性診断中...")
        
        weight_stats = self.results.get('weight_statistics')
        training_state = self.results.get('training_state')
        model_complexity = self.results.get('model_complexity')
        
        # 総合スコア計算
        overall_score = 50.0  # ベースライン
        
        # 重みの健全性
        if weight_stats is not None and len(weight_stats) > 0:
            avg_health = weight_stats['health_score'].mean()
            overall_score += (avg_health - 5) * 5  # -25 to +25
            
            if avg_health >= 8:
                weight_health = 'good'
            elif avg_health >= 5:
                weight_health = 'warning'
            else:
                weight_health = 'bad'
        else:
            weight_health = 'unknown'
            overall_score -= 10
        
        # 収束状態
        convergence_status = 'unknown'
        if training_state is not None and len(training_state) > 0:
            early_stopped = training_state['early_stopped'].iloc[0]
            convergence_status = 'early_stopped' if early_stopped else 'completed'
            if early_stopped:
                overall_score += 10  # Early stopping は良いサイン
        
        # 推奨事項生成
        recommendations = []
        
        if weight_health == 'bad':
            recommendations.append("重みの健全性が低いです。learning_rateを50%削減してください。")
        elif weight_health == 'warning':
            recommendations.append("一部の層で重みの健全性が低下しています。学習率の調整を検討してください。")
        
        if model_complexity is not None and len(model_complexity) > 0:
            complexity = model_complexity['complexity_category'].iloc[0]
            if complexity == 'heavy':
                recommendations.append("モデルが重すぎます。hidden_sizeまたはnum_layersを70%に削減してください。")
        
        if convergence_status == 'completed':
            recommendations.append("Early stoppingが発動しませんでした。max_stepsを増やすか、patience値を調整してください。")
        
        if not recommendations:
            recommendations.append("モデルは健全な状態です。現在の設定を維持してください。")
        
        diagnosis = {
            'model_dir_hash': self.model_dir_hash,
            'overall_score': min(100, max(0, overall_score)),
            'weight_health': weight_health,
            'convergence_status': convergence_status,
            'recommendations': recommendations
        }
        
        df = pd.DataFrame([diagnosis])
        df['recommendations'] = df['recommendations'].apply(lambda x: json.dumps(x, ensure_ascii=False))
        
        print(f"  ✓ 総合スコア: {overall_score:.1f}/100, 健全性: {weight_health}")
        print(f"  推奨事項: {len(recommendations)} 件")
        
        self.results['model_diagnosis'] = df
        return diagnosis
    
    def generate_optimization_suggestions(self) -> pd.DataFrame:
        """レイヤー4-2: 最適化提案"""
        print("\n[8/8] 最適化提案生成中...")
        
        diagnosis = self.results.get('model_diagnosis')
        model_profile = self.results.get('model_profile')
        model_complexity = self.results.get('model_complexity')
        
        if diagnosis is None or model_profile is None:
            return pd.DataFrame()
        
        hyperparams = json.loads(model_profile['hyperparameters'].iloc[0])
        
        suggestions = []
        
        # 複雑度に基づく提案
        if model_complexity is not None and len(model_complexity) > 0:
            complexity = model_complexity['complexity_category'].iloc[0]
            
            if complexity == 'heavy':
                if 'hidden_size' in hyperparams:
                    current = hyperparams['hidden_size']
                    suggestions.append({
                        'category': 'parameter_reduction',
                        'parameter_name': 'hidden_size',
                        'current_value': str(current),
                        'suggested_value': str(int(current * 0.7)),
                        'expected_impact': 'メモリ削減30%, 速度向上20%',
                        'priority': 4
                    })
                
                if 'num_layers' in hyperparams:
                    current = hyperparams['num_layers']
                    if current > 3:
                        suggestions.append({
                            'category': 'parameter_reduction',
                            'parameter_name': 'num_layers',
                            'current_value': str(current),
                            'suggested_value': str(max(2, current - 1)),
                            'expected_impact': 'メモリ削減, 学習速度向上',
                            'priority': 3
                        })
        
        # 健全性に基づく提案
        weight_health = diagnosis['weight_health'].iloc[0]
        if weight_health == 'warning' or weight_health == 'bad':
            if 'learning_rate' in hyperparams:
                current_lr = hyperparams['learning_rate']
                suggestions.append({
                    'category': 'learning_stabilization',
                    'parameter_name': 'learning_rate',
                    'current_value': str(current_lr),
                    'suggested_value': str(current_lr * 0.5),
                    'expected_impact': '学習安定化, 重み健全性向上',
                    'priority': 5
                })
        
        # input_size の提案
        if 'input_size' in hyperparams:
            input_size = hyperparams['input_size']
            seasonality = hyperparams.get('seasonality', 7)
            
            if input_size < seasonality * 2:
                suggestions.append({
                    'category': 'model_capacity',
                    'parameter_name': 'input_size',
                    'current_value': str(input_size),
                    'suggested_value': str(seasonality * 3),
                    'expected_impact': '季節性パターンの捕捉向上',
                    'priority': 4
                })
        
        # batch_size の提案
        if 'batch_size' in hyperparams and model_complexity is not None:
            batch_size = hyperparams['batch_size']
            if batch_size < 32:
                suggestions.append({
                    'category': 'learning_stabilization',
                    'parameter_name': 'batch_size',
                    'current_value': str(batch_size),
                    'suggested_value': str(min(64, batch_size * 2)),
                    'expected_impact': '学習の安定性向上, 勾配推定の改善',
                    'priority': 3
                })
        
        if not suggestions:
            suggestions.append({
                'category': 'none',
                'parameter_name': 'N/A',
                'current_value': 'N/A',
                'suggested_value': 'N/A',
                'expected_impact': 'モデルは適切に設定されています',
                'priority': 1
            })
        
        df = pd.DataFrame(suggestions)
        df['model_dir_hash'] = self.model_dir_hash
        
        high_priority = len(df[df['priority'] >= 4])
        print(f"  ✓ 提案数: {len(df)}, 高優先度(4+): {high_priority}")
        
        self.results['optimization_suggestions'] = df
        return df
    
    def save_to_postgres(self, db_config: Dict = None):
        """PostgreSQLに保存"""
        if not POSTGRES_AVAILABLE:
            print("\n⚠ PostgreSQL機能が無効です")
            return
        
        print("\n" + "="*80)
        print("PostgreSQLへの保存")
        print("="*80)
        
        config = db_config or DB_CONFIG
        
        try:
            with PostgreSQLManager(config) as db:
                for table_name, df in self.results.items():
                    if df is None or len(df) == 0:
                        continue
                    
                    try:
                        # テーブル名変換
                        pg_table_name = f"nf_{table_name}"
                        
                        # DataFrame を PostgreSQL に挿入
                        columns = [col for col in df.columns if col != 'id']
                        values_list = df[columns].values.tolist()
                        
                        # UPSERT (INSERT ... ON CONFLICT)
                        placeholders = ', '.join(['%s'] * len(columns))
                        columns_str = ', '.join(columns)
                        
                        # model_dir_hash 以外の全カラムを更新対象に
                        update_cols = [col for col in columns if col != 'model_dir_hash']
                        update_str = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_cols])
                        
                        insert_query = f"""
                        INSERT INTO {pg_table_name} ({columns_str})
                        VALUES ({placeholders})
                        ON CONFLICT (model_dir_hash) 
                        DO UPDATE SET {update_str}
                        """
                        
                        for row in values_list:
                            db.cursor.execute(insert_query, row)
                        
                        print(f"  ✓ {pg_table_name}: {len(df)} rows")
                        
                    except Exception as e:
                        print(f"  ✗ {table_name}: {e}")
                
                db.commit()
                print("\n✓ PostgreSQL保存完了")
                
        except Exception as e:
            print(f"\n✗ PostgreSQL保存エラー: {e}")
    
    def save_to_files(self, output_dir: Path):
        """ファイルに保存"""
        print("\n" + "="*80)
        print("ファイルへの保存")
        print("="*80)
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 個別CSV保存
        for table_name, df in self.results.items():
            if df is None or len(df) == 0:
                continue
            
            csv_path = output_dir / f"{table_name}_{timestamp}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            print(f"  ✓ {csv_path.name}")
        
        # 統合Excel保存
        try:
            excel_path = output_dir / f"model_analysis_{timestamp}.xlsx"
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                for table_name, df in self.results.items():
                    if df is not None and len(df) > 0:
                        sheet_name = table_name[:31]  # Excel sheet name limit
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"  ✓ {excel_path.name} (統合Excel)")
        except Exception as e:
            print(f"  ⚠ Excel保存エラー: {e}")
        
        print(f"\n✓ ファイル保存完了: {output_dir}")
    
    def run_full_analysis(self, 
                          save_to_postgres: bool = True,
                          save_to_files: bool = True,
                          output_dir: str = "nf_auto_runs/analysis") -> Dict:
        """完全分析の実行"""
        print("\n" + "="*80)
        print("NeuralForecast モデル完全分析")
        print("="*80)
        print(f"モデルディレクトリ: {self.model_dir}")
        print(f"ディレクトリハッシュ: {self.model_dir_hash[:16]}...")
        
        # ステップ1: ファイルロード
        if not self.find_and_load_files():
            print("\n✗ ファイルロードに失敗しました")
            return {}
        
        # ステップ2-8: 分析実行
        try:
            self.extract_model_profile()
            self.extract_dataset_profile()
            self.extract_training_state()
            self.analyze_weight_statistics()
            self.analyze_model_complexity()
            self.analyze_parameter_sensitivity()
            self.diagnose_model_health()
            self.generate_optimization_suggestions()
            
        except Exception as e:
            print(f"\n✗ 分析エラー: {e}")
            import traceback
            traceback.print_exc()
            return {}
        
        # ステップ9: 保存
        if save_to_postgres and POSTGRES_AVAILABLE:
            try:
                self.save_to_postgres()
            except Exception as e:
                print(f"✗ PostgreSQL保存エラー: {e}")
        
        if save_to_files:
            try:
                self.save_to_files(Path(output_dir))
            except Exception as e:
                print(f"✗ ファイル保存エラー: {e}")
        
        print("\n" + "="*80)
        print("✓ 完全分析完了")
        print("="*80)
        
        # サマリ表示
        print("\n分析結果サマリ:")
        for key, df in self.results.items():
            if df is not None and len(df) > 0:
                print(f"  - {key}: {len(df)} rows")
        
        return self.results


# メイン実行
if __name__ == "__main__":
    # コマンドライン引数からモデルディレクトリを取得
    if len(sys.argv) > 1:
        MODEL_DIR = sys.argv[1]
    else:
        # デフォルトパス（Windowsの長いパス）
        MODEL_DIR = r"C:\Users\hashimoto.ryohei\Downloads\zip\unzipped_model\model\dir(data_long)_parent_dir(N_features)_loto(numbers4)_model(AutoTCN)_N(1)_unique_id(N2)_h(1)_loss(MAE())_local_scaler_type(minmax)_num(10000)_freq(D)_num_samples(40)_backend(optuna)_val_rate(6)_cols(5)_rows(10000)"
    
    # 分析実行
    analyzer = NeuralForecastAnalyzer(MODEL_DIR)
    results = analyzer.run_full_analysis(
        save_to_postgres=True,   # PostgreSQLに保存
        save_to_files=True,       # CSVとExcelに保存
        output_dir="nf_auto_runs/analysis"
    )
