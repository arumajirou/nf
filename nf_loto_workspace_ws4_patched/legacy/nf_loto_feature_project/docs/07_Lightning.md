# Lightning

- 抽出日時: 2025-11-12 10:56
- 件数: 7

## 目次
1. [Logging — PyTorch Lightning 2.5.6 documentation](#Logging-PyTorch-Lightning-256-documentation)
2. [Lightning AI | Turn ideas into AI, Lightning fast](#Lightning-AI-Turn-ideas-into-AI-Lightning-fast)
3. [Lightning AI | Turn ideas into AI, Lightning fast](#Lightning-AI-Turn-ideas-into-AI-Lightning-fast)
4. [Lightning AI | Turn ideas into AI, Lightning fast](#Lightning-AI-Turn-ideas-into-AI-Lightning-fast)
5. [Lightning environments - Community-built, reproducible AI environments](#Lightning-environments-Community-built-reproducible-AI-environments)
6. [Lightning AI | Turn ideas into AI, Lightning fast](#Lightning-AI-Turn-ideas-into-AI-Lightning-fast)
7. [Lightning AI | Turn ideas into AI, Lightning fast](#Lightning-AI-Turn-ideas-into-AI-Lightning-fast)


---

## Logging — PyTorch Lightning 2.5.6 documentation
<a id="Logging-PyTorch-Lightning-256-documentation"></a>

- 元URL: https://lightning.ai/docs/pytorch/stable/extensions/logging.html

# Logging[¶](#logging)



## Supported Loggers[¶](#supported-loggers)


The following are loggers we support:




[`CometLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.CometLogger.html#lightning.pytorch.loggers.CometLogger)


Track your parameters, metrics, source code and more using [Comet](https://www.comet.com/?utm_source=lightning.pytorch&utm_medium=referral).



[`CSVLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.CSVLogger.html#lightning.pytorch.loggers.CSVLogger)


Log to local file system in yaml and CSV format.



[`MLFlowLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.MLFlowLogger.html#lightning.pytorch.loggers.MLFlowLogger)


Log using [MLflow](https://mlflow.org).



[`NeptuneLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.NeptuneLogger.html#lightning.pytorch.loggers.NeptuneLogger)


Log using [Neptune](https://docs.neptune.ai/integrations/lightning/).



[`TensorBoardLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.TensorBoardLogger.html#lightning.pytorch.loggers.TensorBoardLogger)


Log to local or remote file system in [TensorBoard](https://www.tensorflow.org/tensorboard) format.



[`WandbLogger`](https://lightning.ai/docs/pytorch/stable/extensions/generated/lightning.pytorch.loggers.WandbLogger.html#lightning.pytorch.loggers.WandbLogger)


Log using [Weights and Biases](https://docs.wandb.ai/guides/integrations/lightning).





The above loggers will normally plot an additional chart (**global_step VS epoch**). Depending on the loggers you use, there might be some additional charts too.


By default, Lightning uses `TensorBoard` logger under the hood, and stores the logs to a directory (by default in `lightning_logs/`).


```
from lightning.pytorch import Trainer

# Automatically logs to a directory (by default ``lightning_logs/``)
trainer = Trainer()
```



To see your logs:


```
tensorboard --logdir=lightning_logs/
```



To visualize tensorboard in a jupyter notebook environment, run the following command in a jupyter cell:


```
%reload_ext tensorboard
%tensorboard --logdir=lightning_logs/
```



You can also pass a custom Logger to the [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer).


```
from lightning.pytorch import loggers as pl_loggers

tb_logger = pl_loggers.TensorBoardLogger(save_dir="logs/")
trainer = Trainer(logger=tb_logger)
```



Choose from any of the others such as MLflow, Comet, Neptune, WandB, etc.


```
comet_logger = pl_loggers.CometLogger(save_dir="logs/")
trainer = Trainer(logger=comet_logger)
```



To use multiple loggers, simply pass in a `list` or `tuple` of loggers.


```
tb_logger = pl_loggers.TensorBoardLogger(save_dir="logs/")
comet_logger = pl_loggers.CometLogger(save_dir="logs/")
trainer = Trainer(logger=[tb_logger, comet_logger])
```




Note


By default, Lightning logs every 50 steps. Use Trainer flags to [Control Logging Frequency](#logging-frequency).




Note


By default, all loggers log to `os.getcwd()`. You can change the logging path using
`Trainer(default_root_dir="/your/path/to/save/checkpoints")` without instantiating a logger.






## Logging from a LightningModule[¶](#logging-from-a-lightningmodule)


Lightning offers automatic log functionalities for logging scalars, or manual logging for anything else.



### Automatic Logging[¶](#automatic-logging)


Use the [`log()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log) or [`log_dict()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log_dict)
methods to log from anywhere in a [LightningModule](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html) and [callbacks](https://lightning.ai/docs/pytorch/stable/extensions/callbacks.html).


```
def training_step(self, batch, batch_idx):
    self.log("my_metric", x)


# or a dict to log all metrics at once with individual plots
def training_step(self, batch, batch_idx):
    self.log_dict({"acc": acc, "recall": recall})
```




Note


Everything explained below applies to both [`log()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log) or [`log_dict()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log_dict) methods.




Note


When using TorchMetrics with Lightning, we recommend referring to the [TorchMetrics Lightning integration documentation](https://lightning.ai/docs/torchmetrics/v1.8.2/pages/lightning.html) for logging best practices, common pitfalls, and proper usage patterns.



Depending on where the [`log()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log) method is called, Lightning auto-determines
the correct logging mode for you. Of course you can override the default behavior by manually setting the
[`log()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log) parameters.


```
def training_step(self, batch, batch_idx):
    self.log("my_loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
```



The [`log()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log) method has a few options:


- `on_step`: Logs the metric at the current step.
- `on_epoch`: Automatically accumulates and logs at the end of the epoch.
- `prog_bar`: Logs to the progress bar (Default: `False`).
- `logger`: Logs to the logger like `Tensorboard`, or any other custom logger passed to the [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer) (Default: `True`).
- `reduce_fx`: Reduction function over step values for end of epoch. Uses [`torch.mean()`](https://docs.pytorch.org/docs/stable/generated/torch.mean.html#torch.mean) by default and is not applied when a [`torchmetrics.Metric`](https://lightning.ai/docs/torchmetrics/stable/references/metric.html#torchmetrics.Metric) is logged.
- `enable_graph`: If True, will not auto detach the graph.
- `sync_dist`: If True, reduces the metric across devices. Use with care as this may lead to a significant communication overhead.
- `sync_dist_group`: The DDP group to sync across.
- `add_dataloader_idx`: If True, appends the index of the current dataloader to the name (when using multiple dataloaders). If False, user needs to give unique names for each dataloader to not mix the values.
- `batch_size`: Current batch size used for accumulating logs logged with `on_epoch=True`. This will be directly inferred from the loaded batch, but for some data structures you might need to explicitly provide it.
- `rank_zero_only`: Set this to `True` only if you call `self.log` explicitly only from rank 0. If `True` you won’t be able to access or specify this metric in callbacks (e.g. early stopping).



Default behavior of logging in Callback or LightningModule[¶](#id3)






Hook


on_step


on_epoch





on_train_start, on_train_epoch_start, on_train_epoch_end


False


True



on_before_backward, on_after_backward, on_before_optimizer_step, on_before_zero_grad


True


False



on_train_batch_start, on_train_batch_end, training_step


True


False



on_validation_start, on_validation_epoch_start, on_validation_epoch_end


False


True



on_validation_batch_start, on_validation_batch_end, validation_step


False


True






Note


While logging tensor metrics with `on_epoch=True` inside step-level hooks and using mean-reduction (default) to accumulate the metrics across the current epoch, Lightning tries to extract the
batch size from the current batch. If multiple possible batch sizes are found, a warning is logged and if it fails to extract the batch size from the current batch, which is possible if
the batch is a custom structure/collection, then an error is raised. To avoid this, you can specify the `batch_size` inside the `self.log(... batch_size=batch_size)` call.


```
def training_step(self, batch, batch_idx):
    # extracts the batch size from `batch`
    self.log("train_loss", loss, on_epoch=True)


def validation_step(self, batch, batch_idx):
    # uses `batch_size=10`
    self.log("val_loss", loss, batch_size=10)
```





Note


- The above config for `validation` applies for `test` hooks as well.
- Setting `on_epoch=True` will cache all your logged values during the full training epoch and perform a
reduction in `on_train_epoch_end`. We recommend using [TorchMetrics](https://torchmetrics.readthedocs.io/), when working with custom reduction.
- Setting both `on_step=True` and `on_epoch=True` will create two keys per metric you log with
suffix `_step` and `_epoch` respectively. You can refer to these keys e.g. in the monitor
argument of [`ModelCheckpoint`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html#lightning.pytorch.callbacks.ModelCheckpoint) or in the graphs plotted to the logger of your choice.



If your work requires to log in an unsupported method, please open an issue with a clear description of why it is blocking you.




### Manual Logging Non-Scalar Artifacts[¶](#manual-logging-non-scalar-artifacts)


If you want to log anything that is not a scalar, like histograms, text, images, etc., you may need to use the logger object directly.


```
def training_step(self):
    ...
    # the logger you used (in this case tensorboard)
    tensorboard = self.logger.experiment
    tensorboard.add_image()
    tensorboard.add_histogram(...)
    tensorboard.add_figure(...)
```







## Make a Custom Logger[¶](#make-a-custom-logger)


You can implement your own logger by writing a class that inherits from [`Logger`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.loggers.logger.html#lightning.pytorch.loggers.logger.Logger).
Use the `rank_zero_experiment()` and `rank_zero_only()` decorators to make sure that only the first process in DDP training creates the experiment and logs the data respectively.


```
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
        # Optional. Any code necessary to save logger data goes here
        pass

    @rank_zero_only
    def finalize(self, status):
        # Optional. Any code that needs to be run after training
        # finishes goes here
        pass
```



If you write a logger that may be useful to others, please send
a pull request to add it to Lightning!





## Control Logging Frequency[¶](#control-logging-frequency)



### Logging frequency[¶](#id2)


It may slow down training to log on every single batch. By default, Lightning logs every 50 rows, or 50 training steps.
To change this behaviour, set the `log_every_n_steps` [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer) flag.


```
k = 10
trainer = Trainer(log_every_n_steps=k)
```





### Log Writing Frequency[¶](#log-writing-frequency)


Individual logger implementations determine their flushing frequency. For example, on the
[`CSVLogger`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.loggers.csv_logs.html#lightning.pytorch.loggers.csv_logs.CSVLogger) you can set the flag `flush_logs_every_n_steps`.






## Progress Bar[¶](#progress-bar)


You can add any metric to the progress bar using [`log()`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.core.LightningModule.html#lightning.pytorch.core.LightningModule.log)
method, setting `prog_bar=True`.


```
def training_step(self, batch, batch_idx):
    self.log("my_loss", loss, prog_bar=True)
```



You could learn more about progress bars supported by Lightning [here](https://lightning.ai/docs/pytorch/stable/common/progress_bar.html).



### Modifying the Progress Bar[¶](#modifying-the-progress-bar)


The progress bar by default already includes the training loss and version number of the experiment
if you are using a logger. These defaults can be customized by overriding the
`get_metrics()` hook in your logger.


```
from lightning.pytorch.callbacks.progress import TQDMProgressBar


class CustomProgressBar(TQDMProgressBar):
    def get_metrics(self, *args, **kwargs):
        # don't show the version number
        items = super().get_metrics(*args, **kwargs)
        items.pop("v_num", None)
        return items
```







## Configure Console Logging[¶](#configure-console-logging)


Lightning logs useful information about the training process and user warnings to the console.
You can retrieve the Lightning console logger and change it to your liking. For example, adjust the logging level
or redirect output for certain modules to log files:


```
import logging

# configure logging at the root level of Lightning
logging.getLogger("lightning.pytorch").setLevel(logging.ERROR)

# configure logging on module level, redirect to file
logger = logging.getLogger("lightning.pytorch.core")
logger.addHandler(logging.FileHandler("core.log"))
```



Read more about custom Python logging [here](https://docs.python.org/3/library/logging.html).





## Logging Hyperparameters[¶](#logging-hyperparameters)


When training a model, it is useful to know what hyperparams went into that model.
When Lightning creates a checkpoint, it stores a key `"hyper_parameters"` with the hyperparams.


```
lightning_checkpoint = torch.load(filepath, map_location=lambda storage, loc: storage)
hyperparams = lightning_checkpoint["hyper_parameters"]
```



Some loggers also allow logging the hyperparams used in the experiment. For instance,
when using the `TensorBoardLogger`, all hyperparams will show
in the hparams tab at [`torch.utils.tensorboard.writer.SummaryWriter.add_hparams()`](https://docs.pytorch.org/docs/stable/tensorboard.html#torch.utils.tensorboard.writer.SummaryWriter.add_hparams).



Note


If you want to track a metric in the tensorboard hparams tab, log scalars to the key `hp_metric`. If tracking multiple metrics, initialize `TensorBoardLogger` with `default_hp_metric=False` and call `log_hyperparams` only once with your metric keys and initial values. Subsequent updates can simply be logged to the metric keys. Refer to the examples below for setting up proper hyperparams metrics tracking within the [LightningModule](https://lightning.ai/docs/pytorch/stable/common/lightning_module.html).


```
# Using default_hp_metric
def validation_step(self, batch, batch_idx):
    self.log("hp_metric", some_scalar)


# Using custom or multiple metrics (default_hp_metric=False)
def on_train_start(self):
    self.logger.log_hyperparams(self.hparams, {"hp/metric_1": 0, "hp/metric_2": 0})


def validation_step(self, batch, batch_idx):
    self.log("hp/metric_1", some_scalar_1)
    self.log("hp/metric_2", some_scalar_2)
```



In the example, using `"hp/"` as a prefix allows for the metrics to be grouped under “hp” in the tensorboard scalar tab where you can collapse them.






## Managing Remote Filesystems[¶](#managing-remote-filesystems)


Lightning supports saving logs to a variety of filesystems, including local filesystems and several cloud storage providers.


Check out the [Remote Filesystems](https://lightning.ai/docs/pytorch/stable/common/remote_fs.html) doc for more info.

---

## Lightning AI | Turn ideas into AI, Lightning fast
<a id="Lightning-AI-Turn-ideas-into-AI-Lightning-fast"></a>

- 元URL: https://lightning.ai/?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme

The all-in-one platform for AI development. Code together. Prototype. Train. Scale. Serve. From your browser - with zero setup. From the creators of PyTorch Lightning.



---

## Lightning AI | Turn ideas into AI, Lightning fast
<a id="Lightning-AI-Turn-ideas-into-AI-Lightning-fast"></a>

- 元URL: https://lightning.ai/pricing?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme

The all-in-one platform for AI development. Code together. Prototype. Train. Scale. Serve. From your browser - with zero setup. From the creators of PyTorch Lightning.



---

## Lightning AI | Turn ideas into AI, Lightning fast
<a id="Lightning-AI-Turn-ideas-into-AI-Lightning-fast"></a>

- 元URL: https://lightning.ai/clusters?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme

The all-in-one platform for AI development. Code together. Prototype. Train. Scale. Serve. From your browser - with zero setup. From the creators of PyTorch Lightning.



---

## Lightning environments - Community-built, reproducible AI environments
<a id="Lightning-environments-Community-built-reproducible-AI-environments"></a>

- 元URL: https://lightning.ai/studios?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme

Reproducible environments to train and serve models, launch endpoints and more. Duplicate to your cloud. Run on your data.



---

## Lightning AI | Turn ideas into AI, Lightning fast
<a id="Lightning-AI-Turn-ideas-into-AI-Lightning-fast"></a>

- 元URL: https://lightning.ai/notebooks?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme

The all-in-one platform for AI development. Code together. Prototype. Train. Scale. Serve. From your browser - with zero setup. From the creators of PyTorch Lightning.



---

## Lightning AI | Turn ideas into AI, Lightning fast
<a id="Lightning-AI-Turn-ideas-into-AI-Lightning-fast"></a>

- 元URL: https://lightning.ai/deploy?utm_source=ptl_readme&utm_medium=referral&utm_campaign=ptl_readme

The all-in-one platform for AI development. Code together. Prototype. Train. Scale. Serve. From your browser - with zero setup. From the creators of PyTorch Lightning.


