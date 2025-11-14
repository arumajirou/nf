-- NeuralForecast AutoML WebUI - Database Schema
-- PostgreSQL 14+
-- Created: 2025-11-13

-- ==========================================
-- 1. EXPERIMENTS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    user_id VARCHAR(255),
    tags JSONB DEFAULT '[]'::jsonb,
    
    CONSTRAINT experiments_name_unique UNIQUE (name)
);

CREATE INDEX idx_experiments_status ON experiments(status);
CREATE INDEX idx_experiments_created_at ON experiments(created_at DESC);
CREATE INDEX idx_experiments_user_id ON experiments(user_id);
CREATE INDEX idx_experiments_tags ON experiments USING gin(tags);

-- ==========================================
-- 2. DATASETS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size_mb FLOAT NOT NULL,
    n_series INTEGER NOT NULL,
    avg_length FLOAT NOT NULL,
    has_exogenous BOOLEAN DEFAULT FALSE,
    has_static BOOLEAN DEFAULT FALSE,
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT datasets_name_unique UNIQUE (name)
);

CREATE INDEX idx_datasets_uploaded_at ON datasets(uploaded_at DESC);

-- ==========================================
-- 3. TRAINING_RUNS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS training_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    dataset_id UUID REFERENCES datasets(id) ON DELETE SET NULL,
    model_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'initializing', 'running', 'completed', 'failed', 'cancelled')),
    start_time TIMESTAMP NOT NULL DEFAULT NOW(),
    end_time TIMESTAMP,
    duration_seconds FLOAT,
    error_message TEXT,
    error_traceback TEXT,
    backend VARCHAR(50) NOT NULL CHECK (backend IN ('optuna', 'ray')),
    num_samples INTEGER,
    num_completed_samples INTEGER DEFAULT 0,
    best_loss FLOAT,
    best_trial_id INTEGER,
    config JSONB NOT NULL DEFAULT '{}'::jsonb,
    
    CONSTRAINT training_runs_duration_check CHECK (duration_seconds IS NULL OR duration_seconds >= 0)
);

CREATE INDEX idx_training_runs_experiment_id ON training_runs(experiment_id);
CREATE INDEX idx_training_runs_status ON training_runs(status);
CREATE INDEX idx_training_runs_start_time ON training_runs(start_time DESC);
CREATE INDEX idx_training_runs_model_name ON training_runs(model_name);

-- ==========================================
-- 4. RESOURCE_METRICS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS resource_metrics (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES training_runs(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- CPU メトリクス
    cpu_percent FLOAT CHECK (cpu_percent >= 0 AND cpu_percent <= 100),
    cpu_count INTEGER,
    
    -- メモリメトリクス
    memory_used_mb FLOAT CHECK (memory_used_mb >= 0),
    memory_total_mb FLOAT CHECK (memory_total_mb >= 0),
    memory_percent FLOAT CHECK (memory_percent >= 0 AND memory_percent <= 100),
    memory_available_mb FLOAT CHECK (memory_available_mb >= 0),
    
    -- GPU メトリクス
    gpu_utilization FLOAT CHECK (gpu_utilization >= 0 AND gpu_utilization <= 100),
    gpu_count INTEGER DEFAULT 0,
    gpu_index INTEGER,
    
    -- VRAM メトリクス
    vram_used_mb FLOAT CHECK (vram_used_mb >= 0),
    vram_total_mb FLOAT CHECK (vram_total_mb >= 0),
    vram_percent FLOAT CHECK (vram_percent >= 0 AND vram_percent <= 100),
    
    -- ディスクI/O メトリクス
    disk_io_read_mb FLOAT CHECK (disk_io_read_mb >= 0),
    disk_io_write_mb FLOAT CHECK (disk_io_write_mb >= 0),
    disk_io_read_speed_mbps FLOAT CHECK (disk_io_read_speed_mbps >= 0),
    disk_io_write_speed_mbps FLOAT CHECK (disk_io_write_speed_mbps >= 0),
    
    -- ネットワークI/O メトリクス
    network_sent_mb FLOAT CHECK (network_sent_mb >= 0),
    network_recv_mb FLOAT CHECK (network_recv_mb >= 0),
    network_sent_speed_mbps FLOAT CHECK (network_sent_speed_mbps >= 0),
    network_recv_speed_mbps FLOAT CHECK (network_recv_speed_mbps >= 0),
    
    -- プロセスメトリクス
    process_cpu_percent FLOAT CHECK (process_cpu_percent >= 0),
    process_memory_mb FLOAT CHECK (process_memory_mb >= 0),
    process_threads INTEGER CHECK (process_threads >= 0)
);

CREATE INDEX idx_resource_metrics_run_id ON resource_metrics(run_id);
CREATE INDEX idx_resource_metrics_timestamp ON resource_metrics(timestamp);
CREATE INDEX idx_resource_metrics_run_timestamp ON resource_metrics(run_id, timestamp DESC);

-- パーティショニング（大量データ対応）
-- CREATE TABLE resource_metrics_y2025m11 PARTITION OF resource_metrics
-- FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');

-- ==========================================
-- 5. RUN_PARAMETERS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS run_parameters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID NOT NULL REFERENCES training_runs(id) ON DELETE CASCADE,
    param_name VARCHAR(255) NOT NULL,
    param_value TEXT NOT NULL,
    param_type VARCHAR(50) NOT NULL CHECK (param_type IN ('int', 'float', 'str', 'bool', 'list', 'dict', 'tuple')),
    is_tunable BOOLEAN DEFAULT FALSE,
    search_space JSONB,
    category VARCHAR(100),
    
    CONSTRAINT run_parameters_unique UNIQUE (run_id, param_name)
);

