# 宝くじ時系列特徴量生成システム 実装計画

## エグゼクティブサマリー

本文書は、「宝くじ時系列特徴量生成システム」の段階的な実装計画を定義します。システムは4つのフェーズに分けて実装し、各フェーズで動作可能なシステムを段階的に構築します。

## Phase 0: 基盤構築（Week 1-2）

### 目標
- プロジェクト基盤の構築
- 開発環境のセットアップ
- 基本的なデータパイプラインの確立

### 成果物

#### 1. プロジェクト構造

```
loto_feature_system_v2/
├── README.md
├── requirements.txt
├── requirements-gpu.txt
├── setup.py
├── .gitignore
├── pytest.ini
├── config/
│   ├── default_config.yaml
│   ├── pipeline_config.yaml
│   ├── db_config.yaml.template
│   └── logging_config.yaml
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── feature_orchestrator.py
│   │   └── database_manager.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   └── base_pipeline.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── gpu_utils.py
│   │   ├── validation.py
│   │   ├── logging_config.py
│   │   └── metrics.py
│   └── integration/
│       ├── __init__.py
│       ├── ray_integration.py
│       └── dask_integration.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_core/
│       ├── __init__.py
│       ├── test_data_loader.py
│       └── test_database_manager.py
├── scripts/
│   ├── setup_database.py
│   ├── run_feature_generation.py
│   └── validate_features.py
└── notebooks/
    └── 00_setup_verification.ipynb
```

#### 2. コア実装

**A. database_manager.py (完全版)**

```python
from typing import List, Dict, Any, Optional
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Date, Float, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """データベース操作を管理するクラス"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Args:
            config: データベース設定
                - host: ホスト名
                - port: ポート番号
                - database: データベース名
                - user: ユーザー名
                - password: パスワード
        """
        self.config = config
        self.engine = self._create_engine()
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
    
    def _create_engine(self):
        """SQLAlchemyエンジンを作成"""
        url = (
            f"postgresql://{self.config['user']}:{self.config['password']}"
            f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        )
        return create_engine(
            url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            echo=False
        )
    
    def create_tables(self):
        """全テーブルを作成"""
        logger.info("テーブル作成開始")
        
        # features_hist テーブル
        self._create_features_hist_table()
        
        # features_futr テーブル
        self._create_features_futr_table()
        
        # features_stat テーブル
        self._create_features_stat_table()
        
        logger.info("テーブル作成完了")
    
    def _create_features_hist_table(self):
        """Historical特徴量テーブルを作成"""
        table_name = 'features_hist'
        
        # テーブルが既に存在する場合はスキップ
        if self.engine.dialect.has_table(self.engine.connect(), table_name):
            logger.info(f"{table_name} テーブルは既に存在します")
            return
        
        # テーブル定義（動的に列を追加）
        columns = [
            Column('loto', String(50), primary_key=True),
            Column('unique_id', String(10), primary_key=True),
            Column('ds', Date, primary_key=True),
        ]
        
        # 基本統計特徴量
        for lag in [1, 2, 3, 7, 14, 21, 28, 30, 60]:
            columns.append(Column(f'hist_y_lag{lag}', Float))
        
        for window in [3, 7, 14, 21, 30, 60, 90]:
            columns.extend([
                Column(f'hist_y_roll_mean_w{window}', Float),
                Column(f'hist_y_roll_std_w{window}', Float),
                Column(f'hist_y_roll_min_w{window}', Float),
                Column(f'hist_y_roll_max_w{window}', Float),
                Column(f'hist_y_roll_median_w{window}', Float),
                Column(f'hist_y_roll_q25_w{window}', Float),
                Column(f'hist_y_roll_q75_w{window}', Float),
            ])
        
        # メタデータ
        columns.extend([
            Column('created_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
            Column('updated_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
        ])
        
        table = Table(table_name, self.metadata, *columns)
        table.create(self.engine)
        
        # インデックス作成
        with self.engine.connect() as conn:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_loto_uid ON {table_name} (loto, unique_id)"))
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_ds ON {table_name} (ds)"))
            conn.commit()
        
        logger.info(f"{table_name} テーブル作成完了")
    
    def _create_features_futr_table(self):
        """Future特徴量テーブルを作成"""
        table_name = 'features_futr'
        
        if self.engine.dialect.has_table(self.engine.connect(), table_name):
            logger.info(f"{table_name} テーブルは既に存在します")
            return
        
        columns = [
            Column('loto', String(50), primary_key=True),
            Column('unique_id', String(10), primary_key=True),
            Column('ds', Date, primary_key=True),
            
            # カレンダー特徴量
            Column('futr_ds_year', Integer),
            Column('futr_ds_quarter', Integer),
            Column('futr_ds_month', Integer),
            Column('futr_ds_week_of_year', Integer),
            Column('futr_ds_day_of_month', Integer),
            Column('futr_ds_day_of_year', Integer),
            Column('futr_ds_day_of_week', Integer),
            Column('futr_ds_days_in_month', Integer),
            Column('futr_ds_is_weekend', Boolean),
            Column('futr_ds_leapyear', Boolean),
            Column('futr_ds_quarter_start', Boolean),
            Column('futr_ds_quarter_end', Boolean),
            Column('futr_ds_month_start', Boolean),
            Column('futr_ds_month_end', Boolean),
            
            # 周期性エンコーディング
            Column('futr_ds_day_sin', Float),
            Column('futr_ds_day_cos', Float),
            Column('futr_ds_week_sin', Float),
            Column('futr_ds_week_cos', Float),
            Column('futr_ds_month_sin', Float),
            Column('futr_ds_month_cos', Float),
            Column('futr_ds_quarter_sin', Float),
            Column('futr_ds_quarter_cos', Float),
            
            # フーリエ特徴量
            Column('futr_p7_k1_sin', Float),
            Column('futr_p7_k1_cos', Float),
            Column('futr_p7_k2_sin', Float),
            Column('futr_p7_k2_cos', Float),
            Column('futr_p30_k1_sin', Float),
            Column('futr_p30_k1_cos', Float),
            Column('futr_p30_k2_sin', Float),
            Column('futr_p30_k2_cos', Float),
            Column('futr_p365_k1_sin', Float),
            Column('futr_p365_k1_cos', Float),
            Column('futr_p365_k2_sin', Float),
            Column('futr_p365_k2_cos', Float),
            
            # 休日特徴量
            Column('futr_is_holiday', Boolean),
            Column('futr_days_since_holiday', Integer),
            Column('futr_days_until_holiday', Integer),
            
            # メタデータ
            Column('created_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
            Column('updated_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
        ]
        
        table = Table(table_name, self.metadata, *columns)
        table.create(self.engine)
        
        # インデックス
        with self.engine.connect() as conn:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_loto_uid ON {table_name} (loto, unique_id)"))
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_ds ON {table_name} (ds)"))
            conn.commit()
        
        logger.info(f"{table_name} テーブル作成完了")
    
    def _create_features_stat_table(self):
        """Static特徴量テーブルを作成"""
        table_name = 'features_stat'
        
        if self.engine.dialect.has_table(self.engine.connect(), table_name):
            logger.info(f"{table_name} テーブルは既に存在します")
            return
        
        columns = [
            Column('loto', String(50), primary_key=True),
            Column('unique_id', String(10), primary_key=True),
            
            # 系列レベル統計
            Column('stat_y_global_mean', Float),
            Column('stat_y_global_std', Float),
            Column('stat_y_global_min', Float),
            Column('stat_y_global_max', Float),
            Column('stat_y_global_range', Float),
            Column('stat_y_global_cv', Float),
            Column('stat_y_global_skewness', Float),
            Column('stat_y_global_kurtosis', Float),
            
            # 系列メタ情報
            Column('stat_series_length', Integer),
            Column('stat_series_start_date', Date),
            Column('stat_series_end_date', Date),
            Column('stat_series_frequency_days', Float),
            
            # tsfeatures系列レベル
            Column('stat_trend_strength', Float),
            Column('stat_seasonality_strength', Float),
            Column('stat_linearity', Float),
            Column('stat_curvature', Float),
            Column('stat_spikiness', Float),
            Column('stat_stability', Float),
            Column('stat_lumpiness', Float),
            Column('stat_entropy_tsfeatures', Float),
            Column('stat_hurst_exponent', Float),
            Column('stat_crossing_points', Integer),
            Column('stat_flat_spots', Float),
            
            # ドメイン固有
            Column('stat_unique_id_category', String(10)),
            Column('stat_loto_type', String(50)),
            Column('stat_loto_number_range_min', Integer),
            Column('stat_loto_number_range_max', Integer),
            Column('stat_loto_draw_count_total', Integer),
            
            # メタデータ
            Column('created_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
            Column('updated_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
        ]
        
        table = Table(table_name, self.metadata, *columns)
        table.create(self.engine)
        
        # インデックス
        with self.engine.connect() as conn:
            conn.execute(text(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_loto ON {table_name} (loto)"))
            conn.commit()
        
        logger.info(f"{table_name} テーブル作成完了")
    
    def upsert_features(
        self,
        df: pd.DataFrame,
        table_name: str,
        batch_size: int = 5000
    ) -> int:
        """
        特徴量をUPSERT（INSERT or UPDATE）
        
        Args:
            df: 特徴量DataFrame
            table_name: テーブル名
            batch_size: バッチサイズ
        
        Returns:
            挿入/更新された行数
        """
        logger.info(f"{table_name} へのUPSERT開始: {len(df)}行")
        
        total_rows = 0
        
        # バッチ処理
        for start_idx in range(0, len(df), batch_size):
            end_idx = min(start_idx + batch_size, len(df))
            batch_df = df.iloc[start_idx:end_idx]
            
            # 辞書形式に変換
            records = batch_df.to_dict('records')
            
            # UPSERTステートメント作成
            stmt = insert(self.metadata.tables[table_name]).values(records)
            
            # 主キー以外の列を更新
            update_dict = {
                col.name: stmt.excluded[col.name]
                for col in self.metadata.tables[table_name].columns
                if not col.primary_key and col.name not in ['created_at']
            }
            update_dict['updated_at'] = text('CURRENT_TIMESTAMP')
            
            stmt = stmt.on_conflict_do_update(
                index_elements=['loto', 'unique_id'] + (['ds'] if 'ds' in batch_df.columns else []),
                set_=update_dict
            )
            
            # 実行
            with self.engine.begin() as conn:
                result = conn.execute(stmt)
                total_rows += result.rowcount
            
            logger.debug(f"バッチ {start_idx}-{end_idx} 完了")
        
        logger.info(f"{table_name} へのUPSERT完了: {total_rows}行")
        return total_rows
    
    def load_table(self, table_name: str, filters: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        テーブルからデータを読み込み
        
        Args:
            table_name: テーブル名
            filters: フィルタ条件 (例: {'loto': 'bingo5', 'unique_id': 'N1'})
        
        Returns:
            DataFrame
        """
        query = f"SELECT * FROM {table_name}"
        
        if filters:
            where_clauses = [f"{k} = :{k}" for k in filters.keys()]
            query += " WHERE " + " AND ".join(where_clauses)
        
        return pd.read_sql(text(query), self.engine, params=filters)
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """任意のSQLクエリを実行"""
        return pd.read_sql(text(query), self.engine, params=params)
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """テーブル情報を取得"""
        with self.engine.connect() as conn:
            # 行数
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            row_count = result.scalar()
            
            # 列情報
            result = conn.execute(text(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
            """))
            columns = {row[0]: row[1] for row in result}
        
        return {
            'row_count': row_count,
            'columns': columns,
            'n_columns': len(columns)
        }
```

