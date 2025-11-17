# 設計概要：自動モデルファクトリーシステム

## 1. アーキテクチャ概要

```
┌─────────────────────────────────────────────────────────────┐
│                   AutoModelFactory                           │
│                  (auto_model_factory.py)                     │
│  - 統合管理                                                    │
│  - MLflow連携                                                 │
│  - 最適化フロー制御                                            │
└───────────┬─────────────────┬───────────────────────────────┘
            │                 │
            ▼                 ▼
┌───────────────────┐  ┌──────────────────────────────────┐
│   Validation      │  │  SearchAlgorithmSelector         │
│  (validation.py)  │  │  (search_algorithm_selector.py)  │
│                   │  │                                  │
│ - 設定検証        │  │ - アルゴリズム選択               │
│ - 環境検証        │  │ - サンプラー/プルーナー生成      │
│ - データ検証      │  │ - 試行回数推奨                   │
└───────────────────┘  └──────────────────────────────────┘
```

## 2. 各モジュールの役割

### 2.1 validation.py - 設定検証モジュール

**目的**: システムの安全性と信頼性を確保するための包括的な検証

**主要クラス**:

#### `ConfigValidator`
- バックエンド設定の検証（Ray/Optuna）
- モデル設定の検証
- MLflow設定の検証
- 実行環境の検証（GPU、メモリ、ディスク容量）

**検証項目**:
```python
# バックエンド検証
- サポートされているバックエンドか
- num_samples、cpus、gpusの妥当性
- GPU利用可能性

# モデル設定検証
- max_steps、learning_rate、batch_sizeの範囲
- val_check_stepsとmax_stepsの整合性
- early_stop_patience_stepsの妥当性

# 環境検証
- PyTorch、CUDA、必要ライブラリのインストール確認
- 利用可能メモリ、ディスク容量のチェック

# MLflow検証
- トラッキングURIの接続性
- 実験名の妥当性
```

#### `DataValidator`
- データセットの構造検証
- 必須カラムの存在確認
- 予測ホライゾンの妥当性検証

**使用例**:
```python
from validation import ConfigValidator, DataValidator

# 設定検証
validator = ConfigValidator(strict_mode=False)
result = validator.validate_backend_config(
    backend="optuna",
    config=my_config,
    num_samples=50,
    cpus=4,
    gpus=1
)

if not result.is_valid:
    print("Errors:", result.errors)
    print("Warnings:", result.warnings)

# データ検証
data_validator = DataValidator()
dataset_result = data_validator.validate_dataset(df)
```

**返り値**: `ValidationResult`
```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    corrected_config: Optional[Dict[str, Any]]
```

---

### 2.2 search_algorithm_selector.py - 探索アルゴリズム選択モジュール

**目的**: モデル特性とデータセット特性に基づいて最適な探索アルゴリズムを自動選択

**主要クラス**:

#### `SearchAlgorithmSelector`
モデルの複雑度、データセットサイズ、探索空間の複雑度に基づいて最適なアルゴリズムを選択

**選択ロジック**:

| 条件 | Optunaアルゴリズム | Ray Tuneアルゴリズム |
|------|-------------------|---------------------|
| 試行数 < 10 | RandomSampler | BasicVariantGenerator |
| 小規模探索空間 | GridSampler | BasicVariantGenerator |
| 大規模データ + 複雑モデル | TPESampler (multivariate) | OptunaSearch with TPE |
| 中規模データ | TPESampler / CmaEsSampler | BayesOptSearch |
| 小規模データ | RandomSampler | HyperOptSearch |

**プルーニング戦略**:

| 条件 | プルーナー | 設定 |
|------|-----------|------|
| 大規模データ + 複雑モデル | HyperbandPruner | min_resource=5, reduction_factor=3 |
| 中規模データ + 複雑モデル | MedianPruner | n_warmup_steps=10 |
| 小規模データ | MedianPruner (慎重) | n_warmup_steps=20 |

