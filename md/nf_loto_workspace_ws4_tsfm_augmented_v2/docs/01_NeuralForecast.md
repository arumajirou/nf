# NeuralForecast

- 抽出日時: 2025-11-12 11:14
- 件数: 25

## 目次
1. [AutoModels - Nixtla](#AutoModels-Nixtla)
2. [PyTorch Losses - Nixtla](#PyTorch-Losses-Nixtla)
3. [Core - Nixtla](#Core-Nixtla)
4. [Reversible Mixture of KAN - RMoK - Nixtla](#Reversible-Mixture-of-KAN-RMoK-Nixtla)
5. [RNN - Nixtla](#RNN-Nixtla)
6. [SOFTS - Nixtla](#SOFTS-Nixtla)
7. [StemGNN - Nixtla](#StemGNN-Nixtla)
8. [TCN - Nixtla](#TCN-Nixtla)
9. [TFT - Nixtla](#TFT-Nixtla)
10. [TiDE - Nixtla](#TiDE-Nixtla)
11. [Time-LLM - Nixtla](#Time-LLM-Nixtla)
12. [TimeMixer - Nixtla](#TimeMixer-Nixtla)
13. [TimesNet - Nixtla](#TimesNet-Nixtla)
14. [TimeXer - Nixtla](#TimeXer-Nixtla)
15. [TSMixer - Nixtla](#TSMixer-Nixtla)
16. [TSMixerx - Nixtla](#TSMixerx-Nixtla)
17. [Vanilla Transformer - Nixtla](#Vanilla-Transformer-Nixtla)
18. [xLSTM - Nixtla](#xLSTM-Nixtla)
19. [PyTorch Losses - Nixtla](#PyTorch-Losses-Nixtla)
20. [NumPy Evaluation - Nixtla](#NumPy-Evaluation-Nixtla)
21. [Hyperparameter Optimization - Nixtla](#Hyperparameter-Optimization-Nixtla)
22. [TemporalNorm - Nixtla](#TemporalNorm-Nixtla)
23. [NN Modules - Nixtla](#NN-Modules-Nixtla)
24. [PyTorch Dataset/Loader - Nixtla](#PyTorch-DatasetLoader-Nixtla)
25. [Example Data - Nixtla](#Example-Data-Nixtla)


---

## AutoModels - Nixtla
<a id="AutoModels-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.html

NeuralForecast contains user-friendly implementations of neural forecasting models that allow for easy transition of computing capabilities (GPU/CPU), computation parallelization, and hyperparameter tuning.

All the NeuralForecast models are “global” because we train them with
all the series from the input pd.DataFrame data `Y_df`, yet the
optimization objective is, momentarily, “univariate” as it does not
consider the interaction between the output predictions across time
series. Like the StatsForecast library, `core.NeuralForecast` allows you
to explore collections of models efficiently and contains functions for
convenient wrangling of input and output pd.DataFrames predictions.
First we load the AirPassengers dataset such that you can run all the
examples.
CopyAsk AI```
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast.tsdataset import TimeSeriesDataset
from neuralforecast.utils import AirPassengersDF as Y_df
```


CopyAsk AI```
# Split train/test and declare time series dataset
Y_train_df = Y_df[Y_df.ds<='1959-12-31'] # 132 train
Y_test_df = Y_df[Y_df.ds>'1959-12-31']   # 12 test
dataset, *_ = TimeSeriesDataset.from_df(Y_train_df)
```


# [​](#1-automatic-forecasting)1. Automatic Forecasting


## [​](#a-rnn-based)A. RNN-Based



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L61)
### [​](#autornn)AutoRNN


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
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoRNN.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=-1, encoder_hidden_size=8)
model = AutoRNN(h=12, config=config, num_samples=1, cpus=1)

model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoRNN(h=12, config=None, num_samples=1, cpus=1, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L136)
### [​](#autolstm)AutoLSTM


> CopyAsk AI AutoLSTM (h, loss=MAE(), valid_loss=None, config=None,
>            search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>            object at 0x7f1320937310>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320937310>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoLSTM.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=-1, encoder_hidden_size=8)
model = AutoLSTM(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoLSTM(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L207)
### [​](#autogru)AutoGRU


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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320e7c2b0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoGRU.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=-1, encoder_hidden_size=8)
model = AutoGRU(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoGRU(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L278)
### [​](#autotcn)AutoTCN


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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f13208f1ae0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTCN.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=-1, encoder_hidden_size=8)
model = AutoTCN(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTCN(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L348)
### [​](#autodeepar)AutoDeepAR


> CopyAsk AI AutoDeepAR (h, loss=DistributionLoss(), valid_loss=MQLoss(), config=None,
>              search_alg=<ray.tune.search.basic_variant.BasicVariantGenerat
>              or object at 0x7f1320ecec80>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossDistributionLossDistributionLoss()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossMQLossMQLoss()Instantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ecec80>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoDeepAR.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, lstm_hidden_size=8)
model = AutoDeepAR(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoDeepAR(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L419)
### [​](#autodilatedrnn)AutoDilatedRNN


> CopyAsk AI AutoDilatedRNN (h, loss=MAE(), valid_loss=None, config=None,
>                  search_alg=<ray.tune.search.basic_variant.BasicVariantGen
>                  erator object at 0x7f132090feb0>, num_samples=10,
>                  refit_with_val=False, cpus=4, gpus=0, verbose=False,
>                  alias=None, backend='ray', callbacks=None)


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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f132090feb0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoDilatedRNN.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=-1, encoder_hidden_size=8)
model = AutoDilatedRNN(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoDilatedRNN(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L491)
### [​](#autobitcn)AutoBiTCN


> CopyAsk AI AutoBiTCN (h, loss=MAE(), valid_loss=None, config=None,
>             search_alg=<ray.tune.search.basic_variant.BasicVariantGenerato
>             r object at 0x7f1320a9c9d0>, num_samples=10,
>             refit_with_val=False, cpus=4, gpus=0, verbose=False,
>             alias=None, backend='ray', callbacks=None)


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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a9c9d0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoBiTCN.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
model = AutoBiTCN(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoBiTCN(h=12, config=None, backend='optuna')
```


## [​](#b-mlp-based)B. MLP-Based



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L559)
### [​](#automlp)AutoMLP


> CopyAsk AI AutoMLP (h, loss=MAE(), valid_loss=None, config=None,
>           search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>           object at 0x7f1320ad7a60>, num_samples=10, refit_with_val=False,
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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ad7a60>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoMLP.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
model = AutoMLP(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoMLP(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L627)
### [​](#autonbeats)AutoNBEATS


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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ad5390>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoNBEATS.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12,
              mlp_units=3*[[8, 8]])
model = AutoNBEATS(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoNBEATS(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L693)
### [​](#autonbeatsx)AutoNBEATSx


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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ac6cb0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoNBEATSx.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12,
              mlp_units=3*[[8, 8]])
model = AutoNBEATSx(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoNBEATSx(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L759)
### [​](#autonhits)AutoNHITS


> CopyAsk AI AutoNHITS (h, loss=MAE(), valid_loss=None, config=None,
>             search_alg=<ray.tune.search.basic_variant.BasicVariantGenerato
>             r object at 0x7f1320ab4100>, num_samples=10,
>             refit_with_val=False, cpus=4, gpus=0, verbose=False,
>             alias=None, backend='ray', callbacks=None)


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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ab4100>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoNHITS.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, 
              mlp_units=3 * [[8, 8]])
model = AutoNHITS(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoNHITS(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L838)
### [​](#autodlinear)AutoDLinear


> CopyAsk AI AutoDLinear (h, loss=MAE(), valid_loss=None, config=None,
>               search_alg=<ray.tune.search.basic_variant.BasicVariantGenera
>               tor object at 0x7f1320a9cd90>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a9cd90>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoDLinear.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoDLinear(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoDLinear(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L905)
### [​](#autonlinear)AutoNLinear


> CopyAsk AI AutoNLinear (h, loss=MAE(), valid_loss=None, config=None,
>               search_alg=<ray.tune.search.basic_variant.BasicVariantGenera
>               tor object at 0x7f1320ab6b00>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ab6b00>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoNLinear.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoNLinear(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoNLinear(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L971)
### [​](#autotide)AutoTiDE


> CopyAsk AI AutoTiDE (h, loss=MAE(), valid_loss=None, config=None,
>            search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>            object at 0x7f1320ad4a60>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ad4a60>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTiDE.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoTiDE(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTiDE(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1045)
### [​](#autodeepnpts)AutoDeepNPTS


> CopyAsk AI AutoDeepNPTS (h, loss=MAE(), valid_loss=None, config=None,
>                search_alg=<ray.tune.search.basic_variant.BasicVariantGener
>                ator object at 0x7f1320dd1000>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320dd1000>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoDeepNPTS.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoDeepNPTS(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoDeepNPTS(h=12, config=None, backend='optuna')
```


## [​](#c-kan-based)C. KAN-Based



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1114)
### [​](#autokan)AutoKAN


> CopyAsk AI AutoKAN (h, loss=MAE(), valid_loss=None, config=None,
>           search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>           object at 0x7f1320a491e0>, num_samples=10, refit_with_val=False,
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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a491e0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoKAN.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoKAN(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoKAN(h=12, config=None, backend='optuna')
```


## [​](#d-transformer-based)D. Transformer-Based



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1183)
### [​](#autotft)AutoTFT


> CopyAsk AI AutoTFT (h, loss=MAE(), valid_loss=None, config=None,
>           search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>           object at 0x7f1320de5780>, num_samples=10, refit_with_val=False,
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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320de5780>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTFT.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
model = AutoTFT(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTFT(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1251)
### [​](#autovanillatransformer)AutoVanillaTransformer


> CopyAsk AI AutoVanillaTransformer (h, loss=MAE(), valid_loss=None, config=None,
>                          search_alg=<ray.tune.search.basic_variant.BasicVa
>                          riantGenerator object at 0x7f1320a54a90>,
>                          num_samples=10, refit_with_val=False, cpus=4,
>                          gpus=0, verbose=False, alias=None, backend='ray',
>                          callbacks=None)


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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a54a90>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoVanillaTransformer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
model = AutoVanillaTransformer(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoVanillaTransformer(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1319)
### [​](#autoinformer)AutoInformer


> CopyAsk AI AutoInformer (h, loss=MAE(), valid_loss=None, config=None,
>                search_alg=<ray.tune.search.basic_variant.BasicVariantGener
>                ator object at 0x7f1320a31660>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a31660>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoInformer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
model = AutoInformer(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoInformer(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1387)
### [​](#autoautoformer)AutoAutoformer


> CopyAsk AI AutoAutoformer (h, loss=MAE(), valid_loss=None, config=None,
>                  search_alg=<ray.tune.search.basic_variant.BasicVariantGen
>                  erator object at 0x7f1320a489d0>, num_samples=10,
>                  refit_with_val=False, cpus=4, gpus=0, verbose=False,
>                  alias=None, backend='ray', callbacks=None)


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
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a489d0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoAutoformer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=8)
model = AutoAutoformer(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoAutoformer(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1455)
### [​](#autofedformer)AutoFEDformer


> CopyAsk AI AutoFEDformer (h, loss=MAE(), valid_loss=None, config=None,
>                 search_alg=<ray.tune.search.basic_variant.BasicVariantGene
>                 rator object at 0x7f1320c40220>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320c40220>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoFEDFormer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=64)
model = AutoFEDformer(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoFEDformer(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1522)
### [​](#autopatchtst)AutoPatchTST


> CopyAsk AI AutoPatchTST (h, loss=MAE(), valid_loss=None, config=None,
>                search_alg=<ray.tune.search.basic_variant.BasicVariantGener
>                ator object at 0x7f13209ed420>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f13209ed420>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoPatchTST.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=16)
model = AutoPatchTST(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoPatchTST(h=12, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1592)
### [​](#autoitransformer)AutoiTransformer


> CopyAsk AI AutoiTransformer (h, n_series, loss=MAE(), valid_loss=None, config=None,
>                    search_alg=<ray.tune.search.basic_variant.BasicVariantG
>                    enerator object at 0x7f1320da8490>, num_samples=10,
>                    refit_with_val=False, cpus=4, gpus=0, verbose=False,
>                    alias=None, backend='ray', callbacks=None)


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
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320da8490>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoiTransformer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=16)
model = AutoiTransformer(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoiTransformer(h=12, n_series=1, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1677)
### [​](#autotimexer)AutoTimeXer


> CopyAsk AI AutoTimeXer (h, n_series, loss=MAE(), valid_loss=None, config=None,
>               search_alg=<ray.tune.search.basic_variant.BasicVariantGenera
>               tor object at 0x7f13209ff2e0>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f13209ff2e0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTimeXer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, patch_len=12)
model = AutoTimeXer(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTimeXer(h=12, n_series=1, config=None, backend='optuna')
```


## [​](#e-cnn-based)E. CNN Based



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1762)
### [​](#autotimesnet)AutoTimesNet


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
validation and test periods.*
**Type****Default****Details**hintForecast horizonlossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a13760>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTimesNet.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=32)
model = AutoTimesNet(h=12, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTimesNet(h=12, config=None, backend='optuna')
```


## [​](#f-multivariate)F. Multivariate



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1830)
### [​](#autostemgnn)AutoStemGNN


> CopyAsk AI AutoStemGNN (h, n_series, loss=MAE(), valid_loss=None, config=None,
>               search_alg=<ray.tune.search.basic_variant.BasicVariantGenera
>               tor object at 0x7f1320bce500>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320bce500>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoStemGNN.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoStemGNN(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoStemGNN(h=12, n_series=1, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1915)
### [​](#autohint)AutoHINT


> CopyAsk AI AutoHINT (cls_model, h, loss, valid_loss, S, config,
>            search_alg=<ray.tune.search.basic_variant.BasicVariantGenerator
>            object at 0x7f13209ff790>, num_samples=10, cpus=4, gpus=0,
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
**Type****Default****Details**cls_modelPyTorch/PyTorchLightning modelSee `neuralforecast.models` [collection here](https://nixtla.github.io/neuralforecast/models.html).hintForecast horizonlossPyTorch moduleInstantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossPyTorch moduleInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).Sconfigdict or callableDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f13209ff790>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.refit_with_valboolFalseRefit of best model should preserve val_size.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Perform a simple hyperparameter optimization with 
# NHITS and then reconcile with HINT
from neuralforecast.losses.pytorch import GMM, sCRPS

base_config = dict(max_steps=1, val_check_steps=1, input_size=8)
base_model = AutoNHITS(h=4, loss=GMM(n_components=2, quantiles=quantiles), 
                       config=base_config, num_samples=1, cpus=1)
model = HINT(h=4, S=S_df.values,
             model=base_model,  reconciliation='MinTraceOLS')

model.fit(dataset=dataset)
y_hat = model.predict(dataset=hint_dataset)

# Perform a conjunct hyperparameter optimization with 
# NHITS + HINT reconciliation configurations
nhits_config = {
       "learning_rate": tune.choice([1e-3]),                                     # Initial Learning rate
       "max_steps": tune.choice([1]),                                            # Number of SGD steps
       "val_check_steps": tune.choice([1]),                                      # Number of steps between validation
       "input_size": tune.choice([5 * 12]),                                      # input_size = multiplier * horizon
       "batch_size": tune.choice([7]),                                           # Number of series in windows
       "windows_batch_size": tune.choice([256]),                                 # Number of windows in batch
       "n_pool_kernel_size": tune.choice([[2, 2, 2], [16, 8, 1]]),               # MaxPool's Kernelsize
       "n_freq_downsample": tune.choice([[168, 24, 1], [24, 12, 1], [1, 1, 1]]), # Interpolation expressivity ratios
       "activation": tune.choice(['ReLU']),                                      # Type of non-linear activation
       "n_blocks":  tune.choice([[1, 1, 1]]),                                    # Blocks per each 3 stacks
       "mlp_units":  tune.choice([[[512, 512], [512, 512], [512, 512]]]),        # 2 512-Layers per block for each stack
       "interpolation_mode": tune.choice(['linear']),                            # Type of multi-step interpolation
       "random_seed": tune.randint(1, 10),
       "reconciliation": tune.choice(['BottomUp', 'MinTraceOLS', 'MinTraceWLS'])
    }
model = AutoHINT(h=4, S=S_df.values,
                 cls_model=NHITS,
                 config=nhits_config,
                 loss=GMM(n_components=2, level=[80, 90]),
                 valid_loss=sCRPS(level=[80, 90]),
                 num_samples=1, cpus=1)
model.fit(dataset=dataset)
y_hat = model.predict(dataset=hint_dataset)
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L1987)
### [​](#autotsmixer)AutoTSMixer


> CopyAsk AI AutoTSMixer (h, n_series, loss=MAE(), valid_loss=None, config=None,
>               search_alg=<ray.tune.search.basic_variant.BasicVariantGenera
>               tor object at 0x7f1320a1f490>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320a1f490>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTSMixer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoTSMixer(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTSMixer(h=12, n_series=1, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L2073)
### [​](#autotsmixerx)AutoTSMixerx


> CopyAsk AI AutoTSMixerx (h, n_series, loss=MAE(), valid_loss=None, config=None,
>                search_alg=<ray.tune.search.basic_variant.BasicVariantGener
>                ator object at 0x7f1320bcdea0>, num_samples=10,
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
validation and test periods.*
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320bcdea0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTSMixerx.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoTSMixerx(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTSMixerx(h=12, n_series=1, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L2159)
### [​](#automlpmultivariate)AutoMLPMultivariate


> CopyAsk AI AutoMLPMultivariate (h, n_series, loss=MAE(), valid_loss=None,
>                       config=None, search_alg=<ray.tune.search.basic_varia
>                       nt.BasicVariantGenerator object at 0x7f1320bbbc70>,
>                       num_samples=10, refit_with_val=False, cpus=4,
>                       gpus=0, verbose=False, alias=None, backend='ray',
>                       callbacks=None)


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
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320bbbc70>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoMLPMultivariate.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12)
model = AutoMLPMultivariate(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoMLPMultivariate(h=12, n_series=1, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L2244)
### [​](#autosofts)AutoSOFTS


> CopyAsk AI AutoSOFTS (h, n_series, loss=MAE(), valid_loss=None, config=None,
>             search_alg=<ray.tune.search.basic_variant.BasicVariantGenerato
>             r object at 0x7f1320bae470>, num_samples=10,
>             refit_with_val=False, cpus=4, gpus=0, verbose=False,
>             alias=None, backend='ray', callbacks=None)


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
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320bae470>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoSOFTS.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, hidden_size=16)
model = AutoSOFTS(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoSOFTS(h=12, n_series=1, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L2329)
### [​](#autotimemixer)AutoTimeMixer


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
validation and test periods.*
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ba16c0>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoTimeMixer.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, d_model=16)
model = AutoTimeMixer(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoTimeMixer(h=12, n_series=1, config=None, backend='optuna')
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/auto.py#L2415)
### [​](#autormok)AutoRMoK


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
validation and test periods.*
**Type****Default****Details**hintForecast horizonn_serieslossMAEMAE()Instantiated train loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).valid_lossNoneTypeNoneInstantiated valid loss class from [losses collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).configNoneTypeNoneDictionary with ray.tune defined search space or function that takes an optuna trial and returns a configuration dict.search_algBasicVariantGenerator<ray.tune.search.basic_variant.BasicVariantGenerator object at 0x7f1320ba3340>For ray see [https://docs.ray.io/en/latest/tune/api_docs/suggestion.html](https://docs.ray.io/en/latest/tune/api_docs/suggestion.html)  
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.refit_with_valboolFalseRefit of best model should preserve val_size.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)
CopyAsk AI```
# Use your own config or AutoRMoK.default_config
config = dict(max_steps=1, val_check_steps=1, input_size=12, learning_rate=1e-2)
model = AutoRMoK(h=12, n_series=1, config=config, num_samples=1, cpus=1)

# Fit and predict
model.fit(dataset=dataset)
y_hat = model.predict(dataset=dataset)

# Optuna
model = AutoRMoK(h=12, n_series=1, config=None, backend='optuna')
```


# [​](#tests)TESTS

---

## PyTorch Losses - Nixtla
<a id="PyTorch-Losses-Nixtla"></a>

- 元URL: https://nixtla.github.io/neuralforecast/losses.pytorch.html

NeuralForecast contains a collection PyTorch Loss classes aimed to be used during the models' optimization.

The most important train signal is the forecast error, which is the
difference between the observed value yτy_{\tau}yτ​ and the prediction
y^τ\hat{y}_{\tau}y^​τ​, at time yτy_{\tau}yτ​:
eτ=yτ−y^ττ∈{t+1,…,t+H}e_{\tau} = y_{\tau}-\hat{y}_{\tau} \qquad \qquad \tau \in \{t+1,\dots,t+H \}eτ​=yτ​−y^​τ​τ∈{t+1,…,t+H}
The train loss summarizes the forecast errors in different train
optimization objectives.
All the losses are `torch.nn.modules` which helps to automatically moved
them across CPU/GPU/TPU devices with Pytorch Lightning.

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L50)
### [​](#basepointloss)BasePointLoss


> CopyAsk AI BasePointLoss (horizon_weight=None, outputsize_multiplier=None,
>                 output_names=None)


*Base class for point loss functions.
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
 `outputsize_multiplier`:
Multiplier for the output size.   
 `output_names`: Names of the
outputs.   
*
# [​](#1-scale-dependent-errors)1. Scale-dependent Errors


These metrics are on the same scale as the data.
## [​](#mean-absolute-error-mae)Mean Absolute Error (MAE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L103)
### [​](#mae-init)MAE.__init__


> CopyAsk AI MAE.__init__ (horizon_weight=None)


*Mean Absolute Error
Calculates Mean Absolute Error between `y` and `y_hat`. MAE measures the
relative prediction accuracy of a forecasting method by calculating the
deviation of the prediction and the true value at a given time and
averages these devations over the length of the series.
MAE(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣\mathrm{MAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} |y_{\tau} - \hat{y}_{\tau}|MAE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​−y^​τ​∣
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L124)
### [​](#mae-call)MAE.__call__


> CopyAsk AI MAE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                mask:Optional[torch.Tensor]=None,
>                y_insample:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`mae`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mae):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mae_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=155a03ab35bf439a5e84d13240ffd1e8)
## [​](#mean-squared-error-mse)Mean Squared Error (MSE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L145)
### [​](#mse-init)MSE.__init__


> CopyAsk AI MSE.__init__ (horizon_weight=None)


*Mean Squared Error
Calculates Mean Squared Error between `y` and `y_hat`. MSE measures the
relative prediction accuracy of a forecasting method by calculating the
squared deviation of the prediction and the true value at a given time,
and averages these devations over the length of the series.
MSE(yτ,y^τ)=1H∑τ=t+1t+H(yτ−y^τ)2\mathrm{MSE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} (y_{\tau} - \hat{y}_{\tau})^{2}MSE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​(yτ​−y^​τ​)2
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L166)
### [​](#mse-call)MSE.__call__


> CopyAsk AI MSE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                y_insample:torch.Tensor, mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`mse`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mse):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mse_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=938bc9e8bbbefece696fe397c823efd7)
## [​](#root-mean-squared-error-rmse)Root Mean Squared Error (RMSE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L187)
### [​](#rmse-init)RMSE.__init__


> CopyAsk AI RMSE.__init__ (horizon_weight=None)


*Root Mean Squared Error
Calculates Root Mean Squared Error between `y` and `y_hat`. RMSE
measures the relative prediction accuracy of a forecasting method by
calculating the squared deviation of the prediction and the observed
value at a given time and averages these devations over the length of
the series. Finally the RMSE will be in the same scale as the original
time series so its comparison with other series is possible only if they
share a common scale. RMSE has a direct connection to the L2 norm.
RMSE(yτ,y^τ)=1H∑τ=t+1t+H(yτ−y^τ)2\mathrm{RMSE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \sqrt{\frac{1}{H} \sum^{t+H}_{\tau=t+1} (y_{\tau} - \hat{y}_{\tau})^{2}}RMSE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​(yτ​−y^​τ​)2​
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L211)
### [​](#rmse-call)RMSE.__call__


> CopyAsk AI RMSE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                 mask:Optional[torch.Tensor]=None,
>                 y_insample:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`rmse`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#rmse):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/rmse_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=ce7c8abd1e08bdb3cd445d13db639aeb)
# [​](#2-percentage-errors)2. Percentage errors


These metrics are unit-free, suitable for comparisons across series.
## [​](#mean-absolute-percentage-error-mape)Mean Absolute Percentage Error (MAPE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L233)
### [​](#mape-init)MAPE.__init__


> CopyAsk AI MAPE.__init__ (horizon_weight=None)


*Mean Absolute Percentage Error
Calculates Mean Absolute Percentage Error between `y` and `y_hat`. MAPE
measures the relative prediction accuracy of a forecasting method by
calculating the percentual deviation of the prediction and the observed
value at a given time and averages these devations over the length of
the series. The closer to zero an observed value is, the higher penalty
MAPE loss assigns to the corresponding error.
MAPE(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣∣yτ∣\mathrm{MAPE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{|y_{\tau}|}MAPE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​∣∣yτ​−y^​τ​∣​
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   

**References:**  
 [Makridakis S., “Accuracy measures: theoretical and
practical
concerns”.](https://www.sciencedirect.com/science/article/pii/0169207093900793)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L258)
### [​](#mape-call)MAPE.__call__


> CopyAsk AI MAPE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                 y_insample:torch.Tensor, mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`mape`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mape):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mape_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=15de69fb4f6f1e7300d31cf4408ccf4f)
## [​](#symmetric-mape-smape)Symmetric MAPE (sMAPE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L281)
### [​](#smape-init)SMAPE.__init__


> CopyAsk AI SMAPE.__init__ (horizon_weight=None)


*Symmetric Mean Absolute Percentage Error
Calculates Symmetric Mean Absolute Percentage Error between `y` and
`y_hat`. SMAPE measures the relative prediction accuracy of a
forecasting method by calculating the relative deviation of the
prediction and the observed value scaled by the sum of the absolute
values for the prediction and observed value at a given time, then
averages these devations over the length of the series. This allows the
SMAPE to have bounds between 0% and 200% which is desireble compared to
normal MAPE that may be undetermined when the target is zero.
sMAPE2(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣∣yτ∣+∣y^τ∣\mathrm{sMAPE}_{2}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{|y_{\tau}|+|\hat{y}_{\tau}|}sMAPE2​(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​∣+∣y^​τ​∣∣yτ​−y^​τ​∣​
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   

**References:**  
 [Makridakis S., “Accuracy measures: theoretical and
practical
concerns”.](https://www.sciencedirect.com/science/article/pii/0169207093900793)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L308)
### [​](#smape-call)SMAPE.__call__


> CopyAsk AI SMAPE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                  mask:Optional[torch.Tensor]=None,
>                  y_insample:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`smape`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#smape):
tensor (single value).*
# [​](#3-scale-independent-errors)3. Scale-independent Errors


These metrics measure the relative improvements versus baselines.
## [​](#mean-absolute-scaled-error-mase)Mean Absolute Scaled Error (MASE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L331)
### [​](#mase-init)MASE.__init__


> CopyAsk AI MASE.__init__ (seasonality:int, horizon_weight=None)


*Mean Absolute Scaled Error Calculates the Mean Absolute Scaled Error
between `y` and `y_hat`. MASE measures the relative prediction accuracy
of a forecasting method by comparinng the mean absolute errors of the
prediction and the observed value against the mean absolute errors of
the seasonal naive model. The MASE partially composed the Overall
Weighted Average (OWA), used in the M4 Competition.
MASE(yτ,y^τ,y^τseason)=1H∑τ=t+1t+H∣yτ−y^τ∣MAE(yτ,y^τseason)\mathrm{MASE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}, \mathbf{\hat{y}}^{season}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{\mathrm{MAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{season}_{\tau})}MASE(yτ​,y^​τ​,y^​τseason​)=H1​∑τ=t+1t+H​MAE(yτ​,y^​τseason​)∣yτ​−y^​τ​∣​
**Parameters:**  
 `seasonality`: int. Main frequency of the time
series; Hourly 24, Daily 7, Weekly 52, Monthly 12, Quarterly 4,
Yearly 1. `horizon_weight`: Tensor of size h, weight for each timestamp
of the forecasting window.   

**References:**  
 [Rob J. Hyndman, & Koehler, A. B. “Another look at
measures of forecast
accuracy”.](https://www.sciencedirect.com/science/article/pii/S0169207006000239)  

[Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, “The
M4 Competition: 100,000 time series and 61 forecasting
methods”.](https://www.sciencedirect.com/science/article/pii/S0169207019301128)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L358)
### [​](#mase-call)MASE.__call__


> CopyAsk AI MASE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                 y_insample:torch.Tensor, mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor (batch_size, output_size), Actual
values.  
 `y_hat`: tensor (batch_size, output_size)), Predicted
values.  
 `y_insample`: tensor (batch_size, input_size), Actual
insample values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`mase`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mase):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mase_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=9cba699ceb4b7ff7b2b9c553207379b9)
## [​](#relative-mean-squared-error-relmse)Relative Mean Squared Error (relMSE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L387)
### [​](#relmse-init)relMSE.__init__


> CopyAsk AI relMSE.__init__ (y_train=None, horizon_weight=None)


*Relative Mean Squared Error Computes Relative Mean Squared Error
(relMSE), as proposed by Hyndman & Koehler (2006) as an alternative to
percentage errors, to avoid measure unstability.
relMSE(y,y^,y^benchmark)=MSE(y,y^)MSE(y,y^benchmark) \mathrm{relMSE}(\mathbf{y}, \mathbf{\hat{y}}, \mathbf{\hat{y}}^{benchmark}) =
\frac{\mathrm{MSE}(\mathbf{y}, \mathbf{\hat{y}})}{\mathrm{MSE}(\mathbf{y}, \mathbf{\hat{y}}^{benchmark})} relMSE(y,y^​,y^​benchmark)=MSE(y,y^​benchmark)MSE(y,y^​)​
**Parameters:**  
 `y_train`: numpy array, deprecated.  

`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 - [Hyndman, R. J and Koehler, A. B. (2006). “Another
look at measures of forecast accuracy”, International Journal of
Forecasting, Volume 22, Issue
4.](https://www.sciencedirect.com/science/article/pii/S0169207006000239)  
 -
[Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan Reddy, Mengfei Cao,
Lee Dicker. “Probabilistic Hierarchical Forecasting with Deep Poisson
Mixtures. Submitted to the International Journal Forecasting, Working
paper available at arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L415)
### [​](#relmse-call)relMSE.__call__


> CopyAsk AI relMSE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                   y_benchmark:torch.Tensor,
>                   mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor (batch_size, output_size), Actual
values.  
 `y_hat`: tensor (batch_size, output_size)), Predicted
values.  
 `y_benchmark`: tensor (batch_size, output_size), Benchmark
predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`relMSE`](https://nixtlaverse.nixtla.io/neuralforecast/losses.pytorch.html#relmse):
tensor (single value).*
# [​](#4-probabilistic-errors)4. Probabilistic Errors


These methods use statistical approaches for estimating unknown
probability distributions using observed data.
Maximum likelihood estimation involves finding the parameter values that
maximize the likelihood function, which measures the probability of
obtaining the observed data given the parameter values. MLE has good
theoretical properties and efficiency under certain satisfied
assumptions.
On the non-parametric approach, quantile regression measures
non-symmetrically deviation, producing under/over estimation.
## [​](#quantile-loss)Quantile Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L439)
### [​](#quantileloss-init)QuantileLoss.__init__


> CopyAsk AI QuantileLoss.__init__ (q, horizon_weight=None)


*Quantile Loss
Computes the quantile loss between `y` and `y_hat`. QL measures the
deviation of a quantile forecast. By weighting the absolute deviation in
a non symmetric way, the loss pays more attention to under or over
estimation. A common value for q is 0.5 for the deviation from the
median (Pinball loss).
QL(yτ,y^τ(q))=1H∑τ=t+1t+H((1−q) (y^τ(q)−yτ)++q (yτ−y^τ(q))+)\mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \Big( (1-q)\,( \hat{y}^{(q)}_{\tau} - y_{\tau} )_{+} + q\,( y_{\tau} - \hat{y}^{(q)}_{\tau} )_{+} \Big)QL(yτ​,y^​τ(q)​)=H1​∑τ=t+1t+H​((1−q)(y^​τ(q)​−yτ​)+​+q(yτ​−y^​τ(q)​)+​)
**Parameters:**  
 `q`: float, between 0 and 1. The slope of the
quantile loss, in the context of quantile regression, the q determines
the conditional quantile level.  
 `horizon_weight`: Tensor of size h,
weight for each timestamp of the forecasting window.   

**References:**  
 [Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L466)
### [​](#quantileloss-call)QuantileLoss.__call__


> CopyAsk AI QuantileLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                         y_insample:torch.Tensor,
>                         mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`quantile_loss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#quantile_loss):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/q_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=426c786498233e8b1f59f960b46b4391)
## [​](#multi-quantile-loss-mqloss)Multi Quantile Loss (MQLoss)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L516)
### [​](#mqloss-init)MQLoss.__init__


> CopyAsk AI MQLoss.__init__ (level=[80, 90], quantiles=None, horizon_weight=None)


*Multi-Quantile loss
Calculates the Multi-Quantile loss (MQL) between `y` and `y_hat`. MQL
calculates the average multi-quantile Loss for a given set of quantiles,
based on the absolute difference between predicted quantiles and
observed values.
MQL(yτ,[y^τ(q1),...,y^τ(qn)])=1n∑qiQL(yτ,y^τ(qi))\mathrm{MQL}(\mathbf{y}_{\tau},[\mathbf{\hat{y}}^{(q_{1})}_{\tau}, ... ,\hat{y}^{(q_{n})}_{\tau}]) = \frac{1}{n} \sum_{q_{i}} \mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q_{i})}_{\tau})MQL(yτ​,[y^​τ(q1​)​,...,y^​τ(qn​)​])=n1​∑qi​​QL(yτ​,y^​τ(qi​)​)
The limit behavior of MQL allows to measure the accuracy of a full
predictive distribution F^τ\mathbf{\hat{F}}_{\tau}F^τ​ with the continuous
ranked probability score (CRPS). This can be achieved through a
numerical integration technique, that discretizes the quantiles and
treats the CRPS integral with a left Riemann approximation, averaging
over uniformly distanced quantiles.
CRPS(yτ,F^τ)=∫01QL(yτ,y^τ(q))dq\mathrm{CRPS}(y_{\tau}, \mathbf{\hat{F}}_{\tau}) = \int^{1}_{0} \mathrm{QL}(y_{\tau}, \hat{y}^{(q)}_{\tau}) dqCRPS(yτ​,F^τ​)=∫01​QL(yτ​,y^​τ(q)​)dq
**Parameters:**  
 `level`: int list [0,100]. Probability levels for
prediction intervals (Defaults median). `quantiles`: float list [0.,
1.]. Alternative to level, quantiles to estimate from y distribution.
`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 [Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)  
 [James E.
Matheson and Robert L. Winkler, “Scoring Rules for Continuous
Probability Distributions”.](https://www.jstor.org/stable/2629907)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L599)
### [​](#mqloss-call)MQLoss.__call__


> CopyAsk AI MQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                   y_insample:torch.Tensor,
>                   mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`mqloss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mqloss):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mq_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=18abc02ceb1f6910df7ab34f03948914)
## [​](#implicit-quantile-loss-iqloss)Implicit Quantile Loss (IQLoss)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L637)
### [​](#quantilelayer)QuantileLayer


> CopyAsk AI QuantileLayer (num_output:int, cos_embedding_dim:int=128)


*Implicit Quantile Layer from the paper
`IQN for Distributional Reinforcement Learning`
([https://arxiv.org/abs/1806.06923](https://arxiv.org/abs/1806.06923)) by Dabney et al. 2018.
Code from GluonTS:
[https://github.com/awslabs/gluonts/blob/dev/src/gluonts/torch/distributions/implicit_quantile_network.py\](https://github.com/awslabs/gluonts/blob/dev/src/gluonts/torch/distributions/implicit_quantile_network.py%5C)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L663)
### [​](#iqloss-init)IQLoss.__init__


> CopyAsk AI IQLoss.__init__ (cos_embedding_dim=64, concentration0=1.0,
>                   concentration1=1.0, horizon_weight=None)


*Implicit Quantile Loss
Computes the quantile loss between `y` and `y_hat`, with the quantile
`q` provided as an input to the network. IQL measures the deviation of a
quantile forecast. By weighting the absolute deviation in a non
symmetric way, the loss pays more attention to under or over estimation.
QL(yτ,y^τ(q))=1H∑τ=t+1t+H((1−q) (y^τ(q)−yτ)++q (yτ−y^τ(q))+)\mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \Big( (1-q)\,( \hat{y}^{(q)}_{\tau} - y_{\tau} )_{+} + q\,( y_{\tau} - \hat{y}^{(q)}_{\tau} )_{+} \Big)QL(yτ​,y^​τ(q)​)=H1​∑τ=t+1t+H​((1−q)(y^​τ(q)​−yτ​)+​+q(yτ​−y^​τ(q)​)+​)
**Parameters:**  
 `quantile_sampling`: str, default=‘uniform’,
sampling distribution used to sample the quantiles during training.
Choose from [‘uniform’, ‘beta’].   
 `horizon_weight`: Tensor of size
h, weight for each timestamp of the forecasting window.   

**References:**  
 [Gouttes, Adèle, Kashif Rasul, Mateusz Koren,
Johannes Stephan, and Tofigh Naghibi, “Probabilistic Time Series
Forecasting with Implicit Quantile
Networks”.](http://arxiv.org/abs/2107.03743)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L466)
### [​](#iqloss-call)IQLoss.__call__


> CopyAsk AI IQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                   y_insample:torch.Tensor,
>                   mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`quantile_loss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#quantile_loss):
tensor (single value).*
## [​](#distributionloss)DistributionLoss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L1785)
### [​](#distributionloss-init)DistributionLoss.__init__


> CopyAsk AI DistributionLoss.__init__ (distribution, level=[80, 90], quantiles=None,
>                             num_samples=1000, return_params=False,
>                             horizon_weight=None, **distribution_kwargs)


*DistributionLoss
This PyTorch module wraps the `torch.distribution` classes allowing it
to interact with NeuralForecast models modularly. It shares the negative
log-likelihood as the optimization objective and a sample method to
generate empirically the quantiles defined by the `level` list.
Additionally, it implements a distribution transformation that
factorizes the scale-dependent likelihood parameters into a base scale
and a multiplier efficiently learnable within the network’s
non-linearities operating ranges.
Available distributions:  
 - Poisson  
 - Normal  
 - StudentT  
 -
NegativeBinomial  
 - Tweedie  
 - Bernoulli (Temporal
Classifiers)  
 - ISQF (Incremental Spline Quantile Function)
**Parameters:**  
 `distribution`: str, identifier of a
torch.distributions.Distribution class.  
 `level`: float list
[0,100], confidence levels for prediction intervals.  
 `quantiles`:
float list [0,1], alternative to level list, target quantiles.  

`num_samples`: int=500, number of samples for the empirical
quantiles.  
 `return_params`: bool=False, wether or not return the
Distribution parameters.  
 `horizon_weight`: Tensor of size h, weight
for each timestamp of the forecasting window.  
  

**References:**  
 - [PyTorch Probability Distributions Package:
StudentT.](https://pytorch.org/docs/stable/distributions.html#studentt)  
 -
[David Salinas, Valentin Flunkert, Jan Gasthaus, Tim Januschowski
(2020). “DeepAR: Probabilistic forecasting with autoregressive recurrent
networks”. International Journal of
Forecasting.](https://www.sciencedirect.com/science/article/pii/S0169207019301888)  
 -
[Park, Youngsuk, Danielle Maddix, François-Xavier Aubet, Kelvin Kan, Jan
Gasthaus, and Yuyang Wang (2022). “Learning Quantile Functions without
Quantile Crossing for Distribution-free Time Series
Forecasting”.](https://proceedings.mlr.press/v151/park22a.html)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L1949)
### [​](#distributionloss-sample)DistributionLoss.sample


> CopyAsk AI DistributionLoss.sample (distr_args:torch.Tensor,
>                           num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2019)
### [​](#distributionloss-call)DistributionLoss.__call__


> CopyAsk AI DistributionLoss.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                             mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `loc`:
Optional tensor, of the same shape as the batch_shape + event_shape of
the resulting distribution.  
 `scale`: Optional tensor, of the same
shape as the batch_shape+event_shape of the resulting distribution.  

`mask`: tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
## [​](#poisson-mixture-mesh-pmm)Poisson Mixture Mesh (PMM)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2053)
### [​](#pmm-init)PMM.__init__


> CopyAsk AI PMM.__init__ (n_components=10, level=[80, 90], quantiles=None,
>                num_samples=1000, return_params=False,
>                batch_correlation=False, horizon_correlation=False,
>                weighted=False)


*Poisson Mixture Mesh
This Poisson Mixture statistical model assumes independence across
groups of data G={[gi]}\mathcal{G}=\{[g_{i}]\}G={[gi​]}, and estimates relationships
within the group.
P(y[b][t+1:t+H])=∏[gi]∈GP(y[gi][τ])=∏β∈[gi](∑k=1Kwk∏(β,τ)∈[gi][t+1:t+H]Poisson(yβ,τ,λ^β,τ,k)) \mathrm{P}\left(\mathbf{y}_{[b][t+1:t+H]}\right) = 
\prod_{ [g_{i}] \in \mathcal{G}} \mathrm{P} \left(\mathbf{y}_{[g_{i}][\tau]} \right) =
\prod_{\beta\in[g_{i}]} 
\left(\sum_{k=1}^{K} w_k \prod_{(\beta,\tau) \in [g_i][t+1:t+H]} \mathrm{Poisson}(y_{\beta,\tau}, \hat{\lambda}_{\beta,\tau,k}) \right)P(y[b][t+1:t+H]​)=[gi​]∈G∏​P(y[gi​][τ]​)=β∈[gi​]∏​​k=1∑K​wk​(β,τ)∈[gi​][t+1:t+H]∏​Poisson(yβ,τ​,λ^β,τ,k​)​
**Parameters:**  
 `n_components`: int=10, the number of mixture
components.  
 `level`: float list [0,100], confidence levels for
prediction intervals.  
 `quantiles`: float list [0,1], alternative
to level list, target quantiles.  
 `return_params`: bool=False, wether
or not return the Distribution parameters.  
 `batch_correlation`:
bool=False, wether or not model batch correlations.  

`horizon_correlation`: bool=False, wether or not model horizon
correlations.  

**References:**  
 [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan
Reddy, Mengfei Cao, Lee Dicker. Probabilistic Hierarchical Forecasting
with Deep Poisson Mixtures. Submitted to the International Journal
Forecasting, Working paper available at
arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2192)
### [​](#pmm-sample)PMM.sample


> CopyAsk AI PMM.sample (distr_args:torch.Tensor, num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2241)
### [​](#pmm-call)PMM.__call__


> CopyAsk AI PMM.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `mask`:
tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/pmm.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=cd0e3519dafef82789a957abafcb5ad8)
## [​](#gaussian-mixture-mesh-gmm)Gaussian Mixture Mesh (GMM)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2279)
### [​](#gmm-init)GMM.__init__


> CopyAsk AI GMM.__init__ (n_components=1, level=[80, 90], quantiles=None,
>                num_samples=1000, return_params=False,
>                batch_correlation=False, horizon_correlation=False,
>                weighted=False)


*Gaussian Mixture Mesh
This Gaussian Mixture statistical model assumes independence across
groups of data G={[gi]}\mathcal{G}=\{[g_{i}]\}G={[gi​]}, and estimates relationships
within the group.
P(y[b][t+1:t+H])=∏[gi]∈GP(y[gi][τ])=∏β∈[gi](∑k=1Kwk∏(β,τ)∈[gi][t+1:t+H]Gaussian(yβ,τ,μ^β,τ,k,σβ,τ,k)) \mathrm{P}\left(\mathbf{y}_{[b][t+1:t+H]}\right) = 
\prod_{ [g_{i}] \in \mathcal{G}} \mathrm{P}\left(\mathbf{y}_{[g_{i}][\tau]}\right)=
\prod_{\beta\in[g_{i}]}
\left(\sum_{k=1}^{K} w_k \prod_{(\beta,\tau) \in [g_i][t+1:t+H]} 
\mathrm{Gaussian}(y_{\beta,\tau}, \hat{\mu}_{\beta,\tau,k}, \sigma_{\beta,\tau,k})\right)P(y[b][t+1:t+H]​)=[gi​]∈G∏​P(y[gi​][τ]​)=β∈[gi​]∏​​k=1∑K​wk​(β,τ)∈[gi​][t+1:t+H]∏​Gaussian(yβ,τ​,μ^​β,τ,k​,σβ,τ,k​)​
**Parameters:**  
 `n_components`: int=10, the number of mixture
components.  
 `level`: float list [0,100], confidence levels for
prediction intervals.  
 `quantiles`: float list [0,1], alternative
to level list, target quantiles.  
 `return_params`: bool=False, wether
or not return the Distribution parameters.  
 `batch_correlation`:
bool=False, wether or not model batch correlations.  

`horizon_correlation`: bool=False, wether or not model horizon
correlations.  
  

**References:**  
 [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan
Reddy, Mengfei Cao, Lee Dicker. Probabilistic Hierarchical Forecasting
with Deep Poisson Mixtures. Submitted to the International Journal
Forecasting, Working paper available at
arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2422)
### [​](#gmm-sample)GMM.sample


> CopyAsk AI GMM.sample (distr_args:torch.Tensor, num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2471)
### [​](#gmm-call)GMM.__call__


> CopyAsk AI GMM.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `mask`:
tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/gmm.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=137c048f21d86e054bc5f2405628fd5f)
## [​](#negative-binomial-mixture-mesh-nbmm)Negative Binomial Mixture Mesh (NBMM)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2508)
### [​](#nbmm-init)NBMM.__init__


> CopyAsk AI NBMM.__init__ (n_components=1, level=[80, 90], quantiles=None,
>                 num_samples=1000, return_params=False, weighted=False)


*Negative Binomial Mixture Mesh
This N. Binomial Mixture statistical model assumes independence across
groups of data G={[gi]}\mathcal{G}=\{[g_{i}]\}G={[gi​]}, and estimates relationships
within the group.
P(y[b][t+1:t+H])=∏[gi]∈GP(y[gi][τ])=∏β∈[gi](∑k=1Kwk∏(β,τ)∈[gi][t+1:t+H]NBinomial(yβ,τ,r^β,τ,k,p^β,τ,k)) \mathrm{P}\left(\mathbf{y}_{[b][t+1:t+H]}\right) = 
\prod_{ [g_{i}] \in \mathcal{G}} \mathrm{P}\left(\mathbf{y}_{[g_{i}][\tau]}\right)=
\prod_{\beta\in[g_{i}]}
\left(\sum_{k=1}^{K} w_k \prod_{(\beta,\tau) \in [g_i][t+1:t+H]} 
\mathrm{NBinomial}(y_{\beta,\tau}, \hat{r}_{\beta,\tau,k}, \hat{p}_{\beta,\tau,k})\right)P(y[b][t+1:t+H]​)=[gi​]∈G∏​P(y[gi​][τ]​)=β∈[gi​]∏​​k=1∑K​wk​(β,τ)∈[gi​][t+1:t+H]∏​NBinomial(yβ,τ​,r^β,τ,k​,p^​β,τ,k​)​
**Parameters:**  
 `n_components`: int=10, the number of mixture
components.  
 `level`: float list [0,100], confidence levels for
prediction intervals.  
 `quantiles`: float list [0,1], alternative
to level list, target quantiles.  
 `return_params`: bool=False, wether
or not return the Distribution parameters.  
  

**References:**  
 [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan
Reddy, Mengfei Cao, Lee Dicker. Probabilistic Hierarchical Forecasting
with Deep Poisson Mixtures. Submitted to the International Journal
Forecasting, Working paper available at
arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2655)
### [​](#nbmm-sample)NBMM.sample


> CopyAsk AI NBMM.sample (distr_args:torch.Tensor, num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2704)
### [​](#nbmm-call)NBMM.__call__


> CopyAsk AI NBMM.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                 mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `mask`:
tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
# [​](#5-robustified-errors)5. Robustified Errors


This type of errors from robust statistic focus on methods resistant to
outliers and violations of assumptions, providing reliable estimates and
inferences. Robust estimators are used to reduce the impact of outliers,
offering more stable results.
## [​](#huber-loss)Huber Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2735)
### [​](#huberloss-init)HuberLoss.__init__


> CopyAsk AI HuberLoss.__init__ (delta:float=1.0, horizon_weight=None)


*Huber Loss
The Huber loss, employed in robust regression, is a loss function that
exhibits reduced sensitivity to outliers in data when compared to the
squared error loss. This function is also refered as SmoothL1.
The Huber loss function is quadratic for small errors and linear for
large errors, with equal values and slopes of the different sections at
the two points where
(yτ−y^τ)2(y_{\tau}-\hat{y}_{\tau})^{2}(yτ​−y^​τ​)2=∣yτ−y^τ∣|y_{\tau}-\hat{y}_{\tau}|∣yτ​−y^​τ​∣.
Lδ(yτ,  y^τ)={12(yτ−y^τ)2  for ∣yτ−y^τ∣≤δδ ⋅(∣yτ−y^τ∣−12δ),  otherwise. L_{\delta}(y_{\tau},\; \hat{y}_{\tau})
=\begin{cases}{\frac{1}{2}}(y_{\tau}-\hat{y}_{\tau})^{2}\;{\text{for }}|y_{\tau}-\hat{y}_{\tau}|\leq \delta \\ 
\delta \ \cdot \left(|y_{\tau}-\hat{y}_{\tau}|-{\frac {1}{2}}\delta \right),\;{\text{otherwise.}}\end{cases}Lδ​(yτ​,y^​τ​)={21​(yτ​−y^​τ​)2for ∣yτ​−y^​τ​∣≤δδ ⋅(∣yτ​−y^​τ​∣−21​δ),otherwise.​
where δ\deltaδ is a threshold parameter that determines the point at
which the loss transitions from quadratic to linear, and can be tuned to
control the trade-off between robustness and accuracy in the
predictions.
**Parameters:**  
 `delta`: float=1.0, Specifies the threshold at which
to change between delta-scaled L1 and L2 loss. `horizon_weight`: Tensor
of size h, weight for each timestamp of the forecasting window.   

**References:**  
 [Huber Peter, J (1964). “Robust Estimation of a
Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2767)
### [​](#huberloss-call)HuberLoss.__call__


> CopyAsk AI HuberLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                      y_insample:torch.Tensor,
>                      mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `huber_loss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/huber_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=2598d8e03e7b8061c8a6f5abc8de00c7)
## [​](#tukey-loss)Tukey Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2788)
### [​](#tukeyloss-init)TukeyLoss.__init__


> CopyAsk AI TukeyLoss.__init__ (c:float=4.685, normalize:bool=True)


*Tukey Loss
The Tukey loss function, also known as Tukey’s biweight function, is a
robust statistical loss function used in robust statistics. Tukey’s loss
exhibits quadratic behavior near the origin, like the Huber loss;
however, it is even more robust to outliers as the loss for large
residuals remains constant instead of scaling linearly.
The parameter ccc in Tukey’s loss determines the ‘’saturation’’ point of
the function: Higher values of ccc enhance sensitivity, while lower
values increase resistance to outliers.
Lc(yτ,  y^τ)={c26[1−(yτ−y^τc)2]3  for ∣yτ−y^τ∣≤cc26otherwise. L_{c}(y_{\tau},\; \hat{y}_{\tau})
=\begin{cases}{
\frac{c^{2}}{6}} \left[1-(\frac{y_{\tau}-\hat{y}_{\tau}}{c})^{2} \right]^{3}    \;\text{for } |y_{\tau}-\hat{y}_{\tau}|\leq c \\ 
\frac{c^{2}}{6} \qquad \text{otherwise.}  \end{cases}Lc​(yτ​,y^​τ​)=⎩⎨⎧​6c2​[1−(cyτ​−y^​τ​​)2]3for ∣yτ​−y^​τ​∣≤c6c2​otherwise.​
Please note that the Tukey loss function assumes the data to be
stationary or normalized beforehand. If the error values are excessively
large, the algorithm may need help to converge during optimization. It
is advisable to employ small learning rates.
**Parameters:**  
 `c`: float=4.685, Specifies the Tukey loss’
threshold on which residuals are no longer considered.  
 `normalize`:
bool=True, Wether normalization is performed within Tukey loss’
computation.  

**References:**  
 [Beaton, A. E., and Tukey, J. W. (1974). “The
Fitting of Power Series, Meaning Polynomials, Illustrated on
Band-Spectroscopic Data.”](https://www.jstor.org/stable/1267936)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2843)
### [​](#tukeyloss-call)TukeyLoss.__call__


> CopyAsk AI TukeyLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                      y_insample:torch.Tensor,
>                      mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `tukey_loss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/tukey_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=1d0b4dcd359c5b2f6248a86839d3d772)
## [​](#huberized-quantile-loss)Huberized Quantile Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2881)
### [​](#huberqloss-init)HuberQLoss.__init__


> CopyAsk AI HuberQLoss.__init__ (q, delta:float=1.0, horizon_weight=None)


*Huberized Quantile Loss
The Huberized quantile loss is a modified version of the quantile loss
function that combines the advantages of the quantile loss and the Huber
loss. It is commonly used in regression tasks, especially when dealing
with data that contains outliers or heavy tails.
The Huberized quantile loss between `y` and `y_hat` measure the Huber
Loss in a non-symmetric way. The loss pays more attention to
under/over-estimation depending on the quantile parameter qqq; and
controls the trade-off between robustness and accuracy in the
predictions with the parameter deltadeltadelta.
HuberQL(yτ,y^τ(q))=(1−q) Lδ(yτ,  y^τ(q))1{y^τ(q)≥yτ}+q Lδ(yτ,  y^τ(q))1{y^τ(q)<yτ} \mathrm{HuberQL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = 
(1-q)\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} \geq y_{\tau} \} + 
q\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} < y_{\tau} \} HuberQL(yτ​,y^​τ(q)​)=(1−q)Lδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​≥yτ​}+qLδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​<yτ​}
**Parameters:**  
 `delta`: float=1.0, Specifies the threshold at which
to change between delta-scaled L1 and L2 loss.  
 `q`: float, between 0
and 1. The slope of the quantile loss, in the context of quantile
regression, the q determines the conditional quantile level.  

`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 [Huber Peter, J (1964). “Robust Estimation of a
Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)  

[Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2915)
### [​](#huberqloss-call)HuberQLoss.__call__


> CopyAsk AI HuberQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                       y_insample:torch.Tensor,
>                       mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  
 `huber_qloss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/huber_qloss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=4f51acd268108c2f53904b76846f181e)
## [​](#huberized-mqloss)Huberized MQLoss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2946)
### [​](#hubermqloss-init)HuberMQLoss.__init__


> CopyAsk AI HuberMQLoss.__init__ (level=[80, 90], quantiles=None, delta:float=1.0,
>                        horizon_weight=None)


*Huberized Multi-Quantile loss
The Huberized Multi-Quantile loss (HuberMQL) is a modified version of
the multi-quantile loss function that combines the advantages of the
quantile loss and the Huber loss. HuberMQL is commonly used in
regression tasks, especially when dealing with data that contains
outliers or heavy tails. The loss function pays more attention to
under/over-estimation depending on the quantile list
[q1,q2,… ][q_{1},q_{2},\dots][q1​,q2​,…] parameter. It controls the trade-off between
robustness and prediction accuracy with the parameter δ\deltaδ.
HuberMQLδ(yτ,[y^τ(q1),...,y^τ(qn)])=1n∑qiHuberQLδ(yτ,y^τ(qi)) \mathrm{HuberMQL}_{\delta}(\mathbf{y}_{\tau},[\mathbf{\hat{y}}^{(q_{1})}_{\tau}, ... ,\hat{y}^{(q_{n})}_{\tau}]) = 
\frac{1}{n} \sum_{q_{i}} \mathrm{HuberQL}_{\delta}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q_{i})}_{\tau}) HuberMQLδ​(yτ​,[y^​τ(q1​)​,...,y^​τ(qn​)​])=n1​qi​∑​HuberQLδ​(yτ​,y^​τ(qi​)​)
**Parameters:**  
 `level`: int list [0,100]. Probability levels for
prediction intervals (Defaults median). `quantiles`: float list [0.,
1.]. Alternative to level, quantiles to estimate from y distribution.
`delta`: float=1.0, Specifies the threshold at which to change between
delta-scaled L1 and L2 loss.  
  

`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 [Huber Peter, J (1964). “Robust Estimation of a
Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)  

[Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3022)
### [​](#hubermqloss-call)HuberMQLoss.__call__


> CopyAsk AI HuberMQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                        y_insample:torch.Tensor,
>                        mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `hmqloss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/hmq_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=4458c07fbc5382a46e31553d60a36902)
## [​](#huberized-iqloss)Huberized IQLoss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3067)
### [​](#huberiqloss-init)HuberIQLoss.__init__


> CopyAsk AI HuberIQLoss.__init__ (cos_embedding_dim=64, concentration0=1.0,
>                        concentration1=1.0, delta=1.0, horizon_weight=None)


*Implicit Huber Quantile Loss
Computes the huberized quantile loss between `y` and `y_hat`, with the
quantile `q` provided as an input to the network. HuberIQLoss measures
the deviation of a huberized quantile forecast. By weighting the
absolute deviation in a non symmetric way, the loss pays more attention
to under or over estimation.
HuberQL(yτ,y^τ(q))=(1−q) Lδ(yτ,  y^τ(q))1{y^τ(q)≥yτ}+q Lδ(yτ,  y^τ(q))1{y^τ(q)<yτ} \mathrm{HuberQL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = 
(1-q)\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} \geq y_{\tau} \} + 
q\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} < y_{\tau} \} HuberQL(yτ​,y^​τ(q)​)=(1−q)Lδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​≥yτ​}+qLδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​<yτ​}
**Parameters:**  
 `quantile_sampling`: str, default=‘uniform’,
sampling distribution used to sample the quantiles during training.
Choose from [‘uniform’, ‘beta’].   
 `horizon_weight`: Tensor of size
h, weight for each timestamp of the forecasting window.   
 `delta`:
float=1.0, Specifies the threshold at which to change between
delta-scaled L1 and L2 loss.  

**References:**  
 [Gouttes, Adèle, Kashif Rasul, Mateusz Koren,
Johannes Stephan, and Tofigh Naghibi, “Probabilistic Time Series
Forecasting with Implicit Quantile
Networks”.](http://arxiv.org/abs/2107.03743) [Huber Peter, J (1964).
“Robust Estimation of a Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)  

[Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2915)
### [​](#huberiqloss-call)HuberIQLoss.__call__


> CopyAsk AI HuberIQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                        y_insample:torch.Tensor,
>                        mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  
 `huber_qloss`: tensor (single value).*
# [​](#6-others)6. Others


## [​](#accuracy)Accuracy



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3174)
### [​](#accuracy-init)Accuracy.__init__


> CopyAsk AI Accuracy.__init__ ()


*Accuracy
Computes the accuracy between categorical `y` and `y_hat`. This
evaluation metric is only meant for evalution, as it is not
differentiable.
Accuracy(yτ,y^τ)=1H∑τ=t+1t+H1{yτ==y^τ}\mathrm{Accuracy}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \mathrm{1}\{\mathbf{y}_{\tau}==\mathbf{\hat{y}}_{\tau}\}Accuracy(yτ​,y^​τ​)=H1​∑τ=t+1t+H​1{yτ​==y^​τ​}*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3203)
### [​](#accuracy-call)Accuracy.__call__


> CopyAsk AI Accuracy.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                     y_insample:torch.Tensor,
>                     mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `accuracy`: tensor (single value).*
## [​](#scaled-continuous-ranked-probability-score-scrps)Scaled Continuous Ranked Probability Score (sCRPS)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3228)
### [​](#scrps-init)sCRPS.__init__


> CopyAsk AI sCRPS.__init__ (level=[80, 90], quantiles=None)


*Scaled Continues Ranked Probability Score
Calculates a scaled variation of the CRPS, as proposed by Rangapuram
(2021), to measure the accuracy of predicted quantiles `y_hat` compared
to the observation `y`.
This metric averages percentual weighted absolute deviations as defined
by the quantile losses.
sCRPS(y^τ(q),yτ)=2N∑i∫01QL(y^τ(qyi,τ)q∑i∣yi,τ∣dq \mathrm{sCRPS}(\mathbf{\hat{y}}^{(q)}_{\tau}, \mathbf{y}_{\tau}) = \frac{2}{N} \sum_{i}
\int^{1}_{0}
\frac{\mathrm{QL}(\mathbf{\hat{y}}^{(q}_{\tau} y_{i,\tau})_{q}}{\sum_{i} | y_{i,\tau} |} dq sCRPS(y^​τ(q)​,yτ​)=N2​i∑​∫01​∑i​∣yi,τ​∣QL(y^​τ(q​yi,τ​)q​​dq
where y^τ(q\mathbf{\hat{y}}^{(q}_{\tau}y^​τ(q​ is the estimated quantile, and
yi,τy_{i,\tau}yi,τ​ are the target variable realizations.
**Parameters:**  
 `level`: int list [0,100]. Probability levels for
prediction intervals (Defaults median). `quantiles`: float list [0.,
1.]. Alternative to level, quantiles to estimate from y distribution.
**References:**  
 - [Gneiting, Tilmann. (2011). “Quantiles as optimal
point forecasts”. International Journal of
Forecasting.](https://www.sciencedirect.com/science/article/pii/S0169207010000063)  
 -
[Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, Zhi
Chen, Anil Gaba, Ilia Tsetlin, Robert L. Winkler. (2022). “The M5
uncertainty competition: Results, findings and conclusions”.
International Journal of
Forecasting.](https://www.sciencedirect.com/science/article/pii/S0169207021001722)  
 -
[Syama Sundar Rangapuram, Lucien D Werner, Konstantinos Benidis, Pedro
Mercado, Jan Gasthaus, Tim Januschowski. (2021). “End-to-End Learning of
Coherent Probabilistic Forecasts for Hierarchical Time Series”.
Proceedings of the 38th International Conference on Machine Learning
(ICML).](https://proceedings.mlr.press/v139/rangapuram21a.html)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3264)
### [​](#scrps-call)sCRPS.__call__


> CopyAsk AI sCRPS.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                  y_insample:torch.Tensor,
>                  mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per series
to consider in loss.  

**Returns:**  
 `scrps`: tensor (single value).*

---

## Core - Nixtla
<a id="Core-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/core.html

NeuralForecast contains two main components, PyTorch implementations deep learning predictive models, as well as parallelization and distributed computation utilities. The first component comprises low-level PyTorch model estimator classes like `models.NBEATS` and `models.RNN`. The second component is a high-level `core.NeuralForecast` wrapper class that operates with sets of time series data stored in pandas DataFrames.

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/core.py#L217)
### [​](#neuralforecast)NeuralForecast


> CopyAsk AI NeuralForecast (models:List[Any], freq:Union[str,int],
>                  local_scaler_type:Optional[str]=None)


*The `core.StatsForecast` class allows you to efficiently fit multiple
[`NeuralForecast`](https://nixtlaverse.nixtla.io/neuralforecast/core.html#neuralforecast)
models for large sets of time series. It operates with pandas DataFrame
`df` that identifies series and datestamps with the `unique_id` and `ds`
columns. The `y` column denotes the target time series variable.*
**Type****Default****Details**modelsListInstantiated `neuralforecast.models`   
see [collection here](https://nixtla.github.io/neuralforecast/models.html).freqUnionFrequency of the data. Must be a valid pandas or polars offset alias, or an integer.local_scaler_typeOptionalNoneScaler to apply per-serie to all features before fitting, which is inverted after predicting.  
Can be ‘standard’, ‘robust’, ‘robust-iqr’, ‘minmax’ or ‘boxcox’**Returns****NeuralForecast****Returns instantiated [`NeuralForecast`](https://nixtlaverse.nixtla.io/neuralforecast/core.html#neuralforecast) class.**

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/core.py#L418)
### [​](#neuralforecast-fit)NeuralForecast.fit


> CopyAsk AI NeuralForecast.fit (df:Union[pandas.core.frame.DataFrame,polars.dataframe
>                      .frame.DataFrame,neuralforecast.compat.SparkDataFrame
>                      ,Sequence[str],NoneType]=None, static_df:Union[pandas
>                      .core.frame.DataFrame,polars.dataframe.frame.DataFram
>                      e,neuralforecast.compat.SparkDataFrame,NoneType]=None
>                      , val_size:Optional[int]=0,
>                      use_init_models:bool=False, verbose:bool=False,
>                      id_col:str='unique_id', time_col:str='ds',
>                      target_col:str='y', distributed_config:Optional[neura
>                      lforecast.common._base_model.DistributedConfig]=None,
>                      prediction_intervals:Optional[neuralforecast.utils.Pr
>                      edictionIntervals]=None)


*Fit the core.NeuralForecast.
Fit `models` to a large set of time series from DataFrame `df`. and
store fitted models for later inspection.*
**Type****Default****Details**dfUnionNoneDataFrame with columns [`unique_id`, `ds`, `y`] and exogenous variables.  
If None, a previously stored dataset is required.static_dfUnionNoneDataFrame with columns [`unique_id`] and static exogenous.val_sizeOptional0Size of validation set.use_init_modelsboolFalseUse initial model passed when NeuralForecast object was instantiated.verboseboolFalsePrint processing steps.id_colstrunique_idColumn that identifies each serie.time_colstrdsColumn that identifies each timestep, its values can be timestamps or integers.target_colstryColumn that contains the target.distributed_configOptionalNoneConfiguration to use for DDP training. Currently only spark is supported.prediction_intervalsOptionalNoneConfiguration to calibrate prediction intervals (Conformal Prediction).**Returns****NeuralForecast****Returns [`NeuralForecast`](https://nixtlaverse.nixtla.io/neuralforecast/core.html#neuralforecast) class with fitted `models`.**

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/core.py#L796)
### [​](#neuralforecast-predict)NeuralForecast.predict


> CopyAsk AI NeuralForecast.predict (df:Union[pandas.core.frame.DataFrame,polars.dataf
>                          rame.frame.DataFrame,neuralforecast.compat.SparkD
>                          ataFrame,NoneType]=None, static_df:Union[pandas.c
>                          ore.frame.DataFrame,polars.dataframe.frame.DataFr
>                          ame,neuralforecast.compat.SparkDataFrame,NoneType
>                          ]=None, futr_df:Union[pandas.core.frame.DataFrame
>                          ,polars.dataframe.frame.DataFrame,neuralforecast.
>                          compat.SparkDataFrame,NoneType]=None,
>                          verbose:bool=False, engine=None,
>                          level:Optional[List[Union[int,float]]]=None,
>                          quantiles:Optional[List[float]]=None,
>                          **data_kwargs)


*Predict with core.NeuralForecast.
Use stored fitted `models` to predict large set of time series from
DataFrame `df`.*
**Type****Default****Details**dfUnionNoneDataFrame with columns [`unique_id`, `ds`, `y`] and exogenous variables.  
If a DataFrame is passed, it is used to generate forecasts.static_dfUnionNoneDataFrame with columns [`unique_id`] and static exogenous.futr_dfUnionNoneDataFrame with [`unique_id`, `ds`] columns and `df`’s future exogenous.verboseboolFalsePrint processing steps.engineNoneTypeNoneDistributed engine for inference. Only used if df is a spark dataframe or if fit was called on a spark dataframe.levelOptionalNoneConfidence levels between 0 and 100.quantilesOptionalNoneAlternative to level, target quantiles to predict.data_kwargsVAR_KEYWORDExtra arguments to be passed to the dataset within each model.**Returns****pandas or polars DataFrame****DataFrame with insample `models` columns for point predictions and probabilistic  
predictions for all fitted `models`. **

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/core.py#L1089)
### [​](#neuralforecast-cross-validation)NeuralForecast.cross_validation


> CopyAsk AI NeuralForecast.cross_validation (df:Union[pandas.core.frame.DataFrame,pol
>                                   ars.dataframe.frame.DataFrame,NoneType]=
>                                   None, static_df:Union[pandas.core.frame.
>                                   DataFrame,polars.dataframe.frame.DataFra
>                                   me,NoneType]=None, n_windows:int=1,
>                                   step_size:int=1,
>                                   val_size:Optional[int]=0,
>                                   test_size:Optional[int]=None,
>                                   use_init_models:bool=False,
>                                   verbose:bool=False,
>                                   refit:Union[bool,int]=False,
>                                   id_col:str='unique_id',
>                                   time_col:str='ds', target_col:str='y', p
>                                   rediction_intervals:Optional[neuralforec
>                                   ast.utils.PredictionIntervals]=None, lev
>                                   el:Optional[List[Union[int,float]]]=None
>                                   , quantiles:Optional[List[float]]=None,
>                                   **data_kwargs)


*Temporal Cross-Validation with core.NeuralForecast.
`core.NeuralForecast`’s cross-validation efficiently fits a list of
NeuralForecast models through multiple windows, in either chained or
rolled manner.*
**Type****Default****Details**dfUnionNoneDataFrame with columns [`unique_id`, `ds`, `y`] and exogenous variables.  
If None, a previously stored dataset is required.static_dfUnionNoneDataFrame with columns [`unique_id`] and static exogenous.n_windowsint1Number of windows used for cross validation.step_sizeint1Step size between each window.val_sizeOptional0Length of validation size. If passed, set `n_windows=None`.test_sizeOptionalNoneLength of test size. If passed, set `n_windows=None`.use_init_modelsboolFalseUse initial model passed when object was instantiated.verboseboolFalsePrint processing steps.refitUnionFalseRetrain model for each cross validation window.  
If False, the models are trained at the beginning and then used to predict each window.  
If positive int, the models are retrained every `refit` windows.id_colstrunique_idColumn that identifies each serie.time_colstrdsColumn that identifies each timestep, its values can be timestamps or integers.target_colstryColumn that contains the target.prediction_intervalsOptionalNoneConfiguration to calibrate prediction intervals (Conformal Prediction).levelOptionalNoneConfidence levels between 0 and 100.quantilesOptionalNoneAlternative to level, target quantiles to predict.data_kwargsVAR_KEYWORDExtra arguments to be passed to the dataset within each model.**Returns****Union****DataFrame with insample `models` columns for point predictions and probabilistic  
predictions for all fitted `models`. **

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/core.py#L1262)
### [​](#neuralforecast-predict-insample)NeuralForecast.predict_insample


> CopyAsk AI NeuralForecast.predict_insample (step_size:int=1,
>                                   level:Optional[List[Union[int,float]]]=N
>                                   one,
>                                   quantiles:Optional[List[float]]=None)


*Predict insample with core.NeuralForecast.
`core.NeuralForecast`’s `predict_insample` uses stored fitted `models`
to predict historic values of a time series from the stored dataframe.*
**Type****Default****Details**step_sizeint1Step size between each window.levelOptionalNoneConfidence levels between 0 and 100.quantilesOptionalNoneAlternative to level, target quantiles to predict.**Returns****pandas.DataFrame****DataFrame with insample predictions for all fitted `models`. **

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/core.py#L1433)
### [​](#neuralforecast-save)NeuralForecast.save


> CopyAsk AI NeuralForecast.save (path:str, model_index:Optional[List]=None,
>                       save_dataset:bool=True, overwrite:bool=False)


*Save NeuralForecast core class.
`core.NeuralForecast`’s method to save current status of models,
dataset, and configuration. Note that by default the `models` are not
saving training checkpoints to save disk memory, to get them change the
individual model `**trainer_kwargs` to include
`enable_checkpointing=True`.*
**Type****Default****Details**pathstrDirectory to save current status.model_indexOptionalNoneList to specify which models from list of self.models to save.save_datasetboolTrueWhether to save dataset or not.overwriteboolFalseWhether to overwrite files or not.
CopyAsk AI```
/opt/hostedtoolcache/Python/3.10.17/x64/lib/python3.10/site-packages/fastcore/docscrape.py:230: UserWarning: potentially wrong underline length... 
Parameters 
----------- in 
Load NeuralForecast
...
  else: warn(msg)
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/core.py#L1549)
### [​](#neuralforecast-load)NeuralForecast.load


> CopyAsk AI NeuralForecast.load (path, verbose=False, **kwargs)


*Load NeuralForecast
`core.NeuralForecast`’s method to load checkpoint from path.*
**Type****Default****Details**pathstrDirectory with stored artifacts.verboseboolFalsekwargsVAR_KEYWORDAdditional keyword arguments to be passed to the function  
`load_from_checkpoint`.**Returns****NeuralForecast****Instantiated [`NeuralForecast`](https://nixtlaverse.nixtla.io/neuralforecast/core.html#neuralforecast) class.**
CopyAsk AI```
# Test predict_insample step_size

h = 12
train_end = AirPassengersPanel_train['ds'].max()
sizes = AirPassengersPanel_train['unique_id'].value_counts().to_numpy()
for step_size, test_size in [(7, 0), (9, 0), (7, 5), (9, 5)]:
    models = [NHITS(h=h, input_size=12, max_steps=1)]
    nf = NeuralForecast(models=models, freq='M')
    nf.fit(AirPassengersPanel_train)
    # Note: only apply set_test_size() upon nf.fit(), otherwise it would have set the test_size = 0
    nf.models[0].set_test_size(test_size)
    
    forecasts = nf.predict_insample(step_size=step_size)
    last_cutoff = train_end - test_size * pd.offsets.MonthEnd() - h * pd.offsets.MonthEnd()
    n_expected_cutoffs = (sizes[0] - test_size - nf.h + step_size) // step_size

    # compare cutoff values
    expected_cutoffs = np.flip(np.array([last_cutoff - step_size * i * pd.offsets.MonthEnd() for i in range(n_expected_cutoffs)]))
    actual_cutoffs = np.array([pd.Timestamp(x) for x in forecasts[forecasts['unique_id']==nf.uids[1]]['cutoff'].unique()])
    np.testing.assert_array_equal(expected_cutoffs, actual_cutoffs, err_msg=f"{step_size=},{expected_cutoffs=},{actual_cutoffs=}")
    
    # check forecast-points count per series
    cutoffs_by_series = forecasts.groupby(['unique_id', 'cutoff']).size().unstack('unique_id')
    pd.testing.assert_series_equal(cutoffs_by_series['Airline1'], cutoffs_by_series['Airline2'], check_names=False)
```


CopyAsk AI```
# Test predict_insample

def get_expected_cols(model, level):
    # index columns
    n_cols = 4
    for model in models:
        if isinstance(loss, (DistributionLoss, PMM, GMM, NBMM)):
            if level is None:
                # Variations of DistributionLoss return the sample mean as well
                n_cols += len(loss.quantiles) + 1
            else:
                # Variations of DistributionLoss return the sample mean as well
                n_cols += 2 * len(level) + 1
        else:
            if level is None:
                # Other probabilistic models return the sample mean as well
                n_cols += 1
            # Other probabilistic models return just the levels
            else:
                n_cols += len(level) + 1
    return n_cols

for loss in [
    # IQLoss(), 
    DistributionLoss(distribution="Normal", level=[80]),
    PMM(level=[80]),
]:
    for level in [None, [80, 90]]:
        models = [
            NHITS(h=12, input_size=12, loss=loss, max_steps=1),
            LSTM(h=12, input_size=12, loss=loss, max_steps=1, recurrent=True),
        ]
        nf = NeuralForecast(models=models, freq='D')

        nf.fit(df=AirPassengersPanel_train)
        df = nf.predict_insample(step_size=1, level=level)
        expected_cols = get_expected_cols(models, level)
        assert df.shape[1] == expected_cols, f'Shape mismatch for {loss} and level={level} in predict_insample: cols={df.shape[1]}, expected_cols={expected_cols}'
```


CopyAsk AI```
def config_optuna(trial):
    return {"input_size": trial.suggest_categorical('input_size', [12, 24]),
        "hist_exog_list": trial.suggest_categorical('hist_exog_list', [['trend'], ['y_[lag12]'], ['trend', 'y_[lag12]']]),
        "futr_exog_list": ['trend'],
        "max_steps": 10,
        "val_check_steps": 5}

config_ray = {'input_size': tune.choice([12, 24]), 
          'hist_exog_list': tune.choice([['trend'], ['y_[lag12]'], ['trend', 'y_[lag12]']]),
          'futr_exog_list': ['trend'],
          'max_steps': 10,
          'val_check_steps': 5}
```


CopyAsk AI```
# Test predict_insample step_size

h = 12
train_end = AirPassengers_pl['time'].max()
sizes = AirPassengers_pl['uid'].value_counts().to_numpy()

for step_size, test_size in [(7, 0), (9, 0), (7, 5), (9, 5)]:
    models = [NHITS(h=h, input_size=12, max_steps=1)]
    nf = NeuralForecast(models=models, freq='1mo')
    nf.fit(
        AirPassengers_pl,
        id_col='uid',
        time_col='time',
        target_col='target',    
    )
    # Note: only apply set_test_size() upon nf.fit(), otherwise it would have set the test_size = 0
    nf.models[0].set_test_size(test_size)    
    
    forecasts = nf.predict_insample(step_size=step_size)
    n_expected_cutoffs = (sizes[0][1] - test_size - nf.h + step_size) // step_size

    # compare cutoff values
    last_cutoff = train_end - test_size * pd.offsets.MonthEnd() - h * pd.offsets.MonthEnd()
    expected_cutoffs = np.flip(np.array([last_cutoff - step_size * i * pd.offsets.MonthEnd() for i in range(n_expected_cutoffs)]))
    pl_cutoffs = forecasts.filter(polars.col('uid') ==nf.uids[1]).select('cutoff').unique(maintain_order=True)
    actual_cutoffs = np.sort(np.array([pd.Timestamp(x['cutoff']) for x in pl_cutoffs.rows(named=True)]))
    np.testing.assert_array_equal(expected_cutoffs, actual_cutoffs, err_msg=f"{step_size=},{expected_cutoffs=},{actual_cutoffs=}")

    # check forecast-points count per series
    cutoffs_by_series = forecasts.group_by(['uid', 'cutoff']).count()
    assert_frame_equal(cutoffs_by_series.filter(polars.col('uid') == "Airline1").select(['cutoff', 'count']), cutoffs_by_series.filter(polars.col('uid') == "Airline2").select(['cutoff', 'count'] ), check_row_order=False)
```

---

## Reversible Mixture of KAN - RMoK - Nixtla
<a id="Reversible-Mixture-of-KAN-RMoK-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.rmok.html

## [​](#1-auxiliary-functions)1. Auxiliary functions


### [​](#1-1-wavekan)1.1 WaveKAN



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/rmok.py#L19)
### [​](#wavekanlayer)WaveKANLayer


> CopyAsk AI WaveKANLayer (in_features, out_features, wavelet_type='mexican_hat',
>                with_bn=True, device='cpu')


*This is a sample code for the simulations of the paper: Bozorgasl,
Zavareh and Chen, Hao, Wav-KAN: Wavelet Kolmogorov-Arnold Networks (May,
2024)
[https://arxiv.org/abs/2405.12832](https://arxiv.org/abs/2405.12832) and also available at:
[https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4835325](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4835325) We used
efficient KAN notation and some part of the code:+*
### [​](#1-2-taylorkan)1.2 TaylorKAN



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/rmok.py#L163)
### [​](#taylorkanlayer)TaylorKANLayer


> CopyAsk AI TaylorKANLayer (input_dim, out_dim, order, addbias=True)


*[https://github.com/Muyuzhierchengse/TaylorKAN/](https://github.com/Muyuzhierchengse/TaylorKAN/)*
### [​](#1-3-jacobikan)1.3. JacobiKAN



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/rmok.py#L198)
### [​](#jacobikanlayer)JacobiKANLayer


> CopyAsk AI JacobiKANLayer (input_dim, output_dim, degree, a=1.0, b=1.0)


*[https://github.com/SpaceLearner/JacobiKAN/blob/main/JacobiKANLayer.py](https://github.com/SpaceLearner/JacobiKAN/blob/main/JacobiKANLayer.py)*
## [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/rmok.py#L260)
### [​](#rmok)RMoK


> CopyAsk AI RMoK (h, input_size, n_series:int, futr_exog_list=None,
>        hist_exog_list=None, stat_exog_list=None, taylor_order:int=3,
>        jacobi_degree:int=6, wavelet_function:str='mexican_hat',
>        dropout:float=0.1, revin_affine:bool=True, loss=MAE(),
>        valid_loss=None, max_steps:int=1000, learning_rate:float=0.001,
>        num_lr_decays:int=-1, early_stop_patience_steps:int=-1,
>        val_check_steps:int=100, batch_size:int=32,
>        valid_batch_size:Optional[int]=None, windows_batch_size=32,
>        inference_windows_batch_size=32, start_padding_enabled=False,
>        step_size:int=1, scaler_type:str='identity', random_seed:int=1,
>        drop_last_loader:bool=False, alias:Optional[str]=None,
>        optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>        lr_scheduler_kwargs=None, dataloader_kwargs=None, **trainer_kwargs)


*Reversible Mixture of KAN
**Parameters:**  
 `h`: int, Forecast horizon.   
 `input_size`: int,
autorregresive inputs size, y=[1,2,3,4] input_size=2 ->
y_[t-2:t]=[1,2].  
 `n_series`: int, number of time-series.  

`futr_exog_list`: str list, future exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`stat_exog_list`: str list, static exogenous columns.  

`taylor_order`: int, order of the Taylor polynomial.  

`jacobi_degree`: int, degree of the Jacobi polynomial.  

`wavelet_function`: str, wavelet function to use in the WaveKAN. Choose
from [“mexican_hat”, “morlet”, “dog”, “meyer”, “shannon”]  

`dropout`: float, dropout rate.  
 `revin_affine`: bool=False, bool to
use affine in RevIn.  
 `loss`: PyTorch module, instantiated train loss
class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=32, number of windows to
sample in each training batch, default uses all.  

`inference_windows_batch_size`: int=32, number of windows to sample in
each inference batch, -1 uses all.  
 `start_padding_enabled`:
bool=False, if True, the model will pad the time series with zeros at
the beginning, by input size.  
 `step_size`: int=1, step size between
each window of temporal data.  
 `scaler_type`: str=‘identity’, type of
scaler for temporal inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int,
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References**  
 - [Xiao Han, Xinfeng Zhang, Yiling Wu, Zhenduo Zhang,
Zhe Wu.”KAN4TSF: Are KAN and KAN-based models Effective for Time Series
Forecasting?“. arXiv.](https://arxiv.org/abs/2408.11306)  
*

### [​](#rmok-fit)RMoK.fit


> CopyAsk AI RMoK.fit (dataset, val_size=0, test_size=0, random_seed=None,
>            distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#rmok-predict)RMoK.predict


> CopyAsk AI RMoK.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#3-usage-example)3. Usage example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import RMoK
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
from neuralforecast.losses.pytorch import MSE

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = RMoK(h=12,
             input_size=24,
             n_series=2,
             taylor_order=3,
             jacobi_degree=6,
             wavelet_function='mexican_hat',
             dropout=0.1,
             revin_affine=True,
             loss=MSE(),
             valid_loss=MAE(),
             early_stop_patience_steps=3,
             batch_size=32)

fcst = NeuralForecast(models=[model], freq='ME')
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['RMoK'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```

---

## RNN - Nixtla
<a id="RNN-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.rnn.html

Elman proposed this classic recurrent neural network
([`RNN`](https://nixtlaverse.nixtla.io/neuralforecast/models.rnn.html#rnn))
in 1990, where each layer uses the following recurrent transformation:
htl=Activation([yt,xt(h),x(s)]Wih⊺+bih+ht−1lWhh⊺+bhh)\mathbf{h}^{l}_{t} = \mathrm{Activation}([\mathbf{y}_{t},\mathbf{x}^{(h)}_{t},\mathbf{x}^{(s)}] W^{\intercal}_{ih} + b_{ih}  +  \mathbf{h}^{l}_{t-1} W^{\intercal}_{hh} + b_{hh})htl​=Activation([yt​,xt(h)​,x(s)]Wih⊺​+bih​+ht−1l​Whh⊺​+bhh​)
where htl\mathbf{h}^{l}_{t}htl​, is the hidden state of RNN layer lll for
time ttt, yt\mathbf{y}_{t}yt​ is the input at time ttt and
ht−1\mathbf{h}_{t-1}ht−1​ is the hidden state of the previous layer at t−1t-1t−1,
x(s)\mathbf{x}^{(s)}x(s) are static exogenous inputs, xt(h)\mathbf{x}^{(h)}_{t}xt(h)​
historic exogenous, x[:t+H](f)\mathbf{x}^{(f)}_{[:t+H]}x[:t+H](f)​ are future exogenous
available at the time of the prediction. The available activations are
`tanh`, and `relu`. The predictions are obtained by transforming the
hidden states into contexts c[t+1:t+H]\mathbf{c}_{[t+1:t+H]}c[t+1:t+H]​, that are decoded
and adapted into y^[t+1:t+H],[q]\mathbf{\hat{y}}_{[t+1:t+H],[q]}y^​[t+1:t+H],[q]​ through MLPs.
**References**  
 -[Jeffrey L. Elman (1990). “Finding Structure in
Time”.](https://onlinelibrary.wiley.com/doiabs/10.1207/s15516709cog1402_1)  

-[Cho, K., van Merrienboer, B., Gülcehre, C., Bougares, F., Schwenk, H.,
& Bengio, Y. (2014). Learning phrase representations using RNN
encoder-decoder for statistical machine
translation.](http://arxiv.org/abs/1406.1078)  

 

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/rnn.py#L18)
### [​](#rnn)RNN


> CopyAsk AI RNN (h:int, input_size:int=-1, inference_input_size:Optional[int]=None,
>       h_train:int=1, encoder_n_layers:int=2, encoder_hidden_size:int=128,
>       encoder_activation:str='tanh', encoder_bias:bool=True,
>       encoder_dropout:float=0.0, context_size:Optional[int]=None,
>       decoder_hidden_size:int=128, decoder_layers:int=2,
>       futr_exog_list=None, hist_exog_list=None, stat_exog_list=None,
>       exclude_insample_y=False, recurrent=False, loss=MAE(),
>       valid_loss=None, max_steps:int=1000, learning_rate:float=0.001,
>       num_lr_decays:int=-1, early_stop_patience_steps:int=-1,
>       val_check_steps:int=100, batch_size=32,
>       valid_batch_size:Optional[int]=None, windows_batch_size=128,
>       inference_windows_batch_size=1024, start_padding_enabled=False,
>       step_size:int=1, scaler_type:str='robust', random_seed=1,
>       drop_last_loader=False, alias:Optional[str]=None, optimizer=None,
>       optimizer_kwargs=None, lr_scheduler=None, lr_scheduler_kwargs=None,
>       dataloader_kwargs=None, **trainer_kwargs)


*RNN
Multi Layer Elman RNN (RNN), with MLP decoder. The network has `tanh` or
`relu` non-linearities, it is trained using ADAM stochastic gradient
descent. The network accepts static, historic and future exogenous data.
**Parameters:**  
 `h`: int, forecast horizon.  
 `input_size`: int,
maximum sequence length for truncated train backpropagation. Default -1
uses 3 * horizon   
 `inference_input_size`: int, maximum sequence
length for truncated inference. Default None uses input_size
history.  
 `h_train`: int, maximum sequence length for truncated train
backpropagation. Default 1.  
 `encoder_n_layers`: int=2, number of
layers for the RNN.  
 `encoder_hidden_size`: int=200, units for the
RNN’s hidden state size.  
 `encoder_activation`: str=`tanh`, type of
RNN activation from `tanh` or `relu`.  
 `encoder_bias`: bool=True,
whether or not to use biases b_ih, b_hh within RNN units.  

`encoder_dropout`: float=0., dropout regularization applied to RNN
outputs.  
 `context_size`: deprecated.  
 `decoder_hidden_size`:
int=200, size of hidden layer for the MLP decoder.  
 `decoder_layers`:
int=2, number of layers for the MLP decoder.  
 `futr_exog_list`: str
list, future exogenous columns.  
 `hist_exog_list`: str list, historic
exogenous columns.  
 `stat_exog_list`: str list, static exogenous
columns.  
 `exclude_insample_y`: bool=False, whether to exclude the
target variable from the historic exogenous data.  
 `recurrent`:
bool=False, whether to produce forecasts recursively (True) or direct
(False).  
 `loss`: PyTorch module, instantiated train loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of
differentseries in each batch.  
 `valid_batch_size`: int=None, number
of different series in each validation and test batch.  

`windows_batch_size`: int=128, number of windows to sample in each
training batch, default uses all.  
 `inference_windows_batch_size`:
int=1024, number of windows to sample in each inference batch, -1 uses
all.  
 `start_padding_enabled`: bool=False, if True, the model will
pad the time series with zeros at the beginning, by input size.  

`step_size`: int=1, step size between each window of temporal
data.  
  

`scaler_type`: str=‘robust’, type of scaler for temporal inputs
normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
  

`dataloader_kwargs`: dict, optional, list of parameters passed into the
PyTorch Lightning dataloader by the `TimeSeriesDataLoader`.   

`**trainer_kwargs`: int, keyword trainer arguments inherited from
[PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  
*

### [​](#rnn-fit)RNN.fit


> CopyAsk AI RNN.fit (dataset, val_size=0, test_size=0, random_seed=None,
>           distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#rnn-predict)RNN.predict


> CopyAsk AI RNN.predict (dataset, test_size=None, step_size=1, random_seed=None,
>               quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#usage-example)Usage Example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import RNN
from neuralforecast.losses.pytorch import MQLoss
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]] # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

fcst = NeuralForecast(
    models=[RNN(h=12,
                input_size=24,
                inference_input_size=24,
                loss=MQLoss(level=[80, 90]),
                valid_loss=MQLoss(level=[80, 90]),
                scaler_type='standard',
                encoder_n_layers=2,
                encoder_hidden_size=128,
                decoder_hidden_size=128,
                decoder_layers=2,
                max_steps=200,
                futr_exog_list=['y_[lag12]'],
                stat_exog_list=['airline1'],
                )
    ],
    freq='ME'
)
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['RNN-median'], c='blue', label='median')
plt.fill_between(x=plot_df['ds'][-12:], 
                 y1=plot_df['RNN-lo-90'][-12:].values, 
                 y2=plot_df['RNN-hi-90'][-12:].values,
                 alpha=0.4, label='level 90')
plt.legend()
plt.grid()
plt.plot()
```

---

## SOFTS - Nixtla
<a id="SOFTS-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.softs.html

## [​](#1-auxiliary-functions)1. Auxiliary functions


### [​](#1-1-embedding)1.1 Embedding



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/softs.py#L17)
### [​](#dataembedding-inverted)DataEmbedding_inverted


> CopyAsk AI DataEmbedding_inverted (c_in, d_model, dropout=0.1)


*Data Embedding*
### [​](#1-2-stad-star-aggregate-dispatch)1.2 STAD (STar Aggregate Dispatch)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/softs.py#L39)
### [​](#stad)STAD


> CopyAsk AI STAD (d_series, d_core)


*STar Aggregate Dispatch Module*
## [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/softs.py#L83)
### [​](#softs)SOFTS


> CopyAsk AI SOFTS (h, input_size, n_series, futr_exog_list=None, hist_exog_list=None,
>         stat_exog_list=None, exclude_insample_y=False,
>         hidden_size:int=512, d_core:int=512, e_layers:int=2,
>         d_ff:int=2048, dropout:float=0.1, use_norm:bool=True, loss=MAE(),
>         valid_loss=None, max_steps:int=1000, learning_rate:float=0.001,
>         num_lr_decays:int=-1, early_stop_patience_steps:int=-1,
>         val_check_steps:int=100, batch_size:int=32,
>         valid_batch_size:Optional[int]=None, windows_batch_size=32,
>         inference_windows_batch_size=32, start_padding_enabled=False,
>         step_size:int=1, scaler_type:str='identity', random_seed:int=1,
>         drop_last_loader:bool=False, alias:Optional[str]=None,
>         optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>         lr_scheduler_kwargs=None, dataloader_kwargs=None,
>         **trainer_kwargs)


*SOFTS
**Parameters:**  
 `h`: int, Forecast horizon.   
 `input_size`: int,
autorregresive inputs size, y=[1,2,3,4] input_size=2 ->
y_[t-2:t]=[1,2].  
 `n_series`: int, number of time-series.  

`futr_exog_list`: str list, future exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`stat_exog_list`: str list, static exogenous columns.  

`exclude_insample_y`: bool=False, whether to exclude the target variable
from the input.  
  

`hidden_size`: int, dimension of the model.  
 `d_core`: int, dimension
of core in STAD.  
 `e_layers`: int, number of encoder layers.  

`d_ff`: int, dimension of fully-connected layer.  
 `dropout`: float,
dropout rate.  
 `use_norm`: bool, whether to normalize or not.  

`loss`: PyTorch module, instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=32, number of windows to
sample in each training batch, default uses all.  

`inference_windows_batch_size`: int=32, number of windows to sample in
each inference batch, -1 uses all.  
 `start_padding_enabled`:
bool=False, if True, the model will pad the time series with zeros at
the beginning, by input size.  
 `step_size`: int=1, step size between
each window of temporal data.  
 `scaler_type`: str=‘identity’, type of
scaler for temporal inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int,
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References**  
 [Lu Han, Xu-Yang Chen, Han-Jia Ye, De-Chuan Zhan.
“SOFTS: Efficient Multivariate Time Series Forecasting with Series-Core
Fusion”](https://arxiv.org/pdf/2404.14197)*

### [​](#softs-fit)SOFTS.fit


> CopyAsk AI SOFTS.fit (dataset, val_size=0, test_size=0, random_seed=None,
>             distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#softs-predict)SOFTS.predict


> CopyAsk AI SOFTS.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                 quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#3-usage-example)3. Usage example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import SOFTS
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
from neuralforecast.losses.pytorch import MASE
Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = SOFTS(h=12,
              input_size=24,
              n_series=2,
              hidden_size=256,
              d_core=256,
              e_layers=2,
              d_ff=64,
              dropout=0.1,
              use_norm=True,
              loss=MASE(seasonality=4),
              early_stop_patience_steps=3,
              batch_size=32)

fcst = NeuralForecast(models=[model], freq='ME')
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['SOFTS'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```

---

## StemGNN - Nixtla
<a id="StemGNN-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.stemgnn.html

The Spectral Temporal Graph Neural Network
([`StemGNN`](https://nixtlaverse.nixtla.io/neuralforecast/models.stemgnn.html#stemgnn))
is a Graph-based multivariate time-series forecasting model.
[`StemGNN`](https://nixtlaverse.nixtla.io/neuralforecast/models.stemgnn.html#stemgnn)
jointly learns temporal dependencies and inter-series correlations in
the spectral domain, by combining Graph Fourier Transform (GFT) and
Discrete Fourier Transform (DFT).
This method proved state-of-the-art performance on geo-temporal datasets
such as `Solar`, `METR-LA`, and `PEMS-BAY`, and
**References**  
 -[Defu Cao, Yujing Wang, Juanyong Duan, Ce Zhang, Xia
Zhu, Congrui Huang, Yunhai Tong, Bixiong Xu, Jing Bai, Jie Tong, Qi
Zhang (2020). “Spectral Temporal Graph Neural Network for Multivariate
Time-series
Forecasting”.](https://proceedings.neurips.cc/paper/2020/hash/cdf6581cb7aca4b7e19ef136c6e601a5-Abstract.html)
 

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tft.py#L46)
### [​](#glu)GLU


> CopyAsk AI GLU (input_channel, output_channel)


*GLU*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/stemgnn.py#L30)
### [​](#stockblocklayer)StockBlockLayer


> CopyAsk AI StockBlockLayer (time_step, unit, multi_layer, stack_cnt=0)


*StockBlockLayer*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/stemgnn.py#L140)
### [​](#stemgnn)StemGNN


> CopyAsk AI StemGNN (h, input_size, n_series, futr_exog_list=None,
>           hist_exog_list=None, stat_exog_list=None,
>           exclude_insample_y=False, n_stacks=2, multi_layer:int=5,
>           dropout_rate:float=0.5, leaky_rate:float=0.2, loss=MAE(),
>           valid_loss=None, max_steps:int=1000, learning_rate:float=0.001,
>           num_lr_decays:int=3, early_stop_patience_steps:int=-1,
>           val_check_steps:int=100, batch_size:int=32,
>           valid_batch_size:Optional[int]=None, windows_batch_size=32,
>           inference_windows_batch_size=32, start_padding_enabled=False,
>           step_size:int=1, scaler_type:str='robust', random_seed:int=1,
>           drop_last_loader=False, alias:Optional[str]=None,
>           optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>           lr_scheduler_kwargs=None, dataloader_kwargs=None,
>           **trainer_kwargs)


*StemGNN
The Spectral Temporal Graph Neural Network
([`StemGNN`](https://nixtlaverse.nixtla.io/neuralforecast/models.stemgnn.html#stemgnn))
is a Graph-based multivariate time-series forecasting model.
[`StemGNN`](https://nixtlaverse.nixtla.io/neuralforecast/models.stemgnn.html#stemgnn)
jointly learns temporal dependencies and inter-series correlations in
the spectral domain, by combining Graph Fourier Transform (GFT) and
Discrete Fourier Transform (DFT).
**Parameters:**  
 `h`: int, Forecast horizon.   
 `input_size`: int,
autorregresive inputs size, y=[1,2,3,4] input_size=2 ->
y_[t-2:t]=[1,2].  
 `n_series`: int, number of time-series.  

`futr_exog_list`: str list, future exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`stat_exog_list`: str list, static exogenous columns.  
 `n_stacks`:
int=2, number of stacks in the model.  
 `multi_layer`: int=5,
multiplier for FC hidden size on StemGNN blocks.  
 `dropout_rate`:
float=0.5, dropout rate.  
 `leaky_rate`: float=0.2, alpha for
LeakyReLU layer on Latent Correlation layer.  
 `loss`: PyTorch module,
instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int, number of windows in each
batch.  
 `valid_batch_size`: int=None, number of different series in
each validation and test batch, if None uses batch_size.  

`windows_batch_size`: int=32, number of windows to sample in each
training batch, default uses all.  
 `inference_windows_batch_size`:
int=32, number of windows to sample in each inference batch, -1 uses
all.  
 `start_padding_enabled`: bool=False, if True, the model will
pad the time series with zeros at the beginning, by input size.  

`step_size`: int=1, step size between each window of temporal data.  

`scaler_type`: str=‘robust’, type of scaler for temporal inputs
normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int,
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  
*

### [​](#stemgnn-fit)StemGNN.fit


> CopyAsk AI StemGNN.fit (dataset, val_size=0, test_size=0, random_seed=None,
>               distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#stemgnn-predict)StemGNN.predict


> CopyAsk AI StemGNN.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                   quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#usage-examples)Usage Examples


Train model and forecast future values with `predict` method.
CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import StemGNN
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
from neuralforecast.losses.pytorch import MAE

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = StemGNN(h=12,
                input_size=24,
                n_series=2,
                scaler_type='standard',
                max_steps=500,
                early_stop_patience_steps=-1,
                val_check_steps=10,
                learning_rate=1e-3,
                loss=MAE(),
                valid_loss=MAE(),
                batch_size=32
                )

fcst = NeuralForecast(models=[model], freq='ME')
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['StemGNN'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```


Using `cross_validation` to forecast multiple historic values.
CopyAsk AI```
fcst = NeuralForecast(models=[model], freq='M')
forecasts = fcst.cross_validation(df=AirPassengersPanel, static_df=AirPassengersStatic, n_windows=2, step_size=12)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.loc['Airline1']
Y_df = AirPassengersPanel[AirPassengersPanel['unique_id']=='Airline1']

plt.plot(Y_df['ds'], Y_df['y'], c='black', label='True')
plt.plot(Y_hat_df['ds'], Y_hat_df['StemGNN'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```

---

## TCN - Nixtla
<a id="TCN-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.tcn.html

For long time in deep learning, sequence modelling was synonymous with
recurrent networks, yet several papers have shown that simple
convolutional architectures can outperform canonical recurrent networks
like LSTMs by demonstrating longer effective memory. By skipping
temporal connections the causal convolution filters can be applied to
larger time spans while remaining computationally efficient.
The predictions are obtained by transforming the hidden states into
contexts c[t+1:t+H]\mathbf{c}_{[t+1:t+H]}c[t+1:t+H]​, that are decoded and adapted into
y^[t+1:t+H],[q]\mathbf{\hat{y}}_{[t+1:t+H],[q]}y^​[t+1:t+H],[q]​ through MLPs.
where ht\mathbf{h}_{t}ht​, is the hidden state for time ttt,
yt\mathbf{y}_{t}yt​ is the input at time ttt and ht−1\mathbf{h}_{t-1}ht−1​ is the
hidden state of the previous layer at t−1t-1t−1, x(s)\mathbf{x}^{(s)}x(s) are
static exogenous inputs, xt(h)\mathbf{x}^{(h)}_{t}xt(h)​ historic exogenous,
x[:t+H](f)\mathbf{x}^{(f)}_{[:t+H]}x[:t+H](f)​ are future exogenous available at the time
of the prediction.
**References**  
 -[van den Oord, A., Dieleman, S., Zen, H., Simonyan,
K., Vinyals, O., Graves, A., Kalchbrenner, N., Senior, A. W., &
Kavukcuoglu, K. (2016). Wavenet: A generative model for raw audio.
Computing Research Repository, abs/1609.03499. URL:
http://arxiv.org/abs/1609.03499.
arXiv:1609.03499.](https://arxiv.org/abs/1609.03499)  
 -[Shaojie Bai,
Zico Kolter, Vladlen Koltun. (2018). An Empirical Evaluation of Generic
Convolutional and Recurrent Networks for Sequence Modeling. Computing
Research Repository, abs/1803.01271. URL:
https://arxiv.org/abs/1803.01271.](https://arxiv.org/abs/1803.01271)  

 

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tcn.py#L17)
### [​](#tcn)TCN


> CopyAsk AI TCN (h:int, input_size:int=-1, inference_input_size:Optional[int]=None,
>       kernel_size:int=2, dilations:List[int]=[1, 2, 4, 8, 16],
>       encoder_hidden_size:int=128, encoder_activation:str='ReLU',
>       context_size:int=10, decoder_hidden_size:int=128,
>       decoder_layers:int=2, futr_exog_list=None, hist_exog_list=None,
>       stat_exog_list=None, loss=MAE(), valid_loss=None,
>       max_steps:int=1000, learning_rate:float=0.001, num_lr_decays:int=-1,
>       early_stop_patience_steps:int=-1, val_check_steps:int=100,
>       batch_size:int=32, valid_batch_size:Optional[int]=None,
>       windows_batch_size=128, inference_windows_batch_size=1024,
>       start_padding_enabled=False, step_size:int=1,
>       scaler_type:str='robust', random_seed:int=1, drop_last_loader=False,
>       alias:Optional[str]=None, optimizer=None, optimizer_kwargs=None,
>       lr_scheduler=None, lr_scheduler_kwargs=None, dataloader_kwargs=None,
>       **trainer_kwargs)


*TCN
Temporal Convolution Network (TCN), with MLP decoder. The historical
encoder uses dilated skip connections to obtain efficient long memory,
while the rest of the architecture allows for future exogenous
alignment.
**Parameters:**  
 `h`: int, forecast horizon.  
 `input_size`: int,
maximum sequence length for truncated train backpropagation. Default -1
uses 3 * horizon   
 `inference_input_size`: int, maximum sequence
length for truncated inference. Default None uses input_size
history.  
 `kernel_size`: int, size of the convolving kernel.  

`dilations`: int list, ontrols the temporal spacing between the kernel
points; also known as the à trous algorithm.  
 `encoder_hidden_size`:
int=200, units for the TCN’s hidden state size.  

`encoder_activation`: str=`tanh`, type of TCN activation from `tanh` or
`relu`.  
 `context_size`: int=10, size of context vector for each
timestamp on the forecasting window.  
 `decoder_hidden_size`: int=200,
size of hidden layer for the MLP decoder.  
 `decoder_layers`: int=2,
number of layers for the MLP decoder.  
 `futr_exog_list`: str list,
future exogenous columns.  
 `hist_exog_list`: str list, historic
exogenous columns.  
 `stat_exog_list`: str list, static exogenous
columns.  
 `loss`: PyTorch module, instantiated train loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of
differentseries in each batch.  
 `batch_size`: int=32, number of
differentseries in each batch.  
 `valid_batch_size`: int=None, number
of different series in each validation and test batch.  

`windows_batch_size`: int=128, number of windows to sample in each
training batch, default uses all.  
 `inference_windows_batch_size`:
int=1024, number of windows to sample in each inference batch, -1 uses
all.  
 `start_padding_enabled`: bool=False, if True, the model will
pad the time series with zeros at the beginning, by input size.  

`step_size`: int=1, step size between each window of temporal
data.  
  

`scaler_type`: str=‘robust’, type of scaler for temporal inputs
normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
  

`dataloader_kwargs`: dict, optional, list of parameters passed into the
PyTorch Lightning dataloader by the `TimeSeriesDataLoader`.   

`**trainer_kwargs`: int, keyword trainer arguments inherited from
[PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  
*

### [​](#tcn-fit)TCN.fit


> CopyAsk AI TCN.fit (dataset, val_size=0, test_size=0, random_seed=None,
>           distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#tcn-predict)TCN.predict


> CopyAsk AI TCN.predict (dataset, test_size=None, step_size=1, random_seed=None,
>               quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#usage-example)Usage Example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import TCN
from neuralforecast.losses.pytorch import  DistributionLoss
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]] # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

fcst = NeuralForecast(
    models=[TCN(h=12,
                input_size=-1,
                loss=DistributionLoss(distribution='Normal', level=[80, 90]),
                learning_rate=5e-4,
                kernel_size=2,
                dilations=[1,2,4,8,16],
                encoder_hidden_size=128,
                context_size=10,
                decoder_hidden_size=128,
                decoder_layers=2,
                max_steps=500,
                scaler_type='robust',
                futr_exog_list=['y_[lag12]'],
                hist_exog_list=None,
                stat_exog_list=['airline1'],
                )
    ],
    freq='ME'
)
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot quantile predictions
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['TCN-median'], c='blue', label='median')
plt.fill_between(x=plot_df['ds'][-12:], 
                 y1=plot_df['TCN-lo-90'][-12:].values,
                 y2=plot_df['TCN-hi-90'][-12:].values,
                 alpha=0.4, label='level 90')
plt.legend()
plt.grid()
plt.plot()
```

---

## TFT - Nixtla
<a id="TFT-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.tft.html

In summary Temporal Fusion Transformer (TFT) combines gating layers, an
LSTM recurrent encoder, with multi-head attention layers for a
multi-step forecasting strategy decoder.  
TFT’s inputs are static
exogenous x(s)\mathbf{x}^{(s)}x(s), historic exogenous
x[:t](h)\mathbf{x}^{(h)}_{[:t]}x[:t](h)​, exogenous available at the time of the
prediction x[:t+H](f)\mathbf{x}^{(f)}_{[:t+H]}x[:t+H](f)​ and autorregresive features
y[:t]\mathbf{y}_{[:t]}y[:t]​, each of these inputs is further decomposed into
categorical and continuous. The network uses a multi-quantile regression
to model the following conditional
probability:P(y[t+1:t+H]∣  y[:t],  x[:t](h),  x[:t+H](f),  x(s))\mathbb{P}(\mathbf{y}_{[t+1:t+H]}|\;\mathbf{y}_{[:t]},\; \mathbf{x}^{(h)}_{[:t]},\; \mathbf{x}^{(f)}_{[:t+H]},\; \mathbf{x}^{(s)})P(y[t+1:t+H]​∣y[:t]​,x[:t](h)​,x[:t+H](f)​,x(s))
**References**  
 - [Jan Golda, Krzysztof Kudrynski. “NVIDIA, Deep
Learning Forecasting
Examples”](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/Forecasting/TFT)  
 -
[Bryan Lim, Sercan O. Arik, Nicolas Loeff, Tomas Pfister, “Temporal
Fusion Transformers for interpretable multi-horizon time series
forecasting”](https://www.sciencedirect.com/science/article/pii/S0169207021000637)  

 
## [​](#1-auxiliary-functions)1. Auxiliary Functions


### [​](#1-1-gating-mechanisms)1.1 Gating Mechanisms


The Gated Residual Network (GRN) provides adaptive depth and network
complexity capable of accommodating different size datasets. As residual
connections allow for the network to skip the non-linear transformation
of input a\mathbf{a}a and context c\mathbf{c}c.
The Gated Linear Unit (GLU) provides the flexibility of supressing
unnecesary parts of the GRN. Consider GRN’s output γ\gammaγ then GLU
transformation is defined by:
GLU(γ)=σ(W4γ+b4)⊙(W5γ+b5)\mathrm{GLU}(\gamma) = \sigma(\mathbf{W}_{4}\gamma +b_{4}) \odot (\mathbf{W}_{5}\gamma +b_{5})GLU(γ)=σ(W4​γ+b4​)⊙(W5​γ+b5​)
 
### [​](#1-2-variable-selection-networks)1.2 Variable Selection Networks


TFT includes automated variable selection capabilities, through its
variable selection network (VSN) components. The VSN takes the original
input
{x(s),x[:t](h),x[:t](f)}\{\mathbf{x}^{(s)}, \mathbf{x}^{(h)}_{[:t]}, \mathbf{x}^{(f)}_{[:t]}\}{x(s),x[:t](h)​,x[:t](f)​}
and transforms it through embeddings or linear transformations into a
high dimensional space
{E(s),E[:t](h),E[:t+H](f)}\{\mathbf{E}^{(s)}, \mathbf{E}^{(h)}_{[:t]}, \mathbf{E}^{(f)}_{[:t+H]}\}{E(s),E[:t](h)​,E[:t+H](f)​}.
For the observed historic data, the embedding matrix
Et(h)\mathbf{E}^{(h)}_{t}Et(h)​ at time ttt is a concatenation of jjj variable
et,j(h)e^{(h)}_{t,j}et,j(h)​ embeddings:
The variable selection weights are given by:
st(h)=SoftMax(GRN(Et(h),E(s)))s^{(h)}_{t}=\mathrm{SoftMax}(\mathrm{GRN}(\mathbf{E}^{(h)}_{t},\mathbf{E}^{(s)}))st(h)​=SoftMax(GRN(Et(h)​,E(s)))
The VSN processed features are then:
E~t(h)=∑jsj(h)e~t,j(h)\tilde{\mathbf{E}}^{(h)}_{t}= \sum_{j} s^{(h)}_{j} \tilde{e}^{(h)}_{t,j}E~t(h)​=∑j​sj(h)​e~t,j(h)​
 
### [​](#1-3-multi-head-attention)1.3. Multi-Head Attention


To avoid information bottlenecks from the classic Seq2Seq architecture,
TFT incorporates a decoder-encoder attention mechanism inherited
transformer architectures ([Li et. al
2019](https://arxiv.org/abs/1907.00235), [Vaswani et. al
2017](https://arxiv.org/abs/1706.03762)). It transform the the outputs
of the LSTM encoded temporal features, and helps the decoder better
capture long-term relationships.
The original multihead attention for each component HmH_{m}Hm​ and its
query, key, and value representations are denoted by
Qm,Km,VmQ_{m}, K_{m}, V_{m}Qm​,Km​,Vm​, its transformation is given by:
TFT modifies the original multihead attention to improve its
interpretability. To do it it uses shared values V~\tilde{V}V~ across
heads and employs additive aggregation,
InterpretableMultiHead(Q,K,V)=H~WM\mathrm{InterpretableMultiHead}(Q,K,V) = \tilde{H} W_{M}InterpretableMultiHead(Q,K,V)=H~WM​. The
mechanism has a great resemblence to a single attention layer, but it
allows for MMM multiple attention weights, and can be therefore be
interpreted as the average ensemble of MMM single attention layers.
## [​](#2-tft-architecture)2. TFT Architecture


The first TFT’s step is embed the original input
{x(s),x(h),x(f)}\{\mathbf{x}^{(s)}, \mathbf{x}^{(h)}, \mathbf{x}^{(f)}\}{x(s),x(h),x(f)} into a high
dimensional space
{E(s),E(h),E(f)}\{\mathbf{E}^{(s)}, \mathbf{E}^{(h)}, \mathbf{E}^{(f)}\}{E(s),E(h),E(f)}, after which
each embedding is gated by a variable selection network (VSN). The
static embedding E(s)\mathbf{E}^{(s)}E(s) is used as context for variable
selection and as initial condition to the LSTM. Finally the encoded
variables are fed into the multi-head attention decoder.
### [​](#2-1-static-covariate-encoder)2.1 Static Covariate Encoder


The static embedding E(s)\mathbf{E}^{(s)}E(s) is transformed by the
StaticCovariateEncoder into contexts cs,ce,ch,ccc_{s}, c_{e}, c_{h}, c_{c}cs​,ce​,ch​,cc​. Where
csc_{s}cs​ are temporal variable selection contexts, cec_{e}ce​ are
TemporalFusionDecoder enriching contexts, and ch,ccc_{h}, c_{c}ch​,cc​ are LSTM’s
hidden/contexts for the TemporalCovariateEncoder.
### [​](#2-2-temporal-covariate-encoder)2.2 Temporal Covariate Encoder


TemporalCovariateEncoder encodes the embeddings
E(h),E(f)\mathbf{E}^{(h)}, \mathbf{E}^{(f)}E(h),E(f) and contexts (ch,cc)(c_{h}, c_{c})(ch​,cc​) with
an LSTM.
An analogous process is repeated for the future data, with the main
difference that E(f)\mathbf{E}^{(f)}E(f) contains the future available
information.
### [​](#2-3-temporal-fusion-decoder)2.3 Temporal Fusion Decoder


The TemporalFusionDecoder enriches the LSTM’s outputs with cec_{e}ce​ and
then uses an attention layer, and multi-step adapter.

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tft.py#L513)
### [​](#tft)TFT


> CopyAsk AI TFT (h, input_size, tgt_size:int=1, stat_exog_list=None,
>       hist_exog_list=None, futr_exog_list=None, hidden_size:int=128,
>       n_head:int=4, attn_dropout:float=0.0, grn_activation:str='ELU',
>       n_rnn_layers:int=1, rnn_type:str='lstm',
>       one_rnn_initial_state:bool=False, dropout:float=0.1, loss=MAE(),
>       valid_loss=None, max_steps:int=1000, learning_rate:float=0.001,
>       num_lr_decays:int=-1, early_stop_patience_steps:int=-1,
>       val_check_steps:int=100, batch_size:int=32,
>       valid_batch_size:Optional[int]=None, windows_batch_size:int=1024,
>       inference_windows_batch_size:int=1024, start_padding_enabled=False,
>       step_size:int=1, scaler_type:str='robust', random_seed:int=1,
>       drop_last_loader=False, alias:Optional[str]=None, optimizer=None,
>       optimizer_kwargs=None, lr_scheduler=None, lr_scheduler_kwargs=None,
>       dataloader_kwargs=None, **trainer_kwargs)


*TFT
The Temporal Fusion Transformer architecture (TFT) is an
Sequence-to-Sequence model that combines static, historic and future
available data to predict an univariate target. The method combines
gating layers, an LSTM recurrent encoder, with and interpretable
multi-head attention layer and a multi-step forecasting strategy
decoder.
**Parameters:**  
 `h`: int, Forecast horizon.   
 `input_size`: int,
autorregresive inputs size, y=[1,2,3,4] input_size=2 ->
y_[t-2:t]=[1,2].  
 `tgt_size`: int=1, target size.  

`stat_exog_list`: str list, static continuous columns.  

`hist_exog_list`: str list, historic continuous columns.  

`futr_exog_list`: str list, future continuous columns.  

`hidden_size`: int, units of embeddings and encoders.  
 `n_head`:
int=4, number of attention heads in temporal fusion decoder.  

`attn_dropout`: float (0, 1), dropout of fusion decoder’s attention
layer.  
 `grn_activation`: str, activation for the GRN module from
[‘ReLU’, ‘Softplus’, ‘Tanh’, ‘SELU’, ‘LeakyReLU’, ‘Sigmoid’, ‘ELU’,
‘GLU’].  
 `n_rnn_layers`: int=1, number of RNN layers.  

`rnn_type`: str=“lstm”, recurrent neural network (RNN) layer type from
[“lstm”,“gru”].  
 `one_rnn_initial_state`:str=False, Initialize all
rnn layers with the same initial states computed from static
covariates.  
 `dropout`: float (0, 1), dropout of inputs VSNs.  

`loss`: PyTorch module, instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int, number of different series
in each batch.  
 `valid_batch_size`: int=None, number of different
series in each validation and test batch.  
 `windows_batch_size`:
int=None, windows sampled from rolled data, default uses all.  

`inference_windows_batch_size`: int=-1, number of windows to sample in
each inference batch, -1 uses all.  
 `start_padding_enabled`:
bool=False, if True, the model will pad the time series with zeros at
the beginning, by input size.  
 `step_size`: int=1, step size between
each window of temporal data.  
 `scaler_type`: str=‘robust’, type of
scaler for temporal inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int, random seed initialization for replicability.  

`drop_last_loader`: bool=False, if True `TimeSeriesDataLoader` drops
last non-full batch.  
 `alias`: str, optional, Custom name of the
model.  
 `optimizer`: Subclass of ‘torch.optim.Optimizer’, optional,
user specified optimizer instead of the default choice (Adam).  

`optimizer_kwargs`: dict, optional, list of parameters used by the user
specified `optimizer`.  
 `lr_scheduler`: Subclass of
‘torch.optim.lr_scheduler.LRScheduler’, optional, user specified
lr_scheduler instead of the default choice (StepLR).  

`lr_scheduler_kwargs`: dict, optional, list of parameters used by the
user specified `lr_scheduler`.  
 `dataloader_kwargs`: dict, optional,
list of parameters passed into the PyTorch Lightning dataloader by the
`TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int, keyword trainer
arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References:**  
 - [Bryan Lim, Sercan O. Arik, Nicolas Loeff, Tomas
Pfister, “Temporal Fusion Transformers for interpretable multi-horizon
time series
forecasting”](https://www.sciencedirect.com/science/article/pii/S0169207021000637)*
## [​](#3-tft-methods)3. TFT methods



### [​](#tft-fit)TFT.fit


> CopyAsk AI TFT.fit (dataset, val_size=0, test_size=0, random_seed=None,
>           distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#tft-predict)TFT.predict


> CopyAsk AI TFT.predict (dataset, test_size=None, step_size=1, random_seed=None,
>               quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tft.py#L785)
### [​](#tft-feature-importances%2C)TFT.feature_importances,


> CopyAsk AI TFT.feature_importances, ()


*Compute the feature importances for historical, future, and static
features.
Returns: dict: A dictionary containing the feature importances for each
feature type. The keys are ‘hist_vsn’, ‘future_vsn’, and ‘static_vsn’,
and the values are pandas DataFrames with the corresponding feature
importances.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tft.py#L844)
### [​](#tft-attention-weights)TFT.attention_weights


> CopyAsk AI TFT.attention_weights ()


*Batch average attention weights
Returns: np.ndarray: A 1D array containing the attention weights for
each time step.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tft.py#L844)
### [​](#tft-attention-weights-2)TFT.attention_weights


> CopyAsk AI TFT.attention_weights ()


*Batch average attention weights
Returns: np.ndarray: A 1D array containing the attention weights for
each time step.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tft.py#L862)
### [​](#tft-feature-importance-correlations)TFT.feature_importance_correlations


> CopyAsk AI TFT.feature_importance_correlations ()


*Compute the correlation between the past and future feature
importances and the mean attention weights.
Returns: pd.DataFrame: A DataFrame containing the correlation
coefficients between the past feature importances and the mean attention
weights.*
## [​](#usage-example)Usage Example


CopyAsk AI```
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from neuralforecast import NeuralForecast

# from neuralforecast.models import TFT
from neuralforecast.losses.pytorch import DistributionLoss
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic

AirPassengersPanel["month"] = AirPassengersPanel.ds.dt.month
Y_train_df = AirPassengersPanel[
    AirPassengersPanel.ds < AirPassengersPanel["ds"].values[-12]
]  # 132 train
Y_test_df = AirPassengersPanel[
    AirPassengersPanel.ds >= AirPassengersPanel["ds"].values[-12]
].reset_index(drop=True)  # 12 test

nf = NeuralForecast(
    models=[
        TFT(
            h=12,
            input_size=48,
            hidden_size=20,
            grn_activation="ELU",
            rnn_type="lstm",
            n_rnn_layers=1,
            one_rnn_initial_state=False,
            loss=DistributionLoss(distribution="StudentT", level=[80, 90]),
            learning_rate=0.005,
            stat_exog_list=["airline1"],
            futr_exog_list=["y_[lag12]", "month"],
            hist_exog_list=["trend"],
            max_steps=300,
            val_check_steps=10,
            early_stop_patience_steps=10,
            scaler_type="robust",
            windows_batch_size=None,
            enable_progress_bar=True,
        ),
    ],
    freq="ME",
)
nf.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
Y_hat_df = nf.predict(futr_df=Y_test_df)

# Plot quantile predictions
Y_hat_df = Y_hat_df.reset_index(drop=False).drop(columns=["unique_id", "ds"])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id == "Airline1"].drop("unique_id", axis=1)
plt.plot(plot_df["ds"], plot_df["y"], c="black", label="True")
plt.plot(plot_df["ds"], plot_df["TFT"], c="purple", label="mean")
plt.plot(plot_df["ds"], plot_df["TFT-median"], c="blue", label="median")
plt.fill_between(
    x=plot_df["ds"][-12:],
    y1=plot_df["TFT-lo-90"][-12:].values,
    y2=plot_df["TFT-hi-90"][-12:].values,
    alpha=0.4,
    label="level 90",
)
plt.legend()
plt.grid()
plt.plot()
```


# [​](#interpretability)Interpretability


## [​](#1-attention-weights)1. Attention Weights


CopyAsk AI```
attention = nf.models[0].attention_weights()
```


CopyAsk AI```
def plot_attention(
    self, plot: str = "time", output: str = "plot", width: int = 800, height: int = 400
):
    """
    Plot the attention weights.

    Args:
        plot (str, optional): The type of plot to generate. Can be one of the following:
            - 'time': Display the mean attention weights over time.
            - 'all': Display the attention weights for each horizon.
            - 'heatmap': Display the attention weights as a heatmap.
            - An integer in the range [1, model.h) to display the attention weights for a specific horizon.
        output (str, optional): The type of output to generate. Can be one of the following:
            - 'plot': Display the plot directly.
            - 'figure': Return the plot as a figure object.
        width (int, optional): Width of the plot in pixels. Default is 800.
        height (int, optional): Height of the plot in pixels. Default is 400.

    Returns:
        matplotlib.figure.Figure: If `output` is 'figure', the function returns the plot as a figure object.
    """

    attention = (
        self.mean_on_batch(self.interpretability_params["attn_wts"])
        .mean(dim=0)
        .cpu()
        .numpy()
    )

    fig, ax = plt.subplots(figsize=(width / 100, height / 100))

    if plot == "time":
        attention = attention[self.input_size :, :].mean(axis=0)
        ax.plot(np.arange(-self.input_size, self.h), attention)
        ax.axvline(
            x=0, color="black", linewidth=3, linestyle="--", label="prediction start"
        )
        ax.set_title("Mean Attention")
        ax.set_xlabel("time")
        ax.set_ylabel("Attention")
        ax.legend()

    elif plot == "all":
        for i in range(self.input_size, attention.shape[0]):
            ax.plot(
                np.arange(-self.input_size, self.h),
                attention[i, :],
                label=f"horizon {i-self.input_size+1}",
            )
        ax.axvline(
            x=0, color="black", linewidth=3, linestyle="--", label="prediction start"
        )
        ax.set_title("Attention per horizon")
        ax.set_xlabel("time")
        ax.set_ylabel("Attention")
        ax.legend()

    elif plot == "heatmap":
        cax = ax.imshow(
            attention,
            aspect="auto",
            cmap="viridis",
            extent=[-self.input_size, self.h, -self.input_size, self.h],
        )
        fig.colorbar(cax)
        ax.set_title("Attention Heatmap")
        ax.set_xlabel("Attention (current time step)")
        ax.set_ylabel("Attention (previous time step)")

    elif isinstance(plot, int) and (plot in np.arange(1, self.h + 1)):
        i = self.input_size + plot - 1
        ax.plot(
            np.arange(-self.input_size, self.h),
            attention[i, :],
            label=f"horizon {plot}",
        )
        ax.axvline(
            x=0, color="black", linewidth=3, linestyle="--", label="prediction start"
        )
        ax.set_title(f"Attention weight for horizon {plot}")
        ax.set_xlabel("time")
        ax.set_ylabel("Attention")
        ax.legend()

    else:
        raise ValueError(
            'plot has to be in ["time","all","heatmap"] or integer in range(1,model.h)'
        )

    plt.tight_layout()

    if output == "plot":
        plt.show()
    elif output == "figure":
        return fig
    else:
        raise ValueError(f"Invalid output: {output}. Expected 'plot' or 'figure'.")
```


#### [​](#1-1-mean-attention)1.1 Mean attention


CopyAsk AI```
plot_attention(nf.models[0], plot="time")
```


#### [​](#1-2-attention-of-all-future-time-steps)1.2 Attention of all future time steps


CopyAsk AI```
plot_attention(nf.models[0], plot="all")
```


#### [​](#1-3-attention-of-a-specific-future-time-step)1.3 Attention of a specific future time step


CopyAsk AI```
plot_attention(nf.models[0], plot=8)
```


## [​](#2-feature-importance)2. Feature Importance


### [​](#2-1-global-feature-importance)2.1 Global feature importance


CopyAsk AI```
feature_importances = nf.models[0].feature_importances()
feature_importances.keys()
```


#### [​](#static-variable-importances)Static variable importances


CopyAsk AI```
feature_importances["Static covariates"].sort_values(by="importance").plot(kind="barh")
```


#### [​](#past-variable-importances)Past variable importances


CopyAsk AI```
feature_importances["Past variable importance over time"].mean().sort_values().plot(
    kind="barh"
)
```


#### [​](#future-variable-importances)Future variable importances


CopyAsk AI```
feature_importances["Future variable importance over time"].mean().sort_values().plot(
    kind="barh"
)
```


### [​](#2-2-variable-importances-over-time)2.2 Variable importances over time


#### [​](#future-variable-importance-over-time)Future variable importance over time


Importance of each future covariate at each future time step
CopyAsk AI```
df = feature_importances["Future variable importance over time"]


fig, ax = plt.subplots(figsize=(20, 10))
bottom = np.zeros(len(df.index))
for col in df.columns:
    p = ax.bar(np.arange(-len(df), 0), df[col].values, 0.6, label=col, bottom=bottom)
    bottom += df[col]
ax.set_title("Future variable importance over time ponderated by attention")
ax.set_ylabel("Importance")
ax.set_xlabel("Time")
ax.grid(True)
ax.legend()
plt.show()
```


2.3
#### [​](#past-variable-importance-over-time)Past variable importance over time


CopyAsk AI```
df = feature_importances["Past variable importance over time"]

fig, ax = plt.subplots(figsize=(20, 10))
bottom = np.zeros(len(df.index))

for col in df.columns:
    p = ax.bar(np.arange(-len(df), 0), df[col].values, 0.6, label=col, bottom=bottom)
    bottom += df[col]
ax.set_title("Past variable importance over time")
ax.set_ylabel("Importance")
ax.set_xlabel("Time")
ax.legend()
ax.grid(True)

plt.show()
```


#### [​](#past-variable-importance-over-time-ponderated-by-attention)Past variable importance over time ponderated by attention


Decomposition of the importance of each time step based on importance of
each variable at that time step
CopyAsk AI```
df = feature_importances["Past variable importance over time"]
mean_attention = (
    nf.models[0]
    .attention_weights()[nf.models[0].input_size :, :]
    .mean(axis=0)[: nf.models[0].input_size]
)
df = df.multiply(mean_attention, axis=0)

fig, ax = plt.subplots(figsize=(20, 10))
bottom = np.zeros(len(df.index))

for col in df.columns:
    p = ax.bar(np.arange(-len(df), 0), df[col].values, 0.6, label=col, bottom=bottom)
    bottom += df[col]
ax.set_title("Past variable importance over time ponderated by attention")
ax.set_ylabel("Importance")
ax.set_xlabel("Time")
ax.legend()
ax.grid(True)
plt.plot(
    np.arange(-len(df), 0),
    mean_attention,
    color="black",
    marker="o",
    linestyle="-",
    linewidth=2,
    label="mean_attention",
)
plt.legend()
plt.show()
```


### [​](#3-variable-importance-correlations-over-time)3. Variable importance correlations over time


Variables which gain and lose importance at same moments
CopyAsk AI```
nf.models[0].feature_importance_correlations()
```

---

## TiDE - Nixtla
<a id="TiDE-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.tide.html

Time-series Dense Encoder (`TiDE`) is a MLP-based univariate time-series forecasting model. `TiDE` uses Multi-layer Perceptrons (MLPs) in an encoder-decoder model for long-term time-series forecasting. In addition, this model can handle exogenous inputs.

## [​](#1-auxiliary-functions)1. Auxiliary Functions


## [​](#1-1-mlp-residual)1.1 MLP residual


An MLP block with a residual connection.

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tide.py#L17)
### [​](#mlpresidual)MLPResidual


> CopyAsk AI MLPResidual (input_dim, hidden_size, output_dim, dropout, layernorm)


*MLPResidual*
## [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tide.py#L51)
### [​](#tide)TiDE


> CopyAsk AI TiDE (h, input_size, hidden_size=512, decoder_output_dim=32,
>        temporal_decoder_dim=128, dropout=0.3, layernorm=True,
>        num_encoder_layers=1, num_decoder_layers=1, temporal_width=4,
>        futr_exog_list=None, hist_exog_list=None, stat_exog_list=None,
>        exclude_insample_y=False, loss=MAE(), valid_loss=None,
>        max_steps:int=1000, learning_rate:float=0.001,
>        num_lr_decays:int=-1, early_stop_patience_steps:int=-1,
>        val_check_steps:int=100, batch_size:int=32,
>        valid_batch_size:Optional[int]=None, windows_batch_size=1024,
>        inference_windows_batch_size=1024, start_padding_enabled=False,
>        step_size:int=1, scaler_type:str='identity', random_seed:int=1,
>        drop_last_loader:bool=False, alias:Optional[str]=None,
>        optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>        lr_scheduler_kwargs=None, dataloader_kwargs=None, **trainer_kwargs)


*TiDE
Time-series Dense Encoder
([`TiDE`](https://nixtlaverse.nixtla.io/neuralforecast/models.tide.html#tide))
is a MLP-based univariate time-series forecasting model.
[`TiDE`](https://nixtlaverse.nixtla.io/neuralforecast/models.tide.html#tide)
uses Multi-layer Perceptrons (MLPs) in an encoder-decoder model for
long-term time-series forecasting.
**Parameters:**  
 `h`: int, forecast horizon.  
 `input_size`: int,
considered autorregresive inputs (lags), y=[1,2,3,4] input_size=2 ->
lags=[1,2].  
 `hidden_size`: int=1024, number of units for the dense
MLPs.  
 `decoder_output_dim`: int=32, number of units for the output
of the decoder.  
 `temporal_decoder_dim`: int=128, number of units for
the hidden sizeof the temporal decoder.  
 `dropout`: float=0.0,
dropout rate between (0, 1) .  
 `layernorm`: bool=True, if True uses
Layer Normalization on the MLP residual block outputs.  

`num_encoder_layers`: int=1, number of encoder layers.  

`num_decoder_layers`: int=1, number of decoder layers.  

`temporal_width`: int=4, lower temporal projected dimension.  

`futr_exog_list`: str list, future exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`stat_exog_list`: str list, static exogenous columns.  
  

`exclude_insample_y`: bool=False, whether to exclude the target variable
from the historic exogenous data.  
 `loss`: PyTorch module,
instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch.  

`windows_batch_size`: int=1024, number of windows to sample in each
training batch, default uses all.  
 `inference_windows_batch_size`:
int=1024, number of windows to sample in each inference batch, -1 uses
all.  
 `start_padding_enabled`: bool=False, if True, the model will
pad the time series with zeros at the beginning, by input size.  

`step_size`: int=1, step size between each window of temporal data.  

`scaler_type`: str=‘identity’, type of scaler for temporal inputs
normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int,
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References:**  
 - [Das, Abhimanyu, Weihao Kong, Andrew Leach, Shaan
Mathur, Rajat Sen, and Rose Yu (2024). “Long-term Forecasting with TiDE:
Time-series Dense Encoder.”](http://arxiv.org/abs/2304.08424)*

### [​](#tide-fit)TiDE.fit


> CopyAsk AI TiDE.fit (dataset, val_size=0, test_size=0, random_seed=None,
>            distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#tide-predict)TiDE.predict


> CopyAsk AI TiDE.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#3-usage-examples)3. Usage Examples


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import TiDE
from neuralforecast.losses.pytorch import GMM
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]] # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

fcst = NeuralForecast(
    models=[
            TiDE(h=12,
                input_size=24,
                loss=GMM(n_components=7, return_params=True, level=[80,90], weighted=True),
                max_steps=100,
                scaler_type='standard',
                futr_exog_list=['y_[lag12]'],
                hist_exog_list=None,
                stat_exog_list=['airline1'],
                ),     
    ],
    freq='ME'
)
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot quantile predictions
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['TiDE-median'], c='blue', label='median')
plt.fill_between(x=plot_df['ds'][-12:], 
                 y1=plot_df['TiDE-lo-90'][-12:].values,
                 y2=plot_df['TiDE-hi-90'][-12:].values,
                 alpha=0.4, label='level 90')
plt.legend()
plt.grid()
```

---

## Time-LLM - Nixtla
<a id="Time-LLM-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.timellm.html

Time-LLM is a reprogramming framework to repurpose LLMs for general time
series forecasting with the backbone language models kept intact. In
other words, it transforms a forecasting task into a “language task”
that can be tackled by an off-the-shelf LLM.
**References**  
 - [Ming Jin, Shiyu Wang, Lintao Ma, Zhixuan Chu,
James Y. Zhang, Xiaoming Shi, Pin-Yu Chen, Yuxuan Liang, Yuan-Fang Li,
Shirui Pan, Qingsong Wen. “Time-LLM: Time Series Forecasting by
Reprogramming Large Language
Models”](https://arxiv.org/abs/2310.01728)  

 
## [​](#1-auxiliary-functions)1. Auxiliary Functions



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timellm.py#L121)
### [​](#reprogramminglayer)ReprogrammingLayer


> CopyAsk AI ReprogrammingLayer (d_model, n_heads, d_keys=None, d_llm=None,
>                      attention_dropout=0.1)


*ReprogrammingLayer*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timexer.py#L22)
### [​](#flattenhead)FlattenHead


> CopyAsk AI FlattenHead (n_vars, nf, target_window, head_dropout=0)


*FlattenHead*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timellm.py#L70)
### [​](#patchembedding)PatchEmbedding


> CopyAsk AI PatchEmbedding (d_model, patch_len, stride, dropout)


*PatchEmbedding*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timellm.py#L43)
### [​](#tokenembedding)TokenEmbedding


> CopyAsk AI TokenEmbedding (c_in, d_model)


*TokenEmbedding*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timellm.py#L28)
### [​](#replicationpad1d)ReplicationPad1d


> CopyAsk AI ReplicationPad1d (padding)


*ReplicationPad1d*
## [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timellm.py#L168)
### [​](#timellm)TimeLLM


> CopyAsk AI TimeLLM (h, input_size, patch_len:int=16, stride:int=8, d_ff:int=128,
>           top_k:int=5, d_llm:int=768, d_model:int=32, n_heads:int=8,
>           enc_in:int=7, dec_in:int=7, llm=None, llm_config=None,
>           llm_tokenizer=None, llm_num_hidden_layers=32,
>           llm_output_attention:bool=True,
>           llm_output_hidden_states:bool=True,
>           prompt_prefix:Optional[str]=None, dropout:float=0.1,
>           stat_exog_list=None, hist_exog_list=None, futr_exog_list=None,
>           loss=MAE(), valid_loss=None, learning_rate:float=0.0001,
>           max_steps:int=5, val_check_steps:int=100, batch_size:int=32,
>           valid_batch_size:Optional[int]=None,
>           windows_batch_size:int=1024,
>           inference_windows_batch_size:int=1024,
>           start_padding_enabled:bool=False, step_size:int=1,
>           num_lr_decays:int=0, early_stop_patience_steps:int=-1,
>           scaler_type:str='identity', random_seed:int=1,
>           drop_last_loader:bool=False, alias:Optional[str]=None,
>           optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>           lr_scheduler_kwargs=None, dataloader_kwargs=None,
>           **trainer_kwargs)


*TimeLLM
Time-LLM is a reprogramming framework to repurpose an off-the-shelf LLM
for time series forecasting.
It trains a reprogramming layer that translates the observed series into
a language task. This is fed to the LLM and an output projection layer
translates the output back to numerical predictions.
**Parameters:**  
 `h`: int, Forecast horizon.   
 `input_size`: int,
autorregresive inputs size, y=[1,2,3,4] input_size=2 ->
y_[t-2:t]=[1,2].  
 `patch_len`: int=16, length of patch.  

`stride`: int=8, stride of patch.  
 `d_ff`: int=128, dimension of
fcn.  
 `top_k`: int=5, top tokens to consider.  
 `d_llm`: int=768,
hidden dimension of LLM.  
 # LLama7b:4096; GPT2-small:768;
BERT-base:768 `d_model`: int=32, dimension of model.  
 `n_heads`:
int=8, number of heads in attention layer.  
 `enc_in`: int=7, encoder
input size.  
 `dec_in`: int=7, decoder input size.  
 `llm` = None,
Path to pretrained LLM model to use. If not specified, it will use GPT-2
from [https://huggingface.co/openai-community/gpt2”](https://huggingface.co/openai-community/gpt2%E2%80%9D)  
 `llm_config` =
Deprecated, configuration of LLM. If not specified, it will use the
configuration of GPT-2 from
[https://huggingface.co/openai-community/gpt2”](https://huggingface.co/openai-community/gpt2%E2%80%9D)  
 `llm_tokenizer` =
Deprecated, tokenizer of LLM. If not specified, it will use the GPT-2
tokenizer from [https://huggingface.co/openai-community/gpt2”](https://huggingface.co/openai-community/gpt2%E2%80%9D)  

`llm_num_hidden_layers` = 32, hidden layers in LLM
`llm_output_attention`: bool = True, whether to output attention in
encoder.  
 `llm_output_hidden_states`: bool = True, whether to output
hidden states.  
 `prompt_prefix`: str=None, prompt to inform the LLM
about the dataset.  
 `dropout`: float=0.1, dropout rate.  

`stat_exog_list`: str list, static exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`futr_exog_list`: str list, future exogenous columns.  
 `loss`:
PyTorch module, instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`max_steps`: int=1000, maximum number of training steps.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=1024, number of windows to
sample in each training batch, default uses all.  

`inference_windows_batch_size`: int=1024, number of windows to sample in
each inference batch.  
 `start_padding_enabled`: bool=False, if True,
the model will pad the time series with zeros at the beginning, by input
size.  
 `step_size`: int=1, step size between each window of temporal
data.  
 `num_lr_decays`: int=-1, Number of learning rate decays,
evenly distributed across max_steps.  
 `early_stop_patience_steps`:
int=-1, Number of validation iterations before early stopping.  

`scaler_type`: str=‘identity’, type of scaler for temporal inputs
normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  
  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int,
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References:**  
 -[Ming Jin, Shiyu Wang, Lintao Ma, Zhixuan Chu,
James Y. Zhang, Xiaoming Shi, Pin-Yu Chen, Yuxuan Liang, Yuan-Fang Li,
Shirui Pan, Qingsong Wen. “Time-LLM: Time Series Forecasting by
Reprogramming Large Language
Models”](https://arxiv.org/abs/2310.01728)*

### [​](#timellm-fit)TimeLLM.fit


> CopyAsk AI TimeLLM.fit (dataset, val_size=0, test_size=0, random_seed=None,
>               distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#timellm-predict)TimeLLM.predict


> CopyAsk AI TimeLLM.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                   quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#usage-example)Usage example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import TimeLLM
from neuralforecast.utils import AirPassengersPanel

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]] # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

prompt_prefix = "The dataset contains data on monthly air passengers. There is a yearly seasonality"

timellm = TimeLLM(h=12,
                 input_size=36,
                 llm='openai-community/gpt2',
                 prompt_prefix=prompt_prefix,
                 batch_size=16,
                 valid_batch_size=16,
                 windows_batch_size=16)

nf = NeuralForecast(
    models=[timellm],
    freq='ME'
)

nf.fit(df=Y_train_df, val_size=12)
forecasts = nf.predict(futr_df=Y_test_df)
```

---

## TimeMixer - Nixtla
<a id="TimeMixer-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.timemixer.html

### [​](#embedding)Embedding



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timemixer.py#L26)
### [​](#dataembedding-wo-pos)DataEmbedding_wo_pos


> CopyAsk AI DataEmbedding_wo_pos (c_in, d_model, dropout=0.1, embed_type='fixed',
>                        freq='h')


*DataEmbedding_wo_pos*
### [​](#dft-decomposition)DFT decomposition



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timemixer.py#L51)
### [​](#dft-series-decomp)DFT_series_decomp


> CopyAsk AI DFT_series_decomp (top_k)


*Series decomposition block*
### [​](#mixing)Mixing



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timemixer.py#L160)
### [​](#pastdecomposablemixing)PastDecomposableMixing


> CopyAsk AI PastDecomposableMixing (seq_len, pred_len, down_sampling_window,
>                          down_sampling_layers, d_model, dropout,
>                          channel_independence, decomp_method, d_ff,
>                          moving_avg, top_k)


*PastDecomposableMixing*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timemixer.py#L114)
### [​](#multiscaletrendmixing)MultiScaleTrendMixing


> CopyAsk AI MultiScaleTrendMixing (seq_len, down_sampling_window,
>                         down_sampling_layers)


*Top-down mixing trend pattern*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timemixer.py#L71)
### [​](#multiscaleseasonmixing)MultiScaleSeasonMixing


> CopyAsk AI MultiScaleSeasonMixing (seq_len, down_sampling_window,
>                          down_sampling_layers)


*Bottom-up mixing season pattern*
## [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timemixer.py#L252)
### [​](#timemixer)TimeMixer


> CopyAsk AI TimeMixer (h, input_size, n_series, stat_exog_list=None,
>             hist_exog_list=None, futr_exog_list=None, d_model:int=32,
>             d_ff:int=32, dropout:float=0.1, e_layers:int=4, top_k:int=5,
>             decomp_method:str='moving_avg', moving_avg:int=25,
>             channel_independence:int=0, down_sampling_layers:int=1,
>             down_sampling_window:int=2, down_sampling_method:str='avg',
>             use_norm:bool=True, decoder_input_size_multiplier:float=0.5,
>             loss=MAE(), valid_loss=None, max_steps:int=1000,
>             learning_rate:float=0.001, num_lr_decays:int=-1,
>             early_stop_patience_steps:int=-1, val_check_steps:int=100,
>             batch_size:int=32, valid_batch_size:Optional[int]=None,
>             windows_batch_size=32, inference_windows_batch_size=32,
>             start_padding_enabled=False, step_size:int=1,
>             scaler_type:str='identity', random_seed:int=1,
>             drop_last_loader:bool=False, alias:Optional[str]=None,
>             optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>             lr_scheduler_kwargs=None, dataloader_kwargs=None,
>             **trainer_kwargs)


*TimeMixer **Parameters**  
 `h`: int, Forecast horizon.   

`input_size`: int, autorregresive inputs size, y=[1,2,3,4]
input_size=2 -> y_[t-2:t]=[1,2].  
 `n_series`: int, number of
time-series.  
 `stat_exog_list`: str list, static exogenous
columns.  
 `hist_exog_list`: str list, historic exogenous columns.  

`futr_exog_list`: str list, future exogenous columns.  
 `d_model`:
int, dimension of the model.  
 `d_ff`: int, dimension of the
fully-connected network.  
 `dropout`: float, dropout rate.  

`e_layers`: int, number of encoder layers.  
 `top_k`: int, number of
selected frequencies.  
 `decomp_method`: str, method of series
decomposition [moving_avg, dft_decomp].  
 `moving_avg`: int, window
size of moving average.  
 `channel_independence`: int, 0: channel
dependence, 1: channel independence.  
 `down_sampling_layers`: int,
number of downsampling layers.  
 `down_sampling_window`: int, size of
downsampling window.  
 `down_sampling_method`: str, down sampling
method [avg, max, conv].  
 `use_norm`: bool, whether to normalize or
not.  
 `decoder_input_size_multiplier`: float = 0.5.  
 `loss`:
PyTorch module, instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=32, number of windows to
sample in each training batch, default uses all.  

`inference_windows_batch_size`: int=32, number of windows to sample in
each inference batch, -1 uses all.  
 `start_padding_enabled`:
bool=False, if True, the model will pad the time series with zeros at
the beginning, by input size.  
 `step_size`: int=1, step size between
each window of temporal data.  
 `scaler_type`: str=‘identity’, type of
scaler for temporal inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`:
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References**  
 [Shiyu Wang, Haixu Wu, Xiaoming Shi, Tengge Hu,
Huakun Luo, Lintao Ma, James Y. Zhang, Jun Zhou.”TimeMixer: Decomposable
Multiscale Mixing For Time Series
Forecasting”](https://openreview.net/pdf?id=7oLshfEIC2)  
*

### [​](#timemixer-fit)TimeMixer.fit


> CopyAsk AI TimeMixer.fit (dataset, val_size=0, test_size=0, random_seed=None,
>                 distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#timemixer-predict)TimeMixer.predict


> CopyAsk AI TimeMixer.predict (dataset, test_size=None, step_size=1,
>                     random_seed=None, quantiles=None,
>                     **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#3-usage-example)3. Usage example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import TimeMixer
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
from neuralforecast.losses.pytorch import MAE

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = TimeMixer(h=12,
                input_size=24,
                n_series=2,
                scaler_type='standard',
                max_steps=500,
                early_stop_patience_steps=-1,
                val_check_steps=5,
                learning_rate=1e-3,
                loss = MAE(),
                valid_loss=MAE(),
                batch_size=32
                )

fcst = NeuralForecast(models=[model], freq='ME')
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['TimeMixer'], c='blue', label='median')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```


Using `cross_validation` to forecast multiple historic values.
CopyAsk AI```
fcst = NeuralForecast(models=[model], freq='M')
forecasts = fcst.cross_validation(df=AirPassengersPanel, static_df=AirPassengersStatic, n_windows=2, step_size=12)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.loc['Airline1']
Y_df = AirPassengersPanel[AirPassengersPanel['unique_id']=='Airline1']

plt.plot(Y_df['ds'], Y_df['y'], c='black', label='True')
plt.plot(Y_hat_df['ds'], Y_hat_df['TimeMixer'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```

---

## TimesNet - Nixtla
<a id="TimesNet-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.timesnet.html

The TimesNet univariate model tackles the challenge of modeling multiple
intraperiod and interperiod temporal variations.
The architecture has the following distinctive features: - An embedding
layer that maps the input sequence into a latent space. - Transformation
of 1D time seires into 2D tensors, based on periods found by FFT. - A
convolutional Inception block that captures temporal variations at
different scales and between periods.
**References**  
 - [Haixu Wu and Tengge Hu and Yong Liu and Hang Zhou
and Jianmin Wang and Mingsheng Long. TimesNet: Temporal 2D-Variation
Modeling for General Time Series
Analysis](https://openreview.net/pdf?id=ju_Uqw384Oq) - Based on the
implementation in [https://github.com/thuml/Time-Series-Library](https://github.com/thuml/Time-Series-Library) (license:
[https://github.com/thuml/Time-Series-Library/blob/main/LICENSE](https://github.com/thuml/Time-Series-Library/blob/main/LICENSE))
 
## [​](#1-auxiliary-functions)1. Auxiliary Functions



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timesnet.py#L20)
### [​](#inception-block-v1)Inception_Block_V1


> CopyAsk AI Inception_Block_V1 (in_channels, out_channels, num_kernels=6,
>                      init_weight=True)


*Inception_Block_V1*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timesnet.py#L66)
### [​](#timesblock)TimesBlock


> CopyAsk AI TimesBlock (input_size, h, k, hidden_size, conv_hidden_size, num_kernels)


*TimesBlock*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timesnet.py#L54)
### [​](#fft-for-period)FFT_for_Period


> CopyAsk AI FFT_for_Period (x, k=2)


## [​](#2-timesnet)2. TimesNet



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timesnet.py#L122)
### [​](#timesnet)TimesNet


> CopyAsk AI TimesNet (h:int, input_size:int, stat_exog_list=None,
>            hist_exog_list=None, futr_exog_list=None,
>            exclude_insample_y=False, hidden_size:int=64,
>            dropout:float=0.1, conv_hidden_size:int=64, top_k:int=5,
>            num_kernels:int=6, encoder_layers:int=2, loss=MAE(),
>            valid_loss=None, max_steps:int=1000,
>            learning_rate:float=0.0001, num_lr_decays:int=-1,
>            early_stop_patience_steps:int=-1, val_check_steps:int=100,
>            batch_size:int=32, valid_batch_size:Optional[int]=None,
>            windows_batch_size=64, inference_windows_batch_size=256,
>            start_padding_enabled=False, step_size:int=1,
>            scaler_type:str='standard', random_seed:int=1,
>            drop_last_loader:bool=False, alias:Optional[str]=None,
>            optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>            lr_scheduler_kwargs=None, dataloader_kwargs=None,
>            **trainer_kwargs)


*TimesNet
The TimesNet univariate model tackles the challenge of modeling multiple
intraperiod and interperiod temporal variations.
**Parameters**  
 `h` : int, Forecast horizon.  
 `input_size` : int,
Length of input window (lags).  
 `stat_exog_list` : list of str,
optional (default=None), Static exogenous columns.  
 `hist_exog_list`
: list of str, optional (default=None), Historic exogenous columns.  

`futr_exog_list` : list of str, optional (default=None), Future
exogenous columns.  
 `exclude_insample_y` : bool (default=False), The
model skips the autoregressive features y[t-input_size:t] if True.  

`hidden_size` : int (default=64), Size of embedding for embedding and
encoders.  
 `dropout` : float between [0, 1) (default=0.1), Dropout
for embeddings.  
 `conv_hidden_size`: int (default=64), Channels of
the Inception block.  
 `top_k`: int (default=5), Number of
periods.  
 `num_kernels`: int (default=6), Number of kernels for the
Inception block.  
 `encoder_layers` : int, (default=2), Number of
encoder layers.  
 `loss`: PyTorch module (default=MAE()), Instantiated
train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).
`valid_loss`: PyTorch module (default=None, uses loss), Instantiated
validation loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int (default=1000), Maximum number of training steps.  

`learning_rate` : float (default=1e-4), Learning rate.  

`num_lr_decays`: int (default=-1), Number of learning rate decays,
evenly distributed across max_steps. If -1, no learning rate decay is
performed.  
 `early_stop_patience_steps` : int (default=-1), Number of
validation iterations before early stopping. If -1, no early stopping is
performed.  
 `val_check_steps` : int (default=100), Number of training
steps between every validation loss check.  
 `batch_size` : int
(default=32), Number of different series in each batch.  

`valid_batch_size` : int (default=None), Number of different series in
each validation and test batch, if None uses batch_size.  

`windows_batch_size` : int (default=64), Number of windows to sample in
each training batch.  
 `inference_windows_batch_size` : int
(default=256), Number of windows to sample in each inference batch.  

`start_padding_enabled` : bool (default=False), If True, the model will
pad the time series with zeros at the beginning by input size.  

`step_size` : int (default=1), Step size between each window of temporal
data.  
 `scaler_type` : str (default=‘standard’), Type of scaler for
temporal inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed` : int (default=1), Random_seed for pytorch initializer and
numpy generators.  
 `drop_last_loader` : bool (default=False), If True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias` : str,
optional (default=None), Custom name of the model.  
 `optimizer`:
Subclass of ‘torch.optim.Optimizer’, optional (default=None), User
specified optimizer instead of the default choice (Adam).  

`optimizer_kwargs`: dict, optional (defualt=None), List of parameters
used by the user specified `optimizer`.  
 `lr_scheduler`: Subclass of
‘torch.optim.lr_scheduler.LRScheduler’, optional, user specified
lr_scheduler instead of the default choice (StepLR).  

`lr_scheduler_kwargs`: dict, optional, list of parameters used by the
user specified `lr_scheduler`.  
  

`dataloader_kwargs`: dict, optional (default=None), List of parameters
passed into the PyTorch Lightning dataloader by the
`TimeSeriesDataLoader`.   
 `**trainer_kwargs`: Keyword trainer
arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer)*

### [​](#timesnet-fit)TimesNet.fit


> CopyAsk AI TimesNet.fit (dataset, val_size=0, test_size=0, random_seed=None,
>                distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#timesnet-predict)TimesNet.predict


> CopyAsk AI TimesNet.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                    quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#usage-example)Usage Example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.losses.pytorch import DistributionLoss
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]] # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = TimesNet(h=12,
                 input_size=24,
                 hidden_size = 16,
                 conv_hidden_size = 32,
                 loss=DistributionLoss(distribution='Normal', level=[80, 90]),
                 scaler_type='standard',
                 learning_rate=1e-3,
                 max_steps=100,
                 val_check_steps=50,
                 early_stop_patience_steps=2)

nf = NeuralForecast(
    models=[model],
    freq='ME'
)
nf.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = nf.predict(futr_df=Y_test_df)

Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

if model.loss.is_distribution_output:
    plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
    plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
    plt.plot(plot_df['ds'], plot_df['TimesNet-median'], c='blue', label='median')
    plt.fill_between(x=plot_df['ds'][-12:], 
                    y1=plot_df['TimesNet-lo-90'][-12:].values, 
                    y2=plot_df['TimesNet-hi-90'][-12:].values,
                    alpha=0.4, label='level 90')
    plt.grid()
    plt.legend()
    plt.plot()
else:
    plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
    plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
    plt.plot(plot_df['ds'], plot_df['TimesNet'], c='blue', label='Forecast')
    plt.legend()
    plt.grid()
```

---

## TimeXer - Nixtla
<a id="TimeXer-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.timexer.html

# [​](#1-auxiliary-functions)1. Auxiliary functions



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timexer.py#L22)
### [​](#flattenhead)FlattenHead


> CopyAsk AI FlattenHead (n_vars, nf, target_window, head_dropout=0)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timexer.py#L37)
### [​](#encoder)Encoder


> CopyAsk AI Encoder (layers, norm_layer=None, projection=None)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timexer.py#L58)
### [​](#encoderlayer)EncoderLayer


> CopyAsk AI EncoderLayer (self_attention, cross_attention, d_model, d_ff=None,
>                dropout=0.1, activation='relu')


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timexer.py#L108)
### [​](#enembedding)EnEmbedding


> CopyAsk AI EnEmbedding (n_vars, d_model, patch_len, dropout)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*
# [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timexer.py#L135)
### [​](#timexer)TimeXer


> CopyAsk AI TimeXer (h, input_size, n_series, futr_exog_list=None,
>           hist_exog_list=None, stat_exog_list=None,
>           exclude_insample_y:bool=False, patch_len:int=16,
>           hidden_size:int=512, n_heads:int=8, e_layers:int=2,
>           d_ff:int=2048, factor:int=1, dropout:float=0.1,
>           use_norm:bool=True, loss=MAE(), valid_loss=None,
>           max_steps:int=1000, learning_rate:float=0.001,
>           num_lr_decays:int=-1, early_stop_patience_steps:int=-1,
>           val_check_steps:int=100, batch_size:int=32,
>           valid_batch_size:Optional[int]=None, windows_batch_size=32,
>           inference_windows_batch_size=32, start_padding_enabled=False,
>           step_size:int=1, scaler_type:str='identity', random_seed:int=1,
>           drop_last_loader:bool=False, alias:Optional[str]=None,
>           optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>           lr_scheduler_kwargs=None, dataloader_kwargs=None,
>           **trainer_kwargs)


*TimeXer
**Parameters:**  
 `h`: int, Forecast horizon.   
 `input_size`: int,
autorregresive inputs size, y=[1,2,3,4] input_size=2 ->
y_[t-2:t]=[1,2].  
 `n_series`: int, number of time-series.  

`futr_exog_list`: str list, future exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`stat_exog_list`: str list, static exogenous columns.  
 `patch_len`:
int, length of patches.  
 `hidden_size`: int, dimension of the
model.  
 `n_heads`: int, number of heads.  
 `e_layers`: int, number
of encoder layers.  
 `d_ff`: int, dimension of fully-connected
layer.  
 `factor`: int, attention factor.  
 `dropout`: float,
dropout rate.  
 `use_norm`: bool, whether to normalize or not.  

`loss`: PyTorch module, instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=32, number of windows in each
batch.  
  

`inference_windows_batch_size`: int=32, number of windows to sample in
each inference batch, -1 uses all.  
 `start_padding_enabled`:
bool=False, if True, the model will pad the time series with zeros at
the beginning, by input size.  
 `step_size`: int=1, step size between
each window of temporal data.  
 `scaler_type`: str=‘identity’, type of
scaler for temporal inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int,
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**Parameters:**  

**References** - [Yuxuan Wang, Haixu Wu, Jiaxiang Dong, Guo Qin, Haoran
Zhang, Yong Liu, Yunzhong Qiu, Jianmin Wang, Mingsheng Long. “TimeXer:
Empowering Transformers for Time Series Forecasting with Exogenous
Variables”](https://arxiv.org/abs/2402.19072)*

### [​](#timexer-fit)TimeXer.fit


> CopyAsk AI TimeXer.fit (dataset, val_size=0, test_size=0, random_seed=None,
>               distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#timexer-predict)TimeXer.predict


> CopyAsk AI TimeXer.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                   quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
CopyAsk AI```
# Unit tests for models
logging.getLogger("pytorch_lightning").setLevel(logging.ERROR)
logging.getLogger("lightning_fabric").setLevel(logging.ERROR)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    check_model(TimeXer, ["airpassengers"])
```


# [​](#3-usage-example)3. Usage example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import TimeXer
from neuralforecast.losses.pytorch import MSE
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic, augment_calendar_df

AirPassengersPanel, calendar_cols = augment_calendar_df(df=AirPassengersPanel, freq='M')

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]] # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = TimeXer(h=12,
                input_size=24,
                n_series=2,
                futr_exog_list=["trend", "month"],
                patch_len=12,
                hidden_size=128,
                n_heads=16,
                e_layers=2,
                d_ff=256,
                factor=1,
                dropout=0.1,
                use_norm=True,
                loss=MSE(),
                valid_loss=MAE(),
                early_stop_patience_steps=3,
                batch_size=32)

fcst = NeuralForecast(models=[model], freq='ME')
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['TimeXer'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```

---

## TSMixer - Nixtla
<a id="TSMixer-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.tsmixer.html

Time-Series Mixer (`TSMixer`) is a MLP-based multivariate time-series forecasting model. `TSMixer` jointly learns temporal and cross-sectional representations of the time-series by repeatedly combining time- and feature information using stacked mixing layers. A mixing layer consists of a sequential time- and feature Multi Layer Perceptron (`MLP`). Note: this model cannot handle exogenous inputs. If you want to use additional exogenous inputs, use `TSMixerx`.

## [​](#1-auxiliary-functions)1. Auxiliary Functions


## [​](#1-1-mixing-layers)1.1 Mixing layers


A mixing layer consists of a sequential time- and feature Multi Layer
Perceptron
([`MLP`](https://nixtlaverse.nixtla.io/neuralforecast/models.mlp.html#mlp)).

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L68)
### [​](#mixinglayer)MixingLayer


> CopyAsk AI MixingLayer (n_series, input_size, dropout, ff_dim)


*MixingLayer*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L37)
### [​](#featuremixing)FeatureMixing


> CopyAsk AI FeatureMixing (n_series, input_size, dropout, ff_dim)


*FeatureMixing*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L17)
### [​](#temporalmixing)TemporalMixing


> CopyAsk AI TemporalMixing (n_series, input_size, dropout)


*TemporalMixing*
## [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixer.py#L97)
### [​](#tsmixer)TSMixer


> CopyAsk AI TSMixer (h, input_size, n_series, futr_exog_list=None,
>           hist_exog_list=None, stat_exog_list=None,
>           exclude_insample_y=False, n_block=2, ff_dim=64, dropout=0.9,
>           revin=True, loss=MAE(), valid_loss=None, max_steps:int=1000,
>           learning_rate:float=0.001, num_lr_decays:int=-1,
>           early_stop_patience_steps:int=-1, val_check_steps:int=100,
>           batch_size:int=32, valid_batch_size:Optional[int]=None,
>           windows_batch_size=32, inference_windows_batch_size=32,
>           start_padding_enabled=False, step_size:int=1,
>           scaler_type:str='identity', random_seed:int=1,
>           drop_last_loader:bool=False, alias:Optional[str]=None,
>           optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>           lr_scheduler_kwargs=None, dataloader_kwargs=None,
>           **trainer_kwargs)


*TSMixer
Time-Series Mixer
([`TSMixer`](https://nixtlaverse.nixtla.io/neuralforecast/models.tsmixer.html#tsmixer))
is a MLP-based multivariate time-series forecasting model.
[`TSMixer`](https://nixtlaverse.nixtla.io/neuralforecast/models.tsmixer.html#tsmixer)
jointly learns temporal and cross-sectional representations of the
time-series by repeatedly combining time- and feature information using
stacked mixing layers. A mixing layer consists of a sequential time- and
feature Multi Layer Perceptron
([`MLP`](https://nixtlaverse.nixtla.io/neuralforecast/models.mlp.html#mlp)).
**Parameters:**  
 `h`: int, forecast horizon.  
 `input_size`: int,
considered autorregresive inputs (lags), y=[1,2,3,4] input_size=2 ->
lags=[1,2].  
 `n_series`: int, number of time-series.  

`futr_exog_list`: str list, future exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`stat_exog_list`: str list, static exogenous columns.  

`exclude_insample_y`: bool=False, if True excludes the target variable
from the input features.  
 `n_block`: int=2, number of mixing layers
in the model.  
 `ff_dim`: int=64, number of units for the second
feed-forward layer in the feature MLP.  
 `dropout`: float=0.9, dropout
rate between (0, 1) .  
 `revin`: bool=True, if True uses Reverse
Instance Normalization to process inputs and outputs.  
 `loss`:
PyTorch module, instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=32, number of windows to
sample in each training batch, default uses all.  

`inference_windows_batch_size`: int=32, number of windows to sample in
each inference batch, -1 uses all.  
 `start_padding_enabled`:
bool=False, if True, the model will pad the time series with zeros at
the beginning, by input size.  
 `step_size`: int=1, step size between
each window of temporal data.  
 `scaler_type`: str=‘identity’, type of
scaler for temporal inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
  

`dataloader_kwargs`: dict, optional, list of parameters passed into the
PyTorch Lightning dataloader by the `TimeSeriesDataLoader`.   

`**trainer_kwargs`: int, keyword trainer arguments inherited from
[PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References:**  
 - [Chen, Si-An, Chun-Liang Li, Nate Yoder, Sercan O.
Arik, and Tomas Pfister (2023). “TSMixer: An All-MLP Architecture for
Time Series Forecasting.”](http://arxiv.org/abs/2303.06053)*

### [​](#tsmixer-fit)TSMixer.fit


> CopyAsk AI TSMixer.fit (dataset, val_size=0, test_size=0, random_seed=None,
>               distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#tsmixer-predict)TSMixer.predict


> CopyAsk AI TSMixer.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                   quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
CopyAsk AI```
# Unit tests for models
logging.getLogger("pytorch_lightning").setLevel(logging.ERROR)
logging.getLogger("lightning_fabric").setLevel(logging.ERROR)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    check_model(TSMixer, ["airpassengers"])
```


## [​](#3-usage-examples)3. Usage Examples


Train model and forecast future values with `predict` method.
CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import TSMixer
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
from neuralforecast.losses.pytorch import MAE, MQLoss

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = TSMixer(h=12,
                input_size=24,
                n_series=2, 
                n_block=4,
                ff_dim=4,
                dropout=0,
                revin=True,
                scaler_type='standard',
                max_steps=500,
                early_stop_patience_steps=-1,
                val_check_steps=5,
                learning_rate=1e-3,
                loss=MQLoss(),
                batch_size=32
                )

fcst = NeuralForecast(models=[model], freq='ME')
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline2'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['TSMixer-median'], c='blue', label='median')
plt.fill_between(x=plot_df['ds'][-12:], 
                 y1=plot_df['TSMixer-lo-90'][-12:].values,
                 y2=plot_df['TSMixer-hi-90'][-12:].values,
                 alpha=0.4, label='level 90')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```


Using `cross_validation` to forecast multiple historic values.
CopyAsk AI```
fcst = NeuralForecast(models=[model], freq='M')
forecasts = fcst.cross_validation(df=AirPassengersPanel, static_df=AirPassengersStatic, n_windows=2, step_size=12)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.loc['Airline1']
Y_df = AirPassengersPanel[AirPassengersPanel['unique_id']=='Airline1']

plt.plot(Y_df['ds'], Y_df['y'], c='black', label='True')
plt.plot(Y_hat_df['ds'], Y_hat_df['TSMixer-median'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```

---

## TSMixerx - Nixtla
<a id="TSMixerx-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.tsmixerx.html

Time-Series Mixer exogenous (`TSMixerx`) is a MLP-based multivariate time-series forecasting model, with capability for additional exogenous inputs. `TSMixerx` jointly learns temporal and cross-sectional representations of the time-series by repeatedly combining time- and feature information using stacked mixing layers. A mixing layer consists of a sequential time- and feature Multi Layer Perceptron (`MLP`).

## [​](#1-auxiliary-functions)1. Auxiliary Functions


## [​](#1-1-mixing-layers)1.1 Mixing layers


A mixing layer consists of a sequential time- and feature Multi Layer
Perceptron
([`MLP`](https://nixtlaverse.nixtla.io/neuralforecast/models.mlp.html#mlp)).

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L93)
### [​](#mixinglayerwithstaticexogenous)MixingLayerWithStaticExogenous


> CopyAsk AI MixingLayerWithStaticExogenous (h, dropout, ff_dim, stat_input_size)


*MixingLayerWithStaticExogenous*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L68)
### [​](#mixinglayer)MixingLayer


> CopyAsk AI MixingLayer (in_features, out_features, h, dropout, ff_dim)


*MixingLayer*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L37)
### [​](#featuremixing)FeatureMixing


> CopyAsk AI FeatureMixing (in_features, out_features, h, dropout, ff_dim)


*FeatureMixing*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L17)
### [​](#temporalmixing)TemporalMixing


> CopyAsk AI TemporalMixing (num_features, h, dropout)


*TemporalMixing*
## [​](#1-2-reversible-instancenormalization)1.2 Reversible InstanceNormalization


An Instance Normalization Layer that is reversible, based on [this
reference
implementation](https://github.com/google-research/google-research/blob/master/tsmixer/tsmixer_basic/models/rev_in.py).  

## [​](#2-model)2. Model



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/tsmixerx.py#L163)
### [​](#tsmixerx)TSMixerx


> CopyAsk AI TSMixerx (h, input_size, n_series, futr_exog_list=None,
>            hist_exog_list=None, stat_exog_list=None,
>            exclude_insample_y=False, n_block=2, ff_dim=64, dropout=0.0,
>            revin=True, loss=MAE(), valid_loss=None, max_steps:int=1000,
>            learning_rate:float=0.001, num_lr_decays:int=-1,
>            early_stop_patience_steps:int=-1, val_check_steps:int=100,
>            batch_size:int=32, valid_batch_size:Optional[int]=None,
>            windows_batch_size=32, inference_windows_batch_size=32,
>            start_padding_enabled=False, step_size:int=1,
>            scaler_type:str='identity', random_seed:int=1,
>            drop_last_loader:bool=False, alias:Optional[str]=None,
>            optimizer=None, optimizer_kwargs=None, lr_scheduler=None,
>            lr_scheduler_kwargs=None, dataloader_kwargs=None,
>            **trainer_kwargs)


*TSMixerx
Time-Series Mixer exogenous
([`TSMixerx`](https://nixtlaverse.nixtla.io/neuralforecast/models.tsmixerx.html#tsmixerx))
is a MLP-based multivariate time-series forecasting model, with
capability for additional exogenous inputs.
[`TSMixerx`](https://nixtlaverse.nixtla.io/neuralforecast/models.tsmixerx.html#tsmixerx)
jointly learns temporal and cross-sectional representations of the
time-series by repeatedly combining time- and feature information using
stacked mixing layers. A mixing layer consists of a sequential time- and
feature Multi Layer Perceptron
([`MLP`](https://nixtlaverse.nixtla.io/neuralforecast/models.mlp.html#mlp)).
**Parameters:**  
 `h`: int, forecast horizon.  
 `input_size`: int,
considered autorregresive inputs (lags), y=[1,2,3,4] input_size=2 ->
lags=[1,2].  
 `n_series`: int, number of time-series.  

`futr_exog_list`: str list, future exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`stat_exog_list`: str list, static exogenous columns.  

`exclude_insample_y`: bool=False, if True excludes insample_y from the
model.  
 `n_block`: int=2, number of mixing layers in the model.  

`ff_dim`: int=64, number of units for the second feed-forward layer in
the feature MLP.  
 `dropout`: float=0.0, dropout rate between (0, 1)
.  
 `revin`: bool=True, if True uses Reverse Instance Normalization on
`insample_y` and applies it to the outputs.  
  

`loss`: PyTorch module, instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=32, number of windows to
sample in each training batch.   
 `inference_windows_batch_size`:
int=32, number of windows to sample in each inference batch, -1 uses
all.  
 `start_padding_enabled`: bool=False, if True, the model will
pad the time series with zeros at the beginning, by input size.  

`step_size`: int=1, step size between each window of temporal data.  

`scaler_type`: str=‘identity’, type of scaler for temporal inputs
normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
  

`dataloader_kwargs`: dict, optional, list of parameters passed into the
PyTorch Lightning dataloader by the `TimeSeriesDataLoader`.   

`**trainer_kwargs`: int, keyword trainer arguments inherited from
[PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

**References:**  
 - [Chen, Si-An, Chun-Liang Li, Nate Yoder, Sercan O.
Arik, and Tomas Pfister (2023). “TSMixer: An All-MLP Architecture for
Time Series Forecasting.”](http://arxiv.org/abs/2303.06053)*

### [​](#tsmixerx-fit)TSMixerx.fit


> CopyAsk AI TSMixerx.fit (dataset, val_size=0, test_size=0, random_seed=None,
>                distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#tsmixerx-predict)TSMixerx.predict


> CopyAsk AI TSMixerx.predict (dataset, test_size=None, step_size=1, random_seed=None,
>                    quantiles=None, **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
CopyAsk AI```
# Unit tests for models
logging.getLogger("pytorch_lightning").setLevel(logging.ERROR)
logging.getLogger("lightning_fabric").setLevel(logging.ERROR)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    check_model(TSMixerx, ["airpassengers"])
```


## [​](#3-usage-examples)3. Usage Examples


Train model and forecast future values with `predict` method.
CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import TSMixerx
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic
from neuralforecast.losses.pytorch import GMM

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = TSMixerx(h=12,
                input_size=24,
                n_series=2,
                stat_exog_list=['airline1'],
                futr_exog_list=['trend'],
                n_block=4,
                ff_dim=4,
                revin=True,
                scaler_type='robust',
                max_steps=500,
                early_stop_patience_steps=-1,
                val_check_steps=5,
                learning_rate=1e-3,
                loss = GMM(n_components=10, weighted=True),
                batch_size=32
                )

fcst = NeuralForecast(models=[model], freq='ME')
fcst.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = fcst.predict(futr_df=Y_test_df)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
plt.plot(plot_df['ds'], plot_df['TSMixerx-median'], c='blue', label='median')
plt.fill_between(x=plot_df['ds'][-12:], 
                 y1=plot_df['TSMixerx-lo-90'][-12:].values,
                 y2=plot_df['TSMixerx-hi-90'][-12:].values,
                 alpha=0.4, label='level 90')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```


Using `cross_validation` to forecast multiple historic values.
CopyAsk AI```
fcst = NeuralForecast(models=[model], freq='M')
forecasts = fcst.cross_validation(df=AirPassengersPanel, static_df=AirPassengersStatic, n_windows=2, step_size=12)

# Plot predictions
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
Y_hat_df = forecasts.loc['Airline1']
Y_df = AirPassengersPanel[AirPassengersPanel['unique_id']=='Airline1']

plt.plot(Y_df['ds'], Y_df['y'], c='black', label='True')
plt.plot(Y_hat_df['ds'], Y_hat_df['TSMixerx-median'], c='blue', label='Forecast')
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Year', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```

---

## Vanilla Transformer - Nixtla
<a id="Vanilla-Transformer-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.vanillatransformer.html

Vanilla Transformer, following implementation of the Informer paper,
used as baseline.
The architecture has three distinctive features: - Full-attention
mechanism with O(L^2) time and memory complexity. - Classic
encoder-decoder proposed by Vaswani et al. (2017) with a multi-head
attention mechanism. - An MLP multi-step decoder that predicts long
time-series sequences in a single forward operation rather than
step-by-step.
The Vanilla Transformer model utilizes a three-component approach to
define its embedding: - It employs encoded autoregressive features
obtained from a convolution network. - It uses window-relative
positional embeddings derived from harmonic functions. - Absolute
positional embeddings obtained from calendar features are utilized.
**References**  
 - [Haoyi Zhou, Shanghang Zhang, Jieqi Peng, Shuai
Zhang, Jianxin Li, Hui Xiong, Wancai Zhang. “Informer: Beyond Efficient
Transformer for Long Sequence Time-Series
Forecasting”](https://arxiv.org/abs/2012.07436)  

 
## [​](#1-vanillatransformer)1. VanillaTransformer



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/vanillatransformer.py#L27)
### [​](#vanillatransformer)VanillaTransformer


> CopyAsk AI VanillaTransformer (h:int, input_size:int, stat_exog_list=None,
>                      hist_exog_list=None, futr_exog_list=None,
>                      exclude_insample_y=False,
>                      decoder_input_size_multiplier:float=0.5,
>                      hidden_size:int=128, dropout:float=0.05,
>                      n_head:int=4, conv_hidden_size:int=32,
>                      activation:str='gelu', encoder_layers:int=2,
>                      decoder_layers:int=1, loss=MAE(), valid_loss=None,
>                      max_steps:int=5000, learning_rate:float=0.0001,
>                      num_lr_decays:int=-1,
>                      early_stop_patience_steps:int=-1,
>                      val_check_steps:int=100, batch_size:int=32,
>                      valid_batch_size:Optional[int]=None,
>                      windows_batch_size=1024,
>                      inference_windows_batch_size:int=1024,
>                      start_padding_enabled=False, step_size:int=1,
>                      scaler_type:str='identity', random_seed:int=1,
>                      drop_last_loader:bool=False,
>                      alias:Optional[str]=None, optimizer=None,
>                      optimizer_kwargs=None, lr_scheduler=None,
>                      lr_scheduler_kwargs=None, dataloader_kwargs=None,
>                      **trainer_kwargs)


*VanillaTransformer
Vanilla Transformer, following implementation of the Informer paper,
used as baseline.
The architecture has three distinctive features: - Full-attention
mechanism with O(L^2) time and memory complexity. - An MLP multi-step
decoder that predicts long time-series sequences in a single forward
operation rather than step-by-step.
The Vanilla Transformer model utilizes a three-component approach to
define its embedding: - It employs encoded autoregressive features
obtained from a convolution network. - It uses window-relative
positional embeddings derived from harmonic functions. - Absolute
positional embeddings obtained from calendar features are utilized.
*Parameters:*  
 `h`: int, forecast horizon.  
 `input_size`: int,
maximum sequence length for truncated train backpropagation.   

`stat_exog_list`: str list, static exogenous columns.  

`hist_exog_list`: str list, historic exogenous columns.  

`futr_exog_list`: str list, future exogenous columns.  

`exclude_insample_y`: bool=False, whether to exclude the target variable
from the input.  
 `decoder_input_size_multiplier`: float = 0.5, .  

`hidden_size`: int=128, units of embeddings and encoders.  
 `dropout`:
float (0, 1), dropout throughout Informer architecture.  
 `n_head`:
int=4, controls number of multi-head’s attention.  

`conv_hidden_size`: int=32, channels of the convolutional encoder.  

`activation`: str=`GELU`, activation from [‘ReLU’, ‘Softplus’, ‘Tanh’,
‘SELU’, ‘LeakyReLU’, ‘PReLU’, ‘Sigmoid’, ‘GELU’].  
 `encoder_layers`:
int=2, number of layers for the TCN encoder.  
 `decoder_layers`:
int=1, number of layers for the MLP decoder.  
 `loss`: PyTorch module,
instantiated train loss class from [losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  

`valid_loss`: PyTorch module=`loss`, instantiated valid loss class from
[losses
collection](https://nixtla.github.io/neuralforecast/losses.pytorch.html).  
  

`max_steps`: int=1000, maximum number of training steps.  

`learning_rate`: float=1e-3, Learning rate between (0, 1).  

`num_lr_decays`: int=-1, Number of learning rate decays, evenly
distributed across max_steps.  
 `early_stop_patience_steps`: int=-1,
Number of validation iterations before early stopping.  

`val_check_steps`: int=100, Number of training steps between every
validation loss check.  
 `batch_size`: int=32, number of different
series in each batch.  
 `valid_batch_size`: int=None, number of
different series in each validation and test batch, if None uses
batch_size.  
 `windows_batch_size`: int=1024, number of windows to
sample in each training batch, default uses all.  

`inference_windows_batch_size`: int=1024, number of windows to sample in
each inference batch.  
 `start_padding_enabled`: bool=False, if True,
the model will pad the time series with zeros at the beginning, by input
size.  
 `step_size`: int=1, step size between each window of temporal
data.  
 `scaler_type`: str=‘robust’, type of scaler for temporal
inputs normalization see [temporal
scalers](https://nixtla.github.io/neuralforecast/common.scalers.html).  

`random_seed`: int=1, random_seed for pytorch initializer and numpy
generators.  
 `drop_last_loader`: bool=False, if True
`TimeSeriesDataLoader` drops last non-full batch.  
 `alias`: str,
optional, Custom name of the model.  
 `optimizer`: Subclass of
‘torch.optim.Optimizer’, optional, user specified optimizer instead of
the default choice (Adam).  
 `optimizer_kwargs`: dict, optional, list
of parameters used by the user specified `optimizer`.  

`lr_scheduler`: Subclass of ‘torch.optim.lr_scheduler.LRScheduler’,
optional, user specified lr_scheduler instead of the default choice
(StepLR).  
 `lr_scheduler_kwargs`: dict, optional, list of parameters
used by the user specified `lr_scheduler`.  
 `dataloader_kwargs`:
dict, optional, list of parameters passed into the PyTorch Lightning
dataloader by the `TimeSeriesDataLoader`.   
 `**trainer_kwargs`: int,
keyword trainer arguments inherited from [PyTorch Lighning’s
trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).  

CopyAsk AI```
*References*<br/>
- [Haoyi Zhou, Shanghang Zhang, Jieqi Peng, Shuai Zhang, Jianxin Li, Hui Xiong, Wancai Zhang. "Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting"](https://arxiv.org/abs/2012.07436)<br/>*
```



### [​](#vanillatransformer-fit)VanillaTransformer.fit


> CopyAsk AI VanillaTransformer.fit (dataset, val_size=0, test_size=0,
>                          random_seed=None, distributed_config=None)


*Fit.
The `fit` method, optimizes the neural network’s weights using the
initialization parameters (`learning_rate`, `windows_batch_size`, …) and
the `loss` function as defined during the initialization. Within `fit`
we use a PyTorch Lightning `Trainer` that inherits the initialization’s
`self.trainer_kwargs`, to customize its inputs, see [PL’s trainer
arguments](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).
The method is designed to be compatible with SKLearn-like classes and in
particular to be compatible with the StatsForecast library.
By default the `model` is not saving training checkpoints to protect
disk memory, to get them change `enable_checkpointing=True` in
`__init__`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`val_size`: int, validation size for temporal cross-validation.  

`random_seed`: int=None, random_seed for pytorch initializer and numpy
generators, overwrites model.__init__’s.  
 `test_size`: int, test
size for temporal cross-validation.  
*

### [​](#vanillatransformer-predict)VanillaTransformer.predict


> CopyAsk AI VanillaTransformer.predict (dataset, test_size=None, step_size=1,
>                              random_seed=None, quantiles=None,
>                              **data_module_kwargs)


*Predict.
Neural network prediction with PL’s `Trainer` execution of
`predict_step`.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset),
see
[documentation](https://nixtla.github.io/neuralforecast/tsdataset.html).  

`test_size`: int=None, test size for temporal cross-validation.  

`step_size`: int=1, Step size between each window.  
 `random_seed`:
int=None, random_seed for pytorch initializer and numpy generators,
overwrites model.__init__’s.  
 `quantiles`: list of floats,
optional (default=None), target quantiles to predict.   

`**data_module_kwargs`: PL’s TimeSeriesDataModule args, see
[documentation](https://pytorch-lightning.readthedocs.io/en/1.6.1/extensions/datamodules.html#using-a-datamodule).*
## [​](#usage-example)Usage Example


CopyAsk AI```
import pandas as pd
import matplotlib.pyplot as plt

from neuralforecast import NeuralForecast
from neuralforecast.models import VanillaTransformer
from neuralforecast.utils import AirPassengersPanel, AirPassengersStatic

Y_train_df = AirPassengersPanel[AirPassengersPanel.ds<AirPassengersPanel['ds'].values[-12]] # 132 train
Y_test_df = AirPassengersPanel[AirPassengersPanel.ds>=AirPassengersPanel['ds'].values[-12]].reset_index(drop=True) # 12 test

model = VanillaTransformer(h=12,
                 input_size=24,
                 hidden_size=16,
                 conv_hidden_size=32,
                 n_head=2,
                 loss=MAE(),
                 scaler_type='robust',
                 learning_rate=1e-3,
                 max_steps=500,
                 val_check_steps=50,
                 early_stop_patience_steps=2)

nf = NeuralForecast(
    models=[model],
    freq='ME'
)
nf.fit(df=Y_train_df, static_df=AirPassengersStatic, val_size=12)
forecasts = nf.predict(futr_df=Y_test_df)

Y_hat_df = forecasts.reset_index(drop=False).drop(columns=['unique_id','ds'])
plot_df = pd.concat([Y_test_df, Y_hat_df], axis=1)
plot_df = pd.concat([Y_train_df, plot_df])

if model.loss.is_distribution_output:
    plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
    plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
    plt.plot(plot_df['ds'], plot_df['VanillaTransformer-median'], c='blue', label='median')
    plt.fill_between(x=plot_df['ds'][-12:], 
                    y1=plot_df['VanillaTransformer-lo-90'][-12:].values, 
                    y2=plot_df['VanillaTransformer-hi-90'][-12:].values,
                    alpha=0.4, label='level 90')
    plt.grid()
    plt.legend()
    plt.plot()
else:
    plot_df = plot_df[plot_df.unique_id=='Airline1'].drop('unique_id', axis=1)
    plt.plot(plot_df['ds'], plot_df['y'], c='black', label='True')
    plt.plot(plot_df['ds'], plot_df['VanillaTransformer'], c='blue', label='Forecast')
    plt.legend()
    plt.grid()
```

---

## xLSTM - Nixtla
<a id="xLSTM-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/models.xlstm

# [​](#module-neuralforecast-models-xlstm)module `neuralforecast.models.xlstm`


## [​](#global-variables)**Global Variables**


- **IS_XLSTM_INSTALLED**



## [​](#class-xlstm)class `xLSTM`


xLSTM
xLSTM encoder, with MLP decoder.
**Args:**
- **`h`** (int):  forecast horizon.
- **`input_size`** (int):  considered autorregresive inputs (lags), y=[1,2,3,4] input_size=2 -> lags=[1,2].
- **`encoder_n_blocks`** (int):  number of blocks for the xLSTM.
- **`encoder_hidden_size`** (int):  units for the xLSTM’s hidden state size.
- **`encoder_bias`** (bool):  whether or not to use biases within xLSTM blocks.
- **`encoder_dropout`** (float):  dropout regularization applied within xLSTM blocks.
- **`decoder_hidden_size`** (int):  size of hidden layer for the MLP decoder.
- **`decoder_layers`** (int):  number of layers for the MLP decoder.
- **`decoder_dropout`** (float):  dropout regularization applied within the MLP decoder.
- **`decoder_activation`** (str):  activation function for the MLP decoder, see [activations collection](https://docs.pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity).
- **`backbone`** (str):  backbone for the xLSTM, either ‘sLSTM’ or ‘mLSTM’.
- **`futr_exog_list`** (List[str]):  future exogenous columns.
- **`hist_exog_list`** (list):  historic exogenous columns.
- **`stat_exog_list`** (list):  static exogenous columns.
- **`exclude_insample_y`** (bool):  whether to exclude the target variable from the input.
- **`recurrent`** (bool):  whether to produce forecasts recursively (True) or direct (False).
- **`loss`** (nn.Module):  instantiated train loss class from [losses collection](https://nixtlaverse.nixtla.io/neuralforecast/losses.pytorch).
- **`valid_loss`** (nn.Module):  instantiated valid loss class from [losses collection](https://nixtlaverse.nixtla.io/neuralforecast/losses.pytorch).
- **`max_steps`** (int):  maximum number of training steps.
- **`learning_rate`** (float):  Learning rate between (0, 1).
- **`num_lr_decays`** (int):  Number of learning rate decays, evenly distributed across max_steps.
- **`early_stop_patience_steps`** (int):  Number of validation iterations before early stopping.
- **`val_check_steps`** (int):  Number of training steps between every validation loss check.
- **`batch_size`** (int):  number of differentseries in each batch.
- **`valid_batch_size`** (int):  number of different series in each validation and test batch.
- **`windows_batch_size`** (int):  number of windows to sample in each training batch, default uses all.
- **`inference_windows_batch_size`** (int):  number of windows to sample in each inference batch, -1 uses all.
- **`start_padding_enabled`** (bool):  if True, the model will pad the time series with zeros at the beginning, by input size.
- **`training_data_availability_threshold`** (Union[float, List[float]]):  minimum fraction of valid data points required for training windows. Single float applies to both insample and outsample; list of two floats specifies [insample_fraction, outsample_fraction]. Default 0.0 allows windows with only 1 valid data point (current behavior).
- **`step_size`** (int):  step size between each window of temporal data.
- **`scaler_type`** (str):  type of scaler for temporal inputs normalization see [temporal scalers](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/common/_scalers.py).
- **`random_seed`** (int):  random_seed for pytorch initializer and numpy generators.
- **`drop_last_loader`** (bool):  if True `TimeSeriesDataLoader` drops last non-full batch.
- **`alias`** (str):  optional,  Custom name of the model.
- **`optimizer`** (Subclass of ‘torch.optim.Optimizer’):  optional, user specified optimizer instead of the default choice (Adam).
- **`optimizer_kwargs`** (dict):  optional, list of parameters used by the user specified `optimizer`.
- **`lr_scheduler`** (Subclass of ‘torch.optim.lr_scheduler.LRScheduler’):  optional, user specified lr_scheduler instead of the default choice (StepLR).
- **`lr_scheduler_kwargs`** (dict):  optional, list of parameters used by the user specified `lr_scheduler`.
- **`dataloader_kwargs`** (dict):  optional, list of parameters passed into the PyTorch Lightning dataloader by the `TimeSeriesDataLoader`.
- **`**trainer_kwargs (int)`**:  keyword trainer arguments inherited from [PyTorch Lighning’s trainer](https://pytorch-lightning.readthedocs.io/en/stable/api/pytorch_lightning.trainer.trainer.Trainer.html?highlight=trainer).


References:
- [Maximilian Beck, Korbinian Pöppel, Markus Spanring, Andreas Auer, Oleksandra Prudnikova, Michael Kopp, Günter Klambauer, Johannes Brandstetter, Sepp Hochreiter (2024). “xLSTM: Extended Long Short-Term Memory”](https://arxiv.org/abs/2405.04517)


### [​](#method-init)method `__init__`


CopyAsk AI```
__init__(
    h: int,
    input_size: int = -1,
    inference_input_size: Optional[int] = None,
    h_train: int = 1,
    encoder_n_blocks: int = 2,
    encoder_hidden_size: int = 128,
    encoder_bias: bool = True,
    encoder_dropout: float = 0.1,
    decoder_hidden_size: int = 128,
    decoder_layers: int = 1,
    decoder_dropout: float = 0.0,
    decoder_activation: str = 'GELU',
    backbone: str = 'mLSTM',
    futr_exog_list=None,
    hist_exog_list=None,
    stat_exog_list=None,
    exclude_insample_y=False,
    recurrent=False,
    loss=MAE(),
    valid_loss=None,
    max_steps: int = 1000,
    learning_rate: float = 0.001,
    num_lr_decays: int = -1,
    early_stop_patience_steps: int = -1,
    val_check_steps: int = 100,
    batch_size=32,
    valid_batch_size: Optional[int] = None,
    windows_batch_size=128,
    inference_windows_batch_size=1024,
    start_padding_enabled=False,
    training_data_availability_threshold=0.0,
    step_size: int = 1,
    scaler_type: str = 'robust',
    random_seed=1,
    drop_last_loader=False,
    alias: Optional[str] = None,
    optimizer=None,
    optimizer_kwargs=None,
    lr_scheduler=None,
    lr_scheduler_kwargs=None,
    dataloader_kwargs=None,
    **trainer_kwargs
)
```



#### [​](#property-automatic-optimization)property automatic_optimization


If set to `False` you are responsible for calling `.backward()`, `.step()`, `.zero_grad()`.

#### [​](#property-current-epoch)property current_epoch


The current epoch in the `Trainer`, or 0 if not attached.

#### [​](#property-device)property device



#### [​](#property-device-mesh)property device_mesh


Strategies like `ModelParallelStrategy` will create a device mesh that can be accessed in the :meth:`~pytorch_lightning.core.hooks.ModelHooks.configure_model` hook to parallelize the LightningModule.

#### [​](#property-dtype)property dtype



#### [​](#property-example-input-array)property example_input_array


The example input array is a specification of what the module can consume in the :meth:`forward` method. The return type is interpreted as follows:
- Single tensor: It is assumed the model takes a single argument, i.e.,  `model.forward(model.example_input_array)`
- Tuple: The input array should be interpreted as a sequence of positional arguments, i.e.,  `model.forward(*model.example_input_array)`
- Dict: The input array represents named keyword arguments, i.e.,  `model.forward(**model.example_input_array)`



#### [​](#property-fabric)property fabric



#### [​](#property-global-rank)property global_rank


The index of the current process across all nodes and devices.

#### [​](#property-global-step)property global_step


Total training batches seen across all epochs.
If no Trainer is attached, this property is 0.

#### [​](#property-hparams)property hparams


The collection of hyperparameters saved with :meth:`save_hyperparameters`. It is mutable by the user. For the frozen set of initial hyperparameters, use :attr:`hparams_initial`.
**Returns:**
Mutable hyperparameters dictionary

#### [​](#property-hparams-initial)property hparams_initial


The collection of hyperparameters saved with :meth:`save_hyperparameters`. These contents are read-only. Manual updates to the saved hyperparameters can instead be performed through :attr:`hparams`.
**Returns:**
- **`AttributeDict`**:  immutable initial hyperparameters



#### [​](#property-local-rank)property local_rank


The index of the current process within a single node.

#### [​](#property-logger)property logger


Reference to the logger object in the Trainer.

#### [​](#property-loggers)property loggers


Reference to the list of loggers in the Trainer.

#### [​](#property-on-gpu)property on_gpu


Returns `True` if this model is currently located on a GPU.
Useful to set flags around the LightningModule for different CPU vs GPU behavior.

#### [​](#property-strict-loading)property strict_loading


Determines how Lightning loads this model using `.load_state_dict(..., strict=model.strict_loading)`.

#### [​](#property-trainer)property trainer



### [​](#method-forward)method `forward`


CopyAsk AI```
forward(windows_batch)
```

---

## PyTorch Losses - Nixtla
<a id="PyTorch-Losses-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/losses.pytorch.html

NeuralForecast contains a collection PyTorch Loss classes aimed to be used during the models' optimization.

The most important train signal is the forecast error, which is the
difference between the observed value yτy_{\tau}yτ​ and the prediction
y^τ\hat{y}_{\tau}y^​τ​, at time yτy_{\tau}yτ​:
eτ=yτ−y^ττ∈{t+1,…,t+H}e_{\tau} = y_{\tau}-\hat{y}_{\tau} \qquad \qquad \tau \in \{t+1,\dots,t+H \}eτ​=yτ​−y^​τ​τ∈{t+1,…,t+H}
The train loss summarizes the forecast errors in different train
optimization objectives.
All the losses are `torch.nn.modules` which helps to automatically moved
them across CPU/GPU/TPU devices with Pytorch Lightning.

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L50)
### [​](#basepointloss)BasePointLoss


> CopyAsk AI BasePointLoss (horizon_weight=None, outputsize_multiplier=None,
>                 output_names=None)


*Base class for point loss functions.
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
 `outputsize_multiplier`:
Multiplier for the output size.   
 `output_names`: Names of the
outputs.   
*
# [​](#1-scale-dependent-errors)1. Scale-dependent Errors


These metrics are on the same scale as the data.
## [​](#mean-absolute-error-mae)Mean Absolute Error (MAE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L103)
### [​](#mae-init)MAE.__init__


> CopyAsk AI MAE.__init__ (horizon_weight=None)


*Mean Absolute Error
Calculates Mean Absolute Error between `y` and `y_hat`. MAE measures the
relative prediction accuracy of a forecasting method by calculating the
deviation of the prediction and the true value at a given time and
averages these devations over the length of the series.
MAE(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣\mathrm{MAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} |y_{\tau} - \hat{y}_{\tau}|MAE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​−y^​τ​∣
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L124)
### [​](#mae-call)MAE.__call__


> CopyAsk AI MAE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                mask:Optional[torch.Tensor]=None,
>                y_insample:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`mae`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mae):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mae_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=155a03ab35bf439a5e84d13240ffd1e8)
## [​](#mean-squared-error-mse)Mean Squared Error (MSE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L145)
### [​](#mse-init)MSE.__init__


> CopyAsk AI MSE.__init__ (horizon_weight=None)


*Mean Squared Error
Calculates Mean Squared Error between `y` and `y_hat`. MSE measures the
relative prediction accuracy of a forecasting method by calculating the
squared deviation of the prediction and the true value at a given time,
and averages these devations over the length of the series.
MSE(yτ,y^τ)=1H∑τ=t+1t+H(yτ−y^τ)2\mathrm{MSE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} (y_{\tau} - \hat{y}_{\tau})^{2}MSE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​(yτ​−y^​τ​)2
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L166)
### [​](#mse-call)MSE.__call__


> CopyAsk AI MSE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                y_insample:torch.Tensor, mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`mse`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mse):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mse_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=938bc9e8bbbefece696fe397c823efd7)
## [​](#root-mean-squared-error-rmse)Root Mean Squared Error (RMSE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L187)
### [​](#rmse-init)RMSE.__init__


> CopyAsk AI RMSE.__init__ (horizon_weight=None)


*Root Mean Squared Error
Calculates Root Mean Squared Error between `y` and `y_hat`. RMSE
measures the relative prediction accuracy of a forecasting method by
calculating the squared deviation of the prediction and the observed
value at a given time and averages these devations over the length of
the series. Finally the RMSE will be in the same scale as the original
time series so its comparison with other series is possible only if they
share a common scale. RMSE has a direct connection to the L2 norm.
RMSE(yτ,y^τ)=1H∑τ=t+1t+H(yτ−y^τ)2\mathrm{RMSE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \sqrt{\frac{1}{H} \sum^{t+H}_{\tau=t+1} (y_{\tau} - \hat{y}_{\tau})^{2}}RMSE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​(yτ​−y^​τ​)2​
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L211)
### [​](#rmse-call)RMSE.__call__


> CopyAsk AI RMSE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                 mask:Optional[torch.Tensor]=None,
>                 y_insample:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`rmse`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#rmse):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/rmse_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=ce7c8abd1e08bdb3cd445d13db639aeb)
# [​](#2-percentage-errors)2. Percentage errors


These metrics are unit-free, suitable for comparisons across series.
## [​](#mean-absolute-percentage-error-mape)Mean Absolute Percentage Error (MAPE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L233)
### [​](#mape-init)MAPE.__init__


> CopyAsk AI MAPE.__init__ (horizon_weight=None)


*Mean Absolute Percentage Error
Calculates Mean Absolute Percentage Error between `y` and `y_hat`. MAPE
measures the relative prediction accuracy of a forecasting method by
calculating the percentual deviation of the prediction and the observed
value at a given time and averages these devations over the length of
the series. The closer to zero an observed value is, the higher penalty
MAPE loss assigns to the corresponding error.
MAPE(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣∣yτ∣\mathrm{MAPE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{|y_{\tau}|}MAPE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​∣∣yτ​−y^​τ​∣​
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   

**References:**  
 [Makridakis S., “Accuracy measures: theoretical and
practical
concerns”.](https://www.sciencedirect.com/science/article/pii/0169207093900793)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L258)
### [​](#mape-call)MAPE.__call__


> CopyAsk AI MAPE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                 y_insample:torch.Tensor, mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`mape`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mape):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mape_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=15de69fb4f6f1e7300d31cf4408ccf4f)
## [​](#symmetric-mape-smape)Symmetric MAPE (sMAPE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L281)
### [​](#smape-init)SMAPE.__init__


> CopyAsk AI SMAPE.__init__ (horizon_weight=None)


*Symmetric Mean Absolute Percentage Error
Calculates Symmetric Mean Absolute Percentage Error between `y` and
`y_hat`. SMAPE measures the relative prediction accuracy of a
forecasting method by calculating the relative deviation of the
prediction and the observed value scaled by the sum of the absolute
values for the prediction and observed value at a given time, then
averages these devations over the length of the series. This allows the
SMAPE to have bounds between 0% and 200% which is desireble compared to
normal MAPE that may be undetermined when the target is zero.
sMAPE2(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣∣yτ∣+∣y^τ∣\mathrm{sMAPE}_{2}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{|y_{\tau}|+|\hat{y}_{\tau}|}sMAPE2​(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​∣+∣y^​τ​∣∣yτ​−y^​τ​∣​
**Parameters:**  
 `horizon_weight`: Tensor of size h, weight for each
timestamp of the forecasting window.   

**References:**  
 [Makridakis S., “Accuracy measures: theoretical and
practical
concerns”.](https://www.sciencedirect.com/science/article/pii/0169207093900793)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L308)
### [​](#smape-call)SMAPE.__call__


> CopyAsk AI SMAPE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                  mask:Optional[torch.Tensor]=None,
>                  y_insample:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`smape`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#smape):
tensor (single value).*
# [​](#3-scale-independent-errors)3. Scale-independent Errors


These metrics measure the relative improvements versus baselines.
## [​](#mean-absolute-scaled-error-mase)Mean Absolute Scaled Error (MASE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L331)
### [​](#mase-init)MASE.__init__


> CopyAsk AI MASE.__init__ (seasonality:int, horizon_weight=None)


*Mean Absolute Scaled Error Calculates the Mean Absolute Scaled Error
between `y` and `y_hat`. MASE measures the relative prediction accuracy
of a forecasting method by comparinng the mean absolute errors of the
prediction and the observed value against the mean absolute errors of
the seasonal naive model. The MASE partially composed the Overall
Weighted Average (OWA), used in the M4 Competition.
MASE(yτ,y^τ,y^τseason)=1H∑τ=t+1t+H∣yτ−y^τ∣MAE(yτ,y^τseason)\mathrm{MASE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}, \mathbf{\hat{y}}^{season}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{\mathrm{MAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{season}_{\tau})}MASE(yτ​,y^​τ​,y^​τseason​)=H1​∑τ=t+1t+H​MAE(yτ​,y^​τseason​)∣yτ​−y^​τ​∣​
**Parameters:**  
 `seasonality`: int. Main frequency of the time
series; Hourly 24, Daily 7, Weekly 52, Monthly 12, Quarterly 4,
Yearly 1. `horizon_weight`: Tensor of size h, weight for each timestamp
of the forecasting window.   

**References:**  
 [Rob J. Hyndman, & Koehler, A. B. “Another look at
measures of forecast
accuracy”.](https://www.sciencedirect.com/science/article/pii/S0169207006000239)  

[Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, “The
M4 Competition: 100,000 time series and 61 forecasting
methods”.](https://www.sciencedirect.com/science/article/pii/S0169207019301128)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L358)
### [​](#mase-call)MASE.__call__


> CopyAsk AI MASE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                 y_insample:torch.Tensor, mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor (batch_size, output_size), Actual
values.  
 `y_hat`: tensor (batch_size, output_size)), Predicted
values.  
 `y_insample`: tensor (batch_size, input_size), Actual
insample values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`mase`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mase):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mase_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=9cba699ceb4b7ff7b2b9c553207379b9)
## [​](#relative-mean-squared-error-relmse)Relative Mean Squared Error (relMSE)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L387)
### [​](#relmse-init)relMSE.__init__


> CopyAsk AI relMSE.__init__ (y_train=None, horizon_weight=None)


*Relative Mean Squared Error Computes Relative Mean Squared Error
(relMSE), as proposed by Hyndman & Koehler (2006) as an alternative to
percentage errors, to avoid measure unstability.
relMSE(y,y^,y^benchmark)=MSE(y,y^)MSE(y,y^benchmark) \mathrm{relMSE}(\mathbf{y}, \mathbf{\hat{y}}, \mathbf{\hat{y}}^{benchmark}) =
\frac{\mathrm{MSE}(\mathbf{y}, \mathbf{\hat{y}})}{\mathrm{MSE}(\mathbf{y}, \mathbf{\hat{y}}^{benchmark})} relMSE(y,y^​,y^​benchmark)=MSE(y,y^​benchmark)MSE(y,y^​)​
**Parameters:**  
 `y_train`: numpy array, deprecated.  

`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 - [Hyndman, R. J and Koehler, A. B. (2006). “Another
look at measures of forecast accuracy”, International Journal of
Forecasting, Volume 22, Issue
4.](https://www.sciencedirect.com/science/article/pii/S0169207006000239)  
 -
[Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan Reddy, Mengfei Cao,
Lee Dicker. “Probabilistic Hierarchical Forecasting with Deep Poisson
Mixtures. Submitted to the International Journal Forecasting, Working
paper available at arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L415)
### [​](#relmse-call)relMSE.__call__


> CopyAsk AI relMSE.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                   y_benchmark:torch.Tensor,
>                   mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor (batch_size, output_size), Actual
values.  
 `y_hat`: tensor (batch_size, output_size)), Predicted
values.  
 `y_benchmark`: tensor (batch_size, output_size), Benchmark
predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`relMSE`](https://nixtlaverse.nixtla.io/neuralforecast/losses.pytorch.html#relmse):
tensor (single value).*
# [​](#4-probabilistic-errors)4. Probabilistic Errors


These methods use statistical approaches for estimating unknown
probability distributions using observed data.
Maximum likelihood estimation involves finding the parameter values that
maximize the likelihood function, which measures the probability of
obtaining the observed data given the parameter values. MLE has good
theoretical properties and efficiency under certain satisfied
assumptions.
On the non-parametric approach, quantile regression measures
non-symmetrically deviation, producing under/over estimation.
## [​](#quantile-loss)Quantile Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L439)
### [​](#quantileloss-init)QuantileLoss.__init__


> CopyAsk AI QuantileLoss.__init__ (q, horizon_weight=None)


*Quantile Loss
Computes the quantile loss between `y` and `y_hat`. QL measures the
deviation of a quantile forecast. By weighting the absolute deviation in
a non symmetric way, the loss pays more attention to under or over
estimation. A common value for q is 0.5 for the deviation from the
median (Pinball loss).
QL(yτ,y^τ(q))=1H∑τ=t+1t+H((1−q) (y^τ(q)−yτ)++q (yτ−y^τ(q))+)\mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \Big( (1-q)\,( \hat{y}^{(q)}_{\tau} - y_{\tau} )_{+} + q\,( y_{\tau} - \hat{y}^{(q)}_{\tau} )_{+} \Big)QL(yτ​,y^​τ(q)​)=H1​∑τ=t+1t+H​((1−q)(y^​τ(q)​−yτ​)+​+q(yτ​−y^​τ(q)​)+​)
**Parameters:**  
 `q`: float, between 0 and 1. The slope of the
quantile loss, in the context of quantile regression, the q determines
the conditional quantile level.  
 `horizon_weight`: Tensor of size h,
weight for each timestamp of the forecasting window.   

**References:**  
 [Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L466)
### [​](#quantileloss-call)QuantileLoss.__call__


> CopyAsk AI QuantileLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                         y_insample:torch.Tensor,
>                         mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`quantile_loss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#quantile_loss):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/q_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=426c786498233e8b1f59f960b46b4391)
## [​](#multi-quantile-loss-mqloss)Multi Quantile Loss (MQLoss)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L516)
### [​](#mqloss-init)MQLoss.__init__


> CopyAsk AI MQLoss.__init__ (level=[80, 90], quantiles=None, horizon_weight=None)


*Multi-Quantile loss
Calculates the Multi-Quantile loss (MQL) between `y` and `y_hat`. MQL
calculates the average multi-quantile Loss for a given set of quantiles,
based on the absolute difference between predicted quantiles and
observed values.
MQL(yτ,[y^τ(q1),...,y^τ(qn)])=1n∑qiQL(yτ,y^τ(qi))\mathrm{MQL}(\mathbf{y}_{\tau},[\mathbf{\hat{y}}^{(q_{1})}_{\tau}, ... ,\hat{y}^{(q_{n})}_{\tau}]) = \frac{1}{n} \sum_{q_{i}} \mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q_{i})}_{\tau})MQL(yτ​,[y^​τ(q1​)​,...,y^​τ(qn​)​])=n1​∑qi​​QL(yτ​,y^​τ(qi​)​)
The limit behavior of MQL allows to measure the accuracy of a full
predictive distribution F^τ\mathbf{\hat{F}}_{\tau}F^τ​ with the continuous
ranked probability score (CRPS). This can be achieved through a
numerical integration technique, that discretizes the quantiles and
treats the CRPS integral with a left Riemann approximation, averaging
over uniformly distanced quantiles.
CRPS(yτ,F^τ)=∫01QL(yτ,y^τ(q))dq\mathrm{CRPS}(y_{\tau}, \mathbf{\hat{F}}_{\tau}) = \int^{1}_{0} \mathrm{QL}(y_{\tau}, \hat{y}^{(q)}_{\tau}) dqCRPS(yτ​,F^τ​)=∫01​QL(yτ​,y^​τ(q)​)dq
**Parameters:**  
 `level`: int list [0,100]. Probability levels for
prediction intervals (Defaults median). `quantiles`: float list [0.,
1.]. Alternative to level, quantiles to estimate from y distribution.
`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 [Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)  
 [James E.
Matheson and Robert L. Winkler, “Scoring Rules for Continuous
Probability Distributions”.](https://www.jstor.org/stable/2629907)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L599)
### [​](#mqloss-call)MQLoss.__call__


> CopyAsk AI MQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                   y_insample:torch.Tensor,
>                   mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  

[`mqloss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mqloss):
tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mq_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=18abc02ceb1f6910df7ab34f03948914)
## [​](#implicit-quantile-loss-iqloss)Implicit Quantile Loss (IQLoss)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L637)
### [​](#quantilelayer)QuantileLayer


> CopyAsk AI QuantileLayer (num_output:int, cos_embedding_dim:int=128)


*Implicit Quantile Layer from the paper
`IQN for Distributional Reinforcement Learning`
([https://arxiv.org/abs/1806.06923](https://arxiv.org/abs/1806.06923)) by Dabney et al. 2018.
Code from GluonTS:
[https://github.com/awslabs/gluonts/blob/dev/src/gluonts/torch/distributions/implicit_quantile_network.py\](https://github.com/awslabs/gluonts/blob/dev/src/gluonts/torch/distributions/implicit_quantile_network.py%5C)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L663)
### [​](#iqloss-init)IQLoss.__init__


> CopyAsk AI IQLoss.__init__ (cos_embedding_dim=64, concentration0=1.0,
>                   concentration1=1.0, horizon_weight=None)


*Implicit Quantile Loss
Computes the quantile loss between `y` and `y_hat`, with the quantile
`q` provided as an input to the network. IQL measures the deviation of a
quantile forecast. By weighting the absolute deviation in a non
symmetric way, the loss pays more attention to under or over estimation.
QL(yτ,y^τ(q))=1H∑τ=t+1t+H((1−q) (y^τ(q)−yτ)++q (yτ−y^τ(q))+)\mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \Big( (1-q)\,( \hat{y}^{(q)}_{\tau} - y_{\tau} )_{+} + q\,( y_{\tau} - \hat{y}^{(q)}_{\tau} )_{+} \Big)QL(yτ​,y^​τ(q)​)=H1​∑τ=t+1t+H​((1−q)(y^​τ(q)​−yτ​)+​+q(yτ​−y^​τ(q)​)+​)
**Parameters:**  
 `quantile_sampling`: str, default=‘uniform’,
sampling distribution used to sample the quantiles during training.
Choose from [‘uniform’, ‘beta’].   
 `horizon_weight`: Tensor of size
h, weight for each timestamp of the forecasting window.   

**References:**  
 [Gouttes, Adèle, Kashif Rasul, Mateusz Koren,
Johannes Stephan, and Tofigh Naghibi, “Probabilistic Time Series
Forecasting with Implicit Quantile
Networks”.](http://arxiv.org/abs/2107.03743)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L466)
### [​](#iqloss-call)IQLoss.__call__


> CopyAsk AI IQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                   y_insample:torch.Tensor,
>                   mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  

[`quantile_loss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#quantile_loss):
tensor (single value).*
## [​](#distributionloss)DistributionLoss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L1785)
### [​](#distributionloss-init)DistributionLoss.__init__


> CopyAsk AI DistributionLoss.__init__ (distribution, level=[80, 90], quantiles=None,
>                             num_samples=1000, return_params=False,
>                             horizon_weight=None, **distribution_kwargs)


*DistributionLoss
This PyTorch module wraps the `torch.distribution` classes allowing it
to interact with NeuralForecast models modularly. It shares the negative
log-likelihood as the optimization objective and a sample method to
generate empirically the quantiles defined by the `level` list.
Additionally, it implements a distribution transformation that
factorizes the scale-dependent likelihood parameters into a base scale
and a multiplier efficiently learnable within the network’s
non-linearities operating ranges.
Available distributions:  
 - Poisson  
 - Normal  
 - StudentT  
 -
NegativeBinomial  
 - Tweedie  
 - Bernoulli (Temporal
Classifiers)  
 - ISQF (Incremental Spline Quantile Function)
**Parameters:**  
 `distribution`: str, identifier of a
torch.distributions.Distribution class.  
 `level`: float list
[0,100], confidence levels for prediction intervals.  
 `quantiles`:
float list [0,1], alternative to level list, target quantiles.  

`num_samples`: int=500, number of samples for the empirical
quantiles.  
 `return_params`: bool=False, wether or not return the
Distribution parameters.  
 `horizon_weight`: Tensor of size h, weight
for each timestamp of the forecasting window.  
  

**References:**  
 - [PyTorch Probability Distributions Package:
StudentT.](https://pytorch.org/docs/stable/distributions.html#studentt)  
 -
[David Salinas, Valentin Flunkert, Jan Gasthaus, Tim Januschowski
(2020). “DeepAR: Probabilistic forecasting with autoregressive recurrent
networks”. International Journal of
Forecasting.](https://www.sciencedirect.com/science/article/pii/S0169207019301888)  
 -
[Park, Youngsuk, Danielle Maddix, François-Xavier Aubet, Kelvin Kan, Jan
Gasthaus, and Yuyang Wang (2022). “Learning Quantile Functions without
Quantile Crossing for Distribution-free Time Series
Forecasting”.](https://proceedings.mlr.press/v151/park22a.html)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L1949)
### [​](#distributionloss-sample)DistributionLoss.sample


> CopyAsk AI DistributionLoss.sample (distr_args:torch.Tensor,
>                           num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2019)
### [​](#distributionloss-call)DistributionLoss.__call__


> CopyAsk AI DistributionLoss.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                             mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `loc`:
Optional tensor, of the same shape as the batch_shape + event_shape of
the resulting distribution.  
 `scale`: Optional tensor, of the same
shape as the batch_shape+event_shape of the resulting distribution.  

`mask`: tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
## [​](#poisson-mixture-mesh-pmm)Poisson Mixture Mesh (PMM)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2053)
### [​](#pmm-init)PMM.__init__


> CopyAsk AI PMM.__init__ (n_components=10, level=[80, 90], quantiles=None,
>                num_samples=1000, return_params=False,
>                batch_correlation=False, horizon_correlation=False,
>                weighted=False)


*Poisson Mixture Mesh
This Poisson Mixture statistical model assumes independence across
groups of data G={[gi]}\mathcal{G}=\{[g_{i}]\}G={[gi​]}, and estimates relationships
within the group.
P(y[b][t+1:t+H])=∏[gi]∈GP(y[gi][τ])=∏β∈[gi](∑k=1Kwk∏(β,τ)∈[gi][t+1:t+H]Poisson(yβ,τ,λ^β,τ,k)) \mathrm{P}\left(\mathbf{y}_{[b][t+1:t+H]}\right) = 
\prod_{ [g_{i}] \in \mathcal{G}} \mathrm{P} \left(\mathbf{y}_{[g_{i}][\tau]} \right) =
\prod_{\beta\in[g_{i}]} 
\left(\sum_{k=1}^{K} w_k \prod_{(\beta,\tau) \in [g_i][t+1:t+H]} \mathrm{Poisson}(y_{\beta,\tau}, \hat{\lambda}_{\beta,\tau,k}) \right)P(y[b][t+1:t+H]​)=[gi​]∈G∏​P(y[gi​][τ]​)=β∈[gi​]∏​​k=1∑K​wk​(β,τ)∈[gi​][t+1:t+H]∏​Poisson(yβ,τ​,λ^β,τ,k​)​
**Parameters:**  
 `n_components`: int=10, the number of mixture
components.  
 `level`: float list [0,100], confidence levels for
prediction intervals.  
 `quantiles`: float list [0,1], alternative
to level list, target quantiles.  
 `return_params`: bool=False, wether
or not return the Distribution parameters.  
 `batch_correlation`:
bool=False, wether or not model batch correlations.  

`horizon_correlation`: bool=False, wether or not model horizon
correlations.  

**References:**  
 [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan
Reddy, Mengfei Cao, Lee Dicker. Probabilistic Hierarchical Forecasting
with Deep Poisson Mixtures. Submitted to the International Journal
Forecasting, Working paper available at
arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2192)
### [​](#pmm-sample)PMM.sample


> CopyAsk AI PMM.sample (distr_args:torch.Tensor, num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2241)
### [​](#pmm-call)PMM.__call__


> CopyAsk AI PMM.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `mask`:
tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/pmm.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=cd0e3519dafef82789a957abafcb5ad8)
## [​](#gaussian-mixture-mesh-gmm)Gaussian Mixture Mesh (GMM)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2279)
### [​](#gmm-init)GMM.__init__


> CopyAsk AI GMM.__init__ (n_components=1, level=[80, 90], quantiles=None,
>                num_samples=1000, return_params=False,
>                batch_correlation=False, horizon_correlation=False,
>                weighted=False)


*Gaussian Mixture Mesh
This Gaussian Mixture statistical model assumes independence across
groups of data G={[gi]}\mathcal{G}=\{[g_{i}]\}G={[gi​]}, and estimates relationships
within the group.
P(y[b][t+1:t+H])=∏[gi]∈GP(y[gi][τ])=∏β∈[gi](∑k=1Kwk∏(β,τ)∈[gi][t+1:t+H]Gaussian(yβ,τ,μ^β,τ,k,σβ,τ,k)) \mathrm{P}\left(\mathbf{y}_{[b][t+1:t+H]}\right) = 
\prod_{ [g_{i}] \in \mathcal{G}} \mathrm{P}\left(\mathbf{y}_{[g_{i}][\tau]}\right)=
\prod_{\beta\in[g_{i}]}
\left(\sum_{k=1}^{K} w_k \prod_{(\beta,\tau) \in [g_i][t+1:t+H]} 
\mathrm{Gaussian}(y_{\beta,\tau}, \hat{\mu}_{\beta,\tau,k}, \sigma_{\beta,\tau,k})\right)P(y[b][t+1:t+H]​)=[gi​]∈G∏​P(y[gi​][τ]​)=β∈[gi​]∏​​k=1∑K​wk​(β,τ)∈[gi​][t+1:t+H]∏​Gaussian(yβ,τ​,μ^​β,τ,k​,σβ,τ,k​)​
**Parameters:**  
 `n_components`: int=10, the number of mixture
components.  
 `level`: float list [0,100], confidence levels for
prediction intervals.  
 `quantiles`: float list [0,1], alternative
to level list, target quantiles.  
 `return_params`: bool=False, wether
or not return the Distribution parameters.  
 `batch_correlation`:
bool=False, wether or not model batch correlations.  

`horizon_correlation`: bool=False, wether or not model horizon
correlations.  
  

**References:**  
 [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan
Reddy, Mengfei Cao, Lee Dicker. Probabilistic Hierarchical Forecasting
with Deep Poisson Mixtures. Submitted to the International Journal
Forecasting, Working paper available at
arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2422)
### [​](#gmm-sample)GMM.sample


> CopyAsk AI GMM.sample (distr_args:torch.Tensor, num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2471)
### [​](#gmm-call)GMM.__call__


> CopyAsk AI GMM.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `mask`:
tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/gmm.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=137c048f21d86e054bc5f2405628fd5f)
## [​](#negative-binomial-mixture-mesh-nbmm)Negative Binomial Mixture Mesh (NBMM)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2508)
### [​](#nbmm-init)NBMM.__init__


> CopyAsk AI NBMM.__init__ (n_components=1, level=[80, 90], quantiles=None,
>                 num_samples=1000, return_params=False, weighted=False)


*Negative Binomial Mixture Mesh
This N. Binomial Mixture statistical model assumes independence across
groups of data G={[gi]}\mathcal{G}=\{[g_{i}]\}G={[gi​]}, and estimates relationships
within the group.
P(y[b][t+1:t+H])=∏[gi]∈GP(y[gi][τ])=∏β∈[gi](∑k=1Kwk∏(β,τ)∈[gi][t+1:t+H]NBinomial(yβ,τ,r^β,τ,k,p^β,τ,k)) \mathrm{P}\left(\mathbf{y}_{[b][t+1:t+H]}\right) = 
\prod_{ [g_{i}] \in \mathcal{G}} \mathrm{P}\left(\mathbf{y}_{[g_{i}][\tau]}\right)=
\prod_{\beta\in[g_{i}]}
\left(\sum_{k=1}^{K} w_k \prod_{(\beta,\tau) \in [g_i][t+1:t+H]} 
\mathrm{NBinomial}(y_{\beta,\tau}, \hat{r}_{\beta,\tau,k}, \hat{p}_{\beta,\tau,k})\right)P(y[b][t+1:t+H]​)=[gi​]∈G∏​P(y[gi​][τ]​)=β∈[gi​]∏​​k=1∑K​wk​(β,τ)∈[gi​][t+1:t+H]∏​NBinomial(yβ,τ​,r^β,τ,k​,p^​β,τ,k​)​
**Parameters:**  
 `n_components`: int=10, the number of mixture
components.  
 `level`: float list [0,100], confidence levels for
prediction intervals.  
 `quantiles`: float list [0,1], alternative
to level list, target quantiles.  
 `return_params`: bool=False, wether
or not return the Distribution parameters.  
  

**References:**  
 [Kin G. Olivares, O. Nganba Meetei, Ruijun Ma, Rohan
Reddy, Mengfei Cao, Lee Dicker. Probabilistic Hierarchical Forecasting
with Deep Poisson Mixtures. Submitted to the International Journal
Forecasting, Working paper available at
arxiv.](https://arxiv.org/pdf/2110.13179.pdf)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2655)
### [​](#nbmm-sample)NBMM.sample


> CopyAsk AI NBMM.sample (distr_args:torch.Tensor, num_samples:Optional[int]=None)


*Construct the empirical quantiles from the estimated Distribution,
sampling from it `num_samples` independently.
**Parameters**  
 `distr_args`: Constructor arguments for the
underlying Distribution type.  
 `num_samples`: int, overwrite number
of samples for the empirical quantiles.  

**Returns**  
 `samples`: tensor, shape [B,H,`num_samples`].  

`quantiles`: tensor, empirical quantiles defined by `levels`.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2704)
### [​](#nbmm-call)NBMM.__call__


> CopyAsk AI NBMM.__call__ (y:torch.Tensor, distr_args:torch.Tensor,
>                 mask:Optional[torch.Tensor]=None)


*Computes the negative log-likelihood objective function. To estimate
the following predictive distribution:
P(yτ ∣ θ)and−log⁡(P(yτ ∣ θ))\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta) \quad \mathrm{and} \quad -\log(\mathrm{P}(\mathbf{y}_{\tau}\,|\,\theta))P(yτ​∣θ)and−log(P(yτ​∣θ))
where θ\thetaθ represents the distributions parameters. It aditionally
summarizes the objective signal using a weighted average using the
`mask` tensor.
**Parameters**  
 `y`: tensor, Actual values.  
 `distr_args`:
Constructor arguments for the underlying Distribution type.  
 `mask`:
tensor, Specifies date stamps per serie to consider in loss.  

**Returns**  
 `loss`: scalar, weighted loss function against which
backpropagation will be performed.  
*
# [​](#5-robustified-errors)5. Robustified Errors


This type of errors from robust statistic focus on methods resistant to
outliers and violations of assumptions, providing reliable estimates and
inferences. Robust estimators are used to reduce the impact of outliers,
offering more stable results.
## [​](#huber-loss)Huber Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2735)
### [​](#huberloss-init)HuberLoss.__init__


> CopyAsk AI HuberLoss.__init__ (delta:float=1.0, horizon_weight=None)


*Huber Loss
The Huber loss, employed in robust regression, is a loss function that
exhibits reduced sensitivity to outliers in data when compared to the
squared error loss. This function is also refered as SmoothL1.
The Huber loss function is quadratic for small errors and linear for
large errors, with equal values and slopes of the different sections at
the two points where
(yτ−y^τ)2(y_{\tau}-\hat{y}_{\tau})^{2}(yτ​−y^​τ​)2=∣yτ−y^τ∣|y_{\tau}-\hat{y}_{\tau}|∣yτ​−y^​τ​∣.
Lδ(yτ,  y^τ)={12(yτ−y^τ)2  for ∣yτ−y^τ∣≤δδ ⋅(∣yτ−y^τ∣−12δ),  otherwise. L_{\delta}(y_{\tau},\; \hat{y}_{\tau})
=\begin{cases}{\frac{1}{2}}(y_{\tau}-\hat{y}_{\tau})^{2}\;{\text{for }}|y_{\tau}-\hat{y}_{\tau}|\leq \delta \\ 
\delta \ \cdot \left(|y_{\tau}-\hat{y}_{\tau}|-{\frac {1}{2}}\delta \right),\;{\text{otherwise.}}\end{cases}Lδ​(yτ​,y^​τ​)={21​(yτ​−y^​τ​)2for ∣yτ​−y^​τ​∣≤δδ ⋅(∣yτ​−y^​τ​∣−21​δ),otherwise.​
where δ\deltaδ is a threshold parameter that determines the point at
which the loss transitions from quadratic to linear, and can be tuned to
control the trade-off between robustness and accuracy in the
predictions.
**Parameters:**  
 `delta`: float=1.0, Specifies the threshold at which
to change between delta-scaled L1 and L2 loss. `horizon_weight`: Tensor
of size h, weight for each timestamp of the forecasting window.   

**References:**  
 [Huber Peter, J (1964). “Robust Estimation of a
Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2767)
### [​](#huberloss-call)HuberLoss.__call__


> CopyAsk AI HuberLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                      y_insample:torch.Tensor,
>                      mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `huber_loss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/huber_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=2598d8e03e7b8061c8a6f5abc8de00c7)
## [​](#tukey-loss)Tukey Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2788)
### [​](#tukeyloss-init)TukeyLoss.__init__


> CopyAsk AI TukeyLoss.__init__ (c:float=4.685, normalize:bool=True)


*Tukey Loss
The Tukey loss function, also known as Tukey’s biweight function, is a
robust statistical loss function used in robust statistics. Tukey’s loss
exhibits quadratic behavior near the origin, like the Huber loss;
however, it is even more robust to outliers as the loss for large
residuals remains constant instead of scaling linearly.
The parameter ccc in Tukey’s loss determines the ‘’saturation’’ point of
the function: Higher values of ccc enhance sensitivity, while lower
values increase resistance to outliers.
Lc(yτ,  y^τ)={c26[1−(yτ−y^τc)2]3  for ∣yτ−y^τ∣≤cc26otherwise. L_{c}(y_{\tau},\; \hat{y}_{\tau})
=\begin{cases}{
\frac{c^{2}}{6}} \left[1-(\frac{y_{\tau}-\hat{y}_{\tau}}{c})^{2} \right]^{3}    \;\text{for } |y_{\tau}-\hat{y}_{\tau}|\leq c \\ 
\frac{c^{2}}{6} \qquad \text{otherwise.}  \end{cases}Lc​(yτ​,y^​τ​)=⎩⎨⎧​6c2​[1−(cyτ​−y^​τ​​)2]3for ∣yτ​−y^​τ​∣≤c6c2​otherwise.​
Please note that the Tukey loss function assumes the data to be
stationary or normalized beforehand. If the error values are excessively
large, the algorithm may need help to converge during optimization. It
is advisable to employ small learning rates.
**Parameters:**  
 `c`: float=4.685, Specifies the Tukey loss’
threshold on which residuals are no longer considered.  
 `normalize`:
bool=True, Wether normalization is performed within Tukey loss’
computation.  

**References:**  
 [Beaton, A. E., and Tukey, J. W. (1974). “The
Fitting of Power Series, Meaning Polynomials, Illustrated on
Band-Spectroscopic Data.”](https://www.jstor.org/stable/1267936)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2843)
### [​](#tukeyloss-call)TukeyLoss.__call__


> CopyAsk AI TukeyLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                      y_insample:torch.Tensor,
>                      mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `tukey_loss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/tukey_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=1d0b4dcd359c5b2f6248a86839d3d772)
## [​](#huberized-quantile-loss)Huberized Quantile Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2881)
### [​](#huberqloss-init)HuberQLoss.__init__


> CopyAsk AI HuberQLoss.__init__ (q, delta:float=1.0, horizon_weight=None)


*Huberized Quantile Loss
The Huberized quantile loss is a modified version of the quantile loss
function that combines the advantages of the quantile loss and the Huber
loss. It is commonly used in regression tasks, especially when dealing
with data that contains outliers or heavy tails.
The Huberized quantile loss between `y` and `y_hat` measure the Huber
Loss in a non-symmetric way. The loss pays more attention to
under/over-estimation depending on the quantile parameter qqq; and
controls the trade-off between robustness and accuracy in the
predictions with the parameter deltadeltadelta.
HuberQL(yτ,y^τ(q))=(1−q) Lδ(yτ,  y^τ(q))1{y^τ(q)≥yτ}+q Lδ(yτ,  y^τ(q))1{y^τ(q)<yτ} \mathrm{HuberQL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = 
(1-q)\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} \geq y_{\tau} \} + 
q\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} < y_{\tau} \} HuberQL(yτ​,y^​τ(q)​)=(1−q)Lδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​≥yτ​}+qLδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​<yτ​}
**Parameters:**  
 `delta`: float=1.0, Specifies the threshold at which
to change between delta-scaled L1 and L2 loss.  
 `q`: float, between 0
and 1. The slope of the quantile loss, in the context of quantile
regression, the q determines the conditional quantile level.  

`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 [Huber Peter, J (1964). “Robust Estimation of a
Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)  

[Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2915)
### [​](#huberqloss-call)HuberQLoss.__call__


> CopyAsk AI HuberQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                       y_insample:torch.Tensor,
>                       mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  
 `huber_qloss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/huber_qloss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=4f51acd268108c2f53904b76846f181e)
## [​](#huberized-mqloss)Huberized MQLoss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2946)
### [​](#hubermqloss-init)HuberMQLoss.__init__


> CopyAsk AI HuberMQLoss.__init__ (level=[80, 90], quantiles=None, delta:float=1.0,
>                        horizon_weight=None)


*Huberized Multi-Quantile loss
The Huberized Multi-Quantile loss (HuberMQL) is a modified version of
the multi-quantile loss function that combines the advantages of the
quantile loss and the Huber loss. HuberMQL is commonly used in
regression tasks, especially when dealing with data that contains
outliers or heavy tails. The loss function pays more attention to
under/over-estimation depending on the quantile list
[q1,q2,… ][q_{1},q_{2},\dots][q1​,q2​,…] parameter. It controls the trade-off between
robustness and prediction accuracy with the parameter δ\deltaδ.
HuberMQLδ(yτ,[y^τ(q1),...,y^τ(qn)])=1n∑qiHuberQLδ(yτ,y^τ(qi)) \mathrm{HuberMQL}_{\delta}(\mathbf{y}_{\tau},[\mathbf{\hat{y}}^{(q_{1})}_{\tau}, ... ,\hat{y}^{(q_{n})}_{\tau}]) = 
\frac{1}{n} \sum_{q_{i}} \mathrm{HuberQL}_{\delta}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q_{i})}_{\tau}) HuberMQLδ​(yτ​,[y^​τ(q1​)​,...,y^​τ(qn​)​])=n1​qi​∑​HuberQLδ​(yτ​,y^​τ(qi​)​)
**Parameters:**  
 `level`: int list [0,100]. Probability levels for
prediction intervals (Defaults median). `quantiles`: float list [0.,
1.]. Alternative to level, quantiles to estimate from y distribution.
`delta`: float=1.0, Specifies the threshold at which to change between
delta-scaled L1 and L2 loss.  
  

`horizon_weight`: Tensor of size h, weight for each timestamp of the
forecasting window.   

**References:**  
 [Huber Peter, J (1964). “Robust Estimation of a
Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)  

[Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3022)
### [​](#hubermqloss-call)HuberMQLoss.__call__


> CopyAsk AI HuberMQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                        y_insample:torch.Tensor,
>                        mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `hmqloss`: tensor (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/hmq_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=4458c07fbc5382a46e31553d60a36902)
## [​](#huberized-iqloss)Huberized IQLoss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3067)
### [​](#huberiqloss-init)HuberIQLoss.__init__


> CopyAsk AI HuberIQLoss.__init__ (cos_embedding_dim=64, concentration0=1.0,
>                        concentration1=1.0, delta=1.0, horizon_weight=None)


*Implicit Huber Quantile Loss
Computes the huberized quantile loss between `y` and `y_hat`, with the
quantile `q` provided as an input to the network. HuberIQLoss measures
the deviation of a huberized quantile forecast. By weighting the
absolute deviation in a non symmetric way, the loss pays more attention
to under or over estimation.
HuberQL(yτ,y^τ(q))=(1−q) Lδ(yτ,  y^τ(q))1{y^τ(q)≥yτ}+q Lδ(yτ,  y^τ(q))1{y^τ(q)<yτ} \mathrm{HuberQL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = 
(1-q)\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} \geq y_{\tau} \} + 
q\, L_{\delta}(y_{\tau},\; \hat{y}^{(q)}_{\tau}) \mathbb{1}\{ \hat{y}^{(q)}_{\tau} < y_{\tau} \} HuberQL(yτ​,y^​τ(q)​)=(1−q)Lδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​≥yτ​}+qLδ​(yτ​,y^​τ(q)​)1{y^​τ(q)​<yτ​}
**Parameters:**  
 `quantile_sampling`: str, default=‘uniform’,
sampling distribution used to sample the quantiles during training.
Choose from [‘uniform’, ‘beta’].   
 `horizon_weight`: Tensor of size
h, weight for each timestamp of the forecasting window.   
 `delta`:
float=1.0, Specifies the threshold at which to change between
delta-scaled L1 and L2 loss.  

**References:**  
 [Gouttes, Adèle, Kashif Rasul, Mateusz Koren,
Johannes Stephan, and Tofigh Naghibi, “Probabilistic Time Series
Forecasting with Implicit Quantile
Networks”.](http://arxiv.org/abs/2107.03743) [Huber Peter, J (1964).
“Robust Estimation of a Location Parameter”. Annals of
Statistics](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-35/issue-1/Robust-Estimation-of-a-Location-Parameter/10.1214/aoms/1177703732.full)  

[Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L2915)
### [​](#huberiqloss-call)HuberIQLoss.__call__


> CopyAsk AI HuberIQLoss.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                        y_insample:torch.Tensor,
>                        mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies datapoints to consider
in loss.  

**Returns:**  
 `huber_qloss`: tensor (single value).*
# [​](#6-others)6. Others


## [​](#accuracy)Accuracy



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3174)
### [​](#accuracy-init)Accuracy.__init__


> CopyAsk AI Accuracy.__init__ ()


*Accuracy
Computes the accuracy between categorical `y` and `y_hat`. This
evaluation metric is only meant for evalution, as it is not
differentiable.
Accuracy(yτ,y^τ)=1H∑τ=t+1t+H1{yτ==y^τ}\mathrm{Accuracy}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \mathrm{1}\{\mathbf{y}_{\tau}==\mathbf{\hat{y}}_{\tau}\}Accuracy(yτ​,y^​τ​)=H1​∑τ=t+1t+H​1{yτ​==y^​τ​}*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3203)
### [​](#accuracy-call)Accuracy.__call__


> CopyAsk AI Accuracy.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                     y_insample:torch.Tensor,
>                     mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per serie to
consider in loss.  

**Returns:**  
 `accuracy`: tensor (single value).*
## [​](#scaled-continuous-ranked-probability-score-scrps)Scaled Continuous Ranked Probability Score (sCRPS)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3228)
### [​](#scrps-init)sCRPS.__init__


> CopyAsk AI sCRPS.__init__ (level=[80, 90], quantiles=None)


*Scaled Continues Ranked Probability Score
Calculates a scaled variation of the CRPS, as proposed by Rangapuram
(2021), to measure the accuracy of predicted quantiles `y_hat` compared
to the observation `y`.
This metric averages percentual weighted absolute deviations as defined
by the quantile losses.
sCRPS(y^τ(q),yτ)=2N∑i∫01QL(y^τ(qyi,τ)q∑i∣yi,τ∣dq \mathrm{sCRPS}(\mathbf{\hat{y}}^{(q)}_{\tau}, \mathbf{y}_{\tau}) = \frac{2}{N} \sum_{i}
\int^{1}_{0}
\frac{\mathrm{QL}(\mathbf{\hat{y}}^{(q}_{\tau} y_{i,\tau})_{q}}{\sum_{i} | y_{i,\tau} |} dq sCRPS(y^​τ(q)​,yτ​)=N2​i∑​∫01​∑i​∣yi,τ​∣QL(y^​τ(q​yi,τ​)q​​dq
where y^τ(q\mathbf{\hat{y}}^{(q}_{\tau}y^​τ(q​ is the estimated quantile, and
yi,τy_{i,\tau}yi,τ​ are the target variable realizations.
**Parameters:**  
 `level`: int list [0,100]. Probability levels for
prediction intervals (Defaults median). `quantiles`: float list [0.,
1.]. Alternative to level, quantiles to estimate from y distribution.
**References:**  
 - [Gneiting, Tilmann. (2011). “Quantiles as optimal
point forecasts”. International Journal of
Forecasting.](https://www.sciencedirect.com/science/article/pii/S0169207010000063)  
 -
[Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, Zhi
Chen, Anil Gaba, Ilia Tsetlin, Robert L. Winkler. (2022). “The M5
uncertainty competition: Results, findings and conclusions”.
International Journal of
Forecasting.](https://www.sciencedirect.com/science/article/pii/S0169207021001722)  
 -
[Syama Sundar Rangapuram, Lucien D Werner, Konstantinos Benidis, Pedro
Mercado, Jan Gasthaus, Tim Januschowski. (2021). “End-to-End Learning of
Coherent Probabilistic Forecasts for Hierarchical Time Series”.
Proceedings of the 38th International Conference on Machine Learning
(ICML).](https://proceedings.mlr.press/v139/rangapuram21a.html)*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/pytorch.py#L3264)
### [​](#scrps-call)sCRPS.__call__


> CopyAsk AI sCRPS.__call__ (y:torch.Tensor, y_hat:torch.Tensor,
>                  y_insample:torch.Tensor,
>                  mask:Optional[torch.Tensor]=None)


***Parameters:**  
 `y`: tensor, Actual values.  
 `y_hat`: tensor,
Predicted values.  
 `mask`: tensor, Specifies date stamps per series
to consider in loss.  

**Returns:**  
 `scrps`: tensor (single value).*

---

## NumPy Evaluation - Nixtla
<a id="NumPy-Evaluation-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html

NeuralForecast contains a collection NumPy loss functions aimed to be used during the models' evaluation.

The most important train signal is the forecast error, which is the
difference between the observed value yτy_{\tau}yτ​ and the prediction
y^τ\hat{y}_{\tau}y^​τ​, at time yτy_{\tau}yτ​:
eτ=yτ−y^ττ∈{t+1,…,t+H}e_{\tau} = y_{\tau}-\hat{y}_{\tau} \qquad \qquad \tau \in \{t+1,\dots,t+H \}eτ​=yτ​−y^​τ​τ∈{t+1,…,t+H}
The train loss summarizes the forecast errors in different evaluation
metrics.
# [​](#1-scale-dependent-errors)1. Scale-dependent Errors


These metrics are on the same scale as the data.
## [​](#mean-absolute-error)Mean Absolute Error



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L31)
### [​](#mae)mae


> CopyAsk AI mae (y:numpy.ndarray, y_hat:numpy.ndarray,
>       weights:Optional[numpy.ndarray]=None, axis:Optional[int]=None)


*Mean Absolute Error
Calculates Mean Absolute Error between `y` and `y_hat`. MAE measures the
relative prediction accuracy of a forecasting method by calculating the
deviation of the prediction and the true value at a given time and
averages these devations over the length of the series.
MAE(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣\mathrm{MAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} |y_{\tau} - \hat{y}_{\tau}|MAE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​−y^​τ​∣
**Parameters:**  
 `y`: numpy array, Actual values.  
 `y_hat`: numpy
array, Predicted values.  
 `mask`: numpy array, Specifies date stamps
per serie to consider in loss.  

**Returns:**  

[`mae`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mae):
numpy array, (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mae_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=155a03ab35bf439a5e84d13240ffd1e8)
## [​](#mean-squared-error)Mean Squared Error



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L69)
### [​](#mse)mse


> CopyAsk AI mse (y:numpy.ndarray, y_hat:numpy.ndarray,
>       weights:Optional[numpy.ndarray]=None, axis:Optional[int]=None)


*Mean Squared Error
Calculates Mean Squared Error between `y` and `y_hat`. MSE measures the
relative prediction accuracy of a forecasting method by calculating the
squared deviation of the prediction and the true value at a given time,
and averages these devations over the length of the series.
MSE(yτ,y^τ)=1H∑τ=t+1t+H(yτ−y^τ)2\mathrm{MSE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} (y_{\tau} - \hat{y}_{\tau})^{2}MSE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​(yτ​−y^​τ​)2
**Parameters:**  
 `y`: numpy array, Actual values.  
 `y_hat`: numpy
array, Predicted values.  
 `mask`: numpy array, Specifies date stamps
per serie to consider in loss.  

**Returns:**  

[`mse`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mse):
numpy array, (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mse_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=938bc9e8bbbefece696fe397c823efd7)
## [​](#root-mean-squared-error)Root Mean Squared Error



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L107)
### [​](#rmse)rmse


> CopyAsk AI rmse (y:numpy.ndarray, y_hat:numpy.ndarray,
>        weights:Optional[numpy.ndarray]=None, axis:Optional[int]=None)


*Root Mean Squared Error
Calculates Root Mean Squared Error between `y` and `y_hat`. RMSE
measures the relative prediction accuracy of a forecasting method by
calculating the squared deviation of the prediction and the observed
value at a given time and averages these devations over the length of
the series. Finally the RMSE will be in the same scale as the original
time series so its comparison with other series is possible only if they
share a common scale. RMSE has a direct connection to the L2 norm.
RMSE(yτ,y^τ)=1H∑τ=t+1t+H(yτ−y^τ)2\mathrm{RMSE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \sqrt{\frac{1}{H} \sum^{t+H}_{\tau=t+1} (y_{\tau} - \hat{y}_{\tau})^{2}}RMSE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​(yτ​−y^​τ​)2​
**Parameters:**  
 `y`: numpy array, Actual values.  
 `y_hat`: numpy
array, Predicted values.  
 `mask`: numpy array, Specifies date stamps
per serie to consider in loss.  

**Returns:**  

[`rmse`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#rmse):
numpy array, (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/rmse_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=ce7c8abd1e08bdb3cd445d13db639aeb)
# [​](#2-percentage-errors)2. Percentage errors


These metrics are unit-free, suitable for comparisons across series.
## [​](#mean-absolute-percentage-error)Mean Absolute Percentage Error



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L138)
### [​](#mape)mape


> CopyAsk AI mape (y:numpy.ndarray, y_hat:numpy.ndarray,
>        weights:Optional[numpy.ndarray]=None, axis:Optional[int]=None)


*Mean Absolute Percentage Error
Calculates Mean Absolute Percentage Error between `y` and `y_hat`. MAPE
measures the relative prediction accuracy of a forecasting method by
calculating the percentual deviation of the prediction and the observed
value at a given time and averages these devations over the length of
the series. The closer to zero an observed value is, the higher penalty
MAPE loss assigns to the corresponding error.
MAPE(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣∣yτ∣\mathrm{MAPE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{|y_{\tau}|}MAPE(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​∣∣yτ​−y^​τ​∣​
**Parameters:**  
 `y`: numpy array, Actual values.  
 `y_hat`: numpy
array, Predicted values.  
 `mask`: numpy array, Specifies date stamps
per serie to consider in loss.  

**Returns:**  

[`mape`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mape):
numpy array, (single value).*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mape_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=15de69fb4f6f1e7300d31cf4408ccf4f)
## [​](#smape)SMAPE



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L174)
### [​](#smape-2)smape


> CopyAsk AI smape (y:numpy.ndarray, y_hat:numpy.ndarray,
>         weights:Optional[numpy.ndarray]=None, axis:Optional[int]=None)


*Symmetric Mean Absolute Percentage Error
Calculates Symmetric Mean Absolute Percentage Error between `y` and
`y_hat`. SMAPE measures the relative prediction accuracy of a
forecasting method by calculating the relative deviation of the
prediction and the observed value scaled by the sum of the absolute
values for the prediction and observed value at a given time, then
averages these devations over the length of the series. This allows the
SMAPE to have bounds between 0% and 200% which is desirable compared to
normal MAPE that may be undetermined when the target is zero.
sMAPE2(yτ,y^τ)=1H∑τ=t+1t+H∣yτ−y^τ∣∣yτ∣+∣y^τ∣\mathrm{sMAPE}_{2}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{|y_{\tau}|+|\hat{y}_{\tau}|}sMAPE2​(yτ​,y^​τ​)=H1​∑τ=t+1t+H​∣yτ​∣+∣y^​τ​∣∣yτ​−y^​τ​∣​
**Parameters:**  
 `y`: numpy array, Actual values.  
 `y_hat`: numpy
array, Predicted values.  
 `mask`: numpy array, Specifies date stamps
per serie to consider in loss.  

**Returns:**  

[`smape`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#smape):
numpy array, (single value).
**References:**  
 [Makridakis S., “Accuracy measures: theoretical and
practical
concerns”.](https://www.sciencedirect.com/science/article/pii/0169207093900793)*
# [​](#3-scale-independent-errors)3. Scale-independent Errors


These metrics measure the relative improvements versus baselines.
## [​](#mean-absolute-scaled-error)Mean Absolute Scaled Error



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L220)
### [​](#mase)mase


> CopyAsk AI mase (y:numpy.ndarray, y_hat:numpy.ndarray, y_train:numpy.ndarray,
>        seasonality:int, weights:Optional[numpy.ndarray]=None,
>        axis:Optional[int]=None)


*Mean Absolute Scaled Error Calculates the Mean Absolute Scaled Error
between `y` and `y_hat`. MASE measures the relative prediction accuracy
of a forecasting method by comparinng the mean absolute errors of the
prediction and the observed value against the mean absolute errors of
the seasonal naive model. The MASE partially composed the Overall
Weighted Average (OWA), used in the M4 Competition.
MASE(yτ,y^τ,y^τseason)=1H∑τ=t+1t+H∣yτ−y^τ∣MAE(yτ,y^τseason)\mathrm{MASE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}, \mathbf{\hat{y}}^{season}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{\mathrm{MAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{season}_{\tau})}MASE(yτ​,y^​τ​,y^​τseason​)=H1​∑τ=t+1t+H​MAE(yτ​,y^​τseason​)∣yτ​−y^​τ​∣​
**Parameters:**  
 `y`: numpy array, (batch_size, output_size), Actual
values.  
 `y_hat`: numpy array, (batch_size, output_size)), Predicted
values.  
 `y_insample`: numpy array, (batch_size, input_size), Actual
insample Seasonal Naive predictions.  
 `seasonality`: int. Main
frequency of the time series; Hourly 24, Daily 7, Weekly 52, Monthly 12,
Quarterly 4, Yearly 1.  

`mask`: numpy array, Specifies date stamps per serie to consider in
loss.  

**Returns:**  

[`mase`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mase):
numpy array, (single value).
**References:**  
 [Rob J. Hyndman, & Koehler, A. B. “Another look at
measures of forecast
accuracy”.](https://www.sciencedirect.com/science/article/pii/S0169207006000239)  

[Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, “The
M4 Competition: 100,000 time series and 61 forecasting
methods”.](https://www.sciencedirect.com/science/article/pii/S0169207019301128)*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mase_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=9cba699ceb4b7ff7b2b9c553207379b9)
## [​](#relative-mean-absolute-error)Relative Mean Absolute Error



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L264)
### [​](#rmae)rmae


> CopyAsk AI rmae (y:numpy.ndarray, y_hat1:numpy.ndarray, y_hat2:numpy.ndarray,
>        weights:Optional[numpy.ndarray]=None, axis:Optional[int]=None)


*RMAE
Calculates Relative Mean Absolute Error (RMAE) between two sets of
forecasts (from two different forecasting methods). A number smaller
than one implies that the forecast in the numerator is better than the
forecast in the denominator.
rMAE(yτ,y^τ,y^τbase)=1H∑τ=t+1t+H∣yτ−y^τ∣MAE(yτ,y^τbase)\mathrm{rMAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}_{\tau}, \mathbf{\hat{y}}^{base}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \frac{|y_{\tau}-\hat{y}_{\tau}|}{\mathrm{MAE}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{base}_{\tau})}rMAE(yτ​,y^​τ​,y^​τbase​)=H1​∑τ=t+1t+H​MAE(yτ​,y^​τbase​)∣yτ​−y^​τ​∣​
**Parameters:**  
 `y`: numpy array, observed values.  
 `y_hat1`:
numpy array. Predicted values of first model.  
 `y_hat2`: numpy array.
Predicted values of baseline model.  
 `weights`: numpy array,
optional. Weights for weighted average.  
 `axis`: None or int,
optional.Axis or axes along which to average a.  
 The default,
axis=None, will average over all of the elements of the input array.
**Returns:**  

[`rmae`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#rmae):
numpy array or double.
**References:**  
 [Rob J. Hyndman, & Koehler, A. B. “Another look at
measures of forecast
accuracy”.](https://www.sciencedirect.com/science/article/pii/S0169207006000239)*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/rmae_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=f7a6b0e0d637dd8c9e5e4a201e2185bb)
# [​](#4-probabilistic-errors)4. Probabilistic Errors


These measure absolute deviation non-symmetrically, that produce
under/over estimation.
## [​](#quantile-loss)Quantile Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L302)
### [​](#quantile-loss-2)quantile_loss


> CopyAsk AI quantile_loss (y:numpy.ndarray, y_hat:numpy.ndarray, q:float=0.5,
>                 weights:Optional[numpy.ndarray]=None,
>                 axis:Optional[int]=None)


*Quantile Loss
Computes the quantile loss between `y` and `y_hat`. QL measures the
deviation of a quantile forecast. By weighting the absolute deviation in
a non symmetric way, the loss pays more attention to under or over
estimation. A common value for q is 0.5 for the deviation from the
median (Pinball loss).
QL(yτ,y^τ(q))=1H∑τ=t+1t+H((1−q) (y^τ(q)−yτ)++q (yτ−y^τ(q))+)\mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q)}_{\tau}) = \frac{1}{H} \sum^{t+H}_{\tau=t+1} \Big( (1-q)\,( \hat{y}^{(q)}_{\tau} - y_{\tau} )_{+} + q\,( y_{\tau} - \hat{y}^{(q)}_{\tau} )_{+} \Big)QL(yτ​,y^​τ(q)​)=H1​∑τ=t+1t+H​((1−q)(y^​τ(q)​−yτ​)+​+q(yτ​−y^​τ(q)​)+​)
**Parameters:**  
 `y`: numpy array, Actual values.  
 `y_hat`: numpy
array, Predicted values.  
 `q`: float, between 0 and 1. The slope of
the quantile loss, in the context of quantile regression, the q
determines the conditional quantile level.  
 `mask`: numpy array,
Specifies date stamps per serie to consider in loss.  

**Returns:**  

[`quantile_loss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#quantile_loss):
numpy array, (single value).
**References:**  
 [Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/q_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=426c786498233e8b1f59f960b46b4391)
## [​](#multi-quantile-loss)Multi-Quantile Loss



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/losses/numpy.py#L346)
### [​](#mqloss)mqloss


> CopyAsk AI mqloss (y:numpy.ndarray, y_hat:numpy.ndarray, quantiles:numpy.ndarray,
>          weights:Optional[numpy.ndarray]=None, axis:Optional[int]=None)


*Multi-Quantile loss
Calculates the Multi-Quantile loss (MQL) between `y` and `y_hat`. MQL
calculates the average multi-quantile Loss for a given set of quantiles,
based on the absolute difference between predicted quantiles and
observed values.
MQL(yτ,[y^τ(q1),...,y^τ(qn)])=1n∑qiQL(yτ,y^τ(qi))\mathrm{MQL}(\mathbf{y}_{\tau},[\mathbf{\hat{y}}^{(q_{1})}_{\tau}, ... ,\hat{y}^{(q_{n})}_{\tau}]) = \frac{1}{n} \sum_{q_{i}} \mathrm{QL}(\mathbf{y}_{\tau}, \mathbf{\hat{y}}^{(q_{i})}_{\tau})MQL(yτ​,[y^​τ(q1​)​,...,y^​τ(qn​)​])=n1​∑qi​​QL(yτ​,y^​τ(qi​)​)
The limit behavior of MQL allows to measure the accuracy of a full
predictive distribution F^τ\mathbf{\hat{F}}_{\tau}F^τ​ with the continuous
ranked probability score (CRPS). This can be achieved through a
numerical integration technique, that discretizes the quantiles and
treats the CRPS integral with a left Riemann approximation, averaging
over uniformly distanced quantiles.
CRPS(yτ,F^τ)=∫01QL(yτ,y^τ(q))dq\mathrm{CRPS}(y_{\tau}, \mathbf{\hat{F}}_{\tau}) = \int^{1}_{0} \mathrm{QL}(y_{\tau}, \hat{y}^{(q)}_{\tau}) dqCRPS(yτ​,F^τ​)=∫01​QL(yτ​,y^​τ(q)​)dq
**Parameters:**  
 `y`: numpy array, Actual values.  
 `y_hat`: numpy
array, Predicted values.  
 `quantiles`: numpy array,(n_quantiles).
Quantiles to estimate from the distribution of y.  
 `mask`: numpy
array, Specifies date stamps per serie to consider in loss.  

**Returns:**  

[`mqloss`](https://nixtlaverse.nixtla.io/neuralforecast/losses.numpy.html#mqloss):
numpy array, (single value).
**References:**  
 [Roger Koenker and Gilbert Bassett, Jr., “Regression
Quantiles”.](https://www.jstor.org/stable/1913643)  
 [James E.
Matheson and Robert L. Winkler, “Scoring Rules for Continuous
Probability Distributions”.](https://www.jstor.org/stable/2629907)*
![](https://mintcdn.com/nixtla/ldwvWbCUC65OBWwN/neuralforecast/imgs_losses/mq_loss.png?fit=max&auto=format&n=ldwvWbCUC65OBWwN&q=85&s=18abc02ceb1f6910df7ab34f03948914)
# [​](#examples-and-validation)Examples and Validation


CopyAsk AI```
import unittest
import torch as t 
import numpy as np

from neuralforecast.losses.pytorch import (
    MAE, MSE, RMSE,      # unscaled errors
    MAPE, SMAPE,         # percentage errors
    MASE,                # scaled error
    QuantileLoss, MQLoss # probabilistic errors
)

from neuralforecast.losses.numpy import (
    mae, mse, rmse,              # unscaled errors
    mape, smape,                 # percentage errors
    mase,                        # scaled error
    quantile_loss, mqloss        # probabilistic errors
)
```

---

## Hyperparameter Optimization - Nixtla
<a id="Hyperparameter-Optimization-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/common.base_auto.html

Machine Learning forecasting methods are defined by many hyperparameters that control their behavior, with effects ranging from their speed and memory requirements to their predictive performance. For a long time, manual hyperparameter tuning prevailed. This approach is time-consuming, **automated hyperparameter optimization** methods have been introduced, proving more efficient than manual tuning, grid search, and random search.<br/><br/> The `BaseAuto` class offers shared API connections to hyperparameter optimization algorithms like [Optuna](https://docs.ray.io/en/latest/tune/examples/bayesopt_example.html), [HyperOpt](https://docs.ray.io/en/latest/tune/examples/hyperopt_example.html), [Dragonfly](https://docs.ray.io/en/releases-2.7.0/tune/examples/dragonfly_example.html) among others through `ray`, which gives you access to grid search, bayesian optimization and other state-of-the-art tools like hyperband.<br/><br/>Comprehending the impacts of hyperparameters is still a precious skill, as it can help guide the design of informed hyperparameter spaces that are faster to explore automatically.

### [​](#baseauto)BaseAuto


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
For optuna see [https://optuna.readthedocs.io/en/stable/reference/samplers/index.html](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html).num_samplesint10Number of hyperparameter optimization steps/samples.cpusint4Number of cpus to use during optimization. Only used with ray tune.gpusint0Number of gpus to use during optimization, default all available. Only used with ray tune.refit_with_valboolFalseRefit of best model should preserve val_size.verboseboolFalseTrack progress.aliasNoneTypeNoneCustom name of the model.backendstrrayBackend to use for searching the hyperparameter space, can be either ‘ray’ or ‘optuna’.callbacksNoneTypeNoneList of functions to call during the optimization process.  
ray reference: [https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html](https://docs.ray.io/en/latest/tune/tutorials/tune-metrics.html)  
optuna reference: [https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html)

### [​](#baseauto-fit)BaseAuto.fit


> CopyAsk AI BaseAuto.fit (dataset, val_size=0, test_size=0, random_seed=None,
>                distributed_config=None)


*BaseAuto.fit
Perform the hyperparameter optimization as specified by the BaseAuto
configuration dictionary `config`.
The optimization is performed on the
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset)
using temporal cross validation with the validation set that
sequentially precedes the test set.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset)
see details
[here](https://nixtla.github.io/neuralforecast/tsdataset.html)  

`val_size`: int, size of temporal validation set (needs to be bigger
than 0).  
 `test_size`: int, size of temporal test set (default
0).  
 `random_seed`: int=None, random_seed for hyperparameter
exploration algorithms, not yet implemented.  
 **Returns:**  

`self`: fitted instance of `BaseAuto` with best hyperparameters and
results  
.*

### [​](#baseauto-predict)BaseAuto.predict


> CopyAsk AI BaseAuto.predict (dataset, step_size=1, **data_kwargs)


*BaseAuto.predict
Predictions of the best performing model on validation.
**Parameters:**  
 `dataset`: NeuralForecast’s
[`TimeSeriesDataset`](https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html#timeseriesdataset)
see details
[here](https://nixtla.github.io/neuralforecast/tsdataset.html)  

`step_size`: int, steps between sequential predictions, (default 1).  

`**data_kwarg`: additional parameters for the dataset module.  

`random_seed`: int=None, random_seed for hyperparameter exploration
algorithms (not implemented).  
 **Returns:**  
 `y_hat`: numpy
predictions of the
[`NeuralForecast`](https://nixtlaverse.nixtla.io/neuralforecast/core.html#neuralforecast)
model.  
*
CopyAsk AI```
class RayLogLossesCallback(tune.Callback):
    def on_trial_complete(self, iteration, trials, trial, **info):
        result = trial.last_result
        print(40 * '-' + 'Trial finished' + 40 * '-')
        print(f'Train loss: {result["train_loss"]:.2f}. Valid loss: {result["loss"]:.2f}')
        print(80 * '-')
```


CopyAsk AI```
config = {
    "hidden_size": tune.choice([512]),
    "num_layers": tune.choice([3, 4]),
    "input_size": 12,
    "max_steps": 10,
    "val_check_steps": 5
}
auto = BaseAuto(h=12, loss=MAE(), valid_loss=MSE(), cls_model=MLP, config=config, num_samples=2, cpus=1, gpus=0, callbacks=[RayLogLossesCallback()])
auto.fit(dataset=dataset)
y_hat = auto.predict(dataset=dataset)
assert mae(Y_test_df['y'].values, y_hat[:, 0]) < 200
```


CopyAsk AI```
def config_f(trial):
    return {
        "hidden_size": trial.suggest_categorical('hidden_size', [512]),
        "num_layers": trial.suggest_categorical('num_layers', [3, 4]),
        "input_size": 12,
        "max_steps": 10,
        "val_check_steps": 5
    }

class OptunaLogLossesCallback:
    def __call__(self, study, trial):
        metrics = trial.user_attrs['METRICS']
        print(40 * '-' + 'Trial finished' + 40 * '-')
        print(f'Train loss: {metrics["train_loss"]:.2f}. Valid loss: {metrics["loss"]:.2f}')
        print(80 * '-')
```


CopyAsk AI```
auto2 = BaseAuto(h=12, loss=MAE(), valid_loss=MSE(), cls_model=MLP, config=config_f, search_alg=optuna.samplers.RandomSampler(), num_samples=2, backend='optuna', callbacks=[OptunaLogLossesCallback()])
auto2.fit(dataset=dataset)
assert isinstance(auto2.results, optuna.Study)
y_hat2 = auto2.predict(dataset=dataset)
assert mae(Y_test_df['y'].values, y_hat2[:, 0]) < 200
```


### [​](#references)References


- [James Bergstra, Remi Bardenet, Yoshua Bengio, and Balazs Kegl
(2011). “Algorithms for Hyper-Parameter Optimization”. In: Advances
in Neural Information Processing Systems. url:
https://proceedings.neurips.cc/paper/2011/file/86e8f7ab32cfd12577bc2619bc635690-Paper.pdf](https://proceedings.neurips.cc/paper/2011/file/86e8f7ab32cfd12577bc2619bc635690-Paper.pdf)
- [Kirthevasan Kandasamy, Karun Raju Vysyaraju, Willie Neiswanger,
Biswajit Paria, Christopher R. Collins, Jeff Schneider, Barnabas
Poczos, Eric P. Xing (2019). “Tuning Hyperparameters without Grad
Students: Scalable and Robust Bayesian Optimisation with Dragonfly”.
Journal of Machine Learning Research. url:
https://arxiv.org/abs/1903.06694](https://arxiv.org/abs/1903.06694)
- [Lisha Li, Kevin Jamieson, Giulia DeSalvo, Afshin Rostamizadeh,
Ameet Talwalkar (2016). “Hyperband: A Novel Bandit-Based Approach to
Hyperparameter Optimization”. Journal of Machine Learning Research.
url:
https://arxiv.org/abs/1603.06560](https://arxiv.org/abs/1603.06560)

---

## TemporalNorm - Nixtla
<a id="TemporalNorm-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/common.scalers.html

Temporal normalization has proven to be essential in neural forecasting tasks, as it enables network's non-linearities to express themselves. Forecasting scaling methods take particular interest in the temporal dimension where most of the variance dwells, contrary to other deep learning techniques like `BatchNorm` that normalizes across batch and temporal dimensions, and `LayerNorm` that normalizes across the feature dimension. Currently we support the following techniques: `std`, `median`, `norm`, `norm1`, `invariant`, `revin`.

## [​](#references)References


- [Kin G. Olivares, David Luo, Cristian Challu, Stefania La Vattiata,
Max Mergenthaler, Artur Dubrawski (2023). “HINT: Hierarchical
Mixture Networks For Coherent Probabilistic Forecasting”. Neural
Information Processing Systems, submitted. Working Paper version
available at arxiv.](https://arxiv.org/abs/2305.07089)
- [Taesung Kim and Jinhee Kim and Yunwon Tae and Cheonbok Park and
Jang-Ho Choi and Jaegul Choo. “Reversible Instance Normalization for
Accurate Time-Series Forecasting against Distribution Shift”. ICLR
2022.](https://openreview.net/pdf?id=cGDAkQo1C0p)
- [David Salinas, Valentin Flunkert, Jan Gasthaus, Tim Januschowski
(2020). “DeepAR: Probabilistic forecasting with autoregressive
recurrent networks”. International Journal of
Forecasting.](https://www.sciencedirect.com/science/article/pii/S0169207019301888)


 
# [​](#1-auxiliary-functions)1. Auxiliary Functions



### [​](#masked-median)masked_median


> CopyAsk AI masked_median (x, mask, dim=-1, keepdim=True)


*Masked Median
Compute the median of tensor `x` along dim, ignoring values where `mask`
is False. `x` and `mask` need to be broadcastable.
**Parameters:**  
 `x`: torch.Tensor to compute median of along `dim`
dimension.  
 `mask`: torch Tensor bool with same shape as `x`, where
`x` is valid and False where `x` should be masked. Mask should not be
all False in any column of dimension dim to avoid NaNs from zero
division.  
 `dim` (int, optional): Dimension to take median of.
Defaults to -1.  
 `keepdim` (bool, optional): Keep dimension of `x` or
not. Defaults to True.  

**Returns:**  
 `x_median`: torch.Tensor with normalized values.*

### [​](#masked-mean)masked_mean


> CopyAsk AI masked_mean (x, mask, dim=-1, keepdim=True)


*Masked Mean
Compute the mean of tensor `x` along dimension, ignoring values where
`mask` is False. `x` and `mask` need to be broadcastable.
**Parameters:**  
 `x`: torch.Tensor to compute mean of along `dim`
dimension.  
 `mask`: torch Tensor bool with same shape as `x`, where
`x` is valid and False where `x` should be masked. Mask should not be
all False in any column of dimension dim to avoid NaNs from zero
division.  
 `dim` (int, optional): Dimension to take mean of. Defaults
to -1.  
 `keepdim` (bool, optional): Keep dimension of `x` or not.
Defaults to True.  

**Returns:**  
 `x_mean`: torch.Tensor with normalized values.*
# [​](#2-scalers)2. Scalers



### [​](#minmax-statistics)minmax_statistics


> CopyAsk AI minmax_statistics (x, mask, eps=1e-06, dim=-1)


*MinMax Scaler
Standardizes temporal features by ensuring its range dweels between
[0,1] range. This transformation is often used as an alternative to
the standard scaler. The scaled features are obtained as:
z=(x[B,T,C]−min(x)[B,1,C])/(max(x)[B,1,C]−min(x)[B,1,C])
\mathbf{z} = (\mathbf{x}_{[B,T,C]}-\mathrm{min}({\mathbf{x}})_{[B,1,C]})/
    (\mathrm{max}({\mathbf{x}})_{[B,1,C]}- \mathrm{min}({\mathbf{x}})_{[B,1,C]})
z=(x[B,T,C]​−min(x)[B,1,C]​)/(max(x)[B,1,C]​−min(x)[B,1,C]​)
**Parameters:**  
 `x`: torch.Tensor input tensor.  
 `mask`: torch
Tensor bool, same dimension as `x`, indicates where `x` is valid and
False where `x` should be masked. Mask should not be all False in any
column of dimension dim to avoid NaNs from zero division.  
 `eps`
(float, optional): Small value to avoid division by zero. Defaults to
1e-6.  
 `dim` (int, optional): Dimension over to compute min and max.
Defaults to -1.  

**Returns:**  
 `z`: torch.Tensor same shape as `x`, except scaled.*

### [​](#minmax1-statistics)minmax1_statistics


> CopyAsk AI minmax1_statistics (x, mask, eps=1e-06, dim=-1)


*MinMax1 Scaler
Standardizes temporal features by ensuring its range dweels between
[-1,1] range. This transformation is often used as an alternative to
the standard scaler or classic Min Max Scaler. The scaled features are
obtained as:
z=2(x[B,T,C]−min(x)[B,1,C])/(max(x)[B,1,C]−min(x)[B,1,C])−1\mathbf{z} = 2 (\mathbf{x}_{[B,T,C]}-\mathrm{min}({\mathbf{x}})_{[B,1,C]})/ (\mathrm{max}({\mathbf{x}})_{[B,1,C]}- \mathrm{min}({\mathbf{x}})_{[B,1,C]})-1z=2(x[B,T,C]​−min(x)[B,1,C]​)/(max(x)[B,1,C]​−min(x)[B,1,C]​)−1
**Parameters:**  
 `x`: torch.Tensor input tensor.  
 `mask`: torch
Tensor bool, same dimension as `x`, indicates where `x` is valid and
False where `x` should be masked. Mask should not be all False in any
column of dimension dim to avoid NaNs from zero division.  
 `eps`
(float, optional): Small value to avoid division by zero. Defaults to
1e-6.  
 `dim` (int, optional): Dimension over to compute min and max.
Defaults to -1.  

**Returns:**  
 `z`: torch.Tensor same shape as `x`, except scaled.*

### [​](#std-statistics)std_statistics


> CopyAsk AI std_statistics (x, mask, dim=-1, eps=1e-06)


*Standard Scaler
Standardizes features by removing the mean and scaling to unit variance
along the `dim` dimension.
For example, for `base_windows` models, the scaled features are obtained
as (with dim=1):
z=(x[B,T,C]−xˉ[B,1,C])/σ^[B,1,C]\mathbf{z} = (\mathbf{x}_{[B,T,C]}-\bar{\mathbf{x}}_{[B,1,C]})/\hat{\sigma}_{[B,1,C]}z=(x[B,T,C]​−xˉ[B,1,C]​)/σ^[B,1,C]​
**Parameters:**  
 `x`: torch.Tensor.  
 `mask`: torch Tensor bool,
same dimension as `x`, indicates where `x` is valid and False where `x`
should be masked. Mask should not be all False in any column of
dimension dim to avoid NaNs from zero division.  
 `eps` (float,
optional): Small value to avoid division by zero. Defaults to 1e-6.  

`dim` (int, optional): Dimension over to compute mean and std. Defaults
to -1.  

**Returns:**  
 `z`: torch.Tensor same shape as `x`, except scaled.*

### [​](#robust-statistics)robust_statistics


> CopyAsk AI robust_statistics (x, mask, dim=-1, eps=1e-06)


*Robust Median Scaler
Standardizes features by removing the median and scaling with the mean
absolute deviation (mad) a robust estimator of variance. This scaler is
particularly useful with noisy data where outliers can heavily influence
the sample mean / variance in a negative way. In these scenarios the
median and amd give better results.
For example, for `base_windows` models, the scaled features are obtained
as (with dim=1):
z=(x[B,T,C]−median(x)[B,1,C])/mad(x)[B,1,C]\mathbf{z} = (\mathbf{x}_{[B,T,C]}-\textrm{median}(\mathbf{x})_{[B,1,C]})/\textrm{mad}(\mathbf{x})_{[B,1,C]}z=(x[B,T,C]​−median(x)[B,1,C]​)/mad(x)[B,1,C]​
mad(x)=1N∑∣x−median(x)∣\textrm{mad}(\mathbf{x}) = \frac{1}{N} \sum_{}|\mathbf{x} - \mathrm{median}(x)|mad(x)=N1​∑​∣x−median(x)∣
**Parameters:**  
 `x`: torch.Tensor input tensor.  
 `mask`: torch
Tensor bool, same dimension as `x`, indicates where `x` is valid and
False where `x` should be masked. Mask should not be all False in any
column of dimension dim to avoid NaNs from zero division.  
 `eps`
(float, optional): Small value to avoid division by zero. Defaults to
1e-6.  
 `dim` (int, optional): Dimension over to compute median and
mad. Defaults to -1.  

**Returns:**  
 `z`: torch.Tensor same shape as `x`, except scaled.*

### [​](#invariant-statistics)invariant_statistics


> CopyAsk AI invariant_statistics (x, mask, dim=-1, eps=1e-06)


*Invariant Median Scaler
Standardizes features by removing the median and scaling with the mean
absolute deviation (mad) a robust estimator of variance. Aditionally it
complements the transformation with the arcsinh transformation.
For example, for `base_windows` models, the scaled features are obtained
as (with dim=1):
z=(x[B,T,C]−median(x)[B,1,C])/mad(x)[B,1,C]\mathbf{z} = (\mathbf{x}_{[B,T,C]}-\textrm{median}(\mathbf{x})_{[B,1,C]})/\textrm{mad}(\mathbf{x})_{[B,1,C]}z=(x[B,T,C]​−median(x)[B,1,C]​)/mad(x)[B,1,C]​
z=arcsinh(z)\mathbf{z} = \textrm{arcsinh}(\mathbf{z})z=arcsinh(z)
**Parameters:**  
 `x`: torch.Tensor input tensor.  
 `mask`: torch
Tensor bool, same dimension as `x`, indicates where `x` is valid and
False where `x` should be masked. Mask should not be all False in any
column of dimension dim to avoid NaNs from zero division.  
 `eps`
(float, optional): Small value to avoid division by zero. Defaults to
1e-6.  
 `dim` (int, optional): Dimension over to compute median and
mad. Defaults to -1.  

**Returns:**  
 `z`: torch.Tensor same shape as `x`, except scaled.*

### [​](#identity-statistics)identity_statistics


> CopyAsk AI identity_statistics (x, mask, dim=-1, eps=1e-06)


*Identity Scaler
A placeholder identity scaler, that is argument insensitive.
**Parameters:**  
 `x`: torch.Tensor input tensor.  
 `mask`: torch
Tensor bool, same dimension as `x`, indicates where `x` is valid and
False where `x` should be masked. Mask should not be all False in any
column of dimension dim to avoid NaNs from zero division.  
 `eps`
(float, optional): Small value to avoid division by zero. Defaults to
1e-6.  
 `dim` (int, optional): Dimension over to compute median and
mad. Defaults to -1.  

**Returns:**  
 `x`: original torch.Tensor `x`.*
# [​](#3-temporalnorm-module)3. TemporalNorm Module



### [​](#temporalnorm)TemporalNorm


> CopyAsk AI TemporalNorm (scaler_type='robust', dim=-1, eps=1e-06, num_features=None)


*Temporal Normalization
Standardization of the features is a common requirement for many machine
learning estimators, and it is commonly achieved by removing the level
and scaling its variance. The `TemporalNorm` module applies temporal
normalization over the batch of inputs as defined by the type of scaler.
z[B,T,C]=Scaler(x[B,T,C])\mathbf{z}_{[B,T,C]} = \textrm{Scaler}(\mathbf{x}_{[B,T,C]})z[B,T,C]​=Scaler(x[B,T,C]​)
If `scaler_type` is `revin` learnable normalization parameters are added
on top of the usual normalization technique, the parameters are learned
through scale decouple global skip connections. The technique is
available for point and probabilistic outputs.
z^[B,T,C]=γ^[1,1,C]z[B,T,C]+β^[1,1,C]\mathbf{\hat{z}}_{[B,T,C]} = \boldsymbol{\hat{\gamma}}_{[1,1,C]} \mathbf{z}_{[B,T,C]} +\boldsymbol{\hat{\beta}}_{[1,1,C]}z^[B,T,C]​=γ^​[1,1,C]​z[B,T,C]​+β^​[1,1,C]​
**Parameters:**  
 `scaler_type`: str, defines the type of scaler used
by TemporalNorm. Available [`identity`, `standard`, `robust`, `minmax`,
`minmax1`, `invariant`, `revin`].  
 `dim` (int, optional): Dimension
over to compute scale and shift. Defaults to -1.  
 `eps` (float,
optional): Small value to avoid division by zero. Defaults to 1e-6.  

`num_features`: int=None, for RevIN-like learnable affine parameters
initialization.  

**References**  
 - [Kin G. Olivares, David Luo, Cristian Challu,
Stefania La Vattiata, Max Mergenthaler, Artur Dubrawski (2023). “HINT:
Hierarchical Mixture Networks For Coherent Probabilistic Forecasting”.
Neural Information Processing Systems, submitted. Working Paper version
available at arxiv.](https://arxiv.org/abs/2305.07089)  
*

### [​](#temporalnorm-transform)TemporalNorm.transform


> CopyAsk AI TemporalNorm.transform (x, mask)


*Center and scale the data.
**Parameters:**  
 `x`: torch.Tensor shape [batch, time,
channels].  
 `mask`: torch Tensor bool, shape [batch, time] where
`x` is valid and False where `x` should be masked. Mask should not be
all False in any column of dimension dim to avoid NaNs from zero
division.  

**Returns:**  
 `z`: torch.Tensor same shape as `x`, except scaled.*

### [​](#temporalnorm-inverse-transform)TemporalNorm.inverse_transform


> CopyAsk AI TemporalNorm.inverse_transform (z, x_shift=None, x_scale=None)


*Scale back the data to the original representation.
**Parameters:**  
 `z`: torch.Tensor shape [batch, time, channels],
scaled.  

**Returns:**  
 `x`: torch.Tensor original data.*
# [​](#example)Example


CopyAsk AI```
import numpy as np
```


CopyAsk AI```
# Declare synthetic batch to normalize
x1 = 10**0 * np.arange(36)[:, None]
x2 = 10**1 * np.arange(36)[:, None]

np_x = np.concatenate([x1, x2], axis=1)
np_x = np.repeat(np_x[None, :,:], repeats=2, axis=0)
np_x[0,:,:] = np_x[0,:,:] + 100

np_mask = np.ones(np_x.shape)
np_mask[:, -12:, :] = 0

print(f'x.shape [batch, time, features]={np_x.shape}')
print(f'mask.shape [batch, time, features]={np_mask.shape}')
```


CopyAsk AI```
# Validate scalers
x = 1.0*torch.tensor(np_x)
mask = torch.tensor(np_mask)
scaler = TemporalNorm(scaler_type='standard', dim=1)
x_scaled = scaler.transform(x=x, mask=mask)
x_recovered = scaler.inverse_transform(x_scaled)

plt.plot(x[0,:,0], label='x1', color='#78ACA8')
plt.plot(x[0,:,1], label='x2',  color='#E3A39A')
plt.title('Before TemporalNorm')
plt.xlabel('Time')
plt.legend()
plt.show()

plt.plot(x_scaled[0,:,0], label='x1', color='#78ACA8')
plt.plot(x_scaled[0,:,1]+0.1, label='x2+0.1', color='#E3A39A')
plt.title(f'TemporalNorm \'{scaler.scaler_type}\' ')
plt.xlabel('Time')
plt.legend()
plt.show()

plt.plot(x_recovered[0,:,0], label='x1', color='#78ACA8')
plt.plot(x_recovered[0,:,1], label='x2', color='#E3A39A')
plt.title('Recovered')
plt.xlabel('Time')
plt.legend()
plt.show()
```

---

## NN Modules - Nixtla
<a id="NN-Modules-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/common.modules.html

## [​](#1-mlp)1. MLP


Multi-Layer Perceptron

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/mlp.py#L16)
### [​](#mlp)MLP


> CopyAsk AI MLP (in_features, out_features, activation, hidden_size, num_layers,
>       dropout)


*Multi-Layer Perceptron Class
**Parameters:**  
 `in_features`: int, dimension of input.  

`out_features`: int, dimension of output.  
 `activation`: str,
activation function to use.  
 `hidden_size`: int, dimension of hidden
layers.  
 `num_layers`: int, number of hidden layers.  
 `dropout`:
float, dropout rate.  
*
## [​](#2-temporal-convolutions)2. Temporal Convolutions


For long time in deep learning, sequence modelling was synonymous with
recurrent networks, yet several papers have shown that simple
convolutional architectures can outperform canonical recurrent networks
like LSTMs by demonstrating longer effective memory.
**References**  
 -[van den Oord, A., Dieleman, S., Zen, H., Simonyan,
K., Vinyals, O., Graves, A., Kalchbrenner, N., Senior, A. W., &
Kavukcuoglu, K. (2016). Wavenet: A generative model for raw audio.
Computing Research Repository, abs/1609.03499. URL:
http://arxiv.org/abs/1609.03499.
arXiv:1609.03499.](https://arxiv.org/abs/1609.03499)  
 -[Shaojie Bai,
Zico Kolter, Vladlen Koltun. (2018). An Empirical Evaluation of Generic
Convolutional and Recurrent Networks for Sequence Modeling. Computing
Research Repository, abs/1803.01271. URL:
https://arxiv.org/abs/1803.01271.](https://arxiv.org/abs/1803.01271)  


### [​](#chomp1d)Chomp1d


> CopyAsk AI Chomp1d (horizon)


*Chomp1d
Receives `x` input of dim [N,C,T], and trims it so that only ‘time
available’ information is used. Used by one dimensional causal
convolutions `CausalConv1d`.
**Parameters:**  
 `horizon`: int, length of outsample values to
skip.*

### [​](#causalconv1d)CausalConv1d


> CopyAsk AI CausalConv1d (in_channels, out_channels, kernel_size, padding, dilation,
>                activation, stride:int=1)


*Causal Convolution 1d
Receives `x` input of dim [N,C_in,T], and computes a causal
convolution in the time dimension. Skipping the H steps of the forecast
horizon, through its dilation. Consider a batch of one element, the
dilated convolution operation on the ttt time step is defined:
Conv1D(x,w)(t)=(x[∗d]w)(t)=∑k=1Kwkxt−dk\mathrm{Conv1D}(\mathbf{x},\mathbf{w})(t) = (\mathbf{x}_{[*d]} \mathbf{w})(t) = \sum^{K}_{k=1} w_{k} \mathbf{x}_{t-dk}Conv1D(x,w)(t)=(x[∗d]​w)(t)=∑k=1K​wk​xt−dk​
where ddd is the dilation factor, KKK is the kernel size, t−dkt-dkt−dk is the
index of the considered past observation. The dilation effectively
applies a filter with skip connections. If d=1d=1d=1 one recovers a normal
convolution.
**Parameters:**  
 `in_channels`: int, dimension of `x` input’s initial
channels.  
 `out_channels`: int, dimension of `x` outputs’s
channels.  
 `activation`: str, identifying activations from PyTorch
activations. select from ‘ReLU’,‘Softplus’,‘Tanh’,‘SELU’,
‘LeakyReLU’,‘PReLU’,‘Sigmoid’.  
 `padding`: int, number of zero
padding used to the left.  
 `kernel_size`: int, convolution’s kernel
size.  
 `dilation`: int, dilation skip connections.  

**Returns:**  
 `x`: tensor, torch tensor of dim [N,C_out,T]
activation(conv1d(inputs, kernel) + bias).   
*

### [​](#temporalconvolutionencoder)TemporalConvolutionEncoder


> CopyAsk AI TemporalConvolutionEncoder (in_channels, out_channels, kernel_size,
>                              dilations, activation:str='ReLU')


*Temporal Convolution Encoder
Receives `x` input of dim [N,T,C_in], permutes it to [N,C_in,T]
applies a deep stack of exponentially dilated causal convolutions. The
exponentially increasing dilations of the convolutions allow for the
creation of weighted averages of exponentially large long-term memory.
**Parameters:**  
 `in_channels`: int, dimension of `x` input’s initial
channels.  
 `out_channels`: int, dimension of `x` outputs’s
channels.  
 `kernel_size`: int, size of the convolving kernel.  

`dilations`: int list, controls the temporal spacing between the kernel
points.  
 `activation`: str, identifying activations from PyTorch
activations. select from ‘ReLU’,‘Softplus’,‘Tanh’,‘SELU’,
‘LeakyReLU’,‘PReLU’,‘Sigmoid’.  

**Returns:**  
 `x`: tensor, torch tensor of dim [N,T,C_out].  
*
## [​](#3-transformers)3. Transformers


**References**  
 - [Haoyi Zhou, Shanghang Zhang, Jieqi Peng, Shuai
Zhang, Jianxin Li, Hui Xiong, Wancai Zhang. “Informer: Beyond Efficient
Transformer for Long Sequence Time-Series
Forecasting”](https://arxiv.org/abs/2012.07436)  
 - [Haixu Wu, Jiehui
Xu, Jianmin Wang, Mingsheng Long.](https://arxiv.org/abs/2106.13008)  


### [​](#transencoder)TransEncoder


> CopyAsk AI TransEncoder (attn_layers, conv_layers=None, norm_layer=None)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#transencoderlayer)TransEncoderLayer


> CopyAsk AI TransEncoderLayer (attention, hidden_size, conv_hidden_size=None,
>                     dropout=0.1, activation='relu')


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#transdecoder)TransDecoder


> CopyAsk AI TransDecoder (layers, norm_layer=None, projection=None)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#transdecoderlayer)TransDecoderLayer


> CopyAsk AI TransDecoderLayer (self_attention, cross_attention, hidden_size,
>                     conv_hidden_size=None, dropout=0.1, activation='relu')


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#attentionlayer)AttentionLayer


> CopyAsk AI AttentionLayer (attention, hidden_size, n_heads, d_keys=None,
>                  d_values=None)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#fullattention)FullAttention


> CopyAsk AI FullAttention (mask_flag=True, factor=5, scale=None,
>                 attention_dropout=0.1, output_attention=False)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#triangularcausalmask)TriangularCausalMask


> CopyAsk AI TriangularCausalMask (B, L, device='cpu')


*TriangularCausalMask*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/softs.py#L17)
### [​](#dataembedding-inverted)DataEmbedding_inverted


> CopyAsk AI DataEmbedding_inverted (c_in, hidden_size, dropout=0.1)


*DataEmbedding_inverted*

### [​](#dataembedding)DataEmbedding


> CopyAsk AI DataEmbedding (c_in, exog_input_size, hidden_size, pos_embedding=True,
>                 dropout=0.1)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#temporalembedding)TemporalEmbedding


> CopyAsk AI TemporalEmbedding (d_model, embed_type='fixed', freq='h')


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#fixedembedding)FixedEmbedding


> CopyAsk AI FixedEmbedding (c_in, d_model)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#timefeatureembedding)TimeFeatureEmbedding


> CopyAsk AI TimeFeatureEmbedding (input_size, hidden_size)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/timellm.py#L43)
### [​](#tokenembedding)TokenEmbedding


> CopyAsk AI TokenEmbedding (c_in, hidden_size)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

### [​](#positionalembedding)PositionalEmbedding


> CopyAsk AI PositionalEmbedding (hidden_size, max_len=5000)


*Base class for all neural network modules.
Your models should also subclass this class.
Modules can also contain other Modules, allowing them to be nested in a
tree structure. You can assign the submodules as regular attributes::
CopyAsk AI```
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 20, 5)
        self.conv2 = nn.Conv2d(20, 20, 5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
```


Submodules assigned in this way will be registered, and will also have
their parameters converted when you call :meth:`to`, etc.
.. note:: As per the example above, an `__init__()` call to the parent
class must be made before assignment on the child.
:ivar training: Boolean represents whether this module is in training or
evaluation mode. :vartype training: bool*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/dlinear.py#L36)
### [​](#seriesdecomp)SeriesDecomp


> CopyAsk AI SeriesDecomp (kernel_size)


*Series decomposition block*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/models/dlinear.py#L17)
### [​](#movingavg)MovingAvg


> CopyAsk AI MovingAvg (kernel_size, stride)


*Moving average block to highlight the trend of time series*

### [​](#revin)RevIN


> CopyAsk AI RevIN (num_features:int, eps=1e-05, affine=False, subtract_last=False,
>         non_norm=False)


*RevIN (Reversible-Instance-Normalization)*

### [​](#revinmultivariate)RevINMultivariate


> CopyAsk AI RevINMultivariate (num_features:int, eps=1e-05, affine=False,
>                     subtract_last=False, non_norm=False)


*ReversibleInstanceNorm1d for Multivariate models*

---

## PyTorch Dataset/Loader - Nixtla
<a id="PyTorch-DatasetLoader-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/tsdataset.html

Torch Dataset for Time Series

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/tsdataset.py#L21)
### [​](#timeseriesloader)TimeSeriesLoader


> CopyAsk AI TimeSeriesLoader (dataset, **kwargs)


*TimeSeriesLoader DataLoader. [Source
code](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/tsdataset.py).
Small change to PyTorch’s Data loader. Combines a dataset and a sampler,
and provides an iterable over the given dataset.
The class `~torch.utils.data.DataLoader` supports both map-style and
iterable-style datasets with single- or multi-process loading,
customizing loading order and optional automatic batching (collation)
and memory pinning.
**Parameters:**  
 `batch_size`: (int, optional): how many samples per
batch to load (default: 1).  
 `shuffle`: (bool, optional): set to
`True` to have the data reshuffled at every epoch (default:
`False`).  
 `sampler`: (Sampler or Iterable, optional): defines the
strategy to draw samples from the dataset.  
 Can be any `Iterable`
with `__len__` implemented. If specified, `shuffle` must not be
specified.  
*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/tsdataset.py#L80)
### [​](#basetimeseriesdataset)BaseTimeSeriesDataset


> CopyAsk AI BaseTimeSeriesDataset (temporal_cols, max_size:int, min_size:int,
>                         y_idx:int, static=None, static_cols=None)


*An abstract class representing a :class:`Dataset`.
All datasets that represent a map from keys to data samples should
subclass it. All subclasses should overwrite :meth:`__getitem__`,
supporting fetching a data sample for a given key. Subclasses could also
optionally overwrite :meth:`__len__`, which is expected to return the
size of the dataset by many :class:`~torch.utils.data.Sampler`
implementations and the default options of
:class:`~torch.utils.data.DataLoader`. Subclasses could also optionally
implement :meth:`__getitems__`, for speedup batched samples loading.
This method accepts list of indices of samples of batch and returns list
of samples.
.. note:: :class:`~torch.utils.data.DataLoader` by default constructs an
index sampler that yields integral indices. To make it work with a
map-style dataset with non-integral indices/keys, a custom sampler must
be provided.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/tsdataset.py#L371)
### [​](#localfilestimeseriesdataset)LocalFilesTimeSeriesDataset


> CopyAsk AI LocalFilesTimeSeriesDataset (files_ds:List[str], temporal_cols,
>                               id_col:str, time_col:str, target_col:str,
>                               last_times, indices, max_size:int,
>                               min_size:int, y_idx:int, static=None,
>                               static_cols=None)


*An abstract class representing a :class:`Dataset`.
All datasets that represent a map from keys to data samples should
subclass it. All subclasses should overwrite :meth:`__getitem__`,
supporting fetching a data sample for a given key. Subclasses could also
optionally overwrite :meth:`__len__`, which is expected to return the
size of the dataset by many :class:`~torch.utils.data.Sampler`
implementations and the default options of
:class:`~torch.utils.data.DataLoader`. Subclasses could also optionally
implement :meth:`__getitems__`, for speedup batched samples loading.
This method accepts list of indices of samples of batch and returns list
of samples.
.. note:: :class:`~torch.utils.data.DataLoader` by default constructs an
index sampler that yields integral indices. To make it work with a
map-style dataset with non-integral indices/keys, a custom sampler must
be provided.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/tsdataset.py#L141)
### [​](#timeseriesdataset)TimeSeriesDataset


> CopyAsk AI TimeSeriesDataset (temporal, temporal_cols, indptr, y_idx:int,
>                     static=None, static_cols=None)


*An abstract class representing a :class:`Dataset`.
All datasets that represent a map from keys to data samples should
subclass it. All subclasses should overwrite :meth:`__getitem__`,
supporting fetching a data sample for a given key. Subclasses could also
optionally overwrite :meth:`__len__`, which is expected to return the
size of the dataset by many :class:`~torch.utils.data.Sampler`
implementations and the default options of
:class:`~torch.utils.data.DataLoader`. Subclasses could also optionally
implement :meth:`__getitems__`, for speedup batched samples loading.
This method accepts list of indices of samples of batch and returns list
of samples.
.. note:: :class:`~torch.utils.data.DataLoader` by default constructs an
index sampler that yields integral indices. To make it work with a
map-style dataset with non-integral indices/keys, a custom sampler must
be provided.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/tsdataset.py#L537)
### [​](#timeseriesdatamodule)TimeSeriesDataModule


> CopyAsk AI TimeSeriesDataModule (dataset:__main__.BaseTimeSeriesDataset,
>                        batch_size=32, valid_batch_size=1024,
>                        drop_last=False, shuffle_train=True,
>                        **dataloaders_kwargs)


*A DataModule standardizes the training, val, test splits, data
preparation and transforms. The main advantage is consistent data
splits, data preparation and transforms across models.
Example::
CopyAsk AI```
import lightning.pytorch as L
import torch.utils.data as data
from pytorch_lightning.demos.boring_classes import RandomDataset

class MyDataModule(L.LightningDataModule):
    def prepare_data(self):
        # download, IO, etc. Useful with shared filesystems
        # only called on 1 GPU/TPU in distributed
        ...

    def setup(self, stage):
        # make assignments here (val/train/test split)
        # called on every process in DDP
        dataset = RandomDataset(1, 100)
        self.train, self.val, self.test = data.random_split(
            dataset, [80, 10, 10], generator=torch.Generator().manual_seed(42)
        )

    def train_dataloader(self):
        return data.DataLoader(self.train)

    def val_dataloader(self):
        return data.DataLoader(self.val)

    def test_dataloader(self):
        return data.DataLoader(self.test)

    def on_exception(self, exception):
        # clean up state after the trainer faced an exception
        ...

    def teardown(self):
        # clean up state after the trainer stops, delete files...
        # called on every process in DDP
        ...*
```


CopyAsk AI```
# To test correct future_df wrangling of the `update_df` method
# We are checking that we are able to recover the AirPassengers dataset
# using the dataframe or splitting it into parts and initializing.
```

---

## Example Data - Nixtla
<a id="Example-Data-Nixtla"></a>

- 元URL: https://nixtlaverse.nixtla.io/neuralforecast/utils.html

The `core.NeuralForecast` class allows you to efficiently fit multiple `NeuralForecast` models for large sets of time series. It operates with pandas DataFrame `df` that identifies individual series and datestamps with the `unique_id` and `ds` columns, and the `y` column denotes the target time series variable. To assist development, we declare useful datasets that we use throughout all `NeuralForecast`'s unit tests.<br/><br/>

# [​](#1-synthetic-panel-data)1. Synthetic Panel Data



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L21)
### [​](#generate-series)generate_series


> CopyAsk AI generate_series (n_series:int, freq:str='D', min_length:int=50,
>                   max_length:int=500, n_temporal_features:int=0,
>                   n_static_features:int=0, equal_ends:bool=False,
>                   seed:int=0)


*Generate Synthetic Panel Series.
Generates `n_series` of frequency `freq` of different lengths in the
interval [`min_length`, `max_length`]. If `n_temporal_features > 0`,
then each serie gets temporal features with random values. If
`n_static_features > 0`, then a static dataframe is returned along the
temporal dataframe. If `equal_ends == True` then all series end at the
same date.
**Parameters:**  
 `n_series`: int, number of series for synthetic
panel.  
 `min_length`: int, minimal length of synthetic panel’s
series.  
 `max_length`: int, minimal length of synthetic panel’s
series.  
 `n_temporal_features`: int, default=0, number of temporal
exogenous variables for synthetic panel’s series.  

`n_static_features`: int, default=0, number of static exogenous
variables for synthetic panel’s series.  
 `equal_ends`: bool, if True,
series finish in the same date stamp `ds`.  
 `freq`: str, frequency of
the data, [panda’s available
frequencies](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases).  

**Returns:**  
 `freq`: pandas.DataFrame, synthetic panel with columns
[`unique_id`, `ds`, `y`] and exogenous.*
CopyAsk AI```
synthetic_panel = generate_series(n_series=2)
synthetic_panel.groupby('unique_id').head(4)
```


CopyAsk AI```
temporal_df, static_df = generate_series(n_series=1000, n_static_features=2,
                                         n_temporal_features=4, equal_ends=False)
static_df.head(2)
```


# [​](#2-airpassengers-data)2. AirPassengers Data


The classic Box & Jenkins airline data. Monthly totals of international
airline passengers, 1949 to 1960.
It has been used as a reference on several forecasting libraries, since
it is a series that shows clear trends and seasonalities it offers a
nice opportunity to quickly showcase a model’s predictions performance.
CopyAsk AI```
AirPassengersDF.head(12)
```


CopyAsk AI```
#We are going to plot the ARIMA predictions, and the prediction intervals.
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
plot_df = AirPassengersDF.set_index('ds')

plot_df[['y']].plot(ax=ax, linewidth=2)
ax.set_title('AirPassengers Forecast', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Timestamp [t]', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```


CopyAsk AI```
import numpy as np
import pandas as pd
```


CopyAsk AI```
n_static_features = 3
n_series = 5

static_features = np.random.uniform(low=0.0, high=1.0, 
                        size=(n_series, n_static_features))
static_df = pd.DataFrame.from_records(static_features, 
                   columns = [f'static_{i}'for i in  range(n_static_features)])
static_df['unique_id'] = np.arange(n_series)
```


CopyAsk AI```
static_df
```


# [​](#3-panel-airpassengers-data)3. Panel AirPassengers Data


Extension to classic Box & Jenkins airline data. Monthly totals of
international airline passengers, 1949 to 1960.
It includes two series with static, temporal and future exogenous
variables, that can help to explore the performance of models like
[`NBEATSx`](https://nixtlaverse.nixtla.io/neuralforecast/models.nbeatsx.html#nbeatsx)
and
[`TFT`](https://nixtlaverse.nixtla.io/neuralforecast/models.tft.html#tft).
CopyAsk AI```
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
plot_df = AirPassengersPanel.set_index('ds')

plot_df.groupby('unique_id')['y'].plot(legend=True)
ax.set_title('AirPassengers Panel Data', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Timestamp [t]', fontsize=20)
ax.legend(title='unique_id', prop={'size': 15})
ax.grid()
```


CopyAsk AI```
fig, ax = plt.subplots(1, 1, figsize = (20, 7))
plot_df = AirPassengersPanel[AirPassengersPanel.unique_id=='Airline1'].set_index('ds')

plot_df[['y', 'trend', 'y_[lag12]']].plot(ax=ax, linewidth=2)
ax.set_title('Box-Cox AirPassengers Data', fontsize=22)
ax.set_ylabel('Monthly Passengers', fontsize=20)
ax.set_xlabel('Timestamp [t]', fontsize=20)
ax.legend(prop={'size': 15})
ax.grid()
```


# [​](#4-time-features)4. Time Features


We have developed a utility that generates normalized calendar features
for use as absolute positional embeddings in Transformer-based models.
These embeddings capture seasonal patterns in time series data and can
be easily incorporated into the model architecture. Additionally, the
features can be used as exogenous variables in other models to inform
them of calendar patterns in the data.
**References**  
 - [Haoyi Zhou, Shanghang Zhang, Jieqi Peng, Shuai
Zhang, Jianxin Li, Hui Xiong, Wancai Zhang. “Informer: Beyond Efficient
Transformer for Long Sequence Time-Series
Forecasting”](https://arxiv.org/abs/2012.07436)  


[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L404)
### [​](#augment-calendar-df)augment_calendar_df


> CopyAsk AI augment_calendar_df (df, freq='H')


*> * Q - [month] > * M - [month] > * W - [Day of month, week
of year] > * D - [Day of week, day of month, day of year] > * B -
[Day of week, day of month, day of year] > * H - [Hour of day, day
of week, day of month, day of year] > * T - [Minute of hour*, hour
of day, day of week, day of month, day of year] > * S - [Second of
minute, minute of hour, hour of day, day of week, day of month, day of
year] *minute returns a number from 0-3 corresponding to the 15 minute
period it falls into.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L366)
### [​](#time-features-from-frequency-str)time_features_from_frequency_str


> CopyAsk AI time_features_from_frequency_str (freq_str:str)


*Returns a list of time features that will be appropriate for the given
frequency string. Parameters ———- freq_str Frequency string of the form
[multiple][granularity] such as “12H”, “5min”, “1D” etc.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L359)
### [​](#weekofyear)WeekOfYear


> CopyAsk AI WeekOfYear ()


*Week of year encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L352)
### [​](#monthofyear)MonthOfYear


> CopyAsk AI MonthOfYear ()


*Month of year encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L345)
### [​](#dayofyear)DayOfYear


> CopyAsk AI DayOfYear ()


*Day of year encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L338)
### [​](#dayofmonth)DayOfMonth


> CopyAsk AI DayOfMonth ()


*Day of month encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L331)
### [​](#dayofweek)DayOfWeek


> CopyAsk AI DayOfWeek ()


*Hour of day encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L324)
### [​](#hourofday)HourOfDay


> CopyAsk AI HourOfDay ()


*Hour of day encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L317)
### [​](#minuteofhour)MinuteOfHour


> CopyAsk AI MinuteOfHour ()


*Minute of hour encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L310)
### [​](#secondofminute)SecondOfMinute


> CopyAsk AI SecondOfMinute ()


*Minute of hour encoded as value between [-0.5, 0.5]*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L299)
### [​](#timefeature)TimeFeature


> CopyAsk AI TimeFeature ()


*Initialize self. See help(type(self)) for accurate signature.*
CopyAsk AI```
AirPassengerPanelCalendar, calendar_cols = augment_calendar_df(df=AirPassengersPanel, freq='M')
AirPassengerPanelCalendar.head()
```


CopyAsk AI```
plot_df = AirPassengerPanelCalendar[AirPassengerPanelCalendar.unique_id=='Airline1'].set_index('ds')
plt.plot(plot_df['month'])
plt.grid()
plt.xlabel('Datestamp')
plt.ylabel('Normalized Month')
plt.show()
```



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L446)
### [​](#get-indexer-raise-missing)get_indexer_raise_missing


> CopyAsk AI get_indexer_raise_missing (idx:pandas.core.indexes.base.Index,
>                             vals:List[str])


# [​](#5-prediction-intervals)5. Prediction Intervals



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L454)
### [​](#predictionintervals)PredictionIntervals


> CopyAsk AI PredictionIntervals (n_windows:int=2,
>                       method:str='conformal_distribution')


*Class for storing prediction intervals metadata information.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L485)
### [​](#add-conformal-distribution-intervals)add_conformal_distribution_intervals


> CopyAsk AI add_conformal_distribution_intervals (model_fcsts:<built-
>                                        infunctionarray>, cs_df:~DFType,
>                                        model:str, cs_n_windows:int,
>                                        n_series:int, horizon:int, level:Op
>                                        tional[List[Union[int,float]]]=None
>                                        , quantiles:Optional[List[float]]=N
>                                        one)


*Adds conformal intervals to a `fcst_df` based on conformal scores
`cs_df`. `level` should be already sorted. This strategy creates
forecasts paths based on errors and calculate quantiles using those
paths.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L535)
### [​](#add-conformal-error-intervals)add_conformal_error_intervals


> CopyAsk AI add_conformal_error_intervals (model_fcsts:<built-infunctionarray>,
>                                 cs_df:~DFType, model:str,
>                                 cs_n_windows:int, n_series:int,
>                                 horizon:int, level:Optional[List[Union[int
>                                 ,float]]]=None,
>                                 quantiles:Optional[List[float]]=None)


*Adds conformal intervals to a `fcst_df` based on conformal scores
`cs_df`. `level` should be already sorted. This startegy creates
prediction intervals based on the absolute errors.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L595)
### [​](#get-prediction-interval-method)get_prediction_interval_method


> CopyAsk AI get_prediction_interval_method (method:str)



[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L620)
### [​](#quantiles-to-level)quantiles_to_level


> CopyAsk AI quantiles_to_level (quantiles:List[float])


*Converts a list of quantiles to a list of levels.*

[source](https://github.com/Nixtla/neuralforecast/blob/main/neuralforecast/utils.py#L608)
### [​](#level-to-quantiles)level_to_quantiles


> CopyAsk AI level_to_quantiles (level:List[Union[int,float]])


*Converts a list of levels to a list of quantiles.*