**B. data_loader.py (完全版)**

```python
from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import logging

try:
    import cudf
    CUDF_AVAILABLE = True
except ImportError:
    CUDF_AVAILABLE = False

logger = logging.getLogger(__name__)

class DataLoader:
    """データ読み込みを管理するクラス"""
    
    def __init__(self, config: Dict[str, Any], use_gpu: bool = False):
        """
        Args:
            config: データベース設定
            use_gpu: GPU使用フラグ
        """
        self.config = config
        self.use_gpu = use_gpu and CUDF_AVAILABLE
        self.engine = self._create_engine()
        
        if self.use_gpu:
            logger.info("GPU モード有効")
        else:
            logger.info("CPU モード")
    
    def _create_engine(self):
        """SQLAlchemyエンジンを作成"""
        url = (
            f"postgresql://{self.config['user']}:{self.config['password']}"
            f"@{self.config['host']}:{self.config['port']}/{self.config['database']}"
        )
        return create_engine(url, pool_pre_ping=True)
    
    def load_from_db(
        self,
        table_name: str,
        filters: Optional[Dict[str, Any]] = None,
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        データベースからデータを読み込み
        
        Args:
            table_name: テーブル名
            filters: フィルタ条件
            columns: 取得する列（Noneの場合は全列）
        
        Returns:
            DataFrame（GPUモードの場合はcuDF.DataFrame）
        """
        # クエリ構築
        col_str = ", ".join(columns) if columns else "*"
        query = f"SELECT {col_str} FROM {table_name}"
        
        if filters:
            where_clauses = [f"{k} = :{k}" for k in filters.keys()]
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += " ORDER BY loto, unique_id, ds"
        
        logger.info(f"クエリ実行: {query[:100]}...")
        
        # データ読み込み
        df = pd.read_sql(text(query), self.engine, params=filters)
        
        logger.info(f"読み込み完了: {len(df)}行")
        
        # GPU変換
        if self.use_gpu:
            df = cudf.from_pandas(df)
            logger.info("cuDFに変換完了")
        
        return df
    
    def load_by_series(
        self,
        table_name: str,
        loto: Optional[str] = None,
        unique_ids: Optional[List[str]] = None
    ) -> Dict[tuple, pd.DataFrame]:
        """
        系列ごとにデータを読み込み
        
        Args:
            table_name: テーブル名
            loto: 宝くじ種類（Noneの場合は全て）
            unique_ids: unique_idリスト（Noneの場合は全て）
        
        Returns:
            {(loto, unique_id): DataFrame} の辞書
        """
        filters = {}
        if loto:
            filters['loto'] = loto
        
        df = self.load_from_db(table_name, filters)
        
        # cuDFの場合はpandasに変換（groupbyのため）
        if self.use_gpu:
            df = df.to_pandas()
        
        # 系列ごとに分割
        df_dict = {}
        for (loto_val, uid), group in df.groupby(['loto', 'unique_id']):
            if unique_ids is None or uid in unique_ids:
                df_dict[(loto_val, uid)] = group.sort_values('ds').reset_index(drop=True)
        
        logger.info(f"{len(df_dict)}系列を読み込み完了")
        return df_dict
    
    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        データの基本的な検証
        
        Returns:
            検証結果の辞書
        """
        # cuDF対応
        if self.use_gpu:
            df = df.to_pandas()
        
        results = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'missing_values': df.isna().sum().to_dict(),
            'duplicates': df.duplicated(subset=['loto', 'unique_id', 'ds']).sum(),
            'date_range': {
                'min': df['ds'].min() if 'ds' in df.columns else None,
                'max': df['ds'].max() if 'ds' in df.columns else None
            },
            'unique_series': len(df.groupby(['loto', 'unique_id'])) if 'loto' in df.columns else None
        }
        
        return results
```