CREATE INDEX idx_run_parameters_run_id ON run_parameters(run_id);
CREATE INDEX idx_run_parameters_param_name ON run_parameters(param_name);
CREATE INDEX idx_run_parameters_is_tunable ON run_parameters(is_tunable) WHERE is_tunable = TRUE;

-- ==========================================
-- 6. RUN_RESULTS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS run_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID NOT NULL REFERENCES training_runs(id) ON DELETE CASCADE,
    trial_number INTEGER,
    metric_name VARCHAR(255) NOT NULL,
    metric_value FLOAT NOT NULL,
    metric_type VARCHAR(50) CHECK (metric_type IN ('loss', 'accuracy', 'mae', 'rmse', 'mape', 'custom')),
    is_best BOOLEAN DEFAULT FALSE,
    step INTEGER,
    
    CONSTRAINT run_results_unique UNIQUE (run_id, trial_number, metric_name, step)
);

CREATE INDEX idx_run_results_run_id ON run_results(run_id);
CREATE INDEX idx_run_results_metric_name ON run_results(metric_name);
CREATE INDEX idx_run_results_is_best ON run_results(is_best) WHERE is_best = TRUE;
CREATE INDEX idx_run_results_trial_number ON run_results(trial_number);

-- ==========================================
-- 7. MODEL_ARTIFACTS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS model_artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id UUID NOT NULL REFERENCES training_runs(id) ON DELETE CASCADE,
    artifact_type VARCHAR(100) NOT NULL CHECK (artifact_type IN ('model', 'checkpoint', 'config', 'predictions', 'plots', 'logs', 'other')),
    file_path TEXT NOT NULL,
    file_size_mb FLOAT CHECK (file_size_mb >= 0),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_model_artifacts_run_id ON model_artifacts(run_id);
CREATE INDEX idx_model_artifacts_artifact_type ON model_artifacts(artifact_type);
CREATE INDEX idx_model_artifacts_created_at ON model_artifacts(created_at DESC);

-- ==========================================
-- 8. PREDICTIONS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS predictions (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES training_runs(id) ON DELETE CASCADE,
    unique_id VARCHAR(255) NOT NULL,
    ds TIMESTAMP NOT NULL,
    y_actual FLOAT,
    y_pred FLOAT NOT NULL,
    y_lower FLOAT,
    y_upper FLOAT,
    residual FLOAT,
    
    CONSTRAINT predictions_unique UNIQUE (run_id, unique_id, ds)
);

CREATE INDEX idx_predictions_run_id ON predictions(run_id);
CREATE INDEX idx_predictions_unique_id ON predictions(unique_id);
CREATE INDEX idx_predictions_ds ON predictions(ds);

