-- ============================================================================
-- NeuralForecast分析システム用SQLクエリ集
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. 基本クエリ
-- ----------------------------------------------------------------------------

-- 全モデルのサマリ（ビュー使用）
SELECT 
    model_alias,
    model_class,
    h,
    total_params,
    n_series,
    epoch,
    complexity_category,
    overall_score,
    weight_health,
    num_layers,
    avg_layer_health,
    analyzed_at
FROM vw_model_analysis_summary
ORDER BY analyzed_at DESC;

-- 最新の分析結果のみ
SELECT *
FROM vw_model_analysis_summary
WHERE analyzed_at = (SELECT MAX(analyzed_at) FROM vw_model_analysis_summary);

-- ----------------------------------------------------------------------------
-- 2. 健全性診断クエリ
-- ----------------------------------------------------------------------------

-- 健全性スコアが低いモデル（要注意）
SELECT 
    mp.model_alias,
    md.overall_score,
    md.weight_health,
    md.convergence_status,
    mp.analyzed_at
FROM nf_model_diagnosis md
JOIN nf_model_profile mp ON md.model_dir_hash = mp.model_dir_hash
WHERE md.overall_score < 60
ORDER BY md.overall_score ASC;

-- 重みの健全性が「bad」のモデル
SELECT 
    mp.model_alias,
    md.weight_health,
    md.overall_score,
    md.recommendations
FROM nf_model_diagnosis md
JOIN nf_model_profile mp ON md.model_dir_hash = mp.model_dir_hash
WHERE md.weight_health = 'bad'
ORDER BY md.overall_score ASC;

-- 健全性スコアが最も低い層（上位20）
SELECT 
    mp.model_alias,
    ws.layer_name,
    ws.layer_type,
    ws.health_score,
    ws.outlier_ratio,
    ws.sparsity
FROM nf_weight_statistics ws
JOIN nf_model_profile mp ON ws.model_dir_hash = mp.model_dir_hash
WHERE ws.health_score < 5
ORDER BY ws.health_score ASC, ws.outlier_ratio DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 3. 最適化提案クエリ
-- ----------------------------------------------------------------------------

-- 高優先度の最適化提案
SELECT 
    mp.model_alias,
    os.category,
    os.parameter_name,
    os.current_value,
    os.suggested_value,
    os.expected_impact,
    os.priority
FROM nf_optimization_suggestions os
JOIN nf_model_profile mp ON os.model_dir_hash = mp.model_dir_hash
WHERE os.priority >= 4
ORDER BY os.priority DESC, mp.model_alias;

-- モデル別の最適化提案数
SELECT 
    mp.model_alias,
    COUNT(*) as total_suggestions,
    SUM(CASE WHEN os.priority >= 4 THEN 1 ELSE 0 END) as high_priority_suggestions,
    AVG(os.priority) as avg_priority
FROM nf_optimization_suggestions os
JOIN nf_model_profile mp ON os.model_dir_hash = mp.model_dir_hash
GROUP BY mp.model_alias
ORDER BY high_priority_suggestions DESC;

-- カテゴリ別の最適化提案
SELECT 
    os.category,
    COUNT(*) as count,
    AVG(os.priority) as avg_priority
FROM nf_optimization_suggestions os
GROUP BY os.category
ORDER BY count DESC;

-- ----------------------------------------------------------------------------
-- 4. モデル複雑度比較
-- ----------------------------------------------------------------------------

-- 複雑度カテゴリ別の統計
SELECT 
    mc.complexity_category,
    COUNT(*) as model_count,
    AVG(mp.total_params) as avg_params,
    AVG(mc.memory_mb) as avg_memory_mb,
    AVG(mc.param_efficiency) as avg_efficiency
FROM nf_model_complexity mc
JOIN nf_model_profile mp ON mc.model_dir_hash = mp.model_dir_hash
GROUP BY mc.complexity_category
ORDER BY avg_params DESC;

-- メモリ消費が大きいモデル（Top 10）
SELECT 
    mp.model_alias,
    mc.memory_mb,
    mp.total_params,
    mc.complexity_category
FROM nf_model_complexity mc
JOIN nf_model_profile mp ON mc.model_dir_hash = mp.model_dir_hash
ORDER BY mc.memory_mb DESC
LIMIT 10;

-- パラメータ効率が低いモデル
SELECT 
    mp.model_alias,
    mp.total_params,
    mp.h,
    mp.input_size,
    mc.param_efficiency,
    mc.complexity_category
FROM nf_model_complexity mc
JOIN nf_model_profile mp ON mc.model_dir_hash = mp.model_dir_hash
WHERE mc.param_efficiency > 1000  -- 閾値は調整可能
ORDER BY mc.param_efficiency DESC;

-- ----------------------------------------------------------------------------
-- 5. パラメータ感度分析
-- ----------------------------------------------------------------------------