#### 3. 設定ファイル

**config/default_config.yaml**

```yaml
# システムデフォルト設定

system:
  name: "Loto Feature Generation System"
  version: "2.0.0"
  
# データベース接続（環境変数で上書き可能）
database:
  host: "${DB_HOST:localhost}"
  port: "${DB_PORT:5432}"
  database: "${DB_NAME:postgres}"
  user: "${DB_USER:postgres}"
  password: "${DB_PASSWORD:z}"
  
  # 接続プール
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30

# 並列実行
parallel:
  use_ray: true
  use_dask: false
  n_workers: 4
  
  # GPU設定
  use_gpu: true
  gpu_per_worker: 0.25
  gpu_memory_limit: 4294967296  # 4GB

# バッチ処理
batch:
  size: 8
  prefetch: 2

# キャッシング
cache:
  enabled: true
  directory: "./cache"
  ttl: 86400  # 24時間

# ロギング
logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "./logs/feature_generation.log"
  max_bytes: 10485760  # 10MB
  backup_count: 5

# エラーハンドリング
error_handling:
  mode: "warn"  # "raise", "warn", "ignore"
  retry_attempts: 3
  retry_delay: 5
```

#### 4. テストコード

**tests/conftest.py**

```python
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture
def sample_config():
    """テスト用設定"""
    return {
        'host': 'localhost',
        'port': 5432,
        'database': 'test_db',
        'user': 'test_user',
        'password': 'test_pass'
    }

@pytest.fixture
def sample_timeseries():
    """テスト用時系列データ"""
    start_date = datetime(2020, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(100)]
    
    return pd.DataFrame({
        'loto': ['bingo5'] * 100,
        'unique_id': ['N1'] * 100,
        'ds': dates,
        'y': np.random.randint(1, 40, 100),
        'num': range(1, 101),
        'co': np.random.randint(0, 10000000, 100)
    })

@pytest.fixture
def sample_series_dict(sample_timeseries):
    """テスト用系列辞書"""
    return {
        ('bingo5', 'N1'): sample_timeseries
    }
```

### タスクリスト

- [ ] プロジェクト構造作成
- [ ] requirements.txt作成
- [ ] database_manager.py実装
- [ ] data_loader.py実装
- [ ] 設定ファイル作成
- [ ] テストコード作成
- [ ] setup_database.pyスクリプト作成
- [ ] ドキュメント作成
- [ ] コードレビュー

### 完了条件
- [ ] 全ユニットテストが通過
- [ ] データベーステーブルが正常に作成される
- [ ] データの読み込みと保存が正常に動作する
- [ ] ドキュメントが完備されている

---

## Phase 1: 基本パイプライン実装（Week 3-4）

### 目標
- 優先度の高い基本パイプラインの実装
- GPU高速化の基盤構築

### 成果物

#### 実装するパイプライン

1. **P1: Basic Statistics Pipeline**
   - ローリング統計（平均、標準偏差、最小値、最大値等）
   - GPU対応（cuDF使用）

2. **P2: Rolling Windows Pipeline**
   - IQR、Z-score、平均からの偏差
   - GPU対応

3. **P3: Lag & Difference Pipeline**
   - ラグ特徴量
   - 差分・パーセント変化
   - GPU対応

4. **P12: Calendar Features Pipeline**
   - カレンダー特徴量
   - 周期性エンコーディング
   - フーリエ特徴量
   - GPU対応

5. **P11: Anomaly Detection Pipeline**
   - Z-score
   - IQR-based
   - Isolation Forest（cuML使用）
   - GPU対応

### タスクリスト

**Week 3:**
- [ ] base_pipeline.py実装
- [ ] basic_stats.py実装
- [ ] rolling_windows.py実装
- [ ] lag_diff.py実装
- [ ] GPU加速の検証

**Week 4:**
- [ ] calendar_features.py実装
- [ ] anomaly_detection.py実装
- [ ] Ray統合（ray_integration.py）
- [ ] パフォーマンステスト
- [ ] ドキュメント更新

