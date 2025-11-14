"""
拡張機能統合実行スクリプト
Extended Features Integration

各フェーズの機能を統合的に実行
"""

import sys
from pathlib import Path
import argparse
from datetime import datetime


def phase2_compare_models(model_list_file: str, output_dir: str = None):
    """フェーズ2: 複数モデル比較"""
    print("\n" + "="*80)
    print("フェーズ2: 複数モデル比較")
    print("="*80)
    
    try:
        from multi_model_comparator import compare_models_from_list
        results = compare_models_from_list(model_list_file, output_dir)
        print("\n✓ 複数モデル比較完了")
        return results
    except Exception as e:
        print(f"\n✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def phase3_integrate_predictions(model_dir: str, predictions_csv: str, output_dir: str = None):
    """フェーズ3: 予測データ統合"""
    print("\n" + "="*80)
    print("フェーズ3: 予測データ統合")
    print("="*80)
    
    try:
        from prediction_integrator import PredictionAnalyzer
        
        analyzer = PredictionAnalyzer(
            model_dir, 
            predictions_csv, 
            output_dir or "nf_auto_runs/prediction_analysis"
        )
        results = analyzer.run_integrated_analysis()
        analyzer.generate_comprehensive_report()
        
        print("\n✓ 予測データ統合完了")
        return results
    except Exception as e:
        print(f"\n✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def phase4_setup_automation():
    """フェーズ4: 自動化セットアップ"""
    print("\n" + "="*80)
    print("フェーズ4: 自動化セットアップ")
    print("="*80)
    
    try:
        from automation_system import setup_automation
        setup_automation()
        print("\n✓ 自動化セットアップ完了")
        return True
    except Exception as e:
        print(f"\n✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


def phase4_run_monitoring():
    """フェーズ4: モニタリング実行"""
    print("\n" + "="*80)
    print("フェーズ4: モニタリング実行")
    print("="*80)
    
    try:
        from automation_system import AutomationConfig, ModelMonitor
        
        config = AutomationConfig()
        monitor = ModelMonitor(config)
        results = monitor.monitor_models()
        
        print("\n✓ モニタリング完了")
        return results
    except Exception as e:
        print(f"\n✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def full_pipeline(model_dir: str, predictions_csv: str = None):
    """完全パイプライン実行"""
    print("\n" + "="*80)
    print("完全パイプライン実行")
    print("="*80)
    print(f"開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # 1. 基本分析
    print("\n【ステップ1】基本分析...")
    try:
        from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
        
        analyzer = NeuralForecastAnalyzer(model_dir)
        basic_results = analyzer.run_full_analysis()
        results['basic_analysis'] = basic_results
        print("  ✓ 基本分析完了")
    except Exception as e:
        print(f"  ✗ エラー: {e}")
        return results
    
    # 2. 予測データ統合（提供されている場合）
    if predictions_csv and Path(predictions_csv).exists():
        print("\n【ステップ2】予測データ統合...")
        try:
            from prediction_integrator import PredictionAnalyzer
            
            pred_analyzer = PredictionAnalyzer(model_dir, predictions_csv)
            pred_results = pred_analyzer.run_integrated_analysis()
            results['prediction_integration'] = pred_results
            print("  ✓ 予測データ統合完了")
        except Exception as e:
            print(f"  ✗ エラー: {e}")
    
    # 3. 可視化
    print("\n【ステップ3】可視化生成...")
    try:
        from analysis_visualizer import AnalysisVisualizer, MATPLOTLIB_AVAILABLE
        
        if MATPLOTLIB_AVAILABLE:
            visualizer = AnalysisVisualizer(
                basic_results,
                output_dir="nf_auto_runs/analysis/visualizations"
            )
            visualizer.generate_all_visualizations()
            print("  ✓ 可視化完了")
        else:
            print("  ⚠ matplotlib が見つかりません")
    except Exception as e:
        print(f"  ✗ エラー: {e}")
    
    print("\n" + "="*80)
    print("完全パイプライン完了")
    print(f"終了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    return results


def show_menu():
    """対話型メニュー"""
    print("\n" + "="*80)
    print("NeuralForecast 拡張機能メニュー")
    print("="*80)
    print("\n拡張フェーズ:")
    print("  1. フェーズ2: 複数モデル比較")
    print("  2. フェーズ3: 予測データ統合")
    print("  3. フェーズ4: 自動化セットアップ")
    print("  4. フェーズ4: モニタリング実行")
    print("\nパイプライン:")
    print("  5. 完全パイプライン実行")
    print("\n基本機能:")
    print("  6. 基本分析のみ")
    print("  7. 可視化のみ")
    print("\n  0. 終了")
    
    choice = input("\n選択 (0-7): ").strip()
    
    if choice == '1':
        model_list = input("モデルリストファイル: ").strip()
        phase2_compare_models(model_list)
    
    elif choice == '2':
        model_dir = input("モデルディレクトリ: ").strip()
        predictions = input("predictions.csv: ").strip()
        phase3_integrate_predictions(model_dir, predictions)
    
    elif choice == '3':
        phase4_setup_automation()
    
    elif choice == '4':
        phase4_run_monitoring()
    
    elif choice == '5':
        model_dir = input("モデルディレクトリ: ").strip()
        predictions = input("predictions.csv (オプション): ").strip()
        full_pipeline(model_dir, predictions if predictions else None)
    
    elif choice == '6':
        model_dir = input("モデルディレクトリ: ").strip()
        from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
        analyzer = NeuralForecastAnalyzer(model_dir)
        analyzer.run_full_analysis()
    
    elif choice == '7':
        analysis_dir = input("分析ディレクトリ: ").strip()
        from run_analysis import run_visualization_only
        run_visualization_only(analysis_dir)
    
    elif choice == '0':
        print("終了します")
        sys.exit(0)
    
    else:
        print("無効な選択です")


def main():
    parser = argparse.ArgumentParser(
        description='NeuralForecast拡張機能統合実行',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:

# 対話型メニュー
python extended_runner.py

# フェーズ2: 複数モデル比較
python extended_runner.py --phase2 model_list.txt

# フェーズ3: 予測データ統合
python extended_runner.py --phase3 ./model ./predictions.csv

# フェーズ4: 自動化セットアップ
python extended_runner.py --phase4-setup

# フェーズ4: モニタリング実行
python extended_runner.py --phase4-monitor

# 完全パイプライン
python extended_runner.py --full-pipeline ./model --predictions ./predictions.csv
        """
    )
    
    parser.add_argument('--phase2', metavar='MODEL_LIST',
                       help='フェーズ2: 複数モデル比較（モデルリストファイル）')
    
    parser.add_argument('--phase3', nargs=2, metavar=('MODEL_DIR', 'PREDICTIONS'),
                       help='フェーズ3: 予測データ統合')
    
    parser.add_argument('--phase4-setup', action='store_true',
                       help='フェーズ4: 自動化セットアップ')
    
    parser.add_argument('--phase4-monitor', action='store_true',
                       help='フェーズ4: モニタリング実行')
    
    parser.add_argument('--full-pipeline', metavar='MODEL_DIR',
                       help='完全パイプライン実行')
    
    parser.add_argument('--predictions', metavar='CSV',
                       help='予測データCSV（--full-pipelineと併用）')
    
    parser.add_argument('--output-dir', metavar='DIR',
                       help='出力ディレクトリ')
    
    args = parser.parse_args()
    
    # コマンドライン引数がない場合は対話型メニュー
    if not any([args.phase2, args.phase3, args.phase4_setup, 
                args.phase4_monitor, args.full_pipeline]):
        while True:
            show_menu()
            input("\nEnterキーで続行...")
    
    # コマンドライン実行
    if args.phase2:
        phase2_compare_models(args.phase2, args.output_dir)
    
    if args.phase3:
        phase3_integrate_predictions(args.phase3[0], args.phase3[1], args.output_dir)
    
    if args.phase4_setup:
        phase4_setup_automation()
    
    if args.phase4_monitor:
        phase4_run_monitoring()
    
    if args.full_pipeline:
        full_pipeline(args.full_pipeline, args.predictions)


if __name__ == "__main__":
    main()
