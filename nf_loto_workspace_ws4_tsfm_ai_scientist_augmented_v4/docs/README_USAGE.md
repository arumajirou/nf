# NeuralForecast パラメータ抽出・PostgreSQL統合ツール

## 概要

NeuralForecastモデルから全パラメータを抽出し、PostgreSQLデータベースに自動的に保存するツールです。

### 主な機能

1. **完全なパラメータ抽出**: モデル、PKL、CKPT、JSON、YAMLファイルから全パラメータを抽出
2. **PostgreSQL統合**: カテゴリごとにテーブルを自動作成し、データを保存
3. **個別ファイル保存**: 処理中断対策として各ステップごとに結果を保存
4. **エラーハンドリング**: 堅牢なエラー処理とログ機能
5. **柔軟な出力形式**: CSV、Excel、JSON、PostgreSQLに対応

## 必要要件

### Pythonパッケージ

```bash
pip install pandas openpyxl psycopg2-binary neuralforecast torch pyyaml
```

### PostgreSQL

- PostgreSQL 12以降
- データベースアクセス権限

## ファイル構成

```
neuralforecast_extractor_postgres.py  # メインスクリプト
postgres_manager.py                    # PostgreSQL操作クラス
db_config.py                          # データベース設定
setup_postgres.py                     # PostgreSQLセットアップスクリプト
README_USAGE.md                       # このファイル
```

## セットアップ

### 1. データベース設定

`db_config.py`を編集して、PostgreSQL接続情報を設定:

```python
DB_CONFIG = {
    'host': '127.0.0.1',      # データベースホスト
    'port': 5432,             # ポート番号
    'database': 'postgres',   # データベース名
    'user': 'postgres',       # ユーザー名
    'password': 'your_password',  # パスワード
}
```

### 2. データベース初期化（オプション）

```bash
python setup_postgres.py
```

これにより、必要なスキーマと権限が設定されます。

## 使い方

### 基本的な使い方

```python
from neuralforecast_extractor_postgres import NeuralForecastExtractor

# モデルディレクトリを指定
MODEL_DIR = r"C:\path\to\your\model"

# 抽出実行
extractor = NeuralForecastExtractor(MODEL_DIR)
results = extractor.run_full_extraction(
    save_to_postgres=True  # PostgreSQLに保存
)

# 結果の取得
df_long = results['df_long']
df_wide_params = results['df_wide_params']
all_params = results['all_params']
```

### ステップごとの実行

```python
# 1. 初期化
extractor = NeuralForecastExtractor(MODEL_DIR)
extractor.scan_files()
extractor.load_model()

# 2. パラメータ抽出（個別実行可能）
extractor.extract_model_params()
extractor.extract_pkl_params()
extractor.extract_ckpt_params()
extractor.extract_json_params()
extractor.extract_yaml_params()

# 3. DataFrame作成
extractor.create_dataframes()

# 4. ファイル保存
extractor.save_all_to_files()

# 5. PostgreSQL保存
extractor.save_to_postgres()
```

### データフィルタリング

```python
from neuralforecast_extractor_postgres import filter_params_by_category, search_params, get_param_value

# カテゴリでフィルタ
model_params = filter_params_by_category(df_long, 'model')
hparams = filter_params_by_category(df_long, 'hparams')

# キーワード検索
dropout_params = search_params(df_long, 'dropout')
learning_params = search_params(df_long, 'learning')

# 特定パラメータの値を取得
h_value = get_param_value(df_long, 'h')
lr_value = get_param_value(df_long, 'learning_rate')
```

## 出力形式

### ファイル出力

すべてのファイルは`{MODEL_DIR}/extracted_params/`に保存されます:

```
extracted_params/
├── params_long_20250101_120000.csv          # 縦持ち形式（推奨）
├── params_wide_20250101_120000.csv          # 横持ち形式（値）
├── params_sources_20250101_120000.csv       # 横持ち形式（ソース）
├── params_all_20250101_120000.xlsx          # Excel形式（全シート）
├── params_raw_20250101_120000.json          # 生データ（JSON）
├── step_model_20250101_120000.json          # モデルステップの結果
├── step_pkl_20250101_120000.json            # PKLステップの結果
├── step_ckpt_20250101_120000.json           # CKPTステップの結果
├── step_json_20250101_120000.json           # JSONステップの結果
├── step_yaml_20250101_120000.json           # YAMLステップの結果
└── postgres_table_mapping.json              # PostgreSQLテーブルマッピング
```

