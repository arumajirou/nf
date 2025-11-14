from typing import Dict, Any, Optional, List
import json
import psycopg2
from psycopg2.extras import Json

from db_config import DB_CONFIG

def _get_conn():
    return psycopg2.connect(**DB_CONFIG)

def init_registry_table() -> None:
    sql = '''
    CREATE TABLE IF NOT EXISTS nf_feature_registry (
        feature_name   TEXT PRIMARY KEY,
        group_name     TEXT NOT NULL,
        source_library TEXT NOT NULL,
        params         JSONB,
        is_active      BOOLEAN DEFAULT TRUE,
        created_at     TIMESTAMP DEFAULT now()
    );
    '''
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

def register_feature(feature_name: str, group_name: str,
                     source_library: str, params: Dict[str, Any]) -> None:
    init_registry_table()
    sql = '''
    INSERT INTO nf_feature_registry (feature_name, group_name, source_library, params)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (feature_name)
    DO UPDATE SET
      group_name = EXCLUDED.group_name,
      source_library = EXCLUDED.source_library,
      params = EXCLUDED.params,
      is_active = TRUE;
    '''
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (feature_name, group_name, source_library, Json(params)))
        conn.commit()

def list_active_features(group_name: Optional[str] = None) -> List[str]:
    init_registry_table()
    sql = 'SELECT feature_name FROM nf_feature_registry WHERE is_active = TRUE'
    params = ()
    if group_name is not None:
        sql += ' AND group_name = %s'
        params = (group_name,)
    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
    return [r[0] for r in rows]
