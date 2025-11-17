# CHANGELOG

## v0.1.1 (internal refactor snapshot)

- `nf_loto_platform.db.loto_pg_store` の import パスを修正  
  - `from db_config import ...` → `from .db_config import ...`  
  - `from loto_etl import build_df_final` → `from .loto_etl import build_df_final`
- `nf_loto_platform.db.setup_postgres` の import パスを修正  
  - `from postgres_manager import ...` → `from .postgres_manager import ...`  
  - `from db_config import DB_CONFIG` → `from .db_config import DB_CONFIG`
- `legacy/nf_loto_webui/src/data_access/loto_repository.py` をベースに  
  `nf_loto_platform.db.loto_repository` を新規追加
- `legacy/nf_loto_webui/src/logging/db_logger.py` をベースに  
  `nf_loto_platform.logging_ext.db_logger` を新規追加
- `nf_loto_platform.ml.model_runner` の import を現行パッケージ階層に合わせて修正  
  - `src.data_access.loto_repository` → `nf_loto_platform.db.loto_repository`  
  - `src.logging.db_logger` → `nf_loto_platform.logging_ext.db_logger`  
  - `src.monitoring.*` → `nf_loto_platform.monitoring.*`
- プロジェクトルートに `pyproject.toml` を追加（src レイアウト・依存関係を定義）
- `report/` ディレクトリを作成し、pytest HTML レポートのサンプルと運用ガイドを追加
- `hist/` ディレクトリを作成し、本 CHANGELOG とリファクタリング計画を追加



## v0.1.2 (test hardening & monitoring API) - 2025-11-14

- `nf_loto_platform.monitoring.prometheus_metrics` に `observe_run_error` を追加し、
  `nf_loto_platform.ml.model_runner` からの呼び出しと静的 import テストの両方が通るように調整
- `tests/monitoring/test_prometheus_metrics.py` を拡張し、公開 API 契約
  (`init_metrics_server`, `observe_run_start`, `observe_run_end`, `observe_run_error`, `observe_train_step`)
  を検査するテストを追加
- `tests/ml/test_model_runner_contract.py` を新規追加し、
  `run_loto_experiment` / `sweep_loto_experiments` エントリポイントと
  `LotoExperimentResult` データクラスの存在を検証
- `tests/logging_ext/test_db_logger_contract.py` を新規追加し、
  DB ロガーの公開関数 (`log_run_start`, `log_run_end`, `log_run_error`) の存在を確認する
  軽量な契約テストを実装
- `tests/db/test_loto_pg_store_contract_extra.py` を新規追加し、
  `COLS` / `TABLE_NAME` の整合性および主要ヘルパ関数群の存在を確認
- `tests/db/test_loto_repository_contract.py` を新規追加し、
  LOTO 系テーブルアクセス用のユーティリティ API
  (`get_connection`, `list_loto_tables`, `load_panel_by_loto`) の存在を検査

## v0.1.2 (nonfunctional & integration tests)

- `tests/nonfunctional/test_reproducibility_seed.py` を本実装し、
  Python random / NumPy / (オプションで) torch の再現性スモークテストを追加
- `tests/nonfunctional/test_minimal_performance_smoke.py` を実装し、
  dummy AutoModel + stubbed NeuralForecast を用いた `run_loto_experiment` の
  性能スモークテストを追加
- `tests/integration/test_training_with_mock_db.py` を実装し、
  - mock DB (`loto_repository.load_panel_by_loto` のスタブ)
  - stubbed AutoModel (`automodel_builder.build_auto_model` / `build_neuralforecast` のスタブ)
  と `run_loto_experiment` を結合した軽量統合テストを追加
- 実 DB + 実 AutoModel を用いた長時間スモークテストをオプションとして追加
  (`NF_LP_REAL_DB_E2E=1` がセットされた環境でのみ実行)


## v0.1.3 (e2e & webui & features tests, skip 解消)

- legacy training パイプライン (`run_legacy_nf_auto_runner`) をテストしやすい形に拡張し、
  pipelines / e2e テストを本実装化。
- webui モジュールに `is_webui_available` を追加し、WebUI 関連テストを skip から移行。
- features モジュールに `add_lag_feature` を実装し、ユニットテスト・統合テストを追加。
- `tests/static/test_all_modules_importable.py` から `pytest.skip` を排除しつつ、
  全モジュール import テストを維持。
- プレースホルダだった複数テストを本実装に置き換え、標準実行時に skip 0 本を目指す構成に整理。

## v0.2.0 (ml_analysis 拡張と実験トラッキング土台の追加)

- `nf_loto_platform.ml_analysis.metrics` を追加し、MAE/RMSE/sMAPE/pinball loss/coverage を共通実装。
- `nf_loto_platform.ml_analysis.reporting` を追加し、予測結果 DataFrame からのメトリクス算出と
  HTML/JSON レポート出力ユーティリティを実装。
- `nf_loto_platform.ml_analysis.experiment_tracking` を追加し、MLflow への
  params/tags/metrics 記録を no-op セーフな薄いラッパーとして提供。
- `tests/ml_analysis` 配下に metrics/reporting/experiment_tracking の単体テストを追加し、
  予測精度評価レイヤの回帰検出を可能にした。
