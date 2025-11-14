"""
データベース接続管理モジュール

PostgreSQLへの接続とセッション管理を提供します。
"""

import os
from contextlib import contextmanager
from typing import Generator, Optional
import logging

from sqlalchemy import create_engine, event, pool
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool, QueuePool
import yaml

logger = logging.getLogger(__name__)

# SQLAlchemyベースクラス
Base = declarative_base()


class DatabaseConfig:
    """データベース設定管理クラス"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Args:
            config_path: 設定ファイルのパス（Noneの場合は環境変数を使用）
        """
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                db_config = config.get('database', {})
        else:
            # 環境変数から設定を取得
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': int(os.getenv('DB_PORT', 5432)),
                'database': os.getenv('DB_DATABASE', 'postgres'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'z'),
            }
        
        self.host = db_config['host']
        self.port = db_config['port']
        self.database = db_config['database']
        self.user = db_config['user']
        self.password = db_config['password']
        
        # 接続プール設定
        self.pool_size = int(os.getenv('DB_POOL_SIZE', 10))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', 20))
        self.pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', 30))
        self.pool_recycle = int(os.getenv('DB_POOL_RECYCLE', 3600))
        
        # 接続オプション
        self.echo = os.getenv('DB_ECHO', 'false').lower() == 'true'
        self.connect_timeout = int(os.getenv('DB_CONNECT_TIMEOUT', 10))
    
    def get_url(self) -> str:
        """データベースURLを取得"""
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )
    
    def get_async_url(self) -> str:
        """非同期データベースURLを取得"""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )


class DatabaseConnection:
    """データベース接続マネージャー"""
    
    def __init__(self, config: Optional[DatabaseConfig] = None):
        """
        Args:
            config: データベース設定（Noneの場合はデフォルト設定を使用）
        """
        self.config = config or DatabaseConfig()
        self._engine = None
        self._session_factory = None
        self._scoped_session = None
    
    @property
    def engine(self):
        """SQLAlchemyエンジンを取得（遅延初期化）"""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine
    
    @property
    def session_factory(self):
        """セッションファクトリーを取得"""
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )
        return self._session_factory
    
    @property
    def scoped_session(self):
        """スコープ付きセッションを取得（スレッドセーフ）"""
        if self._scoped_session is None:
            self._scoped_session = scoped_session(self.session_factory)
        return self._scoped_session
    
    def _create_engine(self):
        """SQLAlchemyエンジンを作成"""
        url = self.config.get_url()
        
        engine = create_engine(
            url,
            poolclass=QueuePool,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow,
            pool_timeout=self.config.pool_timeout,
            pool_recycle=self.config.pool_recycle,
            pool_pre_ping=True,  # 接続の健全性チェック
            echo=self.config.echo,
            connect_args={
                'connect_timeout': self.config.connect_timeout,
            }
        )
        
        # イベントリスナーの設定
        @event.listens_for(engine, "connect")
        def receive_connect(dbapi_conn, connection_record):
            """接続時のイベント"""
            logger.debug(f"Database connection established: {dbapi_conn}")
        
        @event.listens_for(engine, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            """接続プールからチェックアウト時のイベント"""
            logger.debug("Connection checked out from pool")
        
        logger.info(f"Database engine created: {url.split('@')[1]}")  # パスワードを隠す
        return engine
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        コンテキストマネージャーでセッションを提供
        
        Usage:
            with db.get_session() as session:
                result = session.query(Model).all()
        """
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error: {e}")
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """すべてのテーブルを作成"""
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created successfully")
    
    def drop_tables(self):
        """すべてのテーブルを削除（注意！）"""
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=self.engine)
        logger.warning("All database tables dropped")
    
    def test_connection(self) -> bool:
        """接続テスト"""
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
            logger.info("Database connection test: SUCCESS")
            return True
        except Exception as e:
            logger.error(f"Database connection test: FAILED - {e}")
            return False
    
    def get_table_info(self, table_name: str) -> dict:
        """テーブル情報を取得"""
        with self.get_session() as session:
            # 行数を取得
            count_query = f"SELECT COUNT(*) FROM {table_name}"
            row_count = session.execute(count_query).scalar()
            
            # カラム情報を取得
            columns_query = f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """
            columns = session.execute(columns_query).fetchall()
            
            return {
                'table_name': table_name,
                'row_count': row_count,
                'columns': [
                    {
                        'name': col[0],
                        'type': col[1],
                        'nullable': col[2] == 'YES'
                    }
                    for col in columns
                ]
            }
    
    def vacuum_analyze(self):
        """VACUUMとANALYZEを実行（パフォーマンス最適化）"""
        logger.info("Running VACUUM ANALYZE...")
        with self.engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute("VACUUM ANALYZE")
        logger.info("VACUUM ANALYZE completed")
    
    def close(self):
        """接続をクローズ"""
        if self._scoped_session:
            self._scoped_session.remove()
        if self._engine:
            self._engine.dispose()
            logger.info("Database connections closed")


# グローバルインスタンス（シングルトンパターン）
_db_connection: Optional[DatabaseConnection] = None


def get_db_connection(config: Optional[DatabaseConfig] = None) -> DatabaseConnection:
    """
    グローバルデータベース接続を取得
    
    Args:
        config: データベース設定
        
    Returns:
        DatabaseConnection: データベース接続インスタンス
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection(config)
    return _db_connection


def init_database(config_path: Optional[str] = None, create_tables: bool = True):
    """
    データベースを初期化
    
    Args:
        config_path: 設定ファイルのパス
        create_tables: テーブルを作成するかどうか
    """
    config = DatabaseConfig(config_path)
    db = get_db_connection(config)
    
    # 接続テスト
    if not db.test_connection():
        raise ConnectionError("Failed to connect to database")
    
    # テーブル作成
    if create_tables:
        db.create_tables()
    
    logger.info("Database initialized successfully")
    return db


# コンビニエンス関数
@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    便利なセッションコンテキストマネージャー
    
    Usage:
        from database.connection import session_scope
        
        with session_scope() as session:
            result = session.query(Model).all()
    """
    db = get_db_connection()
    with db.get_session() as session:
        yield session


def get_session() -> Session:
    """
    新しいセッションを取得（手動でクローズが必要）
    
    Returns:
        Session: SQLAlchemyセッション
    """
    db = get_db_connection()
    return db.session_factory()
