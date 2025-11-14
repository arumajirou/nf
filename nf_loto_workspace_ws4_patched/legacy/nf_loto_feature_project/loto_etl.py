
import re
from urllib.parse import urlparse
import pandas as pd

# ---- input URLs ----
URLS = [
    "https://loto-life.net/csv/mini",
    "https://loto-life.net/csv/loto6",
    "https://loto-life.net/csv/loto7",
    "https://loto-life.net/csv/bingo5",
    "https://loto-life.net/csv/numbers3",
    "https://loto-life.net/csv/numbers4",
]

# short names for numbers3/4
NAME_MAP = {"numbers3": "num3", "numbers4": "num4"}


def _loto_name_from_url(u: str) -> str:
    tail = urlparse(u).path.strip("/").split("/")[-1]
    return NAME_MAP.get(tail, tail)


def _read_csv_jp(u: str) -> pd.DataFrame:
    for enc in ("cp932", "sjis", "utf-8"):
        try:
            return pd.read_csv(u, encoding=enc)
        except Exception:
            continue
    return pd.read_csv(u)


def _find_date_col(cols) -> str | None:
    for c in cols:
        if re.search(r"(開催日|抽選日)", str(c)):
            return c
    return None


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _rename_core_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    - rename date column to ds and parse
    - 第*数字 -> N*
    - *等口数 -> N*NU
    - *等賞金 -> N*PM
    - numbers3/4 prize columns -> snu/spm/... etc
    """
    df = _normalize_columns(df)

    # date -> ds
    date_col = _find_date_col(df.columns)
    if date_col and date_col != "ds":
        df = df.rename(columns={date_col: "ds"})
    if "ds" in df.columns:
        ds_clean = (
            df["ds"].astype(str)
            .str.replace(r"\(.*?\)", "", regex=True)
            .str.replace("年", "-")
            .str.replace("月", "-")
            .str.replace("日", "")
            .str.replace("/", "-")
        )
        df["ds"] = pd.to_datetime(ds_clean, errors="coerce")

    ren: dict[str, str] = {}

    # main lotto patterns
    for c in df.columns:
        m = re.fullmatch(r"第(\d+)数字", c)
        if m:
            ren[c] = f"N{int(m.group(1))}"
            continue

        m = re.fullmatch(r"(\d+)等口数", c)
        if m:
            ren[c] = f"N{int(m.group(1))}NU"
            continue

        m = re.fullmatch(r"(\d+)等賞金", c)
        if m:
            ren[c] = f"N{int(m.group(1))}PM"
            continue

    # numbers3/4 prize columns -> short names
    prize_ren = {
        "ストレート口数": "snu",
        "ストレート賞金": "spm",
        "ボックス口数": "bnu",
        "ボックス賞金": "bpm",
        "セット(ストレート)口数": "ssnu",
        "セット(ストレート)賞金": "sspm",
        "セット(ボックス)口数": "sbnu",
        "セット(ボックス)賞金": "sbpm",
        "ミニ口数": "mininu",
        "ミニ賞金": "minipm",
    }
    for jp, short in prize_ren.items():
        if jp in df.columns:
            ren[jp] = short

    if ren:
        df = df.rename(columns=ren)
    return df


def _expand_num_draw_columns(df: pd.DataFrame, loto_name: str) -> pd.DataFrame:
    """Expand the "抽選数字" column of numbers3/4 into digit columns N1..N3/N4."""
    df = df.copy()
    if "抽選数字" not in df.columns:
        return df

    s = df["抽選数字"].astype(str)
    digits = s.str.extract(r"(\d+)", expand=False)

    if loto_name == "num3":
        expected = 3
    elif loto_name == "num4":
        expected = 4
    else:
        if digits.notna().any():
            expected = int(digits.str.len().max())
        else:
            return df

    digits_padded = digits.fillna("").str.zfill(expected)

    for i in range(expected):
        col = digits_padded.str[i]
        df[f"N{i+1}"] = pd.to_numeric(col, errors="coerce")

    return df


def _melt_numbers_long(df: pd.DataFrame, loto_name: str) -> pd.DataFrame:
    """Keep only N* columns as 'y' in long format."""
    df = df.copy()
    df["loto"] = loto_name

    n_cols = [c for c in df.columns if re.fullmatch(r"N\d+", str(c))]
    n_cols = sorted(n_cols, key=lambda x: int(re.search(r"\d+", x).group()))
    if not n_cols:
        return pd.DataFrame(columns=["loto", "ds", "unique_id", "y"])

    id_vars = [c for c in df.columns if c not in n_cols]
    long_df = df.melt(
        id_vars=id_vars,
        value_vars=n_cols,
        var_name="unique_id",
        value_name="y",
    )
    long_df["y"] = pd.to_numeric(long_df["y"], errors="coerce")
    return long_df


def build_long_dataframe(urls: list[str]) -> pd.DataFrame:
    out_frames: list[pd.DataFrame] = []

    for u in urls:
        loto = _loto_name_from_url(u)
        raw = _read_csv_jp(u)
        norm = _rename_core_columns(raw)

        if loto in ("num3", "num4"):
            norm = _expand_num_draw_columns(norm, loto)

        long = _melt_numbers_long(norm, loto)
        out_frames.append(long)

    out_frames = [f for f in out_frames if f is not None and not f.empty]
    if not out_frames:
        return pd.DataFrame(columns=["loto", "num", "ds", "unique_id", "y", "CO"])

    result = pd.concat(out_frames, ignore_index=True)

    preferred = ["loto", "開催回", "ds", "unique_id", "y"]
    other = [c for c in result.columns if c not in preferred]
    cols = [c for c in preferred if c in result.columns] + other
    result = result[cols]
    return result


def _to_int64(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0).astype("int64")


def _to_float64(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("float64")


def finalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Finalize dataframe:
      - num, CO as int64
      - y and all other numeric columns (including N*) as float64
      - drop bonus/unused columns
    """
    df = df.copy()

    if "開催回" in df.columns:
        df["num"] = _to_int64(df["開催回"])
    if "キャリーオーバー" in df.columns:
        df["CO"] = _to_int64(df["キャリーオーバー"])
    if "y" in df.columns:
        df["y"] = _to_float64(df["y"])

    exclude = {"loto", "ds", "unique_id", "開催回", "キャリーオーバー", "num", "CO", "y"}
    for c in df.columns:
        if c in exclude:
            continue
        df[c] = _to_float64(df[c])

    drop_cols = [
        c
        for c in [
            "ボーナス数字",
            "ボーナス数字1",
            "ボーナス数字2",
            "キャリーオーバー",
            "開催回",
        ]
        if c in df.columns
    ]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    preferred = ["loto", "num", "ds", "unique_id", "y", "CO"]
    others = [c for c in df.columns if c not in preferred]
    df = df[[c for c in preferred if c in df.columns] + others]

    return df


def build_df_final(urls: list[str] | None = None) -> pd.DataFrame:
    urls_ = urls or URLS
    df_long = build_long_dataframe(urls_)
    df_final = finalize_df(df_long)
    return df_final


if __name__ == "__main__":
    df_final = build_df_final()
    print(df_final.info())
    print(df_final.head())
