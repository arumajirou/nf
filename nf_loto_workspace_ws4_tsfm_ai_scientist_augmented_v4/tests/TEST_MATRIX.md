# nf_loto_platform TEST_MATRIX（ファイル別テスト設計）

このファイルは、nf_loto_platform の各モジュール／ファイルに対して
「どのテストファイルで何を確認するか」を一覧化したものです。

## 1. core

- `src/nf_loto_platform/core/settings.py`
  - `tests/core/test_settings.py`
    - `load_db_config()` の返り値が dict であること
    - `config/db.yaml` と `db.yaml.template` のフォールバック挙動
    - 不正な YAML の扱い（仕様に応じて ConfigError など）

- `src/nf_loto_platform/core/exceptions.py`
  - `tests/core/test_exceptions.py`
    - 例外クラスが Exception を継承していること
    - メッセージが保持されること
    - pipelines 等で RunError が利用されていること

## 2. db

- `db/db_config.py`
  - `tests/db/test_db_config.py`
    - 設定の読み込みと必須キーの検証

- `db/postgres_manager.py`
  - `tests/db/test_postgres_manager_contract.py`
    - 接続コンテキストマネージャの挙動
    - SQL ラッパーの基本挙動

- `db/loto_pg_store.py`
  - `tests/db/test_loto_pg_store_contract.py`
    - 特徴量テーブル保存インタフェースの契約

- `db/loto_etl.py`, `db/loto_etl_updated.py`
  - `tests/db/test_loto_etl_pipeline.py`
    - ETL の入出力スキーマ
    - 日付範囲フィルタなど設定依存の挙動

- `db/setup_postgres.py`
  - `tests/db/test_setup_postgres.py`
    - `sql/*.sql` の適用確認（モックベース）

## 3. db_metadata

- `db_metadata/schema_definitions.py`
  - `tests/db_metadata/test_schema_definitions.py`
    - SQL DDL（`sql/*.sql`）との整合性

## 4. features

- `features/` 配下の各モジュール
  - `tests/features/test_feature_config_contract.py`
  - `tests/features/test_futr_hist_stat_features_contract.py`
  - `tests/features/test_cleaning_contract.py`
    - 特徴量名・prefix・NaN 処理などの契約チェック
    - ※ 実装がまだ無い場合は `pytest.skip` でスキップしつつ枠だけ確保

## 5. logging_ext

- `logging_ext/mlflow_logger.py`
  - `tests/logging_ext/test_mlflow_logger.py`
    - mlflow API 呼び出しのモック検証

- `logging_ext/wandb_logger.py`
  - `tests/logging_ext/test_wandb_logger.py`
    - Weights & Biases 連携の有効・無効モードの確認

## 6. ml

- `ml/automodel_builder.py`
  - `tests/ml/test_automodel_builder.py`
    - モデル名／設定から Auto* モデルが構築されるか
    - 不正なモデル名に対するエラー

- `ml/model_runner.py`
  - `tests/ml/test_model_runner.py`
    - 小さなデータセットに対する学習フローの通し
    - 不正データに対する DataError など

- `ml/model_registry.py`
  - `tests/ml/test_model_registry.py`
    - モデル登録・ロードの round-trip

## 7. monitoring

- `monitoring/resource_monitor.py`
  - `tests/monitoring/test_resource_monitor.py`
    - CPU/メモリ/GPU 情報の取得スキーマ

- `monitoring/prometheus_metrics.py`
  - `tests/monitoring/test_prometheus_metrics.py`
    - メトリクス登録・更新の基本挙動

## 8. pipelines

- `pipelines/training_pipeline.py`
  - `tests/pipelines/test_training_pipeline.py`
    - legacy ランナーのパス解決
    - 例外時の RunError

## 9. reports

- `reports/html_reporter.py`
  - `tests/reports/test_html_reporter.py`
    - HTML 文字列生成
    - ファイル出力の確認

## 10. webui

- `apps/webui_streamlit/streamlit_app.py`
  - `tests/e2e/test_webui_smoke.py`
    - Streamlit アプリの起動スモーク

## 11. integration / e2e / nonfunctional / static

- `tests/integration/test_feature_pipeline_integration.py`
  - db ↔ features の結合テスト
- `tests/integration/test_training_with_mock_db.py`
  - ml ↔ logging ↔ db_metadata の結合テスト
- `tests/e2e/test_cli_nf_auto_runner_e2e.py`
  - CLI 経由でパイプラインが完走するか（小規模設定）
- `tests/nonfunctional/test_reproducibility_seed.py`
  - 同一 seed での結果の安定性
- `tests/nonfunctional/test_minimal_performance_smoke.py`
  - 極小ジョブの実行時間・リソース使用の簡易チェック
- `tests/static/test_py_compile_all.py`
  - src/apps/tests 配下の Python ファイルの構文エラー検出
- `tests/static/test_docs_references.py`
  - docs 内の主要ファイル・参照パスの存在確認

この TEST_MATRIX は、テスト追加時の「どこに置くべきか」「何を確認すべきか」を
細かい粒度で示すためのガイドラインとして利用します。
