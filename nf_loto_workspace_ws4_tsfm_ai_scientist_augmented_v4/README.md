# nf_loto_platform — NeuralForecast Loto Suite 統合システム

`nf_loto_platform` は、C:\nf 配下に存在していた複数のロト実験プロジェクトを 1 つの統合システムとして再構築したものです。
NeuralForecast ライブラリを中核に、特徴量生成・ハイパーパラメータ探索（AutoML）・実験管理・分析・Web UI を一体化した
「ロト予測実験プラットフォーム」を提供します。

この README は、システム全体の構造と役割、主要コンポーネント、実行方法の概要をまとめたものです。
詳細な API 仕様や設計思想は `docs/` 以下のドキュメントを参照してください。


## 1. 全体構成

ディレクトリ構造（トップレベル）は次のようになっています。

```text
nf_loto_platform/
  README.md
  .vscode/                 # VS Code 用の設定
  apps/                    # アプリケーション入口（主に Web UI）
  config/                  # DB・特徴量・WebUI などの設定ファイル
  docs/                    # 設計書・ユーザーガイド・技術ノート
  legacy/                  # 元の C:\nf プロジェクト一式（バックアップ／参照用）
  notebooks/               # チュートリアル／検証用ノートブック
  sql/                     # nf_* メタデータテーブル定義・分析用 SQL
  src/
    nf_loto_platform/      # 統合 Python パッケージ
  tests/                   # pytest 用のテストコード
```

各ディレクトリの役割は以下の通りです。

- `apps/`
  - `webui_streamlit/` : Streamlit ベースの Web UI 一式。
    - `streamlit_app.py` : Web UI のメインエントリ。
    - `nf_auto_runner_full.py` : モデル実行パイプラインを起動するラッパ。
- `config/`
  - ロト用特徴量システム・汎用 Web UI・DB 接続設定などを YAML 形式で管理。
- `docs/`
  - AutoModelFactory 設計、NeuralForecast/Ray/Optuna/MLflow のメモ、特徴量システム設計書など。
- `legacy/`
  - 元の `loto_feature_system_v2`, `nf_loto_feature_project`, `nf_loto_webui`,
    `neuralforecast-automl-webui`, `sonnet` などをそのまま保持した領域。
    実運用では `src/nf_loto_platform/` 側のコードを優先しつつ、参考実装として参照します。
- `notebooks/`
  - `nf_loto_platform_intro.ipynb` など、環境確認やチュートリアル用ノートブック。
- `sql/`
  - 実験メタデータテーブル（`nf_model_runs` など）の DDL・分析クエリ。
- `src/nf_loto_platform/`
  - 統合 Python パッケージ本体。特徴量生成、モデル実行、ログ・モニタリングなどのコアロジックを担当します。
- `tests/`
  - パッケージの import や設定読み込みなどのスモークテスト。


## 2. 統合パッケージ構造（src/nf_loto_platform）

統合パッケージの概略構成は次の通りです。

```text
src/nf_loto_platform/
  __init__.py
  core/
    settings.py
    exceptions.py
  db/
    db_config.py
    loto_etl.py
    loto_etl_updated.py
    loto_pg_store.py
    postgres_manager.py
    setup_postgres.py
  features/
    cleaning.py
    feature_config.py
    futr_features.py
    gpu_utils.py
    hist_features.py
    registry.py
    stat_features.py
    y_representation.py
  pipelines/
    training_pipeline.py
  ml/
    automodel_builder.py
    model_registry.py
    model_runner.py
  logging_ext/
    mlflow_logger.py
    wandb_logger.py
  monitoring/
    prometheus_metrics.py
    resource_monitor.py
  reports/
    html_reporter.py
  db_metadata/
    schema_definitions.py
  ml_analysis/
    # （将来の分析機能用に予約）
  webui/
    # （Web UI 用ヘルパー拡張用に予約）
```

各サブパッケージの責務は以下の通りです。

### 2.1 core

- `core/settings.py`
  - プロジェクトルート `BASE_DIR` の解決。
  - `config/db.yaml` または `config/db.yaml.template` から DB 設定を読み込む `load_db_config()` を提供。
  - 今後、共通設定ローダーとして拡張する想定です。
