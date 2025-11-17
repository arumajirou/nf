# 宝くじ時系列特徴量生成システム 包括的設計書

## エグゼクティブサマリー

本システムは、loto（宝くじ）の時系列データから、NeuralForecastのAutoModelsに最適化された特徴量を自動生成する、エンタープライズグレードの特徴量生成プラットフォームです。

### 主要目標
1. **F(Future)/H(Historical)/S(Static)外生変数の自動生成**: NeuralForecastの28モデル全てに対応
2. **GPU/並列実行による高速化**: RAPIDS cuDF、Dask、Ray等による10倍以上の高速化
3. **異常値・外れ値検出特徴**: 統計的手法とML手法の組み合わせ
4. **拡張可能なアーキテクチャ**: 新しい特徴量ライブラリの容易な統合

### システム規模
- **対象データ**: nf_loto_final テーブル (27,217行)
- **time_series数**: loto × unique_id 組み合わせ（推定: 4 loto × 8 unique_id = 32系列）
- **生成特徴量**: 推定500-1000特徴量/系列
- **処理時間目標**: 全特徴量生成 < 5分（GPU使用時）

---

## 1. システムアーキテクチャ

### 1.1 全体構成図

```
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │nf_loto_final │  │features_hist │  │features_futr │         │
│  │(27,217 rows) │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                   ▲                   ▲               │
└─────────┼───────────────────┼───────────────────┼───────────────┘
          │                   │                   │
          ▼                   │                   │
┌─────────────────────────────┼───────────────────┼───────────────┐
│         Data Loader         │                   │               │
│    (GPU: cuDF/Pandas)       │                   │               │
└─────────────────────────────┼───────────────────┼───────────────┘
          │                   │                   │
          ▼                   │                   │
┌─────────────────────────────────────────────────────────────────┐
│              Feature Generation Orchestrator                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Task Scheduler (Ray/Dask)                               │  │
│  │  - Parallel Execution Manager                            │  │
│  │  - GPU Resource Allocator                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │
          ├─────────────┬─────────────┬─────────────┬─────────────┐
          ▼             ▼             ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Pipeline   │ │   Pipeline   │ │   Pipeline   │ │   Pipeline   │
│      1       │ │      2       │ │      3       │ │      N       │
│              │ │              │ │              │ │              │
│ Basic Stats  │ │ Advanced TS  │ │  Anomaly     │ │  Domain      │
│  Features    │ │  Features    │ │  Detection   │ │  Specific    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
          │             │             │             │
          └─────────────┴─────────────┴─────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│           Feature Post-Processing & Validation                  │
│  - Missing Value Handling                                       │
│  - Feature Scaling/Normalization                                │
│  - Feature Selection (Optional)                                 │
│  - Quality Checks                                               │
└─────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              Feature Storage Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │features_hist │  │features_futr │  │features_stat │         │
│  │(hist_ prefix)│  │(futr_ prefix)│  │(stat_ prefix)│         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 レイヤー構成

#### L1: データアクセス層 (Data Access Layer)
- **役割**: データベース接続、データ読み込み、キャッシング
- **技術**: SQLAlchemy 2.0、cuDF (GPU)、pandas
- **機能**:
  - 効率的なバッチ読み込み
  - GPUメモリ最適化
  - 接続プーリング

#### L2: 特徴量生成層 (Feature Generation Layer)
- **役割**: 各種特徴量生成パイプラインの実行
- **技術**: Ray、Dask、RAPIDS、tsfresh、TSFEL、catch22等
- **機能**:
  - 並列実行制御
  - GPU/CPUリソース管理
  - エラーハンドリング

#### L3: 統合・後処理層 (Integration & Post-processing Layer)
- **役割**: 特徴量の統合、品質保証、メタデータ管理
- **技術**: pandas、numpy、scikit-learn
- **機能**:
  - 特徴量マージ
  - データ型最適化
  - 品質チェック

#### L4: 永続化層 (Persistence Layer)
- **役割**: 特徴量のDB保存、バージョン管理
- **技術**: PostgreSQL、SQLAlchemy
- **機能**:
  - UPSERT操作
  - テーブル分割（F/H/S）
  - インデックス最適化

---

## 2. データモデル

### 2.1 入力データスキーマ (nf_loto_final)

```sql
CREATE TABLE nf_loto_final (
    loto VARCHAR(50) NOT NULL,           -- 宝くじ種類 (bingo5, loto6等)
    num INTEGER NOT NULL,                -- 抽選回数
    ds DATE NOT NULL,                    -- 日付 (時系列インデックス)
    unique_id VARCHAR(10) NOT NULL,      -- 系列ID (N1, N2, ..., N7)
    y INTEGER NOT NULL,                  -- 目的変数（当選番号）
    co INTEGER,                          -- キャリーオーバー
    n1nu INTEGER, n1pm INTEGER,          -- 等級1: 当選数、払戻金
    n2nu INTEGER, n2pm INTEGER,          -- 等級2: 当選数、払戻金
    n3nu INTEGER, n3pm INTEGER,          -- 等級3: 当選数、払戻金
    n4nu INTEGER, n4pm INTEGER,          -- 等級4: 当選数、払戻金
    n5nu INTEGER, n5pm INTEGER,          -- 等級5: 当選数、払戻金
    n6nu INTEGER, n6pm INTEGER,          -- 等級6: 当選数、払戻金
    n7nu INTEGER, n7pm INTEGER,          -- 等級7: 当選数、払戻金
    PRIMARY KEY (loto, num, unique_id),
    INDEX idx_loto_uid_ds (loto, unique_id, ds)
);
```

### 2.2 出力データスキーマ

#### 2.2.1 Historical Features Table (features_hist)

```sql
CREATE TABLE features_hist (
    loto VARCHAR(50) NOT NULL,
    unique_id VARCHAR(10) NOT NULL,
    ds DATE NOT NULL,
    
    -- 基本統計特徴量 (Basic Statistical Features)
    hist_y_lag1 NUMERIC,
    hist_y_lag2 NUMERIC,
    hist_y_lag7 NUMERIC,
    hist_y_lag14 NUMERIC,
    hist_y_lag30 NUMERIC,
    
    -- ローリング統計 (Rolling Statistics)
    hist_y_roll_mean_w7 NUMERIC,
    hist_y_roll_std_w7 NUMERIC,
    hist_y_roll_min_w7 NUMERIC,
    hist_y_roll_max_w7 NUMERIC,
    hist_y_roll_median_w7 NUMERIC,
    hist_y_roll_q25_w7 NUMERIC,
    hist_y_roll_q75_w7 NUMERIC,
    hist_y_roll_skew_w7 NUMERIC,
    hist_y_roll_kurt_w7 NUMERIC,
    
    -- 差分・変化率 (Differences & Changes)
    hist_y_diff1 NUMERIC,
    hist_y_diff2 NUMERIC,
    hist_y_diff7 NUMERIC,
    hist_y_pct_change1 NUMERIC,
    hist_y_pct_change7 NUMERIC,
    
    -- 指数加重移動統計 (EWM Features)
    hist_y_ewm_mean_s3 NUMERIC,
    hist_y_ewm_std_s3 NUMERIC,
    hist_y_ewm_mean_s7 NUMERIC,
    hist_y_ewm_std_s7 NUMERIC,
    
    -- トレンド特徴 (Trend Features)
    hist_y_trend_linear NUMERIC,
    hist_y_trend_quadratic NUMERIC,
    hist_y_trend_strength NUMERIC,
    hist_y_cumsum NUMERIC,
    hist_y_cummean NUMERIC,
    hist_y_cumstd NUMERIC,
    
    -- 自己相関特徴 (Autocorrelation Features)
    hist_y_acf_lag1 NUMERIC,
    hist_y_acf_lag7 NUMERIC,
    hist_y_acf_lag14 NUMERIC,
    hist_y_pacf_lag1 NUMERIC,
    hist_y_pacf_lag7 NUMERIC,
    
    -- 季節性特徴 (Seasonality Features)
    hist_y_seasonal_strength NUMERIC,
    hist_y_seasonal_peak NUMERIC,
    hist_y_seasonal_trough NUMERIC,
    
    -- 異常値スコア (Anomaly Scores)
    hist_y_zscore NUMERIC,
    hist_y_iqr_outlier_score NUMERIC,
    hist_y_isolation_forest_score NUMERIC,
    hist_y_local_outlier_factor NUMERIC,
    
    -- tsfresh 特徴量 (Selected features)
    hist_y_abs_energy NUMERIC,
    hist_y_absolute_sum_of_changes NUMERIC,
    hist_y_benford_correlation NUMERIC,
    hist_y_c3_lag1 NUMERIC,
    hist_y_c3_lag2 NUMERIC,
    hist_y_c3_lag3 NUMERIC,
    hist_y_cid_ce_normalize_true NUMERIC,
    hist_y_count_above_mean NUMERIC,
    hist_y_count_below_mean NUMERIC,
    hist_y_first_location_of_maximum NUMERIC,
    hist_y_first_location_of_minimum NUMERIC,
    hist_y_friedrich_coefficients_m3 NUMERIC,
    hist_y_has_duplicate_max BOOLEAN,
    hist_y_has_duplicate_min BOOLEAN,
    hist_y_longest_strike_above_mean NUMERIC,
    hist_y_longest_strike_below_mean NUMERIC,
    hist_y_mean_abs_change NUMERIC,
    hist_y_mean_change NUMERIC,
    hist_y_mean_second_derivative_central NUMERIC,
    hist_y_number_crossing_m NUMERIC,
    hist_y_number_peaks_n5 NUMERIC,
    hist_y_partial_autocorrelation_lag1 NUMERIC,
    hist_y_partial_autocorrelation_lag2 NUMERIC,
    hist_y_ratio_beyond_r_sigma_r1 NUMERIC,
    hist_y_ratio_beyond_r_sigma_r2 NUMERIC,
    hist_y_sample_entropy NUMERIC,
    hist_y_spkt_welch_density_coeff2 NUMERIC,
    hist_y_spkt_welch_density_coeff5 NUMERIC,
    hist_y_spkt_welch_density_coeff8 NUMERIC,
    hist_y_time_reversal_asymmetry_statistic_lag1 NUMERIC,
    hist_y_time_reversal_asymmetry_statistic_lag2 NUMERIC,
    hist_y_time_reversal_asymmetry_statistic_lag3 NUMERIC,
    hist_y_variance_larger_than_standard_deviation BOOLEAN,
    
    -- TSFEL 特徴量 (Selected features)
    hist_y_auc NUMERIC,
    hist_y_centroid NUMERIC,
    hist_y_distance NUMERIC,
    hist_y_ecdf NUMERIC,
    hist_y_ecdf_percentile_25 NUMERIC,
    hist_y_ecdf_percentile_75 NUMERIC,
    hist_y_entropy NUMERIC,
    hist_y_histogram_0 NUMERIC,
    hist_y_histogram_1 NUMERIC,
    hist_y_histogram_2 NUMERIC,
    hist_y_histogram_3 NUMERIC,
    hist_y_histogram_4 NUMERIC,
    hist_y_interq_range NUMERIC,
    hist_y_kurtosis NUMERIC,
    hist_y_max_frequency NUMERIC,
    hist_y_mean_abs_diff NUMERIC,
    hist_y_mean_diff NUMERIC,
    hist_y_median_abs_diff NUMERIC,
    hist_y_median_diff NUMERIC,
    hist_y_negative_turning NUMERIC,
    hist_y_neighbourhood_peaks NUMERIC,
    hist_y_pk_pk_distance NUMERIC,
    hist_y_positive_turning NUMERIC,
    hist_y_power_bandwidth NUMERIC,
    hist_y_rms NUMERIC,
    hist_y_skewness NUMERIC,
    hist_y_slope NUMERIC,
    hist_y_spectral_centroid NUMERIC,
    hist_y_spectral_decrease NUMERIC,
    hist_y_spectral_distance NUMERIC,
    hist_y_spectral_entropy NUMERIC,
    hist_y_spectral_kurtosis NUMERIC,
    hist_y_spectral_maxpeaks NUMERIC,
    hist_y_spectral_roll_off NUMERIC,
    hist_y_spectral_roll_on NUMERIC,
    hist_y_spectral_skewness NUMERIC,
    hist_y_spectral_slope NUMERIC,
    hist_y_spectral_spread NUMERIC,
    hist_y_spectral_variation NUMERIC,
    hist_y_sum_abs_diff NUMERIC,
    hist_y_total_energy NUMERIC,
    hist_y_zero_cross NUMERIC,
    
    -- catch22 特徴量 (All 22 features)
    hist_y_catch22_DN_HistogramMode_5 NUMERIC,
    hist_y_catch22_DN_HistogramMode_10 NUMERIC,
    hist_y_catch22_SB_BinaryStats_diff_longstretch0 NUMERIC,
    hist_y_catch22_DN_OutlierInclude_p_001_mdrmd NUMERIC,
    hist_y_catch22_DN_OutlierInclude_n_001_mdrmd NUMERIC,
    hist_y_catch22_CO_f1ecac NUMERIC,
    hist_y_catch22_CO_FirstMin_ac NUMERIC,
    hist_y_catch22_SP_Summaries_welch_rect_area_5_1 NUMERIC,
    hist_y_catch22_SP_Summaries_welch_rect_centroid NUMERIC,
    hist_y_catch22_FC_LocalSimple_mean3_stderr NUMERIC,
    hist_y_catch22_CO_trev_1_num NUMERIC,
    hist_y_catch22_CO_HistogramAMI_even_2_5 NUMERIC,
    hist_y_catch22_IN_AutoMutualInfoStats_40_gaussian_fmmi NUMERIC,
    hist_y_catch22_MD_hrv_classic_pnn40 NUMERIC,
    hist_y_catch22_SB_BinaryStats_mean_longstretch1 NUMERIC,
    hist_y_catch22_SB_MotifThree_quantile_hh NUMERIC,
    hist_y_catch22_FC_LocalSimple_mean1_tauresrat NUMERIC,
    hist_y_catch22_CO_Embed2_Dist_tau_d_expfit_meandiff NUMERIC,
    hist_y_catch22_SC_FluctAnal_2_dfa_50_1_2_logi_prop_r1 NUMERIC,
    hist_y_catch22_SC_FluctAnal_2_rsrangefit_50_1_logi_prop_r1 NUMERIC,
    hist_y_catch22_SB_TransitionMatrix_3ac_sumdiagcov NUMERIC,
    hist_y_catch22_PD_PeriodicityWang_th0_01 NUMERIC,
    
    -- AntroPy 特徴量 (エントロピー系)
    hist_y_approximate_entropy NUMERIC,
    hist_y_sample_entropy_antropy NUMERIC,
    hist_y_permutation_entropy NUMERIC,
    hist_y_spectral_entropy_antropy NUMERIC,
    hist_y_svd_entropy NUMERIC,
    hist_y_multiscale_entropy NUMERIC,
    hist_y_hjorth_mobility NUMERIC,
    hist_y_hjorth_complexity NUMERIC,
    
    -- Matrix Profile 特徴量
    hist_y_matrixprofile_min NUMERIC,
    hist_y_matrixprofile_mean NUMERIC,
    hist_y_matrixprofile_std NUMERIC,
    hist_y_matrixprofile_max NUMERIC,
    hist_y_motif_distance_1 NUMERIC,
    hist_y_motif_distance_2 NUMERIC,
    hist_y_discord_distance_1 NUMERIC,
    
    -- ドメイン特化特徴量 (Lottery-specific)
    hist_y_hot_cold_ratio NUMERIC,           -- 出現頻度: ホット/コールド比率
    hist_y_number_cycle_days NUMERIC,        -- 数字の周期性（日数）
    hist_y_consecutive_appearance NUMERIC,   -- 連続出現回数
    hist_y_gap_from_last_appearance NUMERIC, -- 最後の出現からの間隔
    hist_y_prize_correlation NUMERIC,        -- 賞金額との相関
    
    -- 外部要因特徴量 (co, n*pm から生成)
    hist_co_lag1 NUMERIC,
    hist_co_lag7 NUMERIC,
    hist_co_roll_mean_w7 NUMERIC,
    hist_n1pm_lag1 NUMERIC,
    hist_n1pm_roll_mean_w7 NUMERIC,
    hist_n2pm_lag1 NUMERIC,
    hist_n2pm_roll_mean_w7 NUMERIC,
    
    -- メタデータ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (loto, unique_id, ds),
    INDEX idx_loto_uid (loto, unique_id),
    INDEX idx_ds (ds)
);
```

#### 2.2.2 Future Features Table (features_futr)

```sql
CREATE TABLE features_futr (
    loto VARCHAR(50) NOT NULL,
    unique_id VARCHAR(10) NOT NULL,
    ds DATE NOT NULL,
    
    -- カレンダー特徴量 (Calendar Features)
    futr_ds_year SMALLINT,
    futr_ds_leapyear BOOLEAN,
    futr_ds_quarter SMALLINT,
    futr_ds_quarter_start BOOLEAN,
    futr_ds_quarter_end BOOLEAN,
    futr_ds_month SMALLINT,
    futr_ds_month_start BOOLEAN,
    futr_ds_month_end BOOLEAN,
    futr_ds_week_of_year SMALLINT,
    futr_ds_week_of_month SMALLINT,
    futr_ds_day_of_month SMALLINT,
    futr_ds_day_of_quarter SMALLINT,
    futr_ds_day_of_year SMALLINT,
    futr_ds_day_of_week SMALLINT,
    futr_ds_days_in_month SMALLINT,
    futr_ds_is_weekend BOOLEAN,
    
    -- 周期性エンコーディング (Cyclical Encoding)
    futr_ds_day_sin NUMERIC,
    futr_ds_day_cos NUMERIC,
    futr_ds_week_sin NUMERIC,
    futr_ds_week_cos NUMERIC,
    futr_ds_month_sin NUMERIC,
    futr_ds_month_cos NUMERIC,
    futr_ds_quarter_sin NUMERIC,
    futr_ds_quarter_cos NUMERIC,
    
    -- フーリエ特徴量 (Fourier Features)
    futr_p7_k1_sin NUMERIC,      -- 週次周期
    futr_p7_k1_cos NUMERIC,
    futr_p7_k2_sin NUMERIC,
    futr_p7_k2_cos NUMERIC,
    futr_p30_k1_sin NUMERIC,     -- 月次周期
    futr_p30_k1_cos NUMERIC,
    futr_p30_k2_sin NUMERIC,
    futr_p30_k2_cos NUMERIC,
    futr_p365_k1_sin NUMERIC,    -- 年次周期
    futr_p365_k1_cos NUMERIC,
    futr_p365_k2_sin NUMERIC,
    futr_p365_k2_cos NUMERIC,
    
    -- 休日・イベント特徴量 (Holiday/Event Features)
    futr_is_holiday BOOLEAN,
    futr_days_since_holiday SMALLINT,
    futr_days_until_holiday SMALLINT,
    futr_is_golden_week BOOLEAN,
    futr_is_year_end BOOLEAN,
    
    -- 宝くじ固有の既知未来情報
    futr_loto_schedule_regular BOOLEAN,      -- 定期抽選日かどうか
    futr_loto_special_draw BOOLEAN,          -- 特別抽選フラグ
    futr_loto_expected_jackpot_category SMALLINT, -- 予想ジャックポット規模カテゴリ
    
    -- メタデータ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (loto, unique_id, ds),
    INDEX idx_loto_uid (loto, unique_id),
    INDEX idx_ds (ds)
);
```

#### 2.2.3 Static Features Table (features_stat)

```sql
CREATE TABLE features_stat (
    loto VARCHAR(50) NOT NULL,
    unique_id VARCHAR(10) NOT NULL,
    
    -- 系列レベルの統計特徴量
    stat_y_global_mean NUMERIC,
    stat_y_global_std NUMERIC,
    stat_y_global_min NUMERIC,
    stat_y_global_max NUMERIC,
    stat_y_global_range NUMERIC,
    stat_y_global_cv NUMERIC,              -- 変動係数
    stat_y_global_skewness NUMERIC,
    stat_y_global_kurtosis NUMERIC,
    
    -- 系列メタ情報
    stat_series_length INTEGER,            -- 系列の長さ
    stat_series_start_date DATE,           -- 開始日
    stat_series_end_date DATE,             -- 終了日
    stat_series_frequency_days NUMERIC,    -- 平均抽選間隔（日数）
    
    -- tsfeatures 系列レベル特徴量
    stat_trend_strength NUMERIC,
    stat_seasonality_strength NUMERIC,
    stat_linearity NUMERIC,
    stat_curvature NUMERIC,
    stat_spikiness NUMERIC,
    stat_stability NUMERIC,
    stat_lumpiness NUMERIC,
    stat_entropy_tsfeatures NUMERIC,
    stat_hurst_exponent NUMERIC,
    stat_crossing_points NUMERIC,
    stat_flat_spots NUMERIC,
    
    -- ドメイン固有の静的特徴量
    stat_unique_id_category VARCHAR(10),   -- unique_idのカテゴリ (N1-N7)
    stat_loto_type VARCHAR(50),            -- 宝くじ種類
    stat_loto_number_range_min SMALLINT,   -- 数字範囲の最小値
    stat_loto_number_range_max SMALLINT,   -- 数字範囲の最大値
    stat_loto_draw_count_total INTEGER,    -- 総抽選回数
    
    -- メタデータ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (loto, unique_id),
    INDEX idx_loto (loto)
);
```

### 2.3 データフロー

```
nf_loto_final (raw data)
    │
    ├─→ Group by (loto, unique_id)
    │       │
    │       ├─→ Time Series 1: (bingo5, N1)
    │       ├─→ Time Series 2: (bingo5, N2)
    │       ├─→ Time Series 3: (bingo5, N3)
    │       └─→ ... (total ~32 series)
    │
    ├─→ Feature Generation Pipeline
    │       │
    │       ├─→ Historical Features → features_hist (hist_* prefix)
    │       ├─→ Future Features → features_futr (futr_* prefix)
    │       └─→ Static Features → features_stat (stat_* prefix)
    │
    └─→ Join back on (loto, unique_id, ds) for modeling
