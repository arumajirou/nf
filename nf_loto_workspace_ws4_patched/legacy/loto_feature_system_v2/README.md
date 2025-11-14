# 宝くじ時系列特徴量生成システム v2.0

## 概要

loto（宝くじ）の時系列データから、NeuralForecastのAutoModelsに最適化された特徴量を自動生成する、エンタープライズグレードの特徴量生成プラットフォームです。

### 主要機能

- **F(Future)/H(Historical)/S(Static)外生変数の自動生成**: NeuralForecastの28モデル全てに対応
- **GPU/並列実行による高速化**: RAPIDS cuDF、Dask、Ray等による10倍以上の高速化
- **異常値・外れ値検出特徴**: 統計的手法とML手法の組み合わせ
- **拡張可能なアーキテクチャ**: 新しい特徴量ライブラリの容易な統合

### システム規模

- **対象データ**: nf_loto_final テーブル
- **time_series数**: loto × unique_id 組み合わせ（推定: 32系列）
- **生成特徴量**: 推定500-1000特徴量/系列
- **処理時間目標**: 全特徴量生成 < 5分（GPU使用時）

## クイックスタート

### 前提条件

- Python 3.9以上
- PostgreSQL 13以上
- 16GB RAM以上

### インストール

```bash
# 1. リポジトリクローン
git clone <repository-url>
cd loto_feature_system_v2

# 2. 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 依存パッケージインストール
pip install -r requirements.txt

# 4. GPU版（オプション）
pip install -r requirements-gpu.txt
```

### 設定

```bash
# データベース設定
cp config/db_config.yaml.template config/db_config.yaml
# db_config.yamlを編集してデータベース接続情報を設定
```

### 初期セットアップ

```bash
# テーブル作成
python scripts/setup_database.py
```

### 特徴量生成

```bash
# シンプルな実行
python scripts/generate_features_simple.py
```

## プロジェクト構造

```
loto_feature_system_v2/
├── README.md                      # このファイル
├── requirements.txt               # 依存パッケージ
├── requirements-gpu.txt           # GPU版追加パッケージ
├── config/                        # 設定ファイル
│   ├── db_config.yaml            # データベース設定
│   ├── default_config.yaml       # システムデフォルト設定
│   └── pipeline_config.yaml      # パイプライン設定
├── src/                          # ソースコード
│   ├── core/                     # コアモジュール
│   │   ├── database_manager.py  # データベース管理
│   │   └── data_loader.py       # データ読み込み
│   ├── pipelines/                # 特徴量パイプライン
│   │   ├── base_pipeline.py     # パイプライン基底クラス
│   │   ├── basic_stats.py       # 基本統計パイプライン
│   │   └── calendar_features.py # カレンダー特徴量パイプライン
│   ├── utils/                    # ユーティリティ
│   └── integration/              # 外部ツール統合
├── scripts/                      # 実行スクリプト
│   ├── setup_database.py        # データベースセットアップ
│   └── generate_features_simple.py # 特徴量生成
├── tests/                        # テストコード
├── logs/                         # ログファイル
├── cache/                        # キャッシュディレクトリ
└── notebooks/                    # Jupyterノートブック
```

## パイプライン

### 実装済み

1. **P1: Basic Statistics Pipeline** (`basic_stats.py`)
   - ラグ特徴量
   - ローリング統計（平均、標準偏差、最小値、最大値等）
   - 差分・パーセント変化

2. **P12: Calendar Features Pipeline** (`calendar_features.py`)
   - カレンダー特徴量
   - 周期性エンコーディング
   - フーリエ特徴量
   - 休日特徴量（日本）

### 今後実装予定

- P2: Rolling Windows Pipeline
- P3: Lag & Difference Pipeline
- P4: Trend & Seasonality Pipeline
- P5: Autocorrelation Pipeline
- P6: tsfresh Advanced Pipeline
- P7: TSFEL Spectral Pipeline
- P8: catch22 Canonical Pipeline
- P9: AntroPy Entropy Pipeline
- P10: Matrix Profile Pipeline
- P11: Anomaly Detection Pipeline
- P13: Lottery Domain Pipeline
- P14: Static Features Pipeline

## データベーススキーマ

### features_hist (Historical特徴量)

```sql
CREATE TABLE features_hist (
    loto VARCHAR(50) PRIMARY KEY,
    unique_id VARCHAR(10) PRIMARY KEY,
    ds DATE PRIMARY KEY,
    hist_y_lag1 FLOAT,
    hist_y_lag2 FLOAT,
    ...
    hist_y_roll_mean_w7 FLOAT,
    hist_y_roll_std_w7 FLOAT,
    ...
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### features_futr (Future特徴量)

```sql
CREATE TABLE features_futr (
    loto VARCHAR(50) PRIMARY KEY,
    unique_id VARCHAR(10) PRIMARY KEY,
    ds DATE PRIMARY KEY,
    futr_ds_year INTEGER,
    futr_ds_month INTEGER,
    ...
    futr_ds_day_sin FLOAT,
    futr_ds_day_cos FLOAT,
    ...
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### features_stat (Static特徴量)

```sql
CREATE TABLE features_stat (
    loto VARCHAR(50) PRIMARY KEY,
    unique_id VARCHAR(10) PRIMARY KEY,
    stat_y_global_mean FLOAT,
    stat_y_global_std FLOAT,
    ...
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## 設定

### データベース設定 (`config/db_config.yaml`)

```yaml
host: localhost
port: 5432
database: postgres
user: postgres
password: your_password
```

### パイプライン設定 (`config/pipeline_config.yaml`)

```yaml
pipelines:
  basic_stats:
    enabled: true
    priority: 1
    feature_type: "hist"
    config:
      lag_windows: [1, 2, 3, 7, 14, 21, 28, 30, 60]
      rolling_windows: [3, 7, 14, 21, 30, 60, 90]
```

## 開発

### テスト実行

```bash
pytest tests/ -v
```

### コードスタイル

```bash
# フォーマット
black src/ tests/

# リント
pylint src/ tests/
```

## トラブルシューティング

### Q: データベース接続エラー

**A**: `config/db_config.yaml`の設定を確認してください。

```bash
# PostgreSQL接続テスト
psql -h localhost -U postgres -d postgres
```

### Q: nf_loto_finalテーブルが見つからない

**A**: 元データのテーブルが存在することを確認してください。

### Q: GPU OutOfMemory エラー

**A**: `config/default_config.yaml`でGPUを無効化してください。

```yaml
parallel:
  use_gpu: false
```

## ライセンス

MIT License

## 作成者

AI System Architect

## バージョン

2.0.0

## 更新日

2025-01-12

## 参考資料

- 完全設計書: `LOTO_FEATURE_SYSTEM_DESIGN.md`
- 実装計画: `IMPLEMENTATION_PLAN.md`
- クイックスタート: `QUICKSTART.md`
# loto_feature_system_v2
