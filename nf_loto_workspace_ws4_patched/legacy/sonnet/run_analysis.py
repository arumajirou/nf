"""
NeuralForecast分析システム 簡易実行スクリプト

使用方法:
    python run_analysis.py [model_directory]

例:
    python run_analysis.py "C:/path/to/model"
    python run_analysis.py  # デフォルトパス使用
"""

import sys
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='NeuralForecast Model Analyzer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # 基本実行
  python run_analysis.py /path/to/model

  # PostgreSQL保存なし
  python run_analysis.py /path/to/model --no-postgres

  # 可視化のみ
  python run_analysis.py /path/to/model --visualize-only

  # 出力ディレクトリ指定
  python run_analysis.py /path/to/model --output ./results
        """
    )
    
    parser.add_argument(
        'model_dir',
        nargs='?',
        help='モデルディレクトリのパス（省略時はデフォルトパス）'
    )
    
    parser.add_argument(
        '--no-postgres',
        action='store_true',
        help='PostgreSQLへの保存をスキップ'
    )
    
    parser.add_argument(
        '--no-files',
        action='store_true',
        help='CSVファイルへの保存をスキップ'
    )
    
    parser.add_argument(
        '--no-visualize',
        action='store_true',
        help='可視化の生成をスキップ'
    )
    
    parser.add_argument(
        '--visualize-only',
        action='store_true',
        help='分析をスキップして、既存の結果から可視化のみ実行'
    )
    
    parser.add_argument(
        '--output',
        default='nf_auto_runs/analysis',
        help='出力ディレクトリ（デフォルト: nf_auto_runs/analysis）'
    )
    
    args = parser.parse_args()
    
    # モデルディレクトリの決定
    if args.model_dir:
        model_dir = args.model_dir
    else:
        # デフォルトパス（環境に応じて変更）
        model_dir = input("モデルディレクトリのパスを入力してください: ").strip()
        if not model_dir:
            print("✗ モデルディレクトリが指定されていません")
            return 1
    
    model_dir = Path(model_dir)
    if not model_dir.exists():
        print(f"✗ モデルディレクトリが見つかりません: {model_dir}")
        return 1
    
    print("\n" + "="*80)
    print("NeuralForecast Model Analyzer")
    print("="*80)
    print(f"モデルディレクトリ: {model_dir}")
    print(f"出力ディレクトリ: {args.output}")
    print(f"PostgreSQL保存: {'無効' if args.no_postgres else '有効'}")
    print(f"ファイル保存: {'無効' if args.no_files else '有効'}")
    print(f"可視化生成: {'無効' if args.no_visualize else '有効'}")
    print("="*80)
    
    # 可視化のみモード
    if args.visualize_only:
        print("\n可視化のみモード")
        return run_visualization_only(args.output)
    
    # 通常の分析実行
    try:
        from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
        
        analyzer = NeuralForecastAnalyzer(str(model_dir))
        results = analyzer.run_full_analysis(
            save_to_postgres=not args.no_postgres,
            save_to_files=not args.no_files,
            output_dir=args.output
        )
        
        if not results:
            print("\n✗ 分析に失敗しました")
            return 1
        
        # 可視化生成
        if not args.no_visualize:
            try:
                from analysis_visualizer import AnalysisVisualizer, MATPLOTLIB_AVAILABLE
                
                if MATPLOTLIB_AVAILABLE:
                    print("\n可視化を生成中...")
                    visualizer = AnalysisVisualizer(
                        results, 
                        output_dir=str(Path(args.output) / "visualizations")
                    )
                    visualizer.generate_all_visualizations()
                else:
                    print("\n⚠ matplotlib が見つかりません。可視化をスキップします")
                    print("  インストール: pip install matplotlib seaborn")
            except Exception as e:
                print(f"\n⚠ 可視化生成エラー: {e}")
        
        print("\n" + "="*80)
        print("✓ 全ての処理が完了しました")
        print("="*80)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_visualization_only(output_dir: str) -> int:
    """可視化のみ実行"""
    try:
        import pandas as pd
        from pathlib import Path
        from analysis_visualizer import AnalysisVisualizer, MATPLOTLIB_AVAILABLE
        
        if not MATPLOTLIB_AVAILABLE:
            print("✗ matplotlib が見つかりません")
            print("  インストール: pip install matplotlib seaborn")
            return 1
        
        output_dir = Path(output_dir)
        if not output_dir.exists():
            print(f"✗ 出力ディレクトリが見つかりません: {output_dir}")
            return 1
        
        # 最新のCSVファイルを読み込み
        results = {}
        table_names = [
            'model_profile', 'dataset_profile', 'training_state',
            'weight_statistics', 'model_complexity', 'parameter_sensitivity',
            'model_diagnosis', 'optimization_suggestions'
        ]
        
        csv_files = list(output_dir.glob("*.csv"))
        if not csv_files:
            print(f"✗ CSVファイルが見つかりません: {output_dir}")
            return 1
        
        for table_name in table_names:
            matching_files = [f for f in csv_files if f.name.startswith(table_name)]
            if matching_files:
                # 最新ファイル
                latest_file = sorted(matching_files)[-1]
                results[table_name] = pd.read_csv(latest_file)
                print(f"✓ 読み込み: {latest_file.name}")
        
        if not results:
            print("✗ 有効なデータが見つかりませんでした")
            return 1
        
        # 可視化実行
        visualizer = AnalysisVisualizer(results, output_dir=str(output_dir / "visualizations"))
        visualizer.generate_all_visualizations()
        
        print("\n✓ 可視化生成完了")
        return 0
        
    except Exception as e:
        print(f"\n✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