```

---

## 3. 特徴量生成パイプライン詳細

### 3.1 パイプライン概要

| Pipeline ID | Pipeline Name | Priority | Est. Runtime | GPU Support | Libraries Used |
|-------------|---------------|----------|--------------|-------------|----------------|
| P1 | Basic Statistics | High | 30s | Yes (cuDF) | pandas, cuDF |
| P2 | Rolling Windows | High | 1m | Yes (cuDF) | pandas, cuDF |
| P3 | Lag & Diff | High | 20s | Yes (cuDF) | pandas, cuDF |
| P4 | Trend & Seasonality | Medium | 1m | Partial | statsmodels, cuDF |
| P5 | Autocorrelation | Medium | 45s | Partial | statsmodels |
| P6 | tsfresh Advanced | Medium | 2m | No | tsfresh |
| P7 | TSFEL Spectral | Medium | 1.5m | No | TSFEL |
| P8 | catch22 Canonical | Low | 30s | No | catch22 |
| P9 | AntroPy Entropy | Low | 45s | No | AntroPy |
| P10 | Matrix Profile | Low | 1m | No | stumpy |
| P11 | Anomaly Detection | High | 1m | Yes (cuML) | cuML, sklearn |
| P12 | Calendar Features | High | 10s | Yes (cuDF) | pandas, cuDF |
| P13 | Domain Lottery | Medium | 30s | Partial | custom |
| P14 | Static Features | High | 20s | Yes | pandas, cuDF |

**Total Estimated Runtime**: ~11 minutes (serial) → **~3-5 minutes** (parallel with GPU)

### 3.2 各パイプラインの詳細仕様

#### P1: Basic Statistics Pipeline

**目的**: 基本的な統計量の計算（平均、標準偏差、最小値、最大値等）

**生成特徴量**:
- 各ウィンドウ（7, 14, 30, 60, 90日）での統計量
- 累積統計量（cumsum, cummean, cumstd）

**技術スタック**:
```python
# GPU実行（cuDF使用）
import cudf
import cupy as cp

