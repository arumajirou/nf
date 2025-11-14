"""
フェーズ3: 予測データ統合システム
Prediction Data Integration & Advanced Metrics

機能:
- predictions.csvとモデル分析の統合
- 実際の精度メトリクスとモデル特性の相関分析
- Document 1の評価メニュー（A〜J）の実装
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
from scipy import stats
from scipy.stats import ks_2samp
import warnings

warnings.filterwarnings('ignore')

try:
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
except ImportError:
    print("⚠ neuralforecast_analyzer_v2.py が必要です")


class PredictionAnalyzer:
    """予測データと統合した高度な評価システム"""
    
    def __init__(self, model_dir: str, predictions_csv: str, 
                 output_dir: str = "nf_auto_runs/prediction_analysis"):
        self.model_dir = Path(model_dir)
        self.predictions_csv = Path(predictions_csv)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # データ
        self.predictions = None
        self.model_analysis = None
        self.metrics = {}
        
    def run_integrated_analysis(self) -> Dict:
        """統合分析を実行"""
        print("\n" + "="*80)
        print("予測データ統合分析")
        print("="*80)
        
        # ステップ1: モデル分析
        print("\n[1/4] モデル分析実行中...")
        analyzer = NeuralForecastAnalyzer(str(self.model_dir))
        self.model_analysis = analyzer.run_full_analysis(
            save_to_postgres=False,
            save_to_files=False
        )
        print("  ✓ モデル分析完了")
        
        # ステップ2: 予測データ読み込み
        print("\n[2/4] 予測データ読み込み中...")
        self.predictions = pd.read_csv(self.predictions_csv)
        print(f"  ✓ 予測データ: {len(self.predictions)} rows")
        
        # ステップ3: 高度な評価メトリクス計算
        print("\n[3/4] 高度な評価メトリクス計算中...")
        self.metrics['A_error_decomposition'] = self._analyze_error_decomposition()
        self.metrics['B_probabilistic_calibration'] = self._analyze_probabilistic_calibration()
        self.metrics['C_statistical_tests'] = self._perform_statistical_tests()
        self.metrics['D_drift_detection'] = self._detect_drift()
        self.metrics['E_robustness'] = self._analyze_robustness()
        self.metrics['F_multivariate'] = self._analyze_multivariate_structure()
        self.metrics['G_business_metrics'] = self._calculate_business_metrics()
        self.metrics['H_explainability'] = self._analyze_explainability()
        print("  ✓ メトリクス計算完了")
        
        # ステップ4: 結果保存
        print("\n[4/4] 結果保存中...")
        self._save_results()
        print("  ✓ 保存完了")
        
        print("\n✓ 統合分析完了")
        return self.metrics
    
    def _analyze_error_decomposition(self) -> Dict:
        """A. 誤差の分解・安定性"""
        print("    A. 誤差の分解・安定性...")
        
        if 'y' not in self.predictions.columns or 'y_hat' not in self.predictions.columns:
            return {'error': 'Required columns not found'}
        
        y_true = self.predictions['y'].values
        y_pred = self.predictions['y_hat'].values
        
        # 基本誤差メトリクス
        mae = np.mean(np.abs(y_true - y_pred))
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
        
        # sMAPE (対称MAPE)
        smape = np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred) + 1e-8)) * 100
        
        # バイアス（系統的誤差）
        bias = np.mean(y_pred - y_true)
        
        # 誤差の標準偏差（ランダム誤差）
        error_std = np.std(y_pred - y_true)
        
        # MASE（Mean Absolute Scaled Error）
        # ナイーブ予測との比較
        naive_forecast = np.roll(y_true, 1)
        naive_forecast[0] = y_true[0]
        naive_mae = np.mean(np.abs(y_true - naive_forecast))
        mase = mae / (naive_mae + 1e-8)
        
        # 水準別誤差（低需要/中需要/高需要）
        percentiles = np.percentile(y_true, [33, 67])
        low_demand = y_true < percentiles[0]
        mid_demand = (y_true >= percentiles[0]) & (y_true < percentiles[1])
        high_demand = y_true >= percentiles[1]
        
        mae_low = np.mean(np.abs(y_true[low_demand] - y_pred[low_demand]))
        mae_mid = np.mean(np.abs(y_true[mid_demand] - y_pred[mid_demand]))
        mae_high = np.mean(np.abs(y_true[high_demand] - y_pred[high_demand]))
        
        return {
            'mae': float(mae),
            'rmse': float(rmse),
            'mape': float(mape),
            'smape': float(smape),
            'bias': float(bias),
            'error_std': float(error_std),
            'mase': float(mase),
            'mae_by_level': {
                'low_demand': float(mae_low),
                'mid_demand': float(mae_mid),
                'high_demand': float(mae_high)
            }
        }
    
    def _analyze_probabilistic_calibration(self) -> Dict:
        """B. 確率予測の校正と区間品質"""
        print("    B. 確率予測の校正と区間品質...")
        
        # 予測区間のカラムを探す（例: y_hat_lo-90, y_hat_hi-90）
        interval_cols = [col for col in self.predictions.columns if 'lo-' in col or 'hi-' in col]
        
        if not interval_cols or 'y' not in self.predictions.columns:
            return {'message': 'Probabilistic forecasts not available'}
        
        y_true = self.predictions['y'].values
        
        # 90%予測区間を使用
        lo_90 = self.predictions.get('y_hat_lo-90', self.predictions.get('AutoTCN-lo-90'))
        hi_90 = self.predictions.get('y_hat_hi-90', self.predictions.get('AutoTCN-hi-90'))
        
        if lo_90 is None or hi_90 is None:
            return {'message': 'Prediction intervals not found'}
        
        lo_90 = lo_90.values
        hi_90 = hi_90.values
        
        # PICP (Prediction Interval Coverage Probability)
        coverage = np.mean((y_true >= lo_90) & (y_true <= hi_90))
        
        # MIL (Mean Interval Length)
        interval_length = np.mean(hi_90 - lo_90)
        
        # Winklerスコア（区間の品質）
        alpha = 0.1  # 90%区間
        winkler_scores = []
        for i in range(len(y_true)):
            width = hi_90[i] - lo_90[i]
            if y_true[i] < lo_90[i]:
                penalty = 2 / alpha * (lo_90[i] - y_true[i])
            elif y_true[i] > hi_90[i]:
                penalty = 2 / alpha * (y_true[i] - hi_90[i])
            else:
                penalty = 0
            winkler_scores.append(width + penalty)
        
        winkler_score = np.mean(winkler_scores)
        
        return {
            'picp_90': float(coverage),
            'target_coverage': 0.90,
            'coverage_deviation': float(abs(coverage - 0.90)),
            'mean_interval_length': float(interval_length),
            'winkler_score': float(winkler_score),
            'calibration_status': 'good' if abs(coverage - 0.90) < 0.05 else 'needs_adjustment'
        }
    
    def _perform_statistical_tests(self) -> Dict:
        """C. 統計的モデル比較"""
        print("    C. 統計的モデル比較...")
        
        if 'y' not in self.predictions.columns or 'y_hat' not in self.predictions.columns:
            return {}
        
        y_true = self.predictions['y'].values
        y_pred = self.predictions['y_hat'].values
        
        # 残差
        residuals = y_true - y_pred
        
        # Ljung-Box検定（残差の自己相関）
        from scipy.stats import chi2
        
        # 簡易的な自己相関検定
        acf_lag1 = np.corrcoef(residuals[:-1], residuals[1:])[0, 1]
        
        # 正規性検定（Shapiro-Wilk）
        if len(residuals) <= 5000:
            _, normality_pvalue = stats.shapiro(residuals[:5000])
        else:
            normality_pvalue = None
        
        # 残差の統計量
        residuals_mean = np.mean(residuals)
        residuals_std = np.std(residuals)
        residuals_skew = stats.skew(residuals)
        residuals_kurtosis = stats.kurtosis(residuals)
        
        return {
            'acf_lag1': float(acf_lag1),
            'residuals_mean': float(residuals_mean),
            'residuals_std': float(residuals_std),
            'residuals_skewness': float(residuals_skew),
            'residuals_kurtosis': float(residuals_kurtosis),
            'normality_pvalue': float(normality_pvalue) if normality_pvalue else None,
            'white_noise_test': 'pass' if abs(acf_lag1) < 0.1 else 'fail'
        }
    
    def _detect_drift(self) -> Dict:
        """D. データドリフト・レジーム変化"""
        print("    D. データドリフト・レジーム変化...")
        
        if 'y' not in self.predictions.columns:
            return {}
        
        y_true = self.predictions['y'].values
        
        # データを前半/後半に分割
        split_point = len(y_true) // 2
        first_half = y_true[:split_point]
        second_half = y_true[split_point:]
        
        # KS検定（分布の変化）
        ks_stat, ks_pvalue = ks_2samp(first_half, second_half)
        
        # 平均値の変化
        mean_first = np.mean(first_half)
        mean_second = np.mean(second_half)
        mean_shift = (mean_second - mean_first) / (mean_first + 1e-8) * 100
        
        # 分散の変化
        std_first = np.std(first_half)
        std_second = np.std(second_half)
        std_shift = (std_second - std_first) / (std_first + 1e-8) * 100
        
        return {
            'ks_statistic': float(ks_stat),
            'ks_pvalue': float(ks_pvalue),
            'distribution_drift': 'detected' if ks_pvalue < 0.05 else 'not_detected',
            'mean_shift_percent': float(mean_shift),
            'std_shift_percent': float(std_shift)
        }
    
    def _analyze_robustness(self) -> Dict:
        """E. ロバストネス・ストレス試験"""
        print("    E. ロバストネス分析...")
        
        if 'y' not in self.predictions.columns or 'y_hat' not in self.predictions.columns:
            return {}
        
        y_true = self.predictions['y'].values
        y_pred = self.predictions['y_hat'].values
        
        # 外れ値に対するロバストネス
        # IQR法で外れ値を検出
        q1, q3 = np.percentile(y_true, [25, 75])
        iqr = q3 - q1
        outlier_mask = (y_true < q1 - 1.5*iqr) | (y_true > q3 + 1.5*iqr)
        
        # 外れ値でのMAE
        if np.any(outlier_mask):
            mae_outliers = np.mean(np.abs(y_true[outlier_mask] - y_pred[outlier_mask]))
            mae_normal = np.mean(np.abs(y_true[~outlier_mask] - y_pred[~outlier_mask]))
        else:
            mae_outliers = 0
            mae_normal = np.mean(np.abs(y_true - y_pred))
        
        # ゼロ値に対する精度
        zero_mask = y_true == 0
        if np.any(zero_mask):
            mae_zeros = np.mean(np.abs(y_true[zero_mask] - y_pred[zero_mask]))
            zero_prediction_rate = np.mean(y_pred[zero_mask] == 0)
        else:
            mae_zeros = None
            zero_prediction_rate = None
        
        return {
            'outlier_count': int(np.sum(outlier_mask)),
            'outlier_percentage': float(np.mean(outlier_mask) * 100),
            'mae_outliers': float(mae_outliers),
            'mae_normal': float(mae_normal),
            'robustness_ratio': float(mae_outliers / (mae_normal + 1e-8)),
            'zero_count': int(np.sum(zero_mask)),
            'mae_at_zeros': float(mae_zeros) if mae_zeros is not None else None,
            'zero_prediction_rate': float(zero_prediction_rate) if zero_prediction_rate is not None else None
        }
    
    def _analyze_multivariate_structure(self) -> Dict:
        """F. 多変量構造"""
        print("    F. 多変量構造分析...")
        
        # 複数系列がある場合の分析
        if 'unique_id' not in self.predictions.columns:
            return {'message': 'Single series detected'}
        
        unique_ids = self.predictions['unique_id'].unique()
        
        if len(unique_ids) <= 1:
            return {'message': 'Single series detected'}
        
        # 系列ごとのMAE
        series_mae = {}
        for uid in unique_ids[:10]:  # 最大10系列
            series_data = self.predictions[self.predictions['unique_id'] == uid]
            if 'y' in series_data.columns and 'y_hat' in series_data.columns:
                mae = np.mean(np.abs(series_data['y'] - series_data['y_hat']))
                series_mae[str(uid)] = float(mae)
        
        return {
            'num_series': len(unique_ids),
            'series_mae_sample': series_mae,
            'mae_std_across_series': float(np.std(list(series_mae.values())))
        }
    
    def _calculate_business_metrics(self) -> Dict:
        """G. ビジネス適合・意思決定連携"""
        print("    G. ビジネスメトリクス...")
        
        if 'y' not in self.predictions.columns or 'y_hat' not in self.predictions.columns:
            return {}
        
        y_true = self.predictions['y'].values
        y_pred = self.predictions['y_hat'].values
        
        # 過少予測/過大予測の分析
        overforecast = y_pred > y_true
        underforecast = y_pred < y_true
        
        overforecast_count = np.sum(overforecast)
        underforecast_count = np.sum(underforecast)
        
        # 平均バイアス
        mean_bias = np.mean(y_pred - y_true)
        bias_direction = 'overforecasting' if mean_bias > 0 else 'underforecasting'
        
        # コスト敏感メトリクス（仮定: 過少コスト=2倍）
        cost_overforecast = 1.0  # 在庫コスト
        cost_underforecast = 2.0  # 欠品コスト
        
        total_cost = (
            np.sum(np.abs(y_pred[overforecast] - y_true[overforecast])) * cost_overforecast +
            np.sum(np.abs(y_pred[underforecast] - y_true[underforecast])) * cost_underforecast
        )
        
        # サービスレベル（需要を満たせた割合）
        service_level = np.mean(y_pred >= y_true)
        
        return {
            'mean_bias': float(mean_bias),
            'bias_direction': bias_direction,
            'overforecast_rate': float(overforecast_count / len(y_true)),
            'underforecast_rate': float(underforecast_count / len(y_true)),
            'total_cost': float(total_cost),
            'service_level': float(service_level)
        }
    
    def _analyze_explainability(self) -> Dict:
        """H. 可視化・説明可能性"""
        print("    H. 説明可能性分析...")
        
        # モデル分析から重要情報を抽出
        param_sensitivity = self.model_analysis.get('parameter_sensitivity')
        
        if param_sensitivity is None:
            return {}
        
        # 重要度の高いパラメータ
        top_params = param_sensitivity.nlargest(5, 'importance_score')
        
        important_params = {}
        for _, row in top_params.iterrows():
            important_params[row['parameter_name']] = {
                'value': row['parameter_value'],
                'importance': int(row['importance_score'])
            }
        
        return {
            'top_important_parameters': important_params,
            'model_complexity': self.model_analysis.get('model_complexity', {}).get('complexity_category', ['unknown'])[0] if self.model_analysis.get('model_complexity') is not None else 'unknown'
        }
    
    def _save_results(self):
        """結果を保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. JSON形式で全メトリクスを保存
        json_path = self.output_dir / f"integrated_metrics_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
        print(f"  ✓ {json_path}")
        
        # 2. サマリCSVを作成
        summary_data = {
            'metric_category': [],
            'metric_name': [],
            'value': []
        }
        
        for category, metrics in self.metrics.items():
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    if isinstance(value, (int, float)):
                        summary_data['metric_category'].append(category)
                        summary_data['metric_name'].append(key)
                        summary_data['value'].append(value)
        
        summary_df = pd.DataFrame(summary_data)
        csv_path = self.output_dir / f"metrics_summary_{timestamp}.csv"
        summary_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"  ✓ {csv_path}")
    
    def generate_comprehensive_report(self) -> str:
        """包括的レポートを生成"""
        report = []
        report.append("="*80)
        report.append("予測データ統合分析レポート")
        report.append("="*80)
        report.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"モデル: {self.model_dir}")
        report.append(f"予測データ: {self.predictions_csv}")
        report.append("")
        
        # A. 誤差分解
        error_metrics = self.metrics.get('A_error_decomposition', {})
        if error_metrics:
            report.append("【A. 誤差分解】")
            report.append(f"  MAE: {error_metrics.get('mae', 0):.4f}")
            report.append(f"  RMSE: {error_metrics.get('rmse', 0):.4f}")
            report.append(f"  MASE: {error_metrics.get('mase', 0):.4f}")
            report.append(f"  バイアス: {error_metrics.get('bias', 0):.4f}")
            report.append("")
        
        # B. 確率校正
        prob_metrics = self.metrics.get('B_probabilistic_calibration', {})
        if prob_metrics and 'picp_90' in prob_metrics:
            report.append("【B. 確率校正】")
            report.append(f"  カバレッジ(90%): {prob_metrics['picp_90']:.2%}")
            report.append(f"  区間長: {prob_metrics.get('mean_interval_length', 0):.4f}")
            report.append(f"  校正状態: {prob_metrics.get('calibration_status', 'N/A')}")
            report.append("")
        
        # G. ビジネスメトリクス
        business_metrics = self.metrics.get('G_business_metrics', {})
        if business_metrics:
            report.append("【G. ビジネスメトリクス】")
            report.append(f"  サービスレベル: {business_metrics.get('service_level', 0):.2%}")
            report.append(f"  バイアス方向: {business_metrics.get('bias_direction', 'N/A')}")
            report.append(f"  総コスト: {business_metrics.get('total_cost', 0):.2f}")
            report.append("")
        
        report.append("="*80)
        
        report_text = "\n".join(report)
        print("\n" + report_text)
        
        # ファイルに保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_dir / f"integrated_report_{timestamp}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        return report_text


# メイン実行
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  python prediction_integrator.py <model_dir> <predictions.csv>")
        print("\n例:")
        print("  python prediction_integrator.py ./model ./predictions.csv")
        sys.exit(1)
    
    model_dir = sys.argv[1]
    predictions_csv = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    analyzer = PredictionAnalyzer(model_dir, predictions_csv, 
                                  output_dir or "nf_auto_runs/prediction_analysis")
    results = analyzer.run_integrated_analysis()
    analyzer.generate_comprehensive_report()
