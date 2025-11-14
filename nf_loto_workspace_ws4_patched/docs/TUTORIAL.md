# 自動モデルファクトリー - チュートリアル

## 📘 はじめに

このチュートリアルでは、自動モデルファクトリーシステムの使い方を段階的に学びます。各レッスンは独立しており、必要な部分から学習できます。

**所要時間**: 全体で約2-3時間（実践を含む）

---

## 📋 目次

- [レッスン0: 環境セットアップ](#レッスン0-環境セットアップ)
- [レッスン1: 最初の予測（10分）](#レッスン1-最初の予測)
- [レッスン2: データの準備と検証（15分）](#レッスン2-データの準備と検証)
- [レッスン3: モデルの選択（15分）](#レッスン3-モデルの選択)
- [レッスン4: ハイパーパラメータのカスタマイズ（20分）](#レッスン4-ハイパーパラメータのカスタマイズ)
- [レッスン5: MLflowでの実験管理（20分）](#レッスン5-mlflowでの実験管理)
- [レッスン6: 高度な最適化（30分）](#レッスン6-高度な最適化)
- [レッスン7: 本番環境への展開（20分）](#レッスン7-本番環境への展開)

---

## レッスン0: 環境セットアップ

### ステップ1: 必要なパッケージのインストール

```bash
# 基本パッケージ
pip install neuralforecast optuna 'ray[tune]' mlflow pytorch-lightning pandas numpy

# GPU使用時（推奨）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### ステップ2: インストール確認

```python
# test_installation.py
import torch
import neuralforecast
import optuna
import ray
import mlflow

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("GPU count:", torch.cuda.device_count())
print("NeuralForecast version:", neuralforecast.__version__)
print("Optuna version:", optuna.__version__)
print("Ray version:", ray.__version__)
print("MLflow version:", mlflow.__version__)

print("\n✅ All packages installed successfully!")
```

### ステップ3: サンプルデータの準備

```python
# prepare_sample_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_data(n_series=3, n_periods=365):
    """サンプルの時系列データを作成"""
    data = []
    
    for series_id in range(n_series):
        start_date = datetime(2023, 1, 1)
        dates = [start_date + timedelta(days=i) for i in range(n_periods)]
        
        # トレンド + 季節性 + ノイズ
        trend = np.linspace(100, 200, n_periods)
        seasonality = 20 * np.sin(np.arange(n_periods) * 2 * np.pi / 7)
        noise = np.random.normal(0, 5, n_periods)
        values = trend + seasonality + noise + (series_id * 50)
        
        for date, value in zip(dates, values):
            data.append({
                'unique_id': f'series_{series_id}',
                'ds': date,
                'y': value
            })
    
    df = pd.DataFrame(data)
    df.to_csv('sample_data.csv', index=False)
    print(f"✅ Sample data created: {len(df)} rows, {n_series} series")
    return df

# サンプルデータ作成
df = create_sample_data()
print(df.head(10))
```

**必須カラム**:
- `unique_id`: 時系列を識別するID
- `ds`: 日付（datetime型）
- `y`: 予測対象の値（数値）

---

## レッスン1: 最初の予測

**目標**: 最もシンプルな方法で予測を実行する

### ステップ1: 基本的な予測

```python
# lesson1_basic_forecast.py
import pandas as pd
from auto_model_factory import create_auto_model

# データ読み込み
df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

print("📊 Dataset info:")
print(f"  Rows: {len(df)}")
print(f"  Series: {df['unique_id'].nunique()}")
print(f"  Date range: {df['ds'].min()} to {df['ds'].max()}")

# 🚀 自動最適化実行
print("\n🔍 Starting optimization...")
auto_model = create_auto_model(
    model_name="NHITS",       # モデル選択
    h=7,                      # 7日先を予測
    dataset=df,               # データ
    backend="optuna",         # Optunaを使用
    num_samples=10,           # 10回試行（最初は少なめ）
    verbose=True              # 詳細出力
)

# 予測実行
print("\n📈 Making predictions...")
predictions = auto_model.predict(dataset=df)

print("\n✅ Forecast completed!")
print(predictions.head())

# 結果を保存
predictions.to_csv('predictions_lesson1.csv', index=False)
print("\n💾 Results saved to predictions_lesson1.csv")
```

### 理解を深める

**このコードで何が起きているか**:

1. **データ読み込み**: CSVファイルからデータを読み込み
2. **自動最適化**: Optunaが10回の試行で最適なパラメータを探索
3. **予測**: 最適化されたモデルで7日先を予測
4. **結果保存**: 予測結果をCSVに保存

**主要パラメータ**:
- `model_name`: 使用するモデル（NHITS, TFT, DLinearなど）
- `h`: 予測ホライゾン（何ステップ先を予測するか）
- `num_samples`: 試行回数（多いほど精度向上、時間増）

### 演習

1. `num_samples`を5, 10, 20に変更して実行時間と精度の違いを確認
2. `h`を3, 7, 14に変更して異なる予測期間を試す
3. 自分のデータでこのコードを実行

---

## レッスン2: データの準備と検証

**目標**: データの品質を確保し、問題を早期発見する

### ステップ1: データの検証

```python
# lesson2_data_validation.py
import pandas as pd
from validation import DataValidator, print_validation_results

# データ読み込み
df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# データ検証
print("🔍 Validating dataset...")
validator = DataValidator()
result = validator.validate_dataset(df)

# 検証結果の表示
print_validation_results(result)

if result.is_valid:
    print("\n✅ Dataset is valid!")
else:
    print("\n❌ Dataset has issues:")
    for error in result.errors:
        print(f"  - {error}")

# 予測ホライゾンの検証
h = 7
horizon_result = validator.validate_forecast_horizon(df, h)
print_validation_results(horizon_result)
```

### ステップ2: データ品質の分析

```python
# lesson2_data_analysis.py
import pandas as pd
import numpy as np

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

print("📊 Data Quality Analysis\n")

# 1. 基本統計
print("=" * 50)
print("1. Basic Statistics")
print("=" * 50)
print(f"Total rows: {len(df)}")
print(f"Unique series: {df['unique_id'].nunique()}")
print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
print(f"Value range: {df['y'].min():.2f} to {df['y'].max():.2f}")

# 2. 欠損値チェック
print("\n" + "=" * 50)
print("2. Missing Values")
print("=" * 50)
missing = df.isnull().sum()
print(missing)

# 3. 各系列の統計
print("\n" + "=" * 50)
print("3. Per-Series Statistics")
print("=" * 50)
series_stats = df.groupby('unique_id').agg({
    'y': ['count', 'mean', 'std', 'min', 'max']
})
print(series_stats)

# 4. 時系列の連続性チェック
print("\n" + "=" * 50)
print("4. Time Series Continuity")
print("=" * 50)
for series_id in df['unique_id'].unique():
    series_df = df[df['unique_id'] == series_id].sort_values('ds')
    date_diffs = series_df['ds'].diff().dt.days.dropna()
    
    print(f"\n{series_id}:")
    print(f"  Expected frequency: 1 day")
    print(f"  Actual min: {date_diffs.min()} days")
    print(f"  Actual max: {date_diffs.max()} days")
    
    if date_diffs.std() > 0:
        print(f"  ⚠️  Warning: Irregular time intervals detected")

# 5. 外れ値検出
print("\n" + "=" * 50)
print("5. Outlier Detection")
print("=" * 50)
Q1 = df['y'].quantile(0.25)
Q3 = df['y'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['y'] < Q1 - 1.5*IQR) | (df['y'] > Q3 + 1.5*IQR)]
print(f"Outliers found: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

print("\n✅ Analysis complete!")
```

### ステップ3: データのクリーニング

```python
# lesson2_data_cleaning.py
import pandas as pd
import numpy as np

def clean_timeseries_data(df):
    """時系列データをクリーニング"""
    print("🧹 Cleaning data...")
    
    df_clean = df.copy()
    
    # 1. 欠損値の処理
    print("\n1. Handling missing values...")
    before = len(df_clean)
    df_clean = df_clean.dropna(subset=['unique_id', 'ds', 'y'])
    after = len(df_clean)
    print(f"  Removed {before - after} rows with missing values")
    
    # 2. 重複の削除
    print("\n2. Removing duplicates...")
    before = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['unique_id', 'ds'])
    after = len(df_clean)
    print(f"  Removed {before - after} duplicate rows")
    
    # 3. 日付の並び替え
    print("\n3. Sorting by date...")
    df_clean = df_clean.sort_values(['unique_id', 'ds'])
    
    # 4. インデックスのリセット
    df_clean = df_clean.reset_index(drop=True)
    
    print("\n✅ Cleaning complete!")
    return df_clean

# 実行
df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])
df_clean = clean_timeseries_data(df)
df_clean.to_csv('sample_data_cleaned.csv', index=False)
```

### 演習

1. 意図的に欠損値を入れて、検証がそれを検出することを確認
2. 異なる頻度のデータ（時間別、週別）を準備して検証
3. 自分のデータの品質を分析

---

## レッスン3: モデルの選択

**目標**: 適切なモデルを選択する方法を学ぶ

### ステップ1: モデルの特性を理解する

```python
# lesson3_model_characteristics.py
from model_characteristics import MODEL_CATALOG, ModelComplexity

print("📋 Available Models\n")
print("=" * 80)

for model_name, char in MODEL_CATALOG.items():
    print(f"\n🔹 {model_name}")
    print(f"   Complexity: {char.complexity.value}")
    print(f"   Recommended input_size: {char.recommended_input_size_range}")
    print(f"   Training time: ~{char.typical_training_time_minutes} minutes")
    print(f"   Memory footprint: ~{char.memory_footprint_mb} MB")
    print(f"   Supports exogenous: {char.supports_exogenous}")
    print(f"   Supports static: {char.supports_static}")

print("\n" + "=" * 80)
print("\n💡 Selection Guide:")
print("   Simple models (MLP): Fast, good for simple patterns")
print("   Moderate models (NHITS, DLinear): Balance of speed and accuracy")
print("   Complex models (TFT, Transformer): Best accuracy, slower training")
```

### ステップ2: データに基づいてモデルを選択

```python
# lesson3_model_selection.py
import pandas as pd
from search_algorithm_selector import DatasetSize, recommend_num_samples
from model_characteristics import MODEL_CATALOG, ModelComplexity

def select_model_for_data(df, h, time_budget_hours=1.0):
    """データセットに基づいて推奨モデルを選択"""
    
    n_rows = len(df)
    n_series = df['unique_id'].nunique()
    
    print("📊 Dataset Analysis")
    print(f"   Rows: {n_rows:,}")
    print(f"   Series: {n_series}")
    print(f"   Forecast horizon: {h}")
    print(f"   Time budget: {time_budget_hours} hours")
    
    # データサイズの判定
    if n_rows < 10000:
        dataset_size = DatasetSize.SMALL
        print(f"   Dataset size: SMALL")
    elif n_rows < 100000:
        dataset_size = DatasetSize.MEDIUM
        print(f"   Dataset size: MEDIUM")
    else:
        dataset_size = DatasetSize.LARGE
        print(f"   Dataset size: LARGE")
    
    # モデルの推奨
    print("\n🎯 Recommended Models:")
    
    if dataset_size == DatasetSize.SMALL:
        recommendations = [
            ("NHITS", "Good balance for small data"),
            ("NBEATS", "Interpretable, works well"),
            ("MLP", "Fast baseline")
        ]
    elif dataset_size == DatasetSize.MEDIUM:
        recommendations = [
            ("TFT", "Best for complex patterns"),
            ("TSMixer", "Modern architecture"),
            ("NHITS", "Reliable choice")
        ]
    else:  # LARGE
        recommendations = [
            ("DLinear", "Efficient for large data"),
            ("PatchTST", "State-of-the-art"),
            ("TSMixer", "Scalable")
        ]
    
    for model, reason in recommendations:
        char = MODEL_CATALOG[model]
        print(f"\n   {model}")
        print(f"      Reason: {reason}")
        print(f"      Training time: ~{char.typical_training_time_minutes}min")
        
        # 推奨試行回数を計算
        num_samples, _ = recommend_num_samples(
            model_complexity=char.complexity,
            dataset_size=dataset_size,
            time_budget_hours=time_budget_hours
        )
        print(f"      Recommended trials: {num_samples}")
    
    return recommendations[0][0]  # 最も推奨されるモデルを返す

# 実行
df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

recommended_model = select_model_for_data(df, h=7, time_budget_hours=1.0)
print(f"\n✅ Best choice: {recommended_model}")
```

### ステップ3: モデルの比較

```python
# lesson3_model_comparison.py
import pandas as pd
from auto_model_factory import create_auto_model
import time

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

models_to_test = ["MLP", "NHITS", "DLinear"]
results = {}

print("🔬 Comparing Models\n")

for model_name in models_to_test:
    print(f"Testing {model_name}...")
    start_time = time.time()
    
    try:
        auto_model = create_auto_model(
            model_name=model_name,
            h=7,
            dataset=df,
            backend="optuna",
            num_samples=10,  # 少なめで比較
            verbose=False
        )
        
        predictions = auto_model.predict(dataset=df)
        elapsed_time = time.time() - start_time
        
        results[model_name] = {
            'status': 'Success',
            'time_seconds': elapsed_time,
            'predictions': predictions
        }
        
        print(f"  ✅ Complete in {elapsed_time:.1f}s\n")
        
    except Exception as e:
        results[model_name] = {
            'status': 'Failed',
            'error': str(e)
        }
        print(f"  ❌ Failed: {e}\n")

# 結果のサマリー
print("\n📊 Comparison Summary")
print("=" * 60)
for model, result in results.items():
    if result['status'] == 'Success':
        print(f"{model:15s} ✅ {result['time_seconds']:6.1f}s")
    else:
        print(f"{model:15s} ❌ Failed")
```

### 演習

1. 異なるデータサイズで推奨モデルがどう変わるか確認
2. 3つのモデルを実際に比較して、速度と精度を評価
3. 複雑なモデル(TFT)と単純なモデル(MLP)の違いを体感

---

## レッスン4: ハイパーパラメータのカスタマイズ

**目標**: カスタム設定で最適化をコントロールする

### ステップ1: デフォルト設定の理解

```python
# lesson4_default_config.py
from ray import tune
from auto_model_factory import AutoModelFactory

# デフォルト設定を確認
factory = AutoModelFactory(model_name="NHITS", h=7)
default_config = factory._create_default_config()

print("🔧 Default Hyperparameter Configuration\n")
for param, value in default_config.items():
    print(f"{param:25s}: {value}")
```

### ステップ2: カスタム設定の作成

```python
# lesson4_custom_config.py
import pandas as pd
from auto_model_factory import create_auto_model
from ray import tune

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# カスタム探索空間の定義
custom_config = {
    # 学習関連
    'max_steps': tune.choice([500, 1000, 2000]),
    'learning_rate': tune.loguniform(1e-4, 1e-2),
    'batch_size': tune.choice([32, 64, 128]),
    
    # アーキテクチャ関連
    'input_size': tune.choice([7, 14, 28]),
    'hidden_size': tune.choice([256, 512]),
    
    # 正則化
    'dropout_prob_theta': tune.uniform(0.0, 0.5),
    
    # 早期停止
    'early_stop_patience_steps': 3
}

print("🎯 Custom Configuration:")
for param, value in custom_config.items():
    print(f"  {param}: {value}")

print("\n🔍 Starting optimization with custom config...")

auto_model = create_auto_model(
    model_name="NHITS",
    h=7,
    dataset=df,
    config=custom_config,  # カスタム設定を使用
    backend="optuna",
    num_samples=20,
    verbose=True
)

predictions = auto_model.predict(dataset=df)
print("\n✅ Optimization complete!")
```

### ステップ3: 探索空間の設計

```python
# lesson4_search_space_design.py
from ray import tune

def create_narrow_search_space():
    """狭い探索空間: 素早く収束"""
    return {
        'max_steps': tune.choice([1000]),  # 固定
        'learning_rate': tune.loguniform(5e-4, 2e-3),  # 狭い範囲
        'batch_size': tune.choice([64, 128]),  # 少ない選択肢
        'input_size': tune.choice([14])  # 固定
    }

def create_wide_search_space():
    """広い探索空間: より良い解を探索"""
    return {
        'max_steps': tune.choice([500, 1000, 2000, 3000]),
        'learning_rate': tune.loguniform(1e-5, 1e-2),  # 広い範囲
        'batch_size': tune.choice([16, 32, 64, 128, 256]),
        'input_size': tune.choice([7, 14, 28, 56]),
        'hidden_size': tune.choice([128, 256, 512, 1024])
    }

def create_focused_search_space():
    """集中的な探索空間: 重要なパラメータに焦点"""
    return {
        'max_steps': 1000,  # 固定
        'learning_rate': tune.loguniform(1e-4, 1e-2),  # 最重要
        'batch_size': tune.choice([64, 128]),
        'input_size': tune.choice([14, 28]),  # やや重要
        'hidden_size': 512  # 固定
    }

# 使用例
print("📐 Search Space Examples\n")

print("1. Narrow (Fast):")
narrow = create_narrow_search_space()
combinations_narrow = 1 * 10 * 2 * 1  # 大まかな組み合わせ数
print(f"   Approximate combinations: {combinations_narrow}")

print("\n2. Wide (Thorough):")
wide = create_wide_search_space()
combinations_wide = 4 * 20 * 5 * 4 * 4
print(f"   Approximate combinations: {combinations_wide}")

print("\n3. Focused (Balanced):")
focused = create_focused_search_space()
combinations_focused = 1 * 15 * 2 * 2 * 1
print(f"   Approximate combinations: {combinations_focused}")

print("\n💡 Recommendation:")
print("   - Time limited? Use Narrow")
print("   - Best accuracy? Use Wide")
print("   - Balanced? Use Focused")
```

### ステップ4: パラメータの影響を理解する

```python
# lesson4_parameter_impact.py
import pandas as pd
from auto_model_factory import create_auto_model
from ray import tune
import time

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# 異なる learning_rate で比較
learning_rates = [1e-4, 1e-3, 1e-2]
results = {}

print("🔬 Testing different learning rates\n")

for lr in learning_rates:
    print(f"Testing lr={lr}...")
    
    config = {
        'learning_rate': lr,  # 固定値でテスト
        'max_steps': 500,
        'batch_size': 64
    }
    
    start_time = time.time()
    
    auto_model = create_auto_model(
        model_name="NHITS",
        h=7,
        dataset=df,
        config=config,
        backend="optuna",
        num_samples=3,  # 少数の試行
        verbose=False
    )
    
    elapsed = time.time() - start_time
    results[lr] = {'time': elapsed}
    
    print(f"  Complete in {elapsed:.1f}s")

print("\n📊 Results:")
for lr, result in results.items():
    print(f"  lr={lr}: {result['time']:.1f}s")
```

### 演習

1. 探索空間を段階的に広げて、収束時間の違いを観察
2. 最も影響の大きいパラメータを特定
3. 自分のタスクに最適な探索空間を設計

---

## レッスン5: MLflowでの実験管理

**目標**: MLflowを使って実験を追跡・管理する

### ステップ1: MLflowのセットアップ

```bash
# MLflowサーバーの起動
mlflow ui --host 0.0.0.0 --port 5000
```

ブラウザで http://localhost:5000 を開く

### ステップ2: 基本的な実験追跡

```python
# lesson5_mlflow_basic.py
import pandas as pd
from auto_model_factory import create_auto_model
import mlflow

# MLflowの設定
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("lesson5_basic")

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

print("📊 Starting experiment with MLflow tracking...")

# MLflowを有効にして実行
auto_model = create_auto_model(
    model_name="NHITS",
    h=7,
    dataset=df,
    backend="optuna",
    num_samples=20,
    use_mlflow=True,  # MLflow有効化
    mlflow_experiment_name="lesson5_basic",
    verbose=True
)

predictions = auto_model.predict(dataset=df)

print("\n✅ Experiment complete!")
print("📊 View results at http://localhost:5000")
```

### ステップ3: カスタムメトリクスの記録

```python
# lesson5_custom_metrics.py
import pandas as pd
from auto_model_factory import create_auto_model
import mlflow
import numpy as np

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("lesson5_custom_metrics")

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# データセット情報を計算
dataset_info = {
    'n_rows': len(df),
    'n_series': df['unique_id'].nunique(),
    'date_range_days': (df['ds'].max() - df['ds'].min()).days,
    'mean_value': df['y'].mean(),
    'std_value': df['y'].std()
}

print("📊 Dataset Information:")
for key, value in dataset_info.items():
    print(f"  {key}: {value}")

# 実験を実行
with mlflow.start_run(run_name="custom_metrics_run"):
    # データセット情報を記録
    mlflow.log_params(dataset_info)
    
    # 最適化実行
    auto_model = create_auto_model(
        model_name="NHITS",
        h=7,
        dataset=df,
        backend="optuna",
        num_samples=20,
        use_mlflow=False,  # 手動でMLflow管理
        verbose=False
    )
    
    predictions = auto_model.predict(dataset=df)
    
    # カスタムメトリクスを計算
    pred_mean = predictions['NHITS'].mean()
    pred_std = predictions['NHITS'].std()
    
    mlflow.log_metrics({
        'prediction_mean': pred_mean,
        'prediction_std': pred_std,
        'prediction_range': predictions['NHITS'].max() - predictions['NHITS'].min()
    })
    
    # 予測結果を保存
    predictions.to_csv('predictions_custom.csv', index=False)
    mlflow.log_artifact('predictions_custom.csv')
    
    print("\n✅ Custom metrics logged to MLflow!")
```

### ステップ4: 複数実験の比較

```python
# lesson5_compare_experiments.py
import pandas as pd
from auto_model_factory import create_auto_model
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("lesson5_comparison")

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# 異なる設定で3つの実験
configurations = [
    {"name": "fast", "num_samples": 10, "model": "MLP"},
    {"name": "balanced", "num_samples": 20, "model": "NHITS"},
    {"name": "accurate", "num_samples": 30, "model": "TFT"}
]

print("🔬 Running multiple experiments...\n")

for config in configurations:
    print(f"Running: {config['name']}")
    
    with mlflow.start_run(run_name=config['name']):
        # 設定を記録
        mlflow.log_params(config)
        
        # 最適化実行
        auto_model = create_auto_model(
            model_name=config['model'],
            h=7,
            dataset=df,
            backend="optuna",
            num_samples=config['num_samples'],
            use_mlflow=False,
            verbose=False
        )
        
        predictions = auto_model.predict(dataset=df)
        
        # メトリクスを記録
        mlflow.log_metric("mean_prediction", predictions[config['model']].mean())
        
        print(f"  ✅ {config['name']} complete\n")

print("📊 Compare results at http://localhost:5000")
print("   Navigate to the 'lesson5_comparison' experiment")
print("   Select runs and click 'Compare'")
```

### ステップ5: 実験結果の分析

```python
# lesson5_analyze_results.py
import mlflow
import pandas as pd

mlflow.set_tracking_uri("http://localhost:5000")

# 実験の取得
experiment = mlflow.get_experiment_by_name("lesson5_comparison")

if experiment:
    # 実験のすべてのrunを取得
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"]
    )
    
    print("📊 Experiment Results Analysis\n")
    print("=" * 80)
    
    # 基本情報の表示
    print(f"Experiment: {experiment.name}")
    print(f"Total runs: {len(runs)}")
    print(f"Experiment ID: {experiment.experiment_id}")
    
    # runの詳細
    print("\n" + "=" * 80)
    print("Run Details:")
    print("=" * 80)
    
    for idx, run in runs.iterrows():
        print(f"\nRun: {run['tags.mlflow.runName']}")
        print(f"  Status: {run['status']}")
        print(f"  Duration: {run['end_time'] - run['start_time']}")
        print(f"  Parameters:")
        for col in runs.columns:
            if col.startswith('params.'):
                param_name = col.replace('params.', '')
                print(f"    {param_name}: {run[col]}")
        print(f"  Metrics:")
        for col in runs.columns:
            if col.startswith('metrics.'):
                metric_name = col.replace('metrics.', '')
                if pd.notna(run[col]):
                    print(f"    {metric_name}: {run[col]:.4f}")
    
    # ベストrunの特定
    print("\n" + "=" * 80)
    print("Best Run:")
    print("=" * 80)
    
    # mean_predictionが存在する場合
    if 'metrics.mean_prediction' in runs.columns:
        best_idx = runs['metrics.mean_prediction'].idxmax()
        best_run = runs.loc[best_idx]
        print(f"Run Name: {best_run['tags.mlflow.runName']}")
        print(f"Mean Prediction: {best_run['metrics.mean_prediction']:.4f}")

else:
    print("❌ Experiment not found. Run lesson5_compare_experiments.py first.")
```

### 演習

1. MLflow UIで実験結果を可視化
2. 複数のモデルを比較して、ベストモデルを特定
3. カスタムメトリクスを追加して、独自の評価基準を実装

---

## レッスン6: 高度な最適化

**目標**: 高度な機能を使いこなす

### ステップ1: ファクトリークラスの使用

```python
# lesson6_factory_class.py
import pandas as pd
from auto_model_factory import AutoModelFactory, OptimizationConfig

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# 詳細な最適化設定
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=None,  # 自動推奨
    cpus=4,
    gpus=1,
    use_mlflow=True,
    mlflow_tracking_uri="http://localhost:5000",
    mlflow_experiment_name="lesson6_advanced",
    use_pruning=True,  # 早期停止を有効化
    time_budget_hours=0.5,  # 30分の時間制限
    random_seed=42,
    verbose=True
)

print("🏭 Creating factory with advanced configuration...")
print(f"  Backend: {opt_config.backend}")
print(f"  Time budget: {opt_config.time_budget_hours} hours")
print(f"  Pruning enabled: {opt_config.use_pruning}")

# ファクトリー作成
factory = AutoModelFactory(
    model_name="TFT",
    h=7,
    optimization_config=opt_config
)

# 最適化実行
print("\n🔍 Starting optimization...")
auto_model = factory.create_auto_model(dataset=df)

# 最適化履歴の確認
print("\n📊 Optimization Summary:")
summary = factory.get_optimization_summary()
for key, value in summary.items():
    print(f"  {key}: {value}")

predictions = auto_model.predict(dataset=df)
print("\n✅ Advanced optimization complete!")
```

### ステップ2: カスタム損失関数の使用

```python
# lesson6_custom_loss.py
import pandas as pd
from auto_model_factory import create_auto_model
from neuralforecast.losses.pytorch import MQLoss, MAE, MSE

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# 異なる損失関数で比較
loss_functions = {
    'MAE': MAE(),
    'MSE': MSE(),
    'MQ_90': MQLoss(level=[90])  # 90%信頼区間
}

results = {}

print("🔬 Testing different loss functions...\n")

for loss_name, loss_fn in loss_functions.items():
    print(f"Testing {loss_name}...")
    
    auto_model = create_auto_model(
        model_name="NHITS",
        h=7,
        dataset=df,
        loss=loss_fn,  # カスタム損失関数
        backend="optuna",
        num_samples=15,
        verbose=False
    )
    
    predictions = auto_model.predict(dataset=df)
    results[loss_name] = predictions
    
    print(f"  ✅ Complete\n")

print("📊 Results:")
for loss_name, preds in results.items():
    mean_pred = preds['NHITS'].mean()
    print(f"  {loss_name:10s}: mean={mean_pred:.2f}")
```

### ステップ3: 並列実行の最適化

```python
# lesson6_parallel_optimization.py
import pandas as pd
from auto_model_factory import create_auto_model
from ray import tune
import torch

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# システムリソースの確認
n_cpus = 8  # 利用可能なCPU数に応じて調整
n_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 0

print(f"💻 System Resources:")
print(f"  CPUs: {n_cpus}")
print(f"  GPUs: {n_gpus}")

# 並列実行設定
config = {
    'max_steps': tune.choice([500, 1000, 2000]),
    'learning_rate': tune.loguniform(1e-4, 1e-2),
    'batch_size': tune.choice([64, 128, 256])
}

print(f"\n🚀 Running parallel optimization...")
print(f"  Parallel trials: {min(n_cpus // 2, 4)}")

auto_model = create_auto_model(
    model_name="NHITS",
    h=7,
    dataset=df,
    config=config,
    backend="ray",  # Ray Tuneは並列実行に優れている
    num_samples=40,
    cpus=n_cpus,
    gpus=n_gpus,
    verbose=True
)

predictions = auto_model.predict(dataset=df)
print("\n✅ Parallel optimization complete!")
```

### ステップ4: 探索アルゴリズムの選択

```python
# lesson6_algorithm_selection.py
import pandas as pd
from auto_model_factory import AutoModelFactory, OptimizationConfig
from search_algorithm_selector import (
    SearchAlgorithmSelector,
    ModelComplexity,
    DatasetSize
)

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

# データセット分析
n_rows = len(df)
if n_rows < 10000:
    dataset_size = DatasetSize.SMALL
elif n_rows < 100000:
    dataset_size = DatasetSize.MEDIUM
else:
    dataset_size = DatasetSize.LARGE

print(f"📊 Dataset size: {dataset_size.value} ({n_rows} rows)")

# モデル複雑度
model_complexity = ModelComplexity.COMPLEX  # TFTを想定

# アルゴリズム選択
selector = SearchAlgorithmSelector(backend="optuna")
strategy = selector.select_algorithm(
    model_complexity=model_complexity,
    dataset_size=dataset_size,
    num_samples=50,
    use_pruning=True
)

print(f"\n🎯 Selected Algorithm:")
print(f"  Name: {strategy.algorithm_name}")
print(f"  Description: {strategy.description}")
print(f"  Reason: {strategy.reason}")

# サンプラーとプルーナーを取得
sampler = selector.get_optuna_sampler(strategy)
pruner = selector.get_optuna_pruner(strategy)

print(f"\n⚙️ Configuration:")
print(f"  Sampler: {type(sampler).__name__}")
print(f"  Pruner: {type(pruner).__name__ if pruner else 'None'}")

# 最適化実行
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=50,
    use_pruning=True,
    verbose=True
)

factory = AutoModelFactory(
    model_name="TFT",
    h=7,
    optimization_config=opt_config
)

auto_model = factory.create_auto_model(dataset=df)
print("\n✅ Optimization with selected algorithm complete!")
```

### 演習

1. 時間制限を設定して、制限内での最適化を体験
2. 異なる損失関数で予測結果がどう変わるか観察
3. 並列実行の効果を測定（実行時間の比較）

---

## レッスン7: 本番環境への展開

**目標**: 本番環境で使用するためのベストプラクティスを学ぶ

### ステップ1: 堅牢な検証パイプライン

```python
# lesson7_production_pipeline.py
import pandas as pd
from auto_model_factory import create_auto_model
from validation import validate_all, print_validation_results
import mlflow
import logging
from datetime import datetime

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'forecast_{datetime.now():%Y%m%d_%H%M%S}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def production_forecast_pipeline(data_path, model_name, h, num_samples):
    """本番環境用の予測パイプライン"""
    
    logger.info("=" * 80)
    logger.info("PRODUCTION FORECAST PIPELINE STARTED")
    logger.info("=" * 80)
    
    try:
        # 1. データ読み込み
        logger.info("Step 1: Loading data...")
        df = pd.read_csv(data_path)
        df['ds'] = pd.to_datetime(df['ds'])
        logger.info(f"  Loaded {len(df)} rows, {df['unique_id'].nunique()} series")
        
        # 2. 包括的な検証
        logger.info("\nStep 2: Validating configuration...")
        validation_results = validate_all(
            backend="optuna",
            config=None,
            num_samples=num_samples,
            cpus=4,
            gpus=1,
            model_class_name=model_name,
            dataset=df,
            h=h,
            strict_mode=True  # 本番環境では厳格モード
        )
        
        if not validation_results['overall_valid']:
            logger.error("❌ Validation failed!")
            for category, result in validation_results.items():
                if isinstance(result, dict) and not result.get('is_valid', True):
                    logger.error(f"  {category}: {result.get('errors', [])}")
            return None
        
        logger.info("  ✅ All validations passed")
        
        # 3. MLflow設定
        logger.info("\nStep 3: Setting up MLflow...")
        mlflow.set_tracking_uri("http://localhost:5000")
        experiment_name = f"production_{model_name}_{datetime.now():%Y%m%d}"
        mlflow.set_experiment(experiment_name)
        logger.info(f"  Experiment: {experiment_name}")
        
        # 4. 最適化実行
        logger.info("\nStep 4: Running optimization...")
        with mlflow.start_run(run_name=f"forecast_{datetime.now():%H%M%S}"):
            # メタデータを記録
            mlflow.log_params({
                'model_name': model_name,
                'forecast_horizon': h,
                'num_samples': num_samples,
                'data_rows': len(df),
                'n_series': df['unique_id'].nunique()
            })
            
            auto_model = create_auto_model(
                model_name=model_name,
                h=h,
                dataset=df,
                backend="optuna",
                num_samples=num_samples,
                use_mlflow=True,
                verbose=False
            )
            
            logger.info("  ✅ Optimization complete")
            
            # 5. 予測実行
            logger.info("\nStep 5: Generating predictions...")
            predictions = auto_model.predict(dataset=df)
            
            # 6. 結果保存
            output_file = f'predictions_{model_name}_{datetime.now():%Y%m%d_%H%M%S}.csv'
            predictions.to_csv(output_file, index=False)
            mlflow.log_artifact(output_file)
            logger.info(f"  Saved to {output_file}")
            
            # 7. 予測統計
            pred_stats = {
                'mean': predictions[model_name].mean(),
                'std': predictions[model_name].std(),
                'min': predictions[model_name].min(),
                'max': predictions[model_name].max()
            }
            mlflow.log_metrics(pred_stats)
            
            logger.info("\nPrediction Statistics:")
            for key, value in pred_stats.items():
                logger.info(f"  {key}: {value:.2f}")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
        return predictions
        
    except Exception as e:
        logger.error(f"\n❌ Pipeline failed: {e}", exc_info=True)
        return None

# 実行
if __name__ == "__main__":
    predictions = production_forecast_pipeline(
        data_path='sample_data.csv',
        model_name='NHITS',
        h=7,
        num_samples=30
    )
    
    if predictions is not None:
        print("\n✅ Production pipeline successful!")
    else:
        print("\n❌ Production pipeline failed!")
```

### ステップ2: モデルのバージョニング

```python
# lesson7_model_versioning.py
import pandas as pd
from auto_model_factory import create_auto_model
import mlflow
import pickle
from datetime import datetime
import json

def save_model_version(auto_model, metadata, version_dir='models'):
    """モデルをバージョン管理して保存"""
    import os
    os.makedirs(version_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    version_name = f"v_{timestamp}"
    version_path = os.path.join(version_dir, version_name)
    os.makedirs(version_path, exist_ok=True)
    
    # モデル保存
    model_file = os.path.join(version_path, 'model.pkl')
    with open(model_file, 'wb') as f:
        pickle.dump(auto_model, f)
    
    # メタデータ保存
    metadata['version'] = version_name
    metadata['timestamp'] = timestamp
    metadata_file = os.path.join(version_path, 'metadata.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Model saved as version: {version_name}")
    print(f"   Location: {version_path}")
    
    return version_name, version_path

# モデル作成
df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

print("🔧 Creating and versioning model...\n")

auto_model = create_auto_model(
    model_name="NHITS",
    h=7,
    dataset=df,
    backend="optuna",
    num_samples=20,
    verbose=False
)

# メタデータ
metadata = {
    'model_name': 'NHITS',
    'forecast_horizon': 7,
    'num_samples': 20,
    'backend': 'optuna',
    'training_data_rows': len(df),
    'n_series': df['unique_id'].nunique()
}

# バージョン保存
version_name, version_path = save_model_version(auto_model, metadata)

print(f"\n📦 Model Version Info:")
with open(f'{version_path}/metadata.json', 'r') as f:
    metadata = json.load(f)
    for key, value in metadata.items():
        print(f"  {key}: {value}")
```

### ステップ3: エラーハンドリングとリカバリー

```python
# lesson7_error_handling.py
import pandas as pd
from auto_model_factory import create_auto_model
import mlflow
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ForecastError(Exception):
    """予測エラーのカスタム例外"""
    pass

def robust_forecast(
    df: pd.DataFrame,
    model_name: str,
    h: int,
    num_samples: int,
    fallback_model: Optional[str] = "MLP"
) -> pd.DataFrame:
    """
    エラーハンドリングとフォールバック機能を持つ予測
    
    Args:
        df: データセット
        model_name: 主要モデル名
        h: 予測ホライゾン
        num_samples: 試行回数
        fallback_model: フォールバックモデル名
    
    Returns:
        予測結果
    """
    
    # 試行1: メインモデル
    try:
        logger.info(f"Attempting forecast with {model_name}...")
        
        auto_model = create_auto_model(
            model_name=model_name,
            h=h,
            dataset=df,
            backend="optuna",
            num_samples=num_samples,
            verbose=False
        )
        
        predictions = auto_model.predict(dataset=df)
        logger.info(f"✅ Forecast successful with {model_name}")
        return predictions
        
    except Exception as e:
        logger.warning(f"⚠️ {model_name} failed: {e}")
        
        # 試行2: フォールバックモデル
        if fallback_model:
            try:
                logger.info(f"Trying fallback model {fallback_model}...")
                
                auto_model = create_auto_model(
                    model_name=fallback_model,
                    h=h,
                    dataset=df,
                    backend="optuna",
                    num_samples=max(10, num_samples // 2),  # 半分の試行回数
                    verbose=False
                )
                
                predictions = auto_model.predict(dataset=df)
                logger.info(f"✅ Forecast successful with fallback {fallback_model}")
                return predictions
                
            except Exception as e2:
                logger.error(f"❌ Fallback {fallback_model} also failed: {e2}")
                raise ForecastError(f"Both {model_name} and {fallback_model} failed")
        else:
            raise ForecastError(f"{model_name} failed and no fallback specified")

# 使用例
logging.basicConfig(level=logging.INFO)

df = pd.read_csv('sample_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

print("🛡️ Testing robust forecast with error handling...\n")

try:
    predictions = robust_forecast(
        df=df,
        model_name="TFT",  # 複雑なモデル（失敗する可能性あり）
        h=7,
        num_samples=20,
        fallback_model="NHITS"  # フォールバック
    )
    print("\n✅ Forecast completed successfully!")
    print(predictions.head())
    
except ForecastError as e:
    print(f"\n❌ Forecast failed: {e}")
```

### ステップ4: 定期実行スクリプト

```python
# lesson7_scheduled_forecast.py
import pandas as pd
from auto_model_factory import create_auto_model
import mlflow
from datetime import datetime, timedelta
import logging
import schedule
import time

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def daily_forecast_job():
    """毎日実行される予測ジョブ"""
    
    logger.info("=" * 80)
    logger.info(f"DAILY FORECAST JOB STARTED: {datetime.now()}")
    logger.info("=" * 80)
    
    try:
        # 1. 最新データの読み込み
        df = pd.read_csv('sample_data.csv')
        df['ds'] = pd.to_datetime(df['ds'])
        
        # 過去30日間のデータを使用
        cutoff_date = datetime.now() - timedelta(days=30)
        df = df[df['ds'] >= cutoff_date]
        
        logger.info(f"Using data from {cutoff_date.date()} onwards")
        logger.info(f"Total rows: {len(df)}")
        
        # 2. 予測実行
        mlflow.set_experiment("daily_forecast")
        
        with mlflow.start_run(run_name=f"daily_{datetime.now():%Y%m%d}"):
            auto_model = create_auto_model(
                model_name="NHITS",
                h=7,
                dataset=df,
                backend="optuna",
                num_samples=20,
                use_mlflow=True,
                verbose=False
            )
            
            predictions = auto_model.predict(dataset=df)
            
            # 3. 結果保存
            output_file = f'daily_forecast_{datetime.now():%Y%m%d}.csv'
            predictions.to_csv(output_file, index=False)
            mlflow.log_artifact(output_file)
            
            logger.info(f"Forecast saved to {output_file}")
        
        logger.info("✅ Daily forecast job completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Daily forecast job failed: {e}", exc_info=True)
    
    logger.info("=" * 80 + "\n")

# スケジュール設定
def setup_scheduler():
    """定期実行のスケジュール設定"""
    
    # 毎日午前2時に実行
    schedule.every().day.at("02:00").do(daily_forecast_job)
    
    # テスト用: 1分ごとに実行（本番では削除）
    # schedule.every(1).minutes.do(daily_forecast_job)
    
    logger.info("📅 Scheduler configured:")
    logger.info("  Daily forecast at 02:00")
    
    # スケジューラーのループ
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1分ごとにチェック

if __name__ == "__main__":
    print("🕐 Starting forecast scheduler...")
    print("   Press Ctrl+C to stop")
    
    try:
        # 初回実行（テスト用）
        print("\n🧪 Running initial test forecast...")
        daily_forecast_job()
        
        # スケジューラー起動
        # setup_scheduler()  # 本番環境では有効化
        
    except KeyboardInterrupt:
        print("\n⏹️ Scheduler stopped by user")
```

### 演習

1. 本番環境パイプラインを実行して、すべての段階を確認
2. 意図的にエラーを発生させて、エラーハンドリングをテスト
3. モデルバージョニングシステムを使って複数バージョンを管理

---

## 💡 ベストプラクティス総まとめ

### 1. 開発フェーズ

```python
# 開発時は少ない試行回数で素早く反復
auto_model = create_auto_model(
    model_name="NHITS",
    h=7,
    dataset=df,
    num_samples=5,  # 少なめ
    verbose=True    # 詳細出力
)
```

### 2. 実験フェーズ

```python
# 複数設定を試して最適な組み合わせを探索
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=50,
    use_mlflow=True,
    mlflow_experiment_name="experiment_phase"
)
```

### 3. 本番フェーズ

```python
# 堅牢性と再現性を重視
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=30,
    use_mlflow=True,
    use_pruning=True,
    random_seed=42,  # 再現性
    strict_mode=True
)
```

---

## 🎓 次のステップ

チュートリアルを完了したら:

1. **[API_REFERENCE.md](./API_REFERENCE.md)** で詳細なAPIを確認
2. **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** でよくある問題の解決方法を学習
3. **自分のプロジェクト** で実際に使用

---

## ❓ よくある質問（FAQ）

### Q1: 最初に試すべきモデルは？

**A**: データサイズが小〜中規模なら**NHITS**、大規模なら**DLinear**から始めることをお勧めします。

### Q2: num_samplesはいくつにすべき？

**A**: 
- クイックテスト: 5-10
- 通常の最適化: 20-50
- 徹底的な最適化: 50-100

### Q3: GPUは必須？

**A**: 必須ではありませんが、大幅に高速化されます。特に複雑なモデル（TFT、Transformerなど）ではGPU使用を推奨します。

### Q4: エラーが出たらどうすれば？

**A**: 以下の順で確認してください：
1. エラーメッセージを確認
2. [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)で該当する問題を探す
3. 検証機能を使って問題を特定

### Q5: どのバックエンドを使うべき？

**A**:
- **Optuna**: 一般的な使用、使いやすい
- **Ray Tune**: 並列実行、大規模な実験

---

## 🎉 おめでとうございます！

チュートリアルを完了しました！これで自動モデルファクトリーシステムを使いこなせるようになりました。

**次のアクション**:
1. 自分のデータで試す
2. より高度な機能を探索
3. コミュニティに貢献

**Happy Forecasting! 🚀📈**
