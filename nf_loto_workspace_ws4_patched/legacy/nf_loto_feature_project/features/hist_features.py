from typing import List
import pandas as pd

from .feature_config import DEFAULT_CONFIG

def _add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    cfg = DEFAULT_CONFIG.lag
    df = df.sort_values(["loto", "unique_id", "ds"]).copy()
    for lag in cfg.lags:
        df[f"hist_y_lag_{lag}"] = df.groupby(["loto", "unique_id"])["y"].shift(lag)
    for w in cfg.rolling_windows:
        grp = df.groupby(["loto", "unique_id"])["y"]
        df[f"hist_y_roll_mean_{w}"] = grp.rolling(w).mean().reset_index(level=[0,1], drop=True)
        df[f"hist_y_roll_std_{w}"] = grp.rolling(w).std().reset_index(level=[0,1], drop=True)
    return df

def build_hist_features(base_df: pd.DataFrame) -> pd.DataFrame:
    """履歴外生 (hist_) を生成する。

    とりあえずラグ・ローリング統計に絞った軽量版実装。
    拡張として tsfresh / TSFEL / catch22 などを追加できる。
    """
    df = base_df[["loto", "unique_id", "ds", "y"]].copy()
    df = _add_lag_features(df)
    return df
