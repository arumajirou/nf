"""
PostgreSQL分析テーブルセットアップスクリプト
NeuralForecast分析システム用のテーブルを作成
"""

import sys
from postgres_manager import PostgreSQLManager
from db_config import DB_CONFIG


def create_analysis_tables():
    """分析用テーブルを作成"""
    print("\n" + "="*80)
    print("NeuralForecast分析テーブル作成")
    print("="*80)
    
    # テーブル作成SQL
    tables_sql = {
        'nf_model_profile': """
            CREATE TABLE IF NOT EXISTS nf_model_profile (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) UNIQUE NOT NULL,
                model_alias VARCHAR(100),
                model_class VARCHAR(100),
                h INTEGER,
                input_size INTEGER,
                freq VARCHAR(10),
                total_params BIGINT,
                trainable_params BIGINT,
                hyperparameters JSONB,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                CONSTRAINT valid_h CHECK (h > 0),
                CONSTRAINT valid_input_size CHECK (input_size > 0)
            )
        """,
        
        'nf_dataset_profile': """
            CREATE TABLE IF NOT EXISTS nf_dataset_profile (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) REFERENCES nf_model_profile(model_dir_hash),
                n_series INTEGER,
                n_temporal INTEGER,
                total_observations BIGINT,
                mean_value REAL,
                std_value REAL,
                min_value REAL,
                max_value REAL,
                zero_rate REAL,
                missing_rate REAL,
                statistics JSONB,
                
                CONSTRAINT valid_series CHECK (n_series > 0),
                CONSTRAINT valid_temporal CHECK (n_temporal > 0),
                CONSTRAINT valid_rates CHECK (
                    zero_rate >= 0 AND zero_rate <= 1 AND
                    missing_rate >= 0 AND missing_rate <= 1
                )
            )
        """,
        
        'nf_training_state': """
            CREATE TABLE IF NOT EXISTS nf_training_state (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) REFERENCES nf_model_profile(model_dir_hash),
                epoch INTEGER,
                global_step INTEGER,
                early_stopped BOOLEAN,
                final_lr REAL,
                checkpoint_size_mb REAL,
                optimizer_state JSONB,
                
                CONSTRAINT valid_epoch CHECK (epoch >= 0),
                CONSTRAINT valid_lr CHECK (final_lr > 0)
            )
        """,
        
        'nf_weight_statistics': """
            CREATE TABLE IF NOT EXISTS nf_weight_statistics (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) REFERENCES nf_model_profile(model_dir_hash),
                layer_name VARCHAR(200),
                layer_type VARCHAR(50),
                param_count INTEGER,
                mean_val REAL,
                std_val REAL,
                min_val REAL,
                max_val REAL,
                l1_norm REAL,
                l2_norm REAL,
                sparsity REAL,
                outlier_ratio REAL,
                health_score INTEGER,
                
                CONSTRAINT valid_health_score CHECK (health_score >= 0 AND health_score <= 10),
                CONSTRAINT valid_sparsity CHECK (sparsity >= 0 AND sparsity <= 1)
            )
        """,
        
        'nf_model_complexity': """
            CREATE TABLE IF NOT EXISTS nf_model_complexity (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) UNIQUE REFERENCES nf_model_profile(model_dir_hash),
                param_efficiency REAL,
                depth INTEGER,
                width INTEGER,
                memory_mb REAL,
                complexity_category VARCHAR(20),
                
                CONSTRAINT valid_category CHECK (complexity_category IN ('light', 'medium', 'heavy'))
            )
        """,
        
        'nf_parameter_sensitivity': """
            CREATE TABLE IF NOT EXISTS nf_parameter_sensitivity (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) REFERENCES nf_model_profile(model_dir_hash),
                parameter_name VARCHAR(100),
                parameter_value TEXT,
                importance_score INTEGER,
                category VARCHAR(50),
                
                CONSTRAINT valid_importance CHECK (importance_score >= 1 AND importance_score <= 10),
                CONSTRAINT valid_category_type CHECK (category IN ('model', 'training', 'data', 'other'))
            )
        """,
        
        'nf_model_diagnosis': """
            CREATE TABLE IF NOT EXISTS nf_model_diagnosis (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) UNIQUE REFERENCES nf_model_profile(model_dir_hash),
                overall_score REAL,
                weight_health VARCHAR(20),
                convergence_status VARCHAR(50),
                recommendations JSONB,
                diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                CONSTRAINT valid_score CHECK (overall_score >= 0 AND overall_score <= 100),
                CONSTRAINT valid_health CHECK (weight_health IN ('good', 'warning', 'bad', 'unknown'))
            )
        """,
        
        'nf_optimization_suggestions': """
            CREATE TABLE IF NOT EXISTS nf_optimization_suggestions (
                id SERIAL PRIMARY KEY,
                model_dir_hash VARCHAR(64) REFERENCES nf_model_profile(model_dir_hash),
                category VARCHAR(50),
                parameter_name VARCHAR(100),
                current_value TEXT,
                suggested_value TEXT,
                expected_impact TEXT,
                priority INTEGER,
                
                CONSTRAINT valid_priority CHECK (priority >= 1 AND priority <= 5)
            )
        """
    }
    
    # インデックス作成SQL
    indexes_sql = [
        "CREATE INDEX IF NOT EXISTS idx_model_alias ON nf_model_profile(model_alias)",
        "CREATE INDEX IF NOT EXISTS idx_analyzed_at ON nf_model_profile(analyzed_at)",
        "CREATE INDEX IF NOT EXISTS idx_layer_name ON nf_weight_statistics(layer_name)",
        "CREATE INDEX IF NOT EXISTS idx_health_score ON nf_weight_statistics(health_score)",
        "CREATE INDEX IF NOT EXISTS idx_importance_score ON nf_parameter_sensitivity(importance_score DESC)",
        "CREATE INDEX IF NOT EXISTS idx_priority ON nf_optimization_suggestions(priority DESC)"
    ]
    
    # ビュー作成SQL
    view_sql = """
        CREATE OR REPLACE VIEW vw_model_analysis_summary AS
        SELECT 
            mp.model_dir_hash,
            mp.model_alias,
            mp.model_class,
            mp.h,
            mp.input_size,
            mp.total_params,
            dp.n_series,
            dp.n_temporal,
            ts.epoch,
            ts.early_stopped,
            mc.complexity_category,
            md.overall_score,
            md.weight_health,
            COUNT(ws.id) as num_layers,
            AVG(ws.health_score) as avg_layer_health,
            mp.analyzed_at
        FROM nf_model_profile mp
        LEFT JOIN nf_dataset_profile dp ON mp.model_dir_hash = dp.model_dir_hash
        LEFT JOIN nf_training_state ts ON mp.model_dir_hash = ts.model_dir_hash
        LEFT JOIN nf_model_complexity mc ON mp.model_dir_hash = mc.model_dir_hash
        LEFT JOIN nf_model_diagnosis md ON mp.model_dir_hash = md.model_dir_hash
        LEFT JOIN nf_weight_statistics ws ON mp.model_dir_hash = ws.model_dir_hash
        GROUP BY mp.model_dir_hash, mp.model_alias, mp.model_class, mp.h, mp.input_size,
                 mp.total_params, dp.n_series, dp.n_temporal, ts.epoch, ts.early_stopped,
                 mc.complexity_category, md.overall_score, md.weight_health, mp.analyzed_at
    """
    
    try:
        with PostgreSQLManager(DB_CONFIG) as db:
            print("\n[1/3] テーブル作成中...")
            for table_name, sql in tables_sql.items():
                try:
                    db.cursor.execute(sql)
                    print(f"  ✓ {table_name}")
                except Exception as e:
                    print(f"  ✗ {table_name}: {e}")
                    return False
            
            print("\n[2/3] インデックス作成中...")
            for idx_sql in indexes_sql:
                try:
                    db.cursor.execute(idx_sql)
                except Exception as e:
                    print(f"  ✗ インデックス作成エラー: {e}")
            print(f"  ✓ {len(indexes_sql)} 個のインデックス作成完了")
            
            print("\n[3/3] ビュー作成中...")
            try:
                db.cursor.execute(view_sql)
                print("  ✓ vw_model_analysis_summary")
            except Exception as e:
                print(f"  ✗ ビュー作成エラー: {e}")
            
            db.commit()
            
            print("\n" + "="*80)
            print("✓ 分析テーブル作成完了")
            print("="*80)
            print("\n作成されたテーブル:")
            for table_name in tables_sql.keys():
                print(f"  - {table_name}")
            print("\n作成されたビュー:")
            print("  - vw_model_analysis_summary")
            print("\n次のステップ:")
            print("  python neuralforecast_analyzer_v2.py")
            print("="*80 + "\n")
            
            return True
            
    except Exception as e:
        print(f"\n✗ テーブル作成失敗: {e}")
        return False


