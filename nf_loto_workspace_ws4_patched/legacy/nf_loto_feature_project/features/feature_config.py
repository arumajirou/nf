from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class LagConfig:
    lags: List[int]
    rolling_windows: List[int]

@dataclass
class FutrCalendarConfig:
    add_month: bool
    add_dow: bool
    add_weekofyear: bool
    add_holiday_flags: bool
    add_cyclical: bool

@dataclass
class TSFreshConfig:
    enable: bool
    default_fc_parameters: Dict[str, Any]

@dataclass
class TSFELConfig:
    enable: bool
    domains: List[str]

@dataclass
class YAnomalyConfig:
    enable_isolation_forest: bool
    enable_lof: bool

@dataclass
class TS2VecConfig:
    enable: bool
    embedding_dim: int
    window_size: int

@dataclass
class FeatureConfig:
    lag: LagConfig
    futr_calendar: FutrCalendarConfig
    tsfresh: TSFreshConfig
    tsfel: TSFELConfig
    y_anomaly: YAnomalyConfig
    ts2vec: TS2VecConfig

DEFAULT_CONFIG = FeatureConfig(
    lag=LagConfig(
        lags=[1, 2, 7, 14, 28, 52],
        rolling_windows=[7, 14, 28, 52],
    ),
    futr_calendar=FutrCalendarConfig(
        add_month=True,
        add_dow=True,
        add_weekofyear=True,
        add_holiday_flags=True,
        add_cyclical=True,
    ),
    tsfresh=TSFreshConfig(
        enable=True,
        default_fc_parameters={
            "mean": None,
            "variance": None,
            "skewness": None,
            "kurtosis": None,
        },
    ),
    tsfel=TSFELConfig(
        enable=False,
        domains=["statistical", "temporal", "spectral"],
    ),
    y_anomaly=YAnomalyConfig(
        enable_isolation_forest=True,
        enable_lof=True,
    ),
    ts2vec=TS2VecConfig(
        enable=True,
        embedding_dim=32,
        window_size=64,
    ),
)
