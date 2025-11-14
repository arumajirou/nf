"""
カレンダー特徴量パイプライン
"""
import pandas as pd
import numpy as np
from .base_pipeline import BasePipeline
import logging

try:
    import jpholiday
    JPHOLIDAY_AVAILABLE = True
except ImportError:
    JPHOLIDAY_AVAILABLE = False

logger = logging.getLogger(__name__)

class CalendarFeaturesPipeline(BasePipeline):
    """カレンダー特徴量パイプライン"""
    
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        カレンダー特徴量を生成
        
        Args:
            df: 入力DataFrame (ds 必須)
        
        Returns:
            特徴量DataFrame
        """
        if 'ds' not in df.columns:
            logger.error("ds列が見つかりません")
            return pd.DataFrame()
        
        logger.info(f"{self.name}: 特徴量生成開始")
        
        features = pd.DataFrame(index=df.index)
        features['ds'] = df['ds']
        
        # 日付型に変換
        ds = pd.to_datetime(df['ds'])
        
        # 基本カレンダー特徴量
        features['futr_ds_year'] = ds.dt.year
        features['futr_ds_quarter'] = ds.dt.quarter
        features['futr_ds_month'] = ds.dt.month
        features['futr_ds_week_of_year'] = ds.dt.isocalendar().week
        features['futr_ds_day_of_month'] = ds.dt.day
        features['futr_ds_day_of_year'] = ds.dt.dayofyear
        features['futr_ds_day_of_week'] = ds.dt.dayofweek
        features['futr_ds_days_in_month'] = ds.dt.days_in_month
        features['futr_ds_is_weekend'] = (ds.dt.dayofweek >= 5).astype(int)
        features['futr_ds_leapyear'] = ds.dt.is_leap_year.astype(int)
        features['futr_ds_quarter_start'] = ds.dt.is_quarter_start.astype(int)
        features['futr_ds_quarter_end'] = ds.dt.is_quarter_end.astype(int)
        features['futr_ds_month_start'] = ds.dt.is_month_start.astype(int)
        features['futr_ds_month_end'] = ds.dt.is_month_end.astype(int)
        
        # 周期性エンコーディング
        # 曜日
        day_of_week = ds.dt.dayofweek
        features['futr_ds_day_sin'] = np.sin(2 * np.pi * day_of_week / 7)
        features['futr_ds_day_cos'] = np.cos(2 * np.pi * day_of_week / 7)
        
        # 週（年内）
        week_of_year = ds.dt.isocalendar().week
        features['futr_ds_week_sin'] = np.sin(2 * np.pi * week_of_year / 52)
        features['futr_ds_week_cos'] = np.cos(2 * np.pi * week_of_year / 52)
        
        # 月
        month = ds.dt.month
        features['futr_ds_month_sin'] = np.sin(2 * np.pi * month / 12)
        features['futr_ds_month_cos'] = np.cos(2 * np.pi * month / 12)
        
        # 四半期
        quarter = ds.dt.quarter
        features['futr_ds_quarter_sin'] = np.sin(2 * np.pi * quarter / 4)
        features['futr_ds_quarter_cos'] = np.cos(2 * np.pi * quarter / 4)
        
        # フーリエ特徴量
        fourier_orders = self.config.get('fourier_orders', [
            {'period': 7, 'orders': [1, 2]},
            {'period': 30.4375, 'orders': [1, 2]},
            {'period': 365.25, 'orders': [1, 2]}
        ])
        
        # 時系列のインデックス（0から始まる連番）
        t = np.arange(len(df))
        
        for fourier_config in fourier_orders:
            period = fourier_config['period']
            orders = fourier_config['orders']
            
            for k in orders:
                # 周期を整数に丸める（カラム名用）
                period_str = str(int(period)) if period == int(period) else f"{period:.2f}".replace('.', '_')
                
                features[f'futr_p{period_str}_k{k}_sin'] = np.sin(2 * np.pi * k * t / period)
                features[f'futr_p{period_str}_k{k}_cos'] = np.cos(2 * np.pi * k * t / period)
        
        # 休日特徴量（日本の祝日）
        if self.config.get('include_holiday', True) and JPHOLIDAY_AVAILABLE:
            features['futr_is_holiday'] = ds.apply(lambda x: int(jpholiday.is_holiday(x))).values
            
            # 最後の休日からの日数
            features['futr_days_since_holiday'] = 0
            features['futr_days_until_holiday'] = 0
            
            # 簡易実装（改善可能）
            for i in range(len(df)):
                date = ds.iloc[i].date()
                
                # 最後の休日からの日数
                days_since = 0
                for d in range(1, 365):
                    check_date = date - pd.Timedelta(days=d)
                    if jpholiday.is_holiday(check_date):
                        days_since = d
                        break
                features.loc[i, 'futr_days_since_holiday'] = days_since
                
                # 次の休日までの日数
                days_until = 0
                for d in range(1, 365):
                    check_date = date + pd.Timedelta(days=d)
                    if jpholiday.is_holiday(check_date):
                        days_until = d
                        break
                features.loc[i, 'futr_days_until_holiday'] = days_until
        else:
            # 休日機能が無効またはjpholidayが利用不可
            features['futr_is_holiday'] = 0
            features['futr_days_since_holiday'] = 0
            features['futr_days_until_holiday'] = 0
        
        logger.info(f"{self.name}: {len(features.columns)}個の特徴量を生成")
        return features
    
    def get_feature_type(self) -> str:
        return 'futr'
