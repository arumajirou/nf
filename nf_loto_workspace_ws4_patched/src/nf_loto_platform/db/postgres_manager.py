"""
PostgreSQLデータベースマネージャー
NeuralForecastパラメータをPostgreSQLに保存するためのユーティリティ
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
import json
import re
from typing import Any, Dict, List, Tuple, Optional
from pathlib import Path
import pandas as pd
from .db_config import DB_CONFIG, TABLE_PREFIX, MAX_COLUMN_NAME_LENGTH, PYTHON_TO_PG_TYPE


class PostgreSQLManager:
    """PostgreSQLデータベース操作マネージャー"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初期化
        
        Args:
            config: データベース接続設定（Noneの場合はdb_configから取得）
        """
        self.config = config or DB_CONFIG
        self.conn = None
        self.cursor = None
        
    def connect(self) -> bool:
        """データベースに接続"""
        try:
            self.conn = psycopg2.connect(**self.config)
            self.cursor = self.conn.cursor()
            print(f"✓ PostgreSQL接続成功: {self.config['host']}:{self.config['port']}/{self.config['database']}")
            return True
        except Exception as e:
            print(f"✗ PostgreSQL接続失敗: {e}")
            return False
    
    def disconnect(self):
        """データベース接続を閉じる"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("✓ PostgreSQL接続を閉じました")
    
    def __enter__(self):
        """コンテキストマネージャー: with文で使用"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャー: with文終了時"""
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.disconnect()
    
    def commit(self):
        """トランザクションをコミット"""
        if self.conn:
            self.conn.commit()
    
    def rollback(self):
        """トランザクションをロールバック"""
        if self.conn:
            self.conn.rollback()
            print("✗ トランザクションをロールバックしました")
    
    @staticmethod
    def sanitize_table_name(category: str) -> str:
        """
        カテゴリ名をテーブル名に変換
        
        Args:
            category: カテゴリ名（例: "A_model", "B_class_default"）
            
        Returns:
            サニタイズされたテーブル名
        """
        # プレフィックス（A_, B_等）を削除
        name = re.sub(r'^[A-Z]_', '', category)
        # 小文字に変換
        name = name.lower()
        # 特殊文字をアンダースコアに置換
        name = re.sub(r'[^a-z0-9_]', '_', name)
        # 連続するアンダースコアを1つに
        name = re.sub(r'_+', '_', name)
        # 前後のアンダースコアを削除
        name = name.strip('_')
        # テーブル名プレフィックスを追加
        return f"{TABLE_PREFIX}{name}"
    
    @staticmethod
    def sanitize_column_name(parameter: str) -> str:
        """
        パラメータ名をカラム名に変換
        
        Args:
            parameter: パラメータ名（例: "model.batch_size"）
            
        Returns:
            サニタイズされたカラム名
        """
        # プレフィックス（model., hparams.等）を削除
        name = re.sub(r'^[^.]+\.', '', parameter)
        # 小文字に変換
        name = name.lower()
        # 特殊文字をアンダースコアに置換
        name = re.sub(r'[^a-z0-9_]', '_', name)
        # 連続するアンダースコアを1つに
        name = re.sub(r'_+', '_', name)
        # 前後のアンダースコアを削除
        name = name.strip('_')
        # 予約語の場合は接頭辞を追加
        if name in ['user', 'select', 'from', 'where', 'order', 'group']:
            name = f"param_{name}"
        # 最大長を超える場合は切り詰め
        if len(name) > MAX_COLUMN_NAME_LENGTH:
            name = name[:MAX_COLUMN_NAME_LENGTH]
        return name
    
    @staticmethod
    def infer_pg_type(value: Any) -> str:
        """
        Python値からPostgreSQLデータ型を推測
        
        Args:
            value: Python値
            
        Returns:
            PostgreSQLデータ型
        """
        value_type = type(value)
        
        # リストや辞書の場合
        if isinstance(value, (list, dict)):
            return 'JSONB'
        
        # その他の型
        return PYTHON_TO_PG_TYPE.get(value_type, 'TEXT')
    
    @staticmethod
    def convert_value_for_pg(value: Any) -> Any:
        """
        Python値をPostgreSQL互換の値に変換
        
        Args:
            value: Python値
            
        Returns:
            PostgreSQL互換の値
        """
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False)
        elif value is None:
            return None
        elif isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value
        else:
            return str(value)
    
    def create_table_from_category(self, category: str, df_category: pd.DataFrame) -> str:
        """
        カテゴリに基づいてテーブルを作成
        
        Args:
            category: カテゴリ名
            df_category: カテゴリのDataFrame（Parameter, Value, Sourceカラムを持つ）
            
        Returns:
            作成されたテーブル名
        """
        table_name = self.sanitize_table_name(category)
        
        # 既存のテーブルを削除
        drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(
            sql.Identifier(table_name)
        )
        self.cursor.execute(drop_query)
        
        # カラム定義を作成
        columns = []
        columns.append("id SERIAL PRIMARY KEY")
        
        # パラメータごとにカラムを追加
        for _, row in df_category.iterrows():
            param = row['Parameter']
            value = row['Value']
            
            col_name = self.sanitize_column_name(param)
            col_type = self.infer_pg_type(value)
            
            columns.append(f"{col_name} {col_type}")
        
        # Sourceを保存するためのJSONBカラムを追加
        columns.append("sources JSONB")
        columns.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # テーブル作成SQL
        create_query = f"""
        CREATE TABLE {table_name} (
            {', '.join(columns)}
        )
        """
        
        try:
            self.cursor.execute(create_query)
            print(f"  ✓ テーブル作成: {table_name} ({len(df_category)} columns)")
            return table_name
        except Exception as e:
            print(f"  ✗ テーブル作成失敗 {table_name}: {e}")
            raise
    
    def insert_data_to_table(self, table_name: str, df_category: pd.DataFrame):
        """
        テーブルにデータを挿入
        
        Args:
            table_name: テーブル名
            df_category: カテゴリのDataFrame
        """
        # データ行を準備
        row_data = {}
        sources_data = {}
        
        for _, row in df_category.iterrows():
            param = row['Parameter']
            value = row['Value']
            source = row['Source']
            
            col_name = self.sanitize_column_name(param)
            row_data[col_name] = self.convert_value_for_pg(value)
            sources_data[col_name] = source
        
        # カラム名と値を準備
        columns = list(row_data.keys()) + ['sources']
        values = list(row_data.values()) + [json.dumps(sources_data, ensure_ascii=False)]
        
        # INSERT文を作成
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        
        try:
            self.cursor.execute(insert_query, values)
            print(f"  ✓ データ挿入: {table_name} (1 row)")
        except Exception as e:
            print(f"  ✗ データ挿入失敗 {table_name}: {e}")
            raise
    
    def save_dataframe_to_postgres(self, df_long: pd.DataFrame) -> Dict[str, str]:
        """
        DataFrameをPostgreSQLに保存
        
        Args:
            df_long: 縦持ちDataFrame（Category, Parameter, Value, Sourceカラムを持つ）
            
        Returns:
            作成されたテーブル名の辞書（category -> table_name）
        """
        print("\n" + "="*80)
        print("PostgreSQLへのデータ保存を開始")
        print("="*80)
        
        table_mapping = {}
        categories = df_long['Category'].unique()
        
        for i, category in enumerate(categories, 1):
            print(f"\n[{i}/{len(categories)}] カテゴリ: {category}")
            
            # カテゴリでフィルタ
            df_category = df_long[df_long['Category'] == category].copy()
            
            try:
                # テーブル作成
                table_name = self.create_table_from_category(category, df_category)
                
                # データ挿入
                self.insert_data_to_table(table_name, df_category)
                
                table_mapping[category] = table_name
                
            except Exception as e:
                print(f"  ✗ エラー: {e}")
                continue
        
        print("\n" + "="*80)
        print(f"✓ PostgreSQL保存完了: {len(table_mapping)}/{len(categories)} テーブル")
        print("="*80)
        
        return table_mapping
    
    def get_table_info(self, table_name: str) -> pd.DataFrame:
        """
        テーブル情報を取得
        
        Args:
            table_name: テーブル名
            
        Returns:
            テーブル情報のDataFrame
        """
        query = """
        SELECT 
            column_name,
            data_type,
            character_maximum_length,
            is_nullable
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position
        """
        
        self.cursor.execute(query, (table_name,))
        results = self.cursor.fetchall()
        
        return pd.DataFrame(
            results,
            columns=['column_name', 'data_type', 'max_length', 'nullable']
        )
    
    def list_tables(self, schema: str = 'public') -> List[str]:
        """
        スキーマ内のテーブル一覧を取得
        
        Args:
            schema: スキーマ名
            
        Returns:
            テーブル名のリスト
        """
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
        
        self.cursor.execute(query, (schema,))
        results = self.cursor.fetchall()
        
        return [row[0] for row in results]

def get_connection():
    """Jupyter や簡易スクリプト向けの接続ヘルパー関数。

    DB_CONFIG をそのまま psycopg2.connect に渡して
    PostgreSQL の接続オブジェクトを返します。

    Returns
    -------
    psycopg2.extensions.connection
        PostgreSQL への接続オブジェクト

    Raises
    ------
    RuntimeError
        接続に失敗した場合
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"PostgreSQL への接続に失敗しました: {e}") from e

