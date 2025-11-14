#!/usr/bin/env python3
"""
データベース初期化スクリプト

スキーマを作成し、初期データを投入します。
"""

import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from database.connection import init_database
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """メイン処理"""
    logger.info("=" * 60)
    logger.info("Database Initialization")
    logger.info("=" * 60)
    
    try:
        # データベース初期化
        db = init_database(
            config_path=str(project_root / 'config' / 'database.yaml'),
            create_tables=True
        )
        
        logger.info("✓ Database initialized successfully")
        
        # テーブル情報の表示
        logger.info("\nCreated tables:")
        tables = ['experiments', 'datasets', 'training_runs', 'resource_metrics']
        for table in tables:
            try:
                info = db.get_table_info(table)
                logger.info(f"  - {table}: {info['row_count']} rows")
            except Exception as e:
                logger.warning(f"  - {table}: Could not get info ({e})")
        
        logger.info("\n" + "=" * 60)
        logger.info("Database initialization completed!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
