"""
パイプライン基底クラス
"""
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BasePipeline(ABC):
    """パイプライン基底クラス"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Args:
            config: パイプライン設定
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        logger.info(f"{self.name} パイプライン初期化")
    
    @abstractmethod
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        特徴量を生成
        
        Args:
            df: 入力DataFrame (loto, unique_id, ds, y 必須)
        
        Returns:
            特徴量DataFrame
        """
        pass
    
    @abstractmethod
    def get_feature_type(self) -> str:
        """
        特徴量タイプを返す
        
        Returns:
            'hist', 'futr', 'stat' のいずれか
        """
        pass
    
    def validate_input(self, df: pd.DataFrame) -> bool:
        """
        入力データの検証
        
        Args:
            df: 入力DataFrame
        
        Returns:
            検証結果
        """
        required_columns = ['ds', 'y']
        
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"必須カラム {col} が見つかりません")
                return False
        
        if len(df) == 0:
            logger.error("空のDataFrameです")
            return False
        
        return True
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """
        パイプライン情報を返す
        
        Returns:
            パイプライン情報の辞書
        """
        return {
            'name': self.name,
            'feature_type': self.get_feature_type(),
            'config': self.config
        }