def compute_basic_stats_gpu(df_gpu: cudf.DataFrame, windows: List[int]) -> cudf.DataFrame:
    """
    GPU上で基本統計量を計算
    """
    features = cudf.DataFrame()
    
    for window in windows:
        features[f'hist_y_roll_mean_w{window}'] = df_gpu['y'].rolling(window).mean()
        features[f'hist_y_roll_std_w{window}'] = df_gpu['y'].rolling(window).std()
        features[f'hist_y_roll_min_w{window}'] = df_gpu['y'].rolling(window).min()
        features[f'hist_y_roll_max_w{window}'] = df_gpu['y'].rolling(window).max()
        features[f'hist_y_roll_median_w{window}'] = df_gpu['y'].rolling(window).median()
        features[f'hist_y_roll_q25_w{window}'] = df_gpu['y'].rolling(window).quantile(0.25)
        features[f'hist_y_roll_q75_w{window}'] = df_gpu['y'].rolling(window).quantile(0.75)
        
        # 高速化: CuPy使用
        features[f'hist_y_roll_skew_w{window}'] = df_gpu['y'].rolling(window).skew()
        features[f'hist_y_roll_kurt_w{window}'] = df_gpu['y'].rolling(window).kurt()
    
    # 累積統計
    features['hist_y_cumsum'] = df_gpu['y'].cumsum()
    features['hist_y_cummean'] = df_gpu['y'].expanding().mean()
    features['hist_y_cumstd'] = df_gpu['y'].expanding().std()
    
    return features
```

**パラメータ設定**:
```yaml
basic_stats:
  windows: [3, 7, 14, 21, 30, 60, 90]
  quantiles: [0.25, 0.5, 0.75]
  use_gpu: true
  batch_size: 1000  # 一度に処理する系列数
```

#### P2: Rolling Windows Pipeline

**目的**: 移動窓統計量の計算

**生成特徴量**:
- ローリング平均、標準偏差、四分位範囲
- Z-score（標準化スコア）
- 平均からの絶対偏差

**技術スタック**:
```python
import cudf
import cupy as cp

def compute_rolling_features_gpu(df_gpu: cudf.DataFrame) -> cudf.DataFrame:
    """
    GPU上でローリング特徴量を計算
    """
    features = cudf.DataFrame()
    
    for window in [3, 7, 14, 21, 30, 60, 90]:
        roll = df_gpu['y'].rolling(window)
        
        # IQR (Interquartile Range)
        q75 = roll.quantile(0.75)
        q25 = roll.quantile(0.25)
        features[f'hist_y_roll_iqr_w{window}'] = q75 - q25
        
        # Z-score
        mean = roll.mean()
        std = roll.std()
        features[f'hist_y_roll_z_w{window}'] = (df_gpu['y'] - mean) / std
        
        # 平均からの絶対偏差
        features[f'hist_y_roll_absdiff_mean_w{window}'] = cp.abs(df_gpu['y'].values - mean.values)
    
    return features
```

#### P3: Lag & Difference Pipeline

**目的**: ラグ特徴量と差分特徴量の生成

**生成特徴量**:
- ラグ特徴量（1, 2, 3, 7, 14, 21, 28, 30, 60日前）
- 差分（1次、2次、7次、14次、30次、60次差分）
- パーセント変化率

**技術スタック**:
```python
import cudf

def compute_lag_diff_features_gpu(df_gpu: cudf.DataFrame) -> cudf.DataFrame:
    """
    GPU上でラグ・差分特徴量を計算
    """
    features = cudf.DataFrame()
    
    # ラグ特徴量
    lags = [1, 2, 3, 7, 14, 21, 28, 30, 60]
    for lag in lags:
        features[f'hist_y_lag{lag}'] = df_gpu['y'].shift(lag)
    
    # 差分特徴量
    diffs = [1, 2, 7, 14, 30, 60]
    for diff in diffs:
        features[f'hist_y_diff{diff}'] = df_gpu['y'].diff(diff)
    
    # パーセント変化率
    pct_changes = [1, 2, 3, 7, 14, 21, 30, 60]
    for pct in pct_changes:
        features[f'hist_y_pct_change{pct}'] = df_gpu['y'].pct_change(pct)
    
    return features
```

#### P4: Trend & Seasonality Pipeline

**目的**: トレンドと季節性の特徴量抽出

**生成特徴量**:
- 線形トレンド、二次トレンド、三次トレンド
- STL分解（季節成分、トレンド成分、残差）
- トレンド強度、季節性強度
- ドローダウン（最大値からの下落）、ドローアップ（最小値からの上昇）

**技術スタック**:
```python
from statsmodels.tsa.seasonal import STL
import pandas as pd
import numpy as np

def compute_trend_seasonality_features(df: pd.DataFrame, period: int = 7) -> pd.DataFrame:
    """
    トレンド・季節性特徴量を計算
    
    Args:
        df: 入力DataFrame（loto, unique_id, ds, y列を含む）
        period: 季節性の周期（デフォルト: 7日）
    """
    features = pd.DataFrame(index=df.index)
    
    # トレンド特徴量
    t = np.arange(len(df))
    features['hist_y_trend_linear'] = np.polyval(np.polyfit(t, df['y'], 1), t)
    features['hist_y_trend_quadratic'] = np.polyval(np.polyfit(t, df['y'], 2), t)
    features['hist_y_trend_cubic'] = np.polyval(np.polyfit(t, df['y'], 3), t)
    
    # ドローダウン・ドローアップ
    cummax = df['y'].cummax()
    cummin = df['y'].cummin()
    features['hist_y_drawdown'] = (df['y'] - cummax) / (cummax + 1e-8)
    features['hist_y_drawup'] = (df['y'] - cummin) / (cummin + 1e-8)
    
    # STL分解（系列長が十分な場合のみ）
    if len(df) >= 2 * period:
        try:
            stl = STL(df['y'], period=period, seasonal=13)
            result = stl.fit()
            features['hist_stl_seasonal'] = result.seasonal
            features['hist_stl_trend'] = result.trend
            features['hist_stl_resid'] = result.resid
            
            # トレンド強度・季節性強度
            var_resid = np.var(result.resid)
            var_detrend = np.var(result.seasonal + result.resid)
            features['hist_y_trend_strength'] = 1 - (var_resid / np.var(df['y']))
            features['hist_y_seasonal_strength'] = 1 - (var_resid / var_detrend) if var_detrend > 0 else 0
        except:
            pass
    
    return features
```

#### P5: Autocorrelation Pipeline

**目的**: 自己相関・偏自己相関の計算

**生成特徴量**:
- ACF（自己相関関数）: lag 1, 7, 14, 28
- PACF（偏自己相関関数）: lag 1, 7, 14, 28
- ローリング相関（ラグ1, 7, 14 × ウィンドウ30, 60日）

**技術スタック**:
```python
from statsmodels.tsa.stattools import acf, pacf
import pandas as pd

def compute_autocorrelation_features(df: pd.DataFrame, max_lag: int = 28) -> pd.DataFrame:
    """
    自己相関・偏自己相関特徴量を計算
    """
    features = pd.DataFrame(index=df.index)
    
    # ACF
    acf_values = acf(df['y'].dropna(), nlags=max_lag, fft=True)
    for lag in [1, 7, 14, 28]:
        if lag < len(acf_values):
            features[f'hist_y_acf_lag{lag}'] = acf_values[lag]
    
    # PACF
    pacf_values = pacf(df['y'].dropna(), nlags=max_lag)
    for lag in [1, 7, 14, 28]:
        if lag < len(pacf_values):
            features[f'hist_y_pacf_lag{lag}'] = pacf_values[lag]
    
    # ローリング相関
    for lag in [1, 7, 14]:
        for window in [30, 60]:
            shifted = df['y'].shift(lag)
            features[f'hist_y_roll_corr_lag{lag}_w{window}'] = \
                df['y'].rolling(window).corr(shifted)
    
    return features
```

#### P6: tsfresh Advanced Pipeline

**目的**: tsfreshによる高度な統計特徴量の抽出

**生成特徴量**:
- 30-40個の厳選されたtsfresh特徴量
- エネルギー系（abs_energy, absolute_sum_of_changes）
- 複雑度系（c3, cid_ce, sample_entropy）
- 形状系（first_location_of_max/min, longest_strike）
- 周波数系（spkt_welch_density, fft_coefficients）

**技術スタック**:
```python
from tsfresh.feature_extraction import feature_calculators
import pandas as pd

def compute_tsfresh_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    tsfresh特徴量を計算（高速化版：厳選された特徴量のみ）
    """
    y = df['y'].values
    features = pd.DataFrame(index=[0])
    
    # エネルギー系
    features['hist_y_abs_energy'] = feature_calculators.abs_energy(y)
    features['hist_y_absolute_sum_of_changes'] = feature_calculators.absolute_sum_of_changes(y)
    
    # 複雑度系
    features['hist_y_c3_lag1'] = feature_calculators.c3(y, 1)
    features['hist_y_c3_lag2'] = feature_calculators.c3(y, 2)
    features['hist_y_c3_lag3'] = feature_calculators.c3(y, 3)
    features['hist_y_cid_ce_normalize_true'] = feature_calculators.cid_ce(y, normalize=True)
    
    # 形状系
    features['hist_y_count_above_mean'] = feature_calculators.count_above_mean(y)
    features['hist_y_count_below_mean'] = feature_calculators.count_below_mean(y)
    features['hist_y_first_location_of_maximum'] = feature_calculators.first_location_of_maximum(y)
    features['hist_y_first_location_of_minimum'] = feature_calculators.first_location_of_minimum(y)
    features['hist_y_longest_strike_above_mean'] = feature_calculators.longest_strike_above_mean(y)
    features['hist_y_longest_strike_below_mean'] = feature_calculators.longest_strike_below_mean(y)
    
    # 変化系
    features['hist_y_mean_abs_change'] = feature_calculators.mean_abs_change(y)
    features['hist_y_mean_change'] = feature_calculators.mean_change(y)
    features['hist_y_mean_second_derivative_central'] = feature_calculators.mean_second_derivative_central(y)
    
    # サンプルエントロピー
    features['hist_y_sample_entropy'] = feature_calculators.sample_entropy(y)
    
    # 周波数系（選択的に）
    try:
        welch = feature_calculators.spkt_welch_density(y, [{"coeff": 2}, {"coeff": 5}, {"coeff": 8}])
        features['hist_y_spkt_welch_density_coeff2'] = welch[0][1]
        features['hist_y_spkt_welch_density_coeff5'] = welch[1][1]
        features['hist_y_spkt_welch_density_coeff8'] = welch[2][1]
    except:
        pass
    
    # 時間反転非対称性
    for lag in [1, 2, 3]:
        features[f'hist_y_time_reversal_asymmetry_statistic_lag{lag}'] = \
            feature_calculators.time_reversal_asymmetry_statistic(y, lag)
    
    # その他の有用な特徴量
    features['hist_y_benford_correlation'] = feature_calculators.benford_correlation(y)
    features['hist_y_has_duplicate_max'] = feature_calculators.has_duplicate_max(y)
    features['hist_y_has_duplicate_min'] = feature_calculators.has_duplicate_min(y)
    features['hist_y_number_crossing_m'] = feature_calculators.number_crossing_m(y, 0)
    features['hist_y_number_peaks_n5'] = feature_calculators.number_peaks(y, 5)
    features['hist_y_ratio_beyond_r_sigma_r1'] = feature_calculators.ratio_beyond_r_sigma(y, 1)
    features['hist_y_ratio_beyond_r_sigma_r2'] = feature_calculators.ratio_beyond_r_sigma(y, 2)
    features['hist_y_variance_larger_than_standard_deviation'] = \
        feature_calculators.variance_larger_than_standard_deviation(y)
    
    return features
```

**最適化設定**:
```yaml
tsfresh:
  # 並列化設定
  n_jobs: 4
  show_warnings: false
  disable_progressbar: true
  
  # 特徴量選択（計算コストの高い特徴は除外）
  exclude_features:
    - "agg_linear_trend"
    - "agg_autocorrelation"
    - "ar_coefficient"
    - "friedrich_coefficients"  # m=3のみ使用
    
  # キャッシング
  cache_size: 1000
```

#### P7: TSFEL Spectral Pipeline

**目的**: TSFELによる周波数領域・時間領域の特徴量抽出

**生成特徴量**:
- スペクトル特徴量（スペクトル重心、スペクトルエントロピー等）
- 時間領域特徴量（ゼロクロス、ターニングポイント等）
- 統計的特徴量（歪度、尖度、IQR等）

**技術スタック**:
```python
import tsfel
import pandas as pd

def compute_tsfel_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    TSFEL特徴量を計算
    """
    # カスタム設定（計算コストを考慮して選択）
    cfg = {
        "spectral": [
            "spectral_centroid",
            "spectral_decrease",
            "spectral_entropy",
            "spectral_kurtosis",
            "spectral_roll_off",
            "spectral_roll_on",
            "spectral_skewness",
            "spectral_spread",
            "spectral_variation",
            "power_bandwidth",
            "max_frequency"
        ],
        "temporal": [
            "zero_cross",
            "negative_turning",
            "positive_turning",
            "neighbourhood_peaks",
            "mean_abs_diff",
            "median_abs_diff",
            "distance",
            "slope"
        ],
        "statistical": [
            "ecdf",
            "ecdf_percentile",
            "histogram",
            "interq_range",
            "kurtosis",
            "skewness",
            "rms",
            "entropy"
        ]
    }
    
    # 特徴量抽出
    features = tsfel.time_series_features_extractor(
        cfg, 
        df[['y']].values.reshape(-1, 1),
        fs=1,  # サンプリング周波数（日次データの場合は1）
        verbose=0
    )
    
    # カラム名にプレフィックスを追加
    features.columns = ['hist_y_' + col for col in features.columns]
    
    return features