### PostgreSQL出力

#### テーブル命名規則

カテゴリ名から自動的にテーブル名を生成:

- `A_model` → `nf_model`
- `D_hparams` → `nf_hparams`
- `C_config` → `nf_config`
- `F_pkl` → `nf_pkl`

#### テーブル構造

各テーブルは以下の構造を持ちます:

```sql
CREATE TABLE nf_model (
    id SERIAL PRIMARY KEY,
    batch_size INTEGER,
    learning_rate REAL,
    max_steps INTEGER,
    ...
    sources JSONB,              -- 各パラメータのソース情報
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### データ確認

```sql
-- テーブル一覧
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE 'nf_%';

-- モデルパラメータ確認
SELECT * FROM nf_model;

-- ハイパーパラメータ確認
SELECT * FROM nf_hparams;

-- ソース情報の確認
SELECT sources FROM nf_model;
```

## データ構造

### 縦持ち形式（df_long）

| Category | Parameter | Value | Source |
|----------|-----------|-------|--------|
| A_model | model.batch_size | 32 | model.__dict__ |
| A_model | model.learning_rate | 0.001 | model.__dict__ |
| D_hparams | model.hparams.h | 1 | model.hparams |

### カテゴリ分類

- **A_model**: モデル実体の属性
- **B_class_default**: クラスのデフォルト値
- **C_config**: configuration.pkl の設定
- **D_hparams**: ハイパーパラメータ
- **E_pytorch**: PyTorchモデル情報
- **F_pkl**: PKLファイルの内容
- **G_ckpt**: CKPTファイルの内容
- **H_json**: JSONファイルの内容
- **I_yaml**: YAMLファイルの内容

## トラブルシューティング

### PostgreSQL接続エラー

```
✗ PostgreSQL接続失敗: connection refused
```

**解決方法**:
1. PostgreSQLサービスが起動しているか確認
2. `db_config.py`の接続情報が正しいか確認
3. ファイアウォール設定を確認

### モジュールインポートエラー

```
⚠ PostgreSQLマネージャーが利用できません
```

**解決方法**:
```bash
pip install psycopg2-binary
```

### モデルロードエラー

```
✗ モデルロード失敗
```

**解決方法**:
1. モデルディレクトリのパスが正しいか確認
2. 必要なパッケージがインストールされているか確認
3. モデルファイルが破損していないか確認

### 権限エラー

```
✗ データ挿入失敗: permission denied
```

**解決方法**:
```sql
GRANT ALL PRIVILEGES ON SCHEMA public TO your_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
```

## 高度な使い方

### カスタムデータベース設定

```python
custom_db_config = {
    'host': 'remote-server.example.com',
    'port': 5432,
    'database': 'neuralforecast_db',
    'user': 'ml_user',
    'password': 'secure_password',
}

extractor.save_to_postgres(db_config=custom_db_config)
```

### 特定のステップのみ実行

```python
# モデルパラメータのみ抽出
extractor = NeuralForecastExtractor(MODEL_DIR)
extractor.scan_files()
extractor.load_model()
extractor.extract_model_params()
extractor.create_dataframes()
extractor.save_all_to_files()
```

### PostgreSQLからデータを読み込み

```python
from postgres_manager import PostgreSQLManager

with PostgreSQLManager() as db:
    # テーブル一覧を取得
    tables = db.list_tables()
    
    # テーブル情報を取得
    table_info = db.get_table_info('nf_model')
    print(table_info)
```

## 貢献

バグ報告や機能リクエストは、Issueを作成してください。

## ライセンス

MIT License

## 更新履歴

### v2.0.0 (2025-01-11)
- PostgreSQL統合機能の追加
- 個別ファイル保存機能の追加
- エラーハンドリングの強化
- 段階的実行機能の追加

### v1.0.0 (2025-01-10)
- 初版リリース
- 基本的なパラメータ抽出機能
