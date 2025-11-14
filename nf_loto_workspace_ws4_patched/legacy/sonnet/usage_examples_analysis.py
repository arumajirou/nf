"""
NeuralForecast分析システム 使用例

このスクリプトは、分析システムの様々な使い方を示します。
"""

from pathlib import Path
import pandas as pd


# ============================================================================
# 例1: 基本的な分析実行
# ============================================================================

def example_1_basic_analysis():
    """最も基本的な使い方"""
    print("\n" + "="*80)
    print("例1: 基本的な分析実行")
    print("="*80)
    
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
    
    # モデルディレクトリを指定
    MODEL_DIR = "path/to/your/model"
    
    # 分析実行
    analyzer = NeuralForecastAnalyzer(MODEL_DIR)
    results = analyzer.run_full_analysis(
        save_to_postgres=True,   # PostgreSQLに保存
        save_to_files=True,      # CSV/Excelに保存
        output_dir="nf_auto_runs/analysis"
    )
    
    # 結果サマリ表示
    print("\n分析結果:")
    for table_name, df in results.items():
        if df is not None and len(df) > 0:
            print(f"  {table_name}: {len(df)} rows")


# ============================================================================
# 例2: ファイル出力のみ（PostgreSQLなし）
# ============================================================================

def example_2_files_only():
    """PostgreSQLを使用せず、ファイル出力のみ"""
    print("\n" + "="*80)
    print("例2: ファイル出力のみ")
    print("="*80)
    
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
    
    MODEL_DIR = "path/to/your/model"
    
    analyzer = NeuralForecastAnalyzer(MODEL_DIR)
    results = analyzer.run_full_analysis(
        save_to_postgres=False,  # PostgreSQL保存なし
        save_to_files=True,
        output_dir="./my_analysis_results"
    )
    
    print("\n出力先: ./my_analysis_results")


# ============================================================================
# 例3: 分析結果の詳細確認
# ============================================================================

def example_3_examine_results():
    """分析結果を詳しく見る"""
    print("\n" + "="*80)
    print("例3: 分析結果の詳細確認")
    print("="*80)
    
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
    
    MODEL_DIR = "path/to/your/model"
    
    analyzer = NeuralForecastAnalyzer(MODEL_DIR)
    results = analyzer.run_full_analysis(save_to_postgres=False)
    
    # 1. モデル基本情報
    print("\n【モデル基本情報】")
    model_profile = results['model_profile']
    print(f"モデルエイリアス: {model_profile['model_alias'].iloc[0]}")
    print(f"モデルクラス: {model_profile['model_class'].iloc[0]}")
    print(f"総パラメータ数: {model_profile['total_params'].iloc[0]:,}")
    print(f"予測ホライゾン(h): {model_profile['h'].iloc[0]}")
    
    # 2. 健全性診断
    print("\n【健全性診断】")
    diagnosis = results['model_diagnosis']
    print(f"総合スコア: {diagnosis['overall_score'].iloc[0]:.1f}/100")
    print(f"重み健全性: {diagnosis['weight_health'].iloc[0]}")
    print(f"収束状態: {diagnosis['convergence_status'].iloc[0]}")
    
    # 3. 最適化提案（高優先度のみ）
    print("\n【最適化提案（優先度4以上）】")
    suggestions = results['optimization_suggestions']
    high_priority = suggestions[suggestions['priority'] >= 4]
    
    for idx, row in high_priority.iterrows():
        print(f"\n優先度 {row['priority']}: {row['parameter_name']}")
        print(f"  現在値: {row['current_value']}")
        print(f"  推奨値: {row['suggested_value']}")
        print(f"  期待効果: {row['expected_impact']}")
    
    # 4. 重み統計（健全性が低い層）
    print("\n【要注意層（健全性スコア<5）】")
    weight_stats = results['weight_statistics']
    unhealthy = weight_stats[weight_stats['health_score'] < 5]
    
    if len(unhealthy) > 0:
        print(f"要注意層: {len(unhealthy)} 個")
        for idx, row in unhealthy.iterrows():
            print(f"  {row['layer_name']}: スコア {row['health_score']}")
    else:
        print("全ての層が健全です！")


# ============================================================================
# 例4: バッチ処理（複数モデル）
# ============================================================================

