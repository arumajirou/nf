# nf_loto_platform 設計資料パック

この zip には、これまで議論した拡張案を整理した設計資料が含まれています。

## 同梱ファイル

- `TSFM_INTEGRATION_DETAIL.md`  
  - TSFM（Chronos-2 / TimeGPT / TempoPFN）を `nf_loto_platform` に統合するための詳細設計書です。  
  - モジュール構成、`tsfm_adapters.py` の設計、`model_registry` / `model_runner` の改修方針、メタデータ・テスト設計などをまとめています。

- `FEATURE_EXPANSION_SPEC.md`  
  - LLM エージェント、FeatureSet、古典モデル、アンサンブル、評価フレームワーク、MLOps、UI などを含む「多機能拡張」の定義設計書です。  
  - 機能IDベースで整理されており、今後のタスク分解・ロードマップ策定のベースになります。

## 想定する使い方

- 実装前のレビュー資料として、開発チーム・関係者での合意形成に使用。  
- Git リポジトリの `docs/` 配下に配置し、設計ドキュメントとして管理。  
- 必要に応じて、この設計を細分化してクラス設計・テーブル設計・シーケンス図などを足していく前段階の「親ドキュメント」として利用してください。

