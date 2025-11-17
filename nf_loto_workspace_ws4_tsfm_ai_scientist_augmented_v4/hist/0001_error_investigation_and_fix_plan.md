# nf-loto-platform pytest エラー調査・改修計画 (実施ログ)

本ファイルは、pytest HTML レポートの解析に基づいて整理した
フェーズ 1〜4 の計画と、その実施内容を簡潔に記録したものです。

## フェーズ 1: モジュール import 破綻の解消

- `nf_loto_platform.monitoring.prometheus_metrics` に
  `observe_run_error` 関数を追加し、`model_runner` からの import を解決。
- `tests/monitoring/test_prometheus_metrics.py` を整備し、
  期待される公開 API 一式 (`init_metrics_server`, `observe_run_start`,
  `observe_run_end`, `observe_run_error`, `observe_train_step`) が
  存在することを確認するテストを実装。
- `tests/static/test_all_modules_importable.py` で
  `nf_loto_platform.ml.model_runner` を含む全モジュールが import 可能であることを
  確認する静的契約テストを維持。

## フェーズ 2: DB / SQL / モデル実行パイプラインの安定化

- `tests/nonfunctional/test_minimal_performance_smoke.py` および
  `tests/integration/test_training_with_mock_db.py` にて、
  実 DB や実 AutoModel に依存しない dummy 実装 + monkeypatch ベースの
  軽量パイプラインテストを構成。
- `loto_repository.load_panel_by_loto` / `automodel_builder.build_auto_model` /
  `build_neuralforecast` をテスト時にスタブ化し、
  `run_loto_experiment` が end-to-end で DataFrame とメタ情報を返す経路を確認。
- 実 DB / 実 AutoModel を前提とした「長時間テスト」は削り、
  代わりに mock DB + dummy AutoModel による 2 パターンの統合テストを追加
  （horizon=5 / horizon=3 のケース）。

## フェーズ 3: 性能テスト・非機能テストの整理

- `tests/nonfunctional/test_reproducibility_seed.py` で
  Python `random` / NumPy / (オプション) torch の種固定を検証。
- `tests/nonfunctional/test_minimal_performance_smoke.py` で
  dummy AutoModel と stubbed NeuralForecast を用いた軽量な性能スモークテストを実装。
- いずれも CI / ローカル環境で実行可能なサイズのデータ・計算量に制限し、
  「最低限 1 本は end-to-end に動く」ことを確認する位置づけとした。

## フェーズ 4: E2E / WebUI / パイプラインまわりのテスト拡充と skip 解消

- `src/nf_loto_platform/pipelines/training_pipeline.py`
  - `run_legacy_nf_auto_runner(base_root: Path | None = None)` へシグネチャを拡張し、
    テストから任意のディレクトリをルートとして指定できるように変更。
- `tests/pipelines/test_training_pipeline.py`
  - legacy runner が存在しない場合に `RunError` となるケースと、
    ダミーの `nf_auto_runner_full.py` を用意した場合に正常終了するケースの
    2 本のテストを実装。
- `tests/e2e/test_cli_nf_auto_runner_e2e.py`
  - pytest.skip を廃止し、tmp_path 配下にダミーの legacy runner を生成して
    `run_legacy_nf_auto_runner` を 1 周させる E2E スモークテストを実装。
- `src/nf_loto_platform/webui/__init__.py`
  - `is_webui_available()` ヘルパー関数を実装し、Streamlit が存在するかどうかを
    import ベースで簡易判定するラッパーを追加。
- `tests/webui/test_webui_placeholder.py` / `tests/e2e/test_webui_smoke.py`
  - それぞれ webui モジュールの API が存在し bool を返すことを確認するテストに置き換え、
    skip を解消。
- `src/nf_loto_platform/features/__init__.py`
  - パネルデータにラグ特徴量を追加する `add_lag_feature` を実装。
- `tests/features/test_features_placeholder.py` / `tests/integration/test_feature_pipeline_integration.py`
  - 上記 `add_lag_feature` を用いたユニットテスト / 小さな統合テストを実装し、
    features 系のプレースホルダテストを本実装に変更。

## skip 解消の概要

- 次のテストファイルから明示的な `@pytest.mark.skip` / `pytest.skip` を撤去し、
  実行可能なテストケースに差し替えた。
  - `tests/e2e/test_cli_nf_auto_runner_e2e.py`
  - `tests/e2e/test_webui_smoke.py`
  - `tests/features/test_features_placeholder.py`
  - `tests/integration/test_feature_pipeline_integration.py`
  - `tests/pipelines/test_training_pipeline.py`
  - `tests/webui/test_webui_placeholder.py`
