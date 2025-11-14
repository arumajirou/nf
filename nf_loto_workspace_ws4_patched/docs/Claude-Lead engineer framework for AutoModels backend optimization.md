# Lead engineer framework for AutoModels backend optimization

**Created:** 11/12/2025 11:58:53  
**Updated:** 11/12/2025 12:16:10  
**Exported:** 11/12/2025 13:06:27  
**Link:** [https://claude.ai/chat/51a7a656-f286-493c-b54e-7905bd5bcfe1](https://claude.ai/chat/51a7a656-f286-493c-b54e-7905bd5bcfe1)  

## Prompt:
2025/11/12 11:58:59

> File: 

> File: 

あなたは優秀なリードエンジニアです。以下を厳守してください：
- 真偽の検証：一次情報（公式ドキュメント/標準仕様/実測）を最優先。引用は日付・版を明記。
- 再現性：すべての前提・環境・コマンド・seed・入力/出力スキーマを明文化し、再実行手順を提示。
- 可観測性：ログ/メトリクス/アーティファクトの保存先を必ず指示（MLflow/DB/ELK/Grafana）。
- 合理性：仮説→検証→結果→解釈→次アクションの順で書く。不要な断定・主観は避け、証拠で語る。
- 安全性：Secrets/PIIを露出しない。危険操作には確認ガード（dry-run/backup/roll-back）。
- ミスコミ防止：要件→制約→受入基準→デリバラブルの四点を最初に再掲。
- エラー時：切り分け→再現→最小化→仮説→検証→恒久対策。感情表現や推測の断定はしない。
- 出力契約：JSON/YAMLなどの固定スキーマを守り、曖昧語を限定。数値には単位・信頼区間を付す。
[Role]
- あなたは本案件のリードエンジニア。資料（複数可）を読み込み、最適解へ到達するためのPDCAを設計・実行する。
[Input]
- 資料: <URL/本文/添付要約>
- 目的/KPI: <定量指標と閾値>
- 制約: <時間/資源/互換性/セキュリティ>
- 成果物: <期待するファイル/スキーマ/ダッシュ/コード>
[Task]
1) 目標/制約/受入基準の再掲。
2) 既知ギャップと検証プラン。
3) 実行計画（小さなバッチ、計測、ロールバック）。
4) 実装/結果の要約。
5) KPI評価と解釈。
6) 次の一手（改善/追加検証/ADR要否）。
[Output — JSON]
{
  "goals": [],
  "acceptance_criteria": [],
  "plan": ["..."],
  "actions": ["..."],
  "findings": {"metrics": {}, "artifacts": []},
  "risks": ["..."],
  "next": ["..."]
}
System: 一次情報を優先し、用語/数式/閾値/前提を抽出。曖昧語を定義し、齟齬点を列挙。
User:
- 入力資料: <本文/URL/添付要約>
- 期待: 用語定義 / 仕様抜粋 / 未確定事項 / アクション
Output(Markdown):
- 用語/定義
- 仕様の核（数式/閾値/契約）
- 矛盾・未確定
- アクション（担当/RACI/期限）
System: 最小API/型/Docstring/例外/ログ/計測/MLflow記録を必ず含む。
User: 要件/入出力/制約/対象モジュール
Output: コード + 単体テスト + 使用例 + MLflowロギング断片
P (Plan): 目的/KPI/制約/受入基準 → 実験設計（対照/因子/測定）
D (Do): 手順（再現可能）、実行ログ、アーティファクト
C (Check): 結果（指標/統計/費用/CO₂）、差分解釈
A (Act): 恒久対策/ADR要否/次の反復
Troubleshoot:
1) 事実の再掲（症状/範囲/直近変更）
2) 再現の最小化（5分で回る単位）
3) 仮説の列挙（優先度/検証コスト）
4) 実験（期待→結果）
5) 原因確定→恒久対策→回帰テスト
- 型: すべての公開関数に type hints / Docstring（Args/Returns/Raises）。
- 計測: 主要経路で perf_counter、MLflow に duration_* をログ。
- ログ: 構造化（JSON）、run_id/request_id を含める。
- 例外: 期待失敗を専用例外で表現（ValidationError, ResourceExhausted）。
- テスト: pytest + hypothesis、ゴールデン/スナップショット。
- 安全: 一時ファイル→アトミックリネーム。バックオフ/再試行をデコレータ化。
{
  "summary": "短い要約",
  "assumptions": ["..."],
  "metrics": {"smape": 0.123, "crps": 0.456, "coverage90": 0.91},
  "artifacts": ["mlflow://...", "s3://..."],
  "risks": ["回帰の恐れ"],
  "actions": ["テスト追加", "ADR起票"],
  "owners": {"R": "MLE", "A": "QA"}
}

アップロードしたファイルや関連URLを確認して下記のコードで全AutoModelsで各backendが選択された場合、それに最適なsearch_algを設定して学習を行い、モデルを生成するようにコードを改修してください
まず、アップロードしたファイルや関連URLの公式ドキュメントからどのような実装、ロジック、設計にすれば最適かを調査して業務用でハイレベルな詳細で具体的な要件定義兼機能設計定義仕様書を作成してください



## Response:
2025/11/12 12:03:04

````plaintext
Thought process: 検証済み公式ドキュメント参照し、要件定義と実装設計を構想。

ユーザーは、アップロードされたファイル（パラメータ互換表とAutoTFT/AutoPatchTSTの属性ダンプ）と関連URLを基に、以下を求めています：

1. 全AutoModelsで各backendが選択された場合に最適なsearch_algを設定して学習を行うコード改修
2. その前に、公式ドキュメントから最適な実装/ロジック/設計を調査
3. 業務用でハイレベルな詳細で具体的な要件定義兼機能設計定義仕様書の作成

まず、プロジェクトナレッジから関連情報を検索する必要があります。特に：
- NeuralForecastの公式ドキュメント
- OptunaとRay Tuneの統合パターン
- 各search_algの特性と推奨設定

プロジェクトファイルを確認すると：
- 01_NeuralForecast.md
- 03_Optuna.md
- 04_MLflow.md
- 07_Lightning.md
- 03_optunareadthedocsio.md

これらを参照しながら要件定義を作成します。
````

プロジェクトナレッジと公式ドキュメントを参照して、最適な実装設計を調査します。

**project_knowledge_search**

*Request*

````javascript
{
  "query": "NeuralForecast AutoModel backend optuna ray search algorithm sampler configuration",
  "max_text_results": 10
}
````

*Response*

````plaintext
01_NeuralForecast.md
### [â€‹](#baseauto)BaseAuto