-- ==========================================
-- 9. OPTIMIZATION_HISTORY テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS optimization_history (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES training_runs(id) ON DELETE CASCADE,
    trial_number INTEGER NOT NULL,
    trial_state VARCHAR(50) NOT NULL CHECK (trial_state IN ('running', 'complete', 'pruned', 'failed')),
    value FLOAT,
    datetime_start TIMESTAMP NOT NULL,
    datetime_complete TIMESTAMP,
    duration FLOAT,
    params JSONB NOT NULL,
    user_attrs JSONB DEFAULT '{}'::jsonb,
    system_attrs JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT optimization_history_unique UNIQUE (run_id, trial_number)
);

CREATE INDEX idx_optimization_history_run_id ON optimization_history(run_id);
CREATE INDEX idx_optimization_history_trial_number ON optimization_history(trial_number);
CREATE INDEX idx_optimization_history_value ON optimization_history(value);

-- ==========================================
-- 10. LOGS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS logs (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID REFERENCES training_runs(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    level VARCHAR(20) NOT NULL CHECK (level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    logger_name VARCHAR(255),
    message TEXT NOT NULL,
    module VARCHAR(255),
    function_name VARCHAR(255),
    line_number INTEGER,
    exception TEXT,
    extra JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_logs_run_id ON logs(run_id);
CREATE INDEX idx_logs_timestamp ON logs(timestamp DESC);
CREATE INDEX idx_logs_level ON logs(level);

-- ==========================================
-- 11. NOTIFICATIONS テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('info', 'warning', 'error', 'success')),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    read_at TIMESTAMP,
    related_run_id UUID REFERENCES training_runs(id) ON DELETE SET NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read) WHERE is_read = FALSE;
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

-- ==========================================
-- 12. SYSTEM_CONFIG テーブル
-- ==========================================
CREATE TABLE IF NOT EXISTS system_config (
    key VARCHAR(255) PRIMARY KEY,
    value TEXT NOT NULL,
    value_type VARCHAR(50) NOT NULL CHECK (value_type IN ('string', 'int', 'float', 'bool', 'json')),
    description TEXT,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_by VARCHAR(255)
);

-- デフォルト設定の挿入
INSERT INTO system_config (key, value, value_type, description) VALUES
    ('max_concurrent_runs', '5', 'int', 'Maximum number of concurrent training runs'),
    ('default_num_samples', '50', 'int', 'Default number of optimization samples'),
    ('max_upload_size_mb', '500', 'float', 'Maximum dataset upload size in MB'),
    ('resource_monitor_interval_sec', '5', 'int', 'Resource monitoring interval in seconds'),
    ('log_retention_days', '30', 'int', 'Number of days to retain logs'),
    ('enable_gpu', 'true', 'bool', 'Enable GPU usage for training')
ON CONFLICT (key) DO NOTHING;

-- ==========================================
-- VIEWS（便利なクエリビュー）
-- ==========================================

-- 実験サマリービュー
CREATE OR REPLACE VIEW experiment_summary AS
SELECT 
    e.id,
    e.name,
    e.status,
    e.created_at,
    e.updated_at,
    COUNT(DISTINCT tr.id) as total_runs,
    COUNT(DISTINCT tr.id) FILTER (WHERE tr.status = 'completed') as completed_runs,
    COUNT(DISTINCT tr.id) FILTER (WHERE tr.status = 'running') as running_runs,
    COUNT(DISTINCT tr.id) FILTER (WHERE tr.status = 'failed') as failed_runs,
    MIN(tr.best_loss) as best_loss,
    SUM(tr.duration_seconds) as total_duration_seconds
FROM experiments e
LEFT JOIN training_runs tr ON e.id = tr.experiment_id
GROUP BY e.id, e.name, e.status, e.created_at, e.updated_at;

-- リソース使用量サマリービュー
CREATE OR REPLACE VIEW resource_usage_summary AS
SELECT 
    rm.run_id,
    COUNT(*) as measurement_count,
    AVG(rm.cpu_percent) as avg_cpu_percent,
    MAX(rm.cpu_percent) as max_cpu_percent,
    AVG(rm.memory_percent) as avg_memory_percent,
    MAX(rm.memory_percent) as max_memory_percent,
    AVG(rm.gpu_utilization) as avg_gpu_utilization,
    MAX(rm.gpu_utilization) as max_gpu_utilization,
    AVG(rm.vram_percent) as avg_vram_percent,
    MAX(rm.vram_percent) as max_vram_percent,
    SUM(rm.disk_io_read_mb) as total_disk_read_mb,
    SUM(rm.disk_io_write_mb) as total_disk_write_mb
FROM resource_metrics rm
GROUP BY rm.run_id;

-- 最近の実行ビュー
CREATE OR REPLACE VIEW recent_runs AS
SELECT 
    tr.id,
    tr.experiment_id,
    e.name as experiment_name,
    tr.model_name,
    tr.status,
    tr.start_time,
    tr.end_time,
    tr.duration_seconds,
    tr.best_loss,
    tr.num_samples,
    tr.num_completed_samples,
    CASE 
        WHEN tr.num_samples > 0 THEN (tr.num_completed_samples::float / tr.num_samples * 100)
        ELSE 0 
    END as progress_percent
FROM training_runs tr
JOIN experiments e ON tr.experiment_id = e.id
ORDER BY tr.start_time DESC;

-- ==========================================
-- TRIGGERS（自動更新トリガー）
-- ==========================================

-- experiments テーブルの updated_at 自動更新
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_experiments_updated_at 
    BEFORE UPDATE ON experiments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- training_runs の duration_seconds 自動計算
CREATE OR REPLACE FUNCTION calculate_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.end_time IS NOT NULL AND NEW.start_time IS NOT NULL THEN
        NEW.duration_seconds = EXTRACT(EPOCH FROM (NEW.end_time - NEW.start_time));
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER calculate_training_run_duration
    BEFORE INSERT OR UPDATE ON training_runs
    FOR EACH ROW
    EXECUTE FUNCTION calculate_duration();

-- ==========================================
-- FUNCTIONS（便利な関数）
-- ==========================================

-- 実験の完全削除（カスケード）
CREATE OR REPLACE FUNCTION delete_experiment_cascade(exp_id UUID)
RETURNS VOID AS $$
BEGIN
    DELETE FROM experiments WHERE id = exp_id;
END;
$$ LANGUAGE plpgsql;

-- 古いログの削除
CREATE OR REPLACE FUNCTION cleanup_old_logs(retention_days INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM logs 
    WHERE timestamp < NOW() - (retention_days || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- 古いリソースメトリクスの削除
CREATE OR REPLACE FUNCTION cleanup_old_resource_metrics(retention_days INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM resource_metrics 
    WHERE timestamp < NOW() - (retention_days || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- COMMENTS（テーブル説明）
-- ==========================================

COMMENT ON TABLE experiments IS '実験の基本情報を管理';
COMMENT ON TABLE datasets IS 'アップロードされたデータセットの情報';
COMMENT ON TABLE training_runs IS '個別の学習実行を記録';
COMMENT ON TABLE resource_metrics IS 'リソース使用状況の時系列データ';
COMMENT ON TABLE run_parameters IS '実行時のすべてのパラメータ';
COMMENT ON TABLE run_results IS '学習結果のメトリクス';
COMMENT ON TABLE model_artifacts IS 'モデルと関連ファイルの保存情報';
COMMENT ON TABLE predictions IS '予測結果の詳細データ';
COMMENT ON TABLE optimization_history IS '最適化の試行履歴';
COMMENT ON TABLE logs IS 'システムとアプリケーションログ';
COMMENT ON TABLE notifications IS 'ユーザー通知';
COMMENT ON TABLE system_config IS 'システム設定値';

-- ==========================================
-- 初期データ検証クエリ
-- ==========================================

-- スキーマバージョン
CREATE TABLE IF NOT EXISTS schema_version (
    version VARCHAR(50) PRIMARY KEY,
    applied_at TIMESTAMP NOT NULL DEFAULT NOW(),
    description TEXT
);

INSERT INTO schema_version (version, description) VALUES
    ('1.0.0', 'Initial schema creation')
ON CONFLICT (version) DO NOTHING;

-- ==========================================
-- 完了メッセージ
-- ==========================================

DO $$
BEGIN
    RAISE NOTICE '================================';
    RAISE NOTICE 'Database schema created successfully!';
    RAISE NOTICE 'Schema version: 1.0.0';
    RAISE NOTICE 'Created at: %', NOW();
    RAISE NOTICE '================================';
END $$;
