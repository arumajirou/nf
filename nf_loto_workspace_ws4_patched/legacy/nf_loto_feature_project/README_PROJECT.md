# nf_loto_feature_project

ロト系データを対象に、NeuralForecast の外生変数 (futr/hist/stat) を自動生成し、
PostgreSQL に格納するためのプロジェクトです。

* `streamlit` ベースの Web UI (`streamlit_app.py`)
* 特徴量生成モジュール群 (`features/`)
* テーブル確認用ノートブック (`notebooks/`)
* 各種解説用ドキュメント (`docs/`)

既存の `db_config.py`, `postgres_manager.py`, `loto_etl*.py`, `loto_pg_store.py`
をそのまま利用します。
