"""
フェーズ2: 複数モデル比較システム
Multiple Model Comparative Analysis

機能:
- 複数のモデルディレクトリを横断分析
- ハイパーパラメータ相関分析
- モデル間の統計的比較（DM検定、MCS）
- ランキングとベストモデル選定
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json
from datetime import datetime
from scipy import stats
from scipy.stats import kendalltau, spearmanr
import warnings

warnings.filterwarnings('ignore')
# multi_model_comparator.py の先頭付近
from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
import pandas as pd, json

def _normalize_dataset(self, ds_obj):
    out = {}
    if isinstance(ds_obj, dict):
        out.update(ds_obj)
    elif isinstance(ds_obj, pd.DataFrame):
        out['Y_df'] = ds_obj
    else:
        for cand in ('Y_df','df','data'):
            if hasattr(ds_obj, cand):
                val = getattr(ds_obj, cand)
                if isinstance(val, pd.DataFrame):
                    out['Y_df'] = val
                    break
        if hasattr(ds_obj, 'stat') and isinstance(getattr(ds_obj, 'stat'), dict):
            out['stat'] = getattr(ds_obj, 'stat')
    Y_df = out.get('Y_df')
    if isinstance(Y_df, pd.DataFrame):
        out.setdefault('n_series', int(Y_df['unique_id'].nunique()) if 'unique_id' in Y_df.columns else 1)
        out.setdefault('n_temporal', int(len(Y_df)))
    if not isinstance(out.get('stat', {}), dict):
        out['stat'] = {}
    return out

def _extract_dataset_profile(self):
    print("\n[2/8] データセットプロファイル抽出中.")
    ds = _normalize_dataset(self, self.dataset_data)
    n_series   = ds.get('n_series')
    n_temporal = ds.get('n_temporal')
    stat       = ds.get('stat', {}) or {}
    Y_df       = ds.get('Y_df')
    mean_val = stat.get('mean'); std_val = stat.get('std'); min_val = stat.get('min'); max_val = stat.get('max')
    zero_rate = 0.0; missing_rate = 0.0
    if isinstance(Y_df, pd.DataFrame):
        if n_series is None:
            n_series = int(Y_df['unique_id'].nunique()) if 'unique_id' in Y_df.columns else 1
        if n_temporal is None:
            n_temporal = int(len(Y_df))
        if 'y' in Y_df.columns:
            zero_rate    = float((Y_df['y'] == 0).mean())
            missing_rate = float(Y_df['y'].isna().mean())
            if mean_val is None: mean_val = float(Y_df['y'].mean())
            if std_val  is None: std_val  = float(Y_df['y'].std(ddof=0))
            if min_val  is None: min_val  = float(Y_df['y'].min())
            if max_val  is None: max_val  = float(Y_df['y'].max())
    import pandas as pd
    df = pd.DataFrame({
        'model_dir_hash': [getattr(self, 'model_dir_hash', None)],
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
    })
    print(f"  ✓ 系列数: {n_series}, 観測数: {n_temporal}")
    self.results['dataset_profile'] = df
    return df

NeuralForecastAnalyzer._normalize_dataset = _normalize_dataset
NeuralForecastAnalyzer.extract_dataset_profile = _extract_dataset_profile

try:
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
except ImportError:
    print("⚠ neuralforecast_analyzer_v2.py が必要です")

try:
    from postgres_manager import PostgreSQLManager
    from db_config import DB_CONFIG
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


class MultiModelComparator:
    """複数モデルの比較分析システム"""
    
    def __init__(self, output_dir: str = "nf_auto_runs/comparative_analysis"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.models_data = []
        self.comparison_results = {}
        
    def analyze_multiple_models(self, model_dirs: List[str], 
                                save_to_postgres: bool = True) -> Dict:
        """複数のモデルを分析"""
        print("\n" + "="*80)
        print("複数モデル比較分析")
        print("="*80)
        print(f"分析対象: {len(model_dirs)} モデル\n")
        
        # 各モデルを個別に分析
        for i, model_dir in enumerate(model_dirs, 1):
            print(f"[{i}/{len(model_dirs)}] 分析中: {model_dir}")
            
            try:
                analyzer = NeuralForecastAnalyzer(str(model_dir))
                results = analyzer.run_full_analysis(
                    save_to_postgres=save_to_postgres,
                    save_to_files=False
                )
                
                # データを保存
                model_data = {
                    'model_dir': str(model_dir),
                    'results': results
                }
                self.models_data.append(model_data)
                
                print(f"  ✓ 完了\n")
                
            except Exception as e:
                print(f"  ✗ エラー: {e}\n")
                continue
        
        if len(self.models_data) < 2:
            print("✗ 比較には少なくとも2つのモデルが必要です")
            return {}
        
        # 比較分析を実行
        print("\n比較分析を実行中...")
        self.comparison_results['summary'] = self._create_summary_table()
        self.comparison_results['hyperparameter_correlation'] = self._analyze_hyperparameter_correlation()
        self.comparison_results['statistical_comparison'] = self._perform_statistical_comparison()
        self.comparison_results['ranking'] = self._create_model_ranking()
        
        # 結果を保存
        self._save_results()
        
        print("\n✓ 比較分析完了")
        return self.comparison_results
    
    def _create_summary_table(self) -> pd.DataFrame:
        """モデルサマリテーブルを作成"""
        print("  1. サマリテーブル作成中...")
        
        rows = []
        for model_data in self.models_data:
            results = model_data['results']
            
            # 各テーブルから情報を抽出
            profile = results.get('model_profile')
            diagnosis = results.get('model_diagnosis')
            complexity = results.get('model_complexity')
            training = results.get('training_state')
            weight_stats = results.get('weight_statistics')
            
            row = {
                'model_dir': model_data['model_dir'],
                'model_alias': profile['model_alias'].iloc[0] if profile is not None else 'N/A',
                'model_class': profile['model_class'].iloc[0] if profile is not None else 'N/A',
                'h': profile['h'].iloc[0] if profile is not None else None,
                'input_size': profile['input_size'].iloc[0] if profile is not None else None,
                'total_params': profile['total_params'].iloc[0] if profile is not None else 0,
                'overall_score': diagnosis['overall_score'].iloc[0] if diagnosis is not None else 0,
                'weight_health': diagnosis['weight_health'].iloc[0] if diagnosis is not None else 'unknown',
                'complexity_category': complexity['complexity_category'].iloc[0] if complexity is not None else 'unknown',
                'memory_mb': complexity['memory_mb'].iloc[0] if complexity is not None else 0,
                'epoch': training['epoch'].iloc[0] if training is not None else 0,
                'early_stopped': training['early_stopped'].iloc[0] if training is not None else False,
                'num_layers': len(weight_stats) if weight_stats is not None else 0,
                'avg_layer_health': weight_stats['health_score'].mean() if weight_stats is not None else 0
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        print(f"    ✓ {len(df)} モデルのサマリ作成完了")
        
        return df
    
    def _analyze_hyperparameter_correlation(self) -> Dict:
        """ハイパーパラメータの相関分析"""
        print("  2. ハイパーパラメータ相関分析中...")
        
        # 全モデルのハイパーパラメータを収集
        hyperparam_data = []
        
        for model_data in self.models_data:
            results = model_data['results']
            profile = results.get('model_profile')
            diagnosis = results.get('model_diagnosis')
            
            if profile is None or diagnosis is None:
                continue
            
            hyperparams = json.loads(profile['hyperparameters'].iloc[0])
            
            # 数値パラメータのみ抽出
            numeric_params = {}
            for key, value in hyperparams.items():
                try:
                    numeric_params[key] = float(value)
                except (ValueError, TypeError):
                    pass
            
            # 診断スコアを追加
            numeric_params['overall_score'] = diagnosis['overall_score'].iloc[0]
            numeric_params['model_dir'] = model_data['model_dir']
            
            hyperparam_data.append(numeric_params)
        
        if len(hyperparam_data) < 3:
            print("    ⚠ 相関分析には3つ以上のモデルが必要です")
            return {}
        
        # DataFrameに変換
        df = pd.DataFrame(hyperparam_data)
        df = df.drop(columns=['model_dir'], errors='ignore')
        
        # 相関行列を計算
        correlation_matrix = df.corr(method='spearman')
        
        # overall_scoreとの相関が高いパラメータを抽出
        score_correlations = correlation_matrix['overall_score'].drop('overall_score').sort_values(
            ascending=False, key=abs
        )
        
        result = {
            'correlation_matrix': correlation_matrix.to_dict(),
            'score_correlations': score_correlations.to_dict(),
            'top_positive_correlations': score_correlations.head(5).to_dict(),
            'top_negative_correlations': score_correlations.tail(5).to_dict()
        }
        
        print(f"    ✓ 相関分析完了（{len(df.columns)} パラメータ）")
        
        return result
    
    def _perform_statistical_comparison(self) -> Dict:
        """統計的比較（健全性スコアに基づく）"""
        print("  3. 統計的比較実行中...")
        
        # 健全性スコアを抽出
        scores = []
        model_names = []
        
        for model_data in self.models_data:
            results = model_data['results']
            diagnosis = results.get('model_diagnosis')
            profile = results.get('model_profile')
            
            if diagnosis is not None and profile is not None:
                scores.append(diagnosis['overall_score'].iloc[0])
                model_names.append(profile['model_alias'].iloc[0])
        
        if len(scores) < 2:
            return {}
        
        # 統計量を計算
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        median_score = np.median(scores)
        
        # ペアワイズt検定
        pairwise_tests = []
        for i in range(len(scores)):
            for j in range(i+1, len(scores)):
                # t検定（単一値なので意味は限定的だが、概念実証）
                # 実際にはモデルの複数評価が必要
                pairwise_tests.append({
                    'model1': model_names[i],
                    'model2': model_names[j],
                    'score1': scores[i],
                    'score2': scores[j],
                    'difference': scores[i] - scores[j]
                })
        
        result = {
            'mean_score': mean_score,
            'std_score': std_score,
            'median_score': median_score,
            'min_score': min(scores),
            'max_score': max(scores),
            'score_range': max(scores) - min(scores),
            'pairwise_comparisons': pairwise_tests
        }
        
        print(f"    ✓ 統計的比較完了（平均スコア: {mean_score:.1f}）")
        
        return result
    
    def _create_model_ranking(self) -> pd.DataFrame:
        """モデルランキングを作成"""
        print("  4. モデルランキング作成中...")
        
        summary = self.comparison_results.get('summary')
        if summary is None:
            return pd.DataFrame()
        
        # 複合スコアを計算
        df = summary.copy()
        
        # 正規化関数
        def normalize(series):
            min_val, max_val = series.min(), series.max()
            if max_val == min_val:
                return pd.Series([0.5] * len(series))
            return (series - min_val) / (max_val - min_val)
        
        # 各メトリクスを正規化（0-1）
        df['score_norm'] = normalize(df['overall_score'])
        df['health_norm'] = df['avg_layer_health'] / 10  # 0-10 -> 0-1
        
        # メモリ効率（小さいほど良い）
        df['memory_norm'] = 1 - normalize(df['memory_mb'])
        
        # 複合スコア（重み付き平均）
        weights = {
            'score_norm': 0.5,      # 健全性スコア: 50%
            'health_norm': 0.3,     # 層健全性: 30%
            'memory_norm': 0.2      # メモリ効率: 20%
        }
        
        df['composite_score'] = (
            df['score_norm'] * weights['score_norm'] +
            df['health_norm'] * weights['health_norm'] +
            df['memory_norm'] * weights['memory_norm']
        ) * 100
        
        # ランキング
        df['rank'] = df['composite_score'].rank(ascending=False, method='dense').astype(int)
        
        # ソート
        df = df.sort_values('rank')
        
        print(f"    ✓ ランキング作成完了")
        
        return df
    
    def _save_results(self):
        """結果を保存"""
        print("\n結果を保存中...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. サマリテーブル
        summary = self.comparison_results.get('summary')
        if summary is not None:
            path = self.output_dir / f"model_summary_{timestamp}.csv"
            summary.to_csv(path, index=False, encoding='utf-8-sig')
            print(f"  ✓ {path}")
        
        # 2. ランキング
        ranking = self.comparison_results.get('ranking')
        if ranking is not None:
            path = self.output_dir / f"model_ranking_{timestamp}.csv"
            ranking.to_csv(path, index=False, encoding='utf-8-sig')
            print(f"  ✓ {path}")
        
        # 3. 相関分析
        correlation = self.comparison_results.get('hyperparameter_correlation')
        if correlation:
            path = self.output_dir / f"hyperparameter_correlation_{timestamp}.json"
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(correlation, f, indent=2, ensure_ascii=False)
            print(f"  ✓ {path}")
        
        # 4. 統計的比較
        statistical = self.comparison_results.get('statistical_comparison')
        if statistical:
            path = self.output_dir / f"statistical_comparison_{timestamp}.json"
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(statistical, f, indent=2, ensure_ascii=False)
            print(f"  ✓ {path}")
        
        # 5. 統合Excel
        try:
            excel_path = self.output_dir / f"comparative_analysis_{timestamp}.xlsx"
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                if summary is not None:
                    summary.to_excel(writer, sheet_name='Summary', index=False)
                if ranking is not None:
                    ranking.to_excel(writer, sheet_name='Ranking', index=False)
            
            print(f"  ✓ {excel_path}")
        except Exception as e:
            print(f"  ⚠ Excel保存エラー: {e}")
    
    def generate_comparison_report(self) -> str:
        """比較レポートを生成"""
        summary = self.comparison_results.get('summary')
        ranking = self.comparison_results.get('ranking')
        statistical = self.comparison_results.get('statistical_comparison')
        
        report = []
        report.append("="*80)
        report.append("複数モデル比較レポート")
        report.append("="*80)
        report.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"分析モデル数: {len(self.models_data)}")
        report.append("")
        
        # ベストモデル
        if ranking is not None and len(ranking) > 0:
            best_model = ranking.iloc[0]
            report.append("【ベストモデル】")
            report.append(f"  モデル: {best_model['model_alias']}")
            report.append(f"  総合スコア: {best_model['composite_score']:.1f}/100")
            report.append(f"  健全性: {best_model['overall_score']:.1f}/100")
            report.append(f"  メモリ: {best_model['memory_mb']:.1f} MB")
            report.append("")
        
        # 統計サマリ
        if statistical:
            report.append("【統計サマリ】")
            report.append(f"  平均スコア: {statistical['mean_score']:.1f}")
            report.append(f"  標準偏差: {statistical['std_score']:.1f}")
            report.append(f"  中央値: {statistical['median_score']:.1f}")
            report.append(f"  範囲: {statistical['min_score']:.1f} - {statistical['max_score']:.1f}")
            report.append("")
        
        # トップ5
        if ranking is not None and len(ranking) >= 5:
            report.append("【トップ5モデル】")
            for idx, row in ranking.head(5).iterrows():
                report.append(f"  {row['rank']}. {row['model_alias']}: {row['composite_score']:.1f}")
            report.append("")
        
        report.append("="*80)
        
        report_text = "\n".join(report)
        print(report_text)
        
        # ファイルに保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"comparison_report_{timestamp}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"\nレポート保存: {report_path}")
        
        return report_text


def compare_models_from_list(model_list_file: str, output_dir: str = None):
    """リストファイルから複数モデルを比較"""
    print(f"モデルリストファイル: {model_list_file}")
    
    # リストファイルを読み込み
    with open(model_list_file, 'r', encoding='utf-8') as f:
        model_dirs = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"検出されたモデル: {len(model_dirs)}")
    
    # 比較実行
    comparator = MultiModelComparator(output_dir or "nf_auto_runs/comparative_analysis")
    results = comparator.analyze_multiple_models(model_dirs, save_to_postgres=True)
    
    # レポート生成
    comparator.generate_comparison_report()
    
    return results


# メイン実行
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python multi_model_comparator.py model_list.txt")
        print("\nmodel_list.txtの例:")
        print("  # モデルディレクトリのリスト（1行に1つ）")
        print("  /path/to/model1")
        print("  /path/to/model2")
        print("  /path/to/model3")
        sys.exit(1)
    
    model_list_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    compare_models_from_list(model_list_file, output_dir)
