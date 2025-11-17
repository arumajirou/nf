# nf_loto_platform システム詳細設計 & 運用ガイド

本ドキュメントは、`nf_loto_workspace_ws4_patched` 環境の最終統合版として、
ロジック構造・ディレクトリ構成・テスト戦略・運用/インストール/実行手順をまとめたものです。
TSFM 統合を含むモデルレジストリ拡張と、その周辺テスト/ドキュメントも反映済みです。

---

## 1. 全体アーキテクチャ概要

nf_loto_platform は、Nixtla NeuralForecast を中核としたロト時系列予測プラットフォームです。

- core/: 設定・共通ユーティリティ・ドメインロジック
- ml/: モデルレジストリ、学習/推論パイプライン、損失関数など ML 周辺
- pipelines/: ETL・特徴量生成・予測パイプライン定義
- features/: 特徴量設計と FeatureSet 定義
- webui/: Streamlit ベースの Web UI 及び自動実行ランナー
- monitoring/: ログ・メトリクス・将来的なドリフト検知の拡張ポイント
- reports/: レポート生成ロジックとテンプレート
- db/, db_metadata/: DB アクセスレイヤとメタデータ定義

---

## 2. ディレクトリ構成サマリ

### 2.1 ルート

- ルート直下 (nf_loto_workspace_ws4_patched) の主なエントリ:
  - README.md
  - apps
  - config
  - docs
  - hist
  - notebooks
  - pyproject.toml
  - pytest.ini
  - report
  - sql
  - src
  - tests

### 2.2 Python パッケージ nf_loto_platform

- パッケージルート: src/nf_loto_platform
- 主なサブディレクトリ:
  - __pycache__/
  - core/
  - db/
  - db_metadata/
  - features/
  - logging_ext/
  - ml/
  - ml_analysis/
  - monitoring/
  - pipelines/
  - reports/
  - webui/

### 2.3 アプリケーション層

- apps/webui_streamlit/:
  - streamlit_app.py: Web UI 本体
  - nf_auto_runner_full.py: 自動実行ランナー / バックエンド呼び出し

### 2.4 ドキュメント

- docs/ 直下の主な Markdown:
  - 00_DOCS_INDEX.md
  - 01_NeuralForecast.md
  - 02_Ray.md
  - 03_Optuna.md
  - 03_optunareadthedocsio.md
  - 04_MLflow.md
  - 05_MLflow-Databricks.md
  - 06_GitHub.md
  - 07_Lightning.md
  - API_REFERENCE.md
  - Claude-Documentation structure setup.md
  - Claude-Lead engineer framework for AutoModels backend optimization.md
  - Claude-Python factory pattern module structure.md
  - Claude-Time series feature engineering system design.md
  - Claude-Time_series_feature_engineering_system_design.md
  - DESIGN_OVERVIEW.md
  - FEATURE_SYSTEM_SPEC.md
  - IMPLEMENTATION_PLAN.md
  - LOTO_FEATURE_SYSTEM_DESIGN.md
  - QUICKSTART.md
  - QUICKSTART_EXTENDED.md
  - README.md
  - README_ANALYSIS.md
  - README_EXTENDED.md
  - README_USAGE.md
  - TUTORIAL.md
  - UI_UX_IMPROVEMENT_DESIGN.md
  - USER_GUIDE.md
  - パラメータ.md

- docs/ サブディレクトリ:
  - tsfm_integration/

  - 特に docs/tsfm_integration/ 配下に TSFM 統合関連の設計書・サマリーを集約:
    - FEATURE_EXPANSION_SPEC.md
    - TSFM_INTEGRATION_DETAIL.md
    - README_DESIGN_DOCS.md
    - TSFM_Integration_Detailed_Design_Plan.md
    - Implementation_Summary_and_Next_Steps.md

### 2.5 テスト

- tests/ 内のテストファイル:
  - conftest.py
  - test_core_settings.py
  - test_model_registry_tsfm.py
  - test_smoke_imports.py

---

## 3. コアロジック設計概要

### 3.1 モデルレジストリ (src/nf_loto_platform/ml/model_registry.py)

NeuralForecast AutoModel と TSFM モデルを一元管理するレジストリで、
モデルごとの外生変数サポートやコンテキスト長などのメタデータを `AutoModelSpec` として管理します。

- ExogenousSupport: futr/hist/stat の 3 軸で外生変数サポートを明示
- AutoModelSpec: name, family, loss, requires_exogenous, context_length など

主な公開関数:

- list_automodel_names()
- get_model_spec(name)
- list_tsfm_models()
- list_neuralforecast_models()
- get_models_by_exogenous_support(...)
- validate_model_spec(spec)
- _validate_registry_at_module_load()

### 3.2 WebUI / アプリ層

- apps/webui_streamlit/streamlit_app.py:
  - モデル選択・予測実行・結果可視化を行うフロントエンド
- apps/webui_streamlit/nf_auto_runner_full.py:
  - WebUI から nf_loto_platform のパイプライン/モデルランナーを呼び出すオーケストレーター

### 3.3 MLOps / 監視拡張ポイント

- nf_loto_platform/monitoring/:
  - ログ・メトリクス・将来的なドリフト検知・再学習トリガの実装ポイント

---

## 4. インストールガイド (サマリ)

1. プロジェクトルートへ移動:

   ```bash
   cd nf_loto_workspace_ws4_patched
   ```

2. 仮想環境作成・有効化:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows は .venv\Scripts\activate
   ```

3. 依存インストール:

   ```bash
   pip install -U pip
   pip install -e ".[dev]"
   pip install neuralforecast
   ```

---

## 5. テスト実行ガイド (サマリ)

- 全テスト実行:

  ```bash
  pytest
  ```

- TSFM レジストリ関連のみ:

  ```bash
  pytest tests/test_model_registry_tsfm.py -vv
  ```

tests/test_model_registry_tsfm.py では、TSFM モデル登録・外生サポート・
既存モデルへの副作用有無などを検証します。

---

## 6. 運用と拡張

- モデル追加フロー:
  - AutoModelSpec 追加 → ExogenousSupport 定義 → 必要なら設定/キーを config/ に追加 → テスト追加
- MLOps 拡張:
  - MLflow / Ray / Optuna などによる実験管理とハイパラ探索は monitoring/ や ml_analysis/ を拡張して実装

FEATURE_EXPANSION_SPEC.md に定義された F-MODEL, F-FEAT, F-AGENT, F-EVAL, F-MLOPS, F-UI 群の拡張は、
本ドキュメントの構造を土台として段階的に実装していく想定です。
