# nf_loto_platform テスト設計（レイヤー別プラン）

本ファイルは、nf_loto_platform 全体に対するテスト戦略をレイヤー別にまとめたものです。
詳細なファイル単位のテスト設計は TEST_MATRIX.md を参照してください。

## 0. 目的

- 再構築した nf_loto_platform が論理的・構造的に破綻していないことを確認する。
- 各レイヤーに対して適切なテストを用意し、
  どのレイヤーでどの種類の不具合を検知するかを明確にする。

## 1. テストレイヤー

1. レイヤー0: 構造・静的チェック
   - ディレクトリ構造、必須ファイル、import スモーク、py_compile 等。
2. レイヤー1: ユニット／コントラクトテスト
   - core / db / features / ml / logging_ext / monitoring / reports などの単体テスト。
3. レイヤー2: コンポーネント／インテグレーションテスト
   - db ↔ features ↔ ml ↔ logging_ext ↔ db_metadata などの連携。
4. レイヤー3: E2E（エンドツーエンド）テスト
   - CLI / WebUI 起点で実験が完走するかの確認。
5. レイヤー4: 非機能テスト
   - 再現性（seed）、リソース使用状況、簡易パフォーマンスなど。

## 2. tests/ ディレクトリ構成

```text
tests/
  TEST_PLAN.md
  TEST_MATRIX.md
  conftest.py

  test_smoke_imports.py
  test_core_settings.py

  core/
  db/
  db_metadata/
  features/
  logging_ext/
  ml/
  ml_analysis/
  monitoring/
  pipelines/
  reports/
  webui/
  integration/
  e2e/
  nonfunctional/
  static/
```

- `core/`, `db/`, `ml/` 等: 各モジュールのユニットテスト。
- `integration/`: 複数モジュールを連携させるテスト。
- `e2e/`: CLI / WebUI を起点とした E2E テスト。
- `nonfunctional/`: 再現性、パフォーマンスなどのテスト。
- `static/`: py_compile や docs 参照チェックなど、静的検査系。

## 3. 実行ポリシー

- 開発中のローカル:
  - `pytest` または `pytest -m "not (integration or e2e or nonfunctional)"` を基本とする。
- CI:
  - プルリクごとにレイヤー0/1/2 を実行。
  - 日次・週次でレイヤー3/4 を実行するなど、スケジュール分離を行う。

## 4. 詳細設計

- ファイル単位・機能単位のテスト対象・観点・ケースは TEST_MATRIX.md を参照。