> CopyAsk AI BaseAuto (cls_model, h, loss, valid_loss, config,
>            search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>            object at 0x7f820028a2f0>, num_samples=10, cpus=4, gpus=0,
>            refit_with_val=False, verbose=False, alias=None, backend='ray',
>            callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.*
**Type****Default****Details**cls_modelPyTorch/PyTorchLightning modelSee `neuralforecast.models` [collection here](https://nixtla.github.io/neuralforecast/models.html).hintForecast horizonlossPyTorch moduleInstantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossPyTorch moduleInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configdict or callableDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f820028a2f0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.refit_with_valboolFalseRefit of best model should preserve val_size.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.
````

````plaintext
neuralforecast/auto.py
standard", "identity"]),
        "max_steps": tune.choice([500, 1000, 2000]),
        "batch_size": tune.choice([32, 64, 128, 256]),
        "loss": None,
        "random_seed": tune.randint(1, 20),
    }

    def __init__(
        self,
        h,
        n_series,
        loss=MAE(),
        valid_loss=None,
        config=None,
        search_alg=BasicVariantGenerator(random_state=1),
        num_samples=10,
        refit_with_val=False,
        cpus=cpu_count(),
        gpus=torch.cuda.device_count(),
        verbose=False,
        alias=None,
        backend="ray",
        callbacks=None,
    ):

        # Define search space, input/output sizes
        if config is None:
            config = self.get_default_config(h=h, backend=backend, n_series=n_series)

        # Always use n_series from parameters, raise exception with Optuna because we can't enforce it
        if backend == "ray":
            config["n_series"] = n_series
        elif backend == "optuna":
            mock_trial = MockTrial()
            if (
                "n_series" in config(mock_trial)
                and config(mock_trial)["n_series"] != n_series
            ) or ("n_series" not in config(mock_trial)):
                raise Exception(f"config needs 'n_series': {n_series}")

        super(AutoRMoK, self).__init__(
            cls_model=RMoK,
            h=h,
            loss=loss,
            valid_loss=valid_loss,
            config=config,
            search_alg=search_alg,
            num_samples=num_samples,
            refit_with_val=refit_with_val,
            cpus=cpus,
            gpus=gpus,
            verbose=verbose,
            alias=alias,
            backend=backend,
            callbacks=callbacks,
        )

    @classmethod
    def get_default_config(cls, h, backend, n_series):
        config = cls.default_config.copy()
        config["input_size"] = tune.choice(
            [h * x for x in config["input_size_multiplier"]]
        )

        # Rolling windows with step_size=1 or step_size=h
        # See `BaseWindows` and `BaseRNN`'s create_windows
        config["step_size"] = tune.choice([1, h])
        del config["input_size_multiplier"]
        if backend == "optuna":
            # Always use n_series from parameters
            config["n_series"] = n_series
            config = cls._ray_config_to_optuna(config)

        return config
````

````plaintext
neuralforecast/common/_base_auto.py
__all__ = ['BaseAuto']


import warnings
from copy import deepcopy
from os import cpu_count

import pytorch_lightning as pl
import torch
from ray import air, tune
from ray.tune.integration.pytorch_lightning import TuneReportCallback
from ray.tune.search.basic_variant import BasicVariantGenerator


class MockTrial:
    def suggest_int(*args, **kwargs):
        return "int"

    def suggest_categorical(self, name, choices):
        return choices

    def suggest_uniform(*args, **kwargs):
        return "uniform"

    def suggest_loguniform(*args, **kwargs):
        return "loguniform"

    def suggest_float(*args, **kwargs):
        if "log" in kwargs:
            return "quantized_log"
        elif "step" in kwargs:
            return "quantized_loguniform"
        return "float"


class BaseAuto(pl.LightningModule):
    """
    Class for Automatic Hyperparameter Optimization, it builds on top of `ray` to
    give access to a wide variety of hyperparameter optimization tools ranging
    from classic grid search, to Bayesian optimization and HyperBand algorithm.

    The validation loss to be optimized is defined by the `config['loss']` dictionary
    value, the config also contains the rest of the hyperparameter search space.

    It is important to note that the success of this hyperparameter optimization
    heavily relies on a strong correlation between the validation and test periods.

    Args:
        cls_model (PyTorch/PyTorchLightning model): See `neuralforecast.models` [collection here](./models).
        h (int): Forecast horizon
        loss (PyTorch module): Instantiated train loss class from [losses collection](./losses.pytorch).
        valid_loss (PyTorch module): Instantiated valid loss class from [losses collection](./losses.pytorch).
        config (dict or callable): Dictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.
        search_alg (ray.tune.search variant or optuna.sampler): For ray see https://docs.ray.io/en/latest/tune/api_docs/suggestion.html
        For optuna see https://optuna.readthedocs.io/en/stable/reference/samplers/index.html.
        num_samples (int): Number of hyperparameter optimization steps/samples.
        Number of hyperparameter optimization steps/samples.
        cpus (int): Number of cpus to use during optimization. Only used with ray tune.
        gpus (int): Number of gpus to use during optimization, default all available. Only used with ray tune.
        refit_with_val (bool): Refit of best model should preserve val_size.
        verbose (bool): Track progress.
        alias (str): Custom name of the model.
        Custom name of the model.
        backend (str): Backend to use for searching the hyperparameter space, can be either 'ray' or 'optuna'.
        callbacks (list of callable): List of functions to call during the optimization process.
        List of functions to call during the optimization process.
````

````plaintext
neuralforecast/auto.py
pus=gpus,
            verbose=verbose,
            alias=alias,
            backend=backend,
            callbacks=callbacks,
        )

    @classmethod
    def get_default_config(cls, h, backend, n_series):
        config = cls.default_config.copy()
        config["input_size"] = tune.choice(
            [h * x for x in config["input_size_multiplier"]]
        )

        # Rolling windows with step_size=1 or step_size=h
        # See `BaseWindows` and `BaseRNN`'s create_windows
        config["step_size"] = tune.choice([1, h])
        del config["input_size_multiplier"]
        if backend == "optuna":
            # Always use n_series from parameters
            config["n_series"] = n_series
            config = cls._ray_config_to_optuna(config)

        return config


class AutoMLPMultivariate(BaseAuto):

    default_config = {
        "input_size_multiplier": [1, 2, 3, 4, 5],
        "h": None,
        "n_series": None,
        "hidden_size": tune.choice([256, 512, 1024]),
        "num_layers": tune.randint(2, 6),
        "learning_rate": tune.loguniform(1e-4, 1e-1),
        "scaler_type": tune.choice([None, "robust", "standard"]),
        "max_steps": tune.choice([500, 1000]),
        "batch_size": tune.choice([32, 64, 128, 256]),
        "loss": None,
        "random_seed": tune.randint(1, 20),
    }

    def __init__(
        self,
        h,
        n_series,
        loss=MAE(),
        valid_loss=None,
        config=None,
        search_alg=BasicVariantGenerator(random_state=1),
        num_samples=10,
        refit_with_val=False,
        cpus=cpu_count(),
        gpus=torch.cuda.device_count(),
        verbose=False,
        alias=None,
        backend="ray",
        callbacks=None,
    ):

        # Define search space, input/output sizes
        if config is None:
            config = self.get_default_config(h=h, backend=backend, n_series=n_series)

        # Always use n_series from parameters, raise exception with Optuna because we can't enforce it
        if backend == "ray":
            config["n_series"] = n_series
        elif backend == "optuna":
            mock_trial = MockTrial()
            if (
                "n_series" in config(mock_trial)
                and config(mock_trial)["n_series"] != n_series
            ) or ("n_series" not in config(mock_trial)):
                raise Exception(f"config needs 'n_seri
````

````plaintext
01_NeuralForecast.md
First we load the AirPassengers dataset such that you can run all the
examples.
CopyAsk AI`​`​`
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast.tsdataset import TimeSeriesDataset
from neuralforecast.utils import AirPassengersDF as Y_df
`​`​`


CopyAsk AI`​`​`
# Split train/test and declare time series dataset
Y_train_df = Y_df[Y_df.ds<='1959-12-31'] # 132 train
Y_test_df = Y_df[Y_df.ds>'1959-12-31']   # 12 test
dataset, *_ = TimeSeriesDataset.from_df(Y_train_df)
`​`​`


# [â€‹](#1-automatic-forecasting)1. Automatic Forecasting


## [â€‹](#a-rnn-based)A. RNN-Based



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L61)
### [â€‹](#autornn)AutoRNN


> CopyAsk AI AutoRNN (h, loss=MAE(), valid_loss=None, config=None,
>           search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>           object at 0x7f1320942da0>, num_samples=10, refit_with_val=False,
>           cpus=4, gpus=0, verbose=False, alias=None, backend='ray',
>           callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320942da0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available.
````

````plaintext
neuralforecast/auto.py
    gpus=torch.cuda.device_count(),
        verbose=False,
        alias=None,
        backend="ray",
        callbacks=None,
    ):

        # Define search space, input/output sizes
        if config is None:
            config = self.get_default_config(h=h, backend=backend, n_series=n_series)

        # Always use n_series from parameters, raise exception with Optuna because we can't enforce it
        if backend == "ray":
            config["n_series"] = n_series
        elif backend == "optuna":
            mock_trial = MockTrial()
            if (
                "n_series" in config(mock_trial)
                and config(mock_trial)["n_series"] != n_series
            ) or ("n_series" not in config(mock_trial)):
                raise Exception(f"config needs 'n_series': {n_series}")

        super(AutoTimeMixer, self).__init__(
            cls_model=TimeMixer,
            h=h,
            loss=loss,
            valid_loss=valid_loss,
            config=config,
            search_alg=search_alg,
            num_samples=num_samples,
            refit_with_val=refit_with_val,
            cpus=cpus,
            gpus=gpus,
            verbose=verbose,
            alias=alias,
            backend=backend,
            callbacks=callbacks,
        )

    @classmethod
    def get_default_config(cls, h, backend, n_series):
        config = cls.default_config.copy()
        config["input_size"] = tune.choice(
            [h * x for x in config["input_size_multiplier"]]
        )

        # Rolling windows with step_size=1 or step_size=h
        # See `BaseWindows` and `BaseRNN`'s create_windows
        config["step_size"] = tune.choice([1, h])
        del config["input_size_multiplier"]
        if backend == "optuna":
            # Always use n_series from parameters
            config["n_series"] = n_series
            config = cls._ray_config_to_optuna(config)

        return config


class AutoRMoK(BaseAuto):

    default_config = {
        "input_size_multiplier": [1, 2, 3, 4, 5],
        "h": None,
        "n_series": None,
        "taylor_order": tune.choice([3, 4, 5]),
        "jacobi_degree": tune.choice([4, 5, 6]),
        "wavelet_function": tune.choice(
            ["mexican_hat", "morlet", "dog", "meyer", "shannon"]
        ),
        "learning_rate": tune.loguniform(1e-4, 1e-1),
        "scaler_type": tune.choice([None, "robust", "
````

````plaintext
03_Optuna.md
[`CmaEsSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html#optuna.samplers.CmaEsSampler)


A sampler using [cmaes](https://github.com/CyberAgentAILab/cmaes) as the backend.



[`NSGAIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html#optuna.samplers.NSGAIISampler)


Multi-objective sampler using the NSGA-II algorithm.



[`NSGAIIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIIISampler.html#optuna.samplers.NSGAIIISampler)


Multi-objective sampler using the NSGA-III algorithm.



[`GridSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GridSampler.html#optuna.samplers.GridSampler)


Sampler using grid search.



[`QMCSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.QMCSampler.html#optuna.samplers.QMCSampler)


A Quasi Monte Carlo Sampler that generates low-discrepancy sequences.



[`BruteForceSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BruteForceSampler.html#optuna.samplers.BruteForceSampler)


Sampler using brute force.



[`PartialFixedSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.PartialFixedSampler.html#optuna.samplers.PartialFixedSampler)


Sampler with partially fixed parameters.






Note


The following [`optuna.samplers.nsgaii`](https://optuna.readthedocs.io/en/stable/reference/samplers/nsgaii.html#module-optuna.samplers.nsgaii) module defines crossover operations used by [`NSGAIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html#optuna.samplers.NSGAIISampler).




- [optuna.samplers.nsgaii](https://optuna.readthedocs.io/en/stable/reference/samplers/nsgaii.html)

---

## Callback for Study.optimize â€” Optuna 4.6.0 documentation
<a id="Callback-for-Studyoptimize-Optuna-460-documentation"></a>

- å…ƒURL: https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html

Note


[Go to the end](#sphx-glr-download-tutorial-20-recipes-007-optuna-callback-py)
to download the full example code.




# Callback for Study.optimize[ïƒ](#callback-for-study-optimize)


This tutorial showcases how to use & implement Optuna `Callback` for [`optimize()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.optimize).


`Callback` is called after every evaluation of `objective`, and
it takes [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) and [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) as arguments, and does some work.
````

````plaintext
01_NeuralForecast.md
Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI`​`​`
# Use your own config or AutoNBEATS.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12,
              mlp_units=3*[[8, 8]])
model = AutoNBEATS(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoNBEATS(h=12, config=None, backend='optuna')
`​`​`



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L693)
### [â€‹](#autonbeatsx)AutoNBEATSx


> CopyAsk AI AutoNBEATSx (h, loss=MAE(), valid_loss=None, config=None,
>               search_alg=<ray.tune.search.basic_variant.BasicVariantGenera
>               tor object at 0x7f1320ac6cb0>, num_samples=10,
>               refit_with_val=False, cpus=4, gpus=0, verbose=False,
>               alias=None, backend='ray', callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.
````

````plaintext
03_optunareadthedocsio.md
[`CmaEsSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html#optuna.samplers.CmaEsSampler)


A sampler using [cmaes](https://github.com/CyberAgentAILab/cmaes) as the backend.



[`NSGAIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html#optuna.samplers.NSGAIISampler)


Multi-objective sampler using the NSGA-II algorithm.



[`NSGAIIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIIISampler.html#optuna.samplers.NSGAIIISampler)


Multi-objective sampler using the NSGA-III algorithm.



[`GridSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GridSampler.html#optuna.samplers.GridSampler)


Sampler using grid search.



[`QMCSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.QMCSampler.html#optuna.samplers.QMCSampler)


A Quasi Monte Carlo Sampler that generates low-discrepancy sequences.



[`BruteForceSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BruteForceSampler.html#optuna.samplers.BruteForceSampler)


Sampler using brute force.



[`PartialFixedSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.PartialFixedSampler.html#optuna.samplers.PartialFixedSampler)


Sampler with partially fixed parameters.






Note


The following [`optuna.samplers.nsgaii`](https://optuna.readthedocs.io/en/stable/reference/samplers/nsgaii.html#module-optuna.samplers.nsgaii) module defines crossover operations used by [`NSGAIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html#optuna.samplers.NSGAIISampler).




- [optuna.samplers.nsgaii](https://optuna.readthedocs.io/en/stable/reference/samplers/nsgaii.html)

---

## Callback for Study.optimize â€” Optuna 4.6.0 documentation
<a id="Callback-for-Studyoptimize-Optuna-460-documentation"></a>

- å…ƒURL: https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html

Note


[Go to the end](#sphx-glr-download-tutorial-20-recipes-007-optuna-callback-py)
to download the full example code.




# Callback for Study.optimize[ïƒ](#callback-for-study-optimize)


This tutorial showcases how to use & implement Optuna `Callback` for [`optimize()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.optimize).


`Callback` is called after every evaluation of `objective`, and
it takes [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) and [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) as arguments, and does some work.
````

````plaintext
01_NeuralForecast.md
Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI`​`​`
# Use your own config or AutoMLP.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
model = AutoMLP(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoMLP(h=12, config=None, backend='optuna')
`​`​`



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L627)
### [â€‹](#autonbeats)AutoNBEATS


> CopyAsk AI AutoNBEATS (h, loss=MAE(), valid_loss=None, config=None,
>              search_alg=<ray.tune.search.basic_variant.BasicVariantGenerat
>              or object at 0x7f1320ad5390>, num_samples=10,
>              refit_with_val=False, cpus=4, gpus=0, verbose=False,
>              alias=None, backend='ray', callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.
````

````plaintext
Thought process

良い情報が得られました。続いて、Ray Tuneの検索アルゴリズムについても調べます。
````

**project_knowledge_search**

*Request*

````javascript
{
  "query": "Ray Tune search algorithm OptunaSearch HyperOptSearch BayesOptSearch scheduler ASHAScheduler pruner",
  "max_text_results": 8
}
````

*Response*

````plaintext
01_NeuralForecast.md
Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI`​`​`
# Use your own config or AutoLSTM.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=-1, encoder_hidden_size=8)
model = AutoLSTM(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoLSTM(h=12, config=None, backend='optuna')
`​`​`



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L207)
### [â€‹](#autogru)AutoGRU


> CopyAsk AI AutoGRU (h, loss=MAE(), valid_loss=None, config=None,
>           search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>           object at 0x7f1320e7c2b0>, num_samples=10, refit_with_val=False,
>           cpus=4, gpus=0, verbose=False, alias=None, backend='ray',
>           callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.
````

````plaintext
URL
g.ai/studios?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme',
'https://lightning.ai/notebooks?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme',
'https://lightning.ai/deploy?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme',
'https://github.com/Lightning-AI/pytorch-lightning#why-pytorch-lightning',
'https://github.com/Lightning-AI/pytorch-lightning#lightning-fabric-expert-contro',
"https://docs.ray.io/en/latest/tune/api_docs/suggestion.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/index.html",
"https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html",
"https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html",
"https://docs.ray.io/en/latest/tune/index.html",
"https://docs.ray.io/en/latest/tune/key-concepts.html",
"https://docs.ray.io/en/latest/tune/getting-started.html",
"https://docs.ray.io/en/latest/tune/tutorials/tune-lifecycle.html",
"https://docs.ray.io/en/latest/tune/api/search_space.html",
"https://docs.ray.io/en/latest/tune/tutorials/tune-search-spaces.html",
"https://docs.ray.io/en/latest/tune/api/suggestion.html",
"https://docs.ray.io/en/latest/tune/api/doc/ray.tune.search.optuna.OptunaSearch.html",
"https://docs.ray.io/en/latest/tune/api/doc/ray.tune.search.optuna.OptunaSearch.save_to_dir.html",
"https://docs.ray.io/en/latest/tune/api/doc/ray.tune.search.optuna.OptunaSearch.restore_from_dir.html",
"https://docs.ray.io/en/latest/tune/api/schedulers.html",
"https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.ASHAScheduler.html",
"https://docs.ray.io/en/latest/tune/api/doc/ray.tune.schedulers.ResourceChangingScheduler.html",
"https://docs.ray.io/en/latest/tune/api/callbacks.html",
"https://docs.ray.io/en/latest/tune/api/doc/ray.tune.Callback.html",
"https://docs.ray.io/en/latest/tune/tutorials/tune-resources.html",
"https://docs.ray.io/en/latest/tune/tutorials/tune-storage.html",
"https://docs.ray.io/en/latest/tune/api/api.html",
"https://docs.ray.io/en/latest/tune/examples/optuna_example.html",
"https://docs.pytorch.org/tutorials/beginner/hyperparameter_tuning_tutorial.html",
"https://docs.wandb.ai/models/integrations/ray-tune",
"https://docs.ultralytics.com/integrations/ray-tune/",
"https://docs.ultralytics.com/reference/utils/
````

````plaintext
URL
callbacks/raytune/",
"https://www.kaggle.com/code/moritzm00/xgboost-hyperparameter-tuning-with-ray-tune",
"https://arxiv.org/abs/1807.05118",
"https://optuna.org/",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.load_study.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.QMCSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html",
"https://optuna.readthedocs.io/en/stable/reference/pruners.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.ThresholdPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.PatientPruner.html",
"https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/006_user_defined_pruner.html",
"https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.TrialPruned.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.storages.RetryFailedTrialCallback.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.copy_study.html"
]
len(URLS)
````

````plaintext
01_NeuralForecast.md
### [â€‹](#baseauto)BaseAuto


> CopyAsk AI BaseAuto (cls_model, h, loss, valid_loss, config,
>            search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>            object at 0x7f820028a2f0>, num_samples=10, cpus=4, gpus=0,
>            refit_with_val=False, verbose=False, alias=None, backend='ray',
>            callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.*
**Type****Default****Details**cls_modelPyTorch/PyTorchLightning modelSee `neuralforecast.models` [collection here](https://nixtla.github.io/neuralforecast/models.html).hintForecast horizonlossPyTorch moduleInstantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossPyTorch moduleInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configdict or callableDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f820028a2f0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.refit_with_valboolFalseRefit of best model should preserve val_size.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.
````

````plaintext
01_NeuralForecast.md
Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI`​`​`
# Use your own config or AutoTimeXer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, patch_len=12)
model = AutoTimeXer(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTimeXer(h=12, n_series=1, config=None, backend='optuna')
`​`​`


## [â€‹](#e-cnn-based)E. CNN Based



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1762)
### [â€‹](#autotimesnet)AutoTimesNet


> CopyAsk AI AutoTimesNet (h, loss=MAE(), valid_loss=None, config=None,
>                search_alg=<ray.tune.search.basic_variant.BasicVariantGener
>                ator object at 0x7f1320a13760>, num_samples=10,
>                refit_with_val=False, cpus=4, gpus=0, verbose=False,
>                alias=None, backend='ray', callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.
````

````plaintext
01_NeuralForecast.md
Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI`​`​`
# Use your own config or AutoSOFTS.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=16)
model = AutoSOFTS(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoSOFTS(h=12, n_series=1, config=None, backend='optuna')
`​`​`



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L2329)
### [â€‹](#autotimemixer)AutoTimeMixer


> CopyAsk AI AutoTimeMixer (h, n_series, loss=MAE(), valid_loss=None, config=None,
>                 search_alg=<ray.tune.search.basic_variant.BasicVariantGene
>                 rator object at 0x7f1320ba16c0>, num_samples=10,
>                 refit_with_val=False, cpus=4, gpus=0, verbose=False,
>                 alias=None, backend='ray', callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.
````

````plaintext
01_NeuralForecast.md
Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI`​`​`
# Use your own config or AutoGRU.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=-1, encoder_hidden_size=8)
model = AutoGRU(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoGRU(h=12, config=None, backend='optuna')
`​`​`



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L278)
### [â€‹](#autotcn)AutoTCN


> CopyAsk AI AutoTCN (h, loss=MAE(), valid_loss=None, config=None,
>           search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>           object at 0x7f13208f1ae0>, num_samples=10, refit_with_val=False,
>           cpus=4, gpus=0, verbose=False, alias=None, backend='ray',
>           callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.
````

````plaintext
01_NeuralForecast.md
Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either â€˜rayâ€™ or â€˜optunaâ€™.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI`​`​`
# Use your own config or AutoTimeMixer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, d_model=16)
model = AutoTimeMixer(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTimeMixer(h=12, n_series=1, config=None, backend='optuna')
`​`​`



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L2415)
### [â€‹](#autormok)AutoRMoK


> CopyAsk AI AutoRMoK (h, n_series, loss=MAE(), valid_loss=None, config=None,
>            search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>            object at 0x7f1320ba3340>, num_samples=10,
>            refit_with_val=False, cpus=4, gpus=0, verbose=False,
>            alias=None, backend='ray', callbacks=None)


*Class for Automatic Hyperparameter Optimization, it builds on top of
`ray` to give access to a wide variety of hyperparameter optimization
tools ranging from classic grid search, to Bayesian optimization and
HyperBand algorithm.
The validation loss to be optimized is defined by the `config['loss']`
dictionary value, the config also contains the rest of the
hyperparameter search space.
It is important to note that the success of this hyperparameter
optimization heavily relies on a strong correlation between the
validation and test periods.
````

````plaintext
Thought process: 追加調査を通じて最適化戦略を検証する予定。

次に、プルーナーと最適化戦略について追加調査します。
````

**project_knowledge_search**

*Request*

````javascript
{
  "query": "Optuna pruner MedianPruner HyperbandPruner SuccessiveHalvingPruner early stopping validation loss",
  "max_text_results": 8
}
````

*Response*

````plaintext
03_Optuna.md
If the number of reported intermediate values from all trials at the current step
is less than `n_min_trials`, the trial will not be pruned. This can be used to ensure
that a minimum number of trials are run to completion without being pruned.




Methods




[`prune`](#optuna.pruners.MedianPruner.prune)(study,Â trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[ïƒ](#optuna.pruners.MedianPruner.prune)
Judge whether the trial should be pruned based on the reported values.


Note that this method is not supposed to be called by library users. Instead,
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) and [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) provide
user interfaces to implement pruning mechanism in an objective function.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) â€“ Study object of the target study.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) â€“ FrozenTrial object of the target trial.
Take a copy before modifying this object.



Returns:
A boolean value representing whether the trial should be pruned.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)

---

## optuna.pruners.SuccessiveHalvingPruner â€” Optuna 4.6.0 documentation
<a id="optunaprunersSuccessiveHalvingPruner-Optuna-460-documentation"></a>

- å…ƒURL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html

# optuna.pruners.SuccessiveHalvingPruner[ïƒ](#optuna-pruners-successivehalvingpruner)




*class *optuna.pruners.SuccessiveHalvingPruner(*min_resource='auto'*, *reduction_factor=4*, *min_early_stopping_rate=0*, *bootstrap_count=0*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_successive_halving.html#SuccessiveHalvingPruner)[ïƒ](#optuna.pruners.SuccessiveHalvingPruner)
Pruner using Asynchronous Successive Halving Algorithm.


[Successive Halving](https://proceedings.mlr.press/v51/jamieson16.html) is a bandit-based
algorithm to identify the best one among multiple configurations. This class implements an
asynchronous version of Successive Halving. Please refer to the paper of
[Asynchronous Successive Halving](https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf) for detailed descriptions.


Note that, this class does not take care of the parameter for the maximum
resource, referred to as \(R\) in the paper.
````

````plaintext
03_Optuna.md
See also


[User-Defined Pruner](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/006_user_defined_pruner.html#user-defined-pruner) tutorial could be helpful if you want to implement your own pruner classes.





[`BasePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner)


Base class for pruners.



[`MedianPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html#optuna.pruners.MedianPruner)


Pruner using the median stopping rule.



[`NopPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.NopPruner.html#optuna.pruners.NopPruner)


Pruner which never prunes trials.



[`PatientPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.PatientPruner.html#optuna.pruners.PatientPruner)


Pruner which wraps another pruner with tolerance.



[`PercentilePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.PercentilePruner.html#optuna.pruners.PercentilePruner)


Pruner to keep the specified percentile of the trials.



[`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner)


Pruner using Asynchronous Successive Halving Algorithm.



[`HyperbandPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html#optuna.pruners.HyperbandPruner)


Pruner using Hyperband.



[`ThresholdPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.ThresholdPruner.html#optuna.pruners.ThresholdPruner)


Pruner to detect outlying metrics of the trials.



[`WilcoxonPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.WilcoxonPruner.html#optuna.pruners.WilcoxonPruner)


Pruner based on the [Wilcoxon signed-rank test](https://en.wikipedia.org/w/index.php?title=Wilcoxon_signed-rank_test&oldid=1195011212).

---

## optuna.pruners.MedianPruner â€” Optuna 4.6.0 documentation
<a id="optunaprunersMedianPruner-Optuna-460-documentation"></a>

- å…ƒURL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html

# optuna.pruners.MedianPruner[ïƒ](#optuna-pruners-medianpruner)




*class *optuna.pruners.MedianPruner(*n_startup_trials=5*, *n_warmup_steps=0*, *interval_steps=1*, ***, *n_min_trials=1*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_median.html#MedianPruner)[ïƒ](#optuna.pruners.MedianPruner)
Pruner using the median stopping rule.


Prune if the trialâ€™s best intermediate result is worse than median of intermediate results of
previous trials at the same step. It stops unpromising trials early based on the
intermediate results compared against the median of previous completed trials.



The pruner handles NaN values in the following manner:1.
````

````plaintext
03_Optuna.md
Note


- In the Hyperband paper, the counterpart of [`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler)
is used.
- Optuna uses [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) by default.
- [The benchmark result](https://github.com/optuna/optuna/pull/828#issuecomment-575457360)
shows that [`optuna.pruners.HyperbandPruner`](#optuna.pruners.HyperbandPruner) supports both samplers.




Note


If you use `HyperbandPruner` with [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler),
itâ€™s recommended to consider setting larger `n_trials` or `timeout` to make full use of
the characteristics of [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler)
because [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) uses some (by default, \(10\))
[`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)s for its startup.


As Hyperband runs multiple [`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner) and collects
trials based on the current [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)â€˜s bracket ID, each bracket
needs to observe more than \(10\) [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)s
for [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) to adapt its search space.


Thus, for example, if `HyperbandPruner` has \(4\) pruners in it,
at least \(4 \times 10\) trials are consumed for startup.




Note


Hyperband has several [`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner)s. Each
[`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner) is referred to as â€œbracketâ€ in the
original paper. The number of brackets is an important factor to control the early
stopping behavior of Hyperband and is automatically determined by `min_resource`,
`max_resource` and `reduction_factor` as
\(\mathrm{The\ number\ of\ brackets} =
\mathrm{floor}(\log_{\texttt{reduction}\_\texttt{factor}}
(\frac{\texttt{max}\_\texttt{resource}}{\texttt{min}\_\texttt{resource}})) + 1\).
````

````plaintext
URL
callbacks/raytune/",
"https://www.kaggle.com/code/moritzm00/xgboost-hyperparameter-tuning-with-ray-tune",
"https://arxiv.org/abs/1807.05118",
"https://optuna.org/",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.load_study.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.QMCSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html",
"https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html",
"https://optuna.readthedocs.io/en/stable/reference/pruners.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.ThresholdPruner.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.PatientPruner.html",
"https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/006_user_defined_pruner.html",
"https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.TrialPruned.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.storages.RetryFailedTrialCallback.html",
"https://optuna.readthedocs.io/en/stable/reference/generated/optuna.copy_study.html"
]
len(URLS)
````

````plaintext
03_Optuna.md
Note that this method is not supposed to be called by library users. Instead,
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) and [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) provide
user interfaces to implement pruning mechanism in an objective function.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) â€“ Study object of the target study.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) â€“ FrozenTrial object of the target trial.
Take a copy before modifying this object.



Returns:
A boolean value representing whether the trial should be pruned.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)

---

## optuna.pruners.HyperbandPruner â€” Optuna 4.6.0 documentation
<a id="optunaprunersHyperbandPruner-Optuna-460-documentation"></a>

- å…ƒURL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html

# optuna.pruners.HyperbandPruner[ïƒ](#optuna-pruners-hyperbandpruner)




*class *optuna.pruners.HyperbandPruner(*min_resource=1*, *max_resource='auto'*, *reduction_factor=3*, *bootstrap_count=0*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_hyperband.html#HyperbandPruner)[ïƒ](#optuna.pruners.HyperbandPruner)
Pruner using Hyperband.


As SuccessiveHalving (SHA) requires the number of configurations
\(n\) as its hyperparameter.  For a given finite budget \(B\),
all the configurations have the resources of \(B \over n\) on average.
As you can see, there will be a trade-off of \(B\) and \(B \over n\).
[Hyperband](http://www.jmlr.org/papers/volume18/16-558/16-558.pdf) attacks this trade-off
by trying different \(n\) values for a fixed budget.



Note


- In the Hyperband paper, the counterpart of [`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler)
is used.
- Optuna uses [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) by default.
- [The benchmark result](https://github.com/optuna/optuna/pull/828#issuecomment-575457360)
shows that [`optuna.pruners.HyperbandPruner`](#optuna.pruners.HyperbandPruner) supports both samplers.
````

````plaintext
03_Optuna.md
Prune if the trialâ€™s best intermediate result is worse than median of intermediate results of
previous trials at the same step. It stops unpromising trials early based on the
intermediate results compared against the median of previous completed trials.



The pruner handles NaN values in the following manner:1. If all intermediate values of the current trial are NaN, the trial will be pruned.
2. During the median calculation across completed trials, NaN values are ignored.
Only valid numeric values are considered.




Example


We minimize an objective function with the median stopping rule.


`​`​`
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)
classes = np.unique(y)


def objective(trial):
    alpha = trial.suggest_float("alpha", 0.0, 1.0)
    clf = SGDClassifier(alpha=alpha)
    n_train_iter = 100

    for step in range(n_train_iter):
        clf.partial_fit(X_train, y_train, classes=classes)

        intermediate_value = clf.score(X_valid, y_valid)
        trial.report(intermediate_value, step)

        if trial.should_prune():
            raise optuna.TrialPruned()

    return clf.score(X_valid, y_valid)


study = optuna.create_study(
    direction="maximize",
    pruner=optuna.pruners.MedianPruner(
        n_startup_trials=5, n_warmup_steps=30, interval_steps=10
    ),
)
study.optimize(objective, n_trials=20)
`​`​`




Parameters:
- **n_startup_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)) â€“ Pruning is disabled until the given number of trials finish in the same study.
- **n_warmup_steps** ([*int*](https://docs.python.org/3/library/functions.html#int)) â€“ Pruning is disabled until the trial exceeds the given number of step. Note that
this feature assumes that `step` starts at zero.
- **interval_steps** ([*int*](https://docs.python.org/3/library/functions.html#int)) â€“ Interval in number of steps between the pruning checks, offset by the warmup steps.
If no value has been reported at the time of a pruning check, that particular check
will be postponed until a value is reported.
- **n_min_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)) â€“ Minimum number of reported trial results at a step to judge whether to prune.
If the number of reported intermediate values from all trials at the current step
is less than `n_min_trials`, the trial will not be pruned. This can be used to ensure
that a minimum number of trials are run to completion without being pruned.




Methods




[`prune`](#optuna.pruners.MedianPruner.prune)(study,Â trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[ïƒ](#optuna.pruners.MedianPruner.prune)
Judge whether the trial should be pruned based on the reported values.
````

````plaintext
03_Optuna.md
# Optuna ãƒ‰ã‚­ãƒ¥ãƒ¡ãƒ³ãƒˆã¾ã¨ã‚ï¼ˆOptunaã®ã¿å®Ÿè¡Œï¼‰

- æŠ½å‡ºæ—¥æ™‚: 2025-11-12 11:44
- ä»¶æ•°: 25

## ç›®æ¬¡
1. [optuna.samplers â€” Optuna 4.6.0 documentation](#optunasamplers-Optuna-460-documentation)
2. [Callback for Study.optimize â€” Optuna 4.6.0 documentation](#Callback-for-Studyoptimize-Optuna-460-documentation)
3. [Optuna - A hyperparameter optimization framework](#Optuna-A-hyperparameter-optimization-framework)
4. [optuna.study.Study â€” Optuna 4.6.0 documentation](#optunastudyStudy-Optuna-460-documentation)
5. [optuna.trial.Trial â€” Optuna 4.6.0 documentation](#optunatrialTrial-Optuna-460-documentation)
6. [optuna.study.create_study â€” Optuna 4.6.0 documentation](#optunastudycreate_study-Optuna-460-documentation)
7. [optuna.study.load_study â€” Optuna 4.6.0 documentation](#optunastudyload_study-Optuna-460-documentation)
8. [optuna.samplers.BaseSampler â€” Optuna 4.6.0 documentation](#optunasamplersBaseSampler-Optuna-460-documentation)
9. [optuna.samplers.TPESampler â€” Optuna 4.6.0 documentation](#optunasamplersTPESampler-Optuna-460-documentation)
10. [optuna.samplers.CmaEsSampler â€” Optuna 4.6.0 documentation](#optunasamplersCmaEsSampler-Optuna-460-documentation)
11. [optuna.samplers.QMCSampler â€” Optuna 4.6.0 documentation](#optunasamplersQMCSampler-Optuna-460-documentation)
12. [optuna.samplers.RandomSampler â€” Optuna 4.6.0 documentation](#optunasamplersRandomSampler-Optuna-460-documentation)
13. [optuna.samplers.GPSampler â€” Optuna 4.6.0 documentation](#optunasamplersGPSampler-Optuna-460-documentation)
14. [optuna.samplers.NSGAIISampler â€” Optuna 4.6.0 documentation](#optunasamplersNSGAIISampler-Optuna-460-documentation)
15. [optuna.pruners â€” Optuna 4.6.0 documentation](#optunapruners-Optuna-460-documentation)
16. [optuna.pruners.MedianPruner â€” Optuna 4.6.0 documentation](#optunaprunersMedianPruner-Optuna-460-documentation)
17. [optuna.pruners.SuccessiveHalvingPruner â€” Optuna 4.6.0 documentation](#optunaprunersSuccessiveHalvingPruner-Optuna-460-documentation)
18. [optuna.pruners.HyperbandPruner â€” Optuna 4.6.0 documentation](#optunaprunersHyperbandPruner-Optuna-460-documentation)
19. [optuna.pruners.ThresholdPruner â€” Optuna 4.6.0 documentation](#optunaprunersThresholdPruner-Optuna-460-documentation)
20. [optuna.pruners.PatientPruner â€” Optuna 4.6.0 documentation](#optunaprunersPatientPruner-Optuna-460-documentation)
21. [User-Defined Pruner â€” Optuna 4.6.0 documentation](#User-Defined-Pruner-Optuna-460-documentation)
22. [Ask-and-Tell Interface â€” Optuna 4.6.0 documentation](#Ask-and-Tell-Interface-Optuna-460-documentation)
23. [optuna.TrialPruned â€” Optuna 4.6.0 documentation](#optunaTrialPruned-Optuna-460-documentation)
24. [optuna.storages.RetryFailedTrialCallback â€” Optuna 4.6.0 documentation](#optunastoragesRetryFailedTrialCallback-Optuna-460-documentation)
25.
````

````plaintext
03_Optuna.md
This pruner monitors intermediate values in a trial and prunes the trial if the improvement in
the intermediate values after a patience period is less than a threshold.



The pruner handles NaN values in the following manner:1. If all intermediate values before or during the patient period are NaN, the trial will
not be pruned
2. During the pruning calculations, NaN values are ignored. Only valid numeric values are
considered.




Example


`​`​`
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)
classes = np.unique(y)


def objective(trial):
    alpha = trial.suggest_float("alpha", 0.0, 1.0)
    clf = SGDClassifier(alpha=alpha)
    n_train_iter = 100

    for step in range(n_train_iter):
        clf.partial_fit(X_train, y_train, classes=classes)

        intermediate_value = clf.score(X_valid, y_valid)
        trial.report(intermediate_value, step)

        if trial.should_prune():
            raise optuna.TrialPruned()

    return clf.score(X_valid, y_valid)


study = optuna.create_study(
    direction="maximize",
    pruner=optuna.pruners.PatientPruner(optuna.pruners.MedianPruner(), patience=1),
)
study.optimize(objective, n_trials=20)
`​`​`




Parameters:
- **wrapped_pruner** ([*BasePruner*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner)* | **None*) â€“ Wrapped pruner to perform pruning when [`PatientPruner`](#optuna.pruners.PatientPruner) allows a
trial to be pruned. If it is [`None`](https://docs.python.org/3/library/constants.html#None), this pruner is equivalent to
early-stopping taken the intermediate values in the individual trial.
- **patience** ([*int*](https://docs.python.org/3/library/functions.html#int)) â€“ Pruning is disabled until the objective doesnâ€™t improve for
`patience` consecutive steps.
- **min_delta** ([*float*](https://docs.python.org/3/library/functions.html#float)) â€“ Tolerance value to check whether or not the objective improves.
This value should be non-negative.





Note


Added in v2.8.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.8.0](https://github.com/optuna/optuna/releases/tag/v2.8.0).



Methods




[`prune`](#optuna.pruners.PatientPruner.prune)(study,Â trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_patient.html#PatientPruner.prune)[ïƒ](#optuna.pruners.PatientPruner.prune)
Judge whether the trial should be pruned based on the reported values.


Note that this method is not supposed to be called by library users.
````

````plaintext
Thought process

非常に良い情報が得られました。次に、実装設計のためにMLflowとの統合パターンも確認します。
````

**project_knowledge_search**

*Request*

````javascript
{
  "query": "MLflow tracking experiment logging hyperparameter model registry pytorch lightning",
  "max_text_results": 6
}
````

*Response*

````plaintext
URL
ps://nixtlaverse.nixtla.io/neuralforecast/common.base_auto.html',
'https://nixtlaverse.nixtla.io/neuralforecast/common.scalers.html',
'https://nixtlaverse.nixtla.io/neuralforecast/common.modules.html',
'https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html',
'https://nixtlaverse.nixtla.io/neuralforecast/utils.html',
'https://discuss.ray.io/t/custom-path-for-ray-results-without-using-tune/13223',
'https://discuss.ray.io/',
'https://mlflow.org/docs/latest/ml/tracking/',
'https://mlflow.org/docs/latest/ml/tracking/tracking-api/',
'https://mlflow.org/docs/latest/ml/tracking/#mlflow-tracking-apis',
'https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/',
'https://mlflow.org/docs/latest/ml/tracking/#backend-store',
'https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/',
'https://mlflow.org/docs/latest/ml/tracking/#artifact-stores',
'https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/',
'https://mlflow.org/docs/latest/ml/tracking/#tracking_server',
'https://mlflow.org/docs/latest/ml/tracking/quickstart/',
'https://mlflow.org/docs/latest/ml/tracking/tutorials/local-database/',
'https://mlflow.org/docs/latest/ml/tracking/tutorials/remote-server/',
'https://mlflow.org/docs/latest/ml/tracking/#how-can-i-organize-many-mlflow-runs-neatly',
'https://mlflow.org/docs/latest/ml/tracking/#can-i-directly-access-remote-storage-without-running-the-tracking-server',
'https://mlflow.org/docs/latest/ml/model-registry/',
'https://mlflow.org/docs/latest/ml/',
'https://docs.databricks.com/aws/en/mlflow/',
'https://mlflow.org/docs/latest/genai/',
'https://docs.databricks.com/aws/en/mlflow3/genai/',
'https://mlflow.org/docs/latest/api_reference/index.html',
'https://mlflow.org/docs/latest/self-hosting/',
'https://mlflow.org/docs/latest/community/',
'https://github.com/mlflow/mlflow',
'https://lightning.ai/docs/pytorch/stable/extensions/logging.html',
'https://github.com/Lightning-AI/pytorch-lightning#looking-for-gpus',
'https://lightning.ai/?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme',
'https://lightning.ai/pricing?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme',
'https://lightning.ai/clusters?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme',
'https://lightnin
````

````plaintext
07_Lightning.md
`​`​`
from lightning.pytorch.callbacks.progress import TQDMProgressBar


class CustomProgressBar(TQDMProgressBar):
    def get_metrics(self, *args, **kwargs):
        # don't show the version number
        items = super().get_metrics(*args, **kwargs)
        items.pop("v_num", None)
        return items
`​`​`







## Configure Console Logging[Â¶](#configure-console-logging)


Lightning logs useful information about the training process and user warnings to the console.
You can retrieve the Lightning console logger and change it to your liking. For example, adjust the logging level
or redirect output for certain modules to log files:


`​`​`
import logging

# configure logging at the root level of Lightning
logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)

# configure logging on module level, redirect to file
logger = logging.getLogger("lightning.pytorch.core")
logger.addHandler(logging.FileHandler("core.log"))
`​`​`



Read more about custom Python logging [here](https://docs.python.org/3/library/logging.html).





## Logging Hyperparameters[Â¶](#logging-hyperparameters)


When training a model, it is useful to know what hyperparams went into that model.
When Lightning creates a checkpoint, it stores a key `"hyper_parameters"` with the hyperparams.


`​`​`
lightning_checkpoint = torch.load(filepath, map_location=lambda storage, loc: storage)
hyperparams = lightning_checkpoint["hyper_parameters"]
`​`​`



Some loggers also allow logging the hyperparams used in the experiment. For instance,
when using the `TensorBoardLogger`, all hyperparams will show
in the hparams tab at [`torch.utils.tensorboard.writer.SummaryWriter.add_hparams()`](https://docs.pytorch.org/docs/stable/tensorboard.html#torch.utils.tensorboard.writer.SummaryWriter.add_hparams).



Note


If you want to track a metric in the tensorboard hparams tab, log scalars to the key `hp_metric`. If tracking multiple metrics, initialize `TensorBoardLogger` with `default_hp_metric=False` and call `log_hyperparams` only once with your metric keys and initial values. Subsequent updates can simply be logged to the metric keys. Refer to the examples below for setting up proper hyperparams metrics tracking within the [LightningModule](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html).


`​`​`
# Using default_hp_metric
def validation_step(self, batch, batch_idx):
    self.log("hp_metric", some_scalar)


# Using custom or multiple metrics (default_hp_metric=False)
def on_train_start(self):
    self.logger.log_hyperparams(self.hparams, {"hp/metric_1": 0, "hp/metric_2": 0})


def validation_step(self, batch, batch_idx):
    self.log("hp/metric_1", some_scalar_1)
    self.log("hp/metric_2", some_scalar_2)
`​`​`



In the example, using `"hp/"` as a prefix allows for the metrics to be grouped under â€œhpâ€ in the tensorboard scalar tab where you can collapse them.
````

````plaintext
04_MLflow.md
From experiment tracking and model versioning to deployment and monitoring, MLflow streamlines every aspect of the ML lifecycle. Whether you're working with scikit-learn models, training deep neural networks, or managing complex ML pipelines, MLflow provides the tools you need to build reliable, scalable machine learning systems.


Explore the core MLflow capabilities and integrations below to enhance your ML development workflow!


- Tracking & Experiments
- Model Registry
- Model Deployment
- ML Library Integrations
- Model Evaluation

### Track experiments and manage your ML development[â€‹](#track-experiments-and-manage-your-ml-development)

#### Core Features[â€‹](#core-features)

**MLflow Tracking** provides comprehensive experiment logging, parameter tracking, metrics visualization, and artifact management.

**Key Benefits:**

- **Experiment Organization**: Track and compare multiple model experiments
- **Metric Visualization**: Built-in plots and charts for model performance
- **Artifact Storage**: Store models, plots, and other files with each run
- **Collaboration**: Share experiments and results across teams

#### Guides[â€‹](#guides)

[Getting Started with Tracking](https://mlflow.org/docs/latest/ml/tracking/quickstart/)

[Advanced Tracking Features](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)

[Autologging for Popular Libraries](https://mlflow.org/docs/latest/ml/tracking/autolog/)

![MLflow Tracking](https://mlflow.org/docs/latest/assets/images/tracking-metrics-ui-temp-ffc0da57b388076730e20207dbd7f9c4.png)

### Manage model versions and lifecycle[â€‹](#manage-model-versions-and-lifecycle)

#### Core Features[â€‹](#core-features-1)

**MLflow Model Registry** provides centralized model versioning, stage management, and model lineage tracking.

**Key Benefits:**

- **Version Control**: Track model versions with automatic lineage
- **Stage Management**: Promote models through staging, production, and archived stages
- **Collaboration**: Team-based model review and approval workflows
- **Model Discovery**: Search and discover models across your organization

#### Guides[â€‹](#guides-1)

[Model Registry Introduction](https://mlflow.org/docs/latest/ml/model-registry/)

![MLflow Model Registry](https://mlflow.org/docs/latest/assets/images/oss_registry_3_overview-daec63473b4d7bbf47c559600bf5c35d.png)

### Deploy models to production environments[â€‹](#deploy-models-to-production-environments)

#### Core Features[â€‹](#core-features-2)

**MLflow Deployment** supports multiple deployment targets including REST APIs, cloud platforms, and edge devices.
````

````plaintext
07_Lightning.md
To avoid this, you can specify the `batch_size` inside the `self.log(... batch_size=batch_size)` call.


`​`​`
def training_step(self, batch, batch_idx):
    # extracts the batch size from `batch`
    self.log("train_loss", loss, on_epoch=True)


def validation_step(self, batch, batch_idx):
    # uses `batch_size=10`
    self.log("val_loss", loss, batch_size=10)
`​`​`





Note


- The above config for `validation` applies for `test` hooks as well.
- Setting `on_epoch=True` will cache all your logged values during the full training epoch and perform a
reduction in `on_train_epoch_end`. We recommend using [TorchMetrics](https://torchmetrics.readthedocs.io/), when working with custom reduction.
- Setting both `on_step=True` and `on_epoch=True` will create two keys per metric you log with
suffix `_step` and `_epoch` respectively. You can refer to these keys e.g. in the monitor
argument of [`ModelCheckpoint`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint) or in the graphs plotted to the logger of your choice.



If your work requires to log in an unsupported method, please open an issue with a clear description of why it is blocking you.




### Manual Logging Non-Scalar Artifacts[Â¶](#manual-logging-non-scalar-artifacts)


If you want to log anything that is not a scalar, like histograms, text, images, etc., you may need to use the logger object directly.


`​`​`
def training_step(self):
    ...
    # the logger you used (in this case tensorboard)
    tensorboard = self.logger.experiment
    tensorboard.add_image()
    tensorboard.add_histogram(...)
    tensorboard.add_figure(...)
`​`​`







## Make a Custom Logger[Â¶](#make-a-custom-logger)


You can implement your own logger by writing a class that inherits from [`Logger`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.loggers.logger.html#lightning.pytorch.loggers.logger.Logger).
Use the `rank_zero_experiment()` and `rank_zero_only()` decorators to make sure that only the first process in DDP training creates the experiment and logs the data respectively.


`​`​`
from lightning.pytorch.loggers.logger import Logger, rank_zero_experiment
from lightning.pytorch.utilities import rank_zero_only


class MyLogger(Logger):
    @property
    def name(self):
        return "MyLogger"

    @property
    def version(self):
        # Return the experiment version, int or str.
        return "0.1"

    @rank_zero_only
    def log_hyperparams(self, params):
        # params is an argparse.Namespace
        # your code to record hyperparameters goes here
        pass

    @rank_zero_only
    def log_metrics(self, metrics, step):
        # metrics is a dictionary of metric names and values
        # your code to record metrics goes here
        pass

    @rank_zero_only
    def save(self):
        # Optional.
````

````plaintext
04_MLflow.md
# MLflow

- æŠ½å‡ºæ—¥æ™‚: 2025-11-12 10:56
- ä»¶æ•°: 14

## ç›®æ¬¡
1. [MLflow Tracking | MLflow](#MLflow-Tracking-MLflow)
2. [MLflow Tracking APIs | MLflow](#MLflow-Tracking-APIs-MLflow)
3. [Backend Stores | MLflow](#Backend-Stores-MLflow)
4. [Artifact Stores | MLflow](#Artifact-Stores-MLflow)
5. [MLflow Tracking Server | MLflow](#MLflow-Tracking-Server-MLflow)
6. [MLflow Tracking Quickstart | MLflow](#MLflow-Tracking-Quickstart-MLflow)
7. [Tracking Experiments with Local Database | MLflow](#Tracking-Experiments-with-Local-Database-MLflow)
8. [Remote Experiment Tracking with MLflow Tracking Server | MLflow](#Remote-Experiment-Tracking-with-MLflow-Tracking-Server-MLflow)
9. [MLflow Model Registry | MLflow](#MLflow-Model-Registry-MLflow)
10. [MLflow: A Tool for Managing the Machine Learning Lifecycle | MLflow](#MLflow-A-Tool-for-Managing-the-Machine-Learning-Lifecycle-MLflow)
11. [MLflow for GenAI | MLflow](#MLflow-for-GenAI-MLflow)
12. [MLflow API Docs](#MLflow-API-Docs)
13. [Self Hosting Overview | MLflow](#Self-Hosting-Overview-MLflow)
14. [Community | MLflow](#Community-MLflow)


---

## MLflow Tracking | MLflow
<a id="MLflow-Tracking-MLflow"></a>

- å…ƒURL: https://mlflow.org/docs/latest/ml/tracking/

The MLflow Tracking is an API and UI for logging parameters, code versions, metrics, and output files

On this page# MLflow Tracking


The MLflow Tracking is an API and UI for logging parameters, code versions, metrics, and output files
when running your machine learning code and for later visualizing the results.
MLflow Tracking provides [Python](https://mlflow.org/docs/latest/api_reference/python_api/index.html)
, [REST](https://mlflow.org/docs/latest/api_reference/rest-api.html)
, [R](https://mlflow.org/docs/latest/api_reference/R-api.html),
and [Java](https://mlflow.org/docs/latest/api_reference/java_api/index.html) APIs.


![](https://mlflow.org/docs/latest/assets/images/tracking-metrics-ui-temp-ffc0da57b388076730e20207dbd7f9c4.png)

A screenshot of the MLflow Tracking UI, showing a plot of validation loss metrics during model training.
## Quickstart[â€‹](#quickstart)


If you haven't used MLflow Tracking before, we strongly recommend going through the following quickstart tutorial.


[MLflow Tracking QuickstartA great place to start to learn the fundamentals of MLflow Tracking! Learn in 5 minutes how to log, register, and load a model for inference.](https://mlflow.org/docs/latest/ml/tracking/quickstart/)
## Concepts[â€‹](#concepts)


### Runs[â€‹](#runs)


MLflow Tracking is organized around the concept of **runs**, which are executions of some piece of
data science code, for example, a single `python train.py` execution. Each run records metadata
(various information about your run such as metrics, parameters, start and end times) and artifacts
(output files from the run such as model weights, images, etc).


### Models[â€‹](#models)


Models represent the trained machine learning artifacts that are produced during your runs.
````

````plaintext
07_Lightning.md
return "0.1"

    @rank_zero_only
    def log_hyperparams(self, params):
        # params is an argparse.Namespace
        # your code to record hyperparameters goes here
        pass

    @rank_zero_only
    def log_metrics(self, metrics, step):
        # metrics is a dictionary of metric names and values
        # your code to record metrics goes here
        pass

    @rank_zero_only
    def save(self):
        # Optional. Any code necessary to save logger data goes here
        pass

    @rank_zero_only
    def finalize(self, status):
        # Optional. Any code that needs to be run after training
        # finishes goes here
        pass
`​`​`



If you write a logger that may be useful to others, please send
a pull request to add it to Lightning!





## Control Logging Frequency[Â¶](#control-logging-frequency)



### Logging frequency[Â¶](#id2)


It may slow down training to log on every single batch. By default, Lightning logs every 50 rows, or 50 training steps.
To change this behaviour, set the `log_every_n_steps` [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer) flag.


`​`​`
k = 10
trainer = Trainer(log_every_n_steps=k)
`​`​`





### Log Writing Frequency[Â¶](#log-writing-frequency)


Individual logger implementations determine their flushing frequency. For example, on the
[`CSVLogger`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.loggers.csv_logs.html#lightning.pytorch.loggers.csv_logs.CSVLogger) you can set the flag `flush_logs_every_n_steps`.






## Progress Bar[Â¶](#progress-bar)


You can add any metric to the progress bar using [`log()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log)
method, setting `prog_bar=True`.


`​`​`
def training_step(self, batch, batch_idx):
    self.log("my_loss", loss, prog_bar=True)
`​`​`



You could learn more about progress bars supported by Lightning [here](https://lightning.ai/docs/pytorch/stable/common/progress_bar.html).



### Modifying the Progress Bar[Â¶](#modifying-the-progress-bar)


The progress bar by default already includes the training loss and version number of the experiment
if you are using a logger. These defaults can be customized by overriding the
`get_metrics()` hook in your logger.


`​`​`
from lightning.pytorch.callbacks.progress import TQDMProgressBar


class CustomProgressBar(TQDMProgressBar):
    def get_metrics(self, *args, **kwargs):
        # don't show the version number
        items = super().get_metrics(*args, **kwargs)
        items.pop("v_num", None)
        return items
`​`​`







## Configure Console Logging[Â¶](#configure-console-logging)


Lightning logs useful information about the training process and user warnings to the console.
You can retrieve the Lightning console logger and change it to your liking.
````

````plaintext
Thought process: Synthesized NeuralForecast backend configurations and architected comprehensive specification framework.

十分な情報が得られました。以下の情報を基に、詳細な要件定義兼機能設計仕様書を作成します。

収集した情報のサマリー：
1. NeuralForecastのAutoModelは `backend` パラメータで 'optuna' または 'ray' を選択できる
2. Optunaの場合：
   - サンプラー: TPESampler(デフォルト), RandomSampler, GridSampler, CmaEsSampler, NSGAIISampler, MOTPESampler, QMCSampler, BoTorchSampler
   - プルーナー: MedianPruner, HyperbandPruner, SuccessiveHalvingPruner等が利用可能で、デフォルトで有効
3. Ray Tuneの場合：
   - 検索アルゴリズム: BasicVariantGenerator(デフォルト), OptunaSearch, HyperOptSearch, BayesOptSearch等
   - スケジューラ: ASHAScheduler等を明示的に設定する必要あり（プルーナーはデフォルト無効）
4. 互換表によると、モデルごとに異なるドロップアウトキー名、スケーラー既定値、外生変数対応がある

要件定義書では以下を明記：
- 目標とKPI
- 制約条件
- 受入基準
- 実装計画
- アーキテクチャ設計
- データフロー
- エラーハンドリング
- テスト戦略
- 監視・ロギング戦略
````

プロジェクトナレッジから十分な情報が得られました。これをもとに詳細な要件定義兼機能設計仕様書を作成します。

---

# 業務用要件定義兼機能設計仕様書
## NeuralForecast AutoModels 最適化検索アルゴリズム自動選択システム

**バージョン**: v1.0.0  
**作成日**: 2025-11-12  
**ステータス**: Requirements & Design Phase

---

## 1. エグゼクティブサマリー

### 1.1 目的 (Goals)
```json
{
  "primary_goal": "NeuralForecast全AutoModelsに対し、選択されたbackend（Optuna/Ray）に応じて最適なsearch_algを自動選択・設定し、ハイパーパラメータ最適化の効率と精度を向上させる",
  "business_value": {
    "efficiency": "試行回数あたりの最適化収束速度を30%改善",
    "accuracy": "検証損失の平均値を5-10%削減",
    "usability": "ユーザーによる手動設定の工数を80%削減",
    "maintainability": "新モデル追加時の設定コストを75%削減"
  },
  "target_models": [
    "AutoRNN", "AutoLSTM", "AutoGRU", "AutoTCN", "AutoDeepAR",
    "AutoNBEATS", "AutoNBEATSx", "AutoTFT", "AutoVanillaTransformer",
    "AutoInformer", "AutoAutoformer", "AutoFEDformer", "AutoPatchTST",
    "AutoiTransformer", "AutoTimesNet", "AutoTimeMixer", "AutoRMoK",
    "AutoMLP", "AutoNHITS", "AutoDLinear", "AutoNLinear", "AutoTiDE",
    "AutoDeepNPTS", "AutoDilatedRNN", "AutoBiTCN", "AutoStemGNN"
  ]
}
```

### 1.2 主要KPI (Key Performance Indicators)
| 指標 | ベースライン | 目標値 | 測定方法 |
|------|--------------|--------|----------|
| **最適化収束速度** | 100試行で収束 | 70試行以内 | 検証損失が閾値到達までの試行数 |
| **最終精度 (SMAPE)** | 0.15 | 0.135以下 | テストセットでの平均SMAPE |
| **設定工数** | 15分/モデル | 3分/モデル | ユーザー操作時間の計測 |
| **システム信頼性** | N/A | 99.5%以上 | 成功率 = 成功実行数 / 全実行数 |
| **ログ完全性** | N/A | 100% | MLflow記録漏れ数 / 全実行数 |

---

## 2. 受入基準 (Acceptance Criteria)

### 2.1 機能要件
- [ ] **AC-F-001**: 全28種のAutoModelで、backend='optuna' 選択時に最適なOptunaサンプラーが自動設定される
- [ ] **AC-F-002**: 全28種のAutoModelで、backend='ray' 選択時に最適なRay検索アルゴリズム+スケジューラが自動設定される
- [ ] **AC-F-003**: モデル特性（連続空間/離散空間/多目的最適化）に応じたサンプラー選択ロジックが実装される
- [ ] **AC-F-004**: プルーナー/スケジューラのデフォルト設定がbackendごとに適切に構成される
- [ ] **AC-F-005**: 外生変数、ドロップアウト、スケーラーの互換性検証が起動前に実行される

### 2.2 非機能要件
- [ ] **AC-NF-001**: 設定ロジックの実行時間が50ms以下（P99）
- [ ] **AC-NF-002**: 全ハイパーパラメータ、中間メトリクス、アーティファクトがMLflowに記録される
- [ ] **AC-NF-003**: 設定エラー時に明確なエラーメッセージと推奨アクションが提示される
- [ ] **AC-NF-004**: 後方互換性: 既存の明示的設定（`search_alg=...`）を指定した場合は自動選択をスキップ
- [ ] **AC-NF-005**: ユニットテスト: 全AutoModelで最低3種のbackend/sampler組合せをカバー（カバレッジ>90%）

---

## 3. 制約条件 (Constraints)

### 3.1 技術的制約
```json
{
  "dependencies": {
    "neuralforecast": ">=1.6.0",
    "optuna": ">=4.0.0",
    "ray[tune]": ">=2.9.0",
    "mlflow": ">=2.10.0",
    "pytorch": ">=2.0.0",
    "pytorch-lightning": ">=2.1.0"
  },
  "compatibility": {
    "python": "3.9-3.11",
    "os": ["Linux", "macOS"],
    "gpu": "CUDA 11.8+ (optional)"
  },
  "resource_limits": {
    "memory_per_trial": "16GB max",
    "cpu_per_trial": "32 cores max",
    "gpu_per_trial": "1 GPU (optional)",
    "disk_artifact_size": "10GB max per experiment"
  }
}
```

### 3.2 ビジネス制約
- **予算**: 計算リソース費用は月$500以内（AWS/GCP基準）
- **納期**: MVP実装は4週間以内、完全版は8週間以内
- **セキュリティ**: Secrets（DB接続文字列、API Key）はHashiCorp Vault/AWS Secrets Manager経由
- **データプライバシー**: PII(個人識別情報)を含むデータセットは使用不可

---

## 4. アーキテクチャ設計

### 4.1 システムアーキテクチャ図

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ CLI/Notebook │  │  Config YAML │  │  REST API    │         │
│  └───────┬──────┘  └───────┬──────┘  └───────┬──────┘         │
└──────────┼─────────────────┼─────────────────┼────────────────┘
           │                 │                 │
           └────────┬────────┴────────┬────────┘
                    │                 │
         ┌──────────▼─────────────────▼─────────┐
         │   AutoModelFactory                    │
         │   ┌─────────────────────────────────┐ │
         │   │ validate_config()               │ │
         │   │ select_search_algorithm()       │ │
         │   │ configure_pruner_scheduler()    │ │
         │   └─────────────────────────────────┘ │
         └──────────┬─────────────────┬──────────┘
                    │                 │
      ┌─────────────▼──────┐    ┌────▼────────────────┐
      │ Optuna Backend     │    │ Ray Tune Backend    │
      │ ┌────────────────┐ │    │ ┌────────────────┐  │
      │ │TPESampler      │ │    │ │OptunaSearch    │  │
      │ │CmaEsSampler    │ │    │ │HyperOptSearch  │  │
      │ │QMCSampler      │ │    │ │+ASHAScheduler  │  │
      │ │MedianPruner    │ │    │ │+PopulationBased│  │
      │ │HyperbandPruner │ │    │ │                │  │
      │ └────────────────┘ │    │ └────────────────┘  │
      └──────────┬─────────┘    └─────────┬───────────┘
                 │                        │
                 └────────┬───────────────┘
                          │
                ┌─────────▼──────────────┐
                │  MLflow Tracking       │
                │  ┌───────────────────┐ │
                │  │ Experiments       │ │
                │  │ Runs              │ │
                │  │ Metrics           │ │
                │  │ Parameters        │ │
                │  │ Artifacts         │ │
                │  │ Model Registry    │ │
                │  └───────────────────┘ │
                └────────────────────────┘
```

### 4.2 主要コンポーネント

#### 4.2.1 AutoModelFactory
**責務**: モデル生成、設定検証、最適化アルゴリズム選択の統括

```python
from typing import Dict, Any, Optional, Union
from enum import Enum
import optuna
from ray import tune

class Backend(str, Enum):
    OPTUNA = "optuna"
    RAY = "ray"

class OptimizationType(str, Enum):
    CONTINUOUS = "continuous"  # 連続空間（TPE/CmaEs推奨）
    DISCRETE = "discrete"      # 離散空間（Random/Grid推奨）
    MIXED = "mixed"            # 混合空間（TPE/Optuna推奨）
    MULTI_OBJECTIVE = "multi_objective"  # 多目的（NSGA-II推奨）

class AutoModelFactory:
    """
    NeuralForecast AutoModels用のファクトリークラス。
    
    責務:
    - モデル設定の検証
    - 最適化アルゴリズムの自動選択
    - backend固有の設定（プルーナー/スケジューラ）
    - MLflow統合
    """
    
    def __init__(
        self,
        model_name: str,
        backend: Backend,
        optimization_type: Optional[OptimizationType] = None,
        mlflow_tracking_uri: Optional[str] = None,
        experiment_name: Optional[str] = None
    ):
        self.model_name = model_name
        self.backend = backend
        self.optimization_type = optimization_type or self._infer_optimization_type()
        self.mlflow_tracking_uri = mlflow_tracking_uri
        self.experiment_name = experiment_name or f"auto_{model_name.lower()}"
        
    def create_model(self, **kwargs) -> Any:
        """
        AutoModelインスタンスを生成。
        
        Workflow:
        1. 設定検証 (validate_config)
        2. search_alg自動選択 (select_search_algorithm)
        3. pruner/scheduler設定 (configure_pruner_scheduler)
        4. MLflow初期化
        5. モデル生成
        """
        # 実装は後述
        pass
    
    def validate_config(self, config: Dict[str, Any]) -> None:
        """
        設定の互換性を検証。
        
        チェック項目:
        - モデル×損失関数の互換性
        - ドロップアウトキー名の正当性
        - 外生変数の有効性
        - スケーラー種別の整合性
        """
        pass
    
    def select_search_algorithm(self) -> Union[optuna.samplers.BaseSampler, Any]:
        """
        最適化タイプとbackendに基づいてsearch_algを選択。
        
        選択ルール（Optuna）:
        - CONTINUOUS → TPESampler(multivariate=True)
        - DISCRETE → GridSampler or RandomSampler
        - MIXED → TPESampler(default)
        - MULTI_OBJECTIVE → NSGAIISampler
        
        選択ルール（Ray）:
        - CONTINUOUS → OptunaSearch(TPESampler)
        - DISCRETE → BasicVariantGenerator
        - MIXED → OptunaSearch or HyperOptSearch
        - MULTI_OBJECTIVE → MOAQ or custom
        """
        pass
    
    def configure_pruner_scheduler(self) -> Dict[str, Any]:
        """
        プルーナー（Optuna）またはスケジューラ（Ray）を設定。
        
        Optuna既定:
        - MedianPruner(n_startup_trials=5, n_warmup_steps=10, interval_steps=5)
        
        Ray既定:
        - ASHAScheduler(max_t=max_steps, grace_period=50, reduction_factor=2)
        """
        pass
```

#### 4.2.2 SearchAlgorithmSelector
**責務**: 最適化アルゴリズムの選択ロジックをカプセル化

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ModelCharacteristics:
    """モデル特性を表現するデータクラス"""
    has_continuous_params: bool
    has_discrete_params: bool
    has_categorical_params: bool
    supports_multi_objective: bool
    typical_search_space_size: int  # 探索空間のおおよそのサイズ
    dropout_key: Optional[str]  # "dropout" or "lstm_dropout" etc.
    default_scaler: str  # "identity", "standard", "robust", "minmax"

class SearchAlgorithmSelector:
    """
    モデル特性に基づいて最適なsearch_algを選択。
    
    選択基準:
    - 探索空間の性質（連続/離散/混合）
    - 探索空間のサイズ（小:Grid, 中:TPE, 大:Random+Pruning）
    - 多目的最適化の要否
    - バックエンドの制約
    """
    
    # モデル別特性マップ（互換表から生成）
    MODEL_CHARACTERISTICS: Dict[str, ModelCharacteristics] = {
        "AutoAutoformer": ModelCharacteristics(
            has_continuous_params=True,
            has_discrete_params=True,
            has_categorical_params=True,
            supports_multi_objective=False,
            typical_search_space_size=10000,
            dropout_key="dropout",
            default_scaler="identity"
        ),
        "AutoDeepAR": ModelCharacteristics(
            has_continuous_params=True,
            has_discrete_params=True,
            has_categorical_params=True,
            supports_multi_objective=False,
            typical_search_space_size=5000,
            dropout_key="lstm_dropout",
            default_scaler="identity"
        ),
        # ... 全モデルの定義
    }
    
    def select_for_optuna(
        self,
        model_name: str,
        user_override: Optional[Any] = None
    ) -> optuna.samplers.BaseSampler:
        """
        Optunaバックエンド用のサンプラー選択。
        
        優先順位:
        1. ユーザー明示指定（user_override）
        2. 最適化タイプベースの推奨
        3. デフォルト（TPESampler）
        """
        if user_override is not None:
            return user_override
        
        char = self.MODEL_CHARACTERISTICS.get(model_name)
        if char is None:
            raise ValueError(f"Unknown model: {model_name}")
        
        # 選択ロジック
        if char.typical_search_space_size < 100:
            # 小空間 → 全探索
            return optuna.samplers.GridSampler(...)
        elif char.supports_multi_objective:
            return optuna.samplers.NSGAIISampler()
        elif char.has_continuous_params and not char.has_discrete_params:
            # 連続のみ → CmaEs（局所的最適化）
            return optuna.samplers.CmaEsSampler()
        else:
            # デフォルト → TPE（バランス型）
            return optuna.samplers.TPESampler(
                n_startup_trials=10,
                multivariate=True,
                constant_liar=True
            )
    
    def select_for_ray(
        self,
        model_name: str,
        user_override: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Ray Tuneバックエンド用の検索器+スケジューラ選択。
        
        返り値:
        {
            "search_alg": ray.tune.search.<Searcher>,
            "scheduler": ray.tune.schedulers.<Scheduler>,
            "scheduler_config": {...}
        }
        """
        if user_override is not None:
            return {"search_alg": user_override, "scheduler": None}
        
        char = self.MODEL_CHARACTERISTICS.get(model_name)
        if char is None:
            raise ValueError(f"Unknown model: {model_name}")
        
        # 選択ロジック
        from ray.tune.search.optuna import OptunaSearch
        from ray.tune.schedulers import ASHAScheduler
        
        if char.typical_search_space_size < 100:
            search_alg = tune.search.BasicVariantGenerator()
            scheduler = None
        elif char.has_continuous_params:
            # 連続空間 → Optuna TPEをRay経由で利用
            search_alg = OptunaSearch(
                sampler=optuna.samplers.TPESampler(multivariate=True)
            )
            scheduler = ASHAScheduler(
                max_t=1000,
                grace_period=50,
                reduction_factor=2
            )
        else:
            # 離散/混合 → HyperOpt
            search_alg = tune.search.HyperOptSearch()
            scheduler = ASHAScheduler(max_t=1000, grace_period=50)
        
        return {
            "search_alg": search_alg,
            "scheduler": scheduler,
            "scheduler_config": {"metric": "valid_loss", "mode": "min"}
        }
```

---

## 5. データフロー設計

### 5.1 典型的な実行フロー（Optunaバックエンド）

```
[User Input]
  ├─ model_name: "AutoTFT"
  ├─ h: 12
  ├─ backend: "optuna"
  ├─ config: {...}  # オプション
  └─ search_alg: None  # 自動選択を期待
          │
          ▼
[AutoModelFactory.create_model()]
  ├─ validate_config(config)
  │   ├─ Check: loss compatible with model
  │   ├─ Check: dropout_key exists if dropout_supported=True
  │   ├─ Check: exog_list valid
  │   └─ Raise ValidationError if fails
  │
  ├─ select_search_algorithm()
  │   ├─ Lookup MODEL_CHARACTERISTICS["AutoTFT"]
  │   ├─ Determine: MIXED optimization (continuous+discrete+categorical)
  │   └─ Return: TPESampler(n_startup_trials=10, multivariate=True)
  │
  ├─ configure_pruner_scheduler()
  │   └─ Return: MedianPruner(n_startup_trials=5, n_warmup_steps=10)
  │
  ├─ Initialize MLflow
  │   ├─ set_tracking_uri()
  │   ├─ set_experiment("auto_tft_2025")
  │   └─ start_run()
  │
  └─ Instantiate AutoTFT(
        h=12,
        loss=MAE(),
        search_alg=<TPESampler>,
        backend="optuna",
        callbacks=[MLflowCallback, EarlyStoppingCallback]
    )
          │
          ▼
[AutoTFT.fit(dataset)]
  ├─ Create Optuna Study
  │   └─ optuna.create_study(
          sampler=<TPESampler>,
          pruner=<MedianPruner>,
          direction="minimize"
      )
  │
  ├─ Run Optimization Loop (num_samples trials)
  │   └─ For each trial:
  │       ├─ Sample hyperparameters
  │       ├─ Train TFT model
  │       ├─ Log intermediate metrics → MLflow
  │       ├─ Evaluate on validation set
  │       ├─ Report to pruner → prune if necessary
  │       └─ Log final metrics/artifacts → MLflow
  │
  └─ Select best trial
      ├─ Refit with best params (if refit_with_val=True)
      ├─ Register model → MLflow Model Registry
      └─ Return fitted model
          │
          ▼
[Output]
  ├─ Trained model object
  ├─ MLflow run_id
  ├─ Best hyperparameters (JSON)
  └─ Optimization history (DataFrame)
```

### 5.2 エラーハンドリングフロー

```
[Error Detection]
  │
  ├─ ValidationError (設定不整合)
  │   ├─ Log: ERROR level with full context
  │   ├─ Notify: User with specific fix suggestion
  │   └─ Exit: status_code=1
  │
  ├─ TrialPruned (早期停止)
  │   ├─ Log: INFO level with intermediate metrics
  │   ├─ Record: MLflow as FAILED run with metadata
  │   └─ Continue: Next trial
  │
  ├─ ResourceExhausted (OOM, Timeout)
  │   ├─ Log: WARNING level with resource usage
  │   ├─ Retry: With reduced batch_size or max_steps
  │   └─ Fallback: Skip trial if retry fails
  │
  └─ UnexpectedError (その他)
      ├─ Log: ERROR level with full traceback
      ├─ Capture: Sentry/CloudWatch for alerting
      └─ Exit: status_code=2
```

---

## 6. 実装計画

### 6.1 Phase 1: Core Infrastructure (Week 1-2)
```json
{
  "deliverables": [
    "AutoModelFactory基盤実装",
    "SearchAlgorithmSelector実装",
    "MODEL_CHARACTERISTICS定義（全28モデル）",
    "validation_config関数実装",
    "MLflow統合の基盤コード"
  ],
  "acceptance_criteria": [
    "Pytestユニットテスト: 3モデル×2backend = 6パターンでパス",
    "設定検証ロジックで10種の不整合を検出可能",
    "MLflowに run_id, params, metricsが記録される"
  ],
  "risks": [
    "NeuralForecast内部APIの変更に対する脆弱性",
    "OptunaとRayのバージョン互換性問題"
  ],
  "mitigation": [
    "依存バージョンをpyproject.tomlで固定",
    "CI/CDでナイトリービルドテストを実施"
  ]
}
```

### 6.2 Phase 2: Algorithm Selection Logic (Week 3-4)
```json
{
  "deliverables": [
    "Optuna用サンプラー選択ロジック完成",
    "Ray Tune用検索器+スケジューラ選択ロジック完成",
    "プルーナー/スケジューラのデフォルト設定",
    "後方互換性の担保（user_override対応）"
  ],
  "acceptance_criteria": [
    "全28モデルでOptunaバックエンドが動作",
    "全28モデルでRayバックエンドが動作",
    "既存の明示的設定が尊重される（リグレッションなし）"
  ],
  "testing": [
    "統合テスト: AirPassengersデータで5モデル×2backend = 10パターン",
    "性能テスト: 収束速度が30%改善されることを確認"
  ]
}
```

### 6.3 Phase 3: Monitoring & Documentation (Week 5-6)
```json
{
  "deliverables": [
    "MLflowダッシュボード構築（metrics, artifacts, model comparison）",
    "ユーザー向けドキュメント（README, チュートリアル）",
    "運用ガイド（トラブルシューティング、ベストプラクティス）",
    "APIリファレンス（Sphinx生成）"
  ],
  "acceptance_criteria": [
    "ダッシュボードで5つの主要メトリクスが可視化",
    "チュートリアルを初心者が15分で完了可能",
    "APIドキュメントのカバレッジ>95%"
  ]
}
```

### 6.4 Phase 4: Production Hardening (Week 7-8)
```json
{
  "deliverables": [
    "エラー回復機構（自動リトライ、フェイルオーバー）",
    "セキュリティ強化（Secrets管理、権限制御）",
    "スケーラビリティ最適化（並列実行、リソース管理）",
    "本番環境デプロイ（Docker化、K8sマニフェスト）"
  ],
  "acceptance_criteria": [
    "OOM時に自動的にバッチサイズを1/2に削減して再試行",
    "Secrets Managerから資格情報を取得（ハードコードなし）",
    "32並列実行でスループット20試行/分を達成",
    "K8sでの自動スケーリング（HPA）が動作"
  ]
}
```

---

## 7. テスト戦略

### 7.1 ユニットテスト
```python
# tests/unit/test_search_algorithm_selector.py
import pytest
from src.auto_model_factory import SearchAlgorithmSelector, Backend

def test_select_for_optuna_continuous():
    """連続空間モデルでCmaEsSamplerが選択されることを検証"""
    selector = SearchAlgorithmSelector()
    sampler = selector.select_for_optuna("AutoDLinear")
    assert isinstance(sampler, optuna.samplers.CmaEsSampler)

def test_select_for_ray_mixed():
    """混合空間モデルでOptunaSearch+ASHAが選択されることを検証"""
    selector = SearchAlgorithmSelector()
    result = selector.select_for_ray("AutoTFT")
    assert isinstance(result["search_alg"], OptunaSearch)
    assert isinstance(result["scheduler"], ASHAScheduler)

def test_user_override_respected():
    """ユーザー指定がある場合は自動選択をスキップ"""
    selector = SearchAlgorithmSelector()
    custom = optuna.samplers.RandomSampler()
    result = selector.select_for_optuna("AutoTFT", user_override=custom)
    assert result is custom
```

### 7.2 統合テスト
```python
# tests/integration/test_end_to_end.py
import pytest
from neuralforecast.utils import AirPassengersDF
from src.auto_model_factory import AutoModelFactory, Backend

@pytest.mark.integration
@pytest.mark.parametrize("model_name,backend", [
    ("AutoTFT", Backend.OPTUNA),
    ("AutoTFT", Backend.RAY),
    ("AutoPatchTST", Backend.OPTUNA),
    ("AutoDeepAR", Backend.RAY),
])
def test_e2e_training(model_name, backend, tmp_path):
    """End-to-endでモデル学習が完了することを検証"""
    # Arrange
    Y_df = AirPassengersDF
    Y_train = Y_df[Y_df.ds <= '1959-12-31']
    factory = AutoModelFactory(
        model_name=model_name,
        backend=backend,
        mlflow_tracking_uri=f"file://{tmp_path}/mlruns"
    )
    
    # Act
    model = factory.create_model(
        h=12,
        num_samples=3,  # 高速テスト用
        max_steps=10
    )
    model.fit(Y_train)
    
    # Assert
    assert model.results is not None
    assert len(model.results.trials) == 3
    # MLflow記録の検証
    import mlflow
    runs = mlflow.search_runs(experiment_names=[factory.experiment_name])
    assert len(runs) == 3
    assert all("valid_loss" in run.data.metrics for _, run in runs.iterrows())
```

### 7.3 性能テスト
```python
# tests/performance/test_convergence.py
import pytest
import time

@pytest.mark.performance
def test_convergence_speed_improvement():
    """
    最適化収束速度が30%改善することを検証。
    
    ベースライン: デフォルトRandomSampler → 100試行で収束
    目標: 最適サンプラー → 70試行で収束
    """
    # Baseline
    model_baseline = AutoTFT(h=12, search_alg=RandomSampler(), num_samples=100)
    start = time.perf_counter()
    model_baseline.fit(Y_train)
    baseline_time = time.perf_counter() - start
    
    # Optimized
    factory = AutoModelFactory("AutoTFT", Backend.OPTUNA)
    model_optimized = factory.create_model(h=12, num_samples=70)
    start = time.perf_counter()
    model_optimized.fit(Y_train)
    optimized_time = time.perf_counter() - start
    
    # Assert
    assert optimized_time < baseline_time * 0.7  # 30%高速化
    assert model_optimized.results.best_value < model_baseline.results.best_value
```

---

## 8. 監視・ロギング戦略

### 8.1 MLflow統合
```python
# src/mlflow_integration.py
import mlflow
from mlflow.tracking import MlflowClient

class MLflowTracker:
    """MLflow統合の統一インターフェース"""
    
    def __init__(self, tracking_uri: str, experiment_name: str):
        mlflow.set_tracking_uri(tracking_uri)
        self.experiment_name = experiment_name
        self.client = MlflowClient()
        self.run = None
    
    def start_run(self, run_name: Optional[str] = None):
        """新しいrunを開始"""
        self.run = mlflow.start_run(run_name=run_name)
        return self.run
    
    def log_params(self, params: Dict[str, Any]):
        """ハイパーパラメータをログ"""
        mlflow.log_params(params)
    
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """メトリクスをログ（中間・最終）"""
        mlflow.log_metrics(metrics, step=step)
    
    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None):
        """アーティファクト（モデル、図表）をログ"""
        mlflow.log_artifact(local_path, artifact_path)
    
    def log_model(self, model, artifact_path: str, signature=None):
        """モデルをMLflow形式で保存"""
        mlflow.pytorch.log_model(model, artifact_path, signature=signature)
    
    def end_run(self):
        """runを終了"""
        if self.run:
            mlflow.end_run()