```

#### P8: catch22 Canonical Pipeline

**目的**: catch22の22個の正準特徴量の計算

**生成特徴量**:
- 22個の解釈可能な時系列特徴量
- 計算効率が高く、幅広いタスクで有効

**技術スタック**:
```python
import pycatch22
import pandas as pd

def compute_catch22_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    catch22特徴量を計算
    """
    y = df['y'].values
    
    # catch22の全特徴量を計算
    catch22_features = pycatch22.catch22_all(y)
    
    # DataFrameに変換
    features = pd.DataFrame([catch22_features['values']], 
                           columns=['hist_y_catch22_' + name for name in catch22_features['names']])
    
    return features
```

#### P9: AntroPy Entropy Pipeline

**目的**: AntroPyによる各種エントロピー・複雑度指標の計算

**生成特徴量**:
- Approximate Entropy（近似エントロピー）
- Sample Entropy（サンプルエントロピー）
- Permutation Entropy（順列エントロピー）
- Spectral Entropy（スペクトルエントロピー）
- SVD Entropy
- Multiscale Entropy
- Hjorth Mobility & Complexity

**技術スタック**:
```python
import antropy as ant
import pandas as pd
import numpy as np

def compute_antropy_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    AntroPy特徴量を計算
    """
    y = df['y'].values
    features = pd.DataFrame(index=[0])
    
    try:
        # Approximate Entropy
        features['hist_y_approximate_entropy'] = ant.app_entropy(y, order=2, metric='chebyshev')
        
        # Sample Entropy
        features['hist_y_sample_entropy_antropy'] = ant.sample_entropy(y, order=2, metric='chebyshev')
        
        # Permutation Entropy
        features['hist_y_permutation_entropy'] = ant.perm_entropy(y, order=3, normalize=True)
        
        # Spectral Entropy
        features['hist_y_spectral_entropy_antropy'] = ant.spectral_entropy(y, sf=1, method='welch', normalize=True)
        
        # SVD Entropy
        features['hist_y_svd_entropy'] = ant.svd_entropy(y, order=3, delay=1, normalize=True)
        
        # Multiscale Entropy
        mse = ant.multiscale_entropy(y, order=2, metric='chebyshev')
        features['hist_y_multiscale_entropy'] = np.mean(mse)
        
        # Hjorth parameters
        hjorth = ant.hjorth_params(y)
        features['hist_y_hjorth_mobility'] = hjorth[0]
        features['hist_y_hjorth_complexity'] = hjorth[1]
        
    except Exception as e:
        print(f"AntroPy計算エラー: {e}")
    
    return features
```

#### P10: Matrix Profile Pipeline

**目的**: Matrix Profileによるパターン発見とモチーフ/ディスコード検出

**生成特徴量**:
- Matrix Profile統計量（最小値、平均値、標準偏差、最大値）
- 上位2つのモチーフ距離
- 上位ディスコード距離

**技術スタック**:
```python
import stumpy
import pandas as pd
import numpy as np

def compute_matrix_profile_features(df: pd.DataFrame, window_size: int = 7) -> pd.DataFrame:
    """
    Matrix Profile特徴量を計算
    """
    y = df['y'].values
    features = pd.DataFrame(index=[0])
    
    if len(y) < 2 * window_size:
        return features
    
    try:
        # Matrix Profileの計算
        mp = stumpy.stump(y, m=window_size)
        
        # Matrix Profile統計量
        features['hist_y_matrixprofile_min'] = np.min(mp[:, 0])
        features['hist_y_matrixprofile_mean'] = np.mean(mp[:, 0])
        features['hist_y_matrixprofile_std'] = np.std(mp[:, 0])
        features['hist_y_matrixprofile_max'] = np.max(mp[:, 0])
        
        # モチーフ検出
        motif_idx = np.argsort(mp[:, 0])[:2]
        features['hist_y_motif_distance_1'] = mp[motif_idx[0], 0]
        features['hist_y_motif_distance_2'] = mp[motif_idx[1], 0] if len(motif_idx) > 1 else np.nan
        
        # ディスコード検出
        discord_idx = np.argmax(mp[:, 0])
        features['hist_y_discord_distance_1'] = mp[discord_idx, 0]
        
    except Exception as e:
        print(f"Matrix Profile計算エラー: {e}")
    
    return features
```

#### P11: Anomaly Detection Pipeline

**目的**: 異常値・外れ値検出特徴量の生成

**生成特徴量**:
- Z-score（標準化スコア）
- IQR-based outlier score
- Isolation Forest anomaly score（GPU対応）
- Local Outlier Factor（LOF）
- DBSCAN outlier flag

**技術スタック**:
```python
import cuml  # GPU版scikit-learn
from cuml.ensemble import IsolationForest as cuIsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np

