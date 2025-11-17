# リファクタリング計画 (ドラフト)

## フェーズ 1: import 安定化 & テストグリーン化（今回）

- [x] `tests/static/test_all_modules_importable.py` で失敗していた 3 モジュールの修正
- [x] 旧 WebUI プロジェクトから必要なユーティリティ (`loto_repository`, `db_logger`) を移植
- [x] `pyproject.toml` で src レイアウトと依存関係を明示
- [x] `report/` / `hist/` ディレクトリを追加し、テスト・変更履歴の置き場を整備

## フェーズ 2: 実運用環境での検証

- [ ] PostgreSQL 実環境に対して `nf_loto_platform.db.*` の CRUD を確認
- [ ] `nf_loto_platform.logging_ext.db_logger` が `nf_model_runs` テーブルに正常書き込みできるか確認
- [ ] `nf_loto_platform.ml.model_runner` を用いた実験フローを通しで実行

## フェーズ 3: 観測性・運用性の強化

- [ ] MLflow / wandb ロギングパスをドキュメント化し、MLflow UI と整合するか確認
- [ ] Prometheus / Grafana で参照するメトリクス名・ラベルの一覧を `docs/` に整理
- [ ] `report/` への自動レポート出力を CI に組み込み

## フェーズ 4: パッケージング & CI/CD

- [ ] `pyproject.toml` ベースで wheel / sdist を生成し、テスト用インデックスに公開
- [ ] GitHub Actions 等で `pytest` + HTML レポート出力 + artifact 保存まで自動化
- [ ] バージョニング戦略（SemVer など）とリリースノート運用ルールを決定


### 2025-11-14: テストハードニング進捗メモ

- [x] monitoring: Prometheus メトリクス用 API (`observe_run_error`) を実装し、
      `model_runner` からの利用を含めて import 時のエラーを解消
- [x] monitoring/tests: `test_prometheus_metrics.py` で公開 API 契約を明示
- [x] ml/tests: `test_model_runner_contract.py` を追加し、
      コアエントリポイントと結果型の存在を保証
- [x] logging_ext/tests: DB ロガーの契約テストを追加
- [x] db/tests: LOTO ストア / リポジトリ周りの API 契約テストを追加

今後のタスク候補:

- [ ] `tests/nonfunctional/test_reproducibility_seed.py` の本実装
- [ ] `tests/nonfunctional/test_minimal_performance_smoke.py` で
      小規模データを用いたパフォーマンスしきい値を検証
- [ ] `tests/integration/` 配下で DB + features + ml を組み合わせた
      スモールパイプライン検証を段階的に追加