- `core/exceptions.py`
  - 共通例外クラス：
    - `ConfigError` : 設定値の不整合など。
    - `DataError`   : データの欠損・型不整合など。
    - `RunError`    : パイプライン実行時のラップエラー。

### 2.2 db

- `db_config.py`
  - DB 接続設定のラッパーロジック。
- `postgres_manager.py`
  - PostgreSQL への接続、基本的な CRUD・テーブル管理。
- `loto_etl.py`, `loto_etl_updated.py`
  - ロト系テーブルからの ETL パイプライン（元 `loto_feature_system_v2` のロジックを移植）。
- `loto_pg_store.py`
  - 特徴量テーブルや中間生成物を PostgreSQL に格納するためのユーティリティ。
- `setup_postgres.py`
  - 初期テーブル作成・接続確認などのセットアップスクリプト。

これらにより、「DB から生データを取り出し、特徴量生成パイプラインへ渡す」までの責務を担当します。

### 2.3 features

- `futr_features.py`
  - 未来既知特徴（カレンダー情報・曜日・祝日など）の生成。
- `hist_features.py`
  - ラグ・移動平均・ローリング統計などの履歴特徴の生成。
- `stat_features.py`
  - シリーズごとの静的統計量（平均・分散・最大値等）を生成。
- `feature_config.py`
  - 有効にする特徴量セットの定義・管理。
- `cleaning.py`
  - NaN / inf / 外れ値の処理など、時系列データのクリーニング。
- `gpu_utils.py`
  - GPU の有無検出・バッチサイズ調整などの補助。
- `y_representation.py`
  - 目的変数 y の表現（例：異常スコアなど）を拡張するためのモジュール。
- `registry.py`
  - 特徴量メタデータや登録情報の管理（将来的に nf_feature_registry へ発展させる想定）。

ここが、「生のロトデータを NeuralForecast が利用可能な `futr_*/hist_*/stat_*` 形式に変換する層」です。

### 2.4 pipelines

- `training_pipeline.py`
  - 実験実行パイプラインのエントリポイント。
  - 現時点では、`legacy/nf_loto_webui/nf_auto_runner_full.py` を `run_legacy_nf_auto_runner()` 経由で呼び出すラッパー実装。
  - 将来的には AutoModelFactory ベースの統一パイプライン（モデル選択・ハイパラ探索・学習・保存）に差し替えることを想定。

### 2.5 ml

- `automodel_builder.py`
  - NeuralForecast の `AutoTFT`, `AutoPatchTST`, `AutoNHITS`, `AutoDLinear` などを統一 API で扱うためのビルダー。
- `model_runner.py`
  - 学習・検証・予測の実行フロー。
  - 検証スキーム（ホライゾン、クロスバリデーション設定など）を組み立てる。
- `model_registry.py`
  - 学習済みモデルやベストトライアル情報の登録・読み出しを担当。

AutoML 的なモデル探索・トレーニングの実行ロジックは、このサブパッケージに集約されます。

### 2.6 logging_ext

- `mlflow_logger.py`
  - MLflow へのメトリクス・パラメータ・アーティファクト出力を行うためのラッパー。
- `wandb_logger.py`
  - Weights & Biases 連携のラッパー（必要に応じて有効化）。

実験再現性・トレース性を高めるためのログ連携を担当します。

### 2.7 monitoring

- `resource_monitor.py`
  - 実行中の CPU / メモリ / GPU / I/O 使用状況などの収集。
- `prometheus_metrics.py`
  - Prometheus エクスポータとの連携用ヘルパー（メトリクス公開）。

これにより、「実験がどの程度リソースを使っていたか」を後から分析できます。

### 2.8 reports

- `html_reporter.py`
  - 実験結果を HTML レポートとしてまとめるためのユーティリティ。
  - モデルメトリクス・予測 vs 実測のグラフなどをまとめる前提のレイヤー。

### 2.9 db_metadata

- `schema_definitions.py`
  - `nf_model_runs`, `nf_model_metrics`, `nf_model_backtest`, `nf_model_predictions`,
    `nf_model_logs`, `nf_resource_usage`, `nf_drift_metrics`, `nf_residual_anomalies` など
    nf_* 系テーブルのメタ情報をまとめたモジュール。


## 3. Web UI 層（apps/webui_streamlit）

