"""
データ読み込みを管理するモジュール
"""
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
            'duplicates': df.duplicated(subset=['loto', 'unique_id', 'ds']).sum() if all(c in df.columns for c in ['loto', 'unique_id', 'ds']) else 0,
            'date_range': {
                'min': str(df['ds'].min()) if 'ds' in df.columns else None,
                'max': str(df['ds'].max()) if 'ds' in df.columns else None
            },
            'unique_series': len(df.groupby(['loto', 'unique_id'])) if all(c in df.columns for c in ['loto', 'unique_id']) else None
        }
        
        return results