### 完了条件
- [ ] 5つのパイプラインが実装され、テストが通過
- [ ] GPU版がCPU版より3倍以上高速
- [ ] 全パイプラインがRay経由で並列実行可能
- [ ] エラーハンドリングが適切に動作

---

## Phase 2: 高度な特徴量パイプライン実装（Week 5-6）

### 目標
- tsfresh, TSFEL, catch22等の高度なライブラリ統合
- 異常値検出の強化

### 成果物

#### 実装するパイプライン

1. **P4: Trend & Seasonality Pipeline**
   - STL分解
   - トレンド強度・季節性強度
   - ドローダウン/ドローアップ

2. **P5: Autocorrelation Pipeline**
   - ACF/PACF
   - ローリング相関

3. **P6: tsfresh Advanced Pipeline**
   - 厳選された30-40特徴量
   - 並列実行対応

4. **P7: TSFEL Spectral Pipeline**
   - スペクトル特徴量
   - 時間領域特徴量

5. **P8: catch22 Canonical Pipeline**
   - 22個の正準特徴量

6. **P9: AntroPy Entropy Pipeline**
   - 各種エントロピー
   - Hjorth parameters

7. **P10: Matrix Profile Pipeline**
   - Matrix Profile統計量
   - モチーフ/ディスコード検出

### タスクリスト

**Week 5:**
- [ ] trend_seasonality.py実装
- [ ] autocorrelation.py実装
- [ ] tsfresh_advanced.py実装
- [ ] tsfel_spectral.py実装

**Week 6:**
- [ ] catch22_canonical.py実装
- [ ] antropy_entropy.py実装
- [ ] matrix_profile.py実装
- [ ] パイプライン統合テスト
- [ ] パフォーマンスベンチマーク

### 完了条件
- [ ] 7つのパイプラインが実装され、テストが通過
- [ ] 計算時間が許容範囲内（目標: 各パイプライン < 2分）
- [ ] 特徴量の品質検証が完了
- [ ] ドキュメントが更新されている

---

## Phase 3: ドメイン特化とシステム統合（Week 7-8）

### 目標
- 宝くじドメイン固有の特徴量実装
- 全システムの統合とEnd-to-Endテスト

### 成果物

#### 実装するパイプライン

1. **P13: Lottery Domain Pipeline**
   - ホット/コールド分析
   - 数字の周期性
   - 連続出現回数
   - 賞金額との相関

2. **P14: Static Features Pipeline**
   - 系列レベル統計
   - tsfeatures系列レベル特徴量

#### システム統合

**A. feature_orchestrator.py（完全版）**

```python
# (前述のコード参照)
```

**B. 実行スクリプト強化**

```python
# scripts/run_feature_generation.py
# (前述のコード参照)
```

### タスクリスト

**Week 7:**
- [ ] lottery_domain.py実装
- [ ] static_features.py実装
- [ ] feature_orchestrator.py統合
- [ ] 全パイプライン連携テスト

**Week 8:**
- [ ] End-to-Endテスト
- [ ] パフォーマンス最適化
- [ ] エラーハンドリング強化
- [ ] 本番環境準備
- [ ] ドキュメント完成

### 完了条件
- [ ] 全パイプラインが統合され、正常動作
- [ ] End-to-Endテストが全てパス
- [ ] パフォーマンス目標達成（全体 < 5分）
- [ ] 本番環境デプロイ準備完了

---

## Phase 4: 本番デプロイと運用開始（Week 9-10）

### 目標
- 本番環境へのデプロイ
- 監視・運用体制の構築
- ドキュメント完備

### 成果物

#### 1. デプロイメント

**A. Docker化**

```dockerfile
# Dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 基本パッケージ
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python依存パッケージ
COPY requirements.txt requirements-gpu.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-gpu.txt

# アプリケーション
COPY . .

# エントリーポイント
ENTRYPOINT ["python", "scripts/run_feature_generation.py"]
```