def example_4_batch_processing():
    """複数のモデルを一括分析"""
    print("\n" + "="*80)
    print("例4: バッチ処理（複数モデル）")
    print("="*80)
    
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
    
    # モデルディレクトリのリスト
    model_dirs = [
        "path/to/model1",
        "path/to/model2",
        "path/to/model3",
    ]
    
    # または、ディレクトリから自動検索
    # model_dirs = list(Path("models").glob("*/"))
    
    results_summary = []
    
    for i, model_dir in enumerate(model_dirs, 1):
        print(f"\n[{i}/{len(model_dirs)}] 分析中: {model_dir}")
        
        try:
            analyzer = NeuralForecastAnalyzer(str(model_dir))
            results = analyzer.run_full_analysis(
                save_to_postgres=True,
                save_to_files=False  # 個別ファイルは保存しない
            )
            
            # サマリ情報を収集
            diagnosis = results['model_diagnosis']
            profile = results['model_profile']
            
            results_summary.append({
                'model_dir': str(model_dir),
                'model_alias': profile['model_alias'].iloc[0],
                'overall_score': diagnosis['overall_score'].iloc[0],
                'weight_health': diagnosis['weight_health'].iloc[0],
                'total_params': profile['total_params'].iloc[0]
            })
            
            print(f"  ✓ 完了")
            
        except Exception as e:
            print(f"  ✗ エラー: {e}")
            continue
    
    # サマリテーブルを作成
    summary_df = pd.DataFrame(results_summary)
    summary_df.to_csv("batch_analysis_summary.csv", index=False)
    
    print("\n" + "="*80)
    print("バッチ処理完了")
    print("="*80)
    print(summary_df.to_string(index=False))


# ============================================================================
# 例5: 可視化の生成
# ============================================================================

def example_5_visualization():
    """分析結果から可視化を生成"""
    print("\n" + "="*80)
    print("例5: 可視化の生成")
    print("="*80)
    
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
    from analysis_visualizer import AnalysisVisualizer, MATPLOTLIB_AVAILABLE
    
    if not MATPLOTLIB_AVAILABLE:
        print("✗ matplotlib が必要です")
        print("  pip install matplotlib seaborn")
        return
    
    MODEL_DIR = "path/to/your/model"
    
    # 分析実行
    analyzer = NeuralForecastAnalyzer(MODEL_DIR)
    results = analyzer.run_full_analysis(save_to_postgres=False)
    
    # 可視化生成
    visualizer = AnalysisVisualizer(
        results, 
        output_dir="nf_auto_runs/analysis/visualizations"
    )
    visualizer.generate_all_visualizations()
    
    print("\n可視化ファイル:")
    viz_dir = Path("nf_auto_runs/analysis/visualizations")
    for file in viz_dir.glob("*.png"):
        print(f"  {file}")


# ============================================================================
# 例6: 既存のCSVから可視化のみ生成
# ============================================================================

def example_6_visualize_from_csv():
    """既存のCSVファイルから可視化を生成"""
    print("\n" + "="*80)
    print("例6: 既存のCSVから可視化")
    print("="*80)
    
    from analysis_visualizer import AnalysisVisualizer, MATPLOTLIB_AVAILABLE
    
    if not MATPLOTLIB_AVAILABLE:
        print("✗ matplotlib が必要です")
        return
    
    analysis_dir = Path("nf_auto_runs/analysis")
    
    # CSVファイルを読み込み
    results = {}
    table_names = [
        'model_profile', 'dataset_profile', 'training_state',
        'weight_statistics', 'model_complexity', 'parameter_sensitivity',
        'model_diagnosis', 'optimization_suggestions'
    ]
    
    for table_name in table_names:
        csv_files = list(analysis_dir.glob(f"{table_name}_*.csv"))
        if csv_files:
            # 最新ファイルを使用
            latest_file = sorted(csv_files)[-1]
            results[table_name] = pd.read_csv(latest_file)
            print(f"✓ 読み込み: {latest_file.name}")
    
    # 可視化生成
    visualizer = AnalysisVisualizer(
        results, 
        output_dir=str(analysis_dir / "visualizations")
    )
    visualizer.generate_all_visualizations()