-- 重要度が高いパラメータ（Top 20）
SELECT 
    mp.model_alias,
    ps.parameter_name,
    ps.parameter_value,
    ps.importance_score,
    ps.category
FROM nf_parameter_sensitivity ps
JOIN nf_model_profile mp ON ps.model_dir_hash = mp.model_dir_hash
WHERE ps.importance_score >= 8
ORDER BY ps.importance_score DESC, mp.model_alias
LIMIT 20;

-- カテゴリ別の平均重要度
SELECT 
    ps.category,
    COUNT(*) as param_count,
    AVG(ps.importance_score) as avg_importance,
    MAX(ps.importance_score) as max_importance
FROM nf_parameter_sensitivity ps
GROUP BY ps.category
ORDER BY avg_importance DESC;

-- 特定のパラメータの分布（例: learning_rate）
SELECT 
    mp.model_alias,
    ps.parameter_value,
    md.overall_score
FROM nf_parameter_sensitivity ps
JOIN nf_model_profile mp ON ps.model_dir_hash = mp.model_dir_hash
JOIN nf_model_diagnosis md ON ps.model_dir_hash = md.model_dir_hash
WHERE ps.parameter_name = 'learning_rate'
ORDER BY md.overall_score DESC;

-- ----------------------------------------------------------------------------
-- 6. 学習状態分析
-- ----------------------------------------------------------------------------

-- Early stoppingが発動したモデル
SELECT 
    mp.model_alias,
    ts.epoch,
    ts.global_step,
    ts.early_stopped,
    ts.final_lr,
    md.overall_score
FROM nf_training_state ts
JOIN nf_model_profile mp ON ts.model_dir_hash = mp.model_dir_hash
JOIN nf_model_diagnosis md ON ts.model_dir_hash = md.model_dir_hash
WHERE ts.early_stopped = TRUE
ORDER BY ts.epoch DESC;

-- 学習が完了したが健全性が低いモデル（要調査）
SELECT 
    mp.model_alias,
    ts.epoch,
    ts.early_stopped,
    md.overall_score,
    md.weight_health
FROM nf_training_state ts
JOIN nf_model_profile mp ON ts.model_dir_hash = mp.model_dir_hash
JOIN nf_model_diagnosis md ON ts.model_dir_hash = md.model_dir_hash
WHERE ts.early_stopped = FALSE AND md.overall_score < 60
ORDER BY md.overall_score ASC;

-- ----------------------------------------------------------------------------
-- 7. データセット特性分析
-- ----------------------------------------------------------------------------

-- ゼロ率が高いデータセット（低需要データ）
SELECT 
    mp.model_alias,
    dp.n_series,
    dp.n_temporal,
    dp.zero_rate,
    dp.missing_rate
FROM nf_dataset_profile dp
JOIN nf_model_profile mp ON dp.model_dir_hash = mp.model_dir_hash
WHERE dp.zero_rate > 0.3
ORDER BY dp.zero_rate DESC;

-- データセット規模別の統計
SELECT 
    CASE 
        WHEN dp.total_observations < 10000 THEN 'Small (<10k)'
        WHEN dp.total_observations < 100000 THEN 'Medium (10k-100k)'
        ELSE 'Large (>100k)'
    END as dataset_size,
    COUNT(*) as model_count,
    AVG(dp.zero_rate) as avg_zero_rate,
    AVG(md.overall_score) as avg_model_score
FROM nf_dataset_profile dp
JOIN nf_model_profile mp ON dp.model_dir_hash = mp.model_dir_hash
JOIN nf_model_diagnosis md ON dp.model_dir_hash = md.model_dir_hash
GROUP BY dataset_size
ORDER BY 
    CASE dataset_size
        WHEN 'Small (<10k)' THEN 1
        WHEN 'Medium (10k-100k)' THEN 2
        ELSE 3
    END;

-- ----------------------------------------------------------------------------
-- 8. 層別統計
-- ----------------------------------------------------------------------------

-- 層タイプ別の統計
SELECT 
    ws.layer_type,
    COUNT(*) as layer_count,
    AVG(ws.param_count) as avg_params,
    AVG(ws.health_score) as avg_health,
    AVG(ws.sparsity) as avg_sparsity,
    AVG(ws.outlier_ratio) as avg_outlier_ratio
FROM nf_weight_statistics ws
GROUP BY ws.layer_type
ORDER BY avg_params DESC;

-- 最もパラメータが多い層（Top 20）
SELECT 
    mp.model_alias,
    ws.layer_name,
    ws.layer_type,
    ws.param_count,
    ws.health_score
FROM nf_weight_statistics ws
JOIN nf_model_profile mp ON ws.model_dir_hash = mp.model_dir_hash
ORDER BY ws.param_count DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- 9. 総合ランキング
-- ----------------------------------------------------------------------------