**B. Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: loto_features
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  feature_generator:
    build: .
    depends_on:
      - postgres
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: loto_features
      DB_USER: postgres
      DB_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
      - ./cache:/app/cache
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  postgres_data:
```

#### 2. CI/CD

**A. GitHub Actions**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      env:
        DB_HOST: localhost
        DB_PORT: 5432
        DB_NAME: test_db
        DB_USER: test_user
        DB_PASSWORD: test_pass
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

#### 3. 監視・アラート

**A. ヘルスチェック**

```python
# scripts/health_check.py
import logging
from src.core.database_manager import DatabaseManager
from src.utils.metrics import PerformanceMetrics

def health_check():
    """システムヘルスチェック"""
    checks = {
        'database': False,
        'gpu': False,
        'disk_space': False
    }
    
    # データベース接続
    try:
        db_manager = DatabaseManager(config)
        with db_manager.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks['database'] = True
    except Exception as e:
        logging.error(f"Database check failed: {e}")
    
    # GPU確認
    try:
        import cupy as cp
        checks['gpu'] = cp.cuda.runtime.getDeviceCount() > 0
    except:
        pass
    
    # ディスク容量
    import shutil
    stat = shutil.disk_usage('/')
    checks['disk_space'] = stat.free > 10 * 1024**3  # 10GB以上
    
    return checks

if __name__ == "__main__":
    results = health_check()
    print(json.dumps(results, indent=2))
    exit(0 if all(results.values()) else 1)
```

#### 4. ドキュメント

- [ ] README.md（完全版）
- [ ] API_REFERENCE.md
- [ ] PIPELINE_GUIDE.md
- [ ] TROUBLESHOOTING.md
- [ ] DEPLOYMENT_GUIDE.md

### タスクリスト

**Week 9:**
- [ ] Dockerfile作成
- [ ] Docker Compose設定
- [ ] CI/CD構築
- [ ] ヘルスチェック実装
- [ ] 本番環境セットアップ

**Week 10:**
- [ ] 本番デプロイ実行
- [ ] 監視ダッシュボード構築
- [ ] アラート設定
- [ ] 運用手順書作成
- [ ] ドキュメント最終化

### 完了条件
- [ ] 本番環境で正常動作
- [ ] CI/CDパイプラインが機能
- [ ] 監視・アラートが稼働
- [ ] ドキュメントが完備
- [ ] 運用チームへの引き継ぎ完了

---

## マイルストーン

| フェーズ | 期間 | 主要成果物 | 完了条件 |
|---------|------|-----------|---------|
| Phase 0 | Week 1-2 | 基盤構築 | データパイプライン動作 |
| Phase 1 | Week 3-4 | 基本パイプライン | 5パイプライン実装 |
| Phase 2 | Week 5-6 | 高度なパイプライン | 7パイプライン実装 |
| Phase 3 | Week 7-8 | システム統合 | End-to-End動作 |
| Phase 4 | Week 9-10 | 本番デプロイ | 本番稼働開始 |

---

## リスクと対策

| リスク | 影響度 | 確率 | 対策 |
|--------|-------|------|-----|
| GPU環境構築の遅延 | 高 | 中 | CPU版を先行実装 |
| 外部ライブラリの不具合 | 中 | 低 | バージョン固定、代替案準備 |
| パフォーマンス目標未達 | 高 | 中 | 早期ベンチマーク、最適化時間確保 |
| データ品質問題 | 中 | 中 | 検証強化、エラーハンドリング |

---

## 次のアクション

### 即時実行（今週）
1. プロジェクト構造作成
2. requirements.txt作成
3. データベース接続テスト
4. 基本的なデータ読み込みテスト

### 来週
1. database_manager.py完全実装
2. data_loader.py完全実装
3. 基本パイプライン実装開始
4. GPU環境セットアップ

### 今月末まで
1. Phase 0完了
2. Phase 1の50%完了
3. 中間レビュー実施

---

**作成日**: 2025-01-12  
**バージョン**: 1.0.0  
**作成者**: AI System Architect
