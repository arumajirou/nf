# 📦 インストールガイド

## システム要件

### 必須
- Python 3.8以降
- PostgreSQL 12以降（PostgreSQLに保存する場合）
- 空きディスク容量: 最低1GB

### 推奨
- Python 3.10以降
- PostgreSQL 15以降
- メモリ: 8GB以上
- GPU（PyTorchモデルを扱う場合）

## インストール手順

### 1. Pythonパッケージのインストール

#### 基本パッケージ（PostgreSQL統合なし）

```bash
pip install pandas openpyxl neuralforecast torch pyyaml
```

#### 完全版（PostgreSQL統合あり）

```bash
pip install pandas openpyxl psycopg2-binary neuralforecast torch pyyaml
```

#### 仮想環境を使用する場合（推奨）

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# パッケージのインストール
pip install pandas openpyxl psycopg2-binary neuralforecast torch pyyaml
```

### 2. PostgreSQLのインストール（Windows）

#### 方法1: 公式インストーラー（推奨）

1. [PostgreSQL公式サイト](https://www.postgresql.org/download/windows/)からインストーラーをダウンロード
2. インストーラーを実行
3. デフォルト設定で進める
4. スーパーユーザー（postgres）のパスワードを設定
5. ポート番号は5432のまま

#### 方法2: Chocolatey

```powershell
# 管理者PowerShell
choco install postgresql
```

#### PostgreSQLサービスの起動確認

```powershell
# サービス一覧確認
Get-Service postgresql-x64-17

# サービス起動
Start-Service postgresql-x64-17

# または
Restart-Service postgresql-x64-17
```

### 3. ツールのセットアップ

#### ファイルの配置

すべてのファイルを作業ディレクトリに配置:

```
your_project/
├── db_config.py                          # ← 編集必須
├── postgres_manager.py
├── neuralforecast_extractor_postgres.py  # ← 編集必須
├── setup_postgres.py
├── usage_examples.py
└── README_USAGE.md
```

#### データベース設定の編集

`db_config.py`を開いて、接続情報を編集:

```python
DB_CONFIG = {
    'host': '127.0.0.1',          # localhost
    'port': 5432,                 # デフォルトポート
    'database': 'postgres',       # データベース名
    'user': 'postgres',           # ユーザー名
    'password': 'your_password',  # ← パスワードを変更
}
```

### 4. 接続テスト

```bash
python setup_postgres.py test
```

成功例:
```
================================================================================
PostgreSQL 接続テスト
================================================================================

接続情報:
  Host: 127.0.0.1
  Port: 5432
  Database: postgres
  User: postgres

✓ 接続成功

PostgreSQL バージョン:
  PostgreSQL 17.x on x86_64-pc-windows-msvc, compiled by ...
```

失敗例と解決方法:
```
✗ 接続失敗: connection refused

→ 解決方法:
1. PostgreSQLサービスを起動
2. ファイアウォール設定を確認
3. pg_hba.confを確認
```

### 5. 初回実行

#### 5-1. モデルディレクトリを設定

`neuralforecast_extractor_postgres.py`を編集:

```python
# 最下部のMODEL_DIRを変更
MODEL_DIR = r"C:\Users\yourname\path\to\your\model"
```

#### 5-2. 実行

```bash
python neuralforecast_extractor_postgres.py
```

または、Pythonスクリプトから:

```python
from neuralforecast_extractor_postgres import NeuralForecastExtractor

MODEL_DIR = r"C:\path\to\your\model"
extractor = NeuralForecastExtractor(MODEL_DIR)
results = extractor.run_full_extraction(save_to_postgres=True)
```

## トラブルシューティング

### エラー1: psycopg2がインストールできない

```
ERROR: Failed building wheel for psycopg2
```

**解決方法**:

```bash
# バイナリ版をインストール
pip install psycopg2-binary

# または、Visual C++ビルドツールをインストール後、再試行
pip install psycopg2
```

### エラー2: PostgreSQL接続エラー

```
✗ PostgreSQL接続失敗: FATAL: password authentication failed
```

**解決方法**:

1. パスワードが正しいか確認
2. `pg_hba.conf`を確認:
   ```
   # IPv4 local connections:
   host    all             all             127.0.0.1/32            scram-sha-256
   host    all             all             ::1/128                 scram-sha-256
   ```
3. PostgreSQLを再起動:
   ```powershell
   Restart-Service postgresql-x64-17
   ```

### エラー3: NeuralForecastモデルロードエラー

```
✗ モデルロード失敗: No module named 'neuralforecast'
```

**解決方法**:

```bash
pip install neuralforecast
```

### エラー4: メモリエラー

```
MemoryError: Unable to allocate array
```

**解決方法**:

1. バッチサイズを減らす
2. 不要なプロセスを終了
3. より大きいメモリのマシンを使用

### エラー5: 権限エラー

```
✗ データ挿入失敗: permission denied for table nf_model
```

**解決方法**:

```sql
-- psqlで実行
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
```

## PostgreSQLなしで使用する場合

PostgreSQLをインストールせずに使用する場合:

### パッケージインストール

```bash
# psycopg2は不要
pip install pandas openpyxl neuralforecast torch pyyaml
```

### 実行方法

```python
from neuralforecast_extractor_postgres import NeuralForecastExtractor

MODEL_DIR = r"C:\path\to\your\model"
extractor = NeuralForecastExtractor(MODEL_DIR)

# PostgreSQL保存をスキップ
results = extractor.run_full_extraction(save_to_postgres=False)
```

出力ファイルのみが生成されます:
- CSV形式（縦持ち・横持ち）
- Excel形式
- JSON形式

## 依存関係の完全なリスト

### 必須パッケージ

```
pandas>=1.3.0
openpyxl>=3.0.0
```

### オプションパッケージ

```
psycopg2-binary>=2.9.0    # PostgreSQL統合用
neuralforecast>=1.0.0     # モデルロード用
torch>=1.10.0             # モデルロード用
pyyaml>=5.4.0             # YAML解析用
```

### requirements.txtの例

```txt
# 基本パッケージ
pandas>=1.3.0
openpyxl>=3.0.0

# PostgreSQL統合
psycopg2-binary>=2.9.0

# NeuralForecast
neuralforecast>=1.0.0
torch>=1.10.0

# その他
pyyaml>=5.4.0
```

インストール:

```bash
pip install -r requirements.txt
```

## 次のステップ

インストールが完了したら:

1. **README_USAGE.md**: 詳細な使い方
2. **usage_examples.py**: サンプルコード
3. **setup_postgres.py**: データベース管理

## サポート

問題が解決しない場合:

1. エラーメッセージ全文を確認
2. `python --version`と`pip list`で環境を確認
3. `setup_postgres.py test`で接続テスト