# ============================================================================
# 例7: PostgreSQLクエリでのデータ確認
# ============================================================================

def example_7_postgresql_queries():
    """PostgreSQLに保存したデータをクエリ"""
    print("\n" + "="*80)
    print("例7: PostgreSQLクエリ")
    print("="*80)
    
    from postgres_manager import PostgreSQLManager
    from db_config import DB_CONFIG
    
    try:
        with PostgreSQLManager(DB_CONFIG) as db:
            # 全モデルのサマリ
            query = """
            SELECT 
                model_alias,
                overall_score,
                weight_health,
                complexity_category,
                analyzed_at
            FROM vw_model_analysis_summary
            ORDER BY analyzed_at DESC
            LIMIT 10;
            """
            
            db.cursor.execute(query)
            results = db.cursor.fetchall()
            
            print("\n最新の分析結果（10件）:")
            for row in results:
                print(f"  {row[0]}: スコア {row[1]:.1f}, 健全性 {row[2]}")
            
            # 高優先度の最適化提案
            query = """
            SELECT 
                mp.model_alias,
                os.parameter_name,
                os.expected_impact
            FROM nf_optimization_suggestions os
            JOIN nf_model_profile mp ON os.model_dir_hash = mp.model_dir_hash
            WHERE os.priority >= 4
            ORDER BY os.priority DESC
            LIMIT 5;
            """
            
            db.cursor.execute(query)
            suggestions = db.cursor.fetchall()
            
            print("\n高優先度の最適化提案（5件）:")
            for row in suggestions:
                print(f"  {row[0]}: {row[1]} → {row[2]}")
    
    except Exception as e:
        print(f"✗ PostgreSQLエラー: {e}")


# ============================================================================
# 例8: カスタム分析パイプライン
# ============================================================================

def example_8_custom_pipeline():
    """カスタムの分析パイプライン"""
    print("\n" + "="*80)
    print("例8: カスタム分析パイプライン")
    print("="*80)
    
    from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
    
    MODEL_DIR = "path/to/your/model"
    
    analyzer = NeuralForecastAnalyzer(MODEL_DIR)
    
    # ステップ1: ファイルロード
    if not analyzer.find_and_load_files():
        print("✗ ファイルロードに失敗")
        return
    
    # ステップ2: 個別に分析を実行
    model_profile = analyzer.extract_model_profile()
    weight_stats = analyzer.analyze_weight_statistics()
    diagnosis = analyzer.diagnose_model_health()
    
    # ステップ3: カスタム分析
    print("\nカスタム分析:")
    
    # 例: 特定の層タイプの統計
    conv_layers = weight_stats[weight_stats['layer_type'] == 'Conv']
    if len(conv_layers) > 0:
        print(f"\nConv層の統計:")
        print(f"  層数: {len(conv_layers)}")
        print(f"  平均健全性: {conv_layers['health_score'].mean():.1f}")
        print(f"  平均スパース性: {conv_layers['sparsity'].mean():.2%}")
    
    # 例: パラメータ数の分布
    total_params = model_profile['total_params'].iloc[0]
    layer_params = weight_stats['param_count'].sum()
    print(f"\nパラメータ分析:")
    print(f"  総パラメータ数: {total_params:,}")
    print(f"  層の合計: {layer_params:,}")


# ============================================================================
# メイン実行
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("NeuralForecast分析システム 使用例")
    print("="*80)
    print("\n実行する例を選択してください:")
    print("  1. 基本的な分析実行")
    print("  2. ファイル出力のみ")
    print("  3. 分析結果の詳細確認")
    print("  4. バッチ処理")
    print("  5. 可視化の生成")
    print("  6. 既存のCSVから可視化")
    print("  7. PostgreSQLクエリ")
    print("  8. カスタム分析パイプライン")
    
    choice = input("\n番号を入力 (1-8): ").strip()
    
    examples = {
        '1': example_1_basic_analysis,
        '2': example_2_files_only,
        '3': example_3_examine_results,
        '4': example_4_batch_processing,
        '5': example_5_visualization,
        '6': example_6_visualize_from_csv,
        '7': example_7_postgresql_queries,
        '8': example_8_custom_pipeline,
    }
    
    if choice in examples:
        examples[choice]()
    else:
        print("無効な選択です")
