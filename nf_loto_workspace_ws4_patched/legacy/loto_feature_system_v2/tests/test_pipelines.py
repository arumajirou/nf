"""
パイプラインのユニットテスト
"""
import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipelines.basic_stats import BasicStatsPipeline
from pipelines.calendar_features import CalendarFeaturesPipeline

class TestBasicStatsPipeline:
    """BasicStatsPipelineのテスト"""
    
    def test_initialization(self, pipeline_config):
        """パイプライン初期化テスト"""
        pipeline = BasicStatsPipeline(pipeline_config)
        assert pipeline is not None
        assert pipeline.get_feature_type() == 'hist'
    
    def test_generate_features(self, sample_timeseries, pipeline_config):
        """特徴量生成テスト"""
        pipeline = BasicStatsPipeline(pipeline_config)
        features = pipeline.generate(sample_timeseries)
        
        # 特徴量が生成されているか
        assert len(features) > 0
        assert 'ds' in features.columns
        
        # ラグ特徴量が生成されているか
        assert 'hist_y_lag1' in features.columns
        assert 'hist_y_lag7' in features.columns
        
        # ローリング特徴量が生成されているか
        assert 'hist_y_roll_mean_w7' in features.columns
        assert 'hist_y_roll_std_w7' in features.columns
    
    def test_validate_input(self, pipeline_config):
        """入力検証テスト"""
        pipeline = BasicStatsPipeline(pipeline_config)
        
        # 正常なデータ
        valid_df = pd.DataFrame({
            'ds': pd.date_range('2020-01-01', periods=10),
            'y': range(10)
        })
        assert pipeline.validate_input(valid_df) == True
        
        # dsが無い
        invalid_df = pd.DataFrame({
            'y': range(10)
        })
        assert pipeline.validate_input(invalid_df) == False
        
        # 空のDataFrame
        empty_df = pd.DataFrame()
        assert pipeline.validate_input(empty_df) == False

class TestCalendarFeaturesPipeline:
    """CalendarFeaturesPipelineのテスト"""
    
    def test_initialization(self):
        """パイプライン初期化テスト"""
        pipeline = CalendarFeaturesPipeline()
        assert pipeline is not None
        assert pipeline.get_feature_type() == 'futr'
    
    def test_generate_features(self, sample_timeseries):
        """特徴量生成テスト"""
        pipeline = CalendarFeaturesPipeline()
        features = pipeline.generate(sample_timeseries)
        
        # 特徴量が生成されているか
        assert len(features) > 0
        assert 'ds' in features.columns
        
        # カレンダー特徴量が生成されているか
        assert 'futr_ds_year' in features.columns
        assert 'futr_ds_month' in features.columns
        assert 'futr_ds_day_of_week' in features.columns
        
        # 周期性エンコーディングが生成されているか
        assert 'futr_ds_day_sin' in features.columns
        assert 'futr_ds_day_cos' in features.columns
        
        # 休日特徴量が生成されているか
        assert 'futr_is_holiday' in features.columns

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
