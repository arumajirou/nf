# Optuna ドキュメントまとめ（Optunaのみ実行）

- 抽出日時: 2025-11-12 11:44
- 件数: 25

## 目次
1. [optuna.samplers — Optuna 4.6.0 documentation](#optunasamplers-Optuna-460-documentation)
2. [Callback for Study.optimize — Optuna 4.6.0 documentation](#Callback-for-Studyoptimize-Optuna-460-documentation)
3. [Optuna - A hyperparameter optimization framework](#Optuna-A-hyperparameter-optimization-framework)
4. [optuna.study.Study — Optuna 4.6.0 documentation](#optunastudyStudy-Optuna-460-documentation)
5. [optuna.trial.Trial — Optuna 4.6.0 documentation](#optunatrialTrial-Optuna-460-documentation)
6. [optuna.study.create_study — Optuna 4.6.0 documentation](#optunastudycreate_study-Optuna-460-documentation)
7. [optuna.study.load_study — Optuna 4.6.0 documentation](#optunastudyload_study-Optuna-460-documentation)
8. [optuna.samplers.BaseSampler — Optuna 4.6.0 documentation](#optunasamplersBaseSampler-Optuna-460-documentation)
9. [optuna.samplers.TPESampler — Optuna 4.6.0 documentation](#optunasamplersTPESampler-Optuna-460-documentation)
10. [optuna.samplers.CmaEsSampler — Optuna 4.6.0 documentation](#optunasamplersCmaEsSampler-Optuna-460-documentation)
11. [optuna.samplers.QMCSampler — Optuna 4.6.0 documentation](#optunasamplersQMCSampler-Optuna-460-documentation)
12. [optuna.samplers.RandomSampler — Optuna 4.6.0 documentation](#optunasamplersRandomSampler-Optuna-460-documentation)
13. [optuna.samplers.GPSampler — Optuna 4.6.0 documentation](#optunasamplersGPSampler-Optuna-460-documentation)
14. [optuna.samplers.NSGAIISampler — Optuna 4.6.0 documentation](#optunasamplersNSGAIISampler-Optuna-460-documentation)
15. [optuna.pruners — Optuna 4.6.0 documentation](#optunapruners-Optuna-460-documentation)
16. [optuna.pruners.MedianPruner — Optuna 4.6.0 documentation](#optunaprunersMedianPruner-Optuna-460-documentation)
17. [optuna.pruners.SuccessiveHalvingPruner — Optuna 4.6.0 documentation](#optunaprunersSuccessiveHalvingPruner-Optuna-460-documentation)
18. [optuna.pruners.HyperbandPruner — Optuna 4.6.0 documentation](#optunaprunersHyperbandPruner-Optuna-460-documentation)
19. [optuna.pruners.ThresholdPruner — Optuna 4.6.0 documentation](#optunaprunersThresholdPruner-Optuna-460-documentation)
20. [optuna.pruners.PatientPruner — Optuna 4.6.0 documentation](#optunaprunersPatientPruner-Optuna-460-documentation)
21. [User-Defined Pruner — Optuna 4.6.0 documentation](#User-Defined-Pruner-Optuna-460-documentation)
22. [Ask-and-Tell Interface — Optuna 4.6.0 documentation](#Ask-and-Tell-Interface-Optuna-460-documentation)
23. [optuna.TrialPruned — Optuna 4.6.0 documentation](#optunaTrialPruned-Optuna-460-documentation)
24. [optuna.storages.RetryFailedTrialCallback — Optuna 4.6.0 documentation](#optunastoragesRetryFailedTrialCallback-Optuna-460-documentation)
25. [optuna.copy_study — Optuna 4.6.0 documentation](#optunacopy_study-Optuna-460-documentation)


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

---

## Optuna - A hyperparameter optimization framework
<a id="Optuna-A-hyperparameter-optimization-framework"></a>

- 元URL: https://optuna.org/

Optuna is an automatic hyperparameter optimization software framework, particularly designed for machine learning.

Optuna v5 Roadmap 


## 
								Towards Optuna v5
							




We are currently working on the development of Optuna v5. Features related to the v5 roadmap will be added in v4.x updates.




 <h3 class="text-center" id="v5gallery"
							style="padding-top:1em; margin-top:0; padding-bottom:1em; font-weight:bold; color:#333333;">
								Features Gallery
							</h2> 




## Powerful Default Sampler




![](https://optuna.org/assets/img/v5-default-sampler.png)

In Optuna v5, we will improve Optuna's default optimization algorithm and its options to enhance performance and usability.









## Optuna-Dashboard LLM Integration




[![](https://optuna.org/assets/img/v5-smart-filter.png)](https://optuna-dashboard.readthedocs.io/en/latest/tutorials/llm-integration.html)

Flexible control of Optuna-Dashboard powered by LLMs such as data querying with natural language.









## Multi-Objective GPSampler




[![](https://optuna.org/assets/img/v5-ehvi.png)](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html)

Gaussian process-based Bayesian optimization for multi-objective optimization. This is available from Optuna v4.4. See the [document](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html) for more details.







[Read Optuna v5 Roadmap Blog](https://medium.com/optuna/optuna-v5-roadmap-ac7d6935a878)
[Contribute to Optuna v5](https://github.com/optuna/optuna/labels/v5)
[Give Us Your Feedback on Optuna v5](https://forms.gle/wVwLCQ9g6st6AXuq9)

  end of row 
 Key Features 


## 
								Key Features
							






## Eager search
												spaces







Automated search for optimal hyperparameters using Python conditionals, loops, and syntax








## 
												State-of-the-art
												algorithms
											







Efficiently search large spaces and prune unpromising trials for faster results








## Easy
												parallelization



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)

Parallelize hyperparameter searches over multiple threads or processes without modifying code





  end of row 
  end of col-12 
 external links (top) 

- [GitHub](https://github.com/optuna/optuna)
- [Twitter](https://twitter.com/OptunaAutoML)
- [LinkedIn](https://linkedin.com/showcase/optuna)
- [Tutorials](https://optuna.readthedocs.io/en/stable/tutorial/index.html)
- [Docs](https://optuna.readthedocs.io/en/stable/index.html)



  end of row 
 Code Examples 


## Code
								Examples




Optuna is framework agnostic. You can use it with any machine learning or deep learning framework.







- [![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
Quick Start](#code_quickstart)
- [#code_PyTorch](#code_PyTorch)
- [![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==) TensorFlow](#code_tensorflow)
- [Keras](#code_Keras)
- [![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==) Scikit-Learn](#code_ScikitLearn)
- [![XGBoost](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)](#code_XGBoost)
- [LightGBM](#code_LightGBM)
- [Other](#code_other)









A simple optimization problem:


1. Define `objective` function to be optimized. Let's minimize `(x -
																2)^2`
2. Suggest hyperparameter values using `trial` object. Here, a float value of
															`x` is suggested from `-10` to `10`
3. Create a `study` object and invoke the `optimize` method over 100
															trials


```
import optuna

def objective(trial):
    x = trial.suggest_float('x', -10, 10)
    return (x - 2) ** 2

study = optuna.create_study()
study.optimize(objective, n_trials=100)

study.best_params  # E.g. {'x': 2.002108042}
```


[colab.research.google






















Open in Colab
Open in Colab](http://colab.research.google.com/github/optuna/optuna-examples/blob/main/quickstart.ipynb)










You can optimize PyTorch hyperparameters, such as the number of layers and the number of
														hidden nodes in each layer, in three steps:


1. Wrap model training with an `objective` function and return accuracy
2. Suggest hyperparameters using a `trial` object
3. Create a `study` object and execute the optimization


```
import torch

import optuna

# 1. Define an objective function to be maximized.
def objective(trial):

    # 2. Suggest values of the hyperparameters using a trial object.
    n_layers = trial.suggest_int('n_layers', 1, 3)
    layers = []

    in_features = 28 * 28
    for i in range(n_layers):
        out_features = trial.suggest_int(f'n_units_l{i}', 4, 128)
        layers.append(torch.nn.Linear(in_features, out_features))
        layers.append(torch.nn.ReLU())
        in_features = out_features
    layers.append(torch.nn.Linear(in_features, 10))
    layers.append(torch.nn.LogSoftmax(dim=1))
    model = torch.nn.Sequential(*layers).to(torch.device('cpu'))
    ...
    return accuracy

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```


[See full example on GitHub](https://github.com/optuna/optuna-examples/blob/main/pytorch/pytorch_simple.py)








You can optimize TensorFlow hyperparameters, such as the number of layers and the number of
														hidden nodes in each layer, in three steps:


1. Wrap model training with an `objective` function and return accuracy
2. Suggest hyperparameters using a `trial` object
3. Create a `study` object and execute the optimization


```
import tensorflow as tf

import optuna

# 1. Define an objective function to be maximized.
def objective(trial):

    # 2. Suggest values of the hyperparameters using a trial object.
    n_layers = trial.suggest_int('n_layers', 1, 3)
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Flatten())
    for i in range(n_layers):
        num_hidden = trial.suggest_int(f'n_units_l{i}', 4, 128, log=True)
        model.add(tf.keras.layers.Dense(num_hidden, activation='relu'))
    model.add(tf.keras.layers.Dense(CLASSES))
    ...
    return accuracy

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```


[See full example on GitHub](https://github.com/optuna/optuna-examples/blob/main/tensorflow/tensorflow_eager_simple.py)








You can optimize Keras hyperparameters, such as the number of filters and kernel size, in
														three steps:


1. Wrap model training with an `objective` function and return accuracy
2. Suggest hyperparameters using a `trial` object
3. Create a `study` object and execute the optimization


```
import keras

import optuna

# 1. Define an objective function to be maximized.
def objective(trial):
    model = Sequential()

    # 2. Suggest values of the hyperparameters using a trial object.
    model.add(
        Conv2D(filters=trial.suggest_categorical('filters', [32, 64]),
               kernel_size=trial.suggest_categorical('kernel_size', [3, 5]),
               strides=trial.suggest_categorical('strides', [1, 2]),
               activation=trial.suggest_categorical('activation', ['relu', 'linear']),
               input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(CLASSES, activation='softmax'))

    # We compile our model with a sampled learning rate.
    lr = trial.suggest_float('lr', 1e-5, 1e-1, log=True)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=RMSprop(lr=lr), metrics=['accuracy'])
    ...
    return accuracy

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```


[See full example on GitHub](https://github.com/optuna/optuna-examples/blob/main/keras/keras_simple.py)








You can optimize Scikit-Learn hyperparameters, such as the `C` parameter of
														`SVC` and the `max_depth` of the `RandomForestClassifier`,
														in
														three steps:


1. Wrap model training with an `objective` function and return accuracy
2. Suggest hyperparameters using a `trial` object
3. Create a `study` object and execute the optimization


```
import sklearn

import optuna

# 1. Define an objective function to be maximized.
def objective(trial):

    # 2. Suggest values for the hyperparameters using a trial object.
    classifier_name = trial.suggest_categorical('classifier', ['SVC', 'RandomForest'])
    if classifier_name == 'SVC':
         svc_c = trial.suggest_float('svc_c', 1e-10, 1e10, log=True)
         classifier_obj = sklearn.svm.SVC(C=svc_c, gamma='auto')
    else:
        rf_max_depth = trial.suggest_int('rf_max_depth', 2, 32, log=True)
        classifier_obj = sklearn.ensemble.RandomForestClassifier(max_depth=rf_max_depth, n_estimators=10)
    ...
    return accuracy

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```


[See full example on GitHub](https://github.com/optuna/optuna-examples/blob/main/sklearn/sklearn_simple.py)








You can optimize XGBoost hyperparameters, such as the booster type and alpha, in three
														steps:


1. Wrap model training with an `objective` function and return accuracy
2. Suggest hyperparameters using a `trial` object
3. Create a `study` object and execute the optimization


```
import xgboost as xgb

import optuna

# 1. Define an objective function to be maximized.
def objective(trial):
    ...

    # 2. Suggest values of the hyperparameters using a trial object.
    param = {
        "objective": "binary:logistic",
        "booster": trial.suggest_categorical("booster", ["gbtree", "gblinear", "dart"]),
        "lambda": trial.suggest_float("lambda", 1e-8, 1.0, log=True),
        "alpha": trial.suggest_float("alpha", 1e-8, 1.0, log=True),
        "subsample": trial.suggest_float("subsample", 0.2, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.2, 1.0),
    }

    bst = xgb.train(param, dtrain)
    ...
    return accuracy

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```


[See full example on GitHub](https://github.com/optuna/optuna-examples/blob/main/xgboost/xgboost_simple.py)








You can optimize LightGBM hyperparameters, such as boosting type and the number of leaves,
														in
														three steps:


1. Wrap model training with an `objective` function and return accuracy
2. Suggest hyperparameters using a `trial` object
3. Create a `study` object and execute the optimization


```
import lightgbm as lgb

import optuna

# 1. Define an objective function to be maximized.
def objective(trial):
    ...

    # 2. Suggest values of the hyperparameters using a trial object.
    param = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'lambda_l1': trial.suggest_float('lambda_l1', 1e-8, 10.0, log=True),
        'lambda_l2': trial.suggest_float('lambda_l2', 1e-8, 10.0, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 2, 256),
        'feature_fraction': trial.suggest_float('feature_fraction', 0.4, 1.0),
        'bagging_fraction': trial.suggest_float('bagging_fraction', 0.4, 1.0),
        'bagging_freq': trial.suggest_int('bagging_freq', 1, 7),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
    }

    gbm = lgb.train(param, dtrain)
    ...
    return accuracy

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```


[See full example on GitHub](https://github.com/optuna/optuna-examples/blob/main/lightgbm/lightgbm_simple.py)








Check more examples including PyTorch Ignite, Dask-ML and MLFlow at our GitHub
														repository.  

														It also provides the visualization demo as follows:


```

from optuna.visualization import plot_intermediate_values

...
plot_intermediate_values(study)
```



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)


[See full example on GitHub](https://github.com/optuna/optuna-examples/tree/main)







 Code Examples 


## 
								Installation




Optuna can be installed with pip. Python 3.9 or newer is supported.



```
% pip install optuna
```



[Details](https://optuna.readthedocs.io/en/stable/installation.html)



  end of row 
 external links (top) 
- [GitHub](https://github.com/optuna/optuna)
- [Twitter](https://twitter.com/OptunaAutoML)
- [LinkedIn](https://linkedin.com/showcase/optuna)
- [Tutorials](https://optuna.readthedocs.io/en/stable/tutorial/index.html)
- [Docs](https://optuna.readthedocs.io/en/stable/index.html)




## 
								Dashboard



[![Optuna Dashboard](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)](https://github.com/optuna/optuna-dashboard)



[Optuna Dashboard](https://github.com/optuna/optuna-dashboard) is a real-time web dashboard for Optuna.
										You can check the optimization history, hyperparameter importances, etc. in graphs and tables.



```
% pip install optuna-dashboard
% optuna-dashboard sqlite:///db.sqlite3
```



Optuna Dashboard is also available as extensions for Jupyter Lab and Visual Studio Code.






## 
									        			VS Code Extension
									        		



![VS Code Extension](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
To use, install the extension, right-click the SQLite3 files in the file explorer and select the “Open in Optuna Dashboard” from the dropdown menu.









## 
									        			Jupyter Lab Extension
									        		



![Jupyter Lab Extension](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
```
% pip install jupyterlab jupyterlab-optuna
```







[GitHub Repository](https://github.com/optuna/optuna-dashboard)
[Documentation](https://optuna-dashboard.readthedocs.io/en/latest/)
[VS Code Extension (Marketplace)](https://marketplace.visualstudio.com/items?itemName=Optuna.optuna-dashboard#overview)




 end of row 


## 
								OptunaHub




[OptunaHub](https://hub.optuna.org) is a feature-sharing platform for Optuna.
										Users can freely use registered features, and contributors can register the features they implement.
										The following example uses [AutoSampler](https://hub.optuna.org/samplers/auto_sampler/) on OptunaHub, which automatically selects a proper sampler from those implemented in Optuna.



```
% pip install optunahub
% pip install cmaes scipy torch  # install AutoSampler dependencies
```




```
import optuna
import optunahub

def objective(trial: optuna.Trial) -> float:
	x = trial.suggest_float("x", -5, 5)
	y = trial.suggest_float("y", -5, 5)
	return x**2 + y**2

module = optunahub.load_module(package="samplers/auto_sampler")
study = optuna.create_study(sampler=module.AutoSampler())
study.optimize(objective, n_trials=50)

print(study.best_trial.value, study.best_trial.params)
```



[OptunaHub](https://hub.optuna.org)
[Register Your Package](https://github.com/optuna/optunahub-registry)



  end of row 


 The 1st Row of Blogs 


## 
										Blog



 Left Side of the 1st Row 


[Nov 10, 2025
														
## 
															Announcing Optuna 4.6
														



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
                                                            We are excited to announce the release of Optuna 4.6, the latest version of our black-box optimization framework.](https://medium.com/optuna/announcing-optuna-4-6-a9e82183ab07)


 Right Side of the 1st Row 


[Oct 28, 2025
														
## 
															AutoSampler: Full Support for Multi-Objective & Constrained Optimization
														



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
                                                            We have enhanced AutoSampler to fully support multi-objective and constrained optimization.](https://medium.com/optuna/autosampler-full-support-for-multi-objective-constrained-optimization-c1c4fc957ba2)


 End of the 1st Row 



 The 2nd Row of Blogs 



 Left Side of the 2nd Row 


[Sep 22, 2025
										                
## 
										                    [Optuna v4.5] Gaussian Process-Based Sampler (GPSampler) Can Now Perform Constrained Multi-Objective Optimization
										                



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
										                    Optuna v4.5 extends Gaussian process-based sampler (GPSampler) to support constrained multi-objective optimization.](https://medium.com/optuna/optuna-v4-5-81e78d8e077a)


 Right Side of the 2nd Row 


[Jun 16, 2025
														
## 
															Announcing Optuna 4.4
														



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
                                                            We have released the version 4.4 of the black-box optimization framework Optuna. We encourage you to check out the release notes!](https://medium.com/optuna/announcing-optuna-4-4-ece661493126)


 End of the 2nd Row 



 The 3rd Row of Blogs 



 Left Side of the 3rd Row 


[May 26, 2025
														
## 
															Optuna v5 Roadmap
														



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
                                                            Optuna v5 pushes black-box optimization forward - with new features for generative AI, broader applications, and easier integration.](https://medium.com/@HideakiImamura/ac7d6935a878)


 Right Side of the 3rd Row 


[Mar 24, 2025
														
## 
															Distributed Optimization in Optuna and gRPC Storage Proxy
														



![](data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==)
                                                            This article explains how to perform distributed optimization and introduce the gRPC Storage Proxy, which enables large-scale optimization.](https://medium.com/optuna/distributed-optimization-in-optuna-and-grpc-storage-proxy-08db83f1d608)


 End of the 3rd Row 



[See more stories on Medium](https://medium.com/optuna)
## 
								Videos
							










## 
										Papers


### Optuna


If you use Optuna in a scientific publication, please use the following citation:


```
Takuya Akiba, Shotaro Sano, Toshihiko Yanase, Takeru Ohta, and Masanori Koyama. 2019.
	Optuna: A Next-generation Hyperparameter Optimization Framework. In KDD.
```


Bibtex entry:


```
@inproceedings{optuna_2019,
	title={Optuna: A Next-generation Hyperparameter Optimization Framework},
	author={Akiba, Takuya and Sano, Shotaro and Yanase, Toshihiko and Ohta, Takeru and Koyama, Masanori},
	booktitle={Proceedings of the 25th {ACM} {SIGKDD} International Conference on Knowledge Discovery and Data Mining},
	year={2019}
}
```


[View
											Paper](https://dl.acm.org/citation.cfm?id=3330701)
[arXiv
											Preprint](https://arxiv.org/abs/1907.10902)
### OptunaHub


If you use OptunaHub in a scientific publication, please use the following citation:


```
Yoshihiko Ozaki, Shuhei Watanabe, and Toshihiko Yanase. 2025.
	OptunaHub: A Platform for Black-Box Optimization. arXiv preprint arXiv:2510.02798.
```


Bibtex entry:


```
@article{ozaki2025optunahub,
	title={{OptunaHub}: A Platform for Black-Box Optimization},
	author={Ozaki, Yoshihiko and Watanabe, Shuhei and Yanase, Toshihiko},
	journal={arXiv preprint arXiv:2510.02798},
	year={2025}
}
```


[arXiv
											Preprint](https://doi.org/10.48550/arXiv.2510.02798)




- [GitHub](https://github.com/optuna/optuna)
- [Twitter](https://twitter.com/OptunaAutoML)
- [LinkedIn](https://linkedin.com/showcase/optuna)
- [Tutorials](https://optuna.readthedocs.io/en/stable/tutorial/index.html)
- [Docs](https://optuna.readthedocs.io/en/stable/index.html)


  end of container 
  end of section

---

## optuna.study.Study — Optuna 4.6.0 documentation
<a id="optunastudyStudy-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html

# optuna.study.Study[](#optuna-study-study)




*class *optuna.study.Study(*study_name*, *storage*, *sampler=None*, *pruner=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study)[](#optuna.study.Study)
A study corresponds to an optimization task, i.e., a set of trials.


This object provides interfaces to run a new [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial), access trials’
history, set/get user-defined attributes of the study itself.


Note that the direct use of this constructor is not recommended.
To create and load a study, please refer to the documentation of
[`create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html#optuna.study.create_study) and [`load_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.load_study.html#optuna.study.load_study) respectively.


Methods




[`add_trial`](#optuna.study.Study.add_trial)(trial)


Add trial to study.



[`add_trials`](#optuna.study.Study.add_trials)(trials)


Add trials to study.



[`ask`](#optuna.study.Study.ask)([fixed_distributions])


Create a new trial from which hyperparameters can be suggested.



[`enqueue_trial`](#optuna.study.Study.enqueue_trial)(params[, user_attrs, ...])


Enqueue a trial with given parameter values.



[`get_trials`](#optuna.study.Study.get_trials)([deepcopy, states])


Return all trials in the study.



[`optimize`](#optuna.study.Study.optimize)(func[, n_trials, timeout, n_jobs, ...])


Optimize an objective function.



[`set_metric_names`](#optuna.study.Study.set_metric_names)(metric_names)


Set metric names.



[`set_system_attr`](#optuna.study.Study.set_system_attr)(key, value)


Set a system attribute to the study.



[`set_user_attr`](#optuna.study.Study.set_user_attr)(key, value)


Set a user attribute to the study.



[`stop`](#optuna.study.Study.stop)()


Exit from the current optimization loop after the running trials finish.



[`tell`](#optuna.study.Study.tell)(trial[, values, state, skip_if_finished])


Finish a trial created with [`ask()`](#optuna.study.Study.ask).



[`trials_dataframe`](#optuna.study.Study.trials_dataframe)([attrs, multi_index])


Export trials as a pandas [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).





Attributes




[`best_params`](#optuna.study.Study.best_params)


Return parameters of the best trial in the study.



[`best_trial`](#optuna.study.Study.best_trial)


Return the best trial in the study.



[`best_trials`](#optuna.study.Study.best_trials)


Return trials located at the Pareto front in the study.



[`best_value`](#optuna.study.Study.best_value)


Return the best objective value in the study.



[`direction`](#optuna.study.Study.direction)


Return the direction of the study.



[`directions`](#optuna.study.Study.directions)


Return the directions of the study.



[`metric_names`](#optuna.study.Study.metric_names)


Return metric names.



[`system_attrs`](#optuna.study.Study.system_attrs)


Return system attributes.



[`trials`](#optuna.study.Study.trials)


Return all trials in the study.



[`user_attrs`](#optuna.study.Study.user_attrs)


Return user attributes.






Parameters:
- **study_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
- **storage** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **storages.BaseStorage*)
- **sampler** (*'samplers.BaseSampler'** | **None*)
- **pruner** ([*pruners.BasePruner*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner)* | **None*)






add_trial(*trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.add_trial)[](#optuna.study.Study.add_trial)
Add trial to study.


The trial is validated before being added.


Example


```
import optuna
from optuna.distributions import FloatDistribution


def objective(trial):
    x = trial.suggest_float("x", 0, 10)
    return x**2


study = optuna.create_study()
assert len(study.trials) == 0

trial = optuna.trial.create_trial(
    params={"x": 2.0},
    distributions={"x": FloatDistribution(0, 10)},
    value=4.0,
)

study.add_trial(trial)
assert len(study.trials) == 1

study.optimize(objective, n_trials=3)
assert len(study.trials) == 4

other_study = optuna.create_study()

for trial in study.trials:
    other_study.add_trial(trial)
assert len(other_study.trials) == len(study.trials)

other_study.optimize(objective, n_trials=2)
assert len(other_study.trials) == len(study.trials) + 2
```




See also


This method should in general be used to add already evaluated trials
(`trial.state.is_finished() == True`). To queue trials for evaluation,
please refer to [`enqueue_trial()`](#optuna.study.Study.enqueue_trial).




See also


See [`create_trial()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.create_trial.html#optuna.trial.create_trial) for how to create trials.




See also


Please refer to [Second scenario: Have Optuna utilize already evaluated hyperparameters](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/008_specify_params.html#add-trial-tutorial) for the tutorial of specifying
hyperparameters with the evaluated value manually.




Parameters:
**trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Trial to add.



Return type:
None







add_trials(*trials*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.add_trials)[](#optuna.study.Study.add_trials)
Add trials to study.


The trials are validated before being added.


Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", 0, 10)
    return x**2


study = optuna.create_study()
study.optimize(objective, n_trials=3)
assert len(study.trials) == 3

other_study = optuna.create_study()
other_study.add_trials(study.trials)
assert len(other_study.trials) == len(study.trials)

other_study.optimize(objective, n_trials=2)
assert len(other_study.trials) == len(study.trials) + 2
```




See also


See [`add_trial()`](#optuna.study.Study.add_trial) for addition of each trial.




Parameters:
**trials** (*Iterable**[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]*) – Trials to add.



Return type:
None







ask(*fixed_distributions=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.ask)[](#optuna.study.Study.ask)
Create a new trial from which hyperparameters can be suggested.


This method is part of an alternative to [`optimize()`](#optuna.study.Study.optimize) that allows
controlling the lifetime of a trial outside the scope of `func`. Each call to this
method should be followed by a call to [`tell()`](#optuna.study.Study.tell) to finish the
created trial.



See also


The [Ask-and-Tell Interface](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html#ask-and-tell) tutorial provides use-cases with examples.



Example


Getting the trial object with the [`ask()`](#optuna.study.Study.ask) method.


```
import optuna


study = optuna.create_study()

trial = study.ask()

x = trial.suggest_float("x", -1, 1)

study.tell(trial, x**2)
```



Example


Passing previously defined distributions to the [`ask()`](#optuna.study.Study.ask)
method.


```
import optuna


study = optuna.create_study()

distributions = {
    "optimizer": optuna.distributions.CategoricalDistribution(["adam", "sgd"]),
    "lr": optuna.distributions.FloatDistribution(0.0001, 0.1, log=True),
}

# You can pass the distributions previously defined.
trial = study.ask(fixed_distributions=distributions)

# `optimizer` and `lr` are already suggested and accessible with `trial.params`.
assert "optimizer" in trial.params
assert "lr" in trial.params
```




Parameters:
**fixed_distributions** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**] **| **None*) – A dictionary containing the parameter names and parameter’s distributions. Each
parameter in this dictionary is automatically suggested for the returned trial,
even when the suggest method is not explicitly invoked by the user. If this
argument is set to [`None`](https://docs.python.org/3/library/constants.html#None), no parameter is automatically suggested.



Returns:
A [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial).



Return type:
[Trial](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)







*property *best_params*: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*[](#optuna.study.Study.best_params)
Return parameters of the best trial in the study.



Note


This feature can only be used for single-objective optimization.




Returns:
A dictionary containing parameters of the best trial.







*property *best_trial*: [FrozenTrial](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*[](#optuna.study.Study.best_trial)
Return the best trial in the study.



Note


This feature can only be used for single-objective optimization.
If your study is multi-objective,
use [`best_trials`](#optuna.study.Study.best_trials) instead.




Returns:
A [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) object of the best trial.





See also


The [Re-use the best trial](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/010_reuse_best_trial.html#reuse-best-trial) tutorial provides a detailed example of how to use this
method.






*property *best_trials*: [list](https://docs.python.org/3/library/stdtypes.html#list)[[FrozenTrial](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)]*[](#optuna.study.Study.best_trials)
Return trials located at the Pareto front in the study.


A trial is located at the Pareto front if there are no trials that dominate the trial.
It’s called that a trial `t0` dominates another trial `t1` if
`all(v0 <= v1) for v0, v1 in zip(t0.values, t1.values)` and
`any(v0 < v1) for v0, v1 in zip(t0.values, t1.values)` are held.



Returns:
A list of [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) objects.







*property *best_value*: [float](https://docs.python.org/3/library/functions.html#float)*[](#optuna.study.Study.best_value)
Return the best objective value in the study.



Note


This feature can only be used for single-objective optimization.




Returns:
A float representing the best objective value.







*property *direction*: [StudyDirection](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection)*[](#optuna.study.Study.direction)
Return the direction of the study.



Note


This feature can only be used for single-objective optimization.
If your study is multi-objective,
use [`directions`](#optuna.study.Study.directions) instead.




Returns:
A [`StudyDirection`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection) object.







*property *directions*: [list](https://docs.python.org/3/library/stdtypes.html#list)[[StudyDirection](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection)]*[](#optuna.study.Study.directions)
Return the directions of the study.



Returns:
A list of [`StudyDirection`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection) objects.







enqueue_trial(*params*, *user_attrs=None*, *skip_if_exists=False*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.enqueue_trial)[](#optuna.study.Study.enqueue_trial)
Enqueue a trial with given parameter values.


You can fix the next sampling parameters which will be evaluated in your
objective function.


Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", 0, 10)
    return x**2


study = optuna.create_study()
study.enqueue_trial({"x": 5})
study.enqueue_trial({"x": 0}, user_attrs={"memo": "optimal"})
study.optimize(objective, n_trials=2)

assert study.trials[0].params == {"x": 5}
assert study.trials[1].params == {"x": 0}
assert study.trials[1].user_attrs == {"memo": "optimal"}
```




Parameters:
- **params** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, *[*Any*](https://docs.python.org/3/library/typing.html#typing.Any)*]*) – Parameter values to pass your objective function.
- **user_attrs** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, *[*Any*](https://docs.python.org/3/library/typing.html#typing.Any)*] **| **None*) – A dictionary of user-specific attributes other than `params`.
- **skip_if_exists** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

When [`True`](https://docs.python.org/3/library/constants.html#True), prevents duplicate trials from being enqueued again.



Note


This method might produce duplicated trials if called simultaneously
by multiple processes at the same time with same `params` dict.



Return type:
None





See also


Please refer to [First Scenario: Have Optuna evaluate your hyperparameters](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/008_specify_params.html#enqueue-trial-tutorial) for the tutorial of specifying
hyperparameters manually.






get_trials(*deepcopy=True*, *states=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.get_trials)[](#optuna.study.Study.get_trials)
Return all trials in the study.


The returned trials are ordered by trial number.



See also


See [`trials`](#optuna.study.Study.trials) for related property.



Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", -1, 1)
    return x**2


study = optuna.create_study()
study.optimize(objective, n_trials=3)

trials = study.get_trials()
assert len(trials) == 3
```




Parameters:
- **deepcopy** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Flag to control whether to apply `copy.deepcopy()` to the trials.
Note that if you set the flag to [`False`](https://docs.python.org/3/library/constants.html#False), you shouldn’t mutate
any fields of the returned trial. Otherwise the internal state of
the study may corrupt and unexpected behavior may happen.
- **states** (*Container**[*[*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)*] **| **None*) – Trial states to filter on. If [`None`](https://docs.python.org/3/library/constants.html#None), include all states.



Returns:
A list of [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) objects.



Return type:
[list](https://docs.python.org/3/library/stdtypes.html#list)[[FrozenTrial](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)]







*property *metric_names*: [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | [None](https://docs.python.org/3/library/constants.html#None)*[](#optuna.study.Study.metric_names)
Return metric names.



Note


Use [`set_metric_names()`](#optuna.study.Study.set_metric_names) to set the metric names first.




Returns:
A list with names for each dimension of the returned values of the objective function.







optimize(*func*, *n_trials=None*, *timeout=None*, *n_jobs=1*, *catch=()*, *callbacks=None*, *gc_after_trial=False*, *show_progress_bar=False*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.optimize)[](#optuna.study.Study.optimize)
Optimize an objective function.


Optimization is done by choosing a suitable set of hyperparameter values from a given
range. Uses a sampler which implements the task of value suggestion based on a specified
distribution. The sampler is specified in [`create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html#optuna.study.create_study) and the
default choice for the sampler is TPE.
See also [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) for more details on ‘TPE’.


Optimization will be stopped when receiving a termination signal such as SIGINT and
SIGTERM. Unlike other signals, a trial is automatically and cleanly failed when receiving
SIGINT (Ctrl+C). If `n_jobs` is greater than one or if another signal than SIGINT
is used, the interrupted trial state won’t be properly updated.


Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", -1, 1)
    return x**2


study = optuna.create_study()
study.optimize(objective, n_trials=3)
```




Parameters:
- **func** (*ObjectiveFuncType*) – A callable that implements objective function.
- **n_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) –

The number of trials for each process. [`None`](https://docs.python.org/3/library/constants.html#None) represents no limit in terms of
the number of trials. The study continues to create trials until the number of
trials reaches `n_trials`, `timeout` period elapses,
[`stop()`](#optuna.study.Study.stop) is called, or a termination signal such as
SIGTERM or Ctrl+C is received.



See also


[`optuna.study.MaxTrialsCallback`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.MaxTrialsCallback.html#optuna.study.MaxTrialsCallback) can ensure how many times trials
will be performed across all processes.
- **timeout** ([*float*](https://docs.python.org/3/library/functions.html#float)* | **None*) – Stop study after the given number of second(s). [`None`](https://docs.python.org/3/library/constants.html#None) represents no limit in
terms of elapsed time. The study continues to create trials until the number of
trials reaches `n_trials`, `timeout` period elapses,
[`stop()`](#optuna.study.Study.stop) is called or, a termination signal such as
SIGTERM or Ctrl+C is received.
- **n_jobs** ([*int*](https://docs.python.org/3/library/functions.html#int)) –

The number of parallel jobs. If this argument is set to `-1`, the number is
set to CPU count.



Note


`n_jobs` allows parallelization using [`threading`](https://docs.python.org/3/library/threading.html#module-threading) and may suffer from
[Python’s GIL](https://wiki.python.org/moin/GlobalInterpreterLock).
It is recommended to use [process-based parallelization](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/004_distributed.html#distributed)
if `func` is CPU bound.
- **catch** (*Iterable**[*[*type*](https://docs.python.org/3/library/functions.html#type)*[*[*Exception*](https://docs.python.org/3/library/exceptions.html#Exception)*]**] **| *[*type*](https://docs.python.org/3/library/functions.html#type)*[*[*Exception*](https://docs.python.org/3/library/exceptions.html#Exception)*]*) – A study continues to run even when a trial raises one of the exceptions specified
in this argument. Default is an empty tuple, i.e. the study will stop for any
exception except for [`TrialPruned`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.exceptions.TrialPruned.html#optuna.exceptions.TrialPruned).
- **callbacks** (*Iterable**[**Callable**[**[*[*Study*](#optuna.study.Study)*, *[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]**, **None**]**] **| **None*) –

List of callback functions that are invoked at the end of each trial. Each function
must accept two parameters with the following types in this order:
[`Study`](#optuna.study.Study) and [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial).



See also


See the tutorial of [Callback for Study.optimize](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/007_optuna_callback.html#optuna-callback) for how to use and implement
callback functions.
- **gc_after_trial** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

Flag to determine whether to automatically run garbage collection after each trial.
Set to [`True`](https://docs.python.org/3/library/constants.html#True) to run the garbage collection, [`False`](https://docs.python.org/3/library/constants.html#False) otherwise.
When it runs, it runs a full collection by internally calling [`gc.collect()`](https://docs.python.org/3/library/gc.html#gc.collect).
If you see an increase in memory consumption over several trials, try setting this
flag to [`True`](https://docs.python.org/3/library/constants.html#True).



See also


[How do I avoid running out of memory (OOM) when optimizing studies?](https://optuna.readthedocs.io/en/stable/faq.html#out-of-memory-gc-collect)
- **show_progress_bar** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Flag to show progress bars or not. To show progress bar, set this [`True`](https://docs.python.org/3/library/constants.html#True).
Note that it is disabled when `n_trials` is [`None`](https://docs.python.org/3/library/constants.html#None),
`timeout` is not [`None`](https://docs.python.org/3/library/constants.html#None), and `n_jobs` \(\ne 1\).



Raises:
[**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError) – If nested invocation of this method occurs.



Return type:
None







set_metric_names(*metric_names*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.set_metric_names)[](#optuna.study.Study.set_metric_names)
Set metric names.


This method names each dimension of the returned values of the objective function.
It is particularly useful in multi-objective optimization. The metric names are
mainly referenced by the visualization functions.


Example


```
import optuna
import pandas


def objective(trial):
    x = trial.suggest_float("x", 0, 10)
    return x**2, x + 1


study = optuna.create_study(directions=["minimize", "minimize"])
study.set_metric_names(["x**2", "x+1"])
study.optimize(objective, n_trials=3)

df = study.trials_dataframe(multi_index=True)
assert isinstance(df, pandas.DataFrame)
assert list(df.get("values").keys()) == ["x**2", "x+1"]
```




See also


The names set by this method are used in [`trials_dataframe()`](#optuna.study.Study.trials_dataframe)
and [`plot_pareto_front()`](https://optuna.readthedocs.io/en/stable/reference/visualization/generated/optuna.visualization.plot_pareto_front.html#optuna.visualization.plot_pareto_front).




Parameters:
**metric_names** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*]*) – A list of metric names for the objective function.



Return type:
None





Note


Added in v3.2.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.2.0](https://github.com/optuna/optuna/releases/tag/v3.2.0).






set_system_attr(*key*, *value*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.set_system_attr)[](#optuna.study.Study.set_system_attr)
Set a system attribute to the study.


Note that Optuna internally uses this method to save system messages. Please use
[`set_user_attr()`](#optuna.study.Study.set_user_attr) to set users’ attributes.



Parameters:
- **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A key string of the attribute.
- **value** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any)) – A value of the attribute. The value should be JSON serializable.



Return type:
None





Warning


Deprecated in v3.1.0. This feature will be removed in the future. The removal of this
feature is currently scheduled for v5.0.0, but this schedule is subject to change.
See [https://github.com/optuna/optuna/releases/tag/v3.1.0](https://github.com/optuna/optuna/releases/tag/v3.1.0).






set_user_attr(*key*, *value*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.set_user_attr)[](#optuna.study.Study.set_user_attr)
Set a user attribute to the study.



See also


See [`user_attrs`](#optuna.study.Study.user_attrs) for related attribute.




See also


See the recipe on [User Attributes](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/003_attributes.html#attributes).



Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", 0, 1)
    y = trial.suggest_float("y", 0, 1)
    return x**2 + y**2


study = optuna.create_study()

study.set_user_attr("objective function", "quadratic function")
study.set_user_attr("dimensions", 2)
study.set_user_attr("contributors", ["Akiba", "Sano"])

assert study.user_attrs == {
    "objective function": "quadratic function",
    "dimensions": 2,
    "contributors": ["Akiba", "Sano"],
}
```




Parameters:
- **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A key string of the attribute.
- **value** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any)) – A value of the attribute. The value should be JSON serializable.



Return type:
None







stop()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.stop)[](#optuna.study.Study.stop)
Exit from the current optimization loop after the running trials finish.


This method lets the running [`optimize()`](#optuna.study.Study.optimize) method return
immediately after all trials which the [`optimize()`](#optuna.study.Study.optimize) method
spawned finishes.
This method does not affect any behaviors of parallel or successive study processes.
This method only works when it is called inside an objective function or callback.


Example


```
import optuna


def objective(trial):
    if trial.number == 4:
        trial.study.stop()
    x = trial.suggest_float("x", 0, 10)
    return x**2


study = optuna.create_study()
study.optimize(objective, n_trials=10)
assert len(study.trials) == 5
```




Return type:
None







*property *system_attrs*: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*[](#optuna.study.Study.system_attrs)
Return system attributes.



Returns:
A dictionary containing all system attributes.





Warning


Deprecated in v3.1.0. This feature will be removed in the future. The removal of this
feature is currently scheduled for v5.0.0, but this schedule is subject to change.
See [https://github.com/optuna/optuna/releases/tag/v3.1.0](https://github.com/optuna/optuna/releases/tag/v3.1.0).






tell(*trial*, *values=None*, *state=None*, *skip_if_finished=False*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.tell)[](#optuna.study.Study.tell)
Finish a trial created with [`ask()`](#optuna.study.Study.ask).



See also


The [Ask-and-Tell Interface](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html#ask-and-tell) tutorial provides use-cases with examples.



Example


```
import optuna
from optuna.trial import TrialState


def f(x):
    return (x - 2) ** 2


def df(x):
    return 2 * x - 4


study = optuna.create_study()

n_trials = 30

for _ in range(n_trials):
    trial = study.ask()

    lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)

    # Iterative gradient descent objective function.
    x = 3  # Initial value.
    for step in range(128):
        y = f(x)

        trial.report(y, step=step)

        if trial.should_prune():
            # Finish the trial with the pruned state.
            study.tell(trial, state=TrialState.PRUNED)
            break

        gy = df(x)
        x -= gy * lr
    else:
        # Finish the trial with the final value after all iterations.
        study.tell(trial, y)
```




Parameters:
- **trial** ([*Trial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)* | *[*int*](https://docs.python.org/3/library/functions.html#int)) – A [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial) object or a trial number.
- **values** ([*float*](https://docs.python.org/3/library/functions.html#float)* | **Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Optional objective value or a sequence of such values in case the study is used
for multi-objective optimization. Argument must be provided if `state` is
[`COMPLETE`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.COMPLETE) and should be [`None`](https://docs.python.org/3/library/constants.html#None) if `state`
is [`FAIL`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.FAIL) or
[`PRUNED`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.PRUNED).
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)* | **None*) – State to be reported. Must be [`None`](https://docs.python.org/3/library/constants.html#None),
[`COMPLETE`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.COMPLETE),
[`FAIL`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.FAIL) or
[`PRUNED`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.PRUNED).
If `state` is [`None`](https://docs.python.org/3/library/constants.html#None),
it will be updated to [`COMPLETE`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.COMPLETE)
or [`FAIL`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState.FAIL) depending on whether
validation for `values` reported succeed or not.
- **skip_if_finished** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Flag to control whether exception should be raised when values for already
finished trial are told. If [`True`](https://docs.python.org/3/library/constants.html#True), tell is skipped without any error
when the trial is already finished.



Returns:
A [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) representing the resulting trial.
A returned trial is deep copied thus user can modify it as needed.



Return type:
[FrozenTrial](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)







*property *trials*: [list](https://docs.python.org/3/library/stdtypes.html#list)[[FrozenTrial](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)]*[](#optuna.study.Study.trials)
Return all trials in the study.


The returned trials are ordered by trial number.


This is a short form of `self.get_trials(deepcopy=True, states=None)`.



Returns:
A list of [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) objects.



See also


See [`get_trials()`](#optuna.study.Study.get_trials) for related method.








trials_dataframe(*attrs=('number', 'value', 'datetime_start', 'datetime_complete', 'duration', 'params', 'user_attrs', 'system_attrs', 'state')*, *multi_index=False*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#Study.trials_dataframe)[](#optuna.study.Study.trials_dataframe)
Export trials as a pandas [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).


The [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) provides various features to analyze studies. It is also useful to draw a
histogram of objective values and to export trials as a CSV file.
If there are no trials, an empty [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) is returned.


Example


```
import optuna
import pandas


def objective(trial):
    x = trial.suggest_float("x", -1, 1)
    return x**2


study = optuna.create_study()
study.optimize(objective, n_trials=3)

# Create a dataframe from the study.
df = study.trials_dataframe()
assert isinstance(df, pandas.DataFrame)
assert df.shape[0] == 3  # n_trials.
```




Parameters:
- **attrs** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **...**]*) – Specifies field names of [`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) to include them to a
DataFrame of trials.
- **multi_index** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Specifies whether the returned [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) employs [MultiIndex](https://pandas.pydata.org/pandas-docs/stable/advanced.html) or not. Columns that
are hierarchical by nature such as `(params, x)` will be flattened to
`params_x` when set to [`False`](https://docs.python.org/3/library/constants.html#False).



Returns:
A pandas [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) of trials in the [`Study`](#optuna.study.Study).



Return type:
pd.DataFrame





Note


If `value` is in `attrs` during multi-objective optimization, it is implicitly
replaced with `values`.




Note


If [`set_metric_names()`](#optuna.study.Study.set_metric_names) is called, the `value` or `values`
is implicitly replaced with the dictionary with the objective name as key and the
objective value as value.






*property *user_attrs*: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*[](#optuna.study.Study.user_attrs)
Return user attributes.



See also


See [`set_user_attr()`](#optuna.study.Study.set_user_attr) for related method.



Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", 0, 1)
    y = trial.suggest_float("y", 0, 1)
    return x**2 + y**2


study = optuna.create_study()

study.set_user_attr("objective function", "quadratic function")
study.set_user_attr("dimensions", 2)
study.set_user_attr("contributors", ["Akiba", "Sano"])

assert study.user_attrs == {
    "objective function": "quadratic function",
    "dimensions": 2,
    "contributors": ["Akiba", "Sano"],
}
```




Returns:
A dictionary containing all user attributes.

---

## optuna.trial.Trial — Optuna 4.6.0 documentation
<a id="optunatrialTrial-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html

# optuna.trial.Trial[](#optuna-trial-trial)




*class *optuna.trial.Trial(*study*, *trial_id*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial)[](#optuna.trial.Trial)
A trial is a process of evaluating an objective function.


This object is passed to an objective function and provides interfaces to get parameter
suggestion, manage the trial’s state, and set/get user-defined attributes of the trial.


Note that the direct use of this constructor is not recommended.
This object is seamlessly instantiated and passed to the objective function behind
the [`optuna.study.Study.optimize()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.optimize) method; hence library users do not care about
instantiation of this object.



Parameters:
- **study** ([*optuna.study.Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – A [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) object.
- **trial_id** ([*int*](https://docs.python.org/3/library/functions.html#int)) – A trial ID that is automatically generated.




Methods




[`report`](#optuna.trial.Trial.report)(value, step)


Report an objective function value for a given step.



[`set_system_attr`](#optuna.trial.Trial.set_system_attr)(key, value)


Set system attributes to the trial.



[`set_user_attr`](#optuna.trial.Trial.set_user_attr)(key, value)


Set user attributes to the trial.



[`should_prune`](#optuna.trial.Trial.should_prune)()


Suggest whether the trial should be pruned or not.



[`suggest_categorical`](#optuna.trial.Trial.suggest_categorical)()


Suggest a value for the categorical parameter.



[`suggest_discrete_uniform`](#optuna.trial.Trial.suggest_discrete_uniform)(name, low, high, q)


Suggest a value for the discrete parameter.



[`suggest_float`](#optuna.trial.Trial.suggest_float)(name, low, high, *[, step, log])


Suggest a value for the floating point parameter.



[`suggest_int`](#optuna.trial.Trial.suggest_int)(name, low, high, *[, step, log])


Suggest a value for the integer parameter.



[`suggest_loguniform`](#optuna.trial.Trial.suggest_loguniform)(name, low, high)


Suggest a value for the continuous parameter.



[`suggest_uniform`](#optuna.trial.Trial.suggest_uniform)(name, low, high)


Suggest a value for the continuous parameter.





Attributes




[`datetime_start`](#optuna.trial.Trial.datetime_start)


Return start datetime.



[`distributions`](#optuna.trial.Trial.distributions)


Return distributions of parameters to be optimized.



[`number`](#optuna.trial.Trial.number)


Return trial's number which is consecutive and unique in a study.



[`params`](#optuna.trial.Trial.params)


Return parameters to be optimized.



`relative_params`




[`system_attrs`](#optuna.trial.Trial.system_attrs)


Return system attributes.



[`user_attrs`](#optuna.trial.Trial.user_attrs)


Return user attributes.







*property *datetime_start*: [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime) | [None](https://docs.python.org/3/library/constants.html#None)*[](#optuna.trial.Trial.datetime_start)
Return start datetime.



Returns:
Datetime where the [`Trial`](#optuna.trial.Trial) started.







*property *distributions*: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), BaseDistribution]*[](#optuna.trial.Trial.distributions)
Return distributions of parameters to be optimized.



Returns:
A dictionary containing all distributions.







*property *number*: [int](https://docs.python.org/3/library/functions.html#int)*[](#optuna.trial.Trial.number)
Return trial’s number which is consecutive and unique in a study.



Returns:
A trial number.







*property *params*: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*[](#optuna.trial.Trial.params)
Return parameters to be optimized.



Returns:
A dictionary containing all parameters.







report(*value*, *step*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.report)[](#optuna.trial.Trial.report)
Report an objective function value for a given step.


The reported values are used by the pruners to determine whether this trial should be
pruned.



See also


Please refer to [`BasePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner).




Note


The reported value is converted to `float` type by applying `float()`
function internally. Thus, it accepts all float-like types (e.g., `numpy.float32`).
If the conversion fails, a `TypeError` is raised.




Note


If this method is called multiple times at the same `step` in a trial,
the reported `value` only the first time is stored and the reported values
from the second time are ignored.




Note


[`report()`](#optuna.trial.Trial.report) does not support multi-objective
optimization.



Example


Report intermediate scores of [SGDClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html) training.


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)


def objective(trial):
    clf = SGDClassifier(random_state=0)
    for step in range(100):
        clf.partial_fit(X_train, y_train, np.unique(y))
        intermediate_value = clf.score(X_valid, y_valid)
        trial.report(intermediate_value, step=step)
        if trial.should_prune():
            raise optuna.TrialPruned()

    return clf.score(X_valid, y_valid)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=3)
```




Parameters:
- **value** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A value returned from the objective function.
- **step** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Step of the trial (e.g., Epoch of neural network training). Note that pruners
assume that `step` starts at zero. For example,
[`MedianPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html#optuna.pruners.MedianPruner) simply checks if `step` is less than
`n_warmup_steps` as the warmup mechanism.
`step` must be a positive integer.



Return type:
None







set_system_attr(*key*, *value*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.set_system_attr)[](#optuna.trial.Trial.set_system_attr)
Set system attributes to the trial.


Note that Optuna internally uses this method to save system messages such as failure
reason of trials. Please use [`set_user_attr()`](#optuna.trial.Trial.set_user_attr) to set users’
attributes.



Parameters:
- **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A key string of the attribute.
- **value** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any)) – A value of the attribute. The value should be JSON serializable.



Return type:
None





Warning


Deprecated in v3.1.0. This feature will be removed in the future. The removal of this
feature is currently scheduled for v5.0.0, but this schedule is subject to change.
See [https://github.com/optuna/optuna/releases/tag/v3.1.0](https://github.com/optuna/optuna/releases/tag/v3.1.0).






set_user_attr(*key*, *value*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.set_user_attr)[](#optuna.trial.Trial.set_user_attr)
Set user attributes to the trial.


The user attributes in the trial can be access via [`optuna.trial.Trial.user_attrs()`](#optuna.trial.Trial.user_attrs).



See also


See the recipe on [User Attributes](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/003_attributes.html#attributes).



Example


Save fixed hyperparameters of neural network training.


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state=0)


def objective(trial):
    trial.set_user_attr("BATCHSIZE", 128)
    momentum = trial.suggest_float("momentum", 0, 1.0)
    clf = MLPClassifier(
        hidden_layer_sizes=(100, 50),
        batch_size=trial.user_attrs["BATCHSIZE"],
        momentum=momentum,
        solver="sgd",
        random_state=0,
    )
    clf.fit(X_train, y_train)

    return clf.score(X_valid, y_valid)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=3)
assert "BATCHSIZE" in study.best_trial.user_attrs.keys()
assert study.best_trial.user_attrs["BATCHSIZE"] == 128
```




Parameters:
- **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A key string of the attribute.
- **value** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any)) – A value of the attribute. The value should be JSON serializable.



Return type:
None







should_prune()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.should_prune)[](#optuna.trial.Trial.should_prune)
Suggest whether the trial should be pruned or not.


The suggestion is made by a pruning algorithm associated with the trial and is based on
previously reported values. The algorithm can be specified when constructing a
[`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study).



Note


If no values have been reported, the algorithm cannot make meaningful suggestions.
Similarly, if this method is called multiple times with the exact same set of reported
values, the suggestions will be the same.




See also


Please refer to the example code in [`optuna.trial.Trial.report()`](#optuna.trial.Trial.report).




Note


[`should_prune()`](#optuna.trial.Trial.should_prune) does not support multi-objective
optimization.




Returns:
A boolean value. If [`True`](https://docs.python.org/3/library/constants.html#True), the trial should be pruned according to the
configured pruning algorithm. Otherwise, the trial should continue.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)







suggest_categorical(*name: [str](https://docs.python.org/3/library/stdtypes.html#str)*, *choices: [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[None](https://docs.python.org/3/library/constants.html#None)]*) → [None](https://docs.python.org/3/library/constants.html#None)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.suggest_categorical)[](#optuna.trial.Trial.suggest_categorical)

suggest_categorical(*name: [str](https://docs.python.org/3/library/stdtypes.html#str)*, *choices: [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[bool](https://docs.python.org/3/library/functions.html#bool)]*) → [bool](https://docs.python.org/3/library/functions.html#bool)

suggest_categorical(*name: [str](https://docs.python.org/3/library/stdtypes.html#str)*, *choices: [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[int](https://docs.python.org/3/library/functions.html#int)]*) → [int](https://docs.python.org/3/library/functions.html#int)

suggest_categorical(*name: [str](https://docs.python.org/3/library/stdtypes.html#str)*, *choices: [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[float](https://docs.python.org/3/library/functions.html#float)]*) → [float](https://docs.python.org/3/library/functions.html#float)

suggest_categorical(*name: [str](https://docs.python.org/3/library/stdtypes.html#str)*, *choices: [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[str](https://docs.python.org/3/library/stdtypes.html#str)]*) → [str](https://docs.python.org/3/library/stdtypes.html#str)

suggest_categorical(*name: [str](https://docs.python.org/3/library/stdtypes.html#str)*, *choices: [Sequence](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)[[None](https://docs.python.org/3/library/constants.html#None) | [bool](https://docs.python.org/3/library/functions.html#bool) | [int](https://docs.python.org/3/library/functions.html#int) | [float](https://docs.python.org/3/library/functions.html#float) | [str](https://docs.python.org/3/library/stdtypes.html#str)]*) → [None](https://docs.python.org/3/library/constants.html#None) | [bool](https://docs.python.org/3/library/functions.html#bool) | [int](https://docs.python.org/3/library/functions.html#int) | [float](https://docs.python.org/3/library/functions.html#float) | [str](https://docs.python.org/3/library/stdtypes.html#str)
Suggest a value for the categorical parameter.


The value is sampled from `choices`.


Example


Suggest a kernel function of [SVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html).


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)


def objective(trial):
    kernel = trial.suggest_categorical("kernel", ["linear", "poly", "rbf"])
    clf = SVC(kernel=kernel, gamma="scale", random_state=0)
    clf.fit(X_train, y_train)
    return clf.score(X_valid, y_valid)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=3)
```




Parameters:
- **name** – A parameter name.
- **choices** – Parameter value candidates.





See also


[`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html#optuna.distributions.CategoricalDistribution).




Returns:
A suggested value.





See also


[Pythonic Search Space](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html#configurations) tutorial describes more details and flexible usages.






suggest_discrete_uniform(*name*, *low*, *high*, *q*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.suggest_discrete_uniform)[](#optuna.trial.Trial.suggest_discrete_uniform)
Suggest a value for the discrete parameter.


The value is sampled from the range \([\mathsf{low}, \mathsf{high}]\),
and the step of discretization is \(q\). More specifically,
this method returns one of the values in the sequence
\(\mathsf{low}, \mathsf{low} + q, \mathsf{low} + 2 q, \dots,
\mathsf{low} + k q \le \mathsf{high}\),
where \(k\) denotes an integer. Note that \(high\) may be changed due to round-off
errors if \(q\) is not an integer. Please check warning messages to find the changed
values.



Parameters:
- **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A parameter name.
- **low** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Lower endpoint of the range of suggested values. `low` is included in the range.
- **high** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Upper endpoint of the range of suggested values. `high` is included in the range.
- **q** ([*float*](https://docs.python.org/3/library/functions.html#float)) – A step of discretization.



Returns:
A suggested float value.



Return type:
[float](https://docs.python.org/3/library/functions.html#float)





Warning


Deprecated in v3.0.0. This feature will be removed in the future. The removal of this
feature is currently scheduled for v6.0.0, but this schedule is subject to change.
See [https://github.com/optuna/optuna/releases/tag/v3.0.0](https://github.com/optuna/optuna/releases/tag/v3.0.0).


Use suggest_float(…, step=…) instead.






suggest_float(*name*, *low*, *high*, ***, *step=None*, *log=False*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.suggest_float)[](#optuna.trial.Trial.suggest_float)
Suggest a value for the floating point parameter.


Example


Suggest a momentum, learning rate and scaling factor of learning rate
for neural network training.


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state=0)


def objective(trial):
    momentum = trial.suggest_float("momentum", 0.0, 1.0)
    learning_rate_init = trial.suggest_float(
        "learning_rate_init", 1e-5, 1e-3, log=True
    )
    power_t = trial.suggest_float("power_t", 0.2, 0.8, step=0.1)
    clf = MLPClassifier(
        hidden_layer_sizes=(100, 50),
        momentum=momentum,
        learning_rate_init=learning_rate_init,
        solver="sgd",
        random_state=0,
        power_t=power_t,
    )
    clf.fit(X_train, y_train)

    return clf.score(X_valid, y_valid)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=3)
```




Parameters:
- **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A parameter name.
- **low** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Lower endpoint of the range of suggested values. `low` is included in the range.
`low` must be less than or equal to `high`. If `log` is [`True`](https://docs.python.org/3/library/constants.html#True),
`low` must be larger than 0.
- **high** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Upper endpoint of the range of suggested values. `high` is included in the range.
`high` must be greater than or equal to `low`.
- **step** ([*float*](https://docs.python.org/3/library/functions.html#float)* | **None*) –

A step of discretization.



Note


The `step` and `log` arguments cannot be used at the same time. To set
the `step` argument to a float number, set the `log` argument to
[`False`](https://docs.python.org/3/library/constants.html#False).
- **log** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

A flag to sample the value from the log domain or not.
If `log` is true, the value is sampled from the range in the log domain.
Otherwise, the value is sampled from the range in the linear domain.



Note


The `step` and `log` arguments cannot be used at the same time. To set
the `log` argument to [`True`](https://docs.python.org/3/library/constants.html#True), set the `step` argument to [`None`](https://docs.python.org/3/library/constants.html#None).



Returns:
A suggested float value.



Return type:
[float](https://docs.python.org/3/library/functions.html#float)





See also


[Pythonic Search Space](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html#configurations) tutorial describes more details and flexible usages.






suggest_int(*name*, *low*, *high*, ***, *step=1*, *log=False*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.suggest_int)[](#optuna.trial.Trial.suggest_int)
Suggest a value for the integer parameter.


The value is sampled from the integers in \([\mathsf{low}, \mathsf{high}]\).


Example


Suggest the number of trees in [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)


def objective(trial):
    n_estimators = trial.suggest_int("n_estimators", 50, 400)
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=0)
    clf.fit(X_train, y_train)
    return clf.score(X_valid, y_valid)


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=3)
```




Parameters:
- **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A parameter name.
- **low** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Lower endpoint of the range of suggested values. `low` is included in the range.
`low` must be less than or equal to `high`. If `log` is [`True`](https://docs.python.org/3/library/constants.html#True),
`low` must be larger than 0.
- **high** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Upper endpoint of the range of suggested values. `high` is included in the range.
`high` must be greater than or equal to `low`.
- **step** ([*int*](https://docs.python.org/3/library/functions.html#int)) –

A step of discretization.



Note


Note that \(\mathsf{high}\) is modified if the range is not divisible by
\(\mathsf{step}\). Please check the warning messages to find the changed
values.




Note


The method returns one of the values in the sequence
\(\mathsf{low}, \mathsf{low} + \mathsf{step}, \mathsf{low} + 2 *
\mathsf{step}, \dots, \mathsf{low} + k * \mathsf{step} \le
\mathsf{high}\), where \(k\) denotes an integer.




Note


The `step != 1` and `log` arguments cannot be used at the same time.
To set the `step` argument \(\mathsf{step} \ge 2\), set the
`log` argument to [`False`](https://docs.python.org/3/library/constants.html#False).
- **log** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

A flag to sample the value from the log domain or not.



Note


If `log` is true, at first, the range of suggested values is divided into
grid points of width 1. The range of suggested values is then converted to
a log domain, from which a value is sampled. The uniformly sampled
value is re-converted to the original domain and rounded to the nearest grid
point that we just split, and the suggested value is determined.
For example, if low = 2 and high = 8, then the range of suggested values is
[2, 3, 4, 5, 6, 7, 8] and lower values tend to be more sampled than higher
values.




Note


The `step != 1` and `log` arguments cannot be used at the same time.
To set the `log` argument to [`True`](https://docs.python.org/3/library/constants.html#True), set the `step` argument to 1.



Return type:
[int](https://docs.python.org/3/library/functions.html#int)





See also


[Pythonic Search Space](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/002_configurations.html#configurations) tutorial describes more details and flexible usages.






suggest_loguniform(*name*, *low*, *high*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.suggest_loguniform)[](#optuna.trial.Trial.suggest_loguniform)
Suggest a value for the continuous parameter.


The value is sampled from the range \([\mathsf{low}, \mathsf{high})\)
in the log domain. When \(\mathsf{low} = \mathsf{high}\), the value of
\(\mathsf{low}\) will be returned.



Parameters:
- **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A parameter name.
- **low** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Lower endpoint of the range of suggested values. `low` is included in the range.
- **high** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Upper endpoint of the range of suggested values. `high` is included in the range.



Returns:
A suggested float value.



Return type:
[float](https://docs.python.org/3/library/functions.html#float)





Warning


Deprecated in v3.0.0. This feature will be removed in the future. The removal of this
feature is currently scheduled for v6.0.0, but this schedule is subject to change.
See [https://github.com/optuna/optuna/releases/tag/v3.0.0](https://github.com/optuna/optuna/releases/tag/v3.0.0).


Use suggest_float(…, log=True) instead.






suggest_uniform(*name*, *low*, *high*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/trial/_trial.html#Trial.suggest_uniform)[](#optuna.trial.Trial.suggest_uniform)
Suggest a value for the continuous parameter.


The value is sampled from the range \([\mathsf{low}, \mathsf{high})\)
in the linear domain. When \(\mathsf{low} = \mathsf{high}\), the value of
\(\mathsf{low}\) will be returned.



Parameters:
- **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – A parameter name.
- **low** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Lower endpoint of the range of suggested values. `low` is included in the range.
- **high** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Upper endpoint of the range of suggested values. `high` is included in the range.



Returns:
A suggested float value.



Return type:
[float](https://docs.python.org/3/library/functions.html#float)





Warning


Deprecated in v3.0.0. This feature will be removed in the future. The removal of this
feature is currently scheduled for v6.0.0, but this schedule is subject to change.
See [https://github.com/optuna/optuna/releases/tag/v3.0.0](https://github.com/optuna/optuna/releases/tag/v3.0.0).


Use suggest_float instead.






*property *system_attrs*: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*[](#optuna.trial.Trial.system_attrs)
Return system attributes.



Returns:
A dictionary containing all system attributes.





Warning


Deprecated in v3.1.0. This feature will be removed in the future. The removal of this
feature is currently scheduled for v5.0.0, but this schedule is subject to change.
See [https://github.com/optuna/optuna/releases/tag/v3.1.0](https://github.com/optuna/optuna/releases/tag/v3.1.0).






*property *user_attrs*: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*[](#optuna.trial.Trial.user_attrs)
Return user attributes.



Returns:
A dictionary containing all user attributes.

---

## optuna.study.create_study — Optuna 4.6.0 documentation
<a id="optunastudycreate_study-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html

# optuna.study.create_study[](#optuna-study-create-study)




optuna.study.create_study(***, *storage=None*, *sampler=None*, *pruner=None*, *study_name=None*, *direction=None*, *load_if_exists=False*, *directions=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#create_study)[](#optuna.study.create_study)
Create a new [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study).


Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", 0, 10)
    return x**2


study = optuna.create_study()
study.optimize(objective, n_trials=3)
```




Parameters:
- **storage** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **storages.BaseStorage** | **None*) –

Database URL. If this argument is set to None,
[`InMemoryStorage`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.storages.InMemoryStorage.html#optuna.storages.InMemoryStorage) is used, and the
[`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) will not be persistent.



Note


> When a database URL is passed, Optuna internally uses SQLAlchemy to handle
> the database. Please refer to SQLAlchemy’s document for further details.
> If you want to specify non-default options to SQLAlchemy Engine, you can
> instantiate RDBStorage with your desired options and
> pass it to the storage argument instead of a URL.
- **sampler** (*'samplers.BaseSampler'** | **None*) – A sampler object that implements background algorithm for value suggestion.
If [`None`](https://docs.python.org/3/library/constants.html#None) is specified, [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) is used during
single-objective optimization and [`NSGAIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html#optuna.samplers.NSGAIISampler) during
multi-objective optimization. See also [`samplers`](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html#module-optuna.samplers).
- **pruner** ([*pruners.BasePruner*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner)* | **None*) – A pruner object that decides early stopping of unpromising trials. If [`None`](https://docs.python.org/3/library/constants.html#None)
is specified, [`MedianPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html#optuna.pruners.MedianPruner) is used as the default. See
also [`pruners`](https://optuna.readthedocs.io/en/stable/reference/pruners.html#module-optuna.pruners).
- **study_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **None*) – Study’s name. If this argument is set to None, a unique name is generated
automatically.
- **direction** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | *[*StudyDirection*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection)* | **None*) –

Direction of optimization. Set `minimize` for minimization and `maximize` for
maximization. You can also pass the corresponding [`StudyDirection`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection)
object. `direction` and `directions` must not be specified at the same time.



Note


If none of direction and directions are specified, the direction of the study
is set to “minimize”.
- **load_if_exists** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Flag to control the behavior to handle a conflict of study names.
In the case where a study named `study_name` already exists in the `storage`,
a [`DuplicatedStudyError`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.exceptions.DuplicatedStudyError.html#optuna.exceptions.DuplicatedStudyError) is raised if `load_if_exists` is
set to [`False`](https://docs.python.org/3/library/constants.html#False).
Otherwise, the creation of the study is skipped, and the existing one is returned.
- **directions** (*Sequence**[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)* | *[*StudyDirection*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.StudyDirection.html#optuna.study.StudyDirection)*] **| **None*) – A sequence of directions during multi-objective optimization.
`direction` and `directions` must not be specified at the same time.



Returns:
A [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) object.



Return type:
[Study](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)





See also


[`optuna.create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.create_study.html#optuna.create_study) is an alias of [`optuna.study.create_study()`](#optuna.study.create_study).




See also


The [Saving/Resuming Study with RDB Backend](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/001_rdb.html#rdb) tutorial provides concrete examples to save and resume optimization using
RDB.

---

## optuna.study.load_study — Optuna 4.6.0 documentation
<a id="optunastudyload_study-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.load_study.html

# optuna.study.load_study[](#optuna-study-load-study)




optuna.study.load_study(***, *study_name*, *storage*, *sampler=None*, *pruner=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#load_study)[](#optuna.study.load_study)
Load the existing [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) that has the specified name.


Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", 0, 10)
    return x**2


study = optuna.create_study(storage="sqlite:///example.db", study_name="my_study")
study.optimize(objective, n_trials=3)

loaded_study = optuna.load_study(study_name="my_study", storage="sqlite:///example.db")
assert len(loaded_study.trials) == len(study.trials)
```




Parameters:
- **study_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **None*) – Study’s name. Each study has a unique name as an identifier. If [`None`](https://docs.python.org/3/library/constants.html#None), checks
whether the storage contains a single study, and if so loads that study.
`study_name` is required if there are multiple studies in the storage.
- **storage** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **storages.BaseStorage*) – Database URL such as `sqlite:///example.db`. Please see also the documentation of
[`create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html#optuna.study.create_study) for further details.
- **sampler** (*'samplers.BaseSampler'** | **None*) – A sampler object that implements background algorithm for value suggestion.
If [`None`](https://docs.python.org/3/library/constants.html#None) is specified, [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) is used
as the default. See also [`samplers`](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html#module-optuna.samplers).
- **pruner** ([*pruners.BasePruner*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner)* | **None*) – A pruner object that decides early stopping of unpromising trials.
If [`None`](https://docs.python.org/3/library/constants.html#None) is specified, [`MedianPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html#optuna.pruners.MedianPruner) is used
as the default. See also [`pruners`](https://optuna.readthedocs.io/en/stable/reference/pruners.html#module-optuna.pruners).



Returns:
A [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) object.



Return type:
[Study](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)





See also


[`optuna.load_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.load_study.html#optuna.load_study) is an alias of [`optuna.study.load_study()`](#optuna.study.load_study).

---

## optuna.samplers.BaseSampler — Optuna 4.6.0 documentation
<a id="optunasamplersBaseSampler-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html

# optuna.samplers.BaseSampler[](#optuna-samplers-basesampler)




*class *optuna.samplers.BaseSampler[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_base.html#BaseSampler)[](#optuna.samplers.BaseSampler)
Base class for samplers.


Optuna combines two types of sampling strategies, which are called *relative sampling* and
*independent sampling*.


*The relative sampling* determines values of multiple parameters simultaneously so that
sampling algorithms can use relationship between parameters (e.g., correlation).
Target parameters of the relative sampling are described in a relative search space, which
is determined by [`infer_relative_search_space()`](#optuna.samplers.BaseSampler.infer_relative_search_space).


*The independent sampling* determines a value of a single parameter without considering any
relationship between parameters. Target parameters of the independent sampling are the
parameters not described in the relative search space.


More specifically, parameters are sampled by the following procedure.
At the beginning of a trial, [`infer_relative_search_space()`](#optuna.samplers.BaseSampler.infer_relative_search_space)
is called to determine the relative search space for the trial.
During the execution of the objective function,
[`sample_relative()`](#optuna.samplers.BaseSampler.sample_relative) is called only once
when sampling the parameters belonging to the relative search space for the first time.
[`sample_independent()`](#optuna.samplers.BaseSampler.sample_independent) is used to sample
parameters that don’t belong to the relative search space.


The following figure depicts the lifetime of a trial and how the above three methods are
called in the trial.


![../../../_images/sampling-sequence.png](https://optuna.readthedocs.io/en/stable/_images/sampling-sequence.png)

  


Methods




[`after_trial`](#optuna.samplers.BaseSampler.after_trial)(study, trial, state, values)


Trial post-processing.



[`before_trial`](#optuna.samplers.BaseSampler.before_trial)(study, trial)


Trial pre-processing.



[`infer_relative_search_space`](#optuna.samplers.BaseSampler.infer_relative_search_space)(study, trial)


Infer the search space that will be used by relative sampling in the target trial.



[`reseed_rng`](#optuna.samplers.BaseSampler.reseed_rng)()


Reseed sampler's random number generator.



[`sample_independent`](#optuna.samplers.BaseSampler.sample_independent)(study, trial, param_name, ...)


Sample a parameter for a given distribution.



[`sample_relative`](#optuna.samplers.BaseSampler.sample_relative)(study, trial, search_space)


Sample parameters in a given search space.







after_trial(*study*, *trial*, *state*, *values*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_base.html#BaseSampler.after_trial)[](#optuna.samplers.BaseSampler.after_trial)
Trial post-processing.


This method is called after the objective function returns and right before the trial is
finished and its state is stored.



Note


Added in v2.4.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.4.0](https://github.com/optuna/optuna/releases/tag/v2.4.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)) – Resulting trial state.
- **values** (*Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Resulting trial values. Guaranteed to not be [`None`](https://docs.python.org/3/library/constants.html#None) if trial succeeded.



Return type:
None







before_trial(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_base.html#BaseSampler.before_trial)[](#optuna.samplers.BaseSampler.before_trial)
Trial pre-processing.


This method is called before the objective function is called and right after the trial is
instantiated. More precisely, this method is called during trial initialization, just
before the [`infer_relative_search_space()`](#optuna.samplers.BaseSampler.infer_relative_search_space) call. In other
words, it is responsible for pre-processing that should be done before inferring the search
space.



Note


Added in v3.3.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.



Return type:
None







*abstractmethod *infer_relative_search_space(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_base.html#BaseSampler.infer_relative_search_space)[](#optuna.samplers.BaseSampler.infer_relative_search_space)
Infer the search space that will be used by relative sampling in the target trial.


This method is called right before [`sample_relative()`](#optuna.samplers.BaseSampler.sample_relative)
method, and the search space returned by this method is passed to it. The parameters not
contained in the search space will be sampled by using
[`sample_independent()`](#optuna.samplers.BaseSampler.sample_independent) method.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.



Returns:
A dictionary containing the parameter names and parameter’s distributions.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), BaseDistribution]





See also


Please refer to [`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space) as an
implementation of [`infer_relative_search_space()`](#optuna.samplers.BaseSampler.infer_relative_search_space).






reseed_rng()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_base.html#BaseSampler.reseed_rng)[](#optuna.samplers.BaseSampler.reseed_rng)
Reseed sampler’s random number generator.


This method is called by the [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) instance if trials are executed
in parallel with the option `n_jobs>1`. In that case, the sampler instance will be
replicated including the state of the random number generator, and they may suggest the
same values. To prevent this issue, this method assigns a different seed to each random
number generator.



Return type:
None







*abstractmethod *sample_independent(*study*, *trial*, *param_name*, *param_distribution*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_base.html#BaseSampler.sample_independent)[](#optuna.samplers.BaseSampler.sample_independent)
Sample a parameter for a given distribution.


This method is called only for the parameters not contained in the search space returned
by [`sample_relative()`](#optuna.samplers.BaseSampler.sample_relative) method. This method is suitable
for sampling algorithms that do not use relationship between parameters such as random
sampling and TPE.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **param_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the sampled parameter.
- **param_distribution** (*BaseDistribution*) – Distribution object that specifies a prior and/or scale of the sampling algorithm.



Returns:
A parameter value.



Return type:
Any







*abstractmethod *sample_relative(*study*, *trial*, *search_space*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_base.html#BaseSampler.sample_relative)[](#optuna.samplers.BaseSampler.sample_relative)
Sample parameters in a given search space.


This method is called once at the beginning of each trial, i.e., right before the
evaluation of the objective function. This method is suitable for sampling algorithms
that use relationship between parameters such as Gaussian Process and CMA-ES.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **search_space** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]*) – The search space returned by
[`infer_relative_search_space()`](#optuna.samplers.BaseSampler.infer_relative_search_space).



Returns:
A dictionary containing the parameter names and the values.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]

---

## optuna.samplers.TPESampler — Optuna 4.6.0 documentation
<a id="optunasamplersTPESampler-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html

# optuna.samplers.TPESampler[](#optuna-samplers-tpesampler)




*class *optuna.samplers.TPESampler(***, *consider_prior=True*, *prior_weight=1.0*, *consider_magic_clip=True*, *consider_endpoints=False*, *n_startup_trials=10*, *n_ei_candidates=24*, *gamma=<function default_gamma>*, *weights=<function default_weights>*, *seed=None*, *multivariate=False*, *group=False*, *warn_independent_sampling=True*, *constant_liar=False*, *constraints_func=None*, *categorical_distance_func=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler)[](#optuna.samplers.TPESampler)
Sampler using TPE (Tree-structured Parzen Estimator) algorithm.


On each trial, for each parameter, TPE fits one Gaussian Mixture Model (GMM) `l(x)` to
the set of parameter values associated with the best objective values, and another GMM
`g(x)` to the remaining parameter values. It chooses the parameter value `x` that
maximizes the ratio `l(x)/g(x)`.


For further information about TPE algorithm, please refer to the following papers:


- [Algorithms for Hyper-Parameter Optimization](https://papers.nips.cc/paper/4443-algorithms-for-hyper-parameter-optimization.pdf)
- [Making a Science of Model Search: Hyperparameter Optimization in Hundreds of
Dimensions for Vision Architectures](http://proceedings.mlr.press/v28/bergstra13.pdf)
- [Tree-Structured Parzen Estimator: Understanding Its Algorithm Components and Their Roles for
Better Empirical Performance](https://arxiv.org/abs/2304.11127)


For multi-objective TPE (MOTPE), please refer to the following papers:


- [Multiobjective Tree-Structured Parzen Estimator for Computationally Expensive Optimization
Problems](https://doi.org/10.1145/3377930.3389817)
- [Multiobjective Tree-Structured Parzen Estimator](https://doi.org/10.1613/jair.1.13188)


For the categorical_distance_func, please refer to the following paper:


- [Tree-Structured Parzen Estimator Can Solve Black-Box Combinatorial Optimization More
Efficiently](https://arxiv.org/abs/2507.08053)


Please also check our articles:


- [Significant Speed Up of Multi-Objective TPESampler in Optuna v4.0.0](https://medium.com/optuna/significant-speed-up-of-multi-objective-tpesampler-in-optuna-v4-0-0-2bacdcd1d99b)
- [Multivariate TPE Makes Optuna Even More Powerful](https://medium.com/optuna/multivariate-tpe-makes-optuna-even-more-powerful-63c4bfbaebe2)


Example


An example of a single-objective optimization is as follows:


```
import optuna
from optuna.samplers import TPESampler


def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    return x**2


study = optuna.create_study(sampler=TPESampler())
study.optimize(objective, n_trials=10)
```




Note


[`TPESampler`](#optuna.samplers.TPESampler), which became much faster in v4.0.0, c.f. [our article](https://medium.com/optuna/significant-speed-up-of-multi-objective-tpesampler-in-optuna-v4-0-0-2bacdcd1d99b),
can handle multi-objective optimization with many trials as well.
Please note that [`NSGAIISampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html#optuna.samplers.NSGAIISampler) will be used by default for
multi-objective optimization, so if users would like to use
[`TPESampler`](#optuna.samplers.TPESampler) for multi-objective optimization, `sampler` must be
explicitly specified when study is created.




Parameters:
- **consider_prior** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

Enhance the stability of Parzen estimator by imposing a Gaussian prior when
[`True`](https://docs.python.org/3/library/constants.html#True). The prior is only effective if the sampling distribution is
either [`FloatDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.FloatDistribution.html#optuna.distributions.FloatDistribution),
or [`IntDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntDistribution.html#optuna.distributions.IntDistribution).



Warning


Deprecated in v4.3.0. `consider_prior` argument will be removed in the future.
The removal of this feature is currently scheduled for v6.0.0,
but this schedule is subject to change.
From v4.3.0 onward, `consider_prior` automatically falls back to `True`.
See [https://github.com/optuna/optuna/releases/tag/v4.3.0](https://github.com/optuna/optuna/releases/tag/v4.3.0).
- **prior_weight** ([*float*](https://docs.python.org/3/library/functions.html#float)) – The weight of the prior. This argument is used in
[`FloatDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.FloatDistribution.html#optuna.distributions.FloatDistribution),
[`IntDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntDistribution.html#optuna.distributions.IntDistribution), and
[`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html#optuna.distributions.CategoricalDistribution).
- **consider_magic_clip** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Enable a heuristic to limit the smallest variances of Gaussians used in
the Parzen estimator.
- **consider_endpoints** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Take endpoints of domains into account when calculating variances of Gaussians
in Parzen estimator. See the original paper for details on the heuristics
to calculate the variances.
- **n_startup_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The random sampling is used instead of the TPE algorithm until the given number
of trials finish in the same study.
- **n_ei_candidates** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of candidate samples used to calculate the expected improvement.
- **gamma** (*Callable**[**[*[*int*](https://docs.python.org/3/library/functions.html#int)*]**, *[*int*](https://docs.python.org/3/library/functions.html#int)*]*) – A function that takes the number of finished trials and returns the number
of trials to form a density function for samples with low grains.
See the original paper for more details.
- **weights** (*Callable**[**[*[*int*](https://docs.python.org/3/library/functions.html#int)*]**, **np.ndarray**]*) –

A function that takes the number of finished trials and returns a weight for them.
See [Making a Science of Model Search: Hyperparameter Optimization in Hundreds of
Dimensions for Vision Architectures](http://proceedings.mlr.press/v28/bergstra13.pdf) for more details.



Note


In the multi-objective case, this argument is only used to compute the weights of
bad trials, i.e., trials to construct g(x) in the [paper](https://papers.nips.cc/paper/4443-algorithms-for-hyper-parameter-optimization.pdf)
). The weights of good trials, i.e., trials to construct l(x), are computed by a
rule based on the hypervolume contribution proposed in the [paper of MOTPE](https://doi.org/10.1613/jair.1.13188).
- **seed** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) – Seed for random number generator.
- **multivariate** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), the multivariate TPE is used when suggesting parameters.
The multivariate TPE is reported to outperform the independent TPE. See [BOHB: Robust
and Efficient Hyperparameter Optimization at Scale](http://proceedings.mlr.press/v80/falkner18a.html) and [our article](https://medium.com/optuna/multivariate-tpe-makes-optuna-even-more-powerful-63c4bfbaebe2)
for more details.



Note


Added in v2.2.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v2.2.0](https://github.com/optuna/optuna/releases/tag/v2.2.0).
- **group** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this and `multivariate` are [`True`](https://docs.python.org/3/library/constants.html#True), the multivariate TPE with the group
decomposed search space is used when suggesting parameters.
The sampling algorithm decomposes the search space based on past trials and samples
from the joint distribution in each decomposed subspace.
The decomposed subspaces are a partition of the whole search space. Each subspace
is a maximal subset of the whole search space, which satisfies the following:
for a trial in completed trials, the intersection of the subspace and the search space
of the trial becomes subspace itself or an empty set.
Sampling from the joint distribution on the subspace is realized by multivariate TPE.
If `group` is [`True`](https://docs.python.org/3/library/constants.html#True), `multivariate` must be [`True`](https://docs.python.org/3/library/constants.html#True) as well.



Note


Added in v2.8.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v2.8.0](https://github.com/optuna/optuna/releases/tag/v2.8.0).



Example:


```
import optuna


def objective(trial):
    x = trial.suggest_categorical("x", ["A", "B"])
    if x == "A":
        return trial.suggest_float("y", -10, 10)
    else:
        return trial.suggest_int("z", -10, 10)


sampler = optuna.samplers.TPESampler(multivariate=True, group=True)
study = optuna.create_study(sampler=sampler)
study.optimize(objective, n_trials=10)
```
- **warn_independent_sampling** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If this is [`True`](https://docs.python.org/3/library/constants.html#True) and `multivariate=True`, a warning message is emitted when
the value of a parameter is sampled by using an independent sampler.
If `multivariate=False`, this flag has no effect.
- **constant_liar** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If [`True`](https://docs.python.org/3/library/constants.html#True), penalize running trials to avoid suggesting parameter configurations
nearby.



Note


Abnormally terminated trials often leave behind a record with a state of
`RUNNING` in the storage.
Such “zombie” trial parameters will be avoided by the constant liar algorithm
during subsequent sampling.
When using an [`RDBStorage`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.storages.RDBStorage.html#optuna.storages.RDBStorage), it is possible to enable the
`heartbeat_interval` to change the records for abnormally terminated trials to
`FAIL`.




Note


It is recommended to set this value to [`True`](https://docs.python.org/3/library/constants.html#True) during distributed
optimization to avoid having multiple workers evaluating similar parameter
configurations. In particular, if each objective function evaluation is costly
and the durations of the running states are significant, and/or the number of
workers is high.




Note


Added in v2.8.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v2.8.0](https://github.com/optuna/optuna/releases/tag/v2.8.0).
- **constraints_func** (*Callable**[**[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]**, **Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*]**] **| **None*) –

An optional function that computes the objective constraints. It must take a
[`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) and return the constraints. The return value must
be a sequence of [`float`](https://docs.python.org/3/library/functions.html#float) s. A value strictly larger than 0 means that a
constraints is violated. A value equal to or smaller than 0 is considered feasible.
If `constraints_func` returns more than one value for a trial, that trial is
considered feasible if and only if all values are equal to 0 or smaller.


The `constraints_func` will be evaluated after each successful trial.
The function won’t be called when trials fail or they are pruned, but this behavior is
subject to change in the future releases.



Note


Added in v3.0.0 as an experimental feature. The interface may change in newer
versions without prior notice.
See [https://github.com/optuna/optuna/releases/tag/v3.0.0](https://github.com/optuna/optuna/releases/tag/v3.0.0).
- **categorical_distance_func** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **Callable**[**[**CategoricalChoiceType**, **CategoricalChoiceType**]**, *[*float*](https://docs.python.org/3/library/functions.html#float)*]**] **| **None*) –

A dictionary of distance functions for categorical parameters. The key is the name of
the categorical parameter and the value is a distance function that takes two
`CategoricalChoiceType` s and returns a [`float`](https://docs.python.org/3/library/functions.html#float)
value. The distance function must return a non-negative value.


While categorical choices are handled equally by default, this option allows users to
specify prior knowledge on the structure of categorical parameters. When specified,
categorical choices closer to current best choices are more likely to be sampled.



Note


Added in v3.4.0 as an experimental feature. The interface may change in newer
versions without prior notice.
See [https://github.com/optuna/optuna/releases/tag/v3.4.0](https://github.com/optuna/optuna/releases/tag/v3.4.0).




Methods




[`after_trial`](#optuna.samplers.TPESampler.after_trial)(study, trial, state, values)


Trial post-processing.



[`before_trial`](#optuna.samplers.TPESampler.before_trial)(study, trial)


Trial pre-processing.



[`hyperopt_parameters`](#optuna.samplers.TPESampler.hyperopt_parameters)()


Return the the default parameters of hyperopt (v0.1.2).



[`infer_relative_search_space`](#optuna.samplers.TPESampler.infer_relative_search_space)(study, trial)


Infer the search space that will be used by relative sampling in the target trial.



[`reseed_rng`](#optuna.samplers.TPESampler.reseed_rng)()


Reseed sampler's random number generator.



[`sample_independent`](#optuna.samplers.TPESampler.sample_independent)(study, trial, param_name, ...)


Sample a parameter for a given distribution.



[`sample_relative`](#optuna.samplers.TPESampler.sample_relative)(study, trial, search_space)


Sample parameters in a given search space.







after_trial(*study*, *trial*, *state*, *values*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler.after_trial)[](#optuna.samplers.TPESampler.after_trial)
Trial post-processing.


This method is called after the objective function returns and right before the trial is
finished and its state is stored.



Note


Added in v2.4.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.4.0](https://github.com/optuna/optuna/releases/tag/v2.4.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)) – Resulting trial state.
- **values** (*Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Resulting trial values. Guaranteed to not be [`None`](https://docs.python.org/3/library/constants.html#None) if trial succeeded.



Return type:
None







before_trial(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler.before_trial)[](#optuna.samplers.TPESampler.before_trial)
Trial pre-processing.


This method is called before the objective function is called and right after the trial is
instantiated. More precisely, this method is called during trial initialization, just
before the [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space) call. In other
words, it is responsible for pre-processing that should be done before inferring the search
space.



Note


Added in v3.3.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.



Return type:
None







*static *hyperopt_parameters()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler.hyperopt_parameters)[](#optuna.samplers.TPESampler.hyperopt_parameters)
Return the the default parameters of hyperopt (v0.1.2).


[`TPESampler`](#optuna.samplers.TPESampler) can be instantiated with the parameters returned
by this method.


Example


Create a [`TPESampler`](#optuna.samplers.TPESampler) instance with the default
parameters of [hyperopt](https://github.com/hyperopt/hyperopt/tree/0.1.2).


```
import optuna
from optuna.samplers import TPESampler


def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    return x**2


sampler = TPESampler(**TPESampler.hyperopt_parameters())
study = optuna.create_study(sampler=sampler)
study.optimize(objective, n_trials=10)
```




Returns:
A dictionary containing the default parameters of hyperopt.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)]







infer_relative_search_space(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler.infer_relative_search_space)[](#optuna.samplers.TPESampler.infer_relative_search_space)
Infer the search space that will be used by relative sampling in the target trial.


This method is called right before [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative)
method, and the search space returned by this method is passed to it. The parameters not
contained in the search space will be sampled by using
[`sample_independent()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_independent) method.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.



Returns:
A dictionary containing the parameter names and parameter’s distributions.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), BaseDistribution]





See also


Please refer to [`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space) as an
implementation of [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).






reseed_rng()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler.reseed_rng)[](#optuna.samplers.TPESampler.reseed_rng)
Reseed sampler’s random number generator.


This method is called by the [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) instance if trials are executed
in parallel with the option `n_jobs>1`. In that case, the sampler instance will be
replicated including the state of the random number generator, and they may suggest the
same values. To prevent this issue, this method assigns a different seed to each random
number generator.



Return type:
None







sample_independent(*study*, *trial*, *param_name*, *param_distribution*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler.sample_independent)[](#optuna.samplers.TPESampler.sample_independent)
Sample a parameter for a given distribution.


This method is called only for the parameters not contained in the search space returned
by [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative) method. This method is suitable
for sampling algorithms that do not use relationship between parameters such as random
sampling and TPE.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **param_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the sampled parameter.
- **param_distribution** (*BaseDistribution*) – Distribution object that specifies a prior and/or scale of the sampling algorithm.



Returns:
A parameter value.



Return type:
Any







sample_relative(*study*, *trial*, *search_space*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_tpe/sampler.html#TPESampler.sample_relative)[](#optuna.samplers.TPESampler.sample_relative)
Sample parameters in a given search space.


This method is called once at the beginning of each trial, i.e., right before the
evaluation of the objective function. This method is suitable for sampling algorithms
that use relationship between parameters such as Gaussian Process and CMA-ES.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **search_space** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]*) – The search space returned by
[`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).



Returns:
A dictionary containing the parameter names and the values.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]

---

## optuna.samplers.CmaEsSampler — Optuna 4.6.0 documentation
<a id="optunasamplersCmaEsSampler-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html

# optuna.samplers.CmaEsSampler[](#optuna-samplers-cmaessampler)




*class *optuna.samplers.CmaEsSampler(*x0=None*, *sigma0=None*, *n_startup_trials=1*, *independent_sampler=None*, *warn_independent_sampling=True*, *seed=None*, ***, *consider_pruned_trials=False*, *restart_strategy=None*, *popsize=None*, *inc_popsize=-1*, *use_separable_cma=False*, *with_margin=False*, *lr_adapt=False*, *source_trials=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_cmaes.html#CmaEsSampler)[](#optuna.samplers.CmaEsSampler)
A sampler using [cmaes](https://github.com/CyberAgentAILab/cmaes) as the backend.


Example


Optimize a simple quadratic function by using [`CmaEsSampler`](#optuna.samplers.CmaEsSampler).


```
$ pip install cmaes
```



```
import optuna


def objective(trial):
    x = trial.suggest_float("x", -1, 1)
    y = trial.suggest_int("y", -1, 1)
    return x**2 + y


sampler = optuna.samplers.CmaEsSampler()
study = optuna.create_study(sampler=sampler)
study.optimize(objective, n_trials=20)
```



Please note that this sampler does not support CategoricalDistribution.
However, [`FloatDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.FloatDistribution.html#optuna.distributions.FloatDistribution) with `step`,
([`suggest_float()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.suggest_float)) and
[`IntDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntDistribution.html#optuna.distributions.IntDistribution) ([`suggest_int()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.suggest_int))
are supported.


If your search space contains categorical parameters, I recommend you
to use [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) instead.
Furthermore, there is room for performance improvements in parallel
optimization settings. This sampler cannot use some trials for updating
the parameters of multivariate normal distribution.


For further information about CMA-ES algorithm, please refer to the following papers:


- [N. Hansen, The CMA Evolution Strategy: A Tutorial. arXiv:1604.00772, 2016.](https://arxiv.org/abs/1604.00772)
- [A. Auger and N. Hansen. A restart CMA evolution strategy with increasing population
size. In Proceedings of the IEEE Congress on Evolutionary Computation (CEC 2005),
pages 1769–1776. IEEE Press, 2005.](https://doi.org/10.1109/CEC.2005.1554902)
- [N. Hansen. Benchmarking a BI-Population CMA-ES on the BBOB-2009 Function Testbed.
GECCO Workshop, 2009.](https://doi.org/10.1145/1570256.1570333)
- [Raymond Ros, Nikolaus Hansen. A Simple Modification in CMA-ES Achieving Linear Time and
Space Complexity. 10th International Conference on Parallel Problem Solving From Nature,
Sep 2008, Dortmund, Germany. inria-00287367.](https://doi.org/10.1007/978-3-540-87700-4_30)
- [Masahiro Nomura, Shuhei Watanabe, Youhei Akimoto, Yoshihiko Ozaki, Masaki Onishi.
Warm Starting CMA-ES for Hyperparameter Optimization, AAAI. 2021.](https://doi.org/10.1609/aaai.v35i10.17109)
- [R. Hamano, S. Saito, M. Nomura, S. Shirakawa. CMA-ES with Margin: Lower-Bounding Marginal
Probability for Mixed-Integer Black-Box Optimization, GECCO. 2022.](https://doi.org/10.1145/3512290.3528827)
- [M. Nomura, Y. Akimoto, I. Ono. CMA-ES with Learning Rate Adaptation: Can CMA-ES with
Default Population Size Solve Multimodal and Noisy Problems?, GECCO. 2023.](https://doi.org/10.1145/3583131.3590358)



See also


You can also use [optuna_integration.PyCmaSampler](https://optuna-integration.readthedocs.io/en/stable/reference/generated/optuna_integration.PyCmaSampler.html#optuna_integration.PyCmaSampler) which is a sampler using cma
library as the backend.




Parameters:
- **x0** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **Any**] **| **None*) – A dictionary of an initial parameter values for CMA-ES. By default, the mean of `low`
and `high` for each distribution is used. Note that `x0` is sampled uniformly
within the search space domain for each restart if you specify `restart_strategy`
argument.
- **sigma0** ([*float*](https://docs.python.org/3/library/functions.html#float)* | **None*) – Initial standard deviation of CMA-ES. By default, `sigma0` is set to
`min_range / 6`, where `min_range` denotes the minimum range of the distributions
in the search space.
- **seed** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) – A random seed for CMA-ES.
- **n_startup_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The independent sampling is used instead of the CMA-ES algorithm until the given number
of trials finish in the same study.
- **independent_sampler** ([*BaseSampler*](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler)* | **None*) –

A [`BaseSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler) instance that is used for independent
sampling. The parameters not contained in the relative search space are sampled
by this sampler.
The search space for [`CmaEsSampler`](#optuna.samplers.CmaEsSampler) is determined by
[`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space).


If [`None`](https://docs.python.org/3/library/constants.html#None) is specified, [`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler) is used
as the default.



See also


[`optuna.samplers`](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html#module-optuna.samplers) module provides built-in independent samplers
such as [`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler) and
[`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler).
- **warn_independent_sampling** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), a warning message is emitted when
the value of a parameter is sampled by using an independent sampler.


Note that the parameters of the first trial in a study are always sampled
via an independent sampler, so no warning messages are emitted in this case.
- **restart_strategy** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **None*) –

Strategy for restarting CMA-ES optimization when converges to a local minimum.
If [`None`](https://docs.python.org/3/library/constants.html#None) is given, CMA-ES will not restart (default).
If ‘ipop’ is given, CMA-ES will restart with increasing population size.
if ‘bipop’ is given, CMA-ES will restart with the population size
increased or decreased.
Please see also `inc_popsize` parameter.



Warning


Deprecated in v4.4.0. `restart_strategy` argument will be removed in the future.
The removal of this feature is currently scheduled for v6.0.0,
but this schedule is subject to change.
From v4.4.0 onward, `restart_strategy` automatically falls back to `None`, and
`restart_strategy` will be supported in OptunaHub.
See [https://github.com/optuna/optuna/releases/tag/v4.4.0](https://github.com/optuna/optuna/releases/tag/v4.4.0).
- **popsize** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) – A population size of CMA-ES.
- **inc_popsize** ([*int*](https://docs.python.org/3/library/functions.html#int)) –

Multiplier for increasing population size before each restart.
This argument will be used when `restart_strategy = 'ipop'`
or `restart_strategy = 'bipop'` is specified.



Warning


Deprecated in v4.4.0. `inc_popsize` argument will be removed in the future.
The removal of this feature is currently scheduled for v6.0.0,
but this schedule is subject to change.
From v4.4.0 onward, `inc_popsize` is no longer utilized within Optuna, and
`inc_popsize` will be supported in OptunaHub.
See [https://github.com/optuna/optuna/releases/tag/v4.4.0](https://github.com/optuna/optuna/releases/tag/v4.4.0).
- **consider_pruned_trials** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), the PRUNED trials are considered for sampling.



Note


Added in v2.0.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v2.0.0](https://github.com/optuna/optuna/releases/tag/v2.0.0).




Note


It is suggested to set this flag [`False`](https://docs.python.org/3/library/constants.html#False) when the
[`MedianPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html#optuna.pruners.MedianPruner) is used. On the other hand, it is suggested
to set this flag [`True`](https://docs.python.org/3/library/constants.html#True) when the [`HyperbandPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html#optuna.pruners.HyperbandPruner) is
used. Please see [the benchmark result](https://github.com/optuna/optuna/pull/1229) for the details.
- **use_separable_cma** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), the covariance matrix is constrained to be diagonal.
Due to reduce the model complexity, the learning rate for the covariance matrix
is increased. Consequently, this algorithm outperforms CMA-ES on separable functions.



Note


Added in v2.6.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v2.6.0](https://github.com/optuna/optuna/releases/tag/v2.6.0).
- **with_margin** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), CMA-ES with margin is used. This algorithm prevents samples in
each discrete distribution ([`FloatDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.FloatDistribution.html#optuna.distributions.FloatDistribution) with
`step` and [`IntDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntDistribution.html#optuna.distributions.IntDistribution)) from being fixed to a single
point.
Currently, this option cannot be used with `use_separable_cma=True`.



Note


Added in v3.1.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v3.1.0](https://github.com/optuna/optuna/releases/tag/v3.1.0).
- **lr_adapt** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), CMA-ES with learning rate adaptation is used.
This algorithm focuses on working well on multimodal and/or noisy problems
with default settings.
Currently, this option cannot be used with `use_separable_cma=True` or
`with_margin=True`.



Note


Added in v3.3.0 or later, as an experimental feature.
The interface may change in newer versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).
- **source_trials** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)*[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*] **| **None*) –

This option is for Warm Starting CMA-ES, a method to transfer prior knowledge on
similar HPO tasks through the initialization of CMA-ES. This method estimates a
promising distribution from `source_trials` and generates the parameter of
multivariate gaussian distribution. Please note that it is prohibited to use
`x0`, `sigma0`, or `use_separable_cma` argument together.



Note


Added in v2.6.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v2.6.0](https://github.com/optuna/optuna/releases/tag/v2.6.0).




Methods




[`after_trial`](#optuna.samplers.CmaEsSampler.after_trial)(study, trial, state, values)


Trial post-processing.



[`before_trial`](#optuna.samplers.CmaEsSampler.before_trial)(study, trial)


Trial pre-processing.



[`infer_relative_search_space`](#optuna.samplers.CmaEsSampler.infer_relative_search_space)(study, trial)


Infer the search space that will be used by relative sampling in the target trial.



[`reseed_rng`](#optuna.samplers.CmaEsSampler.reseed_rng)()


Reseed sampler's random number generator.



[`sample_independent`](#optuna.samplers.CmaEsSampler.sample_independent)(study, trial, param_name, ...)


Sample a parameter for a given distribution.



[`sample_relative`](#optuna.samplers.CmaEsSampler.sample_relative)(study, trial, search_space)


Sample parameters in a given search space.







after_trial(*study*, *trial*, *state*, *values*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_cmaes.html#CmaEsSampler.after_trial)[](#optuna.samplers.CmaEsSampler.after_trial)
Trial post-processing.


This method is called after the objective function returns and right before the trial is
finished and its state is stored.



Note


Added in v2.4.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.4.0](https://github.com/optuna/optuna/releases/tag/v2.4.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)) – Resulting trial state.
- **values** ([*Sequence*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence)*[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Resulting trial values. Guaranteed to not be [`None`](https://docs.python.org/3/library/constants.html#None) if trial succeeded.



Return type:
None







before_trial(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_cmaes.html#CmaEsSampler.before_trial)[](#optuna.samplers.CmaEsSampler.before_trial)
Trial pre-processing.


This method is called before the objective function is called and right after the trial is
instantiated. More precisely, this method is called during trial initialization, just
before the [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space) call. In other
words, it is responsible for pre-processing that should be done before inferring the search
space.



Note


Added in v3.3.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.



Return type:
None







infer_relative_search_space(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_cmaes.html#CmaEsSampler.infer_relative_search_space)[](#optuna.samplers.CmaEsSampler.infer_relative_search_space)
Infer the search space that will be used by relative sampling in the target trial.


This method is called right before [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative)
method, and the search space returned by this method is passed to it. The parameters not
contained in the search space will be sampled by using
[`sample_independent()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_independent) method.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.



Returns:
A dictionary containing the parameter names and parameter’s distributions.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), *BaseDistribution*]





See also


Please refer to [`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space) as an
implementation of [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).






reseed_rng()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_cmaes.html#CmaEsSampler.reseed_rng)[](#optuna.samplers.CmaEsSampler.reseed_rng)
Reseed sampler’s random number generator.


This method is called by the [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) instance if trials are executed
in parallel with the option `n_jobs>1`. In that case, the sampler instance will be
replicated including the state of the random number generator, and they may suggest the
same values. To prevent this issue, this method assigns a different seed to each random
number generator.



Return type:
None







sample_independent(*study*, *trial*, *param_name*, *param_distribution*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_cmaes.html#CmaEsSampler.sample_independent)[](#optuna.samplers.CmaEsSampler.sample_independent)
Sample a parameter for a given distribution.


This method is called only for the parameters not contained in the search space returned
by [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative) method. This method is suitable
for sampling algorithms that do not use relationship between parameters such as random
sampling and TPE.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **param_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the sampled parameter.
- **param_distribution** (*BaseDistribution*) – Distribution object that specifies a prior and/or scale of the sampling algorithm.



Returns:
A parameter value.



Return type:
[*Any*](https://docs.python.org/3/library/typing.html#typing.Any)







sample_relative(*study*, *trial*, *search_space*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_cmaes.html#CmaEsSampler.sample_relative)[](#optuna.samplers.CmaEsSampler.sample_relative)
Sample parameters in a given search space.


This method is called once at the beginning of each trial, i.e., right before the
evaluation of the objective function. This method is suitable for sampling algorithms
that use relationship between parameters such as Gaussian Process and CMA-ES.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **search_space** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]*) – The search space returned by
[`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).



Returns:
A dictionary containing the parameter names and the values.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)]

---

## optuna.samplers.QMCSampler — Optuna 4.6.0 documentation
<a id="optunasamplersQMCSampler-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.QMCSampler.html

# optuna.samplers.QMCSampler[](#optuna-samplers-qmcsampler)




*class *optuna.samplers.QMCSampler(***, *qmc_type='sobol'*, *scramble=False*, *seed=None*, *independent_sampler=None*, *warn_asynchronous_seeding=True*, *warn_independent_sampling=True*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_qmc.html#QMCSampler)[](#optuna.samplers.QMCSampler)
A Quasi Monte Carlo Sampler that generates low-discrepancy sequences.


Quasi Monte Carlo (QMC) sequences are designed to have lower discrepancies than
standard random sequences. They are known to perform better than the standard
random sequences in hyperparameter optimization.


For further information about the use of QMC sequences for hyperparameter optimization,
please refer to the following paper:


- [Bergstra, James, and Yoshua Bengio. Random search for hyper-parameter optimization.
Journal of machine learning research 13.2, 2012.](https://jmlr.org/papers/v13/bergstra12a.html)


We use the QMC implementations in Scipy. For the details of the QMC algorithm,
see the Scipy API references on [scipy.stats.qmc](https://scipy.github.io/devdocs/reference/stats.qmc.html).



Note


The search space of the sampler is determined by either previous trials in the study or
the first trial that this sampler samples.


If there are previous trials in the study, [`QMCSampler`](#optuna.samplers.QMCSampler) infers its
search space using the trial which was created first in the study.


Otherwise (if the study has no previous trials), [`QMCSampler`](#optuna.samplers.QMCSampler)
samples the first trial using its independent_sampler and then infers the search space
in the second trial.


As mentioned above, the search space of the [`QMCSampler`](#optuna.samplers.QMCSampler) is
determined by the first trial of the study. Once the search space is determined, it cannot
be changed afterwards.




Parameters:
- **qmc_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) –

The type of QMC sequence to be sampled. This must be one of
“halton” and “sobol”. Default is “sobol”.



Note


Sobol’ sequence is designed to have low-discrepancy property when the number of
samples is \(n=2^m\) for each positive integer \(m\). When it is possible
to pre-specify the number of trials suggested by QMCSampler, it is recommended
that the number of trials should be set as power of two.
- **scramble** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If this option is [`True`](https://docs.python.org/3/library/constants.html#True), scrambling (randomization) is applied to the QMC
sequences.
- **seed** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) –

A seed for `QMCSampler`. This argument is used only when `scramble` is [`True`](https://docs.python.org/3/library/constants.html#True).
If this is [`None`](https://docs.python.org/3/library/constants.html#None), the seed is initialized randomly. Default is [`None`](https://docs.python.org/3/library/constants.html#None).



Note


When using multiple [`QMCSampler`](#optuna.samplers.QMCSampler)’s in parallel and/or
distributed optimization, all the samplers must share the same seed when the
scrambling is enabled. Otherwise, the low-discrepancy property of the samples
will be degraded.
- **independent_sampler** ([*BaseSampler*](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler)* | **None*) –

A [`BaseSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler) instance that is used for independent
sampling. The first trial of the study and the parameters not contained in the
relative search space are sampled by this sampler.


If [`None`](https://docs.python.org/3/library/constants.html#None) is specified, [`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler) is used
as the default.



See also


[`samplers`](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html#module-optuna.samplers) module provides built-in independent samplers
such as [`RandomSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html#optuna.samplers.RandomSampler) and
[`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler).
- **warn_independent_sampling** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), a warning message is emitted when
the value of a parameter is sampled by using an independent sampler.


Note that the parameters of the first trial in a study are sampled via an
independent sampler in most cases, so no warning messages are emitted in such cases.
- **warn_asynchronous_seeding** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) –

If this is [`True`](https://docs.python.org/3/library/constants.html#True), a warning message is emitted when the scrambling
(randomization) is applied to the QMC sequence and the random seed of the sampler is
not set manually.



Note


When using parallel and/or distributed optimization without manually
setting the seed, the seed is set randomly for each instances of
[`QMCSampler`](#optuna.samplers.QMCSampler) for different workers, which ends up
asynchronous seeding for multiple samplers used in the optimization.




See also


See parameter `seed` in [`QMCSampler`](#optuna.samplers.QMCSampler).




Example


Optimize a simple quadratic function by using [`QMCSampler`](#optuna.samplers.QMCSampler).


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", -1, 1)
    y = trial.suggest_int("y", -1, 1)
    return x**2 + y


sampler = optuna.samplers.QMCSampler()
study = optuna.create_study(sampler=sampler)
study.optimize(objective, n_trials=8)
```




Note


Added in v3.0.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.0.0](https://github.com/optuna/optuna/releases/tag/v3.0.0).



Methods




[`after_trial`](#optuna.samplers.QMCSampler.after_trial)(study, trial, state, values)


Trial post-processing.



[`before_trial`](#optuna.samplers.QMCSampler.before_trial)(study, trial)


Trial pre-processing.



[`infer_relative_search_space`](#optuna.samplers.QMCSampler.infer_relative_search_space)(study, trial)


Infer the search space that will be used by relative sampling in the target trial.



[`reseed_rng`](#optuna.samplers.QMCSampler.reseed_rng)()


Reseed sampler's random number generator.



[`sample_independent`](#optuna.samplers.QMCSampler.sample_independent)(study, trial, param_name, ...)


Sample a parameter for a given distribution.



[`sample_relative`](#optuna.samplers.QMCSampler.sample_relative)(study, trial, search_space)


Sample parameters in a given search space.







after_trial(*study*, *trial*, *state*, *values*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_qmc.html#QMCSampler.after_trial)[](#optuna.samplers.QMCSampler.after_trial)
Trial post-processing.


This method is called after the objective function returns and right before the trial is
finished and its state is stored.



Note


Added in v2.4.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.4.0](https://github.com/optuna/optuna/releases/tag/v2.4.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*optuna.trial.FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)) – Resulting trial state.
- **values** (*Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Resulting trial values. Guaranteed to not be [`None`](https://docs.python.org/3/library/constants.html#None) if trial succeeded.



Return type:
None







before_trial(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_qmc.html#QMCSampler.before_trial)[](#optuna.samplers.QMCSampler.before_trial)
Trial pre-processing.


This method is called before the objective function is called and right after the trial is
instantiated. More precisely, this method is called during trial initialization, just
before the [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space) call. In other
words, it is responsible for pre-processing that should be done before inferring the search
space.



Note


Added in v3.3.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.



Return type:
None







infer_relative_search_space(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_qmc.html#QMCSampler.infer_relative_search_space)[](#optuna.samplers.QMCSampler.infer_relative_search_space)
Infer the search space that will be used by relative sampling in the target trial.


This method is called right before [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative)
method, and the search space returned by this method is passed to it. The parameters not
contained in the search space will be sampled by using
[`sample_independent()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_independent) method.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.



Returns:
A dictionary containing the parameter names and parameter’s distributions.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), BaseDistribution]





See also


Please refer to [`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space) as an
implementation of [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).






reseed_rng()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_qmc.html#QMCSampler.reseed_rng)[](#optuna.samplers.QMCSampler.reseed_rng)
Reseed sampler’s random number generator.


This method is called by the [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) instance if trials are executed
in parallel with the option `n_jobs>1`. In that case, the sampler instance will be
replicated including the state of the random number generator, and they may suggest the
same values. To prevent this issue, this method assigns a different seed to each random
number generator.



Return type:
None







sample_independent(*study*, *trial*, *param_name*, *param_distribution*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_qmc.html#QMCSampler.sample_independent)[](#optuna.samplers.QMCSampler.sample_independent)
Sample a parameter for a given distribution.


This method is called only for the parameters not contained in the search space returned
by [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative) method. This method is suitable
for sampling algorithms that do not use relationship between parameters such as random
sampling and TPE.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **param_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the sampled parameter.
- **param_distribution** (*BaseDistribution*) – Distribution object that specifies a prior and/or scale of the sampling algorithm.



Returns:
A parameter value.



Return type:
Any







sample_relative(*study*, *trial*, *search_space*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_qmc.html#QMCSampler.sample_relative)[](#optuna.samplers.QMCSampler.sample_relative)
Sample parameters in a given search space.


This method is called once at the beginning of each trial, i.e., right before the
evaluation of the objective function. This method is suitable for sampling algorithms
that use relationship between parameters such as Gaussian Process and CMA-ES.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **search_space** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]*) – The search space returned by
[`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).



Returns:
A dictionary containing the parameter names and the values.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]

---

## optuna.samplers.RandomSampler — Optuna 4.6.0 documentation
<a id="optunasamplersRandomSampler-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.RandomSampler.html

# optuna.samplers.RandomSampler[](#optuna-samplers-randomsampler)




*class *optuna.samplers.RandomSampler(*seed=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_random.html#RandomSampler)[](#optuna.samplers.RandomSampler)
Sampler using random sampling.


This sampler is based on *independent sampling*.
See also [`BaseSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler) for more details of ‘independent sampling’.


Example


```
import optuna
from optuna.samplers import RandomSampler


def objective(trial):
    x = trial.suggest_float("x", -5, 5)
    return x**2


study = optuna.create_study(sampler=RandomSampler())
study.optimize(objective, n_trials=10)
```




Parameters:
**seed** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) – Seed for random number generator.




Methods




[`after_trial`](#optuna.samplers.RandomSampler.after_trial)(study, trial, state, values)


Trial post-processing.



[`before_trial`](#optuna.samplers.RandomSampler.before_trial)(study, trial)


Trial pre-processing.



[`infer_relative_search_space`](#optuna.samplers.RandomSampler.infer_relative_search_space)(study, trial)


Infer the search space that will be used by relative sampling in the target trial.



[`reseed_rng`](#optuna.samplers.RandomSampler.reseed_rng)()


Reseed sampler's random number generator.



[`sample_independent`](#optuna.samplers.RandomSampler.sample_independent)(study, trial, param_name, ...)


Sample a parameter for a given distribution.



[`sample_relative`](#optuna.samplers.RandomSampler.sample_relative)(study, trial, search_space)


Sample parameters in a given search space.







after_trial(*study*, *trial*, *state*, *values*)[](#optuna.samplers.RandomSampler.after_trial)
Trial post-processing.


This method is called after the objective function returns and right before the trial is
finished and its state is stored.



Note


Added in v2.4.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.4.0](https://github.com/optuna/optuna/releases/tag/v2.4.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)) – Resulting trial state.
- **values** (*Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Resulting trial values. Guaranteed to not be [`None`](https://docs.python.org/3/library/constants.html#None) if trial succeeded.



Return type:
None







before_trial(*study*, *trial*)[](#optuna.samplers.RandomSampler.before_trial)
Trial pre-processing.


This method is called before the objective function is called and right after the trial is
instantiated. More precisely, this method is called during trial initialization, just
before the [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space) call. In other
words, it is responsible for pre-processing that should be done before inferring the search
space.



Note


Added in v3.3.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.



Return type:
None







infer_relative_search_space(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_random.html#RandomSampler.infer_relative_search_space)[](#optuna.samplers.RandomSampler.infer_relative_search_space)
Infer the search space that will be used by relative sampling in the target trial.


This method is called right before [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative)
method, and the search space returned by this method is passed to it. The parameters not
contained in the search space will be sampled by using
[`sample_independent()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_independent) method.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.



Returns:
A dictionary containing the parameter names and parameter’s distributions.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), BaseDistribution]





See also


Please refer to [`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space) as an
implementation of [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).






reseed_rng()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_random.html#RandomSampler.reseed_rng)[](#optuna.samplers.RandomSampler.reseed_rng)
Reseed sampler’s random number generator.


This method is called by the [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) instance if trials are executed
in parallel with the option `n_jobs>1`. In that case, the sampler instance will be
replicated including the state of the random number generator, and they may suggest the
same values. To prevent this issue, this method assigns a different seed to each random
number generator.



Return type:
None







sample_independent(*study*, *trial*, *param_name*, *param_distribution*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_random.html#RandomSampler.sample_independent)[](#optuna.samplers.RandomSampler.sample_independent)
Sample a parameter for a given distribution.


This method is called only for the parameters not contained in the search space returned
by [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative) method. This method is suitable
for sampling algorithms that do not use relationship between parameters such as random
sampling and TPE.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **param_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the sampled parameter.
- **param_distribution** (*distributions.BaseDistribution*) – Distribution object that specifies a prior and/or scale of the sampling algorithm.



Returns:
A parameter value.



Return type:
Any







sample_relative(*study*, *trial*, *search_space*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_random.html#RandomSampler.sample_relative)[](#optuna.samplers.RandomSampler.sample_relative)
Sample parameters in a given search space.


This method is called once at the beginning of each trial, i.e., right before the
evaluation of the objective function. This method is suitable for sampling algorithms
that use relationship between parameters such as Gaussian Process and CMA-ES.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **search_space** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]*) – The search space returned by
[`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).



Returns:
A dictionary containing the parameter names and the values.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]

---

## optuna.samplers.GPSampler — Optuna 4.6.0 documentation
<a id="optunasamplersGPSampler-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html

# optuna.samplers.GPSampler[](#optuna-samplers-gpsampler)




*class *optuna.samplers.GPSampler(***, *seed=None*, *independent_sampler=None*, *n_startup_trials=10*, *deterministic_objective=False*, *constraints_func=None*, *warn_independent_sampling=True*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_gp/sampler.html#GPSampler)[](#optuna.samplers.GPSampler)
Sampler using Gaussian process-based Bayesian optimization.


This sampler fits a Gaussian process (GP) to the objective function and optimizes
the acquisition function to suggest the next parameters.


The current implementation uses Matern kernel with nu=2.5 (twice differentiable) with automatic
relevance determination (ARD) for the length scale of each parameter.
The hyperparameters of the kernel are obtained by maximizing the marginal log-likelihood of the
hyperparameters given the past trials.
To prevent overfitting, Gamma prior is introduced for kernel scale and noise variance and
a hand-crafted prior is introduced for inverse squared lengthscales.


As an acquisition function, we use:


- log expected improvement (logEI) for single-objective optimization,
- log expected hypervolume improvement (logEHVI) for Multi-objective optimization, and
- the summation of logEI and the logarithm of the feasible probability with the independent
assumption of each constraint for (black-box inequality) constrained optimization.


For further information about these acquisition functions, please refer to the following
papers:


- [Unexpected Improvements to Expected Improvement for Bayesian Optimization](https://arxiv.org/abs/2310.20708)
- [Differentiable Expected Hypervolume Improvement for Parallel Multi-Objective Bayesian
Optimization](https://arxiv.org/abs/2006.05078)
- [Bayesian Optimization with Inequality Constraints](https://proceedings.mlr.press/v32/gardner14.pdf)


Please also check our articles:


- [[Optuna v4.5] Gaussian Process-Based Sampler (GPSampler) Can Now Perform Constrained
Multi-Objective Optimization](https://medium.com/optuna/optuna-v4-5-81e78d8e077a)
- [[Optuna v4.2] Gaussian Process-Based Sampler (GPSampler) Can Now Handle Inequality
Constraints](https://medium.com/optuna/optuna-v4-2-gaussian-process-based-sampler-can-now-handle-inequality-constraints-a4f68e8ee810)
- [Introducing Optuna’s Native GPSampler](https://medium.com/optuna/introducing-optunas-native-gpsampler-0aa9aa3b4840)


The optimization of the acquisition function is performed via:


1. Collect the best param from the past trials,
2. Collect `n_preliminary_samples` points using Quasi-Monte Carlo (QMC) sampling,
3. Choose the best point from the collected points,
4. Choose `n_local_search - 2` points from the collected points using the roulette
selection,
5. Perform a local search for each chosen point as an initial point, and
6. Return the point with the best acquisition function value as the next parameter.


Note that the procedures for non single-objective optimization setups are slightly different
from the single-objective version described above, but we omit the descriptions for the others
for brevity.


The local search iteratively optimizes the acquisition function by repeating:


1. Gradient ascent using l-BFGS-B for continuous parameters, and
2. Line search or exhaustive search for each discrete parameter independently.


The local search is terminated if the routine stops updating the best parameter set or the
maximum number of iterations is reached.


We use line search instead of rounding the results from the continuous optimization since EI
typically yields a high value between one grid and its adjacent grid.



Note


This sampler requires `scipy` and `torch`.
You can install these dependencies with `pip install scipy torch`.




Parameters:
- **seed** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) – Random seed to initialize internal random number generator.
Defaults to [`None`](https://docs.python.org/3/library/constants.html#None) (a seed is picked randomly).
- **independent_sampler** ([*BaseSampler*](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler)* | **None*) – Sampler used for initial sampling (for the first `n_startup_trials` trials)
and for conditional parameters. Defaults to [`None`](https://docs.python.org/3/library/constants.html#None)
(a random sampler with the same `seed` is used).
- **n_startup_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of initial trials. Defaults to 10.
- **deterministic_objective** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether the objective function is deterministic or not.
If [`True`](https://docs.python.org/3/library/constants.html#True), the sampler will fix the noise variance of the surrogate model to
the minimum value (slightly above 0 to ensure numerical stability).
Defaults to [`False`](https://docs.python.org/3/library/constants.html#False). Currently, all the objectives will be assume to be
deterministic if [`True`](https://docs.python.org/3/library/constants.html#True).
- **constraints_func** (*Callable**[**[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]**, **Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*]**] **| **None*) –

An optional function that computes the objective constraints. It must take a
[`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) and return the constraints. The return value must
be a sequence of [`float`](https://docs.python.org/3/library/functions.html#float) s. A value strictly larger than 0 means that a
constraints is violated. A value equal to or smaller than 0 is considered feasible.
If `constraints_func` returns more than one value for a trial, that trial is
considered feasible if and only if all values are equal to 0 or smaller.


The `constraints_func` will be evaluated after each successful trial.
The function won’t be called when trials fail or are pruned, but this behavior is
subject to change in future releases.
- **warn_independent_sampling** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If this is [`True`](https://docs.python.org/3/library/constants.html#True), a warning message is emitted when
the value of a parameter is sampled by using an independent sampler,
meaning that no GP model is used in the sampling.
Note that the parameters of the first trial in a study are always sampled
via an independent sampler, so no warning messages are emitted in this case.





Note


Added in v3.6.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.6.0](https://github.com/optuna/optuna/releases/tag/v3.6.0).



Methods




[`after_trial`](#optuna.samplers.GPSampler.after_trial)(study, trial, state, values)


Trial post-processing.



[`before_trial`](#optuna.samplers.GPSampler.before_trial)(study, trial)


Trial pre-processing.



[`infer_relative_search_space`](#optuna.samplers.GPSampler.infer_relative_search_space)(study, trial)


Infer the search space that will be used by relative sampling in the target trial.



[`reseed_rng`](#optuna.samplers.GPSampler.reseed_rng)()


Reseed sampler's random number generator.



[`sample_independent`](#optuna.samplers.GPSampler.sample_independent)(study, trial, param_name, ...)


Sample a parameter for a given distribution.



[`sample_relative`](#optuna.samplers.GPSampler.sample_relative)(study, trial, search_space)


Sample parameters in a given search space.







after_trial(*study*, *trial*, *state*, *values*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_gp/sampler.html#GPSampler.after_trial)[](#optuna.samplers.GPSampler.after_trial)
Trial post-processing.


This method is called after the objective function returns and right before the trial is
finished and its state is stored.



Note


Added in v2.4.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.4.0](https://github.com/optuna/optuna/releases/tag/v2.4.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)) – Resulting trial state.
- **values** (*Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Resulting trial values. Guaranteed to not be [`None`](https://docs.python.org/3/library/constants.html#None) if trial succeeded.



Return type:
None







before_trial(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_gp/sampler.html#GPSampler.before_trial)[](#optuna.samplers.GPSampler.before_trial)
Trial pre-processing.


This method is called before the objective function is called and right after the trial is
instantiated. More precisely, this method is called during trial initialization, just
before the [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space) call. In other
words, it is responsible for pre-processing that should be done before inferring the search
space.



Note


Added in v3.3.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.



Return type:
None







infer_relative_search_space(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_gp/sampler.html#GPSampler.infer_relative_search_space)[](#optuna.samplers.GPSampler.infer_relative_search_space)
Infer the search space that will be used by relative sampling in the target trial.


This method is called right before [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative)
method, and the search space returned by this method is passed to it. The parameters not
contained in the search space will be sampled by using
[`sample_independent()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_independent) method.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.



Returns:
A dictionary containing the parameter names and parameter’s distributions.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), BaseDistribution]





See also


Please refer to [`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space) as an
implementation of [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).






reseed_rng()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_gp/sampler.html#GPSampler.reseed_rng)[](#optuna.samplers.GPSampler.reseed_rng)
Reseed sampler’s random number generator.


This method is called by the [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) instance if trials are executed
in parallel with the option `n_jobs>1`. In that case, the sampler instance will be
replicated including the state of the random number generator, and they may suggest the
same values. To prevent this issue, this method assigns a different seed to each random
number generator.



Return type:
None







sample_independent(*study*, *trial*, *param_name*, *param_distribution*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_gp/sampler.html#GPSampler.sample_independent)[](#optuna.samplers.GPSampler.sample_independent)
Sample a parameter for a given distribution.


This method is called only for the parameters not contained in the search space returned
by [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative) method. This method is suitable
for sampling algorithms that do not use relationship between parameters such as random
sampling and TPE.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **param_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the sampled parameter.
- **param_distribution** (*BaseDistribution*) – Distribution object that specifies a prior and/or scale of the sampling algorithm.



Returns:
A parameter value.



Return type:
Any







sample_relative(*study*, *trial*, *search_space*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/_gp/sampler.html#GPSampler.sample_relative)[](#optuna.samplers.GPSampler.sample_relative)
Sample parameters in a given search space.


This method is called once at the beginning of each trial, i.e., right before the
evaluation of the objective function. This method is suitable for sampling algorithms
that use relationship between parameters such as Gaussian Process and CMA-ES.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **search_space** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]*) – The search space returned by
[`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).



Returns:
A dictionary containing the parameter names and the values.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]

---

## optuna.samplers.NSGAIISampler — Optuna 4.6.0 documentation
<a id="optunasamplersNSGAIISampler-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.NSGAIISampler.html

# optuna.samplers.NSGAIISampler[](#optuna-samplers-nsgaiisampler)




*class *optuna.samplers.NSGAIISampler(***, *population_size=50*, *mutation_prob=None*, *crossover=None*, *crossover_prob=0.9*, *swapping_prob=0.5*, *seed=None*, *constraints_func=None*, *elite_population_selection_strategy=None*, *child_generation_strategy=None*, *after_trial_strategy=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler)[](#optuna.samplers.NSGAIISampler)
Multi-objective sampler using the NSGA-II algorithm.


NSGA-II stands for “Nondominated Sorting Genetic Algorithm II”,
which is a well known, fast and elitist multi-objective genetic algorithm.


For further information about NSGA-II, please refer to the following paper:


- [A fast and elitist multiobjective genetic algorithm: NSGA-II](https://doi.org/10.1109/4235.996017)



Note


[`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) became much faster in v4.0.0 and supports several
features not supported by `NSGAIISampler` such as handling of dynamic search
space and categorical distance. To use [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler), you need to
explicitly specify the sampler as follows:


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", -100, 100)
    y = trial.suggest_categorical("y", [-1, 0, 1])
    f1 = x**2 + y
    f2 = -((x - 2) ** 2 + y)
    return f1, f2


# We minimize the first objective and maximize the second objective.
sampler = optuna.samplers.TPESampler()
study = optuna.create_study(directions=["minimize", "maximize"], sampler=sampler)
study.optimize(objective, n_trials=100)
```



Please also check [our article](https://medium.com/optuna/significant-speed-up-of-multi-objective-tpesampler-in-optuna-v4-0-0-2bacdcd1d99b)
for more details of the speedup in v4.0.0.




Parameters:
- **population_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of individuals (trials) in a generation.
`population_size` must be greater than or equal to `crossover.n_parents`.
For [`UNDXCrossover`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.nsgaii.UNDXCrossover.html#optuna.samplers.nsgaii.UNDXCrossover) and
[`SPXCrossover`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.nsgaii.SPXCrossover.html#optuna.samplers.nsgaii.SPXCrossover), `n_parents=3`, and for the other
algorithms, `n_parents=2`.
- **mutation_prob** ([*float*](https://docs.python.org/3/library/functions.html#float)* | **None*) – Probability of mutating each parameter when creating a new individual.
If [`None`](https://docs.python.org/3/library/constants.html#None) is specified, the value `1.0 / len(parent_trial.params)` is used
where `parent_trial` is the parent trial of the target individual.
- **crossover** ([*BaseCrossover*](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.nsgaii.BaseCrossover.html#optuna.samplers.nsgaii.BaseCrossover)* | **None*) –

Crossover to be applied when creating child individuals.
The available crossovers are listed here:
[https://optuna.readthedocs.io/en/stable/reference/samplers/nsgaii.html](https://optuna.readthedocs.io/en/stable/reference/samplers/nsgaii.html).


[`UniformCrossover`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.nsgaii.UniformCrossover.html#optuna.samplers.nsgaii.UniformCrossover) is always applied to parameters
sampled from [`CategoricalDistribution`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html#optuna.distributions.CategoricalDistribution), and by
default for parameters sampled from other distributions unless this argument
is specified.


For more information on each of the crossover method, please refer to
specific crossover documentation.
- **crossover_prob** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Probability that a crossover (parameters swapping between parents) will occur
when creating a new individual.
- **swapping_prob** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Probability of swapping each parameter of the parents during crossover.
- **seed** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) – Seed for random number generator.
- **constraints_func** (*Callable**[**[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]**, **Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*]**] **| **None*) –

An optional function that computes the objective constraints. It must take a
[`FrozenTrial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial) and return the constraints. The return value must
be a sequence of [`float`](https://docs.python.org/3/library/functions.html#float) s. A value strictly larger than 0 means that a
constraints is violated. A value equal to or smaller than 0 is considered feasible.
If `constraints_func` returns more than one value for a trial, that trial is
considered feasible if and only if all values are equal to 0 or smaller.


The `constraints_func` will be evaluated after each successful trial.
The function won’t be called when trials fail or they are pruned, but this behavior is
subject to change in the future releases.


The constraints are handled by the constrained domination. A trial x is said to
constrained-dominate a trial y, if any of the following conditions is true:


1. Trial x is feasible and trial y is not.
2. Trial x and y are both infeasible, but trial x has a smaller overall violation.
3. Trial x and y are feasible and trial x dominates trial y.



Note


Added in v2.5.0 as an experimental feature. The interface may change in newer
versions without prior notice. See
[https://github.com/optuna/optuna/releases/tag/v2.5.0](https://github.com/optuna/optuna/releases/tag/v2.5.0).
- **elite_population_selection_strategy** (*Callable**[**[*[*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)*, *[*list*](https://docs.python.org/3/library/stdtypes.html#list)*[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]**]**, *[*list*](https://docs.python.org/3/library/stdtypes.html#list)*[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]**] **| **None*) –

The selection strategy for determining the individuals to survive from the current
population pool. Default to [`None`](https://docs.python.org/3/library/constants.html#None).



Note


The arguments `elite_population_selection_strategy` was added in v3.3.0 as an
experimental feature. The interface may change in newer versions without prior
notice.
See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).
- **child_generation_strategy** (*Callable**[**[*[*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)*, *[*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]**, *[*list*](https://docs.python.org/3/library/stdtypes.html#list)*[*[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*]**]**, *[*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **Any**]**] **| **None*) –

The strategy for generating child parameters from parent trials. Defaults to
[`None`](https://docs.python.org/3/library/constants.html#None).



Note


The arguments `child_generation_strategy` was added in v3.3.0 as an experimental
feature. The interface may change in newer versions without prior notice.
See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).
- **after_trial_strategy** (*Callable**[**[*[*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)*, *[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)*, *[*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)*, **Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None**]**, **None**] **| **None*) –

A set of procedure to be conducted after each trial. Defaults to [`None`](https://docs.python.org/3/library/constants.html#None).



Note


The arguments `after_trial_strategy` was added in v3.3.0 as an experimental
feature. The interface may change in newer versions without prior notice.
See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Methods




[`after_trial`](#optuna.samplers.NSGAIISampler.after_trial)(study, trial, state, values)


Trial post-processing.



[`before_trial`](#optuna.samplers.NSGAIISampler.before_trial)(study, trial)


Trial pre-processing.



[`get_parent_population`](#optuna.samplers.NSGAIISampler.get_parent_population)(study, generation)


Get the parent population of the given generation.



[`get_population`](#optuna.samplers.NSGAIISampler.get_population)(study, generation)


Get the population of the given generation.



[`get_trial_generation`](#optuna.samplers.NSGAIISampler.get_trial_generation)(study, trial)


Get the generation number of the given trial.



[`infer_relative_search_space`](#optuna.samplers.NSGAIISampler.infer_relative_search_space)(study, trial)


Infer the search space that will be used by relative sampling in the target trial.



[`reseed_rng`](#optuna.samplers.NSGAIISampler.reseed_rng)()


Reseed sampler's random number generator.



[`sample_independent`](#optuna.samplers.NSGAIISampler.sample_independent)(study, trial, param_name, ...)


Sample a parameter for a given distribution.



[`sample_relative`](#optuna.samplers.NSGAIISampler.sample_relative)(study, trial, search_space)


Sample parameters in a given search space.



[`select_parent`](#optuna.samplers.NSGAIISampler.select_parent)(study, generation)


Select parent trials from the population for the given generation.





Attributes




`population_size`








after_trial(*study*, *trial*, *state*, *values*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler.after_trial)[](#optuna.samplers.NSGAIISampler.after_trial)
Trial post-processing.


This method is called after the objective function returns and right before the trial is
finished and its state is stored.



Note


Added in v2.4.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.4.0](https://github.com/optuna/optuna/releases/tag/v2.4.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **state** ([*TrialState*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.TrialState.html#optuna.trial.TrialState)) – Resulting trial state.
- **values** (*Sequence**[*[*float*](https://docs.python.org/3/library/functions.html#float)*] **| **None*) – Resulting trial values. Guaranteed to not be [`None`](https://docs.python.org/3/library/constants.html#None) if trial succeeded.



Return type:
None







before_trial(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler.before_trial)[](#optuna.samplers.NSGAIISampler.before_trial)
Trial pre-processing.


This method is called before the objective function is called and right after the trial is
instantiated. More precisely, this method is called during trial initialization, just
before the [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space) call. In other
words, it is responsible for pre-processing that should be done before inferring the search
space.



Note


Added in v3.3.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.3.0](https://github.com/optuna/optuna/releases/tag/v3.3.0).




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.



Return type:
None







get_parent_population(*study*, *generation*)[](#optuna.samplers.NSGAIISampler.get_parent_population)
Get the parent population of the given generation.


This method caches the parent population in the study’s system attributes.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **generation** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Target generation number.



Returns:
List of parent frozen trials. If generation == 0, returns an empty list.



Return type:
[list](https://docs.python.org/3/library/stdtypes.html#list)[[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)]







get_population(*study*, *generation*)[](#optuna.samplers.NSGAIISampler.get_population)
Get the population of the given generation.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **generation** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Target generation number.



Returns:
List of frozen trials in the given generation.



Return type:
[list](https://docs.python.org/3/library/stdtypes.html#list)[[*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)]







get_trial_generation(*study*, *trial*)[](#optuna.samplers.NSGAIISampler.get_trial_generation)
Get the generation number of the given trial.


This method returns the generation number of the specified trial. If the generation number
is not set in the trial’s system attributes, it will calculate and set the generation
number.


The current generation number depends on the maximum generation number of all completed
trials.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Study object which trial belongs to.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Trial object to get the generation number.



Returns:
Generation number of the given trial.



Return type:
[int](https://docs.python.org/3/library/functions.html#int)







infer_relative_search_space(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler.infer_relative_search_space)[](#optuna.samplers.NSGAIISampler.infer_relative_search_space)
Infer the search space that will be used by relative sampling in the target trial.


This method is called right before [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative)
method, and the search space returned by this method is passed to it. The parameters not
contained in the search space will be sampled by using
[`sample_independent()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_independent) method.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.



Returns:
A dictionary containing the parameter names and parameter’s distributions.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), BaseDistribution]





See also


Please refer to [`intersection_search_space()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.search_space.intersection_search_space.html#optuna.search_space.intersection_search_space) as an
implementation of [`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).






reseed_rng()[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler.reseed_rng)[](#optuna.samplers.NSGAIISampler.reseed_rng)
Reseed sampler’s random number generator.


This method is called by the [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) instance if trials are executed
in parallel with the option `n_jobs>1`. In that case, the sampler instance will be
replicated including the state of the random number generator, and they may suggest the
same values. To prevent this issue, this method assigns a different seed to each random
number generator.



Return type:
None







sample_independent(*study*, *trial*, *param_name*, *param_distribution*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler.sample_independent)[](#optuna.samplers.NSGAIISampler.sample_independent)
Sample a parameter for a given distribution.


This method is called only for the parameters not contained in the search space returned
by [`sample_relative()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.sample_relative) method. This method is suitable
for sampling algorithms that do not use relationship between parameters such as random
sampling and TPE.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **param_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the sampled parameter.
- **param_distribution** (*BaseDistribution*) – Distribution object that specifies a prior and/or scale of the sampling algorithm.



Returns:
A parameter value.



Return type:
Any







sample_relative(*study*, *trial*, *search_space*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler.sample_relative)[](#optuna.samplers.NSGAIISampler.sample_relative)
Sample parameters in a given search space.


This method is called once at the beginning of each trial, i.e., right before the
evaluation of the objective function. This method is suitable for sampling algorithms
that use relationship between parameters such as Gaussian Process and CMA-ES.



Note


The failed trials are ignored by any build-in samplers when they sample new
parameters. Thus, failed trials are regarded as deleted in the samplers’
perspective.




Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – Target trial object.
Take a copy before modifying this object.
- **search_space** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str)*, **BaseDistribution**]*) – The search space returned by
[`infer_relative_search_space()`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler.infer_relative_search_space).



Returns:
A dictionary containing the parameter names and the values.



Return type:
[dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]







select_parent(*study*, *generation*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/samplers/nsgaii/_sampler.html#NSGAIISampler.select_parent)[](#optuna.samplers.NSGAIISampler.select_parent)
Select parent trials from the population for the given generation.


This method is called once per generation to select parents from
the population of the current generation.


Output of this function is cached in the study system attributes.


This method must be implemented in a subclass to define the specific selection strategy.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Target study object.
- **generation** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Target generation number.



Returns:
List of parent frozen trials.



Return type:
[list](https://docs.python.org/3/library/stdtypes.html#list)[[FrozenTrial](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)]

---

## optuna.pruners — Optuna 4.6.0 documentation
<a id="optunapruners-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/pruners.html

# optuna.pruners[](#optuna-pruners)


The [`pruners`](#module-optuna.pruners) module defines a [`BasePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner) class characterized by an abstract [`prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner.prune) method, which, for a given trial and its associated study, returns a boolean value representing whether the trial should be pruned. This determination is made based on stored intermediate values of the objective function, as previously reported for the trial using [`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report). The remaining classes in this module represent child classes, inheriting from [`BasePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner), which implement different pruning strategies.



Warning


Currently [`pruners`](#module-optuna.pruners) module is expected to be used only for single-objective optimization.




See also


[Efficient Optimization Algorithms](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/003_efficient_optimization_algorithms.html#pruning) tutorial explains the concept of the pruner classes and a minimal example.




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

## optuna.pruners.MedianPruner — Optuna 4.6.0 documentation
<a id="optunaprunersMedianPruner-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.MedianPruner.html

# optuna.pruners.MedianPruner[](#optuna-pruners-medianpruner)




*class *optuna.pruners.MedianPruner(*n_startup_trials=5*, *n_warmup_steps=0*, *interval_steps=1*, ***, *n_min_trials=1*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_median.html#MedianPruner)[](#optuna.pruners.MedianPruner)
Pruner using the median stopping rule.


Prune if the trial’s best intermediate result is worse than median of intermediate results of
previous trials at the same step. It stops unpromising trials early based on the
intermediate results compared against the median of previous completed trials.



The pruner handles NaN values in the following manner:1. If all intermediate values of the current trial are NaN, the trial will be pruned.
2. During the median calculation across completed trials, NaN values are ignored.
Only valid numeric values are considered.




Example


We minimize an objective function with the median stopping rule.


```
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
```




Parameters:
- **n_startup_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Pruning is disabled until the given number of trials finish in the same study.
- **n_warmup_steps** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Pruning is disabled until the trial exceeds the given number of step. Note that
this feature assumes that `step` starts at zero.
- **interval_steps** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Interval in number of steps between the pruning checks, offset by the warmup steps.
If no value has been reported at the time of a pruning check, that particular check
will be postponed until a value is reported.
- **n_min_trials** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Minimum number of reported trial results at a step to judge whether to prune.
If the number of reported intermediate values from all trials at the current step
is less than `n_min_trials`, the trial will not be pruned. This can be used to ensure
that a minimum number of trials are run to completion without being pruned.




Methods




[`prune`](#optuna.pruners.MedianPruner.prune)(study, trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[](#optuna.pruners.MedianPruner.prune)
Judge whether the trial should be pruned based on the reported values.


Note that this method is not supposed to be called by library users. Instead,
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) and [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) provide
user interfaces to implement pruning mechanism in an objective function.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Study object of the target study.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – FrozenTrial object of the target trial.
Take a copy before modifying this object.



Returns:
A boolean value representing whether the trial should be pruned.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)

---

## optuna.pruners.SuccessiveHalvingPruner — Optuna 4.6.0 documentation
<a id="optunaprunersSuccessiveHalvingPruner-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html

# optuna.pruners.SuccessiveHalvingPruner[](#optuna-pruners-successivehalvingpruner)




*class *optuna.pruners.SuccessiveHalvingPruner(*min_resource='auto'*, *reduction_factor=4*, *min_early_stopping_rate=0*, *bootstrap_count=0*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_successive_halving.html#SuccessiveHalvingPruner)[](#optuna.pruners.SuccessiveHalvingPruner)
Pruner using Asynchronous Successive Halving Algorithm.


[Successive Halving](https://proceedings.mlr.press/v51/jamieson16.html) is a bandit-based
algorithm to identify the best one among multiple configurations. This class implements an
asynchronous version of Successive Halving. Please refer to the paper of
[Asynchronous Successive Halving](https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf) for detailed descriptions.


Note that, this class does not take care of the parameter for the maximum
resource, referred to as \(R\) in the paper. The maximum resource allocated to a trial is
typically limited inside the objective function (e.g., `step` number in [simple_pruning.py](https://github.com/optuna/optuna-examples/blob/main/basic/pruning.py),
`EPOCH` number in [chainer_integration.py](https://github.com/optuna/optuna-examples/tree/main/chainer/chainer_integration.py#L73)).



See also


Please refer to [`report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report).



Example


We minimize an objective function with `SuccessiveHalvingPruner`.


```
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
    direction="maximize", pruner=optuna.pruners.SuccessiveHalvingPruner()
)
study.optimize(objective, n_trials=20)
```




Parameters:
- **min_resource** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | *[*int*](https://docs.python.org/3/library/functions.html#int)) –

A parameter for specifying the minimum resource allocated to a trial
(in the [paper](https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf) this parameter is referred to as
\(r\)).
This parameter defaults to ‘auto’ where the value is determined based on a heuristic
that looks at the number of required steps for the first trial to complete.


A trial is never pruned until it executes
\(\mathsf{min}\_\mathsf{resource} \times
\mathsf{reduction}\_\mathsf{factor}^{
\mathsf{min}\_\mathsf{early}\_\mathsf{stopping}\_\mathsf{rate}}\)
steps (i.e., the completion point of the first rung). When the trial completes
the first rung, it will be promoted to the next rung only
if the value of the trial is placed in the top
\({1 \over \mathsf{reduction}\_\mathsf{factor}}\) fraction of
the all trials that already have reached the point (otherwise it will be pruned there).
If the trial won the competition, it runs until the next completion point (i.e.,
\(\mathsf{min}\_\mathsf{resource} \times
\mathsf{reduction}\_\mathsf{factor}^{
(\mathsf{min}\_\mathsf{early}\_\mathsf{stopping}\_\mathsf{rate}
+ \mathsf{rung})}\) steps)
and repeats the same procedure.



Note


If the step of the last intermediate value may change with each trial, please
manually specify the minimum possible step to `min_resource`.
- **reduction_factor** ([*int*](https://docs.python.org/3/library/functions.html#int)) – A parameter for specifying reduction factor of promotable trials
(in the [paper](https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf) this parameter is
referred to as \(\eta\)).  At the completion point of each rung,
about \({1 \over \mathsf{reduction}\_\mathsf{factor}}\)
trials will be promoted.
- **min_early_stopping_rate** ([*int*](https://docs.python.org/3/library/functions.html#int)) – A parameter for specifying the minimum early-stopping rate
(in the [paper](https://proceedings.mlsys.org/paper_files/paper/2020/file/a06f20b349c6cf09a6b171c71b88bbfc-Paper.pdf) this parameter is
referred to as \(s\)).
- **bootstrap_count** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Minimum number of trials that need to complete a rung before any trial
is considered for promotion into the next rung.




Methods




[`prune`](#optuna.pruners.SuccessiveHalvingPruner.prune)(study, trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_successive_halving.html#SuccessiveHalvingPruner.prune)[](#optuna.pruners.SuccessiveHalvingPruner.prune)
Judge whether the trial should be pruned based on the reported values.


Note that this method is not supposed to be called by library users. Instead,
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) and [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) provide
user interfaces to implement pruning mechanism in an objective function.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Study object of the target study.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – FrozenTrial object of the target trial.
Take a copy before modifying this object.



Returns:
A boolean value representing whether the trial should be pruned.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)

---

## optuna.pruners.HyperbandPruner — Optuna 4.6.0 documentation
<a id="optunaprunersHyperbandPruner-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.HyperbandPruner.html

# optuna.pruners.HyperbandPruner[](#optuna-pruners-hyperbandpruner)




*class *optuna.pruners.HyperbandPruner(*min_resource=1*, *max_resource='auto'*, *reduction_factor=3*, *bootstrap_count=0*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_hyperband.html#HyperbandPruner)[](#optuna.pruners.HyperbandPruner)
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




Note


If you use `HyperbandPruner` with [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler),
it’s recommended to consider setting larger `n_trials` or `timeout` to make full use of
the characteristics of [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler)
because [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) uses some (by default, \(10\))
[`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)s for its startup.


As Hyperband runs multiple [`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner) and collects
trials based on the current [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)‘s bracket ID, each bracket
needs to observe more than \(10\) [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial)s
for [`TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) to adapt its search space.


Thus, for example, if `HyperbandPruner` has \(4\) pruners in it,
at least \(4 \times 10\) trials are consumed for startup.




Note


Hyperband has several [`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner)s. Each
[`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner) is referred to as “bracket” in the
original paper. The number of brackets is an important factor to control the early
stopping behavior of Hyperband and is automatically determined by `min_resource`,
`max_resource` and `reduction_factor` as
\(\mathrm{The\ number\ of\ brackets} =
\mathrm{floor}(\log_{\texttt{reduction}\_\texttt{factor}}
(\frac{\texttt{max}\_\texttt{resource}}{\texttt{min}\_\texttt{resource}})) + 1\).
Please set `reduction_factor` so that the number of brackets is not too large (about 4 –
6 in most use cases). Please see Section 3.6 of the [original paper](http://www.jmlr.org/papers/volume18/16-558/16-558.pdf) for the detail.




Note


`HyperbandPruner` computes bracket ID for each trial with a
function taking `study_name` of [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) and
[`number`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.number). Please specify `study_name`
to make the pruning algorithm reproducible.



Example


We minimize an objective function with Hyperband pruning algorithm.


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

import optuna

X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)
classes = np.unique(y)
n_train_iter = 100


def objective(trial):
    alpha = trial.suggest_float("alpha", 0.0, 1.0)
    clf = SGDClassifier(alpha=alpha)

    for step in range(n_train_iter):
        clf.partial_fit(X_train, y_train, classes=classes)

        intermediate_value = clf.score(X_valid, y_valid)
        trial.report(intermediate_value, step)

        if trial.should_prune():
            raise optuna.TrialPruned()

    return clf.score(X_valid, y_valid)


study = optuna.create_study(
    direction="maximize",
    pruner=optuna.pruners.HyperbandPruner(
        min_resource=1, max_resource=n_train_iter, reduction_factor=3
    ),
)
study.optimize(objective, n_trials=20)
```




Parameters:
- **min_resource** ([*int*](https://docs.python.org/3/library/functions.html#int)) – A parameter for specifying the minimum resource allocated to a trial noted as \(r\)
in the paper. A smaller \(r\) will give a result faster, but a larger
\(r\) will give a better guarantee of successful judging between configurations.
See the details for [`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner).
- **max_resource** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | *[*int*](https://docs.python.org/3/library/functions.html#int)) –

A parameter for specifying the maximum resource allocated to a trial. \(R\) in the
paper corresponds to `max_resource / min_resource`. This value represents and should
match the maximum iteration steps (e.g., the number of epochs for neural networks).
When this argument is “auto”, the maximum resource is estimated according to the
completed trials. The default value of this argument is “auto”.



Note


With “auto”, the maximum resource will be the largest step reported by
[`report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) in the first, or one of the first if trained in
parallel, completed trial. No trials will be pruned until the maximum resource is
determined.




Note


If the step of the last intermediate value may change with each trial, please
manually specify the maximum possible step to `max_resource`.
- **reduction_factor** ([*int*](https://docs.python.org/3/library/functions.html#int)) – A parameter for specifying reduction factor of promotable trials noted as
\(\eta\) in the paper.
See the details for [`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner).
- **bootstrap_count** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Parameter specifying the number of trials required in a rung before any trial can be
promoted. Incompatible with `max_resource` is `"auto"`.
See the details for [`SuccessiveHalvingPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.SuccessiveHalvingPruner.html#optuna.pruners.SuccessiveHalvingPruner).




Methods




[`prune`](#optuna.pruners.HyperbandPruner.prune)(study, trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_hyperband.html#HyperbandPruner.prune)[](#optuna.pruners.HyperbandPruner.prune)
Judge whether the trial should be pruned based on the reported values.


Note that this method is not supposed to be called by library users. Instead,
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) and [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) provide
user interfaces to implement pruning mechanism in an objective function.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Study object of the target study.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – FrozenTrial object of the target trial.
Take a copy before modifying this object.



Returns:
A boolean value representing whether the trial should be pruned.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)

---

## optuna.pruners.ThresholdPruner — Optuna 4.6.0 documentation
<a id="optunaprunersThresholdPruner-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.ThresholdPruner.html

# optuna.pruners.ThresholdPruner[](#optuna-pruners-thresholdpruner)




*class *optuna.pruners.ThresholdPruner(*lower=None*, *upper=None*, *n_warmup_steps=0*, *interval_steps=1*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_threshold.html#ThresholdPruner)[](#optuna.pruners.ThresholdPruner)
Pruner to detect outlying metrics of the trials.


Prune if a metric exceeds upper threshold,
falls behind lower threshold or reaches `nan`.


Example


```
from optuna import create_study
from optuna.pruners import ThresholdPruner
from optuna import TrialPruned


def objective_for_upper(trial):
    for step, y in enumerate(ys_for_upper):
        trial.report(y, step)

        if trial.should_prune():
            raise TrialPruned()
    return ys_for_upper[-1]


def objective_for_lower(trial):
    for step, y in enumerate(ys_for_lower):
        trial.report(y, step)

        if trial.should_prune():
            raise TrialPruned()
    return ys_for_lower[-1]


ys_for_upper = [0.0, 0.1, 0.2, 0.5, 1.2]
ys_for_lower = [100.0, 90.0, 0.1, 0.0, -1]

study = create_study(pruner=ThresholdPruner(upper=1.0))
study.optimize(objective_for_upper, n_trials=10)

study = create_study(pruner=ThresholdPruner(lower=0.0))
study.optimize(objective_for_lower, n_trials=10)
```




Parameters:
- **lower** ([*float*](https://docs.python.org/3/library/functions.html#float)* | **None*) – A minimum value which determines whether pruner prunes or not.
If an intermediate value is smaller than lower, it prunes.
- **upper** ([*float*](https://docs.python.org/3/library/functions.html#float)* | **None*) – A maximum value which determines whether pruner prunes or not.
If an intermediate value is larger than upper, it prunes.
- **n_warmup_steps** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Pruning is disabled if the step is less than the given number of warmup steps.
- **interval_steps** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Interval in number of steps between the pruning checks, offset by the warmup steps.
If no value has been reported at the time of a pruning check, that particular check
will be postponed until a value is reported. Value must be at least 1.




Methods




[`prune`](#optuna.pruners.ThresholdPruner.prune)(study, trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_threshold.html#ThresholdPruner.prune)[](#optuna.pruners.ThresholdPruner.prune)
Judge whether the trial should be pruned based on the reported values.


Note that this method is not supposed to be called by library users. Instead,
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) and [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) provide
user interfaces to implement pruning mechanism in an objective function.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Study object of the target study.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – FrozenTrial object of the target trial.
Take a copy before modifying this object.



Returns:
A boolean value representing whether the trial should be pruned.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)

---

## optuna.pruners.PatientPruner — Optuna 4.6.0 documentation
<a id="optunaprunersPatientPruner-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.PatientPruner.html

# optuna.pruners.PatientPruner[](#optuna-pruners-patientpruner)




*class *optuna.pruners.PatientPruner(*wrapped_pruner*, *patience*, *min_delta=0.0*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_patient.html#PatientPruner)[](#optuna.pruners.PatientPruner)
Pruner which wraps another pruner with tolerance.


This pruner monitors intermediate values in a trial and prunes the trial if the improvement in
the intermediate values after a patience period is less than a threshold.



The pruner handles NaN values in the following manner:1. If all intermediate values before or during the patient period are NaN, the trial will
not be pruned
2. During the pruning calculations, NaN values are ignored. Only valid numeric values are
considered.




Example


```
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
```




Parameters:
- **wrapped_pruner** ([*BasePruner*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner)* | **None*) – Wrapped pruner to perform pruning when [`PatientPruner`](#optuna.pruners.PatientPruner) allows a
trial to be pruned. If it is [`None`](https://docs.python.org/3/library/constants.html#None), this pruner is equivalent to
early-stopping taken the intermediate values in the individual trial.
- **patience** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Pruning is disabled until the objective doesn’t improve for
`patience` consecutive steps.
- **min_delta** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Tolerance value to check whether or not the objective improves.
This value should be non-negative.





Note


Added in v2.8.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.8.0](https://github.com/optuna/optuna/releases/tag/v2.8.0).



Methods




[`prune`](#optuna.pruners.PatientPruner.prune)(study, trial)


Judge whether the trial should be pruned based on the reported values.







prune(*study*, *trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/pruners/_patient.html#PatientPruner.prune)[](#optuna.pruners.PatientPruner.prune)
Judge whether the trial should be pruned based on the reported values.


Note that this method is not supposed to be called by library users. Instead,
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) and [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) provide
user interfaces to implement pruning mechanism in an objective function.



Parameters:
- **study** ([*Study*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study)) – Study object of the target study.
- **trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – FrozenTrial object of the target trial.
Take a copy before modifying this object.



Returns:
A boolean value representing whether the trial should be pruned.



Return type:
[bool](https://docs.python.org/3/library/functions.html#bool)

---

## User-Defined Pruner — Optuna 4.6.0 documentation
<a id="User-Defined-Pruner-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/006_user_defined_pruner.html

Note


[Go to the end](#sphx-glr-download-tutorial-20-recipes-006-user-defined-pruner-py)
to download the full example code.




# User-Defined Pruner[](#user-defined-pruner)


In [`optuna.pruners`](https://optuna.readthedocs.io/en/stable/reference/pruners.html#module-optuna.pruners), we described how an objective function can optionally include
calls to a pruning feature which allows Optuna to terminate an optimization
trial when intermediate results do not appear promising. In this document, we
describe how to implement your own pruner, i.e., a custom strategy for
determining when to stop a trial.



## Overview of Pruning Interface[](#overview-of-pruning-interface)


The [`create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html#optuna.study.create_study) constructor takes, as an optional
argument, a pruner inheriting from [`BasePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner). The
pruner should implement the abstract method
[`prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner.prune), which takes arguments for the
associated [`Study`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study) and [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial) and
returns a boolean value: [`True`](https://docs.python.org/3/library/constants.html#True) if the trial should be pruned and [`False`](https://docs.python.org/3/library/constants.html#False)
otherwise. Using the Study and Trial objects, you can access all other trials
through the [`get_trials()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.get_trials) method and, and from a trial,
its reported intermediate values through the
[`intermediate_values()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial.intermediate_values) (a
dictionary which maps an integer `step` to a float value).


You can refer to the source code of the built-in Optuna pruners as templates for
building your own. In this document, for illustration, we describe the
construction and usage of a simple (but aggressive) pruner which prunes trials
that are in last place compared to completed trials at the same step.



Note


Please refer to the documentation of [`BasePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.BasePruner.html#optuna.pruners.BasePruner) or,
for example, [`ThresholdPruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.ThresholdPruner.html#optuna.pruners.ThresholdPruner) or
[`PercentilePruner`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.pruners.PercentilePruner.html#optuna.pruners.PercentilePruner) for more robust examples of pruner
implementation, including error checking and complex pruner-internal logic.





## An Example: Implementing `LastPlacePruner`[](#an-example-implementing-lastplacepruner)


We aim to optimize the `loss` and `alpha` hyperparameters for a stochastic
gradient descent classifier (`SGDClassifier`) run on the sklearn iris dataset. We
implement a pruner which terminates a trial at a certain step if it is in last
place compared to completed trials at the same step. We begin considering
pruning after a “warmup” of 1 training step and 5 completed trials. For
demonstration purposes, we [`print()`](https://docs.python.org/3/library/functions.html#print) a diagnostic message from `prune` when
it is about to return [`True`](https://docs.python.org/3/library/constants.html#True) (indicating pruning).


It may be important to note that the `SGDClassifier` score, as it is evaluated on
a holdout set, decreases with enough training steps due to overfitting. This
means that a trial could be pruned even if it had a favorable (high) value on a
previous training set. After pruning, Optuna will take the intermediate value
last reported as the value of the trial.


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier

import optuna
from optuna.pruners import BasePruner
from optuna.trial._state import TrialState


class LastPlacePruner(BasePruner):
    def __init__(self, warmup_steps, warmup_trials):
        self._warmup_steps = warmup_steps
        self._warmup_trials = warmup_trials

    def prune(self, study: "optuna.study.Study", trial: "optuna.trial.FrozenTrial") -> bool:
        # Get the latest score reported from this trial
        step = trial.last_step

        if step:  # trial.last_step == None when no scores have been reported yet
            this_score = trial.intermediate_values[step]

            # Get scores from other trials in the study reported at the same step
            completed_trials = study.get_trials(deepcopy=False, states=(TrialState.COMPLETE,))
            other_scores = [
                t.intermediate_values[step]
                for t in completed_trials
                if step in t.intermediate_values
            ]
            other_scores = sorted(other_scores)

            # Prune if this trial at this step has a lower value than all completed trials
            # at the same step. Note that steps will begin numbering at 0 in the objective
            # function definition below.
            if step >= self._warmup_steps and len(other_scores) > self._warmup_trials:
                if this_score < other_scores[0]:
                    print(f"prune() True: Trial {trial.number}, Step {step}, Score {this_score}")
                    return True

        return False
```



Lastly, let’s confirm the implementation is correct with the simple hyperparameter optimization.


```
def objective(trial):
    iris = load_iris()
    classes = np.unique(iris.target)
    X_train, X_valid, y_train, y_valid = train_test_split(
        iris.data, iris.target, train_size=100, test_size=50, random_state=0
    )

    loss = trial.suggest_categorical("loss", ["hinge", "log_loss", "perceptron"])
    alpha = trial.suggest_float("alpha", 0.00001, 0.001, log=True)
    clf = SGDClassifier(loss=loss, alpha=alpha, random_state=0)
    score = 0

    for step in range(0, 5):
        clf.partial_fit(X_train, y_train, classes=classes)
        score = clf.score(X_valid, y_valid)

        trial.report(score, step)

        if trial.should_prune():
            raise optuna.TrialPruned()

    return score


pruner = LastPlacePruner(warmup_steps=1, warmup_trials=5)
study = optuna.create_study(direction="maximize", pruner=pruner)
study.optimize(objective, n_trials=50)
```



```
prune() True: Trial 9, Step 3, Score 0.48
prune() True: Trial 11, Step 1, Score 0.36
prune() True: Trial 16, Step 4, Score 0.5
prune() True: Trial 28, Step 1, Score 0.34
prune() True: Trial 41, Step 1, Score 0.38
prune() True: Trial 43, Step 1, Score 0.34
prune() True: Trial 44, Step 1, Score 0.38
prune() True: Trial 45, Step 2, Score 0.48
prune() True: Trial 49, Step 4, Score 0.62
```



**Total running time of the script:** (0 minutes 0.467 seconds)




[`Download Jupyter notebook: 006_user_defined_pruner.ipynb`](https://optuna.readthedocs.io/en/stable/_downloads/78587bcda498aafb5da0880193ba8ebe/006_user_defined_pruner.ipynb)




[`Download Python source code: 006_user_defined_pruner.py`](https://optuna.readthedocs.io/en/stable/_downloads/367a7656d509bad6b4c2a664ffbc3653/006_user_defined_pruner.py)




[`Download zipped: 006_user_defined_pruner.zip`](https://optuna.readthedocs.io/en/stable/_downloads/574bb163a740d2709fd49ffb3f7c592b/006_user_defined_pruner.zip)




[Gallery generated by Sphinx-Gallery](https://sphinx-gallery.github.io)

---

## Ask-and-Tell Interface — Optuna 4.6.0 documentation
<a id="Ask-and-Tell-Interface-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html

Note


[Go to the end](#sphx-glr-download-tutorial-20-recipes-009-ask-and-tell-py)
to download the full example code.




# Ask-and-Tell Interface[](#ask-and-tell-interface)


Optuna has an Ask-and-Tell interface, which provides a more flexible interface for hyperparameter optimization.
This tutorial explains three use-cases when the ask-and-tell interface is beneficial:


- [Apply Optuna to an existing optimization problem with minimum modifications](#apply-optuna-to-an-existing-optimization-problem-with-minimum-modifications)
- [Define-and-Run](#define-and-run)
- [Batch Optimization](#batch-optimization)



## Apply Optuna to an existing optimization problem with minimum modifications[](#apply-optuna-to-an-existing-optimization-problem-with-minimum-modifications)


Let’s consider the traditional supervised classification problem; you aim to maximize the validation accuracy.
To do so, you train LogisticRegression as a simple model.


```
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import optuna


X, y = make_classification(n_features=10)
X_train, X_test, y_train, y_test = train_test_split(X, y)

C = 0.01
clf = LogisticRegression(C=C)
clf.fit(X_train, y_train)
val_accuracy = clf.score(X_test, y_test)  # the objective
```



Then you try to optimize hyperparameters `C` and `solver` of the classifier by using optuna.
When you introduce optuna naively, you define an `objective` function
such that it takes `trial` and calls `suggest_*` methods of `trial` to sample the hyperparameters:


```
def objective(trial):
    X, y = make_classification(n_features=10)
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    C = trial.suggest_float("C", 1e-7, 10.0, log=True)
    solver = trial.suggest_categorical("solver", ("lbfgs", "saga"))

    clf = LogisticRegression(C=C, solver=solver)
    clf.fit(X_train, y_train)
    val_accuracy = clf.score(X_test, y_test)

    return val_accuracy


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=10)
```



This interface is not flexible enough.
For example, if `objective` requires additional arguments other than `trial`,
you need to define a class as in
[How to define objective functions that have own arguments?](https://optuna.readthedocs.io/en/stable/faq.html#how-to-define-objective-functions-that-have-own-arguments).
The ask-and-tell interface provides a more flexible syntax to optimize hyperparameters.
The following example is equivalent to the previous code block.


```
study = optuna.create_study(direction="maximize")

n_trials = 10
for _ in range(n_trials):
    trial = study.ask()  # `trial` is a `Trial` and not a `FrozenTrial`.

    C = trial.suggest_float("C", 1e-7, 10.0, log=True)
    solver = trial.suggest_categorical("solver", ("lbfgs", "saga"))

    clf = LogisticRegression(C=C, solver=solver)
    clf.fit(X_train, y_train)
    val_accuracy = clf.score(X_test, y_test)

    study.tell(trial, val_accuracy)  # tell the pair of trial and objective value
```



The main difference is to use two methods: [`optuna.study.Study.ask()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.ask)
and [`optuna.study.Study.tell()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.tell).
[`optuna.study.Study.ask()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.ask) creates a trial that can sample hyperparameters, and
[`optuna.study.Study.tell()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.tell) finishes the trial by passing `trial` and an objective value.
You can apply Optuna’s hyperparameter optimization to your original code
without an `objective` function.


If you want to make your optimization faster with a pruner, you need to explicitly pass the state of trial
to the argument of [`optuna.study.Study.tell()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.tell) method as follows:


```
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

import optuna


X, y = load_iris(return_X_y=True)
X_train, X_valid, y_train, y_valid = train_test_split(X, y)
classes = np.unique(y)
n_train_iter = 100

# define study with hyperband pruner.
study = optuna.create_study(
    direction="maximize",
    pruner=optuna.pruners.HyperbandPruner(
        min_resource=1, max_resource=n_train_iter, reduction_factor=3
    ),
)

for _ in range(20):
    trial = study.ask()

    alpha = trial.suggest_float("alpha", 0.0, 1.0)

    clf = SGDClassifier(alpha=alpha)
    pruned_trial = False

    for step in range(n_train_iter):
        clf.partial_fit(X_train, y_train, classes=classes)

        intermediate_value = clf.score(X_valid, y_valid)
        trial.report(intermediate_value, step)

        if trial.should_prune():
            pruned_trial = True
            break

    if pruned_trial:
        study.tell(trial, state=optuna.trial.TrialState.PRUNED)  # tell the pruned state
    else:
        score = clf.score(X_valid, y_valid)
        study.tell(trial, score)  # tell objective value
```




Note


[`optuna.study.Study.tell()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.tell) method can take a trial number rather than the trial object.
`study.tell(trial.number, y)` is equivalent to `study.tell(trial, y)`.





## Define-and-Run[](#define-and-run)


The ask-and-tell interface supports both define-by-run and define-and-run APIs.
This section shows the example of the define-and-run API
in addition to the define-by-run example above.


Define distributions for the hyperparameters before calling the
[`optuna.study.Study.ask()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.ask) method for define-and-run API.
For example,


```
distributions = {
    "C": optuna.distributions.FloatDistribution(1e-7, 10.0, log=True),
    "solver": optuna.distributions.CategoricalDistribution(("lbfgs", "saga")),
}
```



Pass `distributions` to [`optuna.study.Study.ask()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.ask) method at each call.
The retuned `trial` contains the suggested hyperparameters.


```
study = optuna.create_study(direction="maximize")
n_trials = 10
for _ in range(n_trials):
    trial = study.ask(distributions)  # pass the pre-defined distributions.

    # two hyperparameters are already sampled from the pre-defined distributions
    C = trial.params["C"]
    solver = trial.params["solver"]

    clf = LogisticRegression(C=C, solver=solver)
    clf.fit(X_train, y_train)
    val_accuracy = clf.score(X_test, y_test)

    study.tell(trial, val_accuracy)
```





## Batch Optimization[](#batch-optimization)


The ask-and-tell interface enables us to optimize a batched objective for faster optimization.
For example, parallelizable evaluation, operation over vectors, etc.


The following objective takes batched hyperparameters `xs` and `ys` instead of a single
pair of hyperparameters `x` and `y` and calculates the objective over the full vectors.


```
def batched_objective(xs: np.ndarray, ys: np.ndarray):
    return xs**2 + ys
```



In the following example, the number of pairs of hyperparameters in a batch is \(10\),
and `batched_objective` is evaluated three times.
Thus, the number of trials is \(30\).
Note that you need to store either `trial_numbers` or `trial` to call
[`optuna.study.Study.tell()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.tell) method after the batched evaluations.


```
batch_size = 10
study = optuna.create_study(sampler=optuna.samplers.CmaEsSampler())

for _ in range(3):
    # create batch
    trial_numbers = []
    x_batch = []
    y_batch = []
    for _ in range(batch_size):
        trial = study.ask()
        trial_numbers.append(trial.number)
        x_batch.append(trial.suggest_float("x", -10, 10))
        y_batch.append(trial.suggest_float("y", -10, 10))

    # evaluate batched objective
    x_batch = np.array(x_batch)
    y_batch = np.array(y_batch)
    objectives = batched_objective(x_batch, y_batch)

    # finish all trials in the batch
    for trial_number, objective in zip(trial_numbers, objectives):
        study.tell(trial_number, objective)
```




Tip


[`optuna.samplers.TPESampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.TPESampler.html#optuna.samplers.TPESampler) class can take a boolean parameter `constant_liar`. It
is recommended to set this value to `True` during batched optimization to avoid having
multiple workers evaluating similar parameter configurations. In particular, if each
objective function evaluation is costly and the durations of the running states are
significant, and/or the number of workers is high.




Tip


[`optuna.samplers.CmaEsSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.CmaEsSampler.html#optuna.samplers.CmaEsSampler) class can take a `popsize` attribute parameter
used as the initial population size for the CMA-ES algorithm. In the context of batched
optimization, it can  be set equal to a multiple of the batch size in order to benefit from
parallelizable operations.



**Total running time of the script:** (0 minutes 0.102 seconds)




[`Download Jupyter notebook: 009_ask_and_tell.ipynb`](https://optuna.readthedocs.io/en/stable/_downloads/9e17bbf554dfa22e6c92f27c8c7df53d/009_ask_and_tell.ipynb)




[`Download Python source code: 009_ask_and_tell.py`](https://optuna.readthedocs.io/en/stable/_downloads/a6d16f5a7630e2042b959f18c4d3f2e5/009_ask_and_tell.py)




[`Download zipped: 009_ask_and_tell.zip`](https://optuna.readthedocs.io/en/stable/_downloads/d0f87c1ba4c55129d14d65a505e11426/009_ask_and_tell.zip)




[Gallery generated by Sphinx-Gallery](https://sphinx-gallery.github.io)

---

## optuna.TrialPruned — Optuna 4.6.0 documentation
<a id="optunaTrialPruned-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.TrialPruned.html

# optuna.TrialPruned[](#optuna-trialpruned)




*exception *optuna.TrialPruned[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/exceptions.html#TrialPruned)[](#optuna.TrialPruned)
Exception for pruned trials.


This error tells a trainer that the current [`Trial`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial) was pruned. It is
supposed to be raised after [`optuna.trial.Trial.should_prune()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.should_prune) as shown in the following
example.



See also


[`optuna.TrialPruned`](#optuna.TrialPruned) is an alias of [`optuna.exceptions.TrialPruned`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.exceptions.TrialPruned.html#optuna.exceptions.TrialPruned).



Example


```
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


study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=20)
```





add_note()[](#optuna.TrialPruned.add_note)
Exception.add_note(note) –
add a note to the exception

---

## optuna.storages.RetryFailedTrialCallback — Optuna 4.6.0 documentation
<a id="optunastoragesRetryFailedTrialCallback-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.storages.RetryFailedTrialCallback.html

# optuna.storages.RetryFailedTrialCallback[](#optuna-storages-retryfailedtrialcallback)




*class *optuna.storages.RetryFailedTrialCallback(*max_retry=None*, *inherit_intermediate_values=False*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/storages/_callbacks.html#RetryFailedTrialCallback)[](#optuna.storages.RetryFailedTrialCallback)
Retry a failed trial up to a maximum number of times.


When a trial fails, this callback can be used with a class in [`optuna.storages`](https://optuna.readthedocs.io/en/stable/reference/storages.html#module-optuna.storages) to
recreate the trial in `TrialState.WAITING` to queue up the trial to be run again.


The failed trial can be identified by the
[`retried_trial_number()`](#optuna.storages.RetryFailedTrialCallback.retried_trial_number) function.
Even if repetitive failure occurs (a retried trial fails again),
this method returns the number of the original trial.
To get a full list including the numbers of the retried trials as well as their original trial,
call the [`retry_history()`](#optuna.storages.RetryFailedTrialCallback.retry_history) function.


This callback is helpful in environments where trials may fail due to external conditions,
such as being preempted by other processes.


Usage:


> import optuna
> from optuna.storages import RetryFailedTrialCallback
> storage = optuna.storages.RDBStorage(
>     url="sqlite:///:memory:",
>     heartbeat_interval=60,
>     grace_period=120,
>     failed_trial_callback=RetryFailedTrialCallback(max_retry=3),
> )
> study = optuna.create_study(
>     storage=storage,
> )



See also


See [`RDBStorage`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.storages.RDBStorage.html#optuna.storages.RDBStorage).




Parameters:
- **max_retry** ([*int*](https://docs.python.org/3/library/functions.html#int)* | **None*) – The max number of times a trial can be retried. Must be set to [`None`](https://docs.python.org/3/library/constants.html#None) or an
integer. If set to the default value of [`None`](https://docs.python.org/3/library/constants.html#None) will retry indefinitely.
If set to an integer, will only retry that many times.
- **inherit_intermediate_values** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Option to inherit trial.intermediate_values reported by
[`optuna.trial.Trial.report()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial.report) from the failed trial. Default is [`False`](https://docs.python.org/3/library/constants.html#False).





Note


Added in v2.8.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.8.0](https://github.com/optuna/optuna/releases/tag/v2.8.0).



Methods




[`retried_trial_number`](#optuna.storages.RetryFailedTrialCallback.retried_trial_number)(trial)


Return the number of the original trial being retried.



[`retry_history`](#optuna.storages.RetryFailedTrialCallback.retry_history)(trial)


Return the list of retried trial numbers with respect to the specified trial.







*static *retried_trial_number(*trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/storages/_callbacks.html#RetryFailedTrialCallback.retried_trial_number)[](#optuna.storages.RetryFailedTrialCallback.retried_trial_number)
Return the number of the original trial being retried.



Parameters:
**trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – The trial object.



Returns:
The number of the first failed trial. If not retry of a previous trial,
returns [`None`](https://docs.python.org/3/library/constants.html#None).



Return type:
[int](https://docs.python.org/3/library/functions.html#int) | None





Note


Added in v2.8.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v2.8.0](https://github.com/optuna/optuna/releases/tag/v2.8.0).






*static *retry_history(*trial*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/storages/_callbacks.html#RetryFailedTrialCallback.retry_history)[](#optuna.storages.RetryFailedTrialCallback.retry_history)
Return the list of retried trial numbers with respect to the specified trial.



Parameters:
**trial** ([*FrozenTrial*](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.FrozenTrial.html#optuna.trial.FrozenTrial)) – The trial object.



Returns:
A list of trial numbers in ascending order of the series of retried trials.
The first item of the list indicates the original trial which is identical
to the [`retried_trial_number()`](#optuna.storages.RetryFailedTrialCallback.retried_trial_number),
and the last item is the one right before the specified trial in the retry series.
If the specified trial is not a retry of any trial, returns an empty list.



Return type:
[list](https://docs.python.org/3/library/stdtypes.html#list)[[int](https://docs.python.org/3/library/functions.html#int)]





Note


Added in v3.0.0 as an experimental feature. The interface may change in newer versions
without prior notice. See [https://github.com/optuna/optuna/releases/tag/v3.0.0](https://github.com/optuna/optuna/releases/tag/v3.0.0).

---

## optuna.copy_study — Optuna 4.6.0 documentation
<a id="optunacopy_study-Optuna-460-documentation"></a>

- 元URL: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.copy_study.html

# optuna.copy_study[](#optuna-copy-study)




optuna.copy_study(***, *from_study_name*, *from_storage*, *to_storage*, *to_study_name=None*)[[source]](https://optuna.readthedocs.io/en/stable/_modules/optuna/study/study.html#copy_study)[](#optuna.copy_study)
Copy study from one storage to another.


The direction(s) of the objective(s) in the study, trials, user attributes and system
attributes are copied.



Note


[`copy_study()`](#optuna.copy_study) copies a study even if the optimization is working on.
It means users will get a copied study that contains a trial that is not finished.



Example


```
import optuna


def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    return (x - 2) ** 2


study = optuna.create_study(
    study_name="example-study",
    storage="sqlite:///example.db",
)
study.optimize(objective, n_trials=3)

optuna.copy_study(
    from_study_name="example-study",
    from_storage="sqlite:///example.db",
    to_storage="sqlite:///example_copy.db",
)

study = optuna.load_study(
    study_name=None,
    storage="sqlite:///example_copy.db",
)
```




Parameters:
- **from_study_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of study.
- **from_storage** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **BaseStorage*) – Source database URL such as `sqlite:///example.db`. Please see also the
documentation of [`create_study()`](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.create_study.html#optuna.study.create_study) for further details.
- **to_storage** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **BaseStorage*) – Destination database URL.
- **to_study_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)* | **None*) – Name of the created study. If omitted, `from_study_name` is used.



Raises:
[**DuplicatedStudyError**](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.exceptions.DuplicatedStudyError.html#optuna.exceptions.DuplicatedStudyError) – If a study with a conflicting name already exists in the destination storage.



Return type:
None