Streamlit ベースの Web UI は `apps/webui_streamlit/` 以下に配置されています。

```text
apps/webui_streamlit/
  streamlit_app.py
  nf_auto_runner_full.py
```

- `streamlit_app.py`
  - 元 `nf_loto_webui/streamlit_app.py` をベースにしたロト特化の Web UI。
  - 以下のような機能を提供する想定です。
    - データソース選択（PostgreSQL テーブル / CSV アップロード）
    - `unique_id`, `ds`, `y` と外生変数のカラムマッピング
    - モデル候補（AutoTFT 等）の選択
    - ホライゾン、評価指標、トライアル数などの設定
    - 実行ステータスの表示、ベストスコアの可視化
- `nf_auto_runner_full.py`
  - `nf_loto_platform.pipelines.training_pipeline.run_legacy_nf_auto_runner()` を呼び出す薄いラッパ。
  - 実行コマンド例：
    - `python apps/webui_streamlit/nf_auto_runner_full.py`

Web UI は今後、`src/nf_loto_platform/webui/` 以下のヘルパーと連携する形に整理していく想定です。


## 4. 設定ファイル（config/）

代表的な設定ファイルは次の通りです。

- `db.yaml.template`
  - 統合 DB 接続設定のテンプレート。
  - 実運用時には `db.yaml` を作成して使用します。
- `loto_db_config.yaml.template`, `loto_default_config.yaml`, `loto_pipeline_config.yaml`
  - 元 `loto_feature_system_v2` の設定ファイル（ロト特徴量パイプライン向け）。
- `webui_database.yaml`, `webui_models.yaml`, `webui_ui_config.yaml`, `webui_logging_config.yaml`
  - 元 `neuralforecast-automl-webui` の Web UI 設定群。
- `features.yaml`
  - 統合特徴量セット定義のサンプル。
  - `dataset` のカラム名と、利用する `futr/hist/stat` 特徴を宣言する。

設定値の読み込みには、原則として `core/settings.load_db_config()` や
各サブパッケージ内のローダーを通す方針です。


## 5. 実験メタデータ・分析（sql/ と legacy/sonnet）

- `sql/001_create_nf_model_run_tables.sql`, `002_extend_metadata_tables.sql`
  - nf_* 系メタテーブル（`nf_model_runs` など）の DDL。
- `sql/analysis_queries.sql`, `nf_pg_check.sql`
  - sonnet プロジェクト由来の分析クエリ。

分析用の Python コード（`legacy/sonnet/*.py`）は、今後 `src/nf_loto_platform/ml_analysis/` へ
徐々に移行していくことを想定しています。


## 6. ノートブックとテスト

- `notebooks/nf_loto_platform_intro.ipynb`
  - 環境確認・設定読み込み・パイプライン起動の最小例を含むイントロノートブック。
- `tests/test_smoke_imports.py`
  - `nf_loto_platform` パッケージとトレーニングパイプラインの import を確認するスモークテスト。
- `tests/test_core_settings.py`
  - `core.settings.load_db_config()` が dict を返すかを確認するテスト。

ここから先は、モデルごとの挙動や DB 書き込み、ドリフト検知など、
より詳細なユニットテスト・統合テストを追加していく前提の構成です。


## 7. 実行手順の概略

1. Python 仮想環境を作成し、必要な依存パッケージ（`requirements.txt` 等を参照）をインストールします。
2. `config/db.yaml.template` をコピーして `config/db.yaml` を作成し、PostgreSQL 接続情報を設定します。
3. 必要に応じて、`sql/001_create_nf_model_run_tables.sql` などを適用し、nf_* テーブルを作成します。
4. Streamlit Web UI を起動する場合：
   - プロジェクトルートで `streamlit run apps/webui_streamlit/streamlit_app.py` を実行します。
5. CLI から実験パイプラインのみ起動する場合：
   - `python apps/webui_streamlit/nf_auto_runner_full.py` を実行します。

これらの手順は、環境や目的に応じて調整してください。
詳細な設計や API 仕様は `docs/DESIGN_OVERVIEW.md` および `docs/API_REFERENCE.md` を参照しつつ、
必要に応じて `legacy/` 配下の元コードを参考実装として活用してください。
