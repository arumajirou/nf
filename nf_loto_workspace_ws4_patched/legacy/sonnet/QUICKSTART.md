# ⚡ クイックスタート

## 5分で始める NeuralForecast パラメータ抽出

### ステップ 1: インストール（1分）

```bash
pip install pandas openpyxl psycopg2-binary neuralforecast torch pyyaml
```

### ステップ 2: データベース設定（1分）

`db_config.py`を編集:

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'z',  # ← 変更
}
```

### ステップ 3: 接続テスト（30秒）

```bash
python setup_postgres.py test
```

### ステップ 4: モデル設定（30秒）

`neuralforecast_extractor_postgres.py`を編集:

```python
MODEL_DIR = r"C:\path\to\your\model"  # ← 変更
```

### ステップ 5: 実行（2分）

```bash
python neuralforecast_extractor_postgres.py
```

## 完了！ 🎉

結果を確認:

```bash
# ファイル出力
ls {MODEL_DIR}/extracted_params/

# PostgreSQL確認
python setup_postgres.py info
```

## トラブルシューティング

### 接続エラー？

```powershell
# PostgreSQLを再起動
Restart-Service postgresql-x64-17
```

### PostgreSQLなしで使用？

```python
extractor = NeuralForecastExtractor(MODEL_DIR)
results = extractor.run_full_extraction(save_to_postgres=False)
```

## 次のステップ

- **INSTALL.md**: 詳細なインストール手順
- **README_USAGE.md**: 完全なドキュメント
- **usage_examples.py**: 使用例コード
