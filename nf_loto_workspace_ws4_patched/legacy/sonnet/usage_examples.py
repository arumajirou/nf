"""
使用例スクリプト
NeuralForecastパラメータ抽出の様々な使い方を示すサンプルコード
"""

from neuralforecast_extractor_postgres import (
    NeuralForecastExtractor,
    filter_params_by_category,
    search_params,
    get_param_value
)
from postgres_manager import PostgreSQLManager
import pandas as pd

# =============================================================================
# 例1: 基本的な使い方（全自動）
# =============================================================================

def example_1_basic():
    """基本的な使い方: 全自動でパラメータ抽出とPostgreSQL保存"""
    print("\n" + "="*80)
    print("例1: 基本的な使い方（全自動）")
    print("="*80)
    
    # モデルディレクトリを指定
    MODEL_DIR = r"C:\path\to\your\model"
    
    # 抽出実行
    extractor = NeuralForecastExtractor(MODEL_DIR)
    results = extractor.run_full_extraction(
        save_to_postgres=True  # PostgreSQLに保存
    )
    
    # 結果の取得
    df_long = results['df_long']
    print(f"\n✓ 総パラメータ数: {len(df_long)}")
    print(f"✓ 出力ディレクトリ: {results['output_dir']}")


# =============================================================================
# 例2: ステップごとの実行（詳細制御）
# =============================================================================

def example_2_step_by_step():
    """ステップごとの実行: 各処理を個別に制御"""
    print("\n" + "="*80)
    print("例2: ステップごとの実行（詳細制御）")
    print("="*80)
    
    MODEL_DIR = r"C:\path\to\your\model"
    
    # 1. 初期化
    extractor = NeuralForecastExtractor(MODEL_DIR)
    
    # 2. ファイルスキャン
    extractor.scan_files()
    
    # 3. モデルロード
    if extractor.load_model():
        # 4. パラメータ抽出（必要なものだけ）
        extractor.extract_model_params()
        extractor.extract_pkl_params()
        # CKPT、JSON、YAMLはスキップ
        
        # 5. DataFrame作成
        extractor.create_dataframes()
        
        # 6. ファイル保存のみ（PostgreSQLには保存しない）
        extractor.save_all_to_files()
        
        print("\n✓ パラメータ抽出完了（PostgreSQLには保存していません）")


# =============================================================================
# 例3: データフィルタリングと検索
# =============================================================================

def example_3_filtering():
    """データフィルタリングと検索"""
    print("\n" + "="*80)
    print("例3: データフィルタリングと検索")
    print("="*80)
    
    MODEL_DIR = r"C:\path\to\your\model"
    
    extractor = NeuralForecastExtractor(MODEL_DIR)
    results = extractor.run_full_extraction(save_to_postgres=False)
    df_long = results['df_long']
    
    # カテゴリでフィルタ
    print("\n[A] モデルパラメータのみ表示:")
    model_params = filter_params_by_category(df_long, 'model')
    print(model_params.head(10))
    
    print("\n[B] ハイパーパラメータのみ表示:")
    hparams = filter_params_by_category(df_long, 'hparams')
    print(hparams.head(10))
    
    # キーワード検索
    print("\n[C] 'learning'を含むパラメータ:")
    learning_params = search_params(df_long, 'learning')
    print(learning_params)
    
    print("\n[D] 'dropout'を含むパラメータ:")
    dropout_params = search_params(df_long, 'dropout')
    print(dropout_params)
    
    # 特定パラメータの値を取得
    print("\n[E] 特定パラメータの値取得:")
    h_value = get_param_value(df_long, 'h')
    print(f"  h = {h_value}")
    
    lr_value = get_param_value(df_long, 'learning_rate')
    print(f"  learning_rate = {lr_value}")
    
    batch_size = get_param_value(df_long, 'batch_size')
    print(f"  batch_size = {batch_size}")


# =============================================================================
# 例4: カスタムデータベース設定
# =============================================================================

def example_4_custom_db():
    """カスタムデータベース設定"""
    print("\n" + "="*80)
    print("例4: カスタムデータベース設定")
    print("="*80)
    
    MODEL_DIR = r"C:\path\to\your\model"
    
    # カスタムDB設定
    custom_db_config = {
        'host': 'remote-server.example.com',
        'port': 5432,
        'database': 'neuralforecast_db',
        'user': 'ml_user',
        'password': 'secure_password',
    }
    
    extractor = NeuralForecastExtractor(MODEL_DIR)
    
    # まずパラメータ抽出
    extractor.scan_files()
    extractor.load_model()
    extractor.extract_model_params()
    extractor.extract_pkl_params()
    extractor.create_dataframes()
    extractor.save_all_to_files()
    
    # カスタムDB設定で保存
    extractor.save_to_postgres(db_config=custom_db_config)


# =============================================================================
# 例5: PostgreSQLからデータを読み込み
# =============================================================================

def example_5_read_from_postgres():
    """PostgreSQLからデータを読み込む"""
    print("\n" + "="*80)
    print("例5: PostgreSQLからデータを読み込み")
    print("="*80)
    
    with PostgreSQLManager() as db:
        # テーブル一覧を取得
        tables = db.list_tables()
        print(f"\nテーブル一覧:")
        for table in tables:
            if table.startswith('nf_'):
                print(f"  - {table}")
        
        # モデルパラメータテーブルの情報を取得
        if 'nf_model' in tables:
            print(f"\nnf_model テーブル情報:")
            table_info = db.get_table_info('nf_model')
            print(table_info)
            
            # データを読み込み
            db.cursor.execute("SELECT * FROM nf_model")
            row = db.cursor.fetchone()
            
            if row:
                print(f"\nサンプルデータ:")
                columns = [desc[0] for desc in db.cursor.description]
                for col, val in zip(columns[:10], row[:10]):  # 最初の10カラムのみ
                    print(f"  {col}: {val}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("NeuralForecast パラメータ抽出 - 使用例")
    print("="*80)
    print("\n実行する例を選択してください:")
    print("  1: 基本的な使い方（全自動）")
    print("  2: ステップごとの実行（詳細制御）")
    print("  3: データフィルタリングと検索")
    print("  4: カスタムデータベース設定")
    print("  5: PostgreSQLからデータを読み込み")
    
    choice = input("\n番号を入力 (1-5): ").strip()
    
    if choice == '1':
        example_1_basic()
    elif choice == '2':
        example_2_step_by_step()
    elif choice == '3':
        example_3_filtering()
    elif choice == '4':
        example_4_custom_db()
    elif choice == '5':
        example_5_read_from_postgres()
    else:
        print(f"\n✗ 無効な選択: {choice}")
