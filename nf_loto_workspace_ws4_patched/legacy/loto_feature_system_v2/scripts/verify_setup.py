#!/usr/bin/env python
"""
セットアップ確認スクリプト
システムの基本的な動作を確認します
"""
import sys
import os

def check_python_version():
    """Pythonバージョンチェック"""
    print("=== Pythonバージョン ===")
    print(f"Python {sys.version}")
    if sys.version_info < (3, 9):
        print("❌ Python 3.9以上が必要です")
        return False
    print("✓ OK")
    return True

def check_imports():
    """必須パッケージのインポートチェック"""
    print("\n=== 必須パッケージチェック ===")
    required_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('yaml', 'PyYAML'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('tqdm', 'tqdm'),
    ]
    
    all_ok = True
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"❌ {package_name} がインストールされていません")
            print(f"   pip install {package_name.lower()}")
            all_ok = False
    
    return all_ok

def check_optional_imports():
    """オプションパッケージのインポートチェック"""
    print("\n=== オプションパッケージチェック（GPU等） ===")
    optional_packages = [
        ('cudf', 'cudf (GPU加速)'),
        ('cuml', 'cuML (GPU機械学習)'),
        ('jpholiday', 'jpholiday (日本の祝日)'),
    ]
    
    for module_name, package_name in optional_packages:
        try:
            __import__(module_name)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"- {package_name} (未インストール - オプション)")

def check_project_structure():
    """プロジェクト構造チェック"""
    print("\n=== プロジェクト構造チェック ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    required_dirs = [
        'src',
        'src/core',
        'src/pipelines',
        'config',
        'scripts',
        'tests',
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"✓ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ が見つかりません")
            all_ok = False
    
    return all_ok

def check_config_files():
    """設定ファイルチェック"""
    print("\n=== 設定ファイルチェック ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    config_files = [
        ('config/db_config.yaml.template', True),
        ('config/db_config.yaml', False),
        ('config/default_config.yaml', True),
        ('config/pipeline_config.yaml', True),
    ]
    
    for config_file, required in config_files:
        config_path = os.path.join(base_dir, config_file)
        if os.path.exists(config_path):
            print(f"✓ {config_file}")
        else:
            if required:
                print(f"❌ {config_file} が見つかりません")
            else:
                print(f"- {config_file} (未作成 - 必要に応じて作成)")

def check_source_files():
    """ソースファイルチェック"""
    print("\n=== ソースファイルチェック ===")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    source_files = [
        'src/core/database_manager.py',
        'src/core/data_loader.py',
        'src/pipelines/base_pipeline.py',
        'src/pipelines/basic_stats.py',
        'src/pipelines/calendar_features.py',
    ]
    
    all_ok = True
    for source_file in source_files:
        source_path = os.path.join(base_dir, source_file)
        if os.path.exists(source_path):
            print(f"✓ {source_file}")
        else:
            print(f"❌ {source_file} が見つかりません")
            all_ok = False
    
    return all_ok

def main():
    """メイン処理"""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   宝くじ時系列特徴量生成システム - セットアップ確認      ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    checks = [
        check_python_version(),
        check_imports(),
        check_project_structure(),
        check_config_files(),
        check_source_files(),
    ]
    
    check_optional_imports()
    
    print("\n" + "="*60)
    if all(checks):
        print("✓ セットアップ確認完了！")
        print("\n次のステップ:")
        print("1. config/db_config.yaml を作成して設定")
        print("2. python scripts/setup_database.py でテーブル作成")
        print("3. python scripts/generate_features_simple.py で特徴量生成")
        return 0
    else:
        print("❌ セットアップに問題があります")
        print("上記のエラーを修正してください")
        return 1

if __name__ == "__main__":
    sys.exit(main())