**使用例**:
```python
from search_algorithm_selector import (
    SearchAlgorithmSelector, 
    ModelComplexity, 
    DatasetSize
)

# セレクター作成
selector = SearchAlgorithmSelector(backend="optuna")

# アルゴリズム選択
strategy = selector.select_algorithm(
    model_complexity=ModelComplexity.COMPLEX,
    dataset_size=DatasetSize.LARGE,
    num_samples=100,
    config=my_config,
    use_pruning=True,
    random_seed=42
)

# Optunaのサンプラーとプルーナーを取得
sampler = selector.get_optuna_sampler(strategy)
pruner = selector.get_optuna_pruner(strategy)

print(f"Selected: {strategy.algorithm_name}")
print(f"Description: {strategy.description}")
```

**試行回数推奨機能**:
```python
from search_algorithm_selector import recommend_num_samples

num_samples, explanation = recommend_num_samples(
    model_complexity=ModelComplexity.COMPLEX,
    dataset_size=DatasetSize.MEDIUM,
    search_complexity=SearchComplexity.HIGH,
    time_budget_hours=2.0
)
print(f"{explanation}")
# Output: "Recommended 50 trials based on model complexity..."
```

---

### 2.3 auto_model_factory.py - メインファクトリー

**目的**: 全てのコンポーネントを統合し、自動最適化を実行

**主要クラス**:

#### `AutoModelFactory`
NeuralForecastモデルの自動ハイパーパラメータ最適化を統合管理

**最適化フロー**:
```
1. 検証 (Validation)
   └→ ConfigValidator, DataValidator使用
   
2. データセット分析 (Dataset Analysis)
   └→ サイズ、系列数、外生変数の有無を分析
   
3. 探索戦略選択 (Search Strategy Selection)
   └→ SearchAlgorithmSelector使用
   └→ 試行回数の自動推奨
   
4. ハイパーパラメータ設定 (Hyperparameter Configuration)
   └→ デフォルト設定の生成
   └→ モデル固有パラメータの追加
   
5. モデル作成と最適化 (Model Creation and Optimization)
   └→ NeuralForecast Autoモデル作成
   └→ MLflowでの実験追跡
   └→ 学習実行
```

**使用例**:

**方法1: ファクトリークラスを使用**
```python
from auto_model_factory import AutoModelFactory, OptimizationConfig
import pandas as pd

# データ準備
df = pd.read_csv('timeseries.csv')

# 最適化設定
config = OptimizationConfig(
    backend="optuna",
    num_samples=None,  # 自動推奨
    cpus=8,
    gpus=1,
    use_mlflow=True,
    mlflow_experiment_name="my_experiment",
    use_pruning=True,
    verbose=True
)

# ファクトリー作成
factory = AutoModelFactory(
    model_name="NHITS",
    h=24,  # 24時間先予測
    optimization_config=config
)

# 最適化実行
auto_model = factory.create_auto_model(
    dataset=df,
    config=None,  # デフォルト設定を使用
    loss=None
)

# 予測
predictions = auto_model.predict(dataset=df)

# 最適化履歴
summary = factory.get_optimization_summary()
print(summary)
```

**方法2: 便利関数を使用**
```python
from auto_model_factory import create_auto_model
import pandas as pd

df = pd.read_csv('timeseries.csv')

# シンプルな使用法
auto_model = create_auto_model(
    model_name="TFT",
    h=24,
    dataset=df,
    backend="optuna",
    num_samples=50,
    cpus=4,
    gpus=1,
    use_mlflow=True,
    verbose=True
)

predictions = auto_model.predict(dataset=df)
```

**カスタム設定を使用**:
```python
from ray import tune

# カスタムハイパーパラメータ探索空間
custom_config = {
    'max_steps': tune.choice([1000, 2000, 3000]),
    'learning_rate': tune.loguniform(1e-5, 1e-2),
    'batch_size': tune.choice([64, 128, 256]),
    'n_blocks': tune.choice([[2, 2, 2], [3, 3, 3]]),
    'hidden_size': tune.choice([128, 256, 512])
}

auto_model = create_auto_model(
    model_name="NHITS",
    h=24,
    dataset=df,
    config=custom_config,
    backend="optuna",
    num_samples=100
)
```

#### `ModelCharacteristics`
モデルの特性を定義するデータクラス

```python
@dataclass
class ModelCharacteristics:
    name: str
    complexity: ModelComplexity
    recommended_input_size_range: tuple
    supports_exogenous: bool
    supports_static: bool
    typical_training_time_minutes: float
    memory_footprint_mb: float
```