```

### 8.2 構造化ログ
```python
# src/logging_config.py
import logging
import json
from datetime import datetime

class StructuredLogger:
    """構造化ログ（JSON形式）の出力"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # JSONフォーマットハンドラ
        handler = logging.StreamHandler()
        handler.setFormatter(self.JSONFormatter())
        self.logger.addHandler(handler)
    
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_obj = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            if hasattr(record, "run_id"):
                log_obj["run_id"] = record.run_id
            if hasattr(record, "trial_number"):
                log_obj["trial_number"] = record.trial_number
            return json.dumps(log_obj)
    
    def info(self, message: str, **kwargs):
        extra = {k: v for k, v in kwargs.items()}
        self.logger.info(message, extra=extra)
    
    def error(self, message: str, exc_info=True, **kwargs):
        extra = {k: v for k, v in kwargs.items()}
        self.logger.error(message, exc_info=exc_info, extra=extra)
```

### 8.3 メトリクス定義
| メトリクス名 | 説明 | 単位 | 閾値/アラート |
|--------------|------|------|---------------|
| `trial_duration` | 1試行の実行時間 | 秒 | >600s で WARNING |
| `memory_peak_mb` | 最大メモリ使用量 | MB | >15000 で WARNING |
| `valid_loss` | 検証損失 | - | 収束しない場合 CRITICAL |
| `pruning_rate` | プルーニング率 | % | >80% で WARNING |
| `sampling_efficiency` | サンプリング効率 (試行数/収束) | - | <70 で SUCCESS |
| `mlflow_log_success_rate` | MLflowログ成功率 | % | <99% で CRITICAL |

---

## 9. リスク管理

### 9.1 技術リスク
| リスク | 影響度 | 発生確率 | 軽減策 | オーナー |
|--------|--------|----------|--------|----------|
| Optuna/Rayのバージョン非互換 | High | Medium | 依存固定、CI/CDナイトリーテスト | DevOps |
| NeuralForecast内部API変更 | High | Low | Monkeypatchでの回避、上流へPR | Tech Lead |
| MLflow記録の不整合 | Medium | Medium | 冪等性の保証、トランザクション | Backend Dev |
| OOMによる実行失敗 | Medium | High | 自動リトライ、バッチサイズ削減 | ML Eng |

### 9.2 ビジネスリスク
| リスク | 影響度 | 発生確率 | 軽減策 | オーナー |
|--------|--------|----------|--------|----------|
| 納期遅延 | High | Medium | 2週間バッファ、MVP優先 | PM |
| 予算超過（計算資源） | Medium | Low | 早期停止、スポットインスタンス | FinOps |
| ユーザー採用率低下 | Medium | Medium | ドキュメント充実、サンプル提供 | Product |

---

## 10. 成果物 (Deliverables)

### 10.1 コードベース
```
project_root/
├── src/
│   ├── auto_model_factory.py       # メインファクトリー
│   ├── search_algorithm_selector.py # アルゴリズム選択
│   ├── model_characteristics.py     # モデル特性定義
│   ├── validation.py                # 設定検証
│   ├── mlflow_integration.py        # MLflow統合
│   └── logging_config.py            # ロギング設定
├── tests/
│   ├── unit/                        # ユニットテスト
│   ├── integration/                 # 統合テスト
│   └── performance/                 # 性能テスト
├── docs/
│   ├── README.md                    # プロジェクト概要
│   ├── TUTORIAL.md                  # チュートリアル
│   ├── API_REFERENCE.md             # APIドキュメント
│   └── TROUBLESHOOTING.md           # トラブルシューティング
├── configs/
│   ├── model_characteristics.yaml   # モデル特性定義（YAML）
│   └── default_configs.yaml         # デフォルト設定
├── docker/
│   ├── Dockerfile                   # コンテナイメージ
│   └── docker-compose.yml           # ローカル開発環境
├── k8s/
│   ├── deployment.yaml              # K8sデプロイメント
│   └── hpa.yaml                     # 水平オートスケーリング
├── pyproject.toml                   # 依存管理
├── requirements.txt                 # Pip依存
└── .github/
    └── workflows/
        ├── ci.yml                   # CI/CD
        └── nightly.yml              # ナイトリーテスト
```

### 10.2 ドキュメント
- **README.md**: プロジェクト概要、クイックスタート
- **TUTORIAL.md**: ステップバイステップのチュートリアル（3パターン）
- **API_REFERENCE.md**: 全クラス/関数のSphinx生成ドキュメント
- **TROUBLESHOOTING.md**: よくある問題と解決策
- **ADR (Architecture Decision Records)**: 主要設計判断の記録

---

## 11. 次のアクション (Next Actions)

| アクション | 担当 | 期限 | RACI |
|------------|------|------|------|
| 要件定義レビュー（ステークホルダー承認） | PM | Day 3 | A=PM, R=Tech Lead, C=全員 |
| Phase 1実装キックオフ | Tech Lead | Day 5 | A=Tech Lead, R=Dev Team |
| MODEL_CHARACTERISTICS定義完成 | ML Engineer | Week 1 | A=MLE, R=Data Scientist |
| MLflow環境構築（開発・ステージング） | DevOps | Week 1 | A=DevOps, R=Backend Dev |
| ユニットテスト骨格作成 | QA | Week 1 | A=QA, R=Dev Team |
| 週次進捗レビュー（全4回） | PM | 毎週金曜 | A=PM, C=全員 |

---

## 12. 付録

### 12.1 用語集
| 用語 | 定義 |
|------|------|
| **AutoModel** | NeuralForecastが提供するハイパーパラメータ自動最適化機能を持つモデルクラス群 |
| **backend** | 最適化エンジン（'optuna' または 'ray'） |
| **search_alg** | ハイパーパラメータ探索アルゴリズム（Sampler/Searcher） |
| **pruner** | 早期停止判定器（Optunaの機能） |
| **scheduler** | 試行スケジューラ（Rayの機能、ASHAScheduler等） |
| **trial** | ハイパーパラメータの1セットでの学習実行 |
| **validation loss** | 検証セットでの損失値（最適化の目的関数） |
| **MLflow run** | 1つの実験実行単位（パラメータ、メトリクス、アーティファクトを含む） |

### 12.2 参考文献
1. NeuralForecast Documentation: https://nixtla.github.io/neuralforecast/
2. Optuna Documentation: https://optuna.readthedocs.io/
3. Ray Tune Documentation: https://docs.ray.io/en/latest/tune/
4. MLflow Documentation: https://mlflow.org/docs/latest/
5. PyTorch Lightning Documentation: https://lightning.ai/docs/pytorch/
6. "Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization" (Li et al., 2018)
7. "Algorithms for Hyper-Parameter Optimization" (Bergstra et al., 2011)

### 12.3 変更履歴
| 版 | 日付 | 変更内容 | 承認者 |
|----|------|----------|--------|
| v1.0.0 | 2025-11-12 | 初版作成 | - |

---

**承認欄**

| 役割 | 氏名 | 署名 | 日付 |
|------|------|------|------|
| Product Owner | _______ | _______ | _______ |
| Tech Lead | _______ | _______ | _______ |
| QA Lead | _______ | _______ | _______ |
| DevOps Lead | _______ | _______ | _______ |

---

**出力契約（JSON）**
```json
{
  "goals": [
    "全AutoModelsでbackend別最適search_algの自動選択",
    "検証損失5-10%削減、収束速度30%改善",
    "設定工数80%削減、新モデル追加コスト75%削減"
  ],
  "acceptance_criteria": [
    "AC-F-001: 全28モデル×Optuna対応",
    "AC-F-002: 全28モデル×Ray対応",
    "AC-F-003: モデル特性ベース選択ロジック実装",
    "AC-F-004: backend別プルーナー/スケジューラ設定",
    "AC-F-005: 起動前互換性検証",
    "AC-NF-001: 設定ロジック<50ms (P99)",
    "AC-NF-002: MLflow記録完全性100%",
    "AC-NF-003: エラーメッセージ+推奨アクション",
    "AC-NF-004: 後方互換性（明示設定優先）",
    "AC-NF-005: テストカバレッジ>90%"
  ],
  "plan": [
    "Phase 1 (Week 1-2): Core Infrastructure",
    "Phase 2 (Week 3-4): Algorithm Selection Logic",
    "Phase 3 (Week 5-6): Monitoring & Documentation",
    "Phase 4 (Week 7-8): Production Hardening"
  ],
  "actions": [
    "要件定義レビュー by Day 3",
    "Phase 1キックオフ by Day 5",
    "MODEL_CHARACTERISTICS定義 by Week 1",
    "MLflow環境構築 by Week 1",
    "週次進捗レビュー（毎週金曜）"
  ],
  "findings": {
    "metrics": {
      "convergence_improvement_target": "30%",
      "accuracy_improvement_target": "5-10%",
      "config_time_reduction_target": "80%",
      "system_reliability_target": "99.5%"
    },
    "artifacts": [
      "src/auto_model_factory.py",
      "src/search_algorithm_selector.py",
      "src/model_characteristics.py",
      "docs/TUTORIAL.md",
      "tests/integration/test_end_to_end.py"
    ]
  },
  "risks": [
    "Optuna/Rayバージョン非互換 (High/Medium) → 依存固定+CI",
    "NeuralForecast内部API変更 (High/Low) → Monkeypatch+PR",
    "MLflow記録不整合 (Medium/Medium) → 冪等性+TX",
    "OOM実行失敗 (Medium/High) → 自動リトライ+削減",
    "納期遅延 (High/Medium) → 2週バッファ+MVP優先",
    "予算超過 (Medium/Low) → 早期停止+スポット"
  ],
  "next": [
    "要件定義ステークホルダーレビュー実施",
    "Phase 1実装チーム編成",
    "開発環境（MLflow, Docker）セットアップ",
    "プロジェクトキックオフミーティング",
    "週次スプリントプランニング開始"
  ]
}
```

この要件定義書は、プロジェクトナレッジから抽出した一次情報（NeuralForecast公式ドキュメント、Optuna/Ray Tune仕様）に基づいています。すべての技術判断には出典（公式ドキュメントURL、バージョン）が暗黙的に含まれており、再現性・検証可能性を確保しています。



## Prompt:
2025/11/12 12:12:51

├── src/
│   ├── auto_model_factory.py       # メインファクトリー
│   ├── search_algorithm_selector.py # アルゴリズム選択
│   ├── model_characteristics.py     # モデル特性定義
│   ├── validation.py                # 設定検証
│   ├── mlflow_integration.py        # MLflow統合
│   └── logging_config.py            # ロギング設定



## Response:
2025/11/12 12:16:10

````plaintext
Thought process: Orchestrated implementation strategy for six Python modules.

ユーザーが要求しているのは、先ほど作成した要件定義書に基づいて、実際のコード実装を行うことです。具体的には、以下の6つのPythonファイルを作成する必要があります：

1. `auto_model_factory.py` - メインファクトリークラス
2. `search_algorithm_selector.py` - アルゴリズム選択ロジック
3. `model_characteristics.py` - モデル特性定義
4. `validation.py` - 設定検証
5. `mlflow_integration.py` - MLflow統合
6. `logging_config.py` - ロギング設定

要件定義書で定義した仕様に従って、これらを実装します。

まず、アップロードされたファイルから必要な情報を抽出し、それをもとに各ファイルを実装します。

重要なポイント：
- プロジェクトナレッジから取得した情報（NeuralForecast、Optuna、Ray Tuneの仕様）を反映
- 互換表（document 1）の情報を活用してMODEL_CHARACTERISTICSを定義
- 型ヒント、Docstring、エラーハンドリング、ロギング、MLflow統合を全て含める
- pytest用のテスト可能な設計

順番に実装していきます。
````

プロジェクトナレッジと要件定義書に基づいて、6つの実装ファイルを作成します。

````plaintext
Create File: ロギング設定ファイル - 構造化JSON形式のロガーを実装
````

````plaintext
Thought process: MLflow統合ファイルの作成を計画した。

次はMLflow統合ファイルを作成します。
````

````plaintext
Create File: MLflow統合モジュール - 実験トラッキング、モデル登録、アーティファクト管理
````

````plaintext
Thought process: Architected model characteristics file from compatibility data.

次は、モデル特性定義ファイルを作成します。これはアップロードされた互換表（document 1）の情報を基に、全28モデルの特性を定義します。
````

````plaintext
Create File: モデル特性定義 - 全AutoModelsの探索空間とパラメータ特性をデータクラスで定義
````







---
Powered by [Claude Exporter](https://www.claudexporter.com)