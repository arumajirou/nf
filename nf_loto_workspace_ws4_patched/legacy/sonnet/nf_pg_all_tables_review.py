
import os, pandas as pd
from sqlalchemy import create_engine, text

SCHEMA = os.getenv("TARGET_SCHEMA", "public")
LIKE_PATTERN = os.getenv("LIKE_PATTERN", "nf_%")
HEAD_N = int(os.getenv("HEAD_N", "10"))
MAX_ROWS = os.getenv("MAX_ROWS")
MAX_ROWS = int(MAX_ROWS) if (MAX_ROWS and MAX_ROWS.isdigit()) else None

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    host = os.getenv("PGHOST", "127.0.0.1")
    port = os.getenv("PGPORT", "5432")
    db   = os.getenv("PGDATABASE", "postgres")
    user = os.getenv("PGUSER", "postgres")
    pw   = os.getenv("PGPASSWORD", "")
    DATABASE_URL = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def q(sql: str, params=None) -> pd.DataFrame:
    with engine.begin() as cx:
        return pd.read_sql(text(sql), cx, params=params or {})

like_df = q("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = :schema AND table_name LIKE :pat
ORDER BY table_name
""", {"schema": SCHEMA, "pat": LIKE_PATTERN})

prio = [
    "nf_model_profile","nf_dataset_profile","nf_training_state","nf_weight_statistics",
    "nf_model_complexity","nf_model_diagnosis","nf_parameter_sensitivity","nf_optimization_suggestions",
    "nf_runs","nf_models","nf_model","nf_hparams","nf_ckpt","nf_config","nf_pkl",
]
prio_df = q("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = :schema AND table_name = ANY(:names)
ORDER BY table_name
""", {"schema": SCHEMA, "names": prio})

all_names = sorted(set(like_df["table_name"]).union(set(prio_df["table_name"])))
print("tables:", all_names)

cols_df = q("""
SELECT table_name, ordinal_position, column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_schema = :schema AND table_name = ANY(:names)
ORDER BY table_name, ordinal_position
""", {"schema": SCHEMA, "names": all_names})

def load_table(schema: str, name: str, max_rows=None) -> pd.DataFrame:
    lim = f" LIMIT {int(max_rows)}" if max_rows else ""
    return q(f'SELECT * FROM "{schema}"."{name}"{lim}')

for t in all_names:
    df = load_table(SCHEMA, t, MAX_ROWS)
    print(f"\n=== {t} ===")
    print("[schema]")
    print(cols_df[cols_df['table_name']==t].to_string(index=False))
    print(f"[rows] {len(df)}")
    if len(df) > 0:
        print(df.head(HEAD_N).astype(str).applymap(lambda s: s[:200]).to_string(index=False))