**モデルカタログ**:
```python
MODEL_CATALOG = {
    "MLP": ModelCharacteristics(
        complexity=ModelComplexity.SIMPLE,
        recommended_input_size_range=(7, 14),
        typical_training_time_minutes=5.0
    ),
    "NHITS": ModelCharacteristics(
        complexity=ModelComplexity.MODERATE,
        recommended_input_size_range=(14, 28),
        typical_training_time_minutes=10.0
    ),
    "TFT": ModelCharacteristics(
        complexity=ModelComplexity.COMPLEX,
        recommended_input_size_range=(24, 168),
        typical_training_time_minutes=30.0
    ),
    # ... その他のモデル
}
```

---

## 3. 統合使用例

### 3.1 基本的な使用例

```python
import pandas as pd
from auto_model_factory import create_auto_model

# データ読み込み
df = pd.read_csv('sales_data.csv')  # columns: unique_id, ds, y

# 自動最適化実行
model = create_auto_model(
    model_name="NHITS",
    h=7,  # 7日先予測
    dataset=df,
    backend="optuna",
    num_samples=30,
    use_mlflow=True,
    verbose=True
)

# 予測
forecast = model.predict(dataset=df)
print(forecast)
```

### 3.2 高度な使用例

```python
from auto_model_factory import AutoModelFactory, OptimizationConfig
from search_algorithm_selector import ModelComplexity, DatasetSize
from validation import validate_all
from ray import tune

# 1. 事前検証
df = pd.read_csv('timeseries.csv')
custom_config = {
    'max_steps': tune.choice([500, 1000, 2000]),
    'learning_rate': tune.loguniform(1e-4, 1e-2),
    'batch_size': tune.choice([32, 64, 128]),
}

validation_results = validate_all(
    backend="optuna",
    config=custom_config,
    num_samples=50,
    cpus=8,
    gpus=2,
    model_class_name="TFT",
    dataset=df,
    h=24,
    strict_mode=False
)

# 2. 最適化設定
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=None,  # 自動推奨
    cpus=8,
    gpus=2,
    use_mlflow=True,
    mlflow_tracking_uri="http://mlflow-server:5000",
    mlflow_experiment_name="production_forecast",
    use_pruning=True,
    time_budget_hours=3.0,
    random_seed=42,
    verbose=True
)

# 3. ファクトリー作成と実行
factory = AutoModelFactory(
    model_name="TFT",
    h=24,
    optimization_config=opt_config
)

# カスタム損失関数
from neuralforecast.losses.pytorch import MQLoss
loss = MQLoss(level=[90])

# 最適化実行
auto_model = factory.create_auto_model(
    dataset=df,
    config=custom_config,
    loss=loss
)

# 4. 予測と評価
predictions = auto_model.predict(dataset=df)

# 5. 最適化履歴の確認
history = factory.get_optimization_summary()
print(history)
```

### 3.3 複数モデルの比較

```python
from auto_model_factory import create_auto_model
import pandas as pd

df = pd.read_csv('data.csv')
models_to_compare = ["NHITS", "TFT", "DLinear"]
results = {}

for model_name in models_to_compare:
    print(f"\nOptimizing {model_name}...")
    
    auto_model = create_auto_model(
        model_name=model_name,
        h=24,
        dataset=df,
        backend="optuna",
        num_samples=30,
        mlflow_experiment_name=f"comparison_{model_name}",
        verbose=False
    )
    
    predictions = auto_model.predict(dataset=df)
    results[model_name] = predictions

# 結果の比較
for model_name, pred in results.items():
    print(f"{model_name} predictions: {pred.head()}")
```

---

## 4. エラーハンドリング

### 4.1 検証エラー

```python
from validation import ConfigValidator, ValidationResult

validator = ConfigValidator(strict_mode=True)
result = validator.validate_backend_config(...)

if not result.is_valid:
    print("Configuration errors detected:")
    for error in result.errors:
        print(f"  - {error}")
    
    if result.corrected_config:
        print("Suggested corrections:")
        print(result.corrected_config)
        # 修正後の設定で再試行
```

### 4.2 最適化の中断とリカバリー

