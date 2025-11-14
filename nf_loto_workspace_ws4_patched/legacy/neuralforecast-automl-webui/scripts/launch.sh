#!/bin/bash
# NeuralForecast AutoML WebUI - 起動スクリプト

set -e

echo "================================"
echo "NeuralForecast AutoML WebUI"
echo "================================"
echo ""

# プロジェクトルート
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 仮想環境のチェック
if [ ! -d "venv" ]; then
    echo "🔧 仮想環境が見つかりません。作成します..."
    python3 -m venv venv
    echo "✓ 仮想環境を作成しました"
fi

# 仮想環境の有効化
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "❌ 仮想環境の有効化に失敗しました"
    exit 1
fi

echo "✓ 仮想環境を有効化しました"

# 依存関係のインストール
if [ ! -f "venv/.installed" ]; then
    echo "📦 依存関係をインストールしています..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.installed
    echo "✓ 依存関係をインストールしました"
else
    echo "✓ 依存関係は既にインストール済みです"
fi

# 環境変数の読み込み
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✓ 環境変数を読み込みました"
else
    echo "⚠️  .envファイルが見つかりません (.env.exampleをコピーしてください)"
fi

# データディレクトリの作成
mkdir -p data/uploads data/models data/results data/logs
echo "✓ データディレクトリを作成しました"

# データベース接続テスト
echo ""
echo "🔍 データベース接続をテストしています..."
python -c "
import sys
sys.path.insert(0, '.')
from database.connection import get_db_connection
try:
    db = get_db_connection()
    if db.test_connection():
        print('✓ データベース接続: OK')
    else:
        print('❌ データベース接続: 失敗')
        sys.exit(1)
except Exception as e:
    print(f'❌ データベース接続エラー: {e}')
    print('データベース設定を確認してください (.env または config/database.yaml)')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ データベース接続に失敗しました"
    echo "以下を確認してください:"
    echo "  1. PostgreSQLが起動しているか"
    echo "  2. .envファイルの接続情報が正しいか"
    echo "  3. データベースとユーザーが作成されているか"
    exit 1
fi

echo ""
echo "🚀 アプリケーションを起動しています..."
echo ""
echo "ブラウザで以下のURLを開いてください:"
echo "  http://localhost:8501"
echo ""
echo "終了するには Ctrl+C を押してください"
echo ""

# Streamlitアプリケーション起動
streamlit run webui/app.py --server.port 8501 --server.address localhost
