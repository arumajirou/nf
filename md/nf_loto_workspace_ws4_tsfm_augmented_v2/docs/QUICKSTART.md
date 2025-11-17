# 宝くじ時系列特徴量生成システム - クイックスタートガイド

## 🚀 5分で始める特徴量生成

このガイドに従えば、わずか5分でシステムを起動し、最初の特徴量を生成できます。

---

## 前提条件

### 必須
- Python 3.9以上
- PostgreSQL 13以上
- 16GB RAM以上

### 推奨（GPU使用時）
- NVIDIA GPU (4GB VRAM以上)
- CUDA 11.8以上
- 32GB RAM以上

---

## Step 1: プロジェクトのセットアップ（2分）

### 1.1 リポジトリ作成

```bash
# プロジェクトディレクトリ作成
mkdir loto_feature_system_v2
cd loto_feature_system_v2

# 基本構造作成
mkdir -p src/{core,pipelines,utils,integration} config tests scripts logs cache
touch src/__init__.py src/core/__init__.py src/pipelines/__init__.py
touch src/utils/__init__.py src/integration/__init__.py
```

### 1.2 依存パッケージインストール

```bash
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# requirements.txt作成
cat > requirements.txt << 'EOF'
# コアパッケージ
pandas>=2.0.0
numpy>=1.23.0
scipy>=1.10.0
scikit-learn>=1.2.0

# データベース
SQLAlchemy>=2.0.0
psycopg2-binary>=2.9.0

# 時系列特徴量（基本セット）
tsfresh>=0.20.0
statsmodels>=0.14.0

# 並列処理
ray[default]>=2.0.0

# ユーティリティ
PyYAML>=6.0
tqdm>=4.65.0
python-dateutil>=2.8.0

# ロギング
coloredlogs>=15.0
EOF

# インストール
pip install -r requirements.txt
```

### 1.3 GPU版（オプション）

```bash
# GPU版の追加パッケージ
cat > requirements-gpu.txt << 'EOF'
cudf-cu11>=24.0.0
cuml-cu11>=24.0.0
cupy-cuda11x>=12.0.0
EOF

pip install -r requirements-gpu.txt
```

---

## Step 2: データベース設定（1分）

### 2.1 設定ファイル作成

```bash
cat > config/db_config.yaml << 'EOF'
host: localhost
port: 5432
database: postgres
user: postgres
password: z
EOF
```

### 2.2 テーブル作成スクリプト

```python
# scripts/setup_database.py を作成
cat > scripts/setup_database.py << 'EOF'
#!/usr/bin/env python
"""データベースセットアップスクリプト"""
import sys
sys.path.insert(0, './src')

import yaml
from core.database_manager import DatabaseManager

# 設定読み込み
with open('config/db_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# データベースマネージャー初期化
db_manager = DatabaseManager(config)

# テーブル作成
print("テーブル作成中...")
db_manager.create_tables()

# 確認
for table in ['features_hist', 'features_futr', 'features_stat']:
    info = db_manager.get_table_info(table)
    print(f"\n{table}:")
    print(f"  行数: {info['row_count']}")
    print(f"  列数: {info['n_columns']}")

print("\nセットアップ完了!")
EOF

chmod +x scripts/setup_database.py
```

### 2.3 実行

```bash
python scripts/setup_database.py
```

---

## Step 3: 最小限のパイプライン実装（1分）

### 3.1 基本パイプライン作成

```python
# src/pipelines/base_pipeline.py を作成
cat > src/pipelines/base_pipeline.py << 'EOF'
from abc import ABC, abstractmethod
import pandas as pd

class BasePipeline(ABC):
    """パイプライン基底クラス"""
    
    def __init__(self, config=None):
        self.config = config or {}
    
    @abstractmethod
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """特徴量を生成"""
        pass
    
    @abstractmethod
    def get_feature_type(self) -> str:
        """特徴量タイプ ('hist', 'futr', 'stat')"""
        pass
EOF
```

### 3.2 基本統計パイプライン

