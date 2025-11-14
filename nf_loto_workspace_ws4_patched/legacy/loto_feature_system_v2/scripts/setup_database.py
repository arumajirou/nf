#!/usr/bin/env python
"""
データベースセットアップスクリプト
テーブルを作成し、基本的な検証を行います
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import yaml
import logging
from core.database_manager import DatabaseManager

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """メイン処理"""
    # 設定読み込み
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'db_config.yaml')
    
    if not os.path.exists(config_path):
        logger.error(f"設定ファイルが見つかりません: {config_path}")
        logger.info("config/db_config.yaml.template をコピーして config/db_config.yaml を作成してください")
        return 1
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    logger.info("データベース設定読み込み完了")
    logger.info(f"  ホスト: {config['host']}")
    logger.info(f"  ポート: {config['port']}")
    logger.info(f"  データベース: {config['database']}")
    logger.info(f"  ユーザー: {config['user']}")
    
    # データベースマネージャー初期化
    try:
        db_manager = DatabaseManager(config)
        logger.info("データベース接続成功")
    except Exception as e:
        logger.error(f"データベース接続失敗: {e}")
        return 1
    
    # テーブル作成
    try:
        logger.info("\n=== テーブル作成 ===")
        db_manager.create_tables()
        logger.info("テーブル作成完了")
    except Exception as e:
        logger.error(f"テーブル作成失敗: {e}")
        return 1
    
    # 確認
    logger.info("\n=== テーブル情報確認 ===")
    for table in ['features_hist', 'features_futr', 'features_stat']:
        try:
            info = db_manager.get_table_info(table)
            logger.info(f"\n{table}:")
            logger.info(f"  行数: {info['row_count']}")
            logger.info(f"  列数: {info['n_columns']}")
            logger.info(f"  列: {', '.join(list(info['columns'].keys())[:10])}...")
        except Exception as e:
            logger.error(f"{table} 情報取得失敗: {e}")
    
    logger.info("\n=== セットアップ完了 ===")
    return 0

if __name__ == "__main__":
    sys.exit(main())
