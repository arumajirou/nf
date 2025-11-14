"""
基本統計パイプライン
"""
import pandas as pd
import numpy as np
from .base_pipeline import BasePipeline
import logging

logger = logging.getLogger(__name__)

class BasicStatsPipeline(BasePipeline):
    """基本統計特徴量パイプライン"""
    
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        基本統計特徴量を生成
        
        Args:
            df: 入力DataFrame (ds, y 必須)
        
        Returns:
            特徴量DataFrame
        """
        if not self.validate_input(df):
            return pd.DataFrame()
        
        logger.info(f"{self.name}: 特徴量生成開始")
        
        features = pd.DataFrame(index=df.index)
        features['ds'] = df['ds']
        
        # ラグ特徴量
        lag_windows = self.config.get('lag_windows', [1, 2, 3, 7, 14, 21, 28, 30, 60])
        for lag in lag_windows:
            features[f'hist_y_lag{lag}'] = df['y'].shift(lag)
        
        # ローリング統計
        rolling_windows = self.config.get('rolling_windows', [3, 7, 14, 21, 30, 60, 90])
        rolling_stats = self.config.get('rolling_stats', ['mean', 'std', 'min', 'max', 'median', 'q25', 'q75'])
        
        for window in rolling_windows:
            rolling = df['y'].rolling(window=window, min_periods=1)
            
            if 'mean' in rolling_stats:
                features[f'hist_y_roll_mean_w{window}'] = rolling.mean()
            if 'std' in rolling_stats:
                features[f'hist_y_roll_std_w{window}'] = rolling.std()
            if 'min' in rolling_stats:
                features[f'hist_y_roll_min_w{window}'] = rolling.min()
            if 'max' in rolling_stats:
                features[f'hist_y_roll_max_w{window}'] = rolling.max()
            if 'median' in rolling_stats:
                features[f'hist_y_roll_median_w{window}'] = rolling.median()
            if 'q25' in rolling_stats:
                features[f'hist_y_roll_q25_w{window}'] = rolling.quantile(0.25)
            if 'q75' in rolling_stats:
                features[f'hist_y_roll_q75_w{window}'] = rolling.quantile(0.75)
        
        # 差分
        features['hist_y_diff1'] = df['y'].diff(1)
        features['hist_y_diff7'] = df['y'].diff(7)
        
        # パーセント変化
        features['hist_y_pct_change1'] = df['y'].pct_change(1)
        features['hist_y_pct_change7'] = df['y'].pct_change(7)
        
        logger.info(f"{self.name}: {len(features.columns)}個の特徴量を生成")
        return features
    
    def get_feature_type(self) -> str:
        return 'hist'
