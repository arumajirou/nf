# optuna.readthedocs.io

- 抽出日時: 2025-11-12 10:56
- 件数: 2

## 目次
1. [optuna.samplers — Optuna 4.6.0 documentation](#optunasamplers-Optuna-460-documentation)
2. [Callback for Study.optimize — Optuna 4.6.0 documentation](#Callback-for-Studyoptimize-Optuna-460-documentation)


---

## optuna.samplers — Optuna 4.6.0 documentation
<a id="optunasamplers-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/index.html

# optuna.samplers[](#optuna-samplers)


The [`samplers`](#module-optuna.samplers) module defines a base class for parameter sampling as described extensively in [`BaseSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler). The remaining classes in this module represent child classes, deriving from [`BaseSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler), which implement different sampling strategies.



See also


[Efficient Optimization Algorithms](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/003_efficient_optimization_algorithms.html#pruning) tutorial explains the overview of the sampler classes.




See also


[User-Defined Sampler](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/005_user_defined_sampler.html#user-defined-sampler) tutorial could be helpful if you want to implement your own sampler classes.




See also


If you are unsure about which sampler to use, please consider using [AutoSampler](https://hub.optuna.org/samplers/auto_sampler/), which automatically selects a sampler during optimization. For more detail, see [the article on AutoSampler](https://medium.com/optuna/autosampler-automatic-selection-of-optimization-algorithms-in-optuna-1443875fd8f9).






[`AutoSampler`](https://hub.optuna.org/samplers/auto_sampler/)


[`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler)


[`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler)


[`GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html#optuna.samplers.GPSampler)


[`CmaEsSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html#optuna.samplers.CmaEsSampler)


[`NSGAIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html#optuna.samplers.NSGAIISampler)


[`NSGAIIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIIISampler.html#optuna.samplers.NSGAIIISampler)


[`GridSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GridSampler.html#optuna.samplers.GridSampler)


[`QMCSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.QMCSampler.html#optuna.samplers.QMCSampler)


[`BoTorchSampler`](https://optuna-integration.readthedocs.io/en/latest/reference/generated/optuna_integration.BoTorchSampler.html#optuna_integration.BoTorchSampler)


[`BruteForceSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BruteForceSampler.html#optuna.samplers.BruteForceSampler)





Float parameters


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\) (\(\color{red}\times\) for infinite domain)



Integer parameters


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\color{green}\checkmark\)



Categorical parameters


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\color{green}\checkmark\)



Pruning


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\color{red}\times\) (\(\blacktriangle\) for single-objective)


\(\color{red}\times\) (\(\blacktriangle\) for single-objective)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\color{green}\checkmark\)



Multivariate optimization


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\blacktriangle\)



Conditional search space


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\blacktriangle\)


\(\color{green}\checkmark\)



Multi-objective optimization


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{red}\times\)


\(\color{green}\checkmark\) (\(\blacktriangle\) for single-objective)


\(\color{green}\checkmark\) (\(\blacktriangle\) for single-objective)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)



Batch optimization


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)



Distributed optimization


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\blacktriangle\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)



Constrained optimization


\(\color{green}\checkmark\)


\(\color{red}\times\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{red}\times\)


\(\color{green}\checkmark\)


\(\color{green}\checkmark\)


\(\color{red}\times\)


\(\color{red}\times\)


\(\color{green}\checkmark\)


\(\color{red}\times\)



Time complexity (per trial) (*)


N/A


\(O(d)\)


\(O(dn \log n)\)


\(O(n^3)\)


\(O(d^3)\)


\(O(mp^2)\) (***)


\(O(mp^2)\) (***)


\(O(dn)\)


\(O(dn)\)


\(O(n^3)\)


\(O(d)\)



Recommended budgets (#trials) (**)


as many as one likes


as many as one likes


100–1000


–500


1000–10000


100–10000


100–10000


number of combinations


as many as one likes


10–100


number of combinations






Note


\(\color{green}\checkmark\): Supports this feature.
\(\blacktriangle\): Works, but inefficiently.
\(\color{red}\times\): Causes an error, or has no interface.


> (*): We assumes that \(d\) is the dimension of the search space, \(n\) is the number of finished trials, \(m\) is the number of objectives, and \(p\) is the population size (algorithm specific parameter).
> This table shows the time complexity of the sampling algorithms. We may omit other terms that depend on the implementation in Optuna, including \(O(d)\) to call the sampling methods and \(O(n)\) to collect the completed trials.
> This means that, for example, the actual time complexity of RandomSampler is \(O(d+n+d) = O(d+n)\).
> From another perspective, with the exception of NSGAIISampler and NSGAIIISampler, all time complexity is written for single-objective optimization.
> (**): (1) The budget depends on the number of parameters and the number of objectives. (2) This budget includes n_startup_trials if a sampler has n_startup_trials as one of its arguments.
> (***): This time complexity assumes that the number of population size \(p\) and the number of parallelization are regular.
> This means that the number of parallelization should not exceed the number of population size \(p\).




Note


Samplers initialize their random number generators by specifying `seed` argument at initialization.
However, samplers reseed them when `n_jobs!=1` of [`optuna.study.Study.optimize()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.optimize) to avoid sampling duplicated parameters by using the same generator.
Thus we can hardly reproduce the optimization results with `n_jobs!=1`.
For the same reason, make sure that use either `seed=None` or different `seed` values among processes with distributed optimization explained in [Easy Parallelization](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html#distributed) tutorial.




Note


For float, integer, or categorical parameters, see [Pythonic Search Space](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html#configurations) tutorial.


For pruning, see [Efficient Optimization Algorithms](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/003_efficient_optimization_algorithms.html#pruning) tutorial.


For multivariate optimization, see [`BaseSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler). The multivariate optimization is implemented as [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative) in Optuna. Please check the concrete documents of samplers for more details.


For conditional search space, see [Pythonic Search Space](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html#configurations) tutorial and [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler). The `group` option of [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) allows [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) to handle the conditional search space.


For multi-objective optimization, see [Multi-objective Optimization with Optuna](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/002_multi_objective.html#multi-objective) tutorial.


For batch optimization, see [Batch Optimization](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html#batch-optimization) tutorial. Note that the `constant_liar` option of [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) allows [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) to handle the batch optimization.


For distributed optimization, see [Easy Parallelization](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html#distributed) tutorial. Note that the `constant_liar` option of [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) allows [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) to handle the distributed optimization.


For constrained optimization, see an [example](https://github.com/optuna/optuna-examples/blob/main/multi_objective/botorch_simple.py).





[`BaseSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler)


Base class for samplers.



[`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler)


Sampler using random sampling.



[`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler)


Sampler using TPE (Tree-structured Parzen Estimator) algorithm.



[`GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html#optuna.samplers.GPSampler)


Sampler using Gaussian process-based Bayesian optimization.



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

## Callback for Study.optimize — Optuna 4.6.0 documentation
<a id="Callback-for-Studyoptimize-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html

Note


[Go to the end](#sphx-glr-download-tutorial-20-recipes-007-optuna-callback-py)
to download the full example code.




# Callback for Study.optimize[](#callback-for-study-optimize)


This tutorial showcases how to use & implement Optuna `Callback` for [`optimize()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.optimize).


`Callback` is called after every evaluation of `objective`, and
it takes [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) and [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) as arguments, and does some work.


[MLflowCallback](https://optuna-integration.readthedocs.io/en/stable/reference/generated/optuna_integration.MLflowCallback.html) is a great example.



## Stop optimization after some trials are pruned in a row[](#stop-optimization-after-some-trials-are-pruned-in-a-row)


This example implements a stateful callback which stops the optimization
if a certain number of trials are pruned in a row.
The number of trials pruned in a row is specified by `threshold`.


```
import optuna


class StopWhenTrialKeepBeingPrunedCallback:
    def __init__(self, threshold: int):
        self.threshold = threshold
        self._consequtive_pruned_count = 0

    def __call__(self, study: optuna.study.Study, trial: optuna.trial.FrozenTrial) -> None:
        if trial.state == optuna.trial.TrialState.PRUNED:
            self._consequtive_pruned_count += 1
        else:
            self._consequtive_pruned_count = 0

        if self._consequtive_pruned_count >= self.threshold:
            study.stop()
```



This objective prunes all the trials except for the first 5 trials (`trial.number` starts with 0).


```
def objective(trial):
    if trial.number > 4:
        raise optuna.TrialPruned

    return trial.suggest_float("x", 0, 1)
```



Here, we set the threshold to `2`: optimization finishes once two trials are pruned in a row.
So, we expect this study to stop after 7 trials.


```
import logging
import sys

# Add stream handler of stdout to show the messages
optuna.logging.get_logger("optuna").addHandler(logging.StreamHandler(sys.stdout))

study_stop_cb = StopWhenTrialKeepBeingPrunedCallback(2)
study = optuna.create_study()
study.optimize(objective, n_trials=10, callbacks=[study_stop_cb])
```



```
A new study created in memory with name: no-name-5e5da9cd-8e79-4cbc-9e7b-60b33d9d565f
Trial 0 finished with value: 0.6218430915474218 and parameters: {'x': 0.6218430915474218}. Best is trial 0 with value: 0.6218430915474218.
Trial 1 finished with value: 0.2427726243041084 and parameters: {'x': 0.2427726243041084}. Best is trial 1 with value: 0.2427726243041084.
Trial 2 finished with value: 0.38703104273220823 and parameters: {'x': 0.38703104273220823}. Best is trial 1 with value: 0.2427726243041084.
Trial 3 finished with value: 0.6847177614644492 and parameters: {'x': 0.6847177614644492}. Best is trial 1 with value: 0.2427726243041084.
Trial 4 finished with value: 0.7591046580029978 and parameters: {'x': 0.7591046580029978}. Best is trial 1 with value: 0.2427726243041084.
Trial 5 pruned.
Trial 6 pruned.
```



As you can see in the log above, the study stopped after 7 trials as expected.


**Total running time of the script:** (0 minutes 0.004 seconds)




[`Download Jupyter notebook: 007_optuna_callback.ipynb`](https://optuna.readthedocs.io/en/stable/_downloads/8a3b786e31e54819e53dfa737aebc72d/007_optuna_callback.ipynb)




[`Download Python source code: 007_optuna_callback.py`](https://optuna.readthedocs.io/en/stable/_downloads/69c9a8896808997c60d5d1879065fad2/007_optuna_callback.py)




[`Download zipped: 007_optuna_callback.zip`](https://optuna.readthedocs.io/en/stable/_downloads/a4b5b50f3625a46e93ec9d6547bb65f1/007_optuna_callback.zip)




[Gallery generated by Sphinx-Gallery](https://sphinx-gallery.github.io)
