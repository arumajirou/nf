"""
Pytest設定とフィクスチャ
"""
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture
def sample_config():
    """テスト用データベース設定"""
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

@pytest.fixture
def pipeline_config():
    """テスト用パイプライン設定"""
    return {
        'lag_windows': [1, 7, 14],
        'rolling_windows': [7, 14, 30],
        'rolling_stats': ['mean', 'std', 'min', 'max']
    }
