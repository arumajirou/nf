# NeuralForecast AutoML WebUI

時系列予測モデルの自動最適化を、直感的なWebインターフェースで操作可能にするシステム

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 主要機能

- **📤 データアップロード・管理**: CSV、Parquet、Excel形式のサポート
- **⚙️ モデル設定・パラメータ選択**: 28種類のNeuralForecastモデルに対応
- **🚀 リアルタイム実行監視**: 学習進捗とリソース使用状況を可視化
- **💻 リソースモニタリング**: CPU、メモリ、GPU、ディスクI/Oの監視
- **📊 実験履歴管理**: PostgreSQLによる永続化とMLflowとの統合
- **📈 予測結果可視化**: インタラクティブなグラフと統計情報
- **🔧 並列実行対応**: Optuna・Ray Tuneによる分散最適化

## 🖥️ システム要件

### 必須
- **Python**: 3.9以上、3.12未満
- **PostgreSQL**: 14以上
- **RAM**: 最低8GB (推奨: 16GB以上)
- **ディスク**: 10GB以上の空き容量

### 推奨
- **GPU**: NVIDIA GPU (CUDA対応) - 学習の高速化
- **CPU**: 4コア以上
- **OS**: Ubuntu 20.04+, macOS 11+, Windows 10+

## 📦 インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/your-repo/neuralforecast-automl-webui.git
cd neuralforecast-automl-webui
```

### 2. 環境変数の設定

```bash
cp .env.example .env
# .envファイルを編集してデータベース接続情報を設定
```

### 3. PostgreSQLデータベースの準備

```bash
# PostgreSQLにログイン
psql -U postgres

# データベースとユーザーの作成
CREATE DATABASE neuralforecast_automl;
CREATE USER automl_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE neuralforecast_automl TO automl_user;

# 終了
\q
```

### 4. データベーススキーマの作成

```bash
psql -U postgres -d postgres -f database/schema.sql
```

### 5. 自動セットアップ (推奨)

```bash
chmod +x scripts/launch.sh
./scripts/launch.sh
```

または、手動セットアップ:

```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install --upgrade pip
pip install -r requirements.txt

# データベースの初期化
python scripts/init_db.py

# アプリケーションの起動
streamlit run webui/app.py
```

## 🚀 クイックスタート

### 1. アプリケーションの起動

```bash
./scripts/launch.sh
```

または:

```bash
streamlit run webui/app.py
```

ブラウザで `http://localhost:8501` を開きます。

### 2. データのアップロード

1. 左サイドバーから「📤 Data Upload」を選択
2. CSV/Parquet/Excelファイルをドラッグ&ドロップ
3. データプレビューと検証結果を確認

### 3. モデルの設定

1. 「⚙️ Model Configuration」を選択
2. モデルタイプを選択 (例: NHITS, TFT, DLinear)
3. 予測期間 (horizon) を設定
4. 最適化パラメータを設定

### 4. 学習の実行

1. 「🚀 Training」を選択
2. "Start Training" ボタンをクリック
3. リアルタイム進捗とリソース使用状況を監視

### 5. 結果の確認

1. 「📈 Results」を選択
2. 予測結果のグラフを確認
3. 最適パラメータと性能指標を確認

## 📁 プロジェクト構造

```
neuralforecast-automl-webui/
├── config/                    # 設定ファイル
├── database/                  # データベース関連
│   ├── schema.sql            # テーブル定義
│   ├── models.py             # SQLAlchemyモデル
│   └── connection.py         # DB接続管理
├── monitoring/               # リソース監視
│   └── resource_monitor.py
├── webui/                    # Streamlit UI
│   ├── app.py               # メインアプリ
│   ├── pages/               # ページモジュール
│   └── components/          # UIコンポーネント
├── core/                    # コアロジック（既存）
├── services/                # サービス層
├── scripts/                 # スクリプト
│   ├── launch.sh           # 起動スクリプト
│   └── init_db.py          # DB初期化
└── docs/                    # ドキュメント
```

## 🎯 サポートされるモデル

- NHITS, NBEATS, TFT, MLP, DLinear
- TSMixer, PatchTST, Transformer
- DeepAR, DeepNPTS, NBEATSx, BiTCN
- TiDE, TimesNet, HINT
- LSTM, GRU, RNN, TCN
- Informer, Autoformer, FEDformer
- その他28種類のモデル

## 📚 ドキュメント

- [ユーザーガイド](docs/USER_GUIDE.md)
- [API リファレンス](docs/API_REFERENCE.md)
- [デプロイメント](docs/DEPLOYMENT.md)
- [トラブルシューティング](docs/TROUBLESHOOTING.md)

## 🤝 コントリビューション

プルリクエストを歓迎します!

## 📄 ライセンス

MIT License

## 🙏 謝辞

- [NeuralForecast](https://github.com/Nixtla/neuralforecast)
- [Optuna](https://optuna.org/)
- [Streamlit](https://streamlit.io/)
- [MLflow](https://mlflow.org/)