-- 総合的に優れたモデル（Top 10）
SELECT 
    mp.model_alias,
    md.overall_score,
    md.weight_health,
    mc.complexity_category,
    mc.memory_mb,
    ts.epoch,
    mp.analyzed_at
FROM nf_model_profile mp
JOIN nf_model_diagnosis md ON mp.model_dir_hash = md.model_dir_hash
JOIN nf_model_complexity mc ON mp.model_dir_hash = mc.model_dir_hash
JOIN nf_training_state ts ON mp.model_dir_hash = ts.model_dir_hash
WHERE md.overall_score >= 70
ORDER BY md.overall_score DESC, mc.memory_mb ASC
LIMIT 10;

-- 改善の余地が大きいモデル（高優先度提案が多い）
SELECT 
    mp.model_alias,
    md.overall_score,
    COUNT(os.id) as total_suggestions,
    SUM(CASE WHEN os.priority >= 4 THEN 1 ELSE 0 END) as high_priority_count
FROM nf_model_profile mp
JOIN nf_model_diagnosis md ON mp.model_dir_hash = md.model_dir_hash
JOIN nf_optimization_suggestions os ON mp.model_dir_hash = os.model_dir_hash
GROUP BY mp.model_alias, md.overall_score
HAVING SUM(CASE WHEN os.priority >= 4 THEN 1 ELSE 0 END) > 0
ORDER BY high_priority_count DESC, md.overall_score ASC;

-- ----------------------------------------------------------------------------
-- 10. データエクスポート用クエリ
-- ----------------------------------------------------------------------------

-- モデル全体のレポート（結合テーブル）
SELECT 
    mp.model_alias,
    mp.model_class,
    mp.h,
    mp.input_size,
    mp.total_params,
    mp.freq,
    dp.n_series,
    dp.n_temporal,
    ts.epoch,
    ts.early_stopped,
    mc.complexity_category,
    mc.memory_mb,
    md.overall_score,
    md.weight_health,
    md.convergence_status,
    COUNT(DISTINCT ws.id) as num_layers,
    AVG(ws.health_score) as avg_layer_health,
    COUNT(DISTINCT os.id) as num_suggestions,
    mp.analyzed_at
FROM nf_model_profile mp
LEFT JOIN nf_dataset_profile dp ON mp.model_dir_hash = dp.model_dir_hash
LEFT JOIN nf_training_state ts ON mp.model_dir_hash = ts.model_dir_hash
LEFT JOIN nf_model_complexity mc ON mp.model_dir_hash = mc.model_dir_hash
LEFT JOIN nf_model_diagnosis md ON mp.model_dir_hash = md.model_dir_hash
LEFT JOIN nf_weight_statistics ws ON mp.model_dir_hash = ws.model_dir_hash
LEFT JOIN nf_optimization_suggestions os ON mp.model_dir_hash = os.model_dir_hash
GROUP BY 
    mp.model_alias, mp.model_class, mp.h, mp.input_size, mp.total_params, mp.freq,
    dp.n_series, dp.n_temporal, ts.epoch, ts.early_stopped, mc.complexity_category,
    mc.memory_mb, md.overall_score, md.weight_health, md.convergence_status, mp.analyzed_at
ORDER BY mp.analyzed_at DESC;

-- ----------------------------------------------------------------------------
-- 11. メンテナンス用クエリ
-- ----------------------------------------------------------------------------

-- 古い分析結果の削除（30日以上前）
-- DELETE FROM nf_optimization_suggestions WHERE model_dir_hash IN (
--     SELECT model_dir_hash FROM nf_model_profile 
--     WHERE analyzed_at < NOW() - INTERVAL '30 days'
-- );
-- DELETE FROM nf_model_diagnosis WHERE model_dir_hash IN (
--     SELECT model_dir_hash FROM nf_model_profile 
--     WHERE analyzed_at < NOW() - INTERVAL '30 days'
-- );
-- ... 以下同様に全テーブルで実行 ...

-- テーブルサイズの確認
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE tablename LIKE 'nf_%'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- レコード数の確認
SELECT 
    'nf_model_profile' as table_name, 
    COUNT(*) as count FROM nf_model_profile
UNION ALL
SELECT 'nf_dataset_profile', COUNT(*) FROM nf_dataset_profile
UNION ALL
SELECT 'nf_training_state', COUNT(*) FROM nf_training_state
UNION ALL
SELECT 'nf_weight_statistics', COUNT(*) FROM nf_weight_statistics
UNION ALL
SELECT 'nf_model_complexity', COUNT(*) FROM nf_model_complexity
UNION ALL
SELECT 'nf_parameter_sensitivity', COUNT(*) FROM nf_parameter_sensitivity
UNION ALL
SELECT 'nf_model_diagnosis', COUNT(*) FROM nf_model_diagnosis
UNION ALL
SELECT 'nf_optimization_suggestions', COUNT(*) FROM nf_optimization_suggestions;