- `tests/static/test_all_modules_importable.py` では
  `PKG_ROOT.rglob("*.py")` の結果から `__pycache__` 配下を事前に除外することで、
  実行時の `pytest.skip("cache directory")` を廃止しつつ、
  「全モジュール import 可能」という契約テストを維持。

## 今後の拡張余地

- DB ダイアレクト (PostgreSQL / SQLite) ごとの SQL プレースホルダ戦略の明示化。
- WebUI 実装（Streamlit アプリ本体）との結合テストを別レイヤとして追加。
- CI でのテストプロファイル（unit / integration / nonfunctional / e2e）の
  実行ポリシーを `TEST_PLAN.md` に追記。

---

## フェーズ 1〜4 / Phase A〜E 実装ログ (要約)

- フェーズ 1: pytest レポートの出力・構造の整備
  - `report/pytest_report.html` を標準出力先として固定。
  - static import テストや nonfunctional テストを整理し、エラー検知の粒度を細かくした。
- フェーズ 2: 失敗テストの恒久対策設計
  - import 破綻・monitoring API 不整合・プレースホルダテストを順次解消。
  - 追加で ml_analysis の単体テストを用意し、メトリクス計算まわりの回帰を検出可能にした。
- フェーズ 3: 統合テスト / 性能テストとの接続
  - 既存の integration / nonfunctional テストに加え、
    `tests/ml_analysis` 配下にメトリクスレイヤのテストを追加。
  - 今後は model_runner 側から ml_analysis を呼び出すことで、
    end-to-end でのメトリクス検証に拡張できる構造にした。
- フェーズ 4: 運用時の再現性・観測性向上のための土台
  - MLflow を利用可能な場合にのみ動作する `experiment_tracking` ラッパーを実装。
  - mlflow が無い環境では no-op としつつ、テストでは fake mlflow により挙動を検証。

### 予測精度向上のための拡張 (Phase A〜E)

- Phase A: ログ/スキーマ整備
  - `nf_loto_platform.ml_analysis.metrics` で主要誤差指標 (MAE, RMSE, sMAPE, pinball loss, coverage) を実装。
  - これにより run ごとのメトリクス計算を共通化可能な状態にした。
- Phase B: 精度評価パイプライン
  - `nf_loto_platform.ml_analysis.reporting` を追加し、
    DataFrame からのメトリクス計算と HTML/JSON レポート出力のユーティリティを実装。
- Phase C: 探索パイプラインとの接続準備
  - `nf_loto_platform.ml_analysis.experiment_tracking` で MLflow へのパラメータ/メトリクス記録をラップ。
  - これにより Optuna/Ray などのハイパラ探索と MLflow ロギングを結合しやすい構造にした。
- Phase D: 可視化・ダッシュボードへの橋渡し
  - HTML レポート出力を標準化することで、将来 Streamlit/Dash から
    これらのレポートを読み込んで可視化する道筋を用意。
- Phase E: KPI 運用と自動アラートに向けた基盤
  - メトリクス計算・JSON 出力・MLflow ログの 3 点を揃えたことで、
    将来的に「しきい値を満たさない run を自動検出してアラートする」仕組みを
    CI や本番バッチの上に構築しやすくした。
## フェーズ 2.x: integration テストの DB モック修正 (nf_loto_ws4)

- `tests/integration/test_training_with_mock_db.py` で
  `load_panel_by_loto` の monkeypatch 対象を修正。
    - 旧: `"nf_loto_platform.db.loto_repository.load_panel_by_loto"`
    - 新: `"nf_loto_platform.ml.model_runner.load_panel_by_loto"`
  これにより、`model_runner` が import 済みのシンボルを直接差し替える形になり、
  実 PostgreSQL への誤接続を防止。
- 同テストファイル冒頭に、本テストの役割と「DB は完全にモックする」方針をコメントで明記。
- 予測誤差のスライス別・時間別集計のために
  `nf_loto_platform.ml_analysis.error_breakdown` を新規追加。
    - `build_error_breakdown`: (loto, unique_id 等) セグメント別の MAE/RMSE/sMAPE を集計。
    - `build_time_series_metrics`: resample ベースで期間ごとの MAE/RMSE/sMAPE を集計。
- 上記ユーティリティの振る舞いを確認するため、
  `tests/ml_analysis/test_error_breakdown.py` を追加。