```python
from auto_model_factory import AutoModelFactory
import mlflow

try:
    factory = AutoModelFactory(...)
    auto_model = factory.create_auto_model(...)
except KeyboardInterrupt:
    print("Optimization interrupted by user")
    # MLflowから部分的な結果を取得
    experiment = mlflow.get_experiment_by_name("my_experiment")
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    print("Completed trials:", len(runs))
except Exception as e:
    print(f"Error during optimization: {e}")
    # エラーログの確認
    if factory.config.use_mlflow:
        # MLflowから失敗したrunを確認
        pass
```

---

## 5. パフォーマンスチューニング

### 5.1 大規模データセット

```python
# メモリ効率を重視
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=30,  # 試行回数を抑える
    cpus=16,
    gpus=4,  # 複数GPU使用
    use_pruning=True  # 早期停止で時間節約
)

# バッチサイズを調整
custom_config = {
    'batch_size': tune.choice([256, 512, 1024]),  # 大きめ
    'max_steps': tune.choice([500, 1000]),  # 少なめ
    'early_stop_patience_steps': 2  # 早めに停止
}
```

### 5.2 小規模データセット

```python
# 精度を重視
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=100,  # 多めの試行
    use_pruning=False  # プルーニングを無効化
)

custom_config = {
    'batch_size': tune.choice([16, 32, 64]),  # 小さめ
    'max_steps': tune.choice([2000, 3000, 5000]),  # 長め
    'learning_rate': tune.loguniform(1e-5, 1e-3)  # より広範囲
}
```

---

## 6. ベストプラクティス

### 6.1 段階的アプローチ

```python
# ステップ1: 少ない試行回数で迅速にテスト
quick_test = create_auto_model(
    model_name="NHITS",
    h=24,
    dataset=df,
    num_samples=5,
    verbose=True
)

# ステップ2: 結果が良好なら本格的な最適化
full_optimization = create_auto_model(
    model_name="NHITS",
    h=24,
    dataset=df,
    num_samples=100,
    use_mlflow=True,
    mlflow_experiment_name="production"
)
```

### 6.2 設定の再利用

```python
# 良好な設定を保存
best_config = {
    'max_steps': 2000,
    'learning_rate': 0.001,
    'batch_size': 128,
    # ... 最良の設定
}

# 類似タスクで再利用
model1 = create_auto_model(..., config=best_config)
model2 = create_auto_model(..., config=best_config)
```

### 6.3 MLflowでの追跡

```python
import mlflow

# 実験の整理
mlflow.set_experiment("forecast_production_v1")

with mlflow.start_run(run_name="weekly_forecast"):
    auto_model = create_auto_model(...)
    
    # カスタムメトリクスの追加
    mlflow.log_metrics({
        'dataset_size': len(df),
        'n_series': df['unique_id'].nunique()
    })
```

---

## 7. トラブルシューティング

### 7.1 よくある問題

**問題**: OOM (Out of Memory) エラー
```python
# 解決策1: バッチサイズを減らす
config = {'batch_size': tune.choice([16, 32])}

# 解決策2: GPUを増やす
opt_config = OptimizationConfig(gpus=2)

# 解決策3: input_sizeを減らす
config = {'input_size': tune.choice([7, 14])}
```

**問題**: 最適化が収束しない
```python
# 解決策1: 試行回数を増やす
opt_config = OptimizationConfig(num_samples=200)

# 解決策2: 探索空間を狭める
config = {
    'learning_rate': tune.loguniform(1e-4, 1e-3),  # 狭い範囲
    'batch_size': tune.choice([64, 128])  # 選択肢を減らす
}

# 解決策3: より高度なアルゴリズムを使用
# SearchAlgorithmSelectorが自動選択
```

**問題**: MLflow接続エラー
```python
# トラッキングURIの確認
validation_result = validator.validate_mlflow_config(
    tracking_uri="http://localhost:5000"
)
if not validation_result.is_valid:
    print(validation_result.errors)
```

---

## 8. まとめ

この設計により、以下の利点が得られます:

1. **モジュール性**: 各コンポーネントが独立して動作
2. **柔軟性**: カスタマイズ可能な設定
3. **堅牢性**: 包括的な検証機能
4. **自動化**: 最適なアルゴリズムの自動選択
5. **追跡性**: MLflow統合による実験管理
6. **スケーラビリティ**: Ray/Optunaによる分散実行対応

これらのモジュールを組み合わせることで、初心者でも高度な自動最適化が可能になります。
