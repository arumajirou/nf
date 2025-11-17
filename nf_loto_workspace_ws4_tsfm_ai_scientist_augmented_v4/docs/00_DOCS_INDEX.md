# nf_loto_platform ドキュメント案内（docs/ 一式）

このディレクトリ `docs/` には、NeuralForecast Loto Suite（nf_loto_platform）の
設計・実装・利用方法に関するドキュメントを集約しています。

大きく以下のカテゴリに分かれます。

- システム全体設計
- 実装計画・API 仕様
- 特徴量システム
- AutoML / バックエンド
- 学習・実験運用（MLflow / Lightning / Ray / Optuna）
- Web UI / UX
- クイックスタート / ユーザーガイド
- パラメータ・チューニング

## 1. システム全体設計

- `DESIGN_OVERVIEW.md`
  - nf_loto_platform 全体のアーキテクチャ概要。
  - ディレクトリ構造・コンポーネント・データフロー・責務分担の整理。
- `IMPLEMENTATION_PLAN.md`
  - 機能追加やリファクタリングの実装計画。
  - マイルストーン・優先度・タスク分割など。

## 2. API / 実装リファレンス

- `API_REFERENCE.md`
  - AutoModelFactory／nf_loto_platform の公開 API 一覧。
  - クラス・関数シグネチャと主要な引数・戻り値の説明。
- `README.md`
  - ドキュメント全体の背景や読み方のガイド。
- `README_*` 系（`README_EXTENDED.md`, `README_USAGE.md`, `README_ANALYSIS.md` など）
  - 個別モジュールや分析用ツールの詳細な説明。

## 3. 特徴量システム（Feature System）

- `LOTO_FEATURE_SYSTEM_DESIGN.md`
  - ロト向け特徴量生成システム（loto_feature_system_v2）の全体設計。
  - データ取得 → クリーニング → futr/hist/stat 特徴生成 → 保存までのパイプライン定義。
- `FEATURE_SYSTEM_SPEC.md`
  - 特徴量セットの仕様書。
  - 各特徴量の意味・計算式・カラム名規約など。

## 4. AutoML / モデルバックエンド

- `Claude-Lead engineer framework for AutoModels backend optimization.md`
  - AutoModelFactory／Auto* モデルのバックエンド最適化方針。
  - 検証方法・メトリクス・探索戦略など。
- `Claude-Python factory pattern module structure.md`
  - Python ファクトリパターンでのモジュール構造・依存関係設計。
- `Claude-Documentation structure setup.md`
  - ドキュメント体系（本ファイルを含む）の設計メモ。

## 5. 学習・実験運用（NeuralForecast / Ray / Optuna / MLflow / Lightning）

- `01_NeuralForecast.md`
  - NeuralForecast ライブラリの要点・利用パターン。
- `02_Ray.md`
  - Ray を用いた分散ハイパラ探索／ワーカ管理に関するメモ。
- `03_Optuna.md`, `03_optunareadthedocsio.md`
  - Optuna によるハイパーパラメータ探索の設計・使い方。
- `04_MLflow.md`, `05_MLflow-Databricks.md`
  - MLflow による実験トラッキング／アーティファクト管理。
  - Databricks 連携も含む。
- `07_Lightning.md`
  - PyTorch Lightning（または Lightning AI）との連携に関するメモ。
- `06_GitHub.md`
  - GitHub 上での運用方針やリポジトリ構成メモ。

## 6. Web UI / UX

- `UI_UX_IMPROVEMENT_DESIGN.md`
  - Streamlit ベース Web UI の改善設計。
  - 画面構成、状態管理、操作フローなど。
- `USER_GUIDE.md`
  - Web UI／コマンドラインからシステムを利用するユーザー向けガイド。

## 7. クイックスタート / チュートリアル

- `QUICKSTART.md`, `QUICKSTART_EXTENDED.md`
  - 最小構成での動作確認手順。
  - 拡張版では複数モデル・複数実験を扱う手順を説明。
- `TUTORIAL.md`
  - ステップバイステップでの実験フロー（特徴量生成 → 学習 → 分析）の一連のチュートリアル。

## 8. パラメータ・チューニング

- `パラメータ.md`
  - モデル・特徴量・学習設定などの主要パラメータの一覧と簡易解説。
  - 推奨値／探索範囲などのメモ。

## 9. 使い方の目安

- システム全体像を把握したい場合：
  - `DESIGN_OVERVIEW.md` → `API_REFERENCE.md` → `LOTO_FEATURE_SYSTEM_DESIGN.md`
- 実験実行を始めたい場合：
  - `QUICKSTART.md` → `TUTORIAL.md` → `USER_GUIDE.md`
- 深い設計意図や将来の拡張方針を知りたい場合：
  - `IMPLEMENTATION_PLAN.md` → 各種 `Claude-*` 系設計メモ
- Web UI や UX の設計を改善したい場合：
  - `UI_UX_IMPROVEMENT_DESIGN.md` → `USER_GUIDE.md`

この `00_DOCS_INDEX.md` 自体は、docs/ 一式の「目次」として随時更新していくことを想定しています。
新しいドキュメントを追加した場合は、本ファイルに概要を追記してください。