def drop_analysis_tables():
    """分析テーブルを削除（クリーンアップ用）"""
    print("\n" + "="*80)
    print("⚠ 警告: 分析テーブルを削除します")
    print("="*80)
    
    response = input("\n本当に削除しますか? (yes/no): ").strip().lower()
    if response != 'yes':
        print("キャンセルしました")
        return False
    
    tables = [
        'nf_optimization_suggestions',
        'nf_model_diagnosis',
        'nf_parameter_sensitivity',
        'nf_model_complexity',
        'nf_weight_statistics',
        'nf_training_state',
        'nf_dataset_profile',
        'nf_model_profile'
    ]
    
    try:
        with PostgreSQLManager(DB_CONFIG) as db:
            # ビュー削除
            db.cursor.execute("DROP VIEW IF EXISTS vw_model_analysis_summary CASCADE")
            print("✓ ビュー削除")
            
            # テーブル削除
            for table in tables:
                db.cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                print(f"✓ {table} 削除")
            
            db.commit()
            print("\n✓ 全テーブル削除完了\n")
            return True
            
    except Exception as e:
        print(f"\n✗ 削除失敗: {e}\n")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'create':
            create_analysis_tables()
        elif command == 'drop':
            drop_analysis_tables()
        else:
            print(f"不明なコマンド: {command}")
            print("\n使用方法:")
            print("  python setup_analysis_tables.py create  # テーブル作成")
            print("  python setup_analysis_tables.py drop    # テーブル削除")
    else:
        # デフォルトは作成
        create_analysis_tables()
