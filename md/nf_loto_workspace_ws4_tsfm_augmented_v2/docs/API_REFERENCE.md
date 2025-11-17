# 自動モデルファクトリー - APIリファレンス

## 📕 目次

- [概要](#概要)
- [auto_model_factory.py](#auto_model_factorypy)
  - [create_auto_model()](#create_auto_model)
  - [AutoModelFactory](#automodelfactory)
  - [OptimizationConfig](#optimizationconfig)
  - [ModelCharacteristics](#modelcharacteristics)
- [validation.py](#validationpy)
  - [ConfigValidator](#configvalidator)
  - [DataValidator](#datavalidator)
  - [ValidationResult](#validationresult)
- [search_algorithm_selector.py](#search_algorithm_selectorpy)
  - [SearchAlgorithmSelector](#searchalgorithmselector)
  - [SearchStrategy](#searchstrategy)
  - [recommend_num_samples()](#recommend_num_samples)
- [mlflow_integration.py](#mlflow_integrationpy)
- [logging_config.py](#logging_configpy)
- [データ型定義](#データ型定義)

---

## 概要

この APIリファレンスでは、自動モデルファクトリーシステムのすべての公開API を詳細に説明します。

**バージョン**: 1.0.0  
**最終更新**: 2025年11月12日

---

## auto_model_factory.py

メインファクトリーモジュール。自動ハイパーパラメータ最適化の統合管理を提供します。

### create_auto_model()

**概要**: 最も簡単に自動最適化モデルを作成する便利関数

#### シグネチャ

```python
def create_auto_model(
    model_name: str,
    h: int,
    dataset: pd.DataFrame,
    backend: str = "optuna",
    config: Optional[Dict[str, Any]] = None,
    loss: Optional[Any] = None,
    num_samples: Optional[int] = None,
    cpus: int = 4,
    gpus: int = 0,
    use_mlflow: bool = False,
    mlflow_tracking_uri: Optional[str] = None,
    mlflow_experiment_name: Optional[str] = None,
    use_pruning: bool = False,
    time_budget_hours: Optional[float] = None,
    random_seed: Optional[int] = None,
    verbose: bool = True
) -> Any:
```

#### パラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `model_name` | `str` | **必須** | NeuralForecastモデル名 (例: "NHITS", "TFT", "DLinear") |
| `h` | `int` | **必須** | 予測ホライゾン（何ステップ先を予測するか） |
| `dataset` | `pd.DataFrame` | **必須** | 時系列データ（必須カラム: unique_id, ds, y） |
| `backend` | `str` | `"optuna"` | 最適化バックエンド ("optuna" または "ray") |
| `config` | `Dict[str, Any]` | `None` | カスタムハイパーパラメータ探索空間。Noneの場合はデフォルト設定を使用 |
| `loss` | `Any` | `None` | カスタム損失関数。Noneの場合はモデルのデフォルトを使用 |
| `num_samples` | `int` | `None` | 試行回数。Noneの場合は自動推奨値を使用 |
| `cpus` | `int` | `4` | 使用するCPU数 |
| `gpus` | `int` | `0` | 使用するGPU数 |
| `use_mlflow` | `bool` | `False` | MLflowでの実験追跡を有効化 |
| `mlflow_tracking_uri` | `str` | `None` | MLflowトラッキングサーバーのURI |
| `mlflow_experiment_name` | `str` | `None` | MLflow実験名。Noneの場合は自動生成 |
| `use_pruning` | `bool` | `False` | 早期停止（プルーニング）を有効化 |
| `time_budget_hours` | `float` | `None` | 最適化の時間制限（時間単位） |
| `random_seed` | `int` | `None` | 再現性のための乱数シード |
| `verbose` | `bool` | `True` | 詳細な進捗情報を表示 |

#### 返り値

| 型 | 説明 |
|----|------|
| `NeuralForecast.Auto*` | 最適化されたNeuralForecast Autoモデル |

#### 例外

| 例外 | 条件 |
|------|------|
| `ValueError` | 無効なモデル名、バックエンド名、またはパラメータ |
| `ValidationError` | データセットまたは設定の検証失敗 |
| `RuntimeError` | 最適化中のエラー |

#### 使用例

**基本的な使用**:
```python
from auto_model_factory import create_auto_model
import pandas as pd

df = pd.read_csv('data.csv')

auto_model = create_auto_model(
    model_name="NHITS",
    h=24,
    dataset=df,
    num_samples=50
)

predictions = auto_model.predict(dataset=df)
```

**カスタム設定**:
```python
from ray import tune

custom_config = {
    'max_steps': tune.choice([1000, 2000]),
    'learning_rate': tune.loguniform(1e-4, 1e-2),
    'batch_size': tune.choice([64, 128])
}

auto_model = create_auto_model(
    model_name="TFT",
    h=24,
    dataset=df,
    config=custom_config,
    backend="optuna",
    num_samples=100,
    gpus=2
)
```

**MLflow統合**:
```python
auto_model = create_auto_model(
    model_name="NHITS",
    h=7,
    dataset=df,
    use_mlflow=True,
    mlflow_tracking_uri="http://localhost:5000",
    mlflow_experiment_name="production_forecast",
    verbose=True
)
```

---

### AutoModelFactory

**概要**: 自動モデル作成のファクトリークラス。より細かい制御が必要な場合に使用。

#### シグネチャ

```python
class AutoModelFactory:
    def __init__(
        self,
        model_name: str,
        h: int,
        optimization_config: OptimizationConfig = None
    )
```

#### コンストラクタパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `model_name` | `str` | **必須** | NeuralForecastモデル名 |
| `h` | `int` | **必須** | 予測ホライゾン |
| `optimization_config` | `OptimizationConfig` | `None` | 最適化設定。Noneの場合はデフォルト設定 |

#### メソッド

##### create_auto_model()

自動最適化モデルを作成します。

```python
def create_auto_model(
    self,
    dataset: pd.DataFrame,
    config: Optional[Dict[str, Any]] = None,
    loss: Optional[Any] = None
) -> Any:
```

**パラメータ**:
- `dataset`: 時系列データ
- `config`: カスタムハイパーパラメータ探索空間
- `loss`: カスタム損失関数

**返り値**: 最適化されたモデル

##### get_optimization_summary()

最適化の概要情報を取得します。

```python
def get_optimization_summary(self) -> Dict[str, Any]:
```

**返り値**: 最適化の統計情報を含む辞書
- `model_name`: モデル名
- `forecast_horizon`: 予測ホライゾン
- `backend`: 使用バックエンド
- `num_samples`: 試行回数
- `selected_algorithm`: 選択されたアルゴリズム
- `dataset_characteristics`: データセット特性

##### _create_default_config()

デフォルトのハイパーパラメータ設定を生成します。

```python
def _create_default_config(self) -> Dict[str, Any]:
```

**返り値**: デフォルト設定の辞書

#### 使用例

**基本的な使用**:
```python
from auto_model_factory import AutoModelFactory, OptimizationConfig

# 設定
opt_config = OptimizationConfig(
    backend="optuna",
    num_samples=50,
    cpus=8,
    gpus=1,
    use_mlflow=True,
    verbose=True
)

# ファクトリー作成
factory = AutoModelFactory(
    model_name="TFT",
    h=24,
    optimization_config=opt_config
)

# モデル作成
auto_model = factory.create_auto_model(dataset=df)

# 概要取得
summary = factory.get_optimization_summary()
print(summary)
```

**高度な使用**:
```python
from ray import tune
from neuralforecast.losses.pytorch import MQLoss

# カスタム設定とカスタム損失
custom_config = {
    'max_steps': tune.choice([1000, 2000, 3000]),
    'learning_rate': tune.loguniform(1e-4, 1e-2)
}

custom_loss = MQLoss(level=[90])

factory = AutoModelFactory(
    model_name="NHITS",
    h=24,
    optimization_config=opt_config
)

auto_model = factory.create_auto_model(
    dataset=df,
    config=custom_config,
    loss=custom_loss
)
```

---

### OptimizationConfig

**概要**: 最適化設定を管理するデータクラス

#### シグネチャ

```python
@dataclass
class OptimizationConfig:
    backend: str = "optuna"
    num_samples: Optional[int] = None
    cpus: int = 4
    gpus: int = 0
    use_mlflow: bool = False
    mlflow_tracking_uri: Optional[str] = None
    mlflow_experiment_name: Optional[str] = None
    use_pruning: bool = False
    time_budget_hours: Optional[float] = None
    random_seed: Optional[int] = None
    verbose: bool = True
```

#### フィールド

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `backend` | `str` | `"optuna"` | 最適化バックエンド ("optuna" または "ray") |
| `num_samples` | `int` | `None` | 試行回数。Noneの場合は自動推奨 |
| `cpus` | `int` | `4` | 使用するCPU数 |
| `gpus` | `int` | `0` | 使用するGPU数 |
| `use_mlflow` | `bool` | `False` | MLflow統合を有効化 |
| `mlflow_tracking_uri` | `str` | `None` | MLflowトラッキングURI |
| `mlflow_experiment_name` | `str` | `None` | MLflow実験名 |
| `use_pruning` | `bool` | `False` | 早期停止を有効化 |
| `time_budget_hours` | `float` | `None` | 時間制限（時間単位） |
| `random_seed` | `int` | `None` | 乱数シード |
| `verbose` | `bool` | `True` | 詳細出力を有効化 |

#### 使用例

```python
from auto_model_factory import OptimizationConfig

# 基本設定
config = OptimizationConfig(
    backend="optuna",
    num_samples=50,
    cpus=8,
    gpus=2
)

# MLflow有効化
config = OptimizationConfig(
    backend="optuna",
    num_samples=30,
    use_mlflow=True,
    mlflow_tracking_uri="http://localhost:5000",
    mlflow_experiment_name="my_experiment"
)

# 時間制限とプルーニング
config = OptimizationConfig(
    backend="optuna",
    num_samples=None,  # 自動推奨
    use_pruning=True,
    time_budget_hours=2.0,
    random_seed=42
)
```

---

### ModelCharacteristics

**概要**: モデルの特性を定義するデータクラス

#### シグネチャ

```python
@dataclass
class ModelCharacteristics:
    name: str
    complexity: ModelComplexity
    recommended_input_size_range: Tuple[int, int]
    supports_exogenous: bool
    supports_static: bool
    typical_training_time_minutes: float
    memory_footprint_mb: float
```

#### フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `name` | `str` | モデル名 |
| `complexity` | `ModelComplexity` | モデルの複雑度 (SIMPLE, MODERATE, COMPLEX) |
| `recommended_input_size_range` | `Tuple[int, int]` | 推奨input_sizeの範囲 |
| `supports_exogenous` | `bool` | 外生変数をサポートするか |
| `supports_static` | `bool` | 静的特徴量をサポートするか |
| `typical_training_time_minutes` | `float` | 典型的な学習時間（分） |
| `memory_footprint_mb` | `float` | メモリ使用量（MB） |

#### MODEL_CATALOG

利用可能なすべてのモデルの特性を含む辞書。

```python
MODEL_CATALOG: Dict[str, ModelCharacteristics]
```

#### 使用例

```python
from model_characteristics import MODEL_CATALOG, ModelComplexity

# モデル特性の取得
nhits_char = MODEL_CATALOG["NHITS"]
print(f"Complexity: {nhits_char.complexity}")
print(f"Input size range: {nhits_char.recommended_input_size_range}")
print(f"Training time: {nhits_char.typical_training_time_minutes} min")

# 複雑なモデルのフィルタリング
complex_models = [
    name for name, char in MODEL_CATALOG.items()
    if char.complexity == ModelComplexity.COMPLEX
]
print(f"Complex models: {complex_models}")

# 外生変数をサポートするモデル
exog_models = [
    name for name, char in MODEL_CATALOG.items()
    if char.supports_exogenous
]
print(f"Models supporting exogenous variables: {exog_models}")
```

---

## validation.py

設定、環境、データの検証を提供するモジュール。

### ConfigValidator

**概要**: 設定と環境の検証を行うクラス

#### シグネチャ

```python
class ConfigValidator:
    def __init__(self, strict_mode: bool = False)
```

#### コンストラクタパラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `strict_mode` | `bool` | `False` | 厳格モード。Trueの場合は警告もエラーとして扱う |

#### メソッド

##### validate_backend_config()

バックエンド設定を検証します。

```python
def validate_backend_config(
    self,
    backend: str,
    config: Optional[Dict[str, Any]],
    num_samples: Optional[int],
    cpus: int,
    gpus: int
) -> ValidationResult:
```

**パラメータ**:
- `backend`: バックエンド名 ("optuna" または "ray")
- `config`: ハイパーパラメータ設定
- `num_samples`: 試行回数
- `cpus`: CPU数
- `gpus`: GPU数

**返り値**: `ValidationResult`

##### validate_model_config()

モデル設定を検証します。

```python
def validate_model_config(
    self,
    config: Dict[str, Any],
    model_class_name: str
) -> ValidationResult:
```

**パラメータ**:
- `config`: モデル設定
- `model_class_name`: モデルクラス名

**返り値**: `ValidationResult`

##### validate_environment()

実行環境を検証します。

```python
def validate_environment(
    self,
    required_memory_gb: float = 4.0,
    required_disk_gb: float = 10.0
) -> ValidationResult:
```

**パラメータ**:
- `required_memory_gb`: 必要メモリ（GB）
- `required_disk_gb`: 必要ディスク容量（GB）

**返り値**: `ValidationResult`

##### validate_mlflow_config()

MLflow設定を検証します。

```python
def validate_mlflow_config(
    self,
    tracking_uri: Optional[str] = None,
    experiment_name: Optional[str] = None
) -> ValidationResult:
```

**パラメータ**:
- `tracking_uri`: MLflowトラッキングURI
- `experiment_name`: 実験名

**返り値**: `ValidationResult`

#### 使用例

```python
from validation import ConfigValidator

# バリデーター作成
validator = ConfigValidator(strict_mode=False)

# バックエンド設定の検証
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
    if result.corrected_config:
        print("Suggested config:", result.corrected_config)

# 環境の検証
env_result = validator.validate_environment(
    required_memory_gb=8.0,
    required_disk_gb=20.0
)

# MLflow設定の検証
mlflow_result = validator.validate_mlflow_config(
    tracking_uri="http://localhost:5000",
    experiment_name="my_experiment"
)
```

---

### DataValidator

**概要**: データセットの検証を行うクラス

#### メソッド

##### validate_dataset()

データセットの構造と内容を検証します。

```python
def validate_dataset(
    self,
    df: pd.DataFrame,
    required_columns: List[str] = ['unique_id', 'ds', 'y']
) -> ValidationResult:
```

**パラメータ**:
- `df`: 検証するデータセット
- `required_columns`: 必須カラムのリスト

**返り値**: `ValidationResult`

**検証項目**:
- 必須カラムの存在
- データ型の正確性
- 欠損値の有無
- 重複レコードの有無
- 時系列の連続性

##### validate_forecast_horizon()

予測ホライゾンの妥当性を検証します。

```python
def validate_forecast_horizon(
    self,
    df: pd.DataFrame,
    h: int
) -> ValidationResult:
```

**パラメータ**:
- `df`: データセット
- `h`: 予測ホライゾン

**返り値**: `ValidationResult`

#### 使用例

```python
from validation import DataValidator
import pandas as pd

# データバリデーター作成
validator = DataValidator()

# データセット検証
df = pd.read_csv('data.csv')
result = validator.validate_dataset(df)

if result.is_valid:
    print("✅ Dataset is valid")
else:
    print("❌ Dataset validation failed:")
    for error in result.errors:
        print(f"  - {error}")

# 予測ホライゾン検証
h = 24
horizon_result = validator.validate_forecast_horizon(df, h)

if not horizon_result.is_valid:
    print("⚠️ Forecast horizon may be too large")
    print(horizon_result.warnings)
```

---

### ValidationResult

**概要**: 検証結果を保持するデータクラス

#### シグネチャ

```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    corrected_config: Optional[Dict[str, Any]] = None
```

#### フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `is_valid` | `bool` | 検証が成功したかどうか |
| `errors` | `List[str]` | エラーメッセージのリスト |
| `warnings` | `List[str]` | 警告メッセージのリスト |
| `corrected_config` | `Dict[str, Any]` | 修正された設定（利用可能な場合） |

---

### ユーティリティ関数

#### validate_all()

すべての検証を一度に実行します。

```python
def validate_all(
    backend: str,
    config: Optional[Dict[str, Any]],
    num_samples: Optional[int],
    cpus: int,
    gpus: int,
    model_class_name: str,
    dataset: pd.DataFrame,
    h: int,
    strict_mode: bool = False
) -> Dict[str, Any]:
```

**返り値**: 各カテゴリの検証結果を含む辞書

#### print_validation_results()

検証結果を整形して表示します。

```python
def print_validation_results(result: ValidationResult) -> None:
```

---

## search_algorithm_selector.py

探索アルゴリズムの自動選択を提供するモジュール。

### SearchAlgorithmSelector

**概要**: モデルとデータの特性に基づいて最適なアルゴリズムを選択

#### シグネチャ

```python
class SearchAlgorithmSelector:
    def __init__(self, backend: str = "optuna")
```

#### メソッド

##### select_algorithm()

最適な探索アルゴリズムを選択します。

```python
def select_algorithm(
    self,
    model_complexity: ModelComplexity,
    dataset_size: DatasetSize,
    num_samples: int,
    config: Optional[Dict[str, Any]] = None,
    use_pruning: bool = False,
    random_seed: Optional[int] = None
) -> SearchStrategy:
```

**パラメータ**:
- `model_complexity`: モデルの複雑度
- `dataset_size`: データセットサイズ
- `num_samples`: 試行回数
- `config`: 探索空間設定
- `use_pruning`: プルーニング有効化
- `random_seed`: 乱数シード

**返り値**: `SearchStrategy`

##### get_optuna_sampler()

Optunaサンプラーを取得します。

```python
def get_optuna_sampler(
    self,
    strategy: SearchStrategy
) -> optuna.samplers.BaseSampler:
```

##### get_optuna_pruner()

Optunaプルーナーを取得します。

```python
def get_optuna_pruner(
    self,
    strategy: SearchStrategy
) -> Optional[optuna.pruners.BasePruner]:
```

##### get_ray_search_algorithm()

Ray Tune探索アルゴリズムを取得します。

```python
def get_ray_search_algorithm(
    self,
    strategy: SearchStrategy
) -> Any:
```

#### 使用例

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
    use_pruning=True,
    random_seed=42
)

print(f"Selected: {strategy.algorithm_name}")
print(f"Description: {strategy.description}")
print(f"Reason: {strategy.reason}")

# サンプラーとプルーナーを取得
sampler = selector.get_optuna_sampler(strategy)
pruner = selector.get_optuna_pruner(strategy)
```

---

### SearchStrategy

**概要**: 選択された探索戦略を表すデータクラス

#### シグネチャ

```python
@dataclass
class SearchStrategy:
    algorithm_name: str
    description: str
    reason: str
    hyperparameters: Dict[str, Any]
    use_multivariate: bool = False
    use_pruning: bool = False
    pruning_config: Optional[Dict[str, Any]] = None
```

#### フィールド

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `algorithm_name` | `str` | アルゴリズム名 |
| `description` | `str` | アルゴリズムの説明 |
| `reason` | `str` | 選択理由 |
| `hyperparameters` | `Dict[str, Any]` | アルゴリズムのハイパーパラメータ |
| `use_multivariate` | `bool` | 多変量TPEを使用するか |
| `use_pruning` | `bool` | プルーニングを使用するか |
| `pruning_config` | `Dict[str, Any]` | プルーニング設定 |

---

### recommend_num_samples()

**概要**: 最適な試行回数を推奨する関数

#### シグネチャ

```python
def recommend_num_samples(
    model_complexity: ModelComplexity,
    dataset_size: DatasetSize,
    search_complexity: SearchComplexity = SearchComplexity.MEDIUM,
    time_budget_hours: Optional[float] = None
) -> Tuple[int, str]:
```

#### パラメータ

| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `model_complexity` | `ModelComplexity` | **必須** | モデルの複雑度 |
| `dataset_size` | `DatasetSize` | **必須** | データセットサイズ |
| `search_complexity` | `SearchComplexity` | `MEDIUM` | 探索空間の複雑度 |
| `time_budget_hours` | `float` | `None` | 時間制限（時間単位） |

#### 返り値

| 要素 | 型 | 説明 |
|------|-----|------|
| `num_samples` | `int` | 推奨試行回数 |
| `explanation` | `str` | 推奨理由の説明 |

#### 使用例

```python
from search_algorithm_selector import (
    recommend_num_samples,
    ModelComplexity,
    DatasetSize,
    SearchComplexity
)

# 基本的な推奨
num_samples, explanation = recommend_num_samples(
    model_complexity=ModelComplexity.MODERATE,
    dataset_size=DatasetSize.MEDIUM
)
print(f"Recommended: {num_samples} trials")
print(f"Reason: {explanation}")

# 時間制限付き
num_samples, explanation = recommend_num_samples(
    model_complexity=ModelComplexity.COMPLEX,
    dataset_size=DatasetSize.LARGE,
    search_complexity=SearchComplexity.HIGH,
    time_budget_hours=2.0
)
print(f"Within 2 hours: {num_samples} trials")
```

---

## mlflow_integration.py

MLflowとの統合を提供するモジュール。

### setup_mlflow()

MLflowを設定します。

```python
def setup_mlflow(
    tracking_uri: Optional[str] = None,
    experiment_name: Optional[str] = None
) -> str:
```

**パラメータ**:
- `tracking_uri`: MLflowトラッキングURI
- `experiment_name`: 実験名

**返り値**: 実験ID

### log_optimization_results()

最適化結果をMLflowに記録します。

```python
def log_optimization_results(
    params: Dict[str, Any],
    metrics: Dict[str, float],
    artifacts: Optional[Dict[str, str]] = None
) -> None:
```

**パラメータ**:
- `params`: パラメータの辞書
- `metrics`: メトリクスの辞書
- `artifacts`: アーティファクトの辞書（パス）

---

## logging_config.py

ロギング設定を提供するモジュール。

### setup_logging()

ロギングを設定します。

```python
def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
```

**パラメータ**:
- `level`: ログレベル ("DEBUG", "INFO", "WARNING", "ERROR")
- `log_file`: ログファイルのパス
- `format_string`: ログフォーマット文字列

**返り値**: 設定されたLogger

---

## データ型定義

### Enum型

#### ModelComplexity

```python
class ModelComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
```

#### DatasetSize

```python
class DatasetSize(Enum):
    SMALL = "small"      # < 10,000 rows
    MEDIUM = "medium"    # 10,000 - 100,000 rows
    LARGE = "large"      # > 100,000 rows
```

#### SearchComplexity

```python
class SearchComplexity(Enum):
    LOW = "low"          # < 10 parameters
    MEDIUM = "medium"    # 10 - 20 parameters
    HIGH = "high"        # > 20 parameters
```

---

## よくあるパターン

### パターン1: シンプルな予測

```python
from auto_model_factory import create_auto_model

auto_model = create_auto_model(
    model_name="NHITS",
    h=7,
    dataset=df,
    num_samples=30
)
predictions = auto_model.predict(dataset=df)
```

### パターン2: 詳細な制御

```python
from auto_model_factory import AutoModelFactory, OptimizationConfig
from ray import tune

config = OptimizationConfig(
    backend="optuna",
    num_samples=50,
    gpus=2,
    use_mlflow=True
)

factory = AutoModelFactory(
    model_name="TFT",
    h=24,
    optimization_config=config
)

custom_config = {
    'max_steps': tune.choice([1000, 2000]),
    'learning_rate': tune.loguniform(1e-4, 1e-2)
}

auto_model = factory.create_auto_model(
    dataset=df,
    config=custom_config
)
```

### パターン3: 検証重視

```python
from validation import validate_all, print_validation_results

results = validate_all(
    backend="optuna",
    config=my_config,
    num_samples=50,
    cpus=4,
    gpus=1,
    model_class_name="NHITS",
    dataset=df,
    h=24
)

if results['overall_valid']:
    auto_model = create_auto_model(...)
else:
    print_validation_results(results)
```

---

## バージョン互換性

### v1.0.0
- 初回リリース
- Optuna/Ray Tune統合
- MLflowサポート
- 自動検証機能

---

## 注意事項

1. **GPU使用時**: CUDA互換のPyTorchが必要
2. **大規模データ**: メモリ使用量に注意
3. **並列実行**: Ray使用時はクラスター設定が必要
4. **再現性**: `random_seed`を設定すること

---

## サポートとフィードバック

API仕様に関する質問や提案は、GitHubのIssuesでお願いします。

**ドキュメントバージョン**: 1.0.0  
**最終更新**: 2025年11月12日
