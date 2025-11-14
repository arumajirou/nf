"""
PostgreSQL接続設定
"""

# データベース接続設定
DB_CONFIG = {
    'host': '127.0.0.1',  # localhostの場合
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'z',  # 実際のパスワードに変更してください
}

# テーブル名のプレフィックス
TABLE_PREFIX = 'nf_'

# カラム名の最大長
MAX_COLUMN_NAME_LENGTH = 63

# PostgreSQLデータ型マッピング
PYTHON_TO_PG_TYPE = {
    int: 'INTEGER',
    float: 'REAL',
    str: 'TEXT',
    bool: 'BOOLEAN',
    list: 'JSONB',
    dict: 'JSONB',
    type(None): 'TEXT',
}
