"""
NeuralForecast分析結果の可視化
分析結果から視覚的なレポートを生成
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # GUI不要のバックエンド
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠ matplotlib が見つかりません。可視化機能は無効です")

try:
    import seaborn as sns
    sns.set_style("whitegrid")
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False


class AnalysisVisualizer:
    """分析結果の可視化クラス"""
    
    def __init__(self, analysis_results: dict, output_dir: str = "nf_auto_runs/analysis/visualizations"):
        self.results = analysis_results
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("matplotlib が必要です: pip install matplotlib")
    
    def plot_weight_distributions(self):
        """重み分布のヒストグラムとボックスプロット"""
        print("\n可視化1: 重み分布...")
        
        weight_stats = self.results.get('weight_statistics')
        if weight_stats is None or len(weight_stats) == 0:
            print("  ⚠ 重み統計データが見つかりません")
            return
        
        # 上位10層を選択（パラメータ数順）
        top_layers = weight_stats.nlargest(10, 'param_count')
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Weight Statistics Overview', fontsize=16, fontweight='bold')
        
        # 1. 健全性スコア
        ax1 = axes[0, 0]
        colors = ['green' if x >= 8 else 'orange' if x >= 5 else 'red' 
                  for x in weight_stats['health_score']]
        ax1.barh(range(len(top_layers)), top_layers['health_score'], color=colors[:len(top_layers)])
        ax1.set_yticks(range(len(top_layers)))
        ax1.set_yticklabels([name[:30] for name in top_layers['layer_name']], fontsize=8)
        ax1.set_xlabel('Health Score')
        ax1.set_title('Layer Health Scores (Top 10 by Param Count)')
        ax1.axvline(x=8, color='green', linestyle='--', alpha=0.5, label='Good (≥8)')
        ax1.axvline(x=5, color='orange', linestyle='--', alpha=0.5, label='Warning (≥5)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. L2ノルム
        ax2 = axes[0, 1]
        ax2.bar(range(len(top_layers)), top_layers['l2_norm'], alpha=0.7, color='steelblue')
        ax2.set_xticks(range(len(top_layers)))
        ax2.set_xticklabels(range(1, len(top_layers)+1))
        ax2.set_xlabel('Layer Index')
        ax2.set_ylabel('L2 Norm')
        ax2.set_title('L2 Norms (Top 10 Layers)')
        ax2.grid(True, alpha=0.3)
        
        # 3. スパース性
        ax3 = axes[1, 0]
        ax3.scatter(weight_stats['param_count'], weight_stats['sparsity'], 
                   alpha=0.6, c=weight_stats['health_score'], cmap='RdYlGn', s=50)
        ax3.set_xlabel('Parameter Count')
        ax3.set_ylabel('Sparsity')
        ax3.set_title('Parameter Count vs Sparsity')
        ax3.set_xscale('log')
        cbar = plt.colorbar(ax3.collections[0], ax=ax3)
        cbar.set_label('Health Score')
        ax3.grid(True, alpha=0.3)
        
        # 4. 外れ値比率
        ax4 = axes[1, 1]
        layer_types = weight_stats['layer_type'].unique()
        type_outliers = [weight_stats[weight_stats['layer_type']==t]['outlier_ratio'].mean() 
                        for t in layer_types]
        ax4.bar(range(len(layer_types)), type_outliers, alpha=0.7, color='coral')
        ax4.set_xticks(range(len(layer_types)))
        ax4.set_xticklabels(layer_types, rotation=45, ha='right')
        ax4.set_ylabel('Average Outlier Ratio')
        ax4.set_title('Outlier Ratio by Layer Type')
        ax4.axhline(y=0.05, color='red', linestyle='--', alpha=0.5, label='Warning Threshold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        output_path = self.output_dir / "weight_distributions.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ 保存: {output_path}")
    
    def plot_hyperparameter_radar(self):
        """ハイパーパラメータのレーダーチャート"""
        print("\n可視化2: ハイパーパラメータレーダー...")
        
        param_sensitivity = self.results.get('parameter_sensitivity')
        if param_sensitivity is None or len(param_sensitivity) == 0:
            print("  ⚠ パラメータ感度データが見つかりません")
            return
        
        # 重要度の高いパラメータを抽出
        important_params = param_sensitivity[param_sensitivity['importance_score'] >= 6].copy()
        
        if len(important_params) < 3:
            print("  ⚠ レーダーチャート作成に十分なパラメータがありません")
            return
        
        # 上位8つまで
        important_params = important_params.nlargest(8, 'importance_score')
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # 角度の計算
        categories = important_params['parameter_name'].tolist()
        N = len(categories)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        
        # 値の正規化（0-10スケール）
        values = important_params['importance_score'].tolist()
        
        # プロット（閉じた図形にする）
        values += values[:1]
        angles += angles[:1]
        categories += categories[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, color='steelblue', label='Importance')
        ax.fill(angles, values, alpha=0.25, color='steelblue')
        
        # カテゴリラベル
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories[:-1], fontsize=10)
        
        # スケール設定
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8)
        
        ax.set_title('Hyperparameter Importance Radar', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True)
        
        plt.tight_layout()
        
        output_path = self.output_dir / "hyperparameter_radar.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ 保存: {output_path}")
    
    def plot_model_complexity_overview(self):
        """モデル複雑度の概観"""
        print("\n可視化3: モデル複雑度概観...")
        
        model_profile = self.results.get('model_profile')
        model_complexity = self.results.get('model_complexity')
        weight_stats = self.results.get('weight_statistics')
        
        if model_profile is None or len(model_profile) == 0:
            print("  ⚠ モデルプロファイルが見つかりません")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Model Complexity Overview', fontsize=16, fontweight='bold')
        
        # 1. パラメータ数の内訳（層タイプ別）
        ax1 = axes[0, 0]
        if weight_stats is not None and len(weight_stats) > 0:
            type_params = weight_stats.groupby('layer_type')['param_count'].sum().sort_values(ascending=False)
            colors_map = {'Conv': 'steelblue', 'Linear': 'coral', 'RNN': 'green', 
                         'Normalization': 'gold', 'Bias': 'gray', 'Unknown': 'lightgray'}
            colors = [colors_map.get(t, 'lightgray') for t in type_params.index]
            ax1.pie(type_params.values, labels=type_params.index, autopct='%1.1f%%',
                   startangle=90, colors=colors)
            ax1.set_title('Parameter Distribution by Layer Type')
        else:
            ax1.text(0.5, 0.5, 'No data', ha='center', va='center')
            ax1.set_title('Parameter Distribution by Layer Type')
        
        # 2. 複雑度カテゴリ
        ax2 = axes[0, 1]
        if model_complexity is not None and len(model_complexity) > 0:
            complexity_cat = model_complexity['complexity_category'].iloc[0]
            memory_mb = model_complexity['memory_mb'].iloc[0]
            
            categories = ['light', 'medium', 'heavy']
            values = [1 if complexity_cat == c else 0 for c in categories]
            colors = ['green', 'orange', 'red']
            
            bars = ax2.barh(categories, [100, 100, 100], color=colors, alpha=0.3)
            ax2.barh(categories, [v * 100 for v in values], color=colors, alpha=0.8)
            ax2.set_xlim(0, 100)
            ax2.set_xlabel('Complexity Level')
            ax2.set_title(f'Model Complexity: {complexity_cat.upper()}\nMemory: {memory_mb:.1f} MB')
            ax2.grid(True, alpha=0.3, axis='x')
        else:
            ax2.text(0.5, 0.5, 'No data', ha='center', va='center')
            ax2.set_title('Model Complexity')
        
        # 3. 層の深さと幅
        ax3 = axes[1, 0]
        if weight_stats is not None and len(weight_stats) > 0:
            layer_sizes = weight_stats['param_count'].values
            ax3.plot(range(len(layer_sizes)), layer_sizes, 'o-', linewidth=2, markersize=6, color='steelblue')
            ax3.set_xlabel('Layer Index')
            ax3.set_ylabel('Parameter Count')
            ax3.set_title('Layer-wise Parameter Count')
            ax3.set_yscale('log')
            ax3.grid(True, alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Layer-wise Parameter Count')
        
        # 4. メモリとパラメータ効率
        ax4 = axes[1, 1]
        if model_complexity is not None and len(model_complexity) > 0:
            param_eff = model_complexity['param_efficiency'].iloc[0]
            memory_mb = model_complexity['memory_mb'].iloc[0]
            
            metrics = ['Memory\n(MB)', 'Param\nEfficiency']
            values = [memory_mb, param_eff]
            
            # 正規化（見やすくするため）
            normalized = [memory_mb / 10, min(param_eff / 1000, 10)]
            
            ax4.bar(metrics, normalized, color=['coral', 'steelblue'], alpha=0.7)
            ax4.set_ylabel('Normalized Value')
            ax4.set_title('Resource Metrics')
            
            # 実際の値を表示
            for i, (m, v) in enumerate(zip(metrics, values)):
                ax4.text(i, normalized[i], f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
            
            ax4.grid(True, alpha=0.3, axis='y')
        else:
            ax4.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Resource Metrics')
        
        plt.tight_layout()
        
        output_path = self.output_dir / "model_complexity_overview.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ 保存: {output_path}")
    
    def plot_diagnosis_summary(self):
        """診断サマリ"""
        print("\n可視化4: 診断サマリ...")
        
        diagnosis = self.results.get('model_diagnosis')
        optimization = self.results.get('optimization_suggestions')
        
        if diagnosis is None or len(diagnosis) == 0:
            print("  ⚠ 診断データが見つかりません")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Model Diagnosis Summary', fontsize=16, fontweight='bold')
        
        # 1. 総合スコア
        ax1 = axes[0]
        overall_score = diagnosis['overall_score'].iloc[0]
        weight_health = diagnosis['weight_health'].iloc[0]
        
        # ゲージチャート風
        theta = np.linspace(0, np.pi, 100)
        r = np.ones_like(theta)
        
        ax1 = plt.subplot(1, 2, 1, projection='polar')
        ax1.plot(theta, r, linewidth=20, color='lightgray', alpha=0.3)
        
        # スコアに応じた色
        score_theta = np.linspace(0, np.pi * (overall_score / 100), 100)
        score_color = 'green' if overall_score >= 70 else 'orange' if overall_score >= 50 else 'red'
        ax1.plot(score_theta, r[:len(score_theta)], linewidth=20, color=score_color, alpha=0.8)
        
        ax1.set_ylim(0, 1)
        ax1.set_yticks([])
        ax1.set_xticks([0, np.pi/2, np.pi])
        ax1.set_xticklabels(['0', '50', '100'])
        ax1.set_title(f'Overall Score: {overall_score:.1f}/100\nHealth: {weight_health.upper()}', 
                     fontsize=12, pad=20)
        
        # 2. 最適化提案の優先度分布
        ax2 = axes[1]
        if optimization is not None and len(optimization) > 0:
            priority_counts = optimization['priority'].value_counts().sort_index()
            colors = ['red', 'orange', 'gold', 'lightgreen', 'green']
            
            bars = ax2.barh(priority_counts.index, priority_counts.values, 
                           color=[colors[p-1] for p in priority_counts.index])
            ax2.set_xlabel('Number of Suggestions')
            ax2.set_ylabel('Priority Level')
            ax2.set_title('Optimization Suggestions by Priority')
            ax2.set_yticks(range(1, 6))
            ax2.invert_yaxis()
            ax2.grid(True, alpha=0.3, axis='x')
            
            # 値をバーに表示
            for i, v in enumerate(priority_counts.values):
                ax2.text(v, priority_counts.index[i], f' {v}', va='center')
        else:
            ax2.text(0.5, 0.5, 'No suggestions', ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('Optimization Suggestions by Priority')
        
        plt.tight_layout()
        
        output_path = self.output_dir / "diagnosis_summary.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ 保存: {output_path}")
    
    def generate_all_visualizations(self):
        """全ての可視化を生成"""
        print("\n" + "="*80)
        print("可視化の生成")
        print("="*80)
        
        try:
            self.plot_weight_distributions()
        except Exception as e:
            print(f"  ✗ 重み分布の可視化エラー: {e}")
        
        try:
            self.plot_hyperparameter_radar()
        except Exception as e:
            print(f"  ✗ ハイパーパラメータレーダーの可視化エラー: {e}")
        
        try:
            self.plot_model_complexity_overview()
        except Exception as e:
            print(f"  ✗ モデル複雑度の可視化エラー: {e}")
        
        try:
            self.plot_diagnosis_summary()
        except Exception as e:
            print(f"  ✗ 診断サマリの可視化エラー: {e}")
        
        print("\n✓ 可視化生成完了")
        print(f"出力ディレクトリ: {self.output_dir}")


# スタンドアロン実行用
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python analysis_visualizer.py <analysis_directory>")
        print("例: python analysis_visualizer.py nf_auto_runs/analysis")
        sys.exit(1)
    
    analysis_dir = Path(sys.argv[1])
    
    if not analysis_dir.exists():
        print(f"✗ ディレクトリが見つかりません: {analysis_dir}")
        sys.exit(1)
    
    # 最新の分析結果CSVを読み込み
    results = {}
    
    csv_files = list(analysis_dir.glob("*.csv"))
    if not csv_files:
        print(f"✗ CSVファイルが見つかりません: {analysis_dir}")
        sys.exit(1)
    
    # 各テーブルの最新ファイルを読み込み
    table_names = ['model_profile', 'dataset_profile', 'training_state', 
                   'weight_statistics', 'model_complexity', 'parameter_sensitivity',
                   'model_diagnosis', 'optimization_suggestions']
    
    for table_name in table_names:
        matching_files = [f for f in csv_files if f.name.startswith(table_name)]
        if matching_files:
            # 最新ファイル（タイムスタンプ順）
            latest_file = sorted(matching_files)[-1]
            results[table_name] = pd.read_csv(latest_file)
            print(f"✓ 読み込み: {latest_file.name}")
    
    # 可視化実行
    visualizer = AnalysisVisualizer(results, output_dir=analysis_dir / "visualizations")
    visualizer.generate_all_visualizations()
