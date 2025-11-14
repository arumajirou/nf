from typing import List
import numpy as np
import pandas as pd

def clean_nan_inf(df: pd.DataFrame, key_cols: List[str]) -> pd.DataFrame:
    """NaN / inf をポリシーに従って削除する。

    1. inf/-inf -> NaN
    2. 各特徴列ごとに NaN 割合 r を計算
    3. r <= 0.3: その列の NaN を含む行を削除
    4. r > 0.3: 列ごと削除
    5. 最後に NaN が残っていたら列ごと削除
    """
    if df.empty:
        return df

    df = df.copy()
    # inf を NaN に
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    feature_cols = [c for c in df.columns if c not in key_cols]

    # 列ごとの NaN 割合を算出
    nan_ratio = df[feature_cols].isna().mean()

    cols_drop_all = []  # 最終的に drop する列

    for col in feature_cols:
        r = nan_ratio[col]
        if r == 0:
            continue
        if r <= 0.3:
            # NaN を含む行を削除
            df = df[df[col].notna() | df[col].isna() == False]
        else:
            # 列ごと削除
            cols_drop_all.append(col)

    if cols_drop_all:
        df = df.drop(columns=cols_drop_all)

    # まだ NaN があれば対応列を削る
    remaining_nan_cols = df.columns[df.isna().any()].tolist()
    remaining_nan_cols = [c for c in remaining_nan_cols if c not in key_cols]
    if remaining_nan_cols:
        df = df.drop(columns=remaining_nan_cols)

    return df