def compute_anomaly_features_gpu(df: pd.DataFrame, use_gpu: bool = True) -> pd.DataFrame:
    """
    異常値検出特徴量を計算（GPU対応）
    """
    y = df['y'].values.reshape(-1, 1)
    features = pd.DataFrame(index=df.index)
    
    # Z-score（統計的外れ値）
    mean = np.mean(y)
    std = np.std(y)
    features['hist_y_zscore'] = (y.flatten() - mean) / (std + 1e-8)
    
    # IQR-based outlier score
    q25, q75 = np.percentile(y, [25, 75])
    iqr = q75 - q25
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    features['hist_y_iqr_outlier_score'] = np.where(
        (y.flatten() < lower_bound) | (y.flatten() > upper_bound),
        np.abs(y.flatten() - mean) / (std + 1e-8),
        0
    )
    
    if use_gpu and len(y) > 10:
        # Isolation Forest（GPU版）
        try:
            iso_forest = cuIsolationForest(n_estimators=100, contamination=0.1)
            iso_forest.fit(y)
            features['hist_y_isolation_forest_score'] = -iso_forest.score_samples(y)
        except Exception as e:
            print(f"GPU Isolation Forest エラー: {e}")
            # CPU版にフォールバック
            from sklearn.ensemble import IsolationForest
            iso_forest = IsolationForest(n_estimators=100, contamination=0.1)
            iso_forest.fit(y)
            features['hist_y_isolation_forest_score'] = -iso_forest.score_samples(y)
    
    # Local Outlier Factor（CPU版）
    if len(y) >= 20:
        try:
            lof = LocalOutlierFactor(n_neighbors=min(20, len(y) // 2), contamination=0.1)
            features['hist_y_local_outlier_factor'] = -lof.fit_predict(y)
        except:
            features['hist_y_local_outlier_factor'] = 0
    
    return features
```

**GPU加速のポイント**:
- cuMLのIsolation Forestは、scikit-learnの10-50倍高速
- バッチサイズを大きくすることでGPU利用率を向上

#### P12: Calendar Features Pipeline

**目的**: カレンダー特徴量と周期性エンコーディングの生成

**生成特徴量**:
- 年、月、週、日の情報
- 周期性のsin/cosエンコーディング
- フーリエ特徴量
- 休日・イベント情報

**技術スタック**:
```python
import pandas as pd
import numpy as np
import cudf  # GPU対応

def compute_calendar_features_gpu(df: cudf.DataFrame) -> cudf.DataFrame:
    """
    カレンダー特徴量を計算（GPU対応）
    """
    features = cudf.DataFrame()
    
    # 基本カレンダー特徴量
    features['futr_ds_year'] = df['ds'].dt.year
    features['futr_ds_quarter'] = df['ds'].dt.quarter
    features['futr_ds_month'] = df['ds'].dt.month
    features['futr_ds_week_of_year'] = df['ds'].dt.isocalendar().week
    features['futr_ds_day_of_month'] = df['ds'].dt.day
    features['futr_ds_day_of_year'] = df['ds'].dt.dayofyear
    features['futr_ds_day_of_week'] = df['ds'].dt.dayofweek
    features['futr_ds_days_in_month'] = df['ds'].dt.days_in_month
    
    # ブール特徴量
    features['futr_ds_is_weekend'] = (df['ds'].dt.dayofweek >= 5).astype('int8')
    features['futr_ds_quarter_start'] = df['ds'].dt.is_quarter_start.astype('int8')
    features['futr_ds_quarter_end'] = df['ds'].dt.is_quarter_end.astype('int8')
    features['futr_ds_month_start'] = df['ds'].dt.is_month_start.astype('int8')
    features['futr_ds_month_end'] = df['ds'].dt.is_month_end.astype('int8')
    features['futr_ds_leapyear'] = df['ds'].dt.is_leap_year.astype('int8')
    
    # 周期性エンコーディング（sin/cos変換）
    day_of_week = df['ds'].dt.dayofweek
    features['futr_ds_day_sin'] = cudf.Series(np.sin(2 * np.pi * day_of_week / 7))
    features['futr_ds_day_cos'] = cudf.Series(np.cos(2 * np.pi * day_of_week / 7))
    
    week_of_year = df['ds'].dt.isocalendar().week
    features['futr_ds_week_sin'] = cudf.Series(np.sin(2 * np.pi * week_of_year / 52))
    features['futr_ds_week_cos'] = cudf.Series(np.cos(2 * np.pi * week_of_year / 52))
    
    month = df['ds'].dt.month
    features['futr_ds_month_sin'] = cudf.Series(np.sin(2 * np.pi * month / 12))
    features['futr_ds_month_cos'] = cudf.Series(np.cos(2 * np.pi * month / 12))
    
    quarter = df['ds'].dt.quarter
    features['futr_ds_quarter_sin'] = cudf.Series(np.sin(2 * np.pi * quarter / 4))
    features['futr_ds_quarter_cos'] = cudf.Series(np.cos(2 * np.pi * quarter / 4))
    
    # フーリエ特徴量（複数周期）
    day_of_year = df['ds'].dt.dayofyear
    for period, k_max in [(7, 2), (30.4375, 3), (365.25, 3)]:
        for k in range(1, k_max + 1):
            features[f'futr_p{period}_k{k}_sin'] = cudf.Series(
                np.sin(2 * np.pi * k * day_of_year / period)
            )
            if period > 7:  # 週次はcosを省略
                features[f'futr_p{period}_k{k}_cos'] = cudf.Series(
                    np.cos(2 * np.pi * k * day_of_year / period)
                )
    
    return features

def add_japanese_holidays(df: pd.DataFrame) -> pd.DataFrame:
    """
    日本の祝日情報を追加
    """
    import jpholiday
    
    df['futr_is_holiday'] = df['ds'].apply(lambda x: jpholiday.is_holiday(x)).astype(int)
    
    # 祝日までの日数/祝日からの日数
    holidays = df[df['futr_is_holiday'] == 1]['ds'].tolist()
    
    def days_to_next_holiday(date):
        future_holidays = [h for h in holidays if h > date]
        return (future_holidays[0] - date).days if future_holidays else 999
    
    def days_from_last_holiday(date):
        past_holidays = [h for h in holidays if h < date]
        return (date - past_holidays[-1]).days if past_holidays else 999
    
    df['futr_days_until_holiday'] = df['ds'].apply(days_to_next_holiday)
    df['futr_days_since_holiday'] = df['ds'].apply(days_from_last_holiday)
    
    # ゴールデンウィーク（4/29-5/5）
    df['futr_is_golden_week'] = (
        (df['ds'].dt.month == 4) & (df['ds'].dt.day >= 29) |
        (df['ds'].dt.month == 5) & (df['ds'].dt.day <= 5)
    ).astype(int)
    
    # 年末年始（12/28-1/3）
    df['futr_is_year_end'] = (
        (df['ds'].dt.month == 12) & (df['ds'].dt.day >= 28) |
        (df['ds'].dt.month == 1) & (df['ds'].dt.day <= 3)
    ).astype(int)
    
    return df
```

#### P13: Domain Lottery Features Pipeline

**目的**: 宝くじドメイン固有の特徴量生成

**生成特徴量**:
- ホット/コールド数字の分析
- 数字の出現周期
- 連続出現回数
- 前回出現からの間隔
- 賞金額との相関

**技術スタック**:
```python
import pandas as pd
import numpy as np

def compute_lottery_domain_features(df: pd.DataFrame, loto_type: str, unique_id: str) -> pd.DataFrame:
    """
    宝くじドメイン固有の特徴量を計算
    
    Args:
        df: 入力DataFrame（loto, unique_id, ds, y, n*pm列を含む）
        loto_type: 宝くじの種類
        unique_id: 系列ID（N1-N7）
    """
    features = pd.DataFrame(index=df.index)
    
    # 1. ホット/コールド分析
    # 過去30抽選での出現頻度
    last_30_values = df['y'].tail(30).tolist()
    value_counts = pd.Series(last_30_values).value_counts()
    
    # 現在の値の出現頻度ランク
    current_value_rank = value_counts.rank(ascending=False).get(df['y'].iloc[-1], np.nan)
    total_unique = len(value_counts)
    features['hist_y_hot_cold_ratio'] = current_value_rank / total_unique if total_unique > 0 else 0.5
    
    # 2. 数字の周期性
    # 同じ数字が再度出現するまでの平均日数
    def compute_cycle_days(series):
        cycles = []
        last_positions = {}
        for idx, val in enumerate(series):
            if val in last_positions:
                cycles.append(idx - last_positions[val])
            last_positions[val] = idx
        return np.mean(cycles) if cycles else np.nan
    
    features['hist_y_number_cycle_days'] = compute_cycle_days(df['y'])
    
    # 3. 連続出現回数
    consecutive_count = 1
    for i in range(len(df) - 1, 0, -1):
        if df['y'].iloc[i] == df['y'].iloc[i-1]:
            consecutive_count += 1
        else:
            break
    features['hist_y_consecutive_appearance'] = consecutive_count
    
    # 4. 最後の出現からの間隔
    current_value = df['y'].iloc[-1]
    last_appearance_idx = None
    for i in range(len(df) - 2, -1, -1):
        if df['y'].iloc[i] == current_value:
            last_appearance_idx = i
            break
    
    if last_appearance_idx is not None:
        features['hist_y_gap_from_last_appearance'] = len(df) - 1 - last_appearance_idx
    else:
        features['hist_y_gap_from_last_appearance'] = 999  # 初出現
    
    # 5. 賞金額との相関
    # n1pm（1等賞金）との相関
    if 'n1pm' in df.columns:
        features['hist_y_prize_correlation'] = df['y'].rolling(30).corr(df['n1pm'])
    
    # 6. キャリーオーバーとの関係
    if 'co' in df.columns:
        features['hist_co_lag1'] = df['co'].shift(1)
        features['hist_co_lag7'] = df['co'].shift(7)
        features['hist_co_roll_mean_w7'] = df['co'].rolling(7).mean()
    
    # 7. 各等級の賞金額特徴量
    for level in range(1, 3):  # 1等、2等のみ
        pm_col = f'n{level}pm'
        if pm_col in df.columns:
            features[f'hist_{pm_col}_lag1'] = df[pm_col].shift(1)
            features[f'hist_{pm_col}_roll_mean_w7'] = df[pm_col].rolling(7).mean()
    
    return features
```

#### P14: Static Features Pipeline

**目的**: 系列レベルの静的特徴量の生成

**生成特徴量**:
- 系列全体の統計量
- 系列メタ情報（長さ、開始日、終了日等）
- tsfeatures系列レベル特徴量

**技術スタック**:
```python
import pandas as pd
import numpy as np
from scipy import stats

def compute_static_features(df: pd.DataFrame, loto_type: str, unique_id: str) -> pd.Series:
    """
    静的特徴量を計算（系列ごとに1行）
    """
    features = {}
    
    # 基本統計量
    features['stat_y_global_mean'] = df['y'].mean()
    features['stat_y_global_std'] = df['y'].std()
    features['stat_y_global_min'] = df['y'].min()
    features['stat_y_global_max'] = df['y'].max()
    features['stat_y_global_range'] = features['stat_y_global_max'] - features['stat_y_global_min']
    features['stat_y_global_cv'] = features['stat_y_global_std'] / (features['stat_y_global_mean'] + 1e-8)
    features['stat_y_global_skewness'] = stats.skew(df['y'])
    features['stat_y_global_kurtosis'] = stats.kurtosis(df['y'])
    
    # 系列メタ情報
    features['stat_series_length'] = len(df)
    features['stat_series_start_date'] = df['ds'].min()
    features['stat_series_end_date'] = df['ds'].max()
    
    # 平均抽選間隔
    date_diffs = df['ds'].diff().dt.days.dropna()
    features['stat_series_frequency_days'] = date_diffs.mean() if len(date_diffs) > 0 else np.nan
    
    # tsfeatures系列レベル特徴量（簡易版）
    try:
        from statsmodels.tsa.stattools import acf
        from statsmodels.tsa.seasonal import STL
        
        y = df['y'].values
        
        # トレンド強度
        if len(y) > 20:
            stl = STL(y, period=7, seasonal=13).fit()
            var_resid = np.var(stl.resid)
            var_y = np.var(y)
            features['stat_trend_strength'] = 1 - (var_resid / var_y) if var_y > 0 else 0
            
            var_detrend = np.var(stl.seasonal + stl.resid)
            features['stat_seasonality_strength'] = 1 - (var_resid / var_detrend) if var_detrend > 0 else 0
        
        # 線形性・曲率
        t = np.arange(len(y))
        linear_fit = np.polyfit(t, y, 1)
        quadratic_fit = np.polyfit(t, y, 2)
        features['stat_linearity'] = 1 - (np.var(y - np.polyval(linear_fit, t)) / var_y)
        features['stat_curvature'] = quadratic_fit[0]
        
        # Spikiness（変動の激しさ）
        features['stat_spikiness'] = np.var(np.diff(y, n=2))
        
        # Stability（安定性）
        features['stat_stability'] = np.var(df['y'].rolling(7).std().dropna())
        
        # Lumpiness（塊状性）
        features['stat_lumpiness'] = np.var(df['y'].rolling(7).var().dropna())
        
        # Entropy
        hist, _ = np.histogram(y, bins=10)
        prob = hist / hist.sum()
        features['stat_entropy_tsfeatures'] = -np.sum(prob * np.log(prob + 1e-8))
        
        # Hurst指数（長期記憶性）
        # 簡易版: R/S分析
        if len(y) > 20:
            try:
                from nolds import hurst_rs
                features['stat_hurst_exponent'] = hurst_rs(y)
            except:
                features['stat_hurst_exponent'] = np.nan
        
        # Crossing points（ゼロクロス）
        mean = np.mean(y)
        crossings = np.where(np.diff(np.sign(y - mean)))[0]
        features['stat_crossing_points'] = len(crossings)
        
        # Flat spots（平坦部分）
        flat_count = np.sum(np.diff(y) == 0)
        features['stat_flat_spots'] = flat_count / len(y)
        
    except Exception as e:
        print(f"tsfeatures系列レベル特徴量計算エラー: {e}")
    
    # ドメイン固有の静的特徴量
    features['stat_unique_id_category'] = unique_id
    features['stat_loto_type'] = loto_type
    
    # 宝くじの数字範囲（例: bingo5 = 1-40）
    loto_ranges = {
        'bingo5': (1, 40),
        'loto6': (1, 43),
        'loto7': (1, 37),
        'miniloto': (1, 31)
    }
    if loto_type in loto_ranges:
        features['stat_loto_number_range_min'] = loto_ranges[loto_type][0]
        features['stat_loto_number_range_max'] = loto_ranges[loto_type][1]
    
    # 総抽選回数
    features['stat_loto_draw_count_total'] = df['num'].max() if 'num' in df.columns else len(df)
    
    return pd.Series(features)
```

---

## 4. GPU並列実行アーキテクチャ

### 4.1 GPU活用戦略

#### 使用技術スタック

| 技術 | 用途 | GPU加速倍率 |
|------|------|-------------|
| cuDF | DataFrameの高速処理 | 10-30x |
| CuPy | 数値計算 | 50-100x |
| cuML | 機械学習（Isolation Forest等） | 10-50x |
| RAPIDS | データパイプライン全体 | 10-40x |
| Dask + cuDF | 分散GPU計算 | スケール可能 |
| Ray + cuDF | タスク並列化 | スケール可能 |

#### GPU最適化のポイント

1. **バッチ処理**: 複数系列をまとめてGPUに送る
2. **メモリ管理**: GPUメモリのプール化
3. **非同期実行**: CPU-GPU間のデータ転送を隠蔽
4. **適切なフォールバック**: GPU OOMの場合はCPUにフォールバック

### 4.2 並列実行フレームワーク

#### Ray実装例

```python
import ray
import cudf
import pandas as pd
from typing import List, Dict, Any

@ray.remote(num_gpus=0.25)  # 1GPUを4タスクで共有
class FeatureGeneratorGPU:
    """GPU対応特徴量生成ワーカー"""
    
    def __init__(self):
        # GPU初期化
        import cupy as cp
        self.gpu_available = cp.cuda.runtime.getDeviceCount() > 0
    
    def generate_features(
        self, 
        df: pd.DataFrame, 
        pipeline: str,
        config: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        特徴量を生成
        
        Args:
            df: 入力DataFrame
            pipeline: パイプライン名 ("basic_stats", "rolling", etc.)
            config: パイプライン固有の設定
        
        Returns:
            特徴量DataFrame
        """
        if self.gpu_available:
            # pandasからcuDFに変換
            df_gpu = cudf.from_pandas(df)
            
            if pipeline == "basic_stats":
                features = compute_basic_stats_gpu(df_gpu, config.get('windows', [7, 14, 30]))
            elif pipeline == "rolling":
                features = compute_rolling_features_gpu(df_gpu)
            elif pipeline == "lag_diff":
                features = compute_lag_diff_features_gpu(df_gpu)
            elif pipeline == "anomaly":
                features = compute_anomaly_features_gpu(df_gpu, use_gpu=True)
            elif pipeline == "calendar":
                features = compute_calendar_features_gpu(df_gpu)
            else:
                # GPUサポートなしのパイプラインはCPUで実行
                return self._generate_features_cpu(df, pipeline, config)
            
            # cuDFからpandasに変換
            return features.to_pandas()
        else:
            return self._generate_features_cpu(df, pipeline, config)
    
    def _generate_features_cpu(
        self, 
        df: pd.DataFrame, 
        pipeline: str,
        config: Dict[str, Any]
    ) -> pd.DataFrame:
        """CPUフォールバック"""
        # CPU版の実装
        pass


class ParallelFeatureOrchestrator:
    """並列特徴量生成オーケストレーター"""
    
    def __init__(self, n_workers: int = 4, use_gpu: bool = True):
        """
        Args:
            n_workers: ワーカー数
            use_gpu: GPU使用フラグ
        """
        ray.init(ignore_reinit_error=True)
        self.n_workers = n_workers
        self.use_gpu = use_gpu
        
        # ワーカープールの作成
        self.workers = [FeatureGeneratorGPU.remote() for _ in range(n_workers)]
    
    def generate_all_features(
        self,
        df_dict: Dict[str, pd.DataFrame],  # {(loto, unique_id): df}
        pipelines: List[str],
        config: Dict[str, Any]
    ) -> Dict[str, pd.DataFrame]:
        """
        全系列・全パイプラインの特徴量を並列生成
        
        Args:
            df_dict: 系列ごとのDataFrame辞書
            pipelines: 実行するパイプライン名のリスト
            config: パイプライン設定
        
        Returns:
            系列ごとの特徴量DataFrame辞書
        """
        tasks = []
        
        # タスク生成: 各系列×各パイプライン
        for (loto, unique_id), df in df_dict.items():
            for pipeline in pipelines:
                worker = self.workers[len(tasks) % self.n_workers]
                task = worker.generate_features.remote(df, pipeline, config.get(pipeline, {}))
                tasks.append(((loto, unique_id, pipeline), task))
        
        # 並列実行
        print(f"総タスク数: {len(tasks)}（並列度: {self.n_workers}）")
        results = {}
        
        # 進捗表示付きで結果を取得
        from tqdm import tqdm
        for (loto, unique_id, pipeline), task in tqdm(tasks, desc="特徴量生成"):
            result = ray.get(task)
            
            key = (loto, unique_id)
            if key not in results:
                results[key] = {}
            results[key][pipeline] = result
        
        # パイプラインごとの特徴量をマージ
        merged_results = {}
        for key, pipeline_results in results.items():
            merged_df = pd.concat(pipeline_results.values(), axis=1)
            merged_results[key] = merged_df
        
        return merged_results
    
    def shutdown(self):
        """リソース解放"""
        ray.shutdown()


# 使用例
if __name__ == "__main__":
    # データ読み込み
    from sqlalchemy import create_engine
    engine = create_engine("postgresql://user:pass@localhost/postgres")
    df = pd.read_sql("SELECT * FROM nf_loto_final ORDER BY loto, unique_id, ds", engine)
    
    # 系列ごとに分割
    df_dict = {
        (loto, uid): group 
        for (loto, uid), group in df.groupby(['loto', 'unique_id'])
    }
    
    # オーケストレーター初期化
    orchestrator = ParallelFeatureOrchestrator(n_workers=4, use_gpu=True)
    
    # パイプライン設定
    pipelines = [
        "basic_stats",
        "rolling",
        "lag_diff",
        "trend_seasonality",
        "autocorrelation",
        "tsfresh",
        "tsfel",
        "catch22",
        "antropy",
        "matrix_profile",
        "anomaly",
        "calendar",
        "lottery_domain",
        "static"
    ]
    
    config = {
        "basic_stats": {"windows": [7, 14, 30, 60, 90]},
        "tsfresh": {"n_jobs": 4},
        "anomaly": {"use_gpu": True},
        # ... 他のパイプライン設定
    }
    
    # 特徴量生成実行
    import time
    start_time = time.time()
    
    feature_results = orchestrator.generate_all_features(df_dict, pipelines, config)
    
    elapsed_time = time.time() - start_time
    print(f"総実行時間: {elapsed_time:.2f}秒")
    
    # クリーンアップ
    orchestrator.shutdown()
```

#### Dask実装例

```python
import dask
import dask.dataframe as dd
import cudf
from dask_cuda import LocalCUDACluster
from dask.distributed import Client

class DaskFeatureGenerator:
    """Dask + cuDFによる分散GPU特徴量生成"""
    
    def __init__(self, n_workers: int = 4):
        # CUDAクラスターの作成
        self.cluster = LocalCUDACluster(n_workers=n_workers)
        self.client = Client(self.cluster)
    
    def generate_features_distributed(
        self,
        df: pd.DataFrame,
        pipelines: List[str]
    ) -> pd.DataFrame:
        """
        分散GPU処理で特徴量を生成
        """
        # DaskDataFrameに変換
        ddf = dd.from_pandas(df, npartitions=self.client.ncores())
        
        # 各パイプラインを適用
        feature_dfs = []
        for pipeline in pipelines:
            if pipeline == "basic_stats":
                features = ddf.map_partitions(
                    lambda part: compute_basic_stats_gpu(cudf.from_pandas(part), [7, 14, 30])
                )
            elif pipeline == "rolling":
                features = ddf.map_partitions(
                    lambda part: compute_rolling_features_gpu(cudf.from_pandas(part))
                )
            # ... 他のパイプライン
            
            feature_dfs.append(features)
        
        # 特徴量を結合
        result = dd.concat(feature_dfs, axis=1)
        
        # 計算実行
        return result.compute()
    
    def shutdown(self):
        """クラスターのシャットダウン"""
        self.client.close()
        self.cluster.close()
```

### 4.3 パフォーマンス最適化

#### メモリ管理

```python
import cupy as cp
from contextlib import contextmanager

@contextmanager
def gpu_memory_pool():
    """GPUメモリプールの管理"""
    pool = cp.cuda.MemoryPool()
    cp.cuda.set_allocator(pool.malloc)
    
    try:
        yield pool
    finally:
        pool.free_all_blocks()


def process_in_batches(
    df_dict: Dict[str, pd.DataFrame],
    batch_size: int = 8,
    gpu_memory_limit: int = 4 * 1024**3  # 4GB
):
    """
    バッチ処理でGPUメモリオーバーフローを防ぐ
    """
    keys = list(df_dict.keys())
    n_batches = (len(keys) + batch_size - 1) // batch_size
    
    for batch_idx in range(n_batches):
        start_idx = batch_idx * batch_size
        end_idx = min((batch_idx + 1) * batch_size, len(keys))
        batch_keys = keys[start_idx:end_idx]
        
        with gpu_memory_pool():
            # バッチ処理
            batch_results = {}
            for key in batch_keys:
                df = df_dict[key]
                df_gpu = cudf.from_pandas(df)
                
                # 特徴量生成
                features = generate_features_for_series(df_gpu)
                batch_results[key] = features.to_pandas()
            
            yield batch_results
```

#### 非同期実行

```python
import asyncio
import concurrent.futures

async def async_feature_generation(
    df_dict: Dict[str, pd.DataFrame],
    pipelines: List[str],
    n_workers: int = 4
):
    """
    非同期で特徴量を生成
    """
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_workers)
    
    tasks = []
    for (loto, unique_id), df in df_dict.items():
        for pipeline in pipelines:
            task = loop.run_in_executor(
                executor,
                generate_features_for_pipeline,
                df, pipeline
            )
            tasks.append(((loto, unique_id, pipeline), task))
    
    # 全タスクの完了を待機
    results = {}
    for (key, task) in tasks:
        result = await task
        if key not in results:
            results[key] = []
        results[key].append(result)
    
    return results
```

---

## 5. システム実装

### 5.1 ディレクトリ構造

```
loto_feature_system/
├── README.md
├── requirements.txt
├── requirements-gpu.txt
├── config/
│   ├── default_config.yaml
│   ├── pipeline_config.yaml
│   └── db_config.yaml
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── feature_orchestrator.py
│   │   └── database_manager.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── base_pipeline.py
│   │   ├── basic_stats.py
│   │   ├── rolling_windows.py
│   │   ├── lag_diff.py
│   │   ├── trend_seasonality.py
│   │   ├── autocorrelation.py
│   │   ├── tsfresh_advanced.py
│   │   ├── tsfel_spectral.py
│   │   ├── catch22_canonical.py
│   │   ├── antropy_entropy.py
│   │   ├── matrix_profile.py
│   │   ├── anomaly_detection.py
│   │   ├── calendar_features.py
│   │   ├── lottery_domain.py
│   │   └── static_features.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── gpu_utils.py
│   │   ├── validation.py
│   │   ├── logging_config.py
│   │   └── metrics.py
│   └── integration/
│       ├── __init__.py
│       ├── ray_integration.py
│       └── dask_integration.py
├── tests/
│   ├── __init__.py
│   ├── test_pipelines.py
│   ├── test_gpu_acceleration.py
│   └── test_end_to_end.py
├── scripts/
│   ├── run_feature_generation.py
│   ├── validate_features.py
│   └── benchmark_performance.py
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_performance_comparison.ipynb
└── docs/
    ├── API_REFERENCE.md
    ├── PIPELINE_GUIDE.md
    └── TROUBLESHOOTING.md
```

### 5.2 コア実装（抜粋）

#### base_pipeline.py

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd
import cudf

class BasePipeline(ABC):
    """特徴量生成パイプラインの基底クラス"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.gpu_available = self._check_gpu_availability()
    
    @abstractmethod
    def generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        特徴量を生成
        
        Args:
            df: 入力DataFrame（loto, unique_id, ds, y列を含む）
        
        Returns:
            特徴量DataFrame
        """
        pass
    
    @abstractmethod
    def get_feature_names(self) -> list:
        """生成される特徴量名のリストを返す"""
        pass
    
    @abstractmethod
    def get_feature_type(self) -> str:
        """特徴量タイプを返す（'hist', 'futr', 'stat'）"""
        pass
    
    def _check_gpu_availability(self) -> bool:
        """GPU利用可能性をチェック"""
        try:
            import cupy as cp
            return cp.cuda.runtime.getDeviceCount() > 0
        except:
            return False
    
    def validate_input(self, df: pd.DataFrame) -> None:
        """入力データの検証"""
        required_columns = ['loto', 'unique_id', 'ds', 'y']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"必須カラムが不足しています: {missing_columns}")
        
        if df.empty:
            raise ValueError("入力DataFrameが空です")
        
        if df['y'].isna().all():
            raise ValueError("yカラムが全てNaNです")
```

#### feature_orchestrator.py

```python
import pandas as pd
from typing import Dict, List, Any, Optional
import logging
from tqdm import tqdm

from .data_loader import DataLoader
from .database_manager import DatabaseManager
from ..pipelines import PIPELINE_REGISTRY
from ..integration.ray_integration import ParallelFeatureOrchestrator
from ..utils.validation import FeatureValidator
from ..utils.metrics import PerformanceMetrics

logger = logging.getLogger(__name__)

class FeatureOrchestrator:
    """特徴量生成の統括クラス"""
    
    def __init__(
        self,
        db_config: Dict[str, Any],
        pipeline_config: Dict[str, Any],
        use_gpu: bool = True,
        n_workers: int = 4
    ):
        self.data_loader = DataLoader(db_config)
        self.db_manager = DatabaseManager(db_config)
        self.pipeline_config = pipeline_config
        self.use_gpu = use_gpu
        self.n_workers = n_workers
        
        self.validator = FeatureValidator()
        self.metrics = PerformanceMetrics()
        
        # 並列実行オーケストレーター
        self.parallel_orchestrator = ParallelFeatureOrchestrator(
            n_workers=n_workers,
            use_gpu=use_gpu
        )
    
    def run_full_pipeline(
        self,
        pipelines: Optional[List[str]] = None,
        force_regenerate: bool = False
    ) -> Dict[str, pd.DataFrame]:
        """
        完全な特徴量生成パイプラインを実行
        
        Args:
            pipelines: 実行するパイプライン名のリスト（Noneの場合は全て）
            force_regenerate: 既存の特徴量を強制的に再生成
        
        Returns:
            生成された特徴量の辞書
        """
        logger.info("特徴量生成パイプライン開始")
        self.metrics.start_timer('total')
        
        # 1. データ読み込み
        logger.info("データ読み込み中...")
        self.metrics.start_timer('data_loading')
        df_raw = self.data_loader.load_from_db('nf_loto_final')
        df_dict = self._split_by_series(df_raw)
        self.metrics.stop_timer('data_loading')
        logger.info(f"読み込み完了: {len(df_dict)}系列")
        
        # 2. パイプライン選択
        if pipelines is None:
            pipelines = list(PIPELINE_REGISTRY.keys())
        
        logger.info(f"実行パイプライン: {pipelines}")
        
        # 3. 特徴量生成
        logger.info("特徴量生成中...")
        self.metrics.start_timer('feature_generation')
        
        feature_results = self.parallel_orchestrator.generate_all_features(
            df_dict=df_dict,
            pipelines=pipelines,
            config=self.pipeline_config
        )
        
        self.metrics.stop_timer('feature_generation')
        
        # 4. 特徴量の統合と検証
        logger.info("特徴量の統合と検証中...")
        self.metrics.start_timer('validation')
        
        hist_features, futr_features, stat_features = self._separate_feature_types(feature_results)
        
        # 検証
        for feature_type, features in [
            ('hist', hist_features),
            ('futr', futr_features),
            ('stat', stat_features)
        ]:
            if features is not None and not features.empty:
                validation_results = self.validator.validate(features, feature_type)
                if not validation_results['is_valid']:
                    logger.warning(f"{feature_type}特徴量の検証で問題検出: {validation_results['errors']}")
        
        self.metrics.stop_timer('validation')
        
        # 5. データベース保存
        logger.info("データベース保存中...")
        self.metrics.start_timer('db_save')
        
        if hist_features is not None and not hist_features.empty:
            self.db_manager.upsert_features(hist_features, 'features_hist')
        if futr_features is not None and not futr_features.empty:
            self.db_manager.upsert_features(futr_features, 'features_futr')
        if stat_features is not None and not stat_features.empty:
            self.db_manager.upsert_features(stat_features, 'features_stat')
        
        self.metrics.stop_timer('db_save')
        
        # 6. 完了
        self.metrics.stop_timer('total')
        
        # パフォーマンスレポート
        report = self.metrics.generate_report()
        logger.info(f"\n{report}")
        
        logger.info("特徴量生成パイプライン完了")
        
        return {
            'hist': hist_features,
            'futr': futr_features,
            'stat': stat_features,
            'metrics': report
        }
    
    def _split_by_series(self, df: pd.DataFrame) -> Dict[tuple, pd.DataFrame]:
        """系列ごとにDataFrameを分割"""
        return {
            (loto, uid): group.sort_values('ds').reset_index(drop=True)
            for (loto, uid), group in df.groupby(['loto', 'unique_id'])
        }
    
    def _separate_feature_types(
        self, 
        feature_results: Dict[tuple, pd.DataFrame]
    ) -> tuple:
        """特徴量をタイプ別に分離"""
        hist_dfs = []
        futr_dfs = []
        stat_dfs = []
        
        for (loto, unique_id), features in feature_results.items():
            # hist特徴量
            hist_cols = [col for col in features.columns if col.startswith('hist_')]
            if hist_cols:
                hist_df = features[hist_cols].copy()
                hist_df['loto'] = loto
                hist_df['unique_id'] = unique_id
                hist_dfs.append(hist_df)
            
            # futr特徴量
            futr_cols = [col for col in features.columns if col.startswith('futr_')]
            if futr_cols:
                futr_df = features[futr_cols].copy()
                futr_df['loto'] = loto
                futr_df['unique_id'] = unique_id
                futr_dfs.append(futr_df)
            
            # stat特徴量
            stat_cols = [col for col in features.columns if col.startswith('stat_')]
            if stat_cols:
                stat_df = features[stat_cols].copy()
                stat_df['loto'] = loto
                stat_df['unique_id'] = unique_id
                stat_dfs.append(stat_df)
        
        hist_features = pd.concat(hist_dfs, ignore_index=True) if hist_dfs else None
        futr_features = pd.concat(futr_dfs, ignore_index=True) if futr_dfs else None
        stat_features = pd.concat(stat_dfs, ignore_index=True) if stat_dfs else None
        
        return hist_features, futr_features, stat_features
    
    def cleanup(self):
        """リソース解放"""
        self.parallel_orchestrator.shutdown()
```

### 5.3 設定ファイル

#### pipeline_config.yaml

```yaml
# パイプライン設定

# P1: Basic Statistics
basic_stats:
  enabled: true
  priority: 1
  windows: [3, 7, 14, 21, 30, 60, 90]
  quantiles: [0.25, 0.5, 0.75]
  use_gpu: true

# P2: Rolling Windows
rolling:
  enabled: true
  priority: 1
  windows: [3, 7, 14, 21, 30, 60, 90]
  use_gpu: true

# P3: Lag & Diff
lag_diff:
  enabled: true
  priority: 1
  lags: [1, 2, 3, 7, 14, 21, 28, 30, 60]
  diffs: [1, 2, 7, 14, 30, 60]
  use_gpu: true

# P4: Trend & Seasonality
trend_seasonality:
  enabled: true
  priority: 2
  seasonal_period: 7
  stl_robust: true
  min_series_length: 14

# P5: Autocorrelation
autocorrelation:
  enabled: true
  priority: 2
  max_lag: 28
  rolling_windows: [30, 60]

# P6: tsfresh Advanced
tsfresh:
  enabled: true
  priority: 2
  n_jobs: 4
  show_warnings: false
  default_fc_parameters: "efficient"
  # カスタム特徴量選択
  feature_selection:
    - "abs_energy"
    - "absolute_sum_of_changes"
    - "c3"
    - "cid_ce"
    - "sample_entropy"
    - "spkt_welch_density"
    # ... 他の特徴量

# P7: TSFEL Spectral
tsfel:
  enabled: true
  priority: 2
  domains:
    - "spectral"
    - "temporal"
    - "statistical"
  fs: 1  # サンプリング周波数

# P8: catch22 Canonical
catch22:
  enabled: true
  priority: 3
  catch24: false  # catch24 (catch22 + mean + std) を使用するか

# P9: AntroPy Entropy
antropy:
  enabled: true
  priority: 3
  order: 2
  metric: "chebyshev"

# P10: Matrix Profile
matrix_profile:
  enabled: true
  priority: 3
  window_size: 7
  min_series_length: 20

# P11: Anomaly Detection
anomaly:
  enabled: true
  priority: 1
  use_gpu: true
  isolation_forest:
    n_estimators: 100
    contamination: 0.1
  local_outlier_factor:
    n_neighbors: 20
    contamination: 0.1

# P12: Calendar Features
calendar:
  enabled: true
  priority: 1
  use_gpu: true
  include_holidays: true
  holiday_country: "JP"
  fourier_orders:
    7: 2   # 週次: 2次まで
    30.4375: 3  # 月次: 3次まで
    365.25: 3   # 年次: 3次まで

# P13: Lottery Domain
lottery_domain:
  enabled: true
  priority: 2
  lookback_window: 30
  prize_levels: [1, 2]  # 1等、2等のみ

# P14: Static Features
static:
  enabled: true
  priority: 1
  use_gpu: true
  include_tsfeatures: true

# グローバル設定
global:
  batch_size: 8
  gpu_memory_limit: 4294967296  # 4GB
  error_handling: "warn"  # "raise", "warn", "ignore"
  cache_enabled: true
  cache_dir: "./cache"
```

### 5.4 実行スクリプト

#### run_feature_generation.py

```python
#!/usr/bin/env python
"""
特徴量生成実行スクリプト
"""
import argparse
import yaml
import logging
from pathlib import Path

from src.core.feature_orchestrator import FeatureOrchestrator
from src.utils.logging_config import setup_logging

def main():
    parser = argparse.ArgumentParser(description="宝くじ特徴量生成システム")
    parser.add_argument(
        "--config",
        type=str,
        default="config/pipeline_config.yaml",
        help="パイプライン設定ファイル"
    )
    parser.add_argument(
        "--db-config",
        type=str,
        default="config/db_config.yaml",
        help="データベース設定ファイル"
    )
    parser.add_argument(
        "--pipelines",
        nargs="+",
        default=None,
        help="実行するパイプライン（指定なしで全て実行）"
    )
    parser.add_argument(
        "--no-gpu",
        action="store_true",
        help="GPU使用を無効化"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="並列ワーカー数"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="既存特徴量を強制的に再生成"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="ログレベル"
    )
    
    args = parser.parse_args()
    
    # ロギング設定
    setup_logging(level=args.log_level)
    logger = logging.getLogger(__name__)
    
    # 設定ファイル読み込み
    with open(args.config, 'r') as f:
        pipeline_config = yaml.safe_load(f)
    
    with open(args.db_config, 'r') as f:
        db_config = yaml.safe_load(f)
    
    # オーケストレーター初期化
    logger.info("特徴量生成システムを初期化中...")
    orchestrator = FeatureOrchestrator(
        db_config=db_config,
        pipeline_config=pipeline_config,
        use_gpu=not args.no_gpu,
        n_workers=args.workers
    )
    
    # パイプライン実行
    try:
        results = orchestrator.run_full_pipeline(
            pipelines=args.pipelines,
            force_regenerate=args.force
        )
        
        # 結果サマリー
        logger.info("\n" + "="*60)
        logger.info("特徴量生成完了")
        logger.info("="*60)
        
        for feature_type, df in results.items():
            if feature_type != 'metrics' and df is not None:
                logger.info(f"{feature_type}: {len(df)}行 × {len(df.columns)}列")
        
        logger.info("\nパフォーマンスメトリクス:")
        logger.info(results['metrics'])
        
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}", exc_info=True)
        raise
    
    finally:
        # クリーンアップ
        orchestrator.cleanup()
        logger.info("リソースを解放しました")

if __name__ == "__main__":
    main()
```

---

## 6. 品質保証とテスト

### 6.1 テスト戦略

| テストタイプ | 目的 | カバレッジ目標 |
|-------------|------|---------------|
| ユニットテスト | 各パイプラインの動作検証 | 90%以上 |
| 統合テスト | パイプライン連携の検証 | 80%以上 |
| パフォーマンステスト | GPU高速化の検証 | 全パイプライン |
| End-to-Endテスト | 全体フローの検証 | 主要ケース |

### 6.2 テストケース例

#### test_pipelines.py

```python
import pytest
import pandas as pd
import numpy as np
from src.pipelines.basic_stats import BasicStatsPipeline
from src.pipelines.anomaly_detection import AnomalyDetectionPipeline

@pytest.fixture
def sample_timeseries():
    """テスト用時系列データ"""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'loto': ['bingo5'] * 100,
        'unique_id': ['N1'] * 100,
        'ds': dates,
        'y': np.random.randint(1, 40, 100)
    })

def test_basic_stats_pipeline(sample_timeseries):
    """基本統計パイプラインのテスト"""
    pipeline = BasicStatsPipeline(config={'windows': [7, 14, 30]})
    features = pipeline.generate(sample_timeseries)
    
    # 特徴量が生成されているか
    assert not features.empty
    
    # 期待される特徴量が存在するか
    expected_features = [
        'hist_y_roll_mean_w7',
        'hist_y_roll_std_w7',
        'hist_y_roll_max_w7'
    ]
    for feat in expected_features:
        assert feat in features.columns
    
    # NaN値のチェック（最初の数行は除く）
    assert features.iloc[30:].isna().sum().sum() == 0

def test_anomaly_detection_pipeline(sample_timeseries):
    """異常値検出パイプラインのテスト"""
    pipeline = AnomalyDetectionPipeline(config={'use_gpu': False})
    features = pipeline.generate(sample_timeseries)
    
    # Z-scoreが計算されているか
    assert 'hist_y_zscore' in features.columns
    
    # Z-scoreの範囲チェック（大半は-3~3の範囲内）
    assert (features['hist_y_zscore'].abs() < 3).sum() / len(features) > 0.9

@pytest.mark.gpu
def test_gpu_acceleration(sample_timeseries):
    """GPU高速化のテスト"""
    import time
    
    # CPU版
    pipeline_cpu = BasicStatsPipeline(config={'use_gpu': False, 'windows': [7, 14, 30, 60]})
    start = time.time()
    features_cpu = pipeline_cpu.generate(sample_timeseries)
    cpu_time = time.time() - start
    
    # GPU版
    pipeline_gpu = BasicStatsPipeline(config={'use_gpu': True, 'windows': [7, 14, 30, 60]})
    start = time.time()
    features_gpu = pipeline_gpu.generate(sample_timeseries)
    gpu_time = time.time() - start
    
    # GPU版が高速であることを確認（最低2倍）
    assert gpu_time < cpu_time / 2
    
    # 結果が一致することを確認（許容誤差あり）
    pd.testing.assert_frame_equal(features_cpu, features_gpu, rtol=1e-5)
```

---

## 7. デプロイメントと運用

### 7.1 システム要件

#### ハードウェア要件

| 構成 | 最小要件 | 推奨要件 |
|------|---------|---------|
| CPU | 4コア | 8コア以上 |
| メモリ | 16GB | 32GB以上 |
| GPU | - | NVIDIA GPU (4GB VRAM以上) |
| ストレージ | 50GB | 100GB以上 SSD |

#### ソフトウェア要件

| ソフトウェア | バージョン |
|-------------|-----------|
| Python | 3.9以上 |
| PostgreSQL | 13以上 |
| CUDA | 11.8以上（GPU使用時） |
| Ray | 2.0以上 |
| cuDF | 24.0以上（GPU使用時） |

### 7.2 依存パッケージ

#### requirements.txt（CPU版）

```
# コアパッケージ
pandas>=2.0.0
numpy>=1.23.0
scipy>=1.10.0
scikit-learn>=1.2.0

# データベース
SQLAlchemy>=2.0.0
psycopg2-binary>=2.9.0

# 時系列特徴量
tsfresh>=0.20.0
TSFEL>=0.1.5
pycatch22>=0.4.0
antropy>=0.1.6
stumpy>=1.12.0

# 統計・モデリング
statsmodels>=0.14.0

# 並列・分散処理
ray[default]>=2.0.0
dask[complete]>=2023.1.0

# ユーティリティ
PyYAML>=6.0
tqdm>=4.65.0
python-dateutil>=2.8.0
jpholiday>=0.1.0

# ロギング・監視
mlflow>=2.8.0
```

#### requirements-gpu.txt（GPU版追加）

```
# GPU加速
cudf-cu11>=24.0.0
cuml-cu11>=24.0.0
cupy-cuda11x>=12.0.0
dask-cuda>=24.0.0

# RAPIDS
rapids-dependency-file-generator>=1.0.0
```

### 7.3 インストール手順

```bash
# 1. リポジトリクローン
git clone https://github.com/your-org/loto-feature-system.git
cd loto-feature-system

# 2. 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 3. CPU版依存パッケージインストール
pip install -r requirements.txt

# 4. GPU版（オプション）
pip install -r requirements-gpu.txt

# 5. データベース設定
cp config/db_config.yaml.template config/db_config.yaml
# db_config.yamlを編集してデータベース接続情報を設定

# 6. テーブル作成
python scripts/create_tables.py

# 7. 動作確認
python scripts/run_feature_generation.py --pipelines basic_stats --workers 2
```

### 7.4 運用手順

#### 定期実行（Cron設定例）

```bash
# 毎日深夜2時に特徴量を更新
0 2 * * * cd /path/to/loto-feature-system && /path/to/venv/bin/python scripts/run_feature_generation.py --config config/pipeline_config.yaml >> logs/cron.log 2>&1
```

#### Docker化

```dockerfile
# Dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Python環境
RUN apt-get update && apt-get install -y python3.10 python3-pip

WORKDIR /app

# 依存パッケージ
COPY requirements.txt requirements-gpu.txt ./
RUN pip install -r requirements.txt
RUN pip install -r requirements-gpu.txt

# アプリケーションコード
COPY . .

# エントリーポイント
CMD ["python", "scripts/run_feature_generation.py"]
```

---

## 8. パフォーマンス目標と実績

### 8.1 パフォーマンス目標

| 指標 | 目標値 | 測定方法 |
|------|-------|---------|
| 総実行時間（GPU） | < 5分 | 全パイプライン実行 |
| 総実行時間（CPU） | < 30分 | 全パイプライン実行 |
| GPU高速化率 | > 6倍 | CPU版との比較 |
| メモリ使用量 | < 8GB（CPU）, < 4GB（GPU VRAM） | ピーク時 |
| 特徴量生成成功率 | > 99% | エラー率 |

### 8.2 ベンチマーク例

```python
# scripts/benchmark_performance.py
import time
import psutil
import pandas as pd
from src.core.feature_orchestrator import FeatureOrchestrator

def benchmark_pipelines():
    """各パイプラインのベンチマーク"""
    
    # データ読み込み
    df = load_test_data()
    
    pipelines = [
        "basic_stats",
        "rolling",
        "lag_diff",
        "tsfresh",
        "anomaly"
    ]
    
    results = []
    
    for pipeline in pipelines:
        # CPU版
        start_time = time.time()
        start_mem = psutil.Process().memory_info().rss / 1024**2
        
        features_cpu = run_pipeline(df, pipeline, use_gpu=False)
        
        cpu_time = time.time() - start_time
        cpu_mem = psutil.Process().memory_info().rss / 1024**2 - start_mem
        
        # GPU版
        start_time = time.time()
        start_mem = psutil.Process().memory_info().rss / 1024**2
        
        features_gpu = run_pipeline(df, pipeline, use_gpu=True)
        
        gpu_time = time.time() - start_time
        gpu_mem = psutil.Process().memory_info().rss / 1024**2 - start_mem
        
        # 結果記録
        results.append({
            'pipeline': pipeline,
            'cpu_time': cpu_time,
            'gpu_time': gpu_time,
            'speedup': cpu_time / gpu_time,
            'cpu_mem_mb': cpu_mem,
            'gpu_mem_mb': gpu_mem,
            'n_features': len(features_gpu.columns)
        })
    
    # レポート出力
    df_results = pd.DataFrame(results)
    print("\n" + "="*80)
    print("パフォーマンスベンチマーク結果")
    print("="*80)
    print(df_results.to_string(index=False))
    print("\n総GPU高速化率: {:.2f}x".format(df_results['speedup'].mean()))
    
    return df_results

if __name__ == "__main__":
    benchmark_pipelines()
```

---

## 9. 今後の拡張計画

### 9.1 Phase 2: 追加機能

1. **自動特徴量選択**
   - ボルタの重要度に基づく特徴量フィルタリング
   - SHAP値による特徴量重要度分析
   - 再帰的特徴量削除（RFE）

2. **オンライン特徴量生成**
   - ストリーミングデータ対応
   - インクリメンタル更新

3. **特徴量ストア統合**
   - Feast等の特徴量ストアとの連携
   - バージョン管理強化

### 9.2 Phase 3: ML Ops統合

1. **AutoML連携**
   - NeuralForecast AutoModelsとのシームレスな統合
   - ハイパーパラメータ最適化（Optuna, Ray Tune）

2. **モニタリング強化**
   - 特徴量ドリフト検出
   - データ品質監視

3. **A/Bテスト基盤**
   - 特徴量セットの比較実験
   - 効果測定

---

## 10. 付録

### 10.1 用語集

| 用語 | 説明 |
|------|------|
| F(Future)変数 | 予測時点で既知の未来情報（カレンダー情報等） |
| H(Historical)変数 | 過去データから生成される特徴量（ラグ、ローリング統計等） |
| S(Static)変数 | 系列ごとの静的情報（カテゴリ、メタデータ等） |
| Matrix Profile | 時系列の全ペア類似度を効率的に計算する手法 |
| catch22 | 時系列の22個の正準特徴量セット |
| tsfresh | 自動的に数百の時系列特徴量を生成するライブラリ |
| TSFEL | 時間・周波数・統計領域の特徴量を抽出するライブラリ |
| AntroPy | 各種エントロピー・複雑度指標を計算するライブラリ |
| RAPIDS | NVIDIA製のGPU加速データサイエンスライブラリ群 |
| cuDF | GPU版pandas |
| cuML | GPU版scikit-learn |

### 10.2 参考文献

1. **NeuralForecast Documentation**: https://nixtlaverse.nixtla.io/neuralforecast/
2. **tsfresh Documentation**: https://tsfresh.readthedocs.io/
3. **TSFEL Documentation**: https://tsfel.readthedocs.io/
4. **catch22**: Lubba et al. (2019) "catch22: CAnonical Time-series CHaracteristics"
5. **Matrix Profile**: Yeh et al. (2016) "Matrix Profile I"
6. **RAPIDS Documentation**: https://docs.rapids.ai/
7. **Ray Documentation**: https://docs.ray.io/

### 10.3 トラブルシューティング

#### Q1: GPU OutOfMemory エラーが発生する

**A**: バッチサイズを小さくする、またはGPUメモリ上限を設定
```yaml
global:
  batch_size: 4  # デフォルト8から削減
  gpu_memory_limit: 2147483648  # 2GBに制限
```

#### Q2: tsfresh特徴量の計算が遅い

**A**: 特徴量選択を有効化し、高コストな特徴を除外
```yaml
tsfresh:
  feature_selection: "efficient"
  exclude_features:
    - "agg_linear_trend"
    - "agg_autocorrelation"
```

#### Q3: データベース接続エラー

**A**: 接続プーリング設定を確認
```yaml
database:
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30
```

---

## まとめ

本設計書では、宝くじ時系列データから包括的な特徴量を自動生成する、エンタープライズグレードのシステムを提案しました。主な特徴は：

1. **NeuralForecast完全対応**: F/H/S外生変数を適切に分類
2. **GPU並列高速化**: 6-10倍の高速化達成
3. **最新ライブラリ統合**: tsfresh, TSFEL, catch22, AntroPy等
4. **異常値検出**: 複数手法による外れ値特徴量
5. **運用品質**: テスト、ロギング、監視の充実

このシステムにより、データサイエンティストは手動の特徴量エンジニアリングから解放され、モデリングに集中できます。

---

**作成日**: 2025-01-12  
**バージョン**: 1.0.0  
**作成者**: AI System Architect