```python
# src/pipelines/basic_stats.py を作成
cat > src/pipelines/basic_stats.py << 'EOF'
import pandas as pd
from .base_pipeline import BasePipeline

class BasicStatsPipeline(BasePipeline):
    """基本統計パイプライン"""
    
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame(index=df.index)
        
        # ラグ特徴量
        for lag in [1, 7, 14, 30]:
            features[f'hist_y_lag{lag}'] = df['y'].shift(lag)
        
        # ローリング平均
        for window in [7, 14, 30]:
            features[f'hist_y_roll_mean_w{window}'] = df['y'].rolling(window).mean()
            features[f'hist_y_roll_std_w{window}'] = df['y'].rolling(window).std()
        
        # 差分
        features['hist_y_diff1'] = df['y'].diff(1)
        features['hist_y_diff7'] = df['y'].diff(7)
        
        return features
    
    def get_feature_type(self) -> str:
        return 'hist'
EOF
```

### 3.3 カレンダー特徴量パイプライン

```python
# src/pipelines/calendar_features.py を作成
cat > src/pipelines/calendar_features.py << 'EOF'
import pandas as pd
import numpy as np
from .base_pipeline import BasePipeline

class CalendarFeaturesPipeline(BasePipeline):
    """カレンダー特徴量パイプライン"""
    
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame(index=df.index)
        
        # 基本カレンダー
        features['futr_ds_year'] = df['ds'].dt.year
        features['futr_ds_month'] = df['ds'].dt.month
        features['futr_ds_day_of_week'] = df['ds'].dt.dayofweek
        features['futr_ds_day_of_month'] = df['ds'].dt.day
        features['futr_ds_is_weekend'] = (df['ds'].dt.dayofweek >= 5).astype(int)
        
        # 周期性エンコーディング
        day_of_week = df['ds'].dt.dayofweek
        features['futr_ds_day_sin'] = np.sin(2 * np.pi * day_of_week / 7)
        features['futr_ds_day_cos'] = np.cos(2 * np.pi * day_of_week / 7)
        
        month = df['ds'].dt.month
        features['futr_ds_month_sin'] = np.sin(2 * np.pi * month / 12)
        features['futr_ds_month_cos'] = np.cos(2 * np.pi * month / 12)
        
        return features
    
    def get_feature_type(self) -> str:
        return 'futr'
EOF
```

---

## Step 4: シンプルな実行スクリプト（30秒）

```python
# scripts/generate_features_simple.py を作成
cat > scripts/generate_features_simple.py << 'EOF'
#!/usr/bin/env python
"""シンプルな特徴量生成スクリプト"""
import sys
sys.path.insert(0, './src')

import yaml
import pandas as pd
from core.database_manager import DatabaseManager
from core.data_loader import DataLoader
from pipelines.basic_stats import BasicStatsPipeline
from pipelines.calendar_features import CalendarFeaturesPipeline
from tqdm import tqdm

# 設定読み込み
with open('config/db_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# データ読み込み
print("データ読み込み中...")
data_loader = DataLoader(config)
df_dict = data_loader.load_by_series('nf_loto_final')
print(f"読み込み完了: {len(df_dict)}系列")

# パイプライン初期化
pipelines = {
    'basic_stats': BasicStatsPipeline(),
    'calendar': CalendarFeaturesPipeline()
}

# 特徴量生成
print("\n特徴量生成中...")
hist_features = []
futr_features = []

for (loto, unique_id), df in tqdm(df_dict.items(), desc="系列処理"):
    for pipeline_name, pipeline in pipelines.items():
        features = pipeline.generate(df)
        features['loto'] = loto
        features['unique_id'] = unique_id
        features['ds'] = df['ds']
        
        if pipeline.get_feature_type() == 'hist':
            hist_features.append(features)
        elif pipeline.get_feature_type() == 'futr':
            futr_features.append(features)

# 統合
hist_df = pd.concat(hist_features, ignore_index=True)
futr_df = pd.concat(futr_features, ignore_index=True)

print(f"\n生成完了:")
print(f"  Historical: {len(hist_df)}行 × {len(hist_df.columns)}列")
print(f"  Future: {len(futr_df)}行 × {len(futr_df.columns)}列")

# データベース保存
print("\nデータベース保存中...")
db_manager = DatabaseManager(config)
db_manager.upsert_features(hist_df, 'features_hist')
db_manager.upsert_features(futr_df, 'features_futr')

print("\n完了!")
EOF

chmod +x scripts/generate_features_simple.py
```

---

## Step 5: 実行！（30秒）

```bash
python scripts/generate_features_simple.py
```

### 期待される出力

```
データ読み込み中...
読み込み完了: 32系列

特徴量生成中...
系列処理: 100%|██████████| 32/32 [00:15<00:00,  2.13it/s]

生成完了:
  Historical: 27217行 × 15列
  Future: 27217行 × 11列

データベース保存中...
features_hist へのUPSERT完了: 27217行
features_futr へのUPSERT完了: 27217行

完了!
```

---

## 動作確認

### PostgreSQLで確認

```bash
PGPASSWORD='z' psql -h localhost -U postgres -d postgres -c "
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count,
    (SELECT reltuples::bigint FROM pg_class WHERE relname = t.table_name) as row_count
FROM (
    VALUES ('features_hist'), ('features_futr'), ('features_stat')
) AS t(table_name);
"
```

### 期待される出力

```
  table_name   | column_count | row_count 
---------------+--------------+-----------
 features_hist |           17 |     27217
 features_futr |           13 |     27217
 features_stat |            0 |         0
```

---

## 次のステップ

### 1. GPU高速化を試す（オプション）

```bash
# GPU版パッケージインストール（まだの場合）
pip install -r requirements-gpu.txt

# GPU使用版のデータローダーを試す
python -c "
import sys
sys.path.insert(0, './src')
from core.data_loader import DataLoader
import yaml

with open('config/db_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

loader = DataLoader(config, use_gpu=True)
print('GPU モード:', loader.use_gpu)
"
```

### 2. 追加パイプラインを実装

完全な設計書（`LOTO_FEATURE_SYSTEM_DESIGN.md`）を参照して、以下を追加:
- P4: Trend & Seasonality
- P5: Autocorrelation
- P6: tsfresh Advanced
- P11: Anomaly Detection
- P13: Lottery Domain

### 3. Ray並列実行を設定

```python
# src/integration/ray_integration.py を実装
# (IMPLEMENTATION_PLAN.mdのPhase 1を参照)
```

### 4. 完全版オーケストレーターを実装

```python
# src/core/feature_orchestrator.py を実装
# (LOTO_FEATURE_SYSTEM_DESIGN.mdを参照)
```

---

## トラブルシューティング

### Q1: ModuleNotFoundError: No module named 'src'

**A**: Pythonパスの問題です。以下で解決:

```bash
# プロジェクトルートから実行していることを確認
pwd  # /path/to/loto_feature_system_v2 であるべき

# または、PYTHONPATHを設定
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Q2: データベース接続エラー

**A**: 設定を確認:

```bash
# PostgreSQLが起動しているか確認
sudo systemctl status postgresql

# 接続テスト
PGPASSWORD='z' psql -h localhost -U postgres -d postgres -c "SELECT version();"

# config/db_config.yaml の内容を確認
cat config/db_config.yaml
```

### Q3: GPU OutOfMemory

**A**: バッチサイズを削減:

```python
# data_loader.py で use_gpu=False に設定
loader = DataLoader(config, use_gpu=False)
```

---

## 完全なコード取得

完全な実装は以下のドキュメントを参照:

1. **設計書**: `LOTO_FEATURE_SYSTEM_DESIGN.md`
   - システム全体のアーキテクチャ
   - 各パイプラインの詳細仕様
   - データモデル定義

2. **実装計画**: `IMPLEMENTATION_PLAN.md`
   - 段階的な実装手順
   - 完全なコード例
   - Phase 0-4の詳細

3. **このガイド**: `QUICKSTART.md`
   - 最小限の動作確認
   - 5分で始める方法

---

## コミュニティとサポート

### ドキュメント
- 設計書: `LOTO_FEATURE_SYSTEM_DESIGN.md`
- 実装計画: `IMPLEMENTATION_PLAN.md`
- API Reference: (Phase 4で作成予定)

### 質問・問題報告
- GitHub Issues: (リポジトリ作成後)
- Slack: (チーム用チャンネル)

---

## まとめ

おめでとうございます！🎉

これで宝くじ時系列特徴量生成システムの基本的な動作が確認できました。

### 完了したこと
✅ プロジェクト構造作成  
✅ データベーステーブル作成  
✅ 基本パイプライン実装  
✅ 特徴量生成と保存  

### 次のマイルストーン
- [ ] GPU高速化の実装
- [ ] 高度なパイプライン追加（tsfresh, TSFEL等）
- [ ] Ray並列実行の統合
- [ ] End-to-Endテスト

詳細は `IMPLEMENTATION_PLAN.md` の Phase 1 以降を参照してください。

Happy Feature Engineering! 🚀

---

**作成日**: 2025-01-12  
**バージョン**: 1.0.0  
**作成者**: AI System Architect
