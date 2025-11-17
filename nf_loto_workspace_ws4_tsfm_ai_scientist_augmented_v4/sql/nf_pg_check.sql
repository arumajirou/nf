\echo '=== 対象テーブルの列挙（nf_* または分析テーブル名） ==='
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog','information_schema')
  AND (
       table_name ILIKE 'nf\_%'
       OR table_name IN ('model_profile','dataset_profile','training_state','weight_statistics',
                         'model_complexity','model_diagnosis','parameter_sensitivity','optimization_suggestions')
  )
ORDER BY table_schema, table_name;

\echo ''
\echo '=== 各テーブルの行数（存在するものだけ） ==='
SELECT format(
  'SELECT ''%I.%I'' AS table, COUNT(*) AS rows FROM %I.%I;',
  table_schema, table_name, table_schema, table_name
)
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog','information_schema')
  AND (
       table_name ILIKE 'nf\_%'
       OR table_name IN ('model_profile','dataset_profile','training_state','weight_statistics',
                         'model_complexity','model_diagnosis','parameter_sensitivity','optimization_suggestions')
  )
ORDER BY table_schema, table_name
\gexec

\echo ''
\echo '=== 代表カラムのサンプル（先頭5件）: よく使うテーブル名を優先 ==='
-- サンプル表示（多すぎると煩雑なので、ごく代表的な名前だけ）
SELECT format('SELECT * FROM %I.%I LIMIT 5;', table_schema, table_name)
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog','information_schema')
  AND table_name IN ('model_profile','dataset_profile','training_state','weight_statistics',
                     'model_complexity','model_diagnosis','parameter_sensitivity','optimization_suggestions')
ORDER BY table_schema, table_name
\gexec

\echo ''
\echo '=== VARCHAR(100) 以内に収まっていない可能性の検出（超過件数と最大長） ==='
-- 可変長文字列(<=100)について、長さ超過の可能性を点検
SELECT format($fmt$
  SELECT '%I.%I' AS table, '%I' AS column,
         COUNT(*) FILTER (WHERE length(COALESCE(%I::text, '')) > %s) AS over_limit_rows,
         MAX(length(COALESCE(%I::text, ''))) AS max_len
  FROM %I.%I;
$fmt$, c.table_schema, c.table_name, c.column_name,
      c.column_name, c.character_maximum_length,
      c.column_name, c.table_schema, c.table_name)
FROM information_schema.columns c
JOIN information_schema.tables t
  ON c.table_schema = t.table_schema AND c.table_name = t.table_name
WHERE c.table_schema NOT IN ('pg_catalog','information_schema')
  AND t.table_type='BASE TABLE'
  AND c.data_type='character varying'
  AND c.character_maximum_length IS NOT NULL
  AND c.character_maximum_length <= 100
  AND (
       c.table_name ILIKE 'nf\_%'
       OR c.table_name IN ('model_profile','dataset_profile','training_state','weight_statistics',
                           'model_complexity','model_diagnosis','parameter_sensitivity','optimization_suggestions')
  )
ORDER BY c.table_schema, c.table_name, c.ordinal_position
\gexec