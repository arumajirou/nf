"""
PostgreSQLセットアップスクリプト
データベース、スキーマ、権限を初期化
"""

import sys
from .postgres_manager import PostgreSQLManager
from .db_config import DB_CONFIG


def setup_database():
    """データベースをセットアップ"""
    print("\n" + "="*80)
    print("PostgreSQL セットアップ")
    print("="*80)
    
    # 接続情報を表示
    print(f"\n接続情報:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}")
    
    # 接続テスト
    print("\n[1/3] データベース接続テスト...")
    try:
        with PostgreSQLManager() as db:
            print("✓ 接続成功")
            
            # テーブル一覧を取得
            print("\n[2/3] 既存のテーブルを確認...")
            tables = db.list_tables()
            
            if tables:
                print(f"  既存のテーブル: {len(tables)} 個")
                for table in tables:
                    if table.startswith('nf_'):
                        print(f"    - {table}")
            else:
                print("  既存のテーブル: なし")
            
            # 古いテーブルを削除するか確認
            if tables and any(t.startswith('nf_') for t in tables):
                print("\n⚠ 既存のnf_*テーブルが見つかりました")
                response = input("  これらのテーブルを削除しますか? (y/N): ").strip().lower()
                
                if response == 'y':
                    print("\n[3/3] 既存のテーブルを削除中...")
                    for table in tables:
                        if table.startswith('nf_'):
                            try:
                                db.cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                                print(f"  ✓ 削除: {table}")
                            except Exception as e:
                                print(f"  ✗ 削除失敗 {table}: {e}")
                    db.commit()
                    print("  ✓ 削除完了")
                else:
                    print("  → 削除をスキップしました")
            else:
                print("\n[3/3] 新規セットアップ準備完了")
            
            print("\n" + "="*80)
            print("✓ セットアップ完了")
            print("="*80)
            print("\n次のステップ:")
            print("1. db_config.py を確認・編集")
            print("2. neuralforecast_extractor_postgres.py を実行")
            print("="*80 + "\n")
            
            return True
            
    except Exception as e:
        print(f"\n✗ セットアップ失敗: {e}")
        print("\nトラブルシューティング:")
        print("1. PostgreSQLサービスが起動しているか確認")
        print("2. db_config.py の接続情報が正しいか確認")
        print("3. ユーザーに適切な権限があるか確認")
        return False


def test_connection_only():
    """接続テストのみ実行"""
    print("\n" + "="*80)
    print("PostgreSQL 接続テスト")
    print("="*80)
    
    print(f"\n接続情報:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}")
    
    try:
        with PostgreSQLManager() as db:
            print("\n✓ 接続成功\n")
            
            # バージョン情報を取得
            db.cursor.execute("SELECT version()")
            version = db.cursor.fetchone()[0]
            print(f"PostgreSQL バージョン:")
            print(f"  {version}\n")
            
            return True
            
    except Exception as e:
        print(f"\n✗ 接続失敗: {e}\n")
        return False


def show_table_info():
    """テーブル情報を表示"""
    print("\n" + "="*80)
    print("PostgreSQL テーブル情報")
    print("="*80)
    
    try:
        with PostgreSQLManager() as db:
            tables = db.list_tables()
            
            if not tables:
                print("\nテーブルが見つかりません\n")
                return
            
            nf_tables = [t for t in tables if t.startswith('nf_')]
            
            if not nf_tables:
                print("\nnf_*テーブルが見つかりません\n")
                return
            
            print(f"\nnf_*テーブル: {len(nf_tables)} 個\n")
            
            for table in nf_tables:
                print(f"テーブル: {table}")
                print("-" * 80)
                
                # テーブル情報を取得
                table_info = db.get_table_info(table)
                print(table_info.to_string(index=False))
                print()
                
                # レコード数を取得
                db.cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = db.cursor.fetchone()[0]
                print(f"レコード数: {count}")
                print("=" * 80 + "\n")
                
    except Exception as e:
        print(f"\n✗ エラー: {e}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'test':
            # 接続テストのみ
            test_connection_only()
        elif command == 'info':
            # テーブル情報表示
            show_table_info()
        elif command == 'setup':
            # フルセットアップ
            setup_database()
        else:
            print(f"不明なコマンド: {command}")
            print("\n使用方法:")
            print("  python setup_postgres.py test   # 接続テスト")
            print("  python setup_postgres.py info   # テーブル情報表示")
            print("  python setup_postgres.py setup  # フルセットアップ")
    else:
        # デフォルトはフルセットアップ
        setup_database()
