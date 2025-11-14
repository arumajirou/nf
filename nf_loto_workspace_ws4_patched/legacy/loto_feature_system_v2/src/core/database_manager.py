"""
データベース操作を管理するモジュール
"""
from typing import List, Dict, Any, Optional
import pandas as pd
from sqlalchemy import (
    create_engine, text, MetaData, Table, Column, 
    Integer, String, Date, Float, Boolean, TIMESTAMP
)
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
        with self.engine.connect() as conn:
            if self.engine.dialect.has_table(conn, table_name):
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
            Column('updated_at', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
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
        
        with self.engine.connect() as conn:
            if self.engine.dialect.has_table(conn, table_name):
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
        
        with self.engine.connect() as conn:
            if self.engine.dialect.has_table(conn, table_name):
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
        
        # テーブルをメタデータに反映
        self.metadata.reflect(bind=self.engine, only=[table_name])
        
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
            
            # 主キー列を取得
            primary_keys = ['loto', 'unique_id']
            if 'ds' in batch_df.columns:
                primary_keys.append('ds')
            
            stmt = stmt.on_conflict_do_update(
                index_elements=primary_keys,
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
