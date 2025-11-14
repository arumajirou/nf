import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

def build_y_features(base_df: pd.DataFrame) -> pd.DataFrame:
    """y に対する異常スコアなどを生成する。

    出力: loto, unique_id, ds, hist_* 系の特徴
    """
    df = base_df[["loto", "unique_id", "ds", "y"]].copy()
    # 単純な異常スコア: IsolationForest と LOF を y のみで計算
    # 系列ごとに fit すると重くなるため、ここでは全体で fit する簡易版
    values = df["y"].values.reshape(-1, 1)

    try:
        iso = IsolationForest(random_state=0, n_estimators=100, contamination="auto")
        iso_scores = iso.fit_predict(values)
        df["hist_anom_iforest"] = iso_scores
    except Exception:
        df["hist_anom_iforest"] = np.nan

    try:
        lof = LocalOutlierFactor(n_neighbors=20, contamination="auto")
        lof_scores = lof.fit_predict(values)
        df["hist_anom_lof"] = lof_scores
    except Exception:
        df["hist_anom_lof"] = np.nan

    return df
