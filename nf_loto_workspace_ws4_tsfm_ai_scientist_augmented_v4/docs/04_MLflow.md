# MLflow

- 抽出日時: 2025-11-12 10:56
- 件数: 14

## 目次
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

- 元URL: https://mlflow.org/docs/latest/ml/tracking/

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
## Quickstart[​](#quickstart)


If you haven't used MLflow Tracking before, we strongly recommend going through the following quickstart tutorial.


[MLflow Tracking QuickstartA great place to start to learn the fundamentals of MLflow Tracking! Learn in 5 minutes how to log, register, and load a model for inference.](https://mlflow.org/docs/latest/ml/tracking/quickstart/)
## Concepts[​](#concepts)


### Runs[​](#runs)


MLflow Tracking is organized around the concept of **runs**, which are executions of some piece of
data science code, for example, a single `python train.py` execution. Each run records metadata
(various information about your run such as metrics, parameters, start and end times) and artifacts
(output files from the run such as model weights, images, etc).


### Models[​](#models)


Models represent the trained machine learning artifacts that are produced during your runs. Logged Models contain their own metadata and artifacts similar to runs.


### Experiments[​](#experiments)


An experiment groups together runs and models for a specific task. You can create an experiment using the CLI, API, or UI.
The MLflow API and UI also let you create and search for experiments. See [Organizing Runs into Experiments](https://mlflow.org/docs/latest/ml/tracking/tracking-api/#experiment-organization)
for more details on how to organize your runs into experiments.


## Tracking Runs[​](#start-logging)


[MLflow Tracking APIs](https://mlflow.org/docs/latest/ml/tracking/tracking-api/) provide a set of functions to track your runs. For example, you can call [`mlflow.start_run()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.start_run) to start a new run,
then call [Logging Functions](https://mlflow.org/docs/latest/ml/tracking/tracking-api/) such as [`mlflow.log_param()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_param) and [`mlflow.log_metric()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_metric) to log parameters and metrics respectively.
Please visit the [Tracking API documentation](https://mlflow.org/docs/latest/ml/tracking/tracking-api/) for more details about using these APIs.


python```
import mlflowwith mlflow.start_run():    mlflow.log_param("lr", 0.001)    # Your ml code    ...    mlflow.log_metric("val_loss", val_loss)
```


Alternatively, [Auto-logging](https://mlflow.org/docs/latest/ml/tracking/autolog/) offers an ultra-quick setup for starting MLflow tracking.
This powerful feature allows you to log metrics, parameters, and models without the need for explicit log statements -
all you need to do is call [`mlflow.autolog()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.autolog) before your training code. Auto-logging supports popular
libraries such as [Scikit-learn](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-sklearn), [XGBoost](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-xgboost), [PyTorch](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-pytorch),
[Keras](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-keras), [Spark](https://mlflow.org/docs/latest/ml/tracking/autolog/#autolog-spark), and more. See [Automatic Logging Documentation](https://mlflow.org/docs/latest/ml/tracking/autolog/)
for supported libraries and how to use auto-logging APIs with each of them.


python```
import mlflowmlflow.autolog()# Your training code...
```


noteBy default, without any particular server/database configuration, MLflow Tracking logs data to the local `mlruns` directory.
If you want to log your runs to a different location, such as a remote database and cloud storage, in order to share your results with
your team, follow the instructions in the [Set up MLflow Tracking Environment](#tracking-setup) section.


### Searching Logged Models Programmatically[​](#search_logged_models)


MLflow 3 introduces powerful model search capabilities through [`mlflow.search_logged_models()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.search_logged_models). This API allows you to find specific models across your experiments based on performance metrics, parameters, and model attributes using SQL-like syntax.


python```
import mlflow# Find high-performing models across experimentstop_models = mlflow.search_logged_models(    experiment_ids=["1", "2"],    filter_string="metrics.accuracy > 0.95 AND params.model_type = 'RandomForest'",    order_by=[{"field_name": "metrics.f1_score", "ascending": False}],    max_results=5,)# Get the best model for deploymentbest_model = mlflow.search_logged_models(    experiment_ids=["1"],    filter_string="metrics.accuracy > 0.9",    max_results=1,    order_by=[{"field_name": "metrics.accuracy", "ascending": False}],    output_format="list",)[0]# Load the best model directlyloaded_model = mlflow.pyfunc.load_model(f"models:/{best_model.model_id}")
```


**Key Features:**


- **SQL-like filtering**: Use `metrics.`, `params.`, and attribute prefixes to build complex queries
- **Dataset-aware search**: Filter metrics based on specific datasets for fair model comparison
- **Flexible ordering**: Sort by multiple criteria to find the best models
- **Direct model loading**: Use the new `models:/<model_id>` URI format for immediate model access


For comprehensive examples and advanced search patterns, see the [Search Logged Models Guide](https://mlflow.org/docs/latest/ml/search/search-models/).


### Querying Runs Programmatically[​](#tracking_query_api)


You can also access all of the functions in the Tracking UI programmatically with [MlflowClient](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html#mlflow.client.MlflowClient).


For example, the following code snippet search for runs that has the best validation loss among all runs in the experiment.


python```
client = mlflow.tracking.MlflowClient()experiment_id = "0"best_run = client.search_runs(    experiment_id, order_by=["metrics.val_loss ASC"], max_results=1)[0]print(best_run.info)# {'run_id': '...', 'metrics': {'val_loss': 0.123}, ...}
```


## Tracking Models[​](#tracking-models)


MLflow 3 introduces enhanced model tracking capabilities that allow you to log multiple model checkpoints within a single run and track their performance against different datasets. This is particularly useful for deep learning workflows where you want to save and compare model checkpoints at different training stages.


### Logging Model Checkpoints[​](#logging-model-checkpoints)


You can log model checkpoints at different steps during training using the `step` parameter in model logging functions. Each logged model gets a unique model ID that you can use to reference it later.


python```
import mlflowimport mlflow.pytorchwith mlflow.start_run() as run:    for epoch in range(100):        # Train your model        train_model(model, epoch)        # Log model checkpoint every 10 epochs        if epoch % 10 == 0:            model_info = mlflow.pytorch.log_model(                pytorch_model=model,                name=f"checkpoint-epoch-{epoch}",                step=epoch,                input_example=sample_input,            )            # Log metrics linked to this specific model checkpoint            accuracy = evaluate_model(model, validation_data)            mlflow.log_metric(                key="accuracy",                value=accuracy,                step=epoch,                model_id=model_info.model_id,  # Link metric to specific model                dataset=validation_dataset,            )
```


### Linking Metrics to Models and Datasets[​](#linking-metrics-to-models-and-datasets)


MLflow 3 allows you to link metrics to specific model checkpoints and datasets, providing better traceability of model performance:


python```
# Create a dataset referencetrain_dataset = mlflow.data.from_pandas(train_df, name="training_data")# Log metric with model and dataset linksmlflow.log_metric(    key="f1_score",    value=0.95,    step=epoch,    model_id=model_info.model_id,  # Links to specific model checkpoint    dataset=train_dataset,  # Links to specific dataset)
```


### Searching and Ranking Model Checkpoints[​](#searching-and-ranking-model-checkpoints)


Use [`mlflow.search_logged_models()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.search_logged_models) to search and rank model checkpoints based on their performance metrics:


python```
# Search for all models in a run, ordered by accuracyranked_models = mlflow.search_logged_models(    filter_string=f"source_run_id='{run.info.run_id}'",    order_by=[{"field_name": "metrics.accuracy", "ascending": False}],    output_format="list",)# Get the best performing modelbest_model = ranked_models[0]print(f"Best model: {best_model.name}")print(f"Accuracy: {best_model.metrics[0].value}")# Load the best model for inferenceloaded_model = mlflow.pyfunc.load_model(f"models:/{best_model.model_id}")
```


### Model URIs in MLflow 3[​](#model-uris-in-mlflow-3)


MLflow 3 introduces a new model URI format that uses model IDs instead of run IDs, providing more direct model referencing:


python```
# New MLflow 3 model URI formatmodel_uri = f"models:/{model_info.model_id}"loaded_model = mlflow.pyfunc.load_model(model_uri)# This replaces the older run-based URI format:# model_uri = f"runs:/{run_id}/model_path"
```


This new approach provides several advantages:


- **Direct model reference**: No need to know the run ID and artifact path
- **Better model lifecycle management**: Each model checkpoint has its own unique identifier
- **Improved model comparison**: Easily compare different checkpoints within the same run
- **Enhanced traceability**: Clear links between models, metrics, and datasets


## Tracking Datasets[​](#tracking-datasets)


MLflow offers the ability to track datasets that are associated with model training events. These metadata associated with the Dataset can be stored through the use of the [`mlflow.log_input()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_input) API.
To learn more, please visit the [MLflow data documentation](https://mlflow.org/docs/latest/ml/dataset/) to see the features available in this API.


## Explore Runs, Models, and Results[​](#explore-runs-models-and-results)


### Tracking UI[​](#tracking_ui)


The Tracking UI lets you visually explore your experiments, runs, and models, as shown on top of this page.


- Experiment-based run listing and comparison (including run comparison across multiple experiments)
- Searching for runs by parameter or metric value
- Visualizing run metrics
- Downloading run results (artifacts and metadata)


These features are available for models as well, as shown below.


![MLflow UI Experiment view page models tab](https://mlflow.org/docs/latest/assets/images/tracking-models-ui-0f88d40c517e103cdead462aab12781a.png)

A screenshot of the MLflow Tracking UI on the models tab, showing a list of models under the experiment.
If you log runs to a local `mlruns` directory, run the following command in the directory above it,
then access [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.


bash```
mlflow ui --port 5000
```


Alternatively, the [MLflow Tracking Server](#tracking_server) serves the same UI and enables remote
storage of run artifacts. In that case, you can view the UI at `http://<IP address of your MLflow tracking server>:5000`
from any machine that can connect to your tracking server.


## Set up the MLflow Tracking Environment[​](#tracking-setup)


noteIf you just want to log your experiment data and models to local files, you can skip this section.


MLflow Tracking supports many different scenarios for your development workflow. This section will guide you through how to set up the MLflow Tracking environment for your particular use case.
From a bird's-eye view, the MLflow Tracking environment consists of the following components.


### Components[​](#components)


#### [MLflow Tracking APIs](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)[​](#mlflow-tracking-apis)


You can call MLflow Tracking APIs in your ML code to log runs and communicate with the MLflow Tracking Server if necessary.


#### [Backend Store](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/)[​](#backend-store)


The backend store persists various metadata for each [Run](#runs), such as run ID, start and end times, parameters, metrics, etc.
MLflow supports two types of storage for the backend: **file-system-based** like local files and **database-based** like PostgreSQL.


Additionally, if you are interfacing with a managed service (such as Databricks or Azure Machine Learning), you will be interfacing with a
REST-based backend store that is externally managed and not directly accessible.


#### [Artifact Store](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/)[​](#artifact-stores)


Artifact store persists (typically large) artifacts for each run, such as model weights (e.g. a pickled scikit-learn model),
images (e.g. PNGs), model and data files (e.g. [Parquet](https://parquet.apache.org) file). MLflow stores artifacts ina a
local file (`mlruns`) by default, but also supports different storage options such as Amazon S3 and Azure Blob Storage.


For models which are logged as MLflow artifacts, you can refer the model through a model URI of format: `models:/<model_id>`,
where 'model_id' is the unique identifier assigned to the logged model. This replaces the older `runs:/<run_id>/<artifact_path>` format
and provides more direct model referencing.


If the model is registered in the [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/),
you can also refer the the model through a model URI of format: `models:/<model-name>/<model-version>`,
see [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/) for details.


#### [MLflow Tracking Server](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/) (Optional)[​](#tracking_server)


MLflow Tracking Server is a stand-alone HTTP server that provides REST APIs for accessing backend and/or artifact store.
Tracking server also offers flexibility to configure what data to server, govern access control, versioning, and etc. Read
[MLflow Tracking Server documentation](https://mlflow.org/docs/latest/self-hosting/) for more details.


### Common Setups[​](#tracking_setup)


By configuring these components properly, you can create an MLflow Tracking environment suitable for your team's development workflow.
The following diagram and table show a few common setups for the MLflow Tracking environment.


![](https://mlflow.org/docs/latest/assets/images/tracking-setup-overview-3d8cfd511355d9379328d69573763331.png)


1. Localhost (default)2. Local Tracking with Local Database3. Remote Tracking with [MLflow Tracking Server](#tracking_server)ScenarioSolo developmentSolo developmentTeam developmentUse CaseBy default, MLflow records metadata and artifacts for each run to a local directory, `mlruns`. This is the simplest way to get started with MLflow Tracking, without setting up any external server, database, and storage.The MLflow client can interface with a SQLAlchemy-compatible database (e.g., SQLite, PostgreSQL, MySQL) for the [backend](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/). Saving metadata to a database allows you cleaner management of your experiment data while skipping the effort of setting up a server.MLflow Tracking Server can be configured with an artifacts HTTP proxy, passing artifact requests through the tracking server to store and retrieve artifacts without having to interact with underlying object store services. This is particularly useful for team development scenarios where you want to store artifacts and experiment metadata in a shared location with proper access control.Tutorial[QuickStart](https://mlflow.org/docs/latest/ml/tracking/quickstart/)[Tracking Experiments using a Local Database](https://mlflow.org/docs/latest/ml/tracking/tutorials/local-database/)[Remote Experiment Tracking with MLflow Tracking Server](https://mlflow.org/docs/latest/ml/tracking/tutorials/remote-server/)
## Other Configuration with [MLflow Tracking Server](#tracking_server)[​](#other-tracking-setup)


MLflow Tracking Server provides customizability for other special use cases. Please follow
[Remote Experiment Tracking with MLflow Tracking Server](https://mlflow.org/docs/latest/ml/tracking/tutorials/remote-server/) for learning
the basic setup and continue to the following materials for advanced configurations to meet your needs.


- Local Tracking Server
- Artifacts-only Mode
- Direct Access to Artifacts

#### Using MLflow Tracking Server Locally[​](#using-mlflow-tracking-server-locally)

You can of course run MLflow Tracking Server locally. While this doesn't provide much additional benefit over directly using
the local files or database, might useful for testing your team development workflow locally or running your machine learning
code on a container environment.

![](https://mlflow.org/docs/latest/assets/images/tracking-setup-local-server-cd51180e89bfd0a18c52f5b33e0f188d.png)

#### Running MLflow Tracking Server in Artifacts-only Mode[​](#running-mlflow-tracking-server-in-artifacts-only-mode)

MLflow Tracking Server has an `--artifacts-only` option which allows the server to handle (proxy) exclusively artifacts, without permitting
the processing of metadata. This is particularly useful when you are in a large organization or are training extremely large models. In these scenarios, you might have high artifact
transfer volumes and can benefit from splitting out the traffic for serving artifacts to not impact tracking functionality. Please read
[Optionally using a Tracking Server instance exclusively for artifact handling](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/#tracking-server-artifacts-only)
for more details on how to use this mode.

![](https://mlflow.org/docs/latest/assets/images/tracking-setup-artifacts-only-f9630e7e6dc87eab52eea8f85a706382.png)

#### Disable Artifact Proxying to Allow Direct Access to Artifacts[​](#disable-artifact-proxying-to-allow-direct-access-to-artifacts)

MLflow Tracking Server, by default, serves both artifacts and only metadata. However, in some cases, you may want
to allow direct access to the remote artifacts storage to avoid the overhead of a proxy while preserving the functionality
of metadata tracking. This can be done by disabling artifact proxying by starting server with `--no-serve-artifacts` option.
Refer to [Use Tracking Server without Proxying Artifacts Access](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/#tracking-server-no-proxy)
for how to set this up.

![](https://mlflow.org/docs/latest/assets/images/tracking-setup-no-serve-artifacts-9e21c03b857275a42dc667e4454fba37.png)


## FAQ[​](#faq)


### Can I launch multiple runs in parallel?[​](#can-i-launch-multiple-runs-in-parallel)


Yes, MLflow supports launching multiple runs in parallel e.g. multi processing / threading.
See [Launching Multiple Runs in One Program](https://mlflow.org/docs/latest/ml/tracking/tracking-api/#parallel-execution-strategies) for more details.


### How can I organize many MLflow Runs neatly?[​](#how-can-i-organize-many-mlflow-runs-neatly)


MLflow provides a few ways to organize your runs:


- [Organize runs into experiments](https://mlflow.org/docs/latest/ml/tracking/tracking-api/#experiment-organization) - Experiments are logical containers for your runs. You can create an experiment using the CLI, API, or UI.
- [Create child runs](https://mlflow.org/docs/latest/ml/tracking/tracking-api/#hierarchical-runs-with-parent-child-relationships) - You can create child runs under a single parent run to group them together. For example, you can create a child run for each fold in a cross-validation experiment.
- [Add tags to runs](https://mlflow.org/docs/latest/ml/tracking/tracking-api/#smart-tagging-for-organization) - You can associate arbitrary tags with each run, which allows you to filter and search runs based on tags.


### Can I directly access remote storage without running the Tracking Server?[​](#can-i-directly-access-remote-storage-without-running-the-tracking-server)


Yes, while it is best practice to have the MLflow Tracking Server as a proxy for artifacts access for team development workflows, you may not need that
if you are using it for personal projects or testing. You can achieve this by following the workaround below:


1. Set up artifacts configuration such as credentials and endpoints, just like you would for the MLflow Tracking Server.
See [configure artifact storage](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/#artifacts-store-supported-storages) for more details.
2. Create an experiment with an explicit artifact location,


python```
experiment_name = "your_experiment_name"mlflow.create_experiment(experiment_name, artifact_location="s3://your-bucket")mlflow.set_experiment(experiment_name)
```


Your runs under this experiment will log artifacts to the remote storage directly.


#### How to integrate MLflow Tracking with [Model Registry](https://mlflow.org/docs/latest/ml/model-registry/)?[​](#tracking-with-model-registry)


To use the Model Registry functionality with MLflow tracking, you **must use database backed store** such as PostgresQL and log a model using the `log_model` methods of the corresponding model flavors.
Once a model has been logged, you can add, modify, update, or delete the model in the Model Registry through the UI or the API.
See [Backend Stores](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/) and [Common Setups](https://mlflow.org/docs/latest/self-hosting/architecture/overview/#common-setups) for how to configures backend store properly for your workflow.


#### How to include additional description texts about the run?[​](#how-to-include-additional-description-texts-about-the-run)


A system tag `mlflow.note.content` can be used to add descriptive note about this run. While the other [system tags](https://mlflow.org/docs/latest/ml/tracking/tracking-api/#system-tags-reference) are set automatically,
this tag is **not set by default** and users can override it to include additional information about the run. The content will be displayed on the run's page under
the Notes section.

---

## MLflow Tracking APIs | MLflow
<a id="MLflow-Tracking-APIs-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/ml/tracking/tracking-api/

MLflow Tracking provides comprehensive APIs across multiple programming languages to capture your machine learning experiments. Whether you prefer automatic instrumentation or granular control, MLflow adapts to your workflow.

On this page# MLflow Tracking APIs


[MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/) provides comprehensive APIs across multiple programming languages to capture your machine learning experiments. Whether you prefer automatic instrumentation or granular control, MLflow adapts to your workflow.


## Choose Your Approach[​](#choose-your-approach)


MLflow offers two primary methods for experiment tracking, each optimized for different use cases:


### **🤖 Automatic Logging** - Zero Setup, Maximum Coverage[​](#-automatic-logging---zero-setup-maximum-coverage)


Perfect for getting started quickly or when using supported ML libraries. Just add one line and MLflow captures everything automatically.


python```
import mlflowmlflow.autolog()  # That's it!# Your existing training code works unchangedmodel.fit(X_train, y_train)
```


**What gets logged automatically:**


- Model parameters and hyperparameters
- Training and validation metrics
- Model artifacts and checkpoints
- Training plots and visualizations
- Framework-specific metadata


**Supported libraries:** Scikit-learn, XGBoost, LightGBM, PyTorch, Keras/TensorFlow, Spark, and more.


[**→ Explore Auto Logging**](https://mlflow.org/docs/latest/ml/tracking/autolog/)


### **🛠️ Manual Logging** - Complete Control, Custom Workflows[​](#️-manual-logging---complete-control-custom-workflows)


Ideal for custom training loops, advanced experimentation, or when you need precise control over what gets tracked.


- Python
- Java
- R

python```
import mlflowwith mlflow.start_run():    # Log parameters    mlflow.log_param("learning_rate", 0.01)    mlflow.log_param("batch_size", 32)    # Your training logic here    for epoch in range(num_epochs):        train_loss = train_model()        val_loss = validate_model()        # Log metrics with step tracking        mlflow.log_metrics({"train_loss": train_loss, "val_loss": val_loss}, step=epoch)    # Log final model    mlflow.sklearn.log_model(model, name="model")
```

java```
MlflowClient client = new MlflowClient();RunInfo run = client.createRun();// Log parametersclient.logParam(run.getRunId(), "learning_rate", "0.01");client.logParam(run.getRunId(), "batch_size", "32");// Log metrics with timestepsfor (int epoch = 0; epoch < numEpochs; epoch++) {    double trainLoss = trainModel();    client.logMetric(run.getRunId(), "train_loss", trainLoss,                    System.currentTimeMillis(), epoch);}
```

r```
library(mlflow)with(mlflow_start_run(), {  # Log parameters  mlflow_log_param("learning_rate", 0.01)  mlflow_log_param("batch_size", 32)  # Training loop  for (epoch in 1:num_epochs) {    train_loss <- train_model()    mlflow_log_metric("train_loss", train_loss, step = epoch)  }})
```


## Core Logging Functions[​](#core-logging-functions)


### Setup & Configuration[​](#setup--configuration)


FunctionPurposeExample[`mlflow.set_tracking_uri()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_tracking_uri)Connect to tracking server or database`mlflow.set_tracking_uri("http://localhost:5000")`[`mlflow.get_tracking_uri()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.get_tracking_uri)Get current tracking URI`uri = mlflow.get_tracking_uri()`[`mlflow.create_experiment()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.create_experiment)Create new experiment`exp_id = mlflow.create_experiment("my-experiment")`[`mlflow.set_experiment()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_experiment)Set active experiment`mlflow.set_experiment("fraud-detection")`
### Run Management[​](#run-management)


FunctionPurposeExample[`mlflow.start_run()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.start_run)Start new run (with context manager)`with mlflow.start_run(): ...`[`mlflow.end_run()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.end_run)End current run`mlflow.end_run(status="FINISHED")`[`mlflow.active_run()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.active_run)Get currently active run`run = mlflow.active_run()`[`mlflow.last_active_run()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.last_active_run)Get last completed run`last_run = mlflow.last_active_run()`
### Data Logging[​](#data-logging)


FunctionPurposeExample[`mlflow.log_param()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_param) / [`mlflow.log_params()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_params)Log hyperparameters`mlflow.log_param("lr", 0.01)`[`mlflow.log_metric()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_metric) / [`mlflow.log_metrics()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_metrics)Log performance metrics`mlflow.log_metric("accuracy", 0.95, step=10)`[`mlflow.log_input()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_input)Log dataset information`mlflow.log_input(dataset)`[`mlflow.set_tag()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_tag) / [`mlflow.set_tags()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_tags)Add metadata tags`mlflow.set_tag("model_type", "CNN")`
### Artifact Management[​](#artifact-management)


FunctionPurposeExample[`mlflow.log_artifact()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_artifact)Log single file/directory`mlflow.log_artifact("model.pkl")`[`mlflow.log_artifacts()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_artifacts)Log entire directory`mlflow.log_artifacts("./plots/")`[`mlflow.get_artifact_uri()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.get_artifact_uri)Get artifact storage location`uri = mlflow.get_artifact_uri()`
### Model Management (New in MLflow 3)[​](#model-management-new-in-mlflow-3)


FunctionPurposeExample[`mlflow.initialize_logged_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.initialize_logged_model)Initialize a logged model in PENDING state`model = mlflow.initialize_logged_model(name="my_model")`[`mlflow.create_external_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.create_external_model)Create external model (artifacts stored outside MLflow)`model = mlflow.create_external_model(name="agent")`[`mlflow.finalize_logged_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.finalize_logged_model)Update model status to READY or FAILED`mlflow.finalize_logged_model(model_id, "READY")`[`mlflow.get_logged_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.get_logged_model)Retrieve logged model by ID`model = mlflow.get_logged_model(model_id)`[`mlflow.last_logged_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.last_logged_model)Get most recently logged model`model = mlflow.last_logged_model()`[`mlflow.search_logged_models()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.search_logged_models)Search for logged models`models = mlflow.search_logged_models(filter_string="name='my_model'")`[`mlflow.log_model_params()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_model_params)Log parameters to a specific model`mlflow.log_model_params({"param": "value"}, model_id)`[`mlflow.set_logged_model_tags()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_logged_model_tags)Set tags on a logged model`mlflow.set_logged_model_tags(model_id, {"key": "value"})`[`mlflow.delete_logged_model_tag()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.delete_logged_model_tag)Delete tag from a logged model`mlflow.delete_logged_model_tag(model_id, "key")`
### Active Model Management (New in MLflow 3)[​](#active-model-management-new-in-mlflow-3)


FunctionPurposeExample[`mlflow.set_active_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_active_model)Set active model for trace linking`mlflow.set_active_model(name="my_model")`[`mlflow.get_active_model_id()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.get_active_model_id)Get current active model ID`model_id = mlflow.get_active_model_id()`[`mlflow.clear_active_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.clear_active_model)Clear active model`mlflow.clear_active_model()`
### Language-Specific API Coverage[​](#language-specific-api-coverage)


CapabilityPythonJavaRREST API**Basic Logging**✅ Full✅ Full✅ Full✅ Full**Auto Logging**✅ 15+ Libraries❌ Not Available✅ Limited❌ Not Available**Model Logging**✅ 20+ Flavors✅ Basic Support✅ Basic Support✅ Via Artifacts**Logged Model Management**✅ Full (MLflow 3)❌ Not Available❌ Not Available✅ Basic**Dataset Tracking**✅ Full✅ Basic✅ Basic✅ Basic**Search & Query**✅ Advanced✅ Basic✅ Basic✅ Full
api-parityThe Python API provides the most comprehensive feature set. Java and R APIs offer core functionality with ongoing feature additions in each release.


## Advanced Tracking Patterns[​](#advanced-tracking-patterns)


### Working with Logged Models (New in MLflow 3)[​](#working-with-logged-models-new-in-mlflow-3)


MLflow 3 introduces powerful logged model management capabilities for tracking models independently of runs:


#### Creating and Managing External Models[​](#creating-and-managing-external-models)


For models stored outside MLflow (like deployed agents or external model artifacts):


python```
import mlflow# Create an external model for tracking without storing artifacts in MLflowmodel = mlflow.create_external_model(    name="chatbot_agent",    model_type="agent",    tags={"version": "v1.0", "environment": "production"},)# Log parameters specific to this modelmlflow.log_model_params(    {"temperature": "0.7", "max_tokens": "1000"}, model_id=model.model_id)# Set as active model for automatic trace linkingmlflow.set_active_model(model_id=model.model_id)@mlflow.tracedef chat_with_agent(message):    # This trace will be automatically linked to the active model    return agent.chat(message)# Traces are now linked to your external modeltraces = mlflow.search_traces(model_id=model.model_id)
```


#### Advanced Model Lifecycle Management[​](#advanced-model-lifecycle-management)


For models that require custom preparation or validation:


python```
import mlflowfrom mlflow.entities import LoggedModelStatus# Initialize model in PENDING statemodel = mlflow.initialize_logged_model(    name="custom_neural_network",    model_type="neural_network",    tags={"architecture": "transformer", "dataset": "custom"},)try:    # Custom model preparation logic    train_model()    validate_model()    # Save model artifacts using standard MLflow model logging    mlflow.pytorch.log_model(        pytorch_model=model_instance,        name="model",        model_id=model.model_id,  # Link to the logged model    )    # Finalize model as READY    mlflow.finalize_logged_model(model.model_id, LoggedModelStatus.READY)except Exception as e:    # Mark model as FAILED if issues occur    mlflow.finalize_logged_model(model.model_id, LoggedModelStatus.FAILED)    raise# Retrieve and work with the logged modelfinal_model = mlflow.get_logged_model(model.model_id)print(f"Model {final_model.name} is {final_model.status}")
```


#### Searching and Querying Logged Models[​](#searching-and-querying-logged-models)


python```
# Find all production-ready transformer modelsproduction_models = mlflow.search_logged_models(    filter_string="tags.environment = 'production' AND model_type = 'transformer'",    order_by=[{"field_name": "creation_time", "ascending": False}],    output_format="pandas",)# Search for models with specific performance metricshigh_accuracy_models = mlflow.search_logged_models(    filter_string="metrics.accuracy > 0.95",    datasets=[{"dataset_name": "test_set"}],  # Only consider test set metrics    max_results=10,)# Get the most recently logged model in current sessionlatest_model = mlflow.last_logged_model()if latest_model:    print(f"Latest model: {latest_model.name} (ID: {latest_model.model_id})")
```


### Precise Metric Tracking[​](#precise-metric-tracking)


Control exactly when and how metrics are recorded with custom timestamps and steps:


python```
import timefrom datetime import datetime# Log with custom step (training iteration/epoch)for epoch in range(100):    loss = train_epoch()    mlflow.log_metric("train_loss", loss, step=epoch)# Log with custom timestampnow = int(time.time() * 1000)  # MLflow expects millisecondsmlflow.log_metric("inference_latency", latency, timestamp=now)# Log with both step and timestampmlflow.log_metric("gpu_utilization", gpu_usage, step=epoch, timestamp=now)
```


**Step Requirements:**


- Must be a valid 64-bit integer
- Can be negative or out of order
- Supports gaps in sequences (e.g., 1, 5, 75, -20)


### Experiment Organization[​](#experiment-organization)


Structure your experiments for easy comparison and analysis:


python```
# Method 1: Environment variablesimport osos.environ["MLFLOW_EXPERIMENT_NAME"] = "fraud-detection-v2"# Method 2: Explicit experiment settingmlflow.set_experiment("hyperparameter-tuning")# Method 3: Create with custom configurationexperiment_id = mlflow.create_experiment(    "production-models",    artifact_location="s3://my-bucket/experiments/",    tags={"team": "data-science", "environment": "prod"},)
```


### Hierarchical Runs with Parent-Child Relationships[​](#hierarchical-runs-with-parent-child-relationships)


Organize complex experiments like hyperparameter sweeps or cross-validation:


python```
# Parent run for the entire experimentwith mlflow.start_run(run_name="hyperparameter_sweep") as parent_run:    mlflow.log_param("search_strategy", "random")    best_score = 0    best_params = {}    # Child runs for each parameter combination    for lr in [0.001, 0.01, 0.1]:        for batch_size in [16, 32, 64]:            with mlflow.start_run(                nested=True, run_name=f"lr_{lr}_bs_{batch_size}"            ) as child_run:                mlflow.log_params({"learning_rate": lr, "batch_size": batch_size})                # Train and evaluate                model = train_model(lr, batch_size)                score = evaluate_model(model)                mlflow.log_metric("accuracy", score)                # Track best configuration in parent                if score > best_score:                    best_score = score                    best_params = {"learning_rate": lr, "batch_size": batch_size}    # Log best results to parent run    mlflow.log_params(best_params)    mlflow.log_metric("best_accuracy", best_score)# Query child runschild_runs = mlflow.search_runs(    filter_string=f"tags.mlflow.parentRunId = '{parent_run.info.run_id}'")print("Child run results:")print(child_runs[["run_id", "params.learning_rate", "metrics.accuracy"]])
```


### Parallel Execution Strategies[​](#parallel-execution-strategies)


Handle multiple runs efficiently with different parallelization approaches:


- Sequential Runs
- Multiprocessing
- Multithreading

Perfect for simple hyperparameter sweeps or A/B testing:

python```
configs = [    {"model": "RandomForest", "n_estimators": 100},    {"model": "XGBoost", "max_depth": 6},    {"model": "LogisticRegression", "C": 1.0},]for config in configs:    with mlflow.start_run(run_name=config["model"]):        mlflow.log_params(config)        model = train_model(config)        score = evaluate_model(model)        mlflow.log_metric("f1_score", score)
```

Scale training across multiple CPU cores:

python```
import multiprocessing as mpdef train_with_config(config):    # Set tracking URI in each process (required for spawn method)    mlflow.set_tracking_uri("http://localhost:5000")    mlflow.set_experiment("parallel-training")    with mlflow.start_run():        mlflow.log_params(config)        model = train_model(config)        score = evaluate_model(model)        mlflow.log_metric("accuracy", score)        return scoreif __name__ == "__main__":    configs = [{"lr": lr, "bs": bs} for lr in [0.01, 0.1] for bs in [16, 32]]    with mp.Pool(processes=4) as pool:        results = pool.map(train_with_config, configs)    print(f"Completed {len(results)} experiments")
```

Use child runs for thread-safe parallel execution:

python```
import threadingfrom concurrent.futures import ThreadPoolExecutordef train_worker(config):    with mlflow.start_run(nested=True):        mlflow.log_params(config)        model = train_model(config)        score = evaluate_model(model)        mlflow.log_metric("accuracy", score)        return score# Start parent runwith mlflow.start_run(run_name="threaded_experiment"):    configs = [{"lr": 0.01, "epochs": e} for e in range(10, 101, 10)]    with ThreadPoolExecutor(max_workers=4) as executor:        futures = [executor.submit(train_worker, config) for config in configs]        results = [future.result() for future in futures]    # Log summary to parent run    mlflow.log_metric("avg_accuracy", sum(results) / len(results))    mlflow.log_metric("max_accuracy", max(results))
```


### Smart Tagging for Organization[​](#smart-tagging-for-organization)


Use tags strategically to organize and filter experiments:


python```
with mlflow.start_run():    # Descriptive tags for filtering    mlflow.set_tags(        {            "model_family": "transformer",            "dataset_version": "v2.1",            "environment": "production",            "team": "nlp-research",            "gpu_type": "V100",            "experiment_phase": "hyperparameter_tuning",        }    )    # Special notes tag for documentation    mlflow.set_tag(        "mlflow.note.content",        "Baseline transformer model with attention dropout. "        "Testing different learning rate schedules.",    )    # Training code here...
```


**Search experiments by tags:**


python```
# Find all transformer experimentstransformer_runs = mlflow.search_runs(filter_string="tags.model_family = 'transformer'")# Find production-ready modelsprod_models = mlflow.search_runs(    filter_string="tags.environment = 'production' AND metrics.accuracy > 0.95")
```


### System Tags Reference[​](#system-tags-reference)


MLflow automatically sets several system tags to capture execution context:


TagDescriptionWhen Set`mlflow.source.name`Source file or notebook nameAlways`mlflow.source.type`Source type (NOTEBOOK, JOB, LOCAL, etc.)Always`mlflow.user`User who created the runAlways`mlflow.source.git.commit`Git commit hashWhen run from git repo`mlflow.source.git.branch`Git branch nameMLflow Projects only`mlflow.parentRunId`Parent run ID for nested runsChild runs only`mlflow.docker.image.name`Docker image usedDocker environments`mlflow.note.content`**User-editable** descriptionManual only
pro-tipUse `mlflow.note.content` to document experiment insights, hypotheses, or results directly in the MLflow UI. This tag appears in a dedicated Notes section on the run page.


### Integration with Auto Logging[​](#integration-with-auto-logging)


Combine auto logging with manual tracking for the best of both worlds:


python```
import mlflowfrom sklearn.ensemble import RandomForestClassifierfrom sklearn.metrics import classification_report# Enable auto loggingmlflow.autolog()with mlflow.start_run():    # Auto logging captures model training automatically    model = RandomForestClassifier(n_estimators=100)    model.fit(X_train, y_train)    # Add custom metrics and artifacts    predictions = model.predict(X_test)    # Log custom evaluation metrics    report = classification_report(y_test, predictions, output_dict=True)    mlflow.log_metrics(        {            "precision_macro": report["macro avg"]["precision"],            "recall_macro": report["macro avg"]["recall"],            "f1_macro": report["macro avg"]["f1-score"],        }    )    # Log custom artifacts    feature_importance = pd.DataFrame(        {"feature": feature_names, "importance": model.feature_importances_}    )    feature_importance.to_csv("feature_importance.csv")    mlflow.log_artifact("feature_importance.csv")    # Access the auto-logged run for additional processing    current_run = mlflow.active_run()    print(f"Auto-logged run ID: {current_run.info.run_id}")# Access the completed runlast_run = mlflow.last_active_run()print(f"Final run status: {last_run.info.status}")
```


## Language-Specific Guides[​](#language-specific-guides)


- **Python**: [Complete Python API Reference](https://mlflow.org/docs/latest/api_reference/python_api/index.html)
- **Java**: [Java API Documentation](https://mlflow.org/docs/latest/api_reference/java_api/index.html)
- **R**: [R API Documentation](https://mlflow.org/docs/latest/api_reference/R-api.html)
- **REST**: [REST API Reference](https://mlflow.org/docs/latest/api_reference/rest-api.html)



**Next Steps:**


- [Set up MLflow Tracking Server](https://mlflow.org/docs/latest/self-hosting/) for team collaboration
- [Explore Auto Logging](https://mlflow.org/docs/latest/ml/tracking/autolog/) for supported frameworks
- [Learn advanced search patterns](https://mlflow.org/docs/latest/ml/search/search-runs/) for experiment analysis

---

## Backend Stores | MLflow
<a id="Backend-Stores-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/

The backend store is a core component in MLflow that stores metadata for

On this page# Backend Stores


The backend store is a core component in MLflow that stores metadata for
Runs, models, traces, and experiments such as:


- Run ID
- Model ID
- Trace ID
- Tags
- Start & end time
- Parameters
- Metrics


Large model artifacts such as model weight files are stored in the [artifact store](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/).


## Types of Backend Stores[​](#types-of-backend-stores)


### Relational Database (**Recommended**)[​](#relational-database-recommended)


MLflow supports different databases through SQLAlchemy, including `sqlite`, `postgresql`, `mysql`, and `mssql`. This option provides better performance through indexing and is easier to scale to larger volumes of data than the file system backend..


SQLite is the easiest way to use to database backend. To use it, simply add `--backend-store-uri sqlite:///my.db` when starting MLflow. A database file will be created for you and it will be used to store your tracking data.


### Local File System (**Deprecated Soon**)[​](#local-file-system-deprecated-soon)


By default, MLflow stores metadata in local files in the `./mlruns` directory. This is for the pure sake of simplicity.
For better performance and reliability, we always recommend using a database backend.


TO BE DEPRECATED SOONFile system backend is in Keep-the-Light-On (KTLO) mode and will not receive most of the new features in MLflow.
We recommend using the database backend instead. Database backend will also be the default option soon.


## Configure Backend Store[​](#configure-backend-store)


By default, MLflow stores metadata in local files in the `./mlruns` directory, but MLflow can store metadata to databases as well.
You can configure the location by passing the desired **tracking URI** to MLflow, via either of the following methods:


- Set the `MLFLOW_TRACKING_URI` environment variable.
- Call [`mlflow.set_tracking_uri()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_tracking_uri) in your code.
- If you are running a [Tracking Server](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/), you can set the `tracking_uri` option when starting the server, like `mlflow server --backend-store-uri sqlite:///mydb.sqlite`


Continue to the next section for the supported format of tracking URLs.
Also visit [this guidance](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/) for how to set up the backend store properly for your workflow.


importantThe default file backend works fine for small use cases where you only want to log less than 1000 runs, metrics, and traces. Otherwise, we **highly recommend using a database backend** for better performance and reliability.


## Supported Store Types[​](#supported-store-types)


MLflow supports the following types of tracking URI for backend stores:


- Local file path (specified as `file:/my/local/dir`), where data is just directly stored locally to a system disk where your code is executing.
- A Database, encoded as `<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>`. MLflow supports the dialects `mysql`, `mssql`, `sqlite`, and `postgresql`. For more details, see [SQLAlchemy database uri](https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls).
- HTTP server (specified as `https://my-server:5000`), which is a server hosting an [MLflow tracking server](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/).
- Databricks workspace (specified as `databricks` or as `databricks://<profileName>`, a [Databricks CLI profile](https://github.com/databricks/databricks-cli#installation)).
Refer to Access the MLflow tracking server from outside Databricks [[AWS]](http://docs.databricks.com/applications/mlflow/access-hosted-tracking-server.html)
[[Azure]](http://docs.microsoft.com/azure/databricks/applications/mlflow/access-hosted-tracking-server).


database-requirements**Database-Backed Store Requirements**

When using database-backed stores, please note:

- **Model Registry Integration**: [Model Registry](https://mlflow.org/docs/latest/ml/model-registry/) functionality requires a database-backed store. See [this FAQ](https://mlflow.org/docs/latest/ml/tracking/#tracking-with-model-registry) for more information.
- **Schema Migrations**: `mlflow server` will fail against a database with an out-of-date schema. Always run `mlflow db upgrade [db_uri]` to upgrade your database schema before starting the server. Schema migrations can result in database downtime and may take longer on larger databases. **Always backup your database before running migrations.**


parameter-limitsIn Sep 2023, we increased the max length for params recorded in a Run from 500 to 8k (but we limit param value max length to 6000 internally).
[mlflow/2d6e25af4d3e_increase_max_param_val_length](https://github.com/mlflow/mlflow/blob/master/mlflow/store/db_migrations/versions/2d6e25af4d3e_increase_max_param_val_length.py)
is a non-invertible migration script that increases the cap in existing database to 8k. Please be careful if you want to upgrade and backup your database before upgrading.


## Deletion Behavior[​](#deletion-behavior)


In order to allow MLflow Runs to be restored, Run metadata and artifacts are not automatically removed
from the backend store or artifact store when a Run is deleted. The [mlflow gc](https://mlflow.org/docs/latest/api_reference/cli.html#mlflow-gc) CLI is provided
for permanently removing Run metadata and artifacts for deleted runs.


## SQLAlchemy Options[​](#sqlalchemy-options)


You can inject some [SQLAlchemy connection pooling options](https://docs.sqlalchemy.org/en/latest/core/pooling.html) using environment variables.


MLflow Environment VariableSQLAlchemy QueuePool Option`MLFLOW_SQLALCHEMYSTORE_POOL_SIZE``pool_size``MLFLOW_SQLALCHEMYSTORE_POOL_RECYCLE``pool_recycle``MLFLOW_SQLALCHEMYSTORE_MAX_OVERFLOW``max_overflow`
## MySQL SSL Options[​](#mysql-ssl-options)


When connecting to a MySQL database that requires SSL certificates, you can set the following environment variables:


bash```
# Path to SSL CA certificate fileexport MLFLOW_MYSQL_SSL_CA=/path/to/ca.pem# Path to SSL client certificate file (if needed)export MLFLOW_MYSQL_SSL_CERT=/path/to/client-cert.pem# Path to SSL client key file (if needed)export MLFLOW_MYSQL_SSL_KEY=/path/to/client-key.pem
```


Then start the MLflow server with your MySQL URI:


bash```
mlflow server --backend-store-uri="mysql+pymysql://username@hostname:port/database" --default-artifact-root=s3://your-bucket --host=0.0.0.0 --port=5000
```


These environment variables will be used to configure the SSL connection to the MySQL server.


## File Store Performance[​](#file-store-performance)


MLflow will automatically try to use [LibYAML](https://pyyaml.org/wiki/LibYAML) bindings if they are already installed.
However, if you notice any performance issues when using *file store* backend, it could mean LibYAML is not installed on your system.
On Linux or Mac you can easily install it using your system package manager:


bash```
# On Ubuntu/Debianapt-get install libyaml-cpp-dev libyaml-dev# On macOS using Homebrewbrew install yaml-cpp libyaml
```


After installing LibYAML, you need to reinstall PyYAML:


bash```
# Reinstall PyYAMLpip --no-cache-dir install --force-reinstall -I pyyaml
```


noteWe generally recommend using a database backend to get better performance.

---

## Artifact Stores | MLflow
<a id="Artifact-Stores-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/

The artifact store is a core component in MLflow Tracking where MLflow stores (typically large) artifacts

On this page# Artifact Stores


The artifact store is a core component in [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/) where MLflow stores (typically large) artifacts
for each run such as model weights (e.g. a pickled scikit-learn model), images (e.g. PNGs), model and data files (e.g. [Parquet](https://parquet.apache.org/) file).
Note that metadata like parameters, metrics, and tags are stored in a [backend store](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/) (e.g., PostGres, MySQL, or MSSQL Database), the other component of the MLflow Tracking.


## Configuring an Artifact Store[​](#configuring-an-artifact-store)


MLflow by default stores artifacts in a local (file system) `./mlruns` directory, but also supports various locations suitable for large data:
Amazon S3, Azure Blob Storage, Google Cloud Storage, SFTP server, and NFS. You can connect those remote storages via the MLflow Tracking server.
See [tracking server setup](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/#tracking-server-artifact-store) and the specific section for your storage in [supported storages](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/#artifacts-store-supported-storages) for guidance on
how to connect to the remote storage of your choice.


### Managing Artifact Store Access[​](#artifacts-stores-manage-access)


To allow the server and clients to access the artifact location, you should configure your cloud
provider credentials as you would for accessing them in any other capacity. For example, for S3, you can set the `AWS_ACCESS_KEY_ID`
and `AWS_SECRET_ACCESS_KEY` environment variables, use an IAM role, or configure a default
profile in `~/.aws/credentials`.


importantAccess of credentials and configurations for the artifact storage location are configured **once during the tracking server initialization** instead
of having to provide access credentials for artifact-based operations through the client APIs. Note that **all users who have access to the
Tracking Server in this mode will have access to artifacts served through this assumed role**.


### Setting an access Timeout[​](#setting-an-access-timeout)


You can set the environment variable `MLFLOW_ARTIFACT_UPLOAD_DOWNLOAD_TIMEOUT` (in seconds) to configure the timeout for artifact uploads and downloads.
If it's not set, MLflow will use the default timeout for the underlying storage client library (e.g. boto3 for S3).
Note that this is an experimental feature and it may be modified as needed.


### Setting a Default Artifact Location for Logging[​](#setting-a-default-artifact-location-for-logging)


MLflow automatically records the `artifact_uri` property as a part of [`mlflow.entities.RunInfo`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.entities.html#mlflow.entities.RunInfo) so that you can
retrieve the location of the artifacts for historical runs using the [`mlflow.get_artifact_uri()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.get_artifact_uri) API.
Also, `artifact_location` is a property recorded on [`mlflow.entities.Experiment`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.entities.html#mlflow.entities.Experiment) for setting the
default location to store artifacts for all runs for models within a given experiment.


importantIf you do not specify a `--default-artifact-root` or an artifact URI when creating the experiment
(for example, `mlflow experiments create --artifact-location s3://<my-bucket>`), the artifact root
will be set as a path inside the local file store (the hard drive of the computer executing your run). Typically this is not an appropriate location, as the client and
server probably refer to different physical locations (that is, the same path on different disks or computers).


## Supported storage types for the Artifact Store[​](#artifacts-store-supported-storages)


### Amazon S3 and S3-compatible storage[​](#amazon-s3-and-s3-compatible-storage)


To store artifacts in S3 (whether on Amazon S3 or on an S3-compatible alternative, such as
[MinIO](https://min.io/) or [Digital Ocean Spaces](https://www.digitalocean.com/products/spaces), specify a URI of the form `s3://<bucket>/<path>`. MLflow obtains
credentials to access S3 from your machine's IAM role, a profile in `~/.aws/credentials`, or
the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` depending on which of
these are available. For more information on how to set credentials, see
[Set up AWS Credentials and Region for Development](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/setup-credentials.html).


Followings are commonly used environment variables for configuring S3 storage access. The complete list of configurable parameters for an S3 client is available in the
[boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#configuration).


#### Passing Extra Arguments to S3 Upload[​](#passing-extra-arguments-to-s3-upload)


To add S3 file upload extra arguments, set `MLFLOW_S3_UPLOAD_EXTRA_ARGS` to a JSON object of key/value pairs.
For example, if you want to upload to a KMS Encrypted bucket using the KMS Key 1234:


bash```
export MLFLOW_S3_UPLOAD_EXTRA_ARGS='{"ServerSideEncryption": "aws:kms", "SSEKMSKeyId": "1234"}'
```


For a list of available extra args see [Boto3 ExtraArgs Documentation](https://github.com/boto/boto3/blob/develop/docs/source/guide/s3-uploading-files.rst#the-extraargs-parameter).


#### Setting Custom S3 Endpoints[​](#setting-custom-s3-endpoints)


To store artifacts in a custom endpoint, set the `MLFLOW_S3_ENDPOINT_URL` to your endpoint's URL. For example, if you are using Digital Ocean Spaces:


bash```
export MLFLOW_S3_ENDPOINT_URL=https://<region>.digitaloceanspaces.com
```


If you have a MinIO server at 1.2.3.4 on port 9000:


bash```
export MLFLOW_S3_ENDPOINT_URL=http://1.2.3.4:9000
```


#### Using Non-TLS Authentication[​](#using-non-tls-authentication)


If the MinIO server is configured with using SSL self-signed or signed using some internal-only CA certificate, you could set `MLFLOW_S3_IGNORE_TLS` or `AWS_CA_BUNDLE` variables (not both at the same time!) to disable certificate signature check, or add a custom CA bundle to perform this check, respectively:


bash```
export MLFLOW_S3_IGNORE_TLS=true#orexport AWS_CA_BUNDLE=/some/ca/bundle.pem
```


#### Setting Bucket Region[​](#setting-bucket-region)


Additionally, if MinIO server is configured with non-default region, you should set `AWS_DEFAULT_REGION` variable:


bash```
export AWS_DEFAULT_REGION=my_region
```


warningThe MLflow tracking server utilizes specific reserved keywords to generate a qualified path. These environment configurations, if present in the client environment, can create path resolution issues.
For example, providing `--default-artifact-root $MLFLOW_S3_ENDPOINT_URL` on the server side **and** `MLFLOW_S3_ENDPOINT_URL` on the client side will create a client path resolution issue for the artifact storage location.
Upon resolving the artifact storage location, the MLflow client will use the value provided by `--default-artifact-root` and suffixes the location with the values provided in the environment variable `MLFLOW_S3_ENDPOINT_URL`.
Depending on the value set for the environment variable `MLFLOW_S3_ENDPOINT_URL`, the resulting artifact storage path for this scenario would be one of the following invalid object store paths: `https://<bucketname>.s3.<region>.amazonaws.com/<key>/<bucketname>/<key>` or `s3://<bucketname>/<key>/<bucketname>/<key>`.
To prevent path parsing issues, **ensure that reserved environment variables are removed (`unset`) from client environments**.


### Azure Blob Storage[​](#azure-blob-storage)


To store artifacts in Azure Blob Storage, specify a URI of the form
`wasbs://<container>@<storage-account>.blob.core.windows.net/<path>`.
MLflow expects that your Azure Storage access credentials are located in the
`AZURE_STORAGE_CONNECTION_STRING` and `AZURE_STORAGE_ACCESS_KEY` environment variables
or having your credentials configured such that the [DefaultAzureCredential()](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python) class can pick them up.
The order of precedence is:


1. `AZURE_STORAGE_CONNECTION_STRING`
2. `AZURE_STORAGE_ACCESS_KEY`
3. `DefaultAzureCredential()`


You must set one of these options on **both your client application and your MLflow tracking server**.
Also, you must run `pip install azure-storage-blob` separately (on both your client and the server) to access Azure Blob Storage.
Finally, if you want to use DefaultAzureCredential, you must `pip install azure-identity`;
MLflow does not declare a dependency on these packages by default.


You may set an MLflow environment variable to configure the timeout for artifact uploads and downloads:


- `MLFLOW_ARTIFACT_UPLOAD_DOWNLOAD_TIMEOUT` - (Experimental, may be changed or removed) Sets the timeout for artifact upload/download in seconds (Default: 600 for Azure blob).


### Google Cloud Storage[​](#google-cloud-storage)


To store artifacts in Google Cloud Storage, specify a URI of the form `gs://<bucket>/<path>`.
You should configure credentials for accessing the GCS container on the client and server as described
in the [GCS documentation](https://google-cloud.readthedocs.io/en/latest/core/auth.html).
Finally, you must run `pip install google-cloud-storage` (on both your client and the server)
to access Google Cloud Storage; MLflow does not declare a dependency on this package by default.


You may set some MLflow environment variables to troubleshoot GCS read-timeouts (eg. due to slow transfer speeds) using the following variables:


- `MLFLOW_ARTIFACT_UPLOAD_DOWNLOAD_TIMEOUT` - (Experimental, may be changed or removed) Sets the standard timeout for transfer operations in seconds (Default: 60 for GCS). Use -1 for indefinite timeout.
- `MLFLOW_GCS_UPLOAD_CHUNK_SIZE` - Sets the standard upload chunk size for bigger files in bytes (Default: 104857600 ≙ 100MiB), must be multiple of 256 KB.
- `MLFLOW_GCS_DOWNLOAD_CHUNK_SIZE` - Sets the standard download chunk size for bigger files in bytes (Default: 104857600 ≙ 100MiB), must be multiple of 256 KB


### FTP server[​](#ftp-server)


To store artifacts in a FTP server, specify a URI of the form ftp://user@host/path/to/directory .
The URI may optionally include a password for logging into the server, e.g. `ftp://user:pass@host/path/to/directory`


### SFTP Server[​](#sftp-server)


To store artifacts in an SFTP server, specify a URI of the form `sftp://user@host/path/to/directory`.
You should configure the client to be able to log in to the SFTP server without a password over SSH (e.g. public key, identity file in ssh_config, etc.).


The format `sftp://user:pass@host/` is supported for logging in. However, for safety reasons this is not recommended.


When using this store, `pysftp` must be installed on both the server and the client. Run `pip install pysftp` to install the required package.


### NFS[​](#nfs)


To store artifacts in an NFS mount, specify a URI as a normal file system path, e.g., `/mnt/nfs`.
This path must be the same on both the server and the client -- you may need to use symlinks or remount
the client in order to enforce this property.


### HDFS[​](#hdfs)


To store artifacts in HDFS, specify a `hdfs:` URI. It can contain host and port: `hdfs://<host>:<port>/<path>` or just the path: `hdfs://<path>`.


There are also two ways to authenticate to HDFS:


- Use current UNIX account authorization
- Kerberos credentials using the following environment variables:


bash```
export MLFLOW_KERBEROS_TICKET_CACHE=/tmp/krb5cc_22222222export MLFLOW_KERBEROS_USER=user_name_to_use
```


The HDFS artifact store is accessed using the `pyarrow.fs` module, refer to the
[PyArrow Documentation](https://arrow.apache.org/docs/python/filesystems.html#filesystem-hdfs) for configuration and environment variables needed.


## Deletion Behavior[​](#deletion-behavior)


In order to allow MLflow Runs to be restored, Run metadata and artifacts are not automatically removed
from the backend store or artifact store when a Run is deleted. The [mlflow gc](https://mlflow.org/docs/latest/api_reference/cli.html#mlflow-gc) CLI is provided
for permanently removing Run metadata and artifacts for deleted runs.


## Multipart upload for proxied artifact access[​](#multipart-upload-for-proxied-artifact-access)


The Tracking Server supports uploading large artifacts using multipart upload for proxied artifact access.
To enable this feature, set `MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD` to `true`.


bash```
export MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD=true
```


Under the hood, the Tracking Server will create a multipart upload request with the underlying storage,
generate presigned urls for each part, and let the client upload the parts directly to the storage.
Once all parts are uploaded, the Tracking Server will complete the multipart upload.
None of the data will pass through the Tracking Server.


If the underlying storage does not support multipart upload, the Tracking Server will fallback to a single part upload.
If multipart upload is supported but fails for any reason, an exception will be thrown.


MLflow supports multipart upload for the following storage for proxied artifact access:


- Amazon S3
- Google Cloud Storage


You can configure the following environment variables:


- `MLFLOW_MULTIPART_UPLOAD_MINIMUM_FILE_SIZE` - Specifies the minimum file size in bytes to use multipart upload
when logging artifacts (Default: 500 MB)
- `MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE` - Specifies the chunk size in bytes to use when performing multipart upload
(Default: 100 MB)

---

## MLflow Tracking Server | MLflow
<a id="MLflow-Tracking-Server-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/

MLflow tracking server is a stand-alone HTTP server that serves multiple REST API endpoints for tracking runs/experiments.

On this page# MLflow Tracking Server


MLflow tracking server is a stand-alone HTTP server that serves multiple REST API endpoints for tracking runs/experiments.
While MLflow Tracking can be used in local environment, hosting a tracking server is powerful in the team development
workflow:


- **Collaboration**: Multiple users can log runs to the same endpoint, and query runs and models logged by other users.
- **Sharing Results**: The tracking server also serves [Tracking UI](https://mlflow.org/docs/latest/ml/tracking/#tracking_ui) endpoint, where team members can easily explore each other's results.
- **Centralized Access**: The tracking server can be run as a proxy for the remote access for metadata and artifacts, making it easier to secure and audit access to data.


## Start the Tracking Server[​](#start-the-tracking-server)


Starting the tracking server is as simple as running the following command:


bash```
mlflow server --host 127.0.0.1 --port 8080 --backend-store-uri sqlite:///mlflow.db
```


Once the server starts running, you should see the following output:


text```
INFO:     Started server process [28550]INFO:     Waiting for application startup.INFO:     Application startup complete.INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```


There are many options to configure the server, refer to [Configure Server](#configure-server) for more details.


infoThe `--backend-store-uri` option is not mandatory, but highly recommended. MLflow uses a local filesystem for storing the metadata by default. The above option overrides this to uses a database backend, which provides much better performance and reliability in general. The file backend is in Keep-the-Light-On (KTLO) mode and will not receive most of the new features in MLflow. For different database type such as PostgreSQL, check out [Backend Store](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/).


importantThe server listens on [http://localhost:5000](http://localhost:5000) by default and only accepts
connections from the local machine. To let the server accept connections
from other machines, you will need to pass `--host 0.0.0.0` to listen on
all network interfaces (or a specific interface address). This is typically
required configuration when running the server **in a Kubernetes pod or a
Docker container**.

MLflow 3.5.0+ includes built-in security middleware to protect against DNS rebinding
and CORS attacks. When using `--host 0.0.0.0`, configure the `--allowed-hosts` option
to specify which domains can access your server. See [Security Configuration](https://mlflow.org/docs/latest/self-hosting/security/network/)
for details.


## Logging to a Tracking Server[​](#logging_to_a_tracking_server)


Once the tracking server is started, connect your local clients by setting the `MLFLOW_TRACKING_URI` environment variable to the
server's URI, along with its scheme and port (for example, `http://10.0.0.1:5000`) or call [`mlflow.set_tracking_uri()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_tracking_uri).


MLflow APIs like [`mlflow.start_run()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.start_run), [`mlflow.log_param()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.log_param), [`mlflow.start_trace()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.start_trace) make API requests to your remote tracking server and log the data.


- Python
- TypeScript
- R
- Scala

python```
import mlflowremote_server_uri = "..."  # set to your server URI, e.g. http://127.0.0.1:8080mlflow.set_tracking_uri(remote_server_uri)mlflow.set_experiment("/my-experiment")# Logging a runwith mlflow.start_run():    mlflow.log_param("a", 1)    mlflow.log_metric("b", 2)# Logging a tracewith mlflow.start_span(name="test_trace") as span:    span.set_inputs({"x": 1, "y": 2})    span.set_outputs(3)
```

typescript```
import * as mlflow from "mlflow-tracing";mlflow.init({    trackingUri: "<your-tracking-server-uri>",    experimentId: "<your-experiment-id>",});const myFunc = mlflow.trace(    (a: number, b: number) => {        return a + b;    },    { name: 'my-func' })myFunc(1, 2);
```

r```
library(mlflow)install_mlflow()remote_server_uri = "..." # set to your server URImlflow_set_tracking_uri(remote_server_uri)mlflow_set_experiment("/my-experiment")mlflow_log_param("a", "1")
```

scala```
import org.mlflow.tracking.MlflowClientval remoteServerUri = "..." // set to your server URIval client = new MlflowClient(remoteServerUri)val experimentId = client.createExperiment("my-experiment")client.setExperiment(experimentId)val run = client.createRun(experimentId)client.logParam(run.getRunId(), "a", "1")
```


## Configure Server[​](#configure-server)


This section describes how to configure the tracking server for some common use cases. The section requires you to have a basic knowledge about the tracking server architecture, please visit [Architecture Overview](https://mlflow.org/docs/latest/self-hosting/architecture/overview/) if you are not familiar with it yet.


### Backend Store[​](#backend-store)


By default, the tracking server logs runs metadata to the local filesystem under `./mlruns` directory.
You can configure the different backend store by adding `--backend-store-uri` option:


Examplebash```
# Default: local file systemmlflow server# SQLite: create a SQLite database `my.db` in the current directorymlflow server --backend-store-uri sqlite:///my.db# PostgreSQL: connect to an existing PostgreSQL databasemlflow server --backend-store-uri postgresql://username:password@host:port/database
```


We **recommend using a database backend** in general, because it provides better performance and reliability than the default file backend.


### Remote artifacts store[​](#tracking-server-artifact-store)


#### Using the Tracking Server for proxied artifact access[​](#using-the-tracking-server-for-proxied-artifact-access)


By default, the tracking server stores artifacts in its local filesystem under `./mlartifacts` directory. To configure
the tracking server to connect to remote storage and serve artifacts, start the server with `--artifacts-destination` flag.


bash```
mlflow server \    --host 0.0.0.0 \    --port 8885 \    --artifacts-destination s3://my-bucket
```


With this setting, MLflow server works as a proxy for accessing remote artifacts. The MLflow clients make HTTP request to the server for fetching artifacts.


importantIf you are using remote storage, you have to configure the credentials for the server to access the artifacts. Be aware of that The MLflow artifact proxied
access service enables users to have an *assumed role of access to all artifacts* that are accessible to the Tracking Server. Refer [Manage Access](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/#artifacts-stores-manage-access) for further details.


The tracking server resolves the uri `mlflow-artifacts:/` in tracking request from the client to an otherwise
explicit object store destination (e.g., "s3:/my_bucket/mlartifacts") for interfacing with artifacts. The following patterns will all resolve to the configured proxied object store location (in above example, `s3://my-root-bucket/mlartifacts`):


- `https://<host>:<port>/mlartifacts`
- `http://<host>/mlartifacts`
- `mlflow-artifacts://<host>/mlartifacts`
- `mlflow-artifacts://<host>:<port>/mlartifacts`
- `mlflow-artifacts:/mlartifacts`


importantThe MLflow client caches artifact location information on a per-run basis.
It is therefore not recommended to alter a run's artifact location before it has terminated.


#### Use tracking server w/o proxying artifacts access[​](#tracking-server-no-proxy)


In some cases, you may want to directly access remote storage without proxying through the tracking server.
In this case, you can start the server with `--no-serve-artifacts` flag, and setting `--default-artifact-root` to the remote storage URI
you want to redirect the request to.


bash```
mlflow server --no-serve-artifacts --default-artifact-root s3://my-bucket
```


With this setting, the MLflow client still makes minimum HTTP requests to the tracking server for fetching proper remote storage URI,
but can directly upload artifacts to / download artifacts from the remote storage. While this might not be a good practice for access and
secury governance, it could be useful when you want to avoid the overhead of proxying artifacts through the tracking server.


noteIf the MLflow server is *not configured* with the `--serve-artifacts` option, the client directly pushes artifacts
to the artifact store. It does not proxy these through the tracking server by default.

For this reason, the client needs direct access to the artifact store. For instructions on setting up these credentials,
see [Artifact Stores documentation](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/#artifacts-stores-manage-access).


noteWhen an experiment is created, the artifact storage location from the configuration of the tracking server is logged in the experiment's metadata.
When enabling proxied artifact storage, any existing experiments that were created while operating a tracking server in
non-proxied mode will continue to use a non-proxied artifact location. In order to use proxied artifact logging, a new experiment must be created.
If the intention of enabling a tracking server in `-serve-artifacts` mode is to eliminate the need for a client to have authentication to
the underlying storage, new experiments should be created for use by clients so that the tracking server can handle authentication after this migration.


#### Optionally using a Tracking Server instance exclusively for artifact handling[​](#tracking-server-artifacts-only)


MLflow Tracking Server can be configured to use different backend store and artifact store, and provides a single endpoint for the clients.


However, if the volume of tracking server requests is sufficiently large and performance issues are noticed, a tracking server
can be configured to serve in `--artifacts-only` mode, operating in tandem with an instance that
operates with `--no-serve-artifacts` specified. This configuration ensures that the processing of artifacts is isolated
from all other tracking server event handling.


When a tracking server is configured in `--artifacts-only` mode, any tasks apart from those concerned with artifact
handling (i.e., model logging, loading models, logging artifacts, listing artifacts, etc.) will return an HTTPError.
See the following example of a client REST call in Python attempting to list experiments from a server that is configured in
`--artifacts-only` mode:


bash```
# Launch the artifact-only servermlflow server --artifacts-only ...
```


python```
import requests# Attempt to list experiments from the serverresponse = requests.get("http://0.0.0.0:8885/api/2.0/mlflow/experiments/list")
```


Output_```
>> HTTPError: Endpoint: /api/2.0/mlflow/experiments/list disabled due to the mlflow server running in `--artifacts-only` mode.
```


Using an additional MLflow server to handle artifacts exclusively can be useful for large-scale MLOps infrastructure.
Decoupling the longer running and more compute-intensive tasks of artifact handling from the faster and higher-volume
metadata functionality of the other Tracking API requests can help minimize the burden of an otherwise single MLflow
server handling both types of payloads.


noteIf an MLflow server is running with the `--artifacts-only` flag, the client should interact with this server explicitly by
including either a `host` or `host:port` definition for uri location references for artifacts.
Otherwise, all artifact requests will route to the MLflow Tracking server, defeating the purpose of running a distinct artifact server.


## Secure Tracking Server[​](#tracking-auth)


### Built-in Security Middleware[​](#built-in-security-middleware)


MLflow 3.5.0+ includes security middleware that automatically protects against common web vulnerabilities:


- **DNS Rebinding Protection**: Validates Host headers to prevent attacks on internal services
- **CORS Protection**: Controls which web applications can access your API
- **Clickjacking Prevention**: X-Frame-Options header controls iframe embedding


Configure these features with simple command-line options:


bash```
mlflow server --host 0.0.0.0 \  --allowed-hosts "mlflow.company.com" \  --cors-allowed-origins "https://app.company.com"
```


For detailed configuration options, see [Security Configuration](https://mlflow.org/docs/latest/self-hosting/security/network/).


### Authentication and Encryption[​](#authentication-and-encryption)


For production deployments, we recommend using a reverse proxy (NGINX, Apache httpd) or VPN to add:


- **TLS/HTTPS encryption** for secure communication
- **Authentication** via proxy authentication headers


You can pass authentication headers to MLflow using these environment variables:


- `MLFLOW_TRACKING_USERNAME` and `MLFLOW_TRACKING_PASSWORD` - username and password to use with HTTP
Basic authentication. To use Basic authentication, you must set `both` environment variables.
- `MLFLOW_TRACKING_TOKEN` - token to use with HTTP Bearer authentication. Basic authentication takes precedence if set.
- `MLFLOW_TRACKING_INSECURE_TLS` - If set to the literal `true`, MLflow does not verify the TLS connection,
meaning it does not validate certificates or hostnames for `https://` tracking URIs. This flag is not recommended for
production environments. If this is set to `true` then `MLFLOW_TRACKING_SERVER_CERT_PATH` must not be set.
- `MLFLOW_TRACKING_SERVER_CERT_PATH` - Path to a CA bundle to use. Sets the `verify` param of the
`requests.request` function
(see [requests main interface](https://requests.readthedocs.io/en/master/api)).
When you use a self-signed server certificate you can use this to verify it on client side.
If this is set `MLFLOW_TRACKING_INSECURE_TLS` must not be set (false).
- `MLFLOW_TRACKING_CLIENT_CERT_PATH` - Path to ssl client cert file (.pem). Sets the `cert` param
of the `requests.request` function
(see [requests main interface](https://requests.readthedocs.io/en/master/api)).
This can be used to use a (self-signed) client certificate.


For notebook integration and UI embedding options, see [Network Security](https://mlflow.org/docs/latest/self-hosting/security/network/) configuration.


## Tracking Server versioning[​](#tracking-server-versioning)


The version of MLflow running on the server can be found by querying the `/version` endpoint.
This can be used to check that the client-side version of MLflow is up-to-date with a remote tracking server prior to running experiments.
For example:


python```
import requestsimport mlflowresponse = requests.get("http://<mlflow-host>:<mlflow-port>/version")assert response.text == mlflow.__version__  # Checking for a strict version match
```


## Model Version Source Validation[​](#model-version-source-validation)


The tracking server can be configured to validate model version sources using a regular expression pattern. This security feature helps ensure that only model versions from approved sources are registered in your model registry.


### Configuration[​](#configuration)


Set the `MLFLOW_CREATE_MODEL_VERSION_SOURCE_VALIDATION_REGEX` environment variable when starting the tracking server:


bash```
export MLFLOW_CREATE_MODEL_VERSION_SOURCE_VALIDATION_REGEX="^mlflow-artifacts:/.*$"mlflow server --host 0.0.0.0 --port 5000
```


When this environment variable is set, the tracking server will validate the `source` parameter in model version creation requests against the specified regular expression pattern. If the source doesn't match the pattern, the request will be rejected with an error.


### Example: Restricting to MLflow Artifacts[​](#example-restricting-to-mlflow-artifacts)


To only allow model versions from MLflow artifacts storage:


bash```
export MLFLOW_CREATE_MODEL_VERSION_SOURCE_VALIDATION_REGEX="^mlflow-artifacts:/.*$"mlflow server --host 0.0.0.0 --port 5000
```


With this configuration:


python```
import mlflowfrom mlflow import MlflowClientclient = MlflowClient("http://localhost:5000")# This will work - source matches the patternclient.create_model_version(    name="my-model",    source="mlflow-artifacts://1/artifacts/model",    run_id="abc123",)# This will fail - source doesn't match the patternclient.create_model_version(    name="my-model",    source="s3://my-bucket/model",    run_id="def456",)  # Raises MlflowException: Invalid model version source
```


### Example: Restricting to Specific S3 Buckets[​](#example-restricting-to-specific-s3-buckets)


To only allow model versions from specific S3 buckets:


bash```
export MLFLOW_CREATE_MODEL_VERSION_SOURCE_VALIDATION_REGEX="^s3://(production-models|staging-models)/.*$"mlflow server --host 0.0.0.0 --port 5000
```


This pattern would allow sources like:


- `s3://production-models/model-v1/`
- `s3://staging-models/experiment-123/model/`


But reject sources like:


- `s3://untrusted-bucket/model/`
- `file:///local/path/model`


note- If the environment variable is not set, no source validation is performed.
- The validation only applies to the `/mlflow/model-versions/create` API endpoint.
- The regular expression is applied using Python's `re.search()` function.
- Use standard regular expression syntax for pattern matching.


## Fetching Server Version[​](#fetching-server-version)


The version of MLflow running on the server can be found by querying the `/version` endpoint.
This can be used to check that the client-side version of MLflow is up-to-date with a remote tracking server prior to running experiments.
For example:


python```
import requestsimport mlflowresponse = requests.get("http://<mlflow-host>:<mlflow-port>/version")assert response.text == mlflow.__version__  # Checking for a strict version match
```


## Handling timeout when uploading/downloading large artifacts[​](#handling-timeout-when-uploadingdownloading-large-artifacts)


When uploading or downloading large artifacts through the tracking server with the artifact proxy enabled, the server may take a long time to process the request. If it exceeds the timeout limit, the server will terminate the request, resulting in a request failure on the client side.


Example client code:


python```
import mlflowmlflow.set_tracking_uri("<TRACKING_SERVER_URI>")with mlflow.start_run():    mlflow.log_artifact("large.txt")
```


Client traceback:


text```
Traceback (most recent call last):  File "/Users/user/python3.10/site-packages/requests/adapters.py", line 486, in send    resp = conn.urlopen(  File "/Users/user/python3.10/site-packages/urllib3/connectionpool.py", line 826, in urlopen    return self.urlopen(  ...  File "/Users/user/python3.10/site-packages/urllib3/connectionpool.py", line 798, in urlopen    retries = retries.increment(  File "/Users/user/python3.10/site-packages/urllib3/util/retry.py", line 592, in increment    raise MaxRetryError(_pool, url, error or ResponseError(cause))urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='mlflow.example.com', port=443): Max retries exceeded with url: ... (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:2426)')))During handling of the above exception, another exception occurred:
```


Tracking server logs:


bash```
INFO:     Started server process [82]INFO:     Waiting for application startup.INFO:     Application startup complete.INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)...WARNING:  Request timeout exceededERROR:    Exception in ASGI application
```


To mitigate this issue, the timeout length can be increased by using the `--uvicorn-opts` option when starting the server as shown below:


bash```
mlflow server --uvicorn-opts "--timeout-keep-alive=120" ...
```


For users still using gunicorn (via `--gunicorn-opts`), the equivalent command would be:


bash```
mlflow server --gunicorn-opts "--timeout=120" ...
```


See the [uvicorn settings documentation](https://www.uvicorn.org/settings/) for more configuration options.


## Full List of Command Line Options[​](#full-list-of-command-line-options)


Please run `mlflow server --help` for the full list of command line options.

---

## MLflow Tracking Quickstart | MLflow
<a id="MLflow-Tracking-Quickstart-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/ml/tracking/quickstart/

The purpose of this quickstart is to provide a quick guide to the most essential core APIs of MLflow Tracking. In just a few minutes of following along with this quickstart, you will learn:

On this page# MLflow Tracking Quickstart


The purpose of this quickstart is to provide a quick guide to the most essential core APIs of MLflow Tracking. In just a few minutes of following along with this quickstart, you will learn:


- How to **log** parameters, metrics, and a model using the MLflow logging API
- How to navigate to a model in the **MLflow UI**
- How to **load** a logged model for inference


## Step 1 - Set up MLflow[​](#step-1---set-up-mlflow)


MLflow is available on PyPI. If you don't already have it installed on your system, you can install it with:


bash```
pip install mlflow
```


Then, follow the instructions in the [Set Up MLflow](https://mlflow.org/docs/latest/ml/getting-started/running-notebooks/) guide to set up MLflow.


If you just want to start super quick, run the following code in a notebook cell:


python```
import mlflowmlflow.set_experiment("MLflow Quickstart")
```


## Step 2 - Prepare training data[​](#step-2---prepare-training-data)


Before training our first model, let's prepare the training data and model hyperparameters.


python```
import pandas as pdfrom sklearn import datasetsfrom sklearn.model_selection import train_test_splitfrom sklearn.linear_model import LogisticRegressionfrom sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score# Load the Iris datasetX, y = datasets.load_iris(return_X_y=True)# Split the data into training and test setsX_train, X_test, y_train, y_test = train_test_split(    X, y, test_size=0.2, random_state=42)# Define the model hyperparametersparams = {    "solver": "lbfgs",    "max_iter": 1000,    "multi_class": "auto",    "random_state": 8888,}
```


## Step 3 - Train a model with MLflow Autologging[​](#step-3---train-a-model-with-mlflow-autologging)


In this step, we train the model on the training data loaded in the previous step, and log the model and its metadata to MLflow. The easiest way to do this is to using MLflow's **Autologging** feature.


python```
import mlflow# Enable autologging for scikit-learnmlflow.sklearn.autolog()# Just train the model normallylr = LogisticRegression(**params)lr.fit(X_train, y_train)
```


With just one line of additional code `mlflow.sklearn.autolog()`, now you get the best of both worlds: you can focus on training the model, and MLflow will take care of the rest:


- Saving the trained model.
- Recording the model's performance metrics during training, such as accuracy, precision, AUC curve.
- Logging hyperparameter values used to train the model.
- Track metadata such as input data format, user, timestamp, etc.


To learn more about autologging and supported libraries, see the [Autologging](https://mlflow.org/docs/latest/ml/tracking/autolog/) documentation.


## Step 4 - View the Run in the MLflow UI[​](#step-4---view-the-run-in-the-mlflow-ui)


To see the results of training, you can access the MLflow UI by navigating to the URL of the Tracking Server. If you have not started one, open a new terminal and run the following command at the root of the MLflow project and access the UI at [http://localhost:5000](http://localhost:5000) (or the port number you specified).


bash```
mlflow ui --port 5000
```


When opening the site, you will see a screen similar to the following:


![MLflow UI Home page](https://mlflow.org/docs/latest/images/tutorials/introductory/quickstart-tracking/quickstart-ui-home.png)
The "Experiments" section shows a list of (recently created) experiments. Click on the "MLflow Quickstart" experiment.


![MLflow UI Run list page](https://mlflow.org/docs/latest/images/tutorials/introductory/quickstart-tracking/quickstart-ui-run-list.png)
The training **Run** created by MLflow is listed in the table. Click the run to view the details.


![MLflow UI Run detail page](https://mlflow.org/docs/latest/images/tutorials/introductory/quickstart-tracking/quickstart-our-run.png)
The Run detail page shows an overview of the run, its recorded metrics, hyper-parameters, tags, and more. Play around with the UI to see the different views and features.


Scroll down to the "Model" section and you will see the model that was logged during training. Click on the model to view the details.


![MLflow UI Model detail page](https://mlflow.org/docs/latest/images/tutorials/introductory/quickstart-tracking/quickstart-ui-logged-models.png)
The model page displays similar metadata such as performance metrics and hyper-parameters. It also includes an "Artifacts" section that lists the files that were logged during training. You can also see environment information such as the Python version and dependencies, which are stored for reproducibility.


![MLflow UI Model detail page](https://mlflow.org/docs/latest/images/tutorials/introductory/quickstart-tracking/quickstart-our-model.png)
## Step 5 - Log a model and metadata manually[​](#step-5---log-a-model-and-metadata-manually)


Now that we've learned how to log a model training run with MLflow autologging, let's step further and learn how to log a model and metadata manually. This is useful when you want to have more control over the logging process.


The steps that we will take are:


- Initiate an MLflow **run** context to start a new run that we will log the model and metadata to.
- Train and test the model.
- **Log** model **parameters** and performance **metrics**.
- **Tag** the run for easy retrieval.


python```
# Start an MLflow runwith mlflow.start_run():    # Log the hyperparameters    mlflow.log_params(params)    # Train the model    lr = LogisticRegression(**params)    lr.fit(X_train, y_train)    # Log the model    mlflow.sklearn.log_model(sk_model=lr, name="iris_model")    # Predict on the test set, compute and log the loss metric    y_pred = lr.predict(X_test)    accuracy = accuracy_score(y_test, y_pred)    mlflow.log_metric("accuracy", accuracy)    # Optional: Set a tag that we can use to remind ourselves what this run was for    mlflow.set_tag("Training Info", "Basic LR model for iris data")
```


## Step 6 - Load the model back for inference.[​](#step-6---load-the-model-back-for-inference)


After logging the model, we can perform inference by:


- **Loading** the model using MLflow's `pyfunc` flavor.
- Running **Predict** on new data using the loaded model.


infoTo load the model as native scikit-learn model, use `mlflow.sklearn.load_model(model_info.model_uri)` instead of the pyfunc flavor.


python```
# Load the model back for predictions as a generic Python Function modelloaded_model = mlflow.pyfunc.load_model(model_info.model_uri)predictions = loaded_model.predict(X_test)iris_feature_names = datasets.load_iris().feature_namesresult = pd.DataFrame(X_test, columns=iris_feature_names)result["actual_class"] = y_testresult["predicted_class"] = predictionsresult[:4]
```


The output of this code will look something like this:


sepal length (cm)sepal width (cm)petal length (cm)petal width (cm)actual_classpredicted_class6.12.84.71.2115.73.81.70.3007.72.66.92.3226.02.94.51.511
## Next Steps[​](#next-steps)


Congratulations on working through the MLflow Tracking Quickstart! You should now have a basic understanding of how to use the MLflow Tracking API to log models.


- [MLflow for GenAI](https://mlflow.org/docs/latest/genai/): Learn how to use MLflow for GenAI/LLM development.
- [MLflow for Deep Learning](https://mlflow.org/docs/latest/ml/deep-learning/): Learn how to use MLflow for deep learning frameworks such as PyTorch, TensorFlow, etc.
- [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/): Learn more about the MLflow Tracking APIs.
- [Self-hosting Guide](https://mlflow.org/docs/latest/self-hosting/): Learn how to self-host the MLflow Tracking Server and set it up for team collaboration.

---

## Tracking Experiments with Local Database | MLflow
<a id="Tracking-Experiments-with-Local-Database-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/ml/tracking/tutorials/local-database/

In this tutorial, you will learn how to use a local database to track your experiment metadata with MLflow.

On this page# Tracking Experiments with Local Database


In this tutorial, you will learn how to use a local database to track your experiment metadata with MLflow.


By default, MLflow Tracking logs (*writes*) run data to local files,
which may cause some frustration due to fractured small files and the lack of a simple access interface. Also, if you are using Python, you can use SQLite that runs
upon your local file system (e.g. `mlruns.db`) and has a built-in client `sqlite3`, eliminating the effort to install any additional dependencies and setting up database server.


## Step 1. Get MLflow[​](#step-1-get-mlflow)


MLflow is available on PyPI. If you don't already have it installed on your local machine, you can install it with:


bash```
pip install mlflow
```


## Step 2. Configure MLflow to Log to SQLite Database[​](#step-2-configure-mlflow-to-log-to-sqlite-database)


To point MLflow to your local SQLite database, you need to set the environment variable `MLFLOW_TRACKING_URI` (e.g., `sqlite:///mlruns.db`).
This will create a SQLite database file (`mlruns.db`) in the current directory. Specify a different path if you want to store the database file in a different location.


bash```
export MLFLOW_TRACKING_URI=sqlite:///mlruns.db
```


If you are in a notebook, run the following cell instead:


text```
%env MLFLOW_TRACKING_URI=sqlite:///mlruns.db
```


noteFor using a SQLite database, MLflow automatically creates a new database if it does not exist. If you want to use a different database, you need to create the database first.


## Step 3. Start Logging[​](#step-3-start-logging)


Now you are ready to start logging your experiment runs. For example, the following code runs training for a scikit-learn RandomForest model on the diabetes dataset:


python```
import mlflowfrom sklearn.model_selection import train_test_splitfrom sklearn.datasets import load_diabetesfrom sklearn.ensemble import RandomForestRegressormlflow.sklearn.autolog()db = load_diabetes()X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)# Create and train models.rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)rf.fit(X_train, y_train)# Use the model to make predictions on the test dataset.predictions = rf.predict(X_test)
```


## Step 4. View Your Logged Run in Tracking UI[​](#step-4-view-your-logged-run-in-tracking-ui)


Once your training job finishes, you can run the following command to launch the MLflow UI (You will have to specify the path to SQLite database file with `--backend-store-uri` option):


bash```
mlflow ui --port 8080 --backend-store-uri sqlite:///mlruns.db
```


Then, navigate to [`http://localhost:8080`](http://localhost:8080) in your browser to view the results.


## What's Next?[​](#whats-next)


You've now learned how to connect MLflow Tracking with a remote storage and a database.


There are a couple of more advanced topics you can explore:


- **Remote environment setup for team development**: While storing runs and experiments data in local machine is perfectly fine for solo development, you should
consider using [MLflow Tracking Server](https://mlflow.org/docs/latest/ml/tracking/#tracking_server) when you set up a team collaboration environment with MLflow Tracking. Read the
[Remote Experiment Tracking with MLflow Tracking Server](https://mlflow.org/docs/latest/ml/tracking/tutorials/remote-server/) tutorial to learn more.

---

## Remote Experiment Tracking with MLflow Tracking Server | MLflow
<a id="Remote-Experiment-Tracking-with-MLflow-Tracking-Server-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/ml/tracking/tutorials/remote-server/

In this tutorial, you will learn how to set up MLflow Tracking environment for team development using the MLflow Tracking Server.

On this page# Remote Experiment Tracking with MLflow Tracking Server


In this tutorial, you will learn how to set up MLflow Tracking environment for team development using the [MLflow Tracking Server](https://mlflow.org/docs/latest/ml/tracking/#tracking_server).


There are many benefits to utilize MLflow Tracking Server for remote experiment tracking:


- **Collaboration**: Multiple users can log runs to the same endpoint, and query runs and models logged by other users.
- **Sharing Results**: The tracking server also serves a [Tracking UI](https://mlflow.org/docs/latest/ml/tracking/#tracking_ui) endpoint, where team members can easily explore each other's results.
- **Centralized Access**: The tracking server can be run as a proxy for the remote access for metadata and artifacts, making it easier to secure and audit access to data.


## How does it work?[​](#how-does-it-work)


The following picture depicts the architecture of using a remote MLflow Tracking Server with PostgreSQL and S3


![](https://mlflow.org/docs/latest/assets/images/scenario_5-26381271ff593f8d5c9e5c4c11aeaeb4.png)

Artifacture diagram of MLflow Tracking Server with PostgreSQL and S3
noteYou can find the list of supported data stores in the [artifact stores](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/) and [backend stores](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/) documentation guides.


When you start logging runs to the MLflow Tracking Server, the following happens:


- **Part 1a and b**:


- The MLflow client creates an instance of a *RestStore* and sends REST API requests to log MLflow entities
- The Tracking Server creates an instance of an *SQLAlchemyStore* and connects to the remote host for inserting
tracking information in the database (i.e., metrics, parameters, tags, etc.)
- **Part 1c and d**:


- Retrieval requests by the client return information from the configured *SQLAlchemyStore* table
- **Part 2a and b**:


- Logging events for artifacts are made by the client using the `HttpArtifactRepository` to write files to MLflow Tracking Server
- The Tracking Server then writes these files to the configured object store location with assumed role authentication
- **Part 2c and d**:


- Retrieving artifacts from the configured backend store for a user request is done with the same authorized authentication that was configured at server start
- Artifacts are passed to the end user through the Tracking Server through the interface of the `HttpArtifactRepository`


## Getting Started[​](#getting-started)


### Preface[​](#preface)


In an actual production deployment environment, you will have multiple remote hosts to run both the tracking server and databases, as shown in the diagram above. However, for the purposes of this tutorial,
we will just use a single machine with multiple Docker containers running on different ports, mimicking the remote environment with a far easier evaluation tutorial setup. We will also use [MinIO](https://min.io/),
an S3-compatible object storage, as an artifact store so that you don't need to have AWS account to run this tutorial.


### Step 1 - Get MLflow and additional dependencies[​](#step-1---get-mlflow-and-additional-dependencies)


MLflow is available on PyPI. Also [pyscopg2](https://pypi.org/project/psycopg2/) and [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) are required for accessing PostgreSQL and S3 with Python.
If you don't already have them installed on your system, you can install them with:


bash```
pip install mlflow psycopg2 boto3
```


### Step 2 - Set up remote data stores[​](#step-2---set-up-remote-data-stores)


MLflow Tracking Server can interact with a variety of data stores to store experiment and run data as well as artifacts.
In this tutorial, we will use **Docker Compose** to start two containers, each of them simulating remote servers in an actual environment.


1. [PostgreSQL](https://www.postgresql.org/) database as a backend store.
2. [MinIO](https://min.io/) server as an artifact store.


#### Install docker and docker-compose[​](#install-docker-and-docker-compose)


noteThese docker steps are only required for the tutorial purpose. MLflow itself doesn't depend on Docker at all.


Follow the official instructions for installing [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/). Then, run `docker --version` and `docker-compose --version` to make sure they are installed correctly.


#### Create `compose.yaml`[​](#create-composeyaml)


Create a file named `compose.yaml` with the following content:


compose.yamlyaml```
version: "3.7"services:  # PostgreSQL database  postgres:    image: postgres:latest    environment:      POSTGRES_USER: user      POSTGRES_PASSWORD: password      POSTGRES_DB: mlflowdb    ports:      - 5432:5432    volumes:      - ./postgres-data:/var/lib/postgresql  # MinIO server  minio:    image: minio/minio    expose:      - "9000"    ports:      - "9000:9000"      # MinIO Console is available at http://localhost:9001      - "9001:9001"    environment:      MINIO_ROOT_USER: "minio_user"      MINIO_ROOT_PASSWORD: "minio_password"    healthcheck:      test: timeout 5s bash -c ':> /dev/tcp/127.0.0.1/9000' || exit 1      interval: 1s      timeout: 10s      retries: 5    command: server /data --console-address ":9001"  # Create a bucket named "bucket" if it doesn't exist  minio-create-bucket:    image: minio/mc    depends_on:      minio:        condition: service_healthy    entrypoint: >      bash -c "      mc alias set minio http://minio:9000 minio_user minio_password &&      if ! mc ls minio/bucket; then        mc mb minio/bucket      else        echo 'bucket already exists'      fi      "
```


#### Start the containers[​](#start-the-containers)


Run the following command from the same directory `compose.yaml` file resides to start the containers.
This will start the containers for PostgreSQL and Minio server in the background, as well as create a
new bucket named "bucket" in Minio.


bash```
docker compose up -d
```


### Step 3 - Start the Tracking Server[​](#step-3---start-the-tracking-server)


noteIn actual environment, you will have a remote host that will run the tracking server, but in this tutorial we will just use our local machine as a simulated surrogate for a remote machine.


#### Configure access[​](#configure-access)


For the tracking server to access remote storage, it needs to be configured with the necessary credentials.


bash```
export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000 # Replace this with remote storage endpoint e.g. s3://my-bucket in real use casesexport AWS_ACCESS_KEY_ID=minio_userexport AWS_SECRET_ACCESS_KEY=minio_password
```


You can find the instructions for how to configure credentials for other storages in [Supported Storage](https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/#artifacts-store-supported-storages).


#### Launch the tracking server[​](#launch-the-tracking-server)


To specify the backend store and artifact store, you can use the `--backend-store-uri` and `--artifacts-store-uri` options respectively.


bash```
mlflow server \  --backend-store-uri postgresql://user:password@localhost:5432/mlflowdb \  --artifacts-destination s3://bucket \  --host 0.0.0.0 \  --port 5000
```


Replace `localhost` with the remote host name or IP address for your database server in actual environment.


### Step 4: Logging to the Tracking Server[​](#step-4-logging-to-the-tracking-server)


Once the tracking server is running, you can log runs to it by setting the MLflow Tracking URI to the tracking server's URI. Alternatively, you can use the [`mlflow.set_tracking_uri()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.set_tracking_uri) API to set the tracking URI.


bash```
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000  # Replace with remote host name or IP address in an actual environment
```


Then run your code with MLflow tracking APIs as usual. The following code runs training for a scikit-learn RandomForest model on the diabetes dataset:


python```
import mlflowfrom sklearn.model_selection import train_test_splitfrom sklearn.datasets import load_diabetesfrom sklearn.ensemble import RandomForestRegressormlflow.autolog()db = load_diabetes()X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)# Create and train models.rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)rf.fit(X_train, y_train)# Use the model to make predictions on the test dataset.predictions = rf.predict(X_test)
```


### Step 5: View logged Run in Tracking UI[​](#step-5-view-logged-run-in-tracking-ui)


Our pseudo-remote MLflow Tracking Server also hosts the Tracking UI on the same endpoint. In an actual deployment environment with a remote tracking server, this is also the case.
You can access the UI by navigating to [`http://127.0.0.1:5000`](http://127.0.0.1:5000) (replace with remote host name or IP address in actual environment) in your browser.


### Step 6: Download artifacts[​](#step-6-download-artifacts)


MLflow Tracking Server also serves as a proxy host for artifact access. Artifact access is enabled through the proxy URIs such as `models:/`, `mlflow-artifacts:/`,
giving users access to this location without having to manage credentials or permissions of direct access.


python```
import mlflowmodel_id = "YOUR_MODEL_ID"  # You can find model ID in the Tracking UI# Download artifact via the tracking servermlflow_artifact_uri = f"models:/{model_id}"local_path = mlflow.artifacts.download_artifacts(mlflow_artifact_uri)# Load the modelmodel = mlflow.sklearn.load_model(local_path)
```


## What's Next?[​](#whats-next)


Now you have learned how to set up MLflow Tracking Server for remote experiment tracking!
There are a couple of more advanced topics you can explore:


- **Other configurations for the Tracking Server**: By default, MLflow Tracking Server serves both backend store and artifact store.
You can also configure the Tracking Server to serve only backend store or artifact store, to handle different use cases such as large
traffic or security concerns. See [other use cases](https://mlflow.org/docs/latest/ml/tracking/#other-tracking-setup) for how to customize the Tracking Server for these use cases.
- **Secure the Tracking Server**: The `--host` option exposes the service on all interfaces. If running a server in production, we
would recommend not exposing the built-in server broadly (as it is unauthenticated and unencrypted). Read [Secure Tracking Server](https://mlflow.org/docs/latest/self-hosting/security/network/)
for the best practices to secure the Tracking Server in production.

---

## MLflow Model Registry | MLflow
<a id="MLflow-Model-Registry-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/ml/model-registry/

The MLflow Model Registry is a centralized model store, set of APIs and a UI designed to

On this page# MLflow Model Registry


The MLflow Model Registry is a centralized model store, set of APIs and a UI designed to
collaboratively manage the full lifecycle of a model. It provides lineage (i.e., which
MLflow experiment and run produced the model), versioning, aliasing, metadata tagging and
annotation support to ensure that you have the full spectrum of information at every stage from development to production deployment.


## Why Model Registry?[​](#why-model-registry)


As machine learning projects grow in complexity and scale, managing models manually across different environments, teams, and iterations becomes increasingly error-prone and inefficient.
The MLflow Model Registry addresses this challenge by providing a centralized, structured system for organizing and governing ML models throughout their lifecycle.


Using the Model Registry offers the following benefits:


- **🗂️ Version Control**: The registry automatically tracks versions of each model, allowing teams to compare iterations, roll back to previous states, and manage multiple versions in parallel (e.g., staging vs. production).
- **🧬 Model Lineage and Traceability**: Each registered model version is linked to the MLflow run, logged model or notebook that produced it, enabling full reproducibility. You can trace back exactly how a model was trained, with what data and parameters.
- **🚀 Production-Ready Workflows**: Features like model aliases (e.g., @champion) and tags make it easier to manage deployment workflows, promoting models to experimental, staging, or production environments in a controlled and auditable way.
- **🛡️ Governance and Compliance**: With structured metadata, tagging, and role-based access controls (when used with a backend like Databricks or a managed MLflow service), the Model Registry supports governance requirements critical for enterprise-grade ML operations.


Whether you're a solo data scientist or part of a large ML platform team, the Model Registry is a foundational component for scaling reliable and maintainable machine learning systems.


## Concepts[​](#concepts)


The Model Registry introduces a few concepts that describe and facilitate the full lifecycle of an MLflow Model.


ConceptDescriptionModelAn MLflow Model is created with one of the model flavor's **`mlflow.<model_flavor>.log_model()`** methods, or **[`mlflow.create_external_model()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.create_external_model)** API since MLflow 3.
Once logged, this model can then be registered with the Model Registry.

Registered ModelAn MLflow Model can be registered with the Model Registry. A registered model has a unique name, contains versions, aliases, tags, and other metadata.

Model VersionEach registered model can have one or many versions. When a new model is added to the Model Registry, it is added as version 1. Each new model registered to
the same model name **increments the version number**. Model versions have tags, which can be useful for tracking attributes of the model version (e.g. *`pre_deploy_checks: "PASSED"`*)

Model URIYou can refer to the registered model by using a URI of this format: `models:/<model-name>/<model-version>`, e.g., if you have a registered model with name "MyModel" and version 1, the URI referring to the model is: `models:/MyModel/1`".

Model AliasModel aliases allow you to assign a mutable, named reference to a particular version of a registered model. By assigning an alias to a specific model version,
you can use the alias to refer to that model version via a model URI or the model registry API. For example, you can create an alias named **`champion`** that
points to version 1 of a model named **`MyModel`**. You can then refer to version 1 of **`MyModel`** by using the URI **`models:/MyModel@champion`**.

Aliases are especially useful for deploying models. For example, you could assign a **`champion`** alias to the model version intended for production traffic
and target this alias in production workloads. You can then update the model serving production traffic by reassigning the **`champion`** alias to a different model version.

TagsTags are key-value pairs that you associate with registered models and model versions, allowing you to label and categorize them by function or status. For example, you
could apply a tag with key **`"task"`** and value **`"question-answering"`** (displayed in the UI as **`task:question-answering`**) to registered models intended for question
answering tasks. At the model version level, you could tag versions undergoing pre-deployment validation with **`validation_status:pending`** and those cleared for deployment
with **`validation_status:approved`**.

Annotations and DescriptionsYou can annotate the top-level model and each version individually using Markdown, including the description and any relevant information useful for the team such as algorithm
descriptions, datasets employed or the overall methodology involved in a given version's modeling approach.


## Model Registry in practice[​](#model-registry-in-practice)


The MLflow Model Registry is available in both open-source (OSS) MLflow and managed platforms like Databricks. Depending on the environment, the registry offers different
levels of integration, governance, and collaboration features.


### Model Registry in OSS MLflow[​](#model-registry-in-oss-mlflow)


In the open-source version of MLflow, the Model Registry provides both a UI and API for managing the lifecycle of machine learning models.
You can register models, track versions, add tags and descriptions, and transition models between stages such as Staging and Production.


Register a model in MLflow- Python APIs
- MLflow UI

#### Register a model with MLflow Python APIs[​](#register-a-model-with-mlflow-python-apis)

MLflow provides several ways to register a model version

text```
# Option 1: specify `registered_model_name` parameter when logging a modelmlflow.<flavor>.log_model(..., registered_model_name="<YOUR_MODEL_NAME>")# Option 2: register a logged modelmlflow.register_model(model_uri="<YOUR_MODEL_URI>", name="<YOUR_MODEL_NAME>")
```

After registering the model, you can load it back with the model name and version

text```
mlflow.<flavor>.load_model("models:/<YOUR_MODEL_NAME>/<YOUR_MODEL_VERSION>")
```

#### Register a model on MLflow UI[​](#register-a-model-on-mlflow-ui)

1. Open the details page for the MLflow Run containing the logged MLflow model you'd like to register. Select the model folder containing the intended MLflow model in the
**Artifacts** section.

![](https://mlflow.org/docs/latest/assets/images/oss_registry_1_register-a71f2ea36d15265894cf0ea1810dd95f.png)

1. Click the **Register Model** button, which will trigger a modal form to pop up.
2. In the **Model** dropdown menu on the form, you can either select "Create New Model" (which creates a new registered model with your MLflow model as its initial version)
or select an existing registered model (which registers your model under it as a new version). The screenshot below demonstrates registering the MLflow model to a new registered
model named `"iris_model_testing"`.

![](https://mlflow.org/docs/latest/assets/images/oss_registry_2_dialog-1ac2c5e115d621eb507274c577093173.png)


To learn more about the OSS Model Registry, refer to the [tutorial on the model registry](https://mlflow.org/docs/latest/ml/model-registry/tutorial/).


### Model Registry in Databricks[​](#model-registry-in-databricks)


Databricks extends MLflow's capabilities by integrating the Model Registry with Unity Catalog, enabling centralized governance, fine-grained access control, and cross-workspace collaboration.


Key benefits of Unity Catalog integration include:


- **🛡️ Enhanced governance**: Apply access policies and permission controls to model assets.
- **🌐 Cross-workspace access**: Register models once and access them across multiple Databricks workspaces.
- **🔗 Model lineage**: Track which notebooks, datasets, and experiments were used to create each model.
- **🔍 Discovery and reuse**: Browse and reuse production-grade models from a shared catalog.


Register a model in Databricks UC- Python APIs
- Databricks UI

#### Register a model to Databricks UC with MLflow Python APIs[​](#register-a-model-to-databricks-uc-with-mlflow-python-apis)

**Prerequisite**: Set tracking uri to Databricks

python```
import mlflowmlflow.set_registry_uri("databricks-uc")
```

Use MLflow APIs to register the model

text```
# Option 1: specify `registered_model_name` parameter when logging a modelmlflow.<flavor>.log_model(..., registered_model_name="<YOUR_MODEL_NAME>")# Option 2: register a logged modelmlflow.register_model(model_uri="<YOUR_MODEL_URI>", name="<YOUR_MODEL_NAME>")
```

warningML model versions in UC must have a [model signature](https://mlflow.org/docs/latest/ml/model/signatures/). If you want to set a signature on a model that's
already logged or saved, the [`mlflow.models.set_signature()`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.models.html#mlflow.models.set_signature) API is available for this purpose.

After registering the model, you can load it back with the model name and version

text```
mlflow.<flavor>.load_model("models:/<YOUR_MODEL_NAME>/<YOUR_MODEL_VERSION>")
```

#### Register a model on Databricks UI[​](#register-a-model-on-databricks-ui)

1. From the experiment run page or models page, click Register model in the upper-right corner of the UI.
2. In the dialog, select Unity Catalog, and select a destination model from the drop down list.

![](https://mlflow.org/docs/latest/assets/images/uc_register_model_1_dialog-dbc7806e79613776eb84159fa6c394e2.png)

1. Click Register.

![](https://mlflow.org/docs/latest/assets/images/uc_register_model_2_button-e6b3b94bde6506bda3be82836db5e019.png)

Registering a model can take time. To monitor progress, navigate to the destination model in Unity Catalog and refresh periodically.


For more information, refer to the [Databricks documentation](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle) on managing the model lifecycle.

---

## MLflow: A Tool for Managing the Machine Learning Lifecycle | MLflow
<a id="MLflow-A-Tool-for-Managing-the-Machine-Learning-Lifecycle-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/ml/

MLflow is an open-source platform, purpose-built to assist machine learning practitioners and teams in

On this page# MLflow: A Tool for Managing the Machine Learning Lifecycle


MLflow is an open-source platform, purpose-built to assist machine learning practitioners and teams in
handling the complexities of the machine learning process. MLflow focuses on the full lifecycle for
machine learning projects, ensuring that each phase is manageable, traceable, and reproducible.


## MLflow Getting Started Resources[​](#mlflow-getting-started-resources)


If this is your first time exploring MLflow, the tutorials and guides here are a great place to start. The emphasis in each of these is
getting you up to speed as quickly as possible with the basic functionality, terms, APIs, and general best practices of using MLflow in order to
enhance your learning in area-specific guides and tutorials.


[### Quickstart

A quick guide to learn the basics of MLflow by training a simple scikit-learn model

Start learning →](https://mlflow.org/docs/latest/ml/getting-started/quickstart/)[### MLflow for GenAI / LLM

A walkthrough of MLflow's GenAI / LLM capabilities, including tracing, evaluation, and prompt management

Start building →](https://mlflow.org/docs/latest/genai/getting-started/connect-environment/)[### Deep Learning Guide

A hands-on tutorial on how to use MLflow to track deep learning model training using PyTorch as an example

Start training →](https://mlflow.org/docs/latest/ml/getting-started/deep-learning/)
## Traditional ML and Deep Learning with MLflow[​](#traditional-ml-and-deep-learning-with-mlflow)


MLflow provides comprehensive support for traditional machine learning and deep learning workflows. From experiment tracking and model versioning to deployment and monitoring, MLflow streamlines every aspect of the ML lifecycle. Whether you're working with scikit-learn models, training deep neural networks, or managing complex ML pipelines, MLflow provides the tools you need to build reliable, scalable machine learning systems.


Explore the core MLflow capabilities and integrations below to enhance your ML development workflow!


- Tracking & Experiments
- Model Registry
- Model Deployment
- ML Library Integrations
- Model Evaluation

### Track experiments and manage your ML development[​](#track-experiments-and-manage-your-ml-development)

#### Core Features[​](#core-features)

**MLflow Tracking** provides comprehensive experiment logging, parameter tracking, metrics visualization, and artifact management.

**Key Benefits:**

- **Experiment Organization**: Track and compare multiple model experiments
- **Metric Visualization**: Built-in plots and charts for model performance
- **Artifact Storage**: Store models, plots, and other files with each run
- **Collaboration**: Share experiments and results across teams

#### Guides[​](#guides)

[Getting Started with Tracking](https://mlflow.org/docs/latest/ml/tracking/quickstart/)

[Advanced Tracking Features](https://mlflow.org/docs/latest/ml/tracking/tracking-api/)

[Autologging for Popular Libraries](https://mlflow.org/docs/latest/ml/tracking/autolog/)

![MLflow Tracking](https://mlflow.org/docs/latest/assets/images/tracking-metrics-ui-temp-ffc0da57b388076730e20207dbd7f9c4.png)

### Manage model versions and lifecycle[​](#manage-model-versions-and-lifecycle)

#### Core Features[​](#core-features-1)

**MLflow Model Registry** provides centralized model versioning, stage management, and model lineage tracking.

**Key Benefits:**

- **Version Control**: Track model versions with automatic lineage
- **Stage Management**: Promote models through staging, production, and archived stages
- **Collaboration**: Team-based model review and approval workflows
- **Model Discovery**: Search and discover models across your organization

#### Guides[​](#guides-1)

[Model Registry Introduction](https://mlflow.org/docs/latest/ml/model-registry/)

![MLflow Model Registry](https://mlflow.org/docs/latest/assets/images/oss_registry_3_overview-daec63473b4d7bbf47c559600bf5c35d.png)

### Deploy models to production environments[​](#deploy-models-to-production-environments)

#### Core Features[​](#core-features-2)

**MLflow Deployment** supports multiple deployment targets including REST APIs, cloud platforms, and edge devices.

**Key Benefits:**

- **Multiple Targets**: Deploy to local servers, cloud platforms, or containerized - enronments
- **Model Serving**: Built-in REST API serving with automatic input validation
- **Batch Inference**: Support for batch scoring and offline predictions
- **Production Ready**: Scalable deployment options for enterprise use

#### Guides[​](#guides-2)

[Model Deployment Overview](https://mlflow.org/docs/latest/ml/deployment/)

[Local Model Serving](https://mlflow.org/docs/latest/ml/deployment/deploy-model-locally/)

[Cloud Deployment Options](https://mlflow.org/docs/latest/ml/deployment/deploy-model-to-sagemaker/)

[Kubernetes Deployment](https://mlflow.org/docs/latest/ml/deployment/deploy-model-to-kubernetes/)

![MLflow Deployment](https://mlflow.org/docs/latest/assets/images/mlflow-deployment-overview-99db410b2c58fedf506eb9ce5aa41a86.png)

### Explore Native MLflow ML Library Integrations[​](#explore-native-mlflow-ml-library-integrations)

[![Scikit-learn](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gR2VuZXJhdG9yOiBBZG9iZSBJbGx1c3RyYXRvciAxNC4wLjAsIFNWRyBFeHBvcnQgUGx1Zy1JbiAuIFNWRyBWZXJzaW9uOiA2LjAwIEJ1aWxkIDQzMzYzKSAgLS0+Cgo8c3ZnCiAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgeG1sbnM6Y2M9Imh0dHA6Ly9jcmVhdGl2ZWNvbW1vbnMub3JnL25zIyIKICAgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIgogICB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnNvZGlwb2RpPSJodHRwOi8vc29kaXBvZGkuc291cmNlZm9yZ2UubmV0L0RURC9zb2RpcG9kaS0wLmR0ZCIKICAgeG1sbnM6aW5rc2NhcGU9Imh0dHA6Ly93d3cuaW5rc2NhcGUub3JnL25hbWVzcGFjZXMvaW5rc2NhcGUiCiAgIHZlcnNpb249IjEuMSIKICAgaWQ9IkxheWVyXzEiCiAgIHg9IjBweCIKICAgeT0iMHB4IgogICB3aWR0aD0iNzMuMzc0MDg0bW0iCiAgIGhlaWdodD0iMzkuNTcwNzYzbW0iCiAgIHZpZXdCb3g9IjAgMCAyNzcuMzE5MzcgMTQ5LjU1ODc5IgogICBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCA3OTIgNjEyIgogICB4bWw6c3BhY2U9InByZXNlcnZlIgogICBpbmtzY2FwZTp2ZXJzaW9uPSIwLjkyLjMgKDI0MDU1NDYsIDIwMTgtMDMtMTEpIgogICBzb2RpcG9kaTpkb2NuYW1lPSJzY2lraXQgbGVhcm4gbG9nbyBzbWFsbC5zdmciPjxtZXRhZGF0YQogICBpZD0ibWV0YWRhdGEzNSI+PHJkZjpSREY+PGNjOldvcmsKICAgICAgIHJkZjphYm91dD0iIj48ZGM6Zm9ybWF0PmltYWdlL3N2Zyt4bWw8L2RjOmZvcm1hdD48ZGM6dHlwZQogICAgICAgICByZGY6cmVzb3VyY2U9Imh0dHA6Ly9wdXJsLm9yZy9kYy9kY21pdHlwZS9TdGlsbEltYWdlIiAvPjxkYzp0aXRsZT48L2RjOnRpdGxlPjwvY2M6V29yaz48L3JkZjpSREY+PC9tZXRhZGF0YT48ZGVmcwogICBpZD0iZGVmczMzIiAvPjxzb2RpcG9kaTpuYW1lZHZpZXcKICAgcGFnZWNvbG9yPSIjZmZmZmZmIgogICBib3JkZXJjb2xvcj0iIzY2NjY2NiIKICAgYm9yZGVyb3BhY2l0eT0iMSIKICAgb2JqZWN0dG9sZXJhbmNlPSIxMCIKICAgZ3JpZHRvbGVyYW5jZT0iMTAiCiAgIGd1aWRldG9sZXJhbmNlPSIxMCIKICAgaW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAiCiAgIGlua3NjYXBlOnBhZ2VzaGFkb3c9IjIiCiAgIGlua3NjYXBlOndpbmRvdy13aWR0aD0iNzc3IgogICBpbmtzY2FwZTp3aW5kb3ctaGVpZ2h0PSI2MjYiCiAgIGlkPSJuYW1lZHZpZXczMSIKICAgc2hvd2dyaWQ9ImZhbHNlIgogICBpbmtzY2FwZTp6b29tPSIxLjA5MDcwMDciCiAgIGlua3NjYXBlOmN4PSIxMjEuNjg4NCIKICAgaW5rc2NhcGU6Y3k9Ijc5LjQ5MjI5IgogICBpbmtzY2FwZTp3aW5kb3cteD0iMjk1MSIKICAgaW5rc2NhcGU6d2luZG93LXk9IjY3OSIKICAgaW5rc2NhcGU6d2luZG93LW1heGltaXplZD0iMCIKICAgaW5rc2NhcGU6Y3VycmVudC1sYXllcj0iTGF5ZXJfMSIKICAgdW5pdHM9Im1tIgogICBzaG93Ym9yZGVyPSJ0cnVlIgogICBmaXQtbWFyZ2luLXRvcD0iMCIKICAgZml0LW1hcmdpbi1sZWZ0PSIwIgogICBmaXQtbWFyZ2luLXJpZ2h0PSIwIgogICBmaXQtbWFyZ2luLWJvdHRvbT0iMCIgLz4KPGcKICAgaWQ9ImczIgogICB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMTIwLjYwODYxLC0yMjAuMjYwMTcpIj4KCTxwYXRoCiAgIGQ9Im0gMzMzLjMyLDM0Ny4zNDggYyAzMy44NjksLTMzLjg2NyAzOS40OTgsLTgzLjE0NiAxMi41NzIsLTExMC4wNyAtMjYuOTIyLC0yNi45MjEgLTc2LjE5OSwtMjEuMjkzIC0xMTAuMDY2LDEyLjU3MiAtMzMuODY3LDMzLjg2NiAtMjQuMDcsOTguNTY4IC0xMi41NywxMTAuMDcgOS4yOTMsOS4yOTMgNzYuMTk5LDIxLjI5MyAxMTAuMDY0LC0xMi41NzIgeiIKICAgaWQ9InBhdGg1IgogICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICBzdHlsZT0iZmlsbDojZjg5OTM5IiAvPgoJPHBhdGgKICAgZD0ibSAxOTQuMzUsMjk4LjQxMSBjIC0xOS42NDgsLTE5LjY0OCAtNDguMjQyLC0yMi45MTkgLTYzLjg2NywtNy4yOTUgLTE1LjYyMSwxNS42MjIgLTEyLjM1NSw0NC4yMiA3LjI5Nyw2My44NjUgMTkuNjUyLDE5LjY1NCA1Ny4xOTUsMTMuOTY5IDYzLjg2Myw3LjI5NSA1LjM5NiwtNS4zODcgMTIuMzYxLC00NC4yMTUgLTcuMjkzLC02My44NjUgeiIKICAgaWQ9InBhdGg3IgogICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICBzdHlsZT0iZmlsbDojMzQ5OWNkIiAvPgo8L2c+CjxnCiAgIGlkPSJnOSIKICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMC42MDg2MSwtMjIwLjI2MDE3KSI+Cgk8ZwogICBpZD0iZzExIj4KCQk8cGF0aAogICBkPSJtIDI2Mi4xNDMsMzM5LjA0NyBjIC0zLjQ3MSwzLjE5NSAtNi41MTYsNS41NTMgLTkuMTMzLDcuMDY4IC0yLjYxNywxLjUyIC01LjExMywyLjI3OSAtNy40ODgsMi4yNzkgLTIuNzMyLDAgLTQuOTM2LC0xLjA1OSAtNi42MDcsLTMuMTc4IC0xLjY3NCwtMi4xMjEgLTIuNTA4LC00Ljk2NSAtMi41MDgsLTguNTQzIDAsLTUuMzYxIDEuMTYyLC0xMS43OTcgMy40ODYsLTE5LjMwMSAyLjMyLC03LjUxIDUuMTQ1LC0xNC40MyA4LjQ2MywtMjAuNzYxIGwgOS43MjksLTMuNjAyIGMgMC4zMDUsLTAuMTAyIDAuNTM3LC0wLjE1NCAwLjY5MSwtMC4xNTQgMC43MzgsMCAxLjM0OCwwLjU0NCAxLjgxNiwxLjYyNyAwLjQ3MywxLjA4OCAwLjcxMSwyLjU1IDAuNzExLDQuMzg4IDAsNS4yMDkgLTEuMTk5LDEwLjI1MiAtMy42MDIsMTUuMTI5IC0yLjQwMiw0Ljg3OSAtNi4xNTQsMTAuMDg2IC0xMS4yNiwxNS42MjcgLTAuMjA1LDIuNjU2IC0wLjMwNyw0LjQ4IC0wLjMwNyw1LjQ3NyAwLDIuMjIzIDAuNDA4LDMuOTgyIDEuMjI1LDUuMjg1IDAuODE4LDEuMzA1IDEuOTAyLDEuOTUzIDMuMjU2LDEuOTUzIDEuMzgxLDAgMi44NDgsLTAuNDk0IDQuNDA2LC0xLjQ5IDEuNTU1LC0wLjk5OCAzLjkzLC0zLjA2NCA3LjEyMSwtNi4yMDcgdiA0LjQwMyB6IG0gLTE0LjY2OCwtMTQuOTczIGMgMy4yNDIsLTMuNjA1IDUuODc1LC03LjY0OCA3Ljg5MSwtMTIuMTIxIDIuMDE2LC00LjQ3NSAzLjAyMywtOC4zMjQgMy4wMjMsLTExLjU0OSAwLC0wLjk0IC0wLjEzOSwtMS43MDQgLTAuNDE4LC0yLjI3OCAtMC4yODEsLTAuNTc1IC0wLjY0MSwtMC44NjQgLTEuMDc0LC0wLjg2NCAtMC45NDEsMCAtMi4zMTYsMi4zNTIgLTQuMTE3LDcuMDU3IC0xLjgwMSw0LjcwNCAtMy41NjksMTEuMjkgLTUuMzA1LDE5Ljc1NSB6IgogICBpZD0icGF0aDEzIgogICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICBzdHlsZT0iZmlsbDojMDEwMTAxIiAvPgoJCTxwYXRoCiAgIGQ9Im0gMjkwLjc5NSwzMzkuMDQ3IGMgLTMuMjQyLDMuMTk1IC02LjE1Miw1LjU1MyAtOC43MzIsNy4wNjggLTIuNTgsMS41MiAtNS40MjQsMi4yNzkgLTguNTQxLDIuMjc5IC0zLjQ3MywwIC02LjI3NSwtMS4xMTEgLTguNDEsLTMuMzMgLTIuMTMxLC0yLjIyNSAtMy4xOTUsLTUuMTQ2IC0zLjE5NSwtOC43NzMgMCwtNS40MTIgMS44NzUsLTEwLjMwOSA1LjYzMywtMTQuNjg4IDMuNzUsLTQuMzgxIDcuOTE0LC02LjU3IDEyLjQ4NCwtNi41NyAyLjM3NSwwIDQuMjc1LDAuNjE1IDUuNzA3LDEuODQgMS40MywxLjIyNyAyLjE0NSwyLjgzNCAyLjE0NSw0LjgyNiAwLDUuMjg3IC01LjYxNyw5LjU3NCAtMTYuODUyLDEyLjg2OSAxLjAyLDQuOTc3IDMuNjg4LDcuNDY5IDguMDA0LDcuNDY5IDEuNjg2LDAgMy4yOTMsLTAuNDUzIDQuODI0LC0xLjM1NyAxLjUzNSwtMC45MDggMy44NDQsLTIuOTIyIDYuOTM0LC02LjAzNSB2IDQuNDAyIHogbSAtMjAuMDcsLTcuMDg0IGMgNi41MzUsLTEuODQgOS44MDUsLTUuMjM0IDkuODA1LC0xMC4xODggMCwtMi40NTEgLTAuODk1LC0zLjY3NiAtMi42OCwtMy42NzYgLTEuNjg2LDAgLTMuMjkzLDEuMjgxIC00LjgyNCwzLjg1IC0xLjUzNiwyLjU2NSAtMi4zMDEsNS45MDEgLTIuMzAxLDEwLjAxNCB6IgogICBpZD0icGF0aDE1IgogICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICBzdHlsZT0iZmlsbDojMDEwMTAxIiAvPgoJCTxwYXRoCiAgIGQ9Im0gMzMxLjcwMSwzMzkuMDQ3IGMgLTQuMDg2LDMuODgxIC03LjAxLDYuNDEyIC04Ljc3LDcuNTg4IC0xLjc2MiwxLjE3NCAtMy40NDcsMS43NiAtNS4wNTcsMS43NiAtNC4wMzUsMCAtNS45MzYsLTMuNTYxIC01LjcwNywtMTAuNjg2IC0yLjU1MywzLjY1IC00LjkxLDYuMzQ0IC03LjA2OCw4LjA4NCAtMi4xNTYsMS43MzYgLTQuMzgzLDIuNjAyIC02LjY4NCwyLjYwMiAtMi4yNDQsMCAtNC4xNTIsLTEuMDUxIC01LjcyNSwtMy4xNTggLTEuNTczLC0yLjEwNyAtMi4zNTQsLTQuNjkxIC0yLjM1NCwtNy43NTggMCwtMy44MjggMS4wNTEsLTcuNDggMy4xNTYsLTEwLjk1NSAyLjEwOSwtMy40NzMgNC44MDksLTYuMjc5IDguMTAyLC04LjQyNCAzLjI5MywtMi4xNDUgNi4yMDcsLTMuMjE5IDguNzMyLC0zLjIxOSAzLjE5MywwIDUuNDI4LDEuNDY5IDYuNzA1LDQuNDA0IGwgNy44MjgsLTQuMzI2IGggMi4xNDggbCAtMy4zODEsMTEuMjIxIGMgLTEuNzM2LDUuNjQ1IC0yLjYwNyw5LjUxNCAtMi42MDcsMTEuNjA3IDAsMi4xOTUgMC43NzcsMy4yOTMgMi4zMzYsMy4yOTMgMC45OTIsMCAyLjA5LC0wLjUyOSAzLjI5MSwtMS41OSAxLjIwMSwtMS4wNjEgMi44ODMsLTIuNjc2IDUuMDUzLC00Ljg0NiB2IDQuNDAzIHogbSAtMjguMDM3LDIuMTA5IGMgMi41NTMsMCA0Ljk1OSwtMi4xNzYgNy4yMjMsLTYuNTI5IDIuMjYsLTQuMzU1IDMuMzg5LC04LjM3MyAzLjM4OSwtMTIuMDQ5IDAsLTEuNDI4IC0wLjMyMiwtMi41NDcgLTAuOTU3LC0zLjM1IC0wLjY0MSwtMC44MDcgLTEuNDk2LC0xLjIwNyAtMi41NjYsLTEuMjA3IC0yLjU1NSwwIC00Ljk3NywyLjE3IC03LjI1OCw2LjUxMiAtMi4yODUsNC4zNDIgLTMuNDMsOC4zMzggLTMuNDMsMTEuOTg2IDAsMS4zODEgMC4zNCwyLjQ5OCAxLjAxNiwzLjM1NCAwLjY3NiwwLjg1NiAxLjUzNCwxLjI4MyAyLjU4MywxLjI4MyB6IgogICBpZD0icGF0aDE3IgogICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICBzdHlsZT0iZmlsbDojMDEwMTAxIiAvPgoJCTxwYXRoCiAgIGQ9Im0gMzYwLjMxNCwzMzkuMDQ3IGMgLTYuNDEsNi4yODEgLTExLjM1Miw5LjQyNCAtMTQuODI0LDkuNDI0IC0xLjU1OSwwIC0yLjg3NSwtMC42NTggLTMuOTQ1LC0xLjk2OSAtMS4wNywtMS4zMTYgLTEuNjA5LC0yLjk0NSAtMS42MDksLTQuODg3IDAsLTMuNiAxLjkzLC04LjQyNCA1Ljc4NSwtMTQuNDc3IC0xLjg5MSwwLjk3MSAtMy45NTcsMS42NDUgLTYuMjA1LDIuMDI5IC0xLjY2LDMuMDY0IC00LjI2Niw2LjM1OSAtNy44MTQsOS44NzkgaCAtMC44NzkgdiAtMy40NDMgYyAxLjk5LC0yLjA2OCAzLjc5MSwtNC4yOTEgNS40LC02LjY2NiAtMi4xOTksLTAuOTcxIC0zLjI5NSwtMi40MTQgLTMuMjk1LC00LjMyNiAwLC0xLjk2OSAwLjY2OCwtNC4wNjggMi4wMTIsLTYuMzA1IDEuMzQsLTIuMjMyIDMuMTg0LC0zLjM0OCA1LjUzNSwtMy4zNDggMS45OTIsMCAyLjk4NiwxLjAxOCAyLjk4NiwzLjA2MiAwLDEuNjA5IC0wLjU3NCwzLjkwNiAtMS43MjUsNi44OTUgNC4yMzgsLTAuNDYxIDcuOTQxLC0zLjcwMSAxMS4xMDksLTkuNzI5IGwgMy40ODQsLTAuMTU0IC0zLjU2Miw5LjgwNSBjIC0xLjQ4LDQuMTM3IC0yLjQzOCw2Ljk1NSAtMi44NzEsOC40NDcgLTAuNDMzLDEuNDkyIC0wLjY1MiwyLjgxNiAtMC42NTIsMy45NjMgMCwxLjA3NCAwLjI1LDEuOTMyIDAuNzQ2LDIuNTY2IDAuNDk4LDAuNjQzIDEuMTcsMC45NTkgMi4wMTIsMC45NTkgMC45MTgsMCAxLjgwMSwtMC4zMTQgMi42NDMsLTAuOTM2IDAuODQyLC0wLjYzMSAyLjczMiwtMi4zNTkgNS42NywtNS4xOTMgdiA0LjQwNCB6IgogICBpZD0icGF0aDE5IgogICBpbmtzY2FwZTpjb25uZWN0b3ItY3VydmF0dXJlPSIwIgogICBzdHlsZT0iZmlsbDojMDEwMTAxIiAvPgoJCTxwYXRoCiAgIGQ9Im0gMzk3LjkyOCwzMzkuMDQ3IGMgLTUuODk4LDYuMjM0IC0xMC45NTcsOS4zNDggLTE1LjE2OCw5LjM0OCAtMS43MTEsMCAtMy4wOSwtMC42IC00LjEzNywtMS44MDEgLTEuMDQ5LC0xLjE5OSAtMS41NzIsLTIuODA3IC0xLjU3MiwtNC44MjQgMCwtMi43MzIgMS4xMjUsLTYuOTA4IDMuMzczLC0xMi41MjMgMS4xOTksLTMuMDE0IDEuODAxLC00LjkzMiAxLjgwMSwtNS43NDYgMCwtMC44MTggLTAuMzIyLC0xLjIyNyAtMC45NTcsLTEuMjI3IC0wLjM1NywwIC0wLjgzMiwwLjE4IC0xLjQxOCwwLjUzNSAtMC41MzksMC4zNTcgLTEuMTY0LDAuODU5IC0xLjg3OSwxLjQ5NiAtMC42MzcsMC41ODYgLTEuMzU0LDEuMzAxIC0yLjE0NSwyLjE0MSAtMC42OTEsMC43MjEgLTEuNDMyLDEuNTM3IC0yLjIxOSwyLjQ1MyBsIC0yLjE0OCwyLjQ5MiBjIC0wLjk0MywxLjE0OCAtMS41MzEsMi4zNTkgLTEuNzYsMy42MzcgLTAuMzg1LDIuMTcgLTAuNjM5LDQuMTY0IC0wLjc2OCw1Ljk3OSAtMC4wNzgsMS4zNSAtMC4xMTUsMy4xNzQgLTAuMTE1LDUuNDc3IGwgLTguNDY1LDEuOTg4IGMgLTAuMjc5LC0zLjQ0NyAtMC40MjIsLTYuMDE0IC0wLjQyMiwtNy42OTcgMCwtNC4xMTEgMC40NzksLTguMDA2IDEuNDM4LC0xMS42ODIgMC45NTcsLTMuNjggMi40OTQsLTcuODE0IDQuNjE1LC0xMi40MTIgbCA5LjM0NCwtMS43OTkgYyAtMS45NjUsNS4yODcgLTMuMjU0LDkuNDQ3IC0zLjg2NywxMi40ODQgNC4xODgsLTQuNjcyIDcuNTA4LC03LjkwNiA5Ljk2OSwtOS43MDkgMi40NTcsLTEuODAxIDQuNjQ1LC0yLjY5NyA2LjU1NywtMi42OTcgMS4yOTksMCAyLjM4NSwwLjQ5IDMuMjUsMS40NzEgMC44NjksMC45ODIgMS4zMDEsMi4yMTUgMS4zMDEsMy42ODkgMCwyLjQ0OSAtMS4wOTgsNi40ODQgLTMuMjkxLDEyLjEwNCAtMS41MDgsMy44NTQgLTIuMjYyLDYuMzU1IC0yLjI2Miw3LjUxIDAsMS41MzcgMC42MjcsMi4zMDUgMS44ODEsMi4zMDUgMS44NjcsMCA0Ljg5MSwtMi40NjUgOS4wNjQsLTcuMzkzIHoiCiAgIGlkPSJwYXRoMjEiCiAgIGlua3NjYXBlOmNvbm5lY3Rvci1jdXJ2YXR1cmU9IjAiCiAgIHN0eWxlPSJmaWxsOiMwMTAxMDEiIC8+Cgk8L2c+CjwvZz4KCjx0ZXh0CiAgIGZvbnQtc2l6ZT0iMjMuMDc5NSIKICAgaWQ9InRleHQyNSIKICAgc3R5bGU9ImZvbnQtc2l6ZToyMy4wNzk1MDAycHg7bGluZS1oZWlnaHQ6MCU7Zm9udC1mYW1pbHk6SGVsdmV0aWNhO2ZpbGw6I2ZmZmZmZiIKICAgeD0iMTUzLjMzMjc5IgogICB5PSI4MS45NDU5MzgiPnNjaWtpdDwvdGV4dD4KCgoKCgoKPC9zdmc+)](https://mlflow.org/docs/latest/ml/traditional-ml/sklearn/)

Scikit-learn

[![XGBoost](https://mlflow.org/docs/latest/assets/images/xgboost-logo-34eb19cd705f245f4c29ca879b417b96.svg)](https://mlflow.org/docs/latest/ml/traditional-ml/xgboost/)

XGBoost

[![TensorFlow](data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDI1LjAuMSwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8c3ZnIHZlcnNpb249IjEuMCIgaWQ9ImthdG1hbl8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCIKCSB2aWV3Qm94PSIwIDAgMzM4IDIwMCIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMzM4IDIwMDsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8c3R5bGUgdHlwZT0idGV4dC9jc3MiPgoJLnN0MHtjbGlwLXBhdGg6dXJsKCNTVkdJRF8yXyk7fQoJLnN0MXtmaWxsOnVybCgjU1ZHSURfM18pO30KCS5zdDJ7Y2xpcC1wYXRoOnVybCgjU1ZHSURfNV8pO30KCS5zdDN7ZmlsbDp1cmwoI1NWR0lEXzZfKTt9Cgkuc3Q0e2ZpbGw6IzQyNTA2Njt9Cjwvc3R5bGU+CjxnPgoJPGc+CgkJPGc+CgkJCTxkZWZzPgoJCQkJPHBvbHlnb24gaWQ9IlNWR0lEXzFfIiBwb2ludHM9IjczLjUsODUuNiA1MSw3Mi44IDUxLDEyNS40IDYwLDEyMC4yIDYwLDEwNS40IDY2LjgsMTA5LjMgNjYuNyw5OS4yIDYwLDk1LjMgNjAsODkuNCA3My41LDk3LjMgCgkJCQkJCQkJCSIvPgoJCQk8L2RlZnM+CgkJCTxjbGlwUGF0aCBpZD0iU1ZHSURfMl8iPgoJCQkJPHVzZSB4bGluazpocmVmPSIjU1ZHSURfMV8iICBzdHlsZT0ib3ZlcmZsb3c6dmlzaWJsZTsiLz4KCQkJPC9jbGlwUGF0aD4KCQkJPGcgY2xhc3M9InN0MCI+CgkJCQkKCQkJCQk8bGluZWFyR3JhZGllbnQgaWQ9IlNWR0lEXzNfIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjI0LjQiIHkxPSItMjAxLjA1IiB4Mj0iNzkuNiIgeTI9Ii0yMDEuMDUiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMSAwIDAgLTEgMCAtMTAyKSI+CgkJCQkJPHN0b3AgIG9mZnNldD0iMCIgc3R5bGU9InN0b3AtY29sb3I6I0ZGNkYwMCIvPgoJCQkJCTxzdG9wICBvZmZzZXQ9IjEiIHN0eWxlPSJzdG9wLWNvbG9yOiNGRkE4MDAiLz4KCQkJCTwvbGluZWFyR3JhZGllbnQ+CgkJCQk8cGF0aCBjbGFzcz0ic3QxIiBkPSJNMjQuNCw3Mi42aDU1LjJ2NTIuOUgyNC40VjcyLjZ6Ii8+CgkJCTwvZz4KCQk8L2c+Cgk8L2c+CjwvZz4KPGc+Cgk8Zz4KCQk8Zz4KCQkJPGRlZnM+CgkJCQk8cG9seWdvbiBpZD0iU1ZHSURfNF8iIHBvaW50cz0iMjYuNSw4NS42IDQ5LDcyLjggNDksMTI1LjQgNDAsMTIwLjIgNDAsODkuNCAyNi41LDk3LjMgCQkJCSIvPgoJCQk8L2RlZnM+CgkJCTxjbGlwUGF0aCBpZD0iU1ZHSURfNV8iPgoJCQkJPHVzZSB4bGluazpocmVmPSIjU1ZHSURfNF8iICBzdHlsZT0ib3ZlcmZsb3c6dmlzaWJsZTsiLz4KCQkJPC9jbGlwUGF0aD4KCQkJPGcgY2xhc3M9InN0MiI+CgkJCQkKCQkJCQk8bGluZWFyR3JhZGllbnQgaWQ9IlNWR0lEXzZfIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjI0LjEiIHkxPSItMjAxLjA1IiB4Mj0iNzkuMyIgeTI9Ii0yMDEuMDUiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMSAwIDAgLTEgMCAtMTAyKSI+CgkJCQkJPHN0b3AgIG9mZnNldD0iMCIgc3R5bGU9InN0b3AtY29sb3I6I0ZGNkYwMCIvPgoJCQkJCTxzdG9wICBvZmZzZXQ9IjEiIHN0eWxlPSJzdG9wLWNvbG9yOiNGRkE4MDAiLz4KCQkJCTwvbGluZWFyR3JhZGllbnQ+CgkJCQk8cGF0aCBjbGFzcz0ic3QzIiBkPSJNMjQuMSw3Mi42aDU1LjJ2NTIuOUgyNC4xVjcyLjZ6Ii8+CgkJCTwvZz4KCQk8L2c+Cgk8L2c+CjwvZz4KPHBhdGggY2xhc3M9InN0NCIgZD0iTTExNC4yLDg5LjFoLTEwdjI3LjdoLTUuNlY4OS4xaC0xMHYtNC41aDI1LjZWODkuMXoiLz4KPHBhdGggY2xhc3M9InN0NCIgZD0iTTEyMC45LDExNy4yYy0zLjQsMC02LjItMS4xLTguMy0zLjJjLTIuMS0yLjEtMy4yLTUtMy4yLTguNnYtMC43YzAtMi4yLDAuNC00LjQsMS40LTYuNAoJYzAuOS0xLjgsMi4yLTMuMywzLjktNC40YzEuNy0xLjEsMy42LTEuNiw1LjYtMS42YzMuMywwLDUuOCwxLDcuNiwzLjFzMi43LDUsMi43LDguOHYyLjJoLTE1LjdjMC4xLDEuOCwwLjgsMy40LDIsNC43CgljMS4yLDEuMiwyLjcsMS44LDQuNCwxLjdjMi40LDAuMSw0LjYtMS4xLDYtM2wyLjksMi44Yy0xLDEuNC0yLjMsMi42LTMuOCwzLjNDMTI0LjYsMTE2LjksMTIyLjgsMTE3LjMsMTIwLjksMTE3LjJ6IE0xMjAuMyw5Ni43CgljLTEuNC0wLjEtMi43LDAuNS0zLjYsMS41Yy0xLDEuMi0xLjYsMi43LTEuNyw0LjNoMTAuM3YtMC40Yy0wLjEtMS44LTAuNi0zLjItMS40LTQuMUMxMjIuOSw5Ny4yLDEyMS42LDk2LjYsMTIwLjMsOTYuN3oKCSBNMTM5LjcsOTIuOGwwLjIsMi44YzEuNy0yLjEsNC4zLTMuMyw3LTMuMmM1LDAsNy41LDIuOSw3LjYsOC42djE1LjhoLTUuNHYtMTUuNWMwLTEuNS0wLjMtMi42LTEtMy40Yy0wLjctMC43LTEuNy0xLjEtMy4yLTEuMQoJYy0yLjEtMC4xLTQsMS4xLTQuOSwyLjl2MTdoLTUuNHYtMjRDMTM0LjYsOTIuNywxMzkuNyw5Mi44LDEzOS43LDkyLjh6IE0xNzEuOSwxMTAuM2MwLTAuOS0wLjQtMS43LTEuMi0yLjIKCWMtMS4yLTAuNy0yLjYtMS4xLTMuOS0xLjNjLTEuNi0wLjMtMy4xLTAuOC00LjYtMS41Yy0yLjctMS4zLTQtMy4yLTQtNS42YzAtMiwxLTQsMi42LTUuMmMxLjctMS40LDQtMi4xLDYuNi0yLjEKCWMyLjksMCw1LjIsMC43LDYuOSwyLjFjMS43LDEuMywyLjcsMy40LDIuNiw1LjVoLTUuNGMwLTEtMC40LTEuOS0xLjItMi42Yy0wLjktMC43LTEuOS0xLjEtMy4xLTFjLTEsMC0yLDAuMi0yLjksMC44CgljLTAuNywwLjUtMS4xLDEuMy0xLjEsMi4yYzAsMC44LDAuNCwxLjUsMSwxLjljMC43LDAuNSwyLjEsMC45LDQuMiwxLjRjMS43LDAuMywzLjQsMC45LDUsMS43YzEuMSwwLjUsMiwxLjMsMi43LDIuMwoJYzAuNiwxLDAuOSwyLjEsMC45LDMuM2MwLDIuMS0xLDQtMi43LDUuMmMtMS44LDEuMy00LjEsMi03LDJjLTEuOCwwLTMuNi0wLjMtNS4yLTEuMWMtMS40LTAuNi0yLjctMS42LTMuNi0yLjkKCWMtMC44LTEuMi0xLjMtMi42LTEuMy00aDUuMmMwLDEuMSwwLjUsMi4yLDEuNCwyLjljMSwwLjcsMi4zLDEuMSwzLjUsMWMxLjQsMCwyLjUtMC4zLDMuMi0wLjhDMTcxLjUsMTExLjksMTcxLjksMTExLjEsMTcxLjksMTEwLjMKCUwxNzEuOSwxMTAuM3ogTTE4MCwxMDQuNmMwLTIuMiwwLjQtNC40LDEuNC02LjNjMC45LTEuOCwyLjItMy4zLDMuOS00LjNjMS44LTEsMy44LTEuNiw1LjgtMS41YzMuMiwwLDUuOSwxLDcuOSwzLjEKCWMyLDIuMSwzLjEsNC44LDMuMyw4LjN2MS4zYzAsMi4yLTAuNCw0LjMtMS40LDYuM2MtMC44LDEuOC0yLjIsMy4zLTMuOSw0LjNjLTEuOCwxLTMuOCwxLjYtNS45LDEuNWMtMy40LDAtNi4xLTEuMS04LjEtMy40CgljLTItMi4yLTMtNS4yLTMuMS05TDE4MCwxMDQuNnogTTE4NS4zLDEwNS4xYzAsMi41LDAuNSw0LjQsMS41LDUuOGMxLjgsMi4zLDUuMSwyLjgsNy41LDFjMC40LTAuMywwLjctMC42LDEtMQoJYzEtMS40LDEuNS0zLjUsMS41LTYuMmMwLTIuNC0wLjUtNC4zLTEuNi01LjhjLTEuNy0yLjMtNS0yLjgtNy40LTEuMWMtMC40LDAuMy0wLjgsMC43LTEuMSwxQzE4NS45LDEwMC4yLDE4NS4zLDEwMi4zLDE4NS4zLDEwNS4xegoJIE0yMTguNCw5Ny44Yy0wLjctMC4xLTEuNS0wLjItMi4yLTAuMmMtMi41LDAtNC4xLDAuOS01LDIuOHYxNi40aC01LjR2LTI0aDUuMWwwLjEsMi43YzEuMy0yLjEsMy4xLTMuMSw1LjQtMy4xCgljMC42LDAsMS4zLDAuMSwxLjksMC4zTDIxOC40LDk3LjhMMjE4LjQsOTcuOHogTTI0MC45LDEwMy4xaC0xM3YxMy43aC01LjZWODQuNmgyMC41djQuNWgtMTQuOXY5LjZoMTNWMTAzLjF6IE0yNTEuNiwxMTYuOGgtNS40CglWODQuNWg1LjRDMjUxLjYsODQuNSwyNTEuNiwxMTYuOCwyNTEuNiwxMTYuOHogTTI1NS41LDEwNC42YzAtMi4yLDAuNC00LjQsMS40LTYuM2MwLjktMS44LDIuMi0zLjMsMy45LTQuM2MxLjgtMSwzLjgtMS42LDUuOC0xLjUKCWMzLjIsMCw1LjksMSw3LjksMy4xYzIsMi4xLDMuMSw0LjgsMy4zLDguM3YxLjNjMCwyLjItMC40LDQuMy0xLjMsNi4zYy0wLjgsMS44LTIuMiwzLjMtMy45LDQuM2MtMS44LDEtMy44LDEuNi01LjksMS41CgljLTMuNCwwLTYuMS0xLjEtOC4xLTMuNGMtMi0yLjItMy4xLTUuMi0zLjEtOUwyNTUuNSwxMDQuNkwyNTUuNSwxMDQuNnogTTI2MC45LDEwNS4xYzAsMi41LDAuNSw0LjQsMS41LDUuOHMyLjYsMi4yLDQuMywyLjEKCWMxLjcsMC4xLDMuMy0wLjcsNC4yLTIuMWMxLTEuNCwxLjUtMy41LDEuNS02LjJjMC0yLjQtMC41LTQuMy0xLjYtNS44Yy0xLjctMi4zLTUtMi44LTcuNC0xLjFjLTAuNCwwLjMtMC44LDAuNy0xLjEsMQoJQzI2MS40LDEwMC4yLDI2MC45LDEwMi4zLDI2MC45LDEwNS4xeiBNMzAyLjEsMTA5LjRsMy44LTE2LjVoNS4ybC02LjUsMjRoLTQuNGwtNS4xLTE2LjVsLTUuMSwxNi41aC00LjRsLTYuNi0yNGg1LjNsMy45LDE2LjQKCWw0LjktMTYuNGg0LjFMMzAyLjEsMTA5LjRMMzAyLjEsMTA5LjR6Ii8+Cjwvc3ZnPgo=)](https://mlflow.org/docs/latest/ml/deep-learning/tensorflow/)

TensorFlow

[![PyTorch](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAiIGhlaWdodD0iNjAiPjxnIHRyYW5zZm9ybT0ibWF0cml4KDEuMjE2NjAxIDAgMCAxLjIxNjYwMSAtMTcuMjc3MTQ5IDExLjQzMTYyMikiIGZpbGw9IiNlZTRjMmMiPjxwYXRoIGQ9Ik00MC44IDkuM2wtMi4xIDIuMWMzLjUgMy41IDMuNSA5LjIgMCAxMi43cy05LjIgMy41LTEyLjcgMC0zLjUtOS4yIDAtMTIuN2w1LjYtNS42LjctLjhWLjhsLTguNSA4LjVhMTEuODkgMTEuODkgMCAwIDAgMCAxNi45IDExLjg5IDExLjg5IDAgMCAwIDE2LjkgMGM0LjgtNC43IDQuOC0xMi4zLjEtMTYuOXoiLz48Y2lyY2xlIGN4PSIzNi42IiBjeT0iNy4xIiByPSIxLjYiLz48L2c+PHBhdGggZD0iTTQ4LjAwOCAzMi4wMjhoLTJ2NS4xNDRoLTEuNDkzVjIyLjU3aDMuNjVjMy44NzIgMCA1LjY5NyAxLjg4IDUuNjk3IDQuNiAwIDMuMjA4LTIuMjY4IDQuODEyLTUuODYzIDQuODY3em0uMS04LjA3NUg0NS45NnY2LjY5M2wyLjEwMi0uMDU1YzIuNzY2LS4wNTUgNC4yNi0xLjE2MiA0LjI2LTMuNDMgMC0yLjA0Ni0xLjQzOC0zLjIwOC00LjIwNC0zLjIwOHpNNjAuNjIgMzcuMTE2bC0uODg1IDIuMzIzYy0uOTk2IDIuNi0yIDMuMzc0LTMuNDg1IDMuMzc0LS44MyAwLTEuNDM4LS4yMi0yLjEwMi0uNDk4bC40NDItMS4zMjdjLjQ5OC4yNzcgMS4wNS40NDIgMS42Ni40NDIuODMgMCAxLjQzOC0uNDQyIDIuMjEyLTIuNWwuNzItMS44OC00LjE0OC0xMC41NjRoMS41NWwzLjM3NCA4Ljg1IDMuMzItOC44NWgxLjQ5M3ptOS4xMjUtMTMuMTA4djEzLjIyaC0xLjQ5M3YtMTMuMjJoLTUuMTQ0VjIyLjU3aDExLjc4djEuMzgzaC01LjE0NHptOS4zNDcgMTMuNDk1Yy0yLjk4NyAwLTUuMi0yLjIxMi01LjItNS42NDJzMi4yNjgtNS42OTcgNS4zLTUuNjk3YzIuOTg3IDAgNS4xNDQgMi4yMTIgNS4xNDQgNS42NDJzLTIuMjY4IDUuNjk3LTUuMjU1IDUuNjk3em0uMDU1LTEwYy0yLjI2OCAwLTMuNzYgMS44MjUtMy43NiA0LjMxNCAwIDIuNiAxLjU1IDQuMzcgMy44MTYgNC4zN3MzLjc2LTEuODI1IDMuNzYtNC4zMTRjMC0yLjYtMS41NS00LjM3LTMuODE2LTQuMzd6bTguOTA2IDkuNzI0aC0xLjQzOHYtMTAuNzNsMS40MzgtLjI3N3YyLjI2OGMuNzItMS4zODMgMS43Ny0yLjI2OCAzLjE1My0yLjI2OGEzLjkyIDMuOTIgMCAwIDEgMS44OC40OThMOTIuNyAyOC4xYy0uNDQyLS4yNzctMS4wNS0uNDQyLTEuNjYtLjQ0Mi0xLjEwNiAwLTIuMTU3LjgzLTMuMDQyIDIuNzY2djYuODAzem0xMC43My4yNzZjLTMuMjA4IDAtNS4yNTUtMi4zMjMtNS4yNTUtNS42NDIgMC0zLjM3NCAyLjIxMi01LjY5NyA1LjI1NS01LjY5NyAxLjMyNyAwIDIuNDM0LjMzMiAzLjM3NC45NGwtLjM4NyAxLjMyN2MtLjgzLS41NTMtMS44MjUtLjg4NS0yLjk4Ny0uODg1LTIuMzIzIDAtMy43NiAxLjcxNS0zLjc2IDQuMjYgMCAyLjYgMS41NSA0LjMxNCAzLjgxNiA0LjMxNGE1LjU3IDUuNTcgMCAwIDAgMi45ODctLjg4NWwuMjc3IDEuMzI3Yy0uOTQuNjA4LTIuMTAyLjk0LTMuMzIuOTR6bTEyLjMzNC0uMjc2di02LjkxNGMwLTEuODgtLjc3NC0yLjctMi4yNjgtMi43LTEuMjE3IDAtMi40MzQuNjA4LTMuMzIgMS41NXY4LjEzaC0xLjQzOHYtMTUuODJsMS40MzgtLjI3N3Y2Ljc0OGMxLjEwNi0xLjEwNiAyLjU0NC0xLjcxNSAzLjcwNi0xLjcxNSAyLjEwMiAwIDMuMzc0IDEuMzI3IDMuMzc0IDMuNjV2Ny4zNTZ6IiBmaWxsPSIjMjUyNTI1Ii8+PC9zdmc+)](https://mlflow.org/docs/latest/ml/deep-learning/pytorch/)

PyTorch

[![Keras](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNjQuNjY1MDcgMzY0LjY2NTA3IiBoZWlnaHQ9IjM4OC45NzYiIHdpZHRoPSIzODguOTc2Ij48cGF0aCBmaWxsPSIjZDAwMDAwIiBkPSJNMCAwaDM2NC42NjV2MzY0LjY2NUgweiIvPjxwYXRoIGQ9Ik0xMzUuNTkyIDI4MS40OHYtNjcuN2wyNy40OS0yNy40MDQgNjguOTYzIDEwMS45MSAzMS41ODcuMjQ4IDUuODMyLTExLjkwNS04MC4yNDgtMTE2LjQxNSA3My44NzYtNzUuMTA4LTQuMDktMTEuOTA5SDIyNy40OGwtOTEuODg4IDkxLjg2M1Y4MC4yMWwtNi43MTctNy4wMTNIMTA2LjA2bC02LjcxOCA3LjAxMnYyMDAuOTc2bDcuMDc1IDcuMTkgMjEuOTg1LS4wODh6IiBmaWxsPSIjZmZmIi8+PC9zdmc+)](https://mlflow.org/docs/latest/ml/deep-learning/keras/)

Keras

[![Spark MLlib](data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjIwMS44NTAwMSIgdmlld0JveD0iMCAwIDM4OC4xMTI0OSAyMDEuODUwMDEiIHdpZHRoPSIzODguMTEyNDkiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgdHJhbnNmb3JtPSJtYXRyaXgoLjEyNSAwIDAgLS4xMjUgMCAyMDEuODUpIj48cGF0aCBkPSJtMjg0MC4yMiA4MDAuMDc4Yy0yLjY4IDUuNzIzLTMuODkgOC42MS01LjM1IDExLjM3OS0zOC45IDczLjk1Ny03Ny43MSAxNDcuOTY5LTExNi45NiAyMjEuNzQzLTMuOTYgNy40MS0zLjQ3IDExLjgyIDEuOTUgMTguMTUgNjEuODcgNzIuMjggMTIzLjQyIDE0NC44NSAxODUuMDQgMjE3LjM1IDIuMTYgMi41NCA0LjExIDUuMjYgNC45NCA5Ljc4LTE4LjAyLTQuNzEtMzYuMDQtOS4zNi01NC4wNC0xNC4xMy03NC43Ni0xOS44MS0xNDkuNTQtMzkuNTYtMjI0LjIzLTU5LjY0LTYuOTctMS44Ny0xMC4xMy4xNy0xMy41OSA1Ljk0LTQyLjQ1IDcwLjkxLTg1LjE0IDE0MS42Ny0xMjcuNzggMjEyLjQ2LTIuMjEgMy42OC00LjU4IDcuMjUtOS4yNyAxMC4zNC0zLjQzLTE4Ljg5LTYuOTItMzcuNzctMTAuMjgtNTYuNjctMTEuODgtNjYuNzItMjMuNzItMTMzLjQ2LTM1LjU2LTIwMC4xOS0xLjI5LTcuMi0zLjA3LTE0LjM3LTMuNjgtMjEuNjMtLjYtNi44OS00LjEzLTkuNDMtMTAuMzYtMTEuMzktODguMTEtMjcuNjYtMTc2LjEzLTU1LjU5LTI2NC4xNS04My40OS0zLjg3LTEuMjItNy42NC0yLjgtMTEuNzktNi41NyA3Mi4wMS0yOC42MiAxNDQuMDItNTcuMjM3IDIxNy4xNC04Ni4yOTUtMi42Ni0yLjExMy00LjM5LTMuNzM4LTYuMzQtNS4wMDgtNDUuMDItMjkuMTI5LTkwLjExLTU4LjE0MS0xMzUuMDItODcuNDIyLTUuMzctMy41LTkuNjQtMy45OTYtMTUuNjgtMS4yNzctNTMuNzcgMjQuMjE1LTEwNy43NSA0Ny45NzItMTYxLjYgNzIuMDIzLTI0LjE4IDEwLjc5Ny00NS45MyAyNS4xNDEtNjIuODcgNDUuODU2LTM4LjI5IDQ2Ljg0My0zMC43MyAxMDAuMTMzIDIwLjI5IDEzMi42ODMgMTYuNyAxMC42NSAzNS42NSAxOC42NCA1NC41NiAyNC44MSA4Ni4yOSAyOC4xMSAxNzIuOTEgNTUuMjIgMjU5LjQ5IDgyLjQyIDcuMjUgMi4yNyAxMC42MiA1LjUyIDExLjk3IDEzLjM4IDExLjUzIDY2Ljc5IDIzLjUgMTMzLjUxIDM1LjUzIDIwMC4yIDYuNDQgMzUuNjYgOS44NiA3Mi4yNCAyNy4yMiAxMDQuOTIgNi42NiAxMi41NiAxNC42NSAyNC44NyAyNC4xNSAzNS40IDM0LjM2IDM4LjE0IDgyLjMzIDM5LjYyIDExOC42NyAzLjI4IDEyLjI2LTEyLjI2IDIyLjgxLTI2LjczIDMxLjkyLTQxLjU3IDQwLjA0LTY1LjI3IDc5LjQyLTEzMC45NiAxMTguNTktMTk2Ljc2IDQuNjMtNy43OCA4LjgxLTkuMzUgMTcuMzgtNy4wNSA5Ni41NCAyNS44OCAxOTMuMTggNTEuMzYgMjg5LjgyIDc2Ljg5IDE5LjkzIDUuMjYgNDAuMDkgNy4yIDYwLjU1IDMuMzcgNDQuNTQtOC4zNCA2NC4wMS00Mi4yNSA0OC45NC04NS4yNy02Ljg2LTE5LjYxLTE4LjY5LTM2LjE2LTMyLTUxLjgtNjcuNDMtNzkuMy0xMzQuNzUtMTU4LjY5LTIwMi40MS0yMzcuNzktNS41My02LjQ2LTUuNjUtMTEuMTQtMS44Mi0xOC4zNiA0MC4zNi03Ni4wNzcgODAuMzctMTUyLjMzOSAxMjAuNTMtMjI4LjUyNyA5LjYxLTE4LjI0MiAxNi45NC0zNy4xNiAxNy4xNi01OC4xMDEuNDgtNDcuNjI5LTM0LjM1LTg2LjYwNi04MS42OC05My41NDMtMjYuNTEtMy44OTUtNTEuMTQgMS43NjktNzUuOTggOS40NDEtNjAuNTMgMTguNzExLTEyMS4xNyAzNy4xMS0xODEuODQgNTUuMzU2LTUuNjIgMS42ODMtNy43NyAzLjg4Mi04Ljc2IDkuOTQxLTYuOTggNDIuNjk1LTE0LjU5IDg1LjI5Ny0yMS45NSAxMjcuOTM0LS4yMSAxLjE3Mi4xNCAyLjQzNy4zMiA1LjA0NyA2OS4wNy0xOS4wNTUgMTM3LjU0LTM3Ljk0MiAyMDguODMtNTcuNjEiIGZpbGw9IiNlMjVhMWMiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxnIGZpbGw9IiMzYzNhM2UiPjxwYXRoIGQ9Im0yNzIyLjIgMTc4LjIzYy01NC41OS4wOTgtMTA5LjE4LjM0OC0xNjMuNzguMTI5LTcuMi0uMDE5LTExLjI5IDIuMDgyLTE1LjMxIDguMjExLTY0LjYzIDk4LjQ0Mi0xMjkuNTUgMTk2LjY5Mi0xOTQuNDIgMjk0Ljk4MS0yLjA3IDMuMTI5LTQuMjcgNi4xNDgtNy45NCAxMS40MS0xMy45Ny0xMDYuMTYtMjcuNjItMjA5Ljk0OS00MS4zLTMxNC00Ny43NyAwLTk0LjU5IDAtMTQyLjk2IDAgMS42NyAxMy45MyAzLjE0IDI3LjM5MSA0LjkgNDAuODAxIDEzLjk2IDEwNi41OSAyNy45NyAyMTMuMTc5IDQxLjk4IDMxOS43NTggMTMuMzggMTAxLjgzOSAyNi43MiAyMDMuNjc5IDQwLjMgMzA1LjUuNCAzLjAzOSAyLjQyIDYuODc1IDQuOSA4LjQ4OCA0OS4xOSAzMi4wNzQgOTguNTUgNjMuODcxIDE0Ny45MSA5NS42OTEuNzIuNDY5IDEuNzIuNTI0IDQuMjcgMS4yNDYtMTQuOTMtMTEzLjg3MS0yOS43NS0yMjYuODUxLTQ0LjU3LTMzOS44MzYuNTktLjM5OCAxLjE3LS44IDEuNzYtMS4yMTEgNzcuNDQgODUuODQ0IDE1NC44OSAxNzEuNjg4IDIzNCAyNTkuMzcyIDIuMjktMTMuMiA0LjI3LTI0LjQ5NyA2LjIxLTM1LjgwMSA1LjU1LTMyLjM2NyAxMC44Ny02NC43ODEgMTYuODEtOTcuMDgyIDEuMi02LjUwOC0uNTMtMTAuNTU5LTQuODctMTUuMDg2LTUwLjA4LTUyLjQxLTk5Ljk3LTEwNS0xNDkuOS0xNTcuNTM5LTIuMTgtMi4yOTMtNC4yNy00LjY3Mi02Ljc1LTcuMzkxIDEuNTktMi41NTEgMi45NS01IDQuNTYtNy4yNjkgODYuMTMtMTIwLjg5MSAxNzIuMjYtMjQxLjc2MiAyNTguNDYtMzYyLjYwMiAxLjU2LTIuMTkxIDMuODEtMy45MSA1Ljc0LTUuODUyIDAtLjYzNiAwLTEuMjc3IDAtMS45MTgiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Im0xMDI3LjY0IDQ5Mi40ODhjLTIuMTggMTEuMTQxLTMuNzQgMjcuNS04LjY5IDQyLjc4Mi0yMy45MzggNzMuODcxLTk5LjczNSAxMTQuMzc4LTE3OC4xODggOTYuMTE3LTg2LjA2My0yMC4wMjgtMTQ3LjU2Ny04Ny42ODgtMTU2LjQ2NS0xNzUuNTA4LTYuNTg2LTY0Ljk1NyAyOC4zOTQtMTI3LjUzOSA5My40MzMtMTUxLjAyNyA1Mi4zOTktMTguOTMgMTAyLjg0OC0xMS4wMTIgMTQ5LjY4OCAxNy4wNzggNjIuMDg2IDM3LjI1IDk1Ljc2MiA5Mi41NSAxMDAuMjIyIDE3MC41NTh6bS0zNzcuOTM3LTI3NC41NjZjLTQuMjQ2LTMxLjc4MS04LjI5Ny02MS43MzEtMTIuMjM4LTkxLjcwMy01LjIzNS0zOS44NDAxLTEwLjQ1Ny03OS42ODc3LTE1LjQ3My0xMTkuNTQ3MTItLjU4Ni00LjY1MjM1LTEuOTk2LTYuNzAzMTMtNi45OTItNi42NzE4OC0zOS4yNy4xNjAxNTYtNzguNTM5LjEyMTA5NC0xMTcuODA1LjE3OTY4OC0uODk0IDAtMS43ODkuNDkyMTg3LTMuOTE4IDEuMDg5ODQyIDIuMzc1IDE4LjgwODU3IDQuNjg0IDM3LjY3MTg3IDcuMTUzIDU2LjUxOTU3IDguNjY0IDY2LjA4MTkgMTcuMzA4IDEzMi4xNzE5IDI2LjEwMSAxOTguMjQxOSAxMC4wNTUgNzUuNTQ3IDE4LjAyIDE1MS40NTcgMzAuODk1IDIyNi41MiAyMi44MDQgMTMyLjkxNCAxMzUuNTYyIDI0Ny40NTcgMjY3Ljg3OSAyNzUuOTc2IDc2LjcxMSAxNi41NDcgMTUwLjEyNSA4Ljg5MSAyMTcuMDk1LTM0LjI3MyA2Ni43OS00My4wNDcgMTA1LjEtMTA1LjUxNiAxMTMuODMtMTg0LjA5NCAxMi4zNS0xMTEuMTAxLTI4LjU0LTIwMy4zMzItMTA3LjQ2LTI3OS42MjktNTEuNzkzLTUwLjA5LTExMy44MDUtODEuOTIyLTE4NS4zMzItOTIuNjc5LTczLjY4NC0xMS4xMTQtMTQyLjk0NiAxLjE3OS0yMDUuMTAyIDQ0LjYxNy0yLjI4NSAxLjU5LTQuNzIzIDIuOTgtOC42MzMgNS40NTMiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Im01ODUuNzExIDg0OS41MTJjLTQ0LjAzOS0zMi43ODUtODYuNDk2LTY0LjM4Ny0xMjkuMTM3LTk2LjEyOS02Ljg3MSAxMC44NDQtMTMuMDI3IDIxLjY0NC0yMC4yMTUgMzEuNjk1LTE4LjUgMjUuODUyLTQxLjQ3NiA0NS4xNjgtNzQuODk0IDQ3LjUxMi0yNy43OTMgMS45NDktNTEuNTYzLTcuMjA3LTcwLjQ4MS0yNy42OTktMTYuOTIxLTE4LjMyNS0xOS4xMzItNDQuMzc5LTMuMzItNjUuMDc1IDE3LjQwNi0yMi43ODEgMzYuNDU3LTQ0LjM5NCA1NS45MS02NS40ODQgMzIuMjQ2LTM0Ljk2MSA2NS45NTMtNjguNTgyIDk3Ljk5Mi0xMDMuNzMgMjkuMTUzLTMxLjk3MyA1Mi4zOTEtNjcuODUyIDU5LjU2Ny0xMTEuNTcxIDguNTM1LTUxLjk3Mi0xLjgzMi0xMDEuNDcyLTI2LjQxOC0xNDcuMTUyLTQ1LjQ5Ni04NC41MjctMTE3LjE0MS0xMzMuNTctMjExLjcyMy0xNDguOTE4LTQxLjc2OS02Ljc3LTgzLjQyNi01LjQyMi0xMjQuMTgzIDYuNTc4LTU0LjA5MDIgMTUuOTIyLTkxLjczODcgNTEuMzcxLTExNS45NDk2IDEwMS40My04LjU1NDcgMTcuNjk5LTE1LjA5NzY4IDM2LjM3MS0yMi44NTk0IDU1LjM0IDQ3LjM1NTUgMjUuMzM5IDkzLjM1NTUgNDkuOTYxIDE0MC4wMzEgNzQuOTQxIDEuNjI5LTMuODkxIDIuNzY2LTcuMTI5IDQuMjg1LTEwLjE2IDcuOTU3LTE1LjkzIDE0LjQ3My0zMi44NTIgMjQuMzMyLTQ3LjUxMiAyOS4yMzUtNDMuNDY5IDc2LjQ1Ny01Ni42OTkgMTI0LjM2NC0zNS4yMDcgMTIuMzA0IDUuNTIgMjQuMTU2IDEzLjMwOSAzNC4yNSAyMi4yNTggMzAuODcxIDI3LjQwMiAzNi42NiA2NS41NTEgMTMuODA4IDEwMC4wMzEtMTMuMTI5IDE5LjgwOS0yOS41NSAzNy41Ny00NS41MzUgNTUuMzItMzguMjAzIDQyLjQzLTc3Ljk2MSA4My41LTExNS4yODEgMTI2LjY5Mi0yNS43MjcgMjkuNzY5LTQzLjIwNyA2NC40ODgtNDguNzM4IDEwNC4zNjMtNi4wNDMgNDMuNTM1IDIuNjY0IDg0LjYxNyAyNS4zMiAxMjEuMjcgNTYuMzI0IDkxLjEwNSAxMzguMTcyIDEzOC41IDI0Ni40MyAxMzQuNTc0IDYxLjcxOC0yLjIzOCAxMTAuODYzLTMxLjA5OCAxNDkuMDExLTc5LjA1MSAxMS4yODktMTQuMTgzIDIxLjg2OC0yOC45MzMgMzMuNDM0LTQ0LjMxNiIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0ibTE2MzEuNDQgMzYwLjM5OGMtNy4xOC01NC44NzgtMTMuOTUtMTA3LjAzOS0yMC45OS0xNTkuMTYtLjM2LTIuNjM2LTIuNDMtNi4yMjYtNC42OC03LjI3Ny0xMDYuNTYtNDkuMzUyLTI0Ni44OC00Mi40NjEtMzM0LjM5IDU2LjkxOC00Ny4wMiA1My4zOTEtNjYuNzUgMTE2Ljc2Mi02My44IDE4Ny4yNjIgNi44MiAxNjMuMTk5IDE0Mi4xMyAzMDUuNjY4IDMwMy45NCAzMjUuNTc0IDk0LjU0IDExLjYzMyAxNzcuNDUtMTMuOTAyIDI0MS41LTg3LjM0IDQzLjYyLTUwLjAzMSA2My44LTEwOS43NzMgNjAuODItMTc1LjcwMy0xLjk2LTQzLjU1MS04Ljc5LTg2LjkxLTE0LjIxLTEzMC4yNjItNy42OC02MS4zOTgtMTYuMDctMTIyLjcxOS0yNC4xOC0xODQuMDctLjI5LTIuMTgtLjczLTQuMzQtMS4yMi03LjExLTQyLjE5IDAtODQuMTMgMC0xMjcuNDggMCAxLjcgMTQuMDk4IDMuMjUgMjcuODk5IDUuMDQgNDEuNjY4IDkuMjMgNzAuODY0IDE5LjM4IDE0MS42MTQgMjcuNDcgMjEyLjYwMiA1LjA0IDQ0LjIxMSAxLjg3IDg4LjA5LTE4LjM1IDEyOS4wMzktMjEuNTEgNDMuNTItNTcuNTcgNjYuNTM5LTEwNSA3MS41Ny05OC4xNiAxMC4zOTEtMTkxLjU1LTU3LjgyLTIxMi40OS0xNTQuNDE4LTEzLjgzLTYzLjc2OSA3Ljk3LTEyNC44OSA1OC43NS0xNTguNjc5IDQ5LjUtMzIuOTM0IDEwMi41MS0zMy4wNDMgMTU2LjQ1LTExLjY4NCAyNy4zNSAxMC44MiA1MC42NSAyNy45NTMgNzIuODIgNTEuMDciIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Im0yMTY4LjIzIDc1MS4zMjRjLTUuODItNDQuMTk5LTExLjU1LTg3LjczOC0xNy40MS0xMzIuMTc5LTI2Ljk1IDAtNTMuMzguMTU2LTc5LjgtLjA1NS0yMS40MS0uMTY4LTQwLjk1LTEzLjk4OC00Ny4zOC0zMy45ODEtMi41Mi03LjgyLTMuNDUtMTYuMTg3LTQuNTMtMjQuMzktMTMuNDEtMTAxLjQ4OS0yNi43Mi0yMDIuOTgxLTQwLjAzLTMwNC40ODEtMy4zNi0yNS41OS02LjYzLTUxLjE5OS05Ljk5LTc3LjE3OS00NC4yMiAwLTg3LjgxIDAtMTMyLjY5IDAgMi40OCAxOS41MTkgNC44MiAzOC40MDIgNy4yOSA1Ny4yNjEgOC42MyA2NS43ODIgMTcuMjYgMTMxLjUzOSAyNiAxOTcuMjg5IDcuNTUgNTYuOTAzIDE0LjI4IDExMy45MyAyMy4xNyAxNzAuNjIxIDExLjkyIDc1Ljk5NyA4Ny41MyAxNDMuNDg1IDE2NC4yMiAxNDYuODIxIDM2LjU5IDEuNTkgNzMuMzEuMjczIDExMS4xNS4yNzMiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Im0yODc4LjYzIDE3OS4wNTl2NTYuMDExaC0uMzJsLTIxLjk4LTU2LjAxMWgtNy4wMWwtMjEuOTggNTYuMDExaC0uMzN2LTU2LjAxMWgtMTEuMDd2NjcuMDg5aDE3LjA5bDIwLjAzLTUwLjk2OCAxOS43MSA1MC45NjhoMTYuOTR2LTY3LjA4OXptLTk3LjM4IDU4LjEyMXYtNTguMTIxaC0xMS4wN3Y1OC4xMjFoLTIxLjAxdjguOTY4aDUzLjA5di04Ljk2OHoiLz48cGF0aCBkPSJtNzYzLjQ1NyA5NDMuNzE5aDMyLjg5OGwtNy43NTcgNDkuODA4em0zOC4wNjMtMzIuMThoLTU0LjczNWwtMTcuMzg3LTM0LjA1OWgtMzguNzYxbDg1LjUgMTU5LjczaDM3LjM2N2wyOS4xMTMtMTU5LjczaC0zNS45MzN6Ii8+PHBhdGggZD0ibTk5Ny4zNTIgMTAwNS4wNGgtMTkuNWwtNi41NjMtMzYuODc2aDE5LjQ4NGMxMS43NTcgMCAyMS4xNTcgNy43MzggMjEuMTU3IDIyLjMxMyAwIDkuNjMzLTUuODkgMTQuNTYzLTE0LjU3OCAxNC41NjN6bS00Ny4yMTUgMzIuMTdoNTEuMjIzYzI2Ljc4IDAgNDUuNTYtMTUuOTcgNDUuNTYtNDMuNDQ0IDAtMzQuNTM2LTI0LjQzLTU3Ljc4Mi01OS4xOTctNTcuNzgyaC0yMi4wNzVsLTEwLjM0Ny01OC41MDRoLTMzLjM0eiIvPjxwYXRoIGQ9Im0xMTYwLjIyIDk0My43MTloMzIuOWwtNy43NiA0OS44MDh6bTM4LjA2LTMyLjE4aC01NC43M2wtMTcuMzktMzQuMDU5aC0zOC43Nmw4NS41IDE1OS43M2gzNy4zNmwyOS4xMi0xNTkuNzNoLTM1LjkzeiIvPjxwYXRoIGQ9Im0xNDE0LjY3IDg4My4xMjVjLTExLjI3LTUuMTY0LTIzLjcxLTguMjM0LTM2LjE3LTguMjM0LTQyLjI3IDAtNjguODMgMzEuNzIyLTY4LjgzIDcxLjQyMiAwIDUwLjc0NiA0Mi43NSA5My40OTcgOTMuNSA5My40OTcgMTIuNjggMCAyNC4yLTMuMDUgMzMuNTktOC4yMmwtNC43LTM4LjMwMWMtNy4wNCA3Ljc2MS0xOC4zMyAxMy4xNjEtMzIuNDIgMTMuMTYxLTI5LjEyIDAtNTQuOTYtMjYuMzIxLTU0Ljk2LTU2Ljg0OCAwLTIzLjI1IDE0LjU2LTQxLjM1NiAzNy41OS00MS4zNTYgMTQuMSAwIDI3LjcxIDUuNDA2IDM2Ljg3IDEyLjkyMnoiLz48cGF0aCBkPSJtMTYxOC41MiA5NDEuODQ4aC02OS41M2wtMTEuMjktNjQuMzY4aC0zMy4zNGwyOC4xOCAxNTkuNzNoMzMuMzZsLTExLjI3LTYzLjE4M2g2OS41M2wxMS4yNiA2My4xODNoMzMuMzZsLTI4LjE3LTE1OS43M2gtMzMuMzZ6Ii8+PHBhdGggZD0ibTE3NDAuODUgODc3LjQ4IDI4LjE3IDE1OS43M2g4OC41N2wtNS42NC0zMi4xN2gtNTUuMjFsLTUuNjItMzEuMDEzaDUwLjcybC01LjYyLTMyLjE3OWgtNTAuNzVsLTUuNjQtMzIuMTg0aDU1LjIxbC01LjY0LTMyLjE4NHoiLz48L2c+PC9nPjwvc3ZnPg==)](https://mlflow.org/docs/latest/ml/traditional-ml/sparkml/)

Spark MLlib

### Evaluate and validate your ML models[​](#evaluate-and-validate-your-ml-models)

#### Core Features[​](#core-features-3)

**MLflow Evaluation** provides comprehensive model validation tools, automated metrics calculation, and model comparison capabilities.

**Key Benefits:**

- **Automated Metrics**: Built-in evaluation metrics for classification, regression, and - mo
- **Custom Evaluators**: Create custom evaluation functions for domain-specific metrics
- **Model Comparison**: Compare multiple models and versions side-by-side
- **Validation Datasets**: Track evaluation datasets and ensure reproducible results

#### Guides[​](#guides-3)

Learn how to [evaluate your ML models](https://mlflow.org/docs/latest/ml/evaluation/) with MLflow

Discover [custom evaluation metrics](https://mlflow.org/docs/latest/ml/evaluation/metrics-visualizations/) and functions

Compare models with [MLflow Model Comparison](https://mlflow.org/docs/latest/ml/evaluation/model-eval/)

![MLflow Evaluation](https://mlflow.org/docs/latest/assets/images/evaluate_metrics-bee252801c0dd3bc77ff472f8e7d4a48.png)


## Running MLflow Anywhere[​](#running-mlflow-anywhere)


MLflow can be used in a variety of environments, including your local environment, on-premises clusters, cloud platforms, and managed services. Being an open-source platform, MLflow is **vendor-neutral**; no matter where you are doing machine learning, you have access to the MLflow's core capabilities sets such as tracking, evaluation, observability, and more.


[![Databricks Logo](https://mlflow.org/docs/latest/assets/images/databricks-logo-0d41838793b124a124f8a8a4cc86c7d2.png)](https://docs.databricks.com/aws/en/mlflow3/genai/)[![Amazon SageMaker Logo](data:image/png;base64,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)](https://aws.amazon.com/sagemaker-ai/experiments/)[![Azure Machine Learning Logo](https://mlflow.org/docs/latest/assets/images/azure-ml-logo-92b5684b6330ac456815e6dc3233bbd8.png)](https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow?view=azureml-api-2)[![Nebius Logo](data:image/png;base64,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)](https://nebius.com/services/managed-mlflow)[![Kubernetes Logo](https://mlflow.org/docs/latest/assets/images/kubernetes-logo-0728374966fe59ee08e213e966513d00.png)](https://mlflow.org/docs/latest/ml/tracking/)

---

## MLflow for GenAI | MLflow
<a id="MLflow-for-GenAI-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/genai/

Build with MLflow GenAI

On this page# Build with MLflow GenAI

Learn how to get started with MLflow for building production-ready GenAI applications.

![MLflow GenAI Platform](https://mlflow.org/docs/latest/assets/images/mlflow-3-trace-ui-be096b13c40e7433a7cc3ae46e9b861c.png)
[### Get Started

Build your first GenAI app with MLflow

Start building →](https://mlflow.org/docs/latest/genai/getting-started/)[### Environment Setup

Install and configure MLflow

Setup guide →](https://mlflow.org/docs/latest/genai/getting-started/connect-environment/)[### API Reference

Complete API documentation

Browse APIs →](https://mlflow.org/docs/latest/api_reference/index.html)[### Tracing & Debug

Observe AI application flows

Start tracing →](https://mlflow.org/docs/latest/genai/tracing/)[### Evaluation

Test and improve AI quality

Evaluate apps →](https://mlflow.org/docs/latest/genai/eval-monitor/)[### Prompt Engineering

Design and version prompts

Engineer prompts →](https://mlflow.org/docs/latest/genai/prompt-registry/)[### Deploy & Serve

Production deployment guide

Deploy apps →](https://mlflow.org/docs/latest/genai/serving/)[### AI Gateway

Unified API for AI providers

Learn more →](https://mlflow.org/docs/latest/genai/governance/ai-gateway/)[### Integrations

Framework connections

View integrations →](https://mlflow.org/docs/latest/genai/tracing/integrations/)
## Why choose MLflow?[​](#why-choose-mlflow)


#### Open Source

Join thousands of teams building GenAI with MLflow. As part of the Linux Foundation, MLflow ensures your AI infrastructure remains open and vendor-neutral.

#### Production-Ready Platform

Deploy anywhere with confidence. From local servers to cloud platforms, MLflow handles the complexity of GenAI deployment, monitoring, and optimization.

#### End-to-End Lifecycle

Manage the complete GenAI journey from experimentation to production. Track prompts, evaluate quality, deploy models, and monitor performance in one platform.

#### Framework Integration

Use any GenAI framework or model provider. With 20+ native integrations and extensible APIs, MLflow adapts to your tech stack, not the other way around.

#### Complete Observability

See inside every AI decision with comprehensive tracing that captures prompts, retrievals, tool calls, and model responses. Debug complex workflows with confidence.

#### Automated Quality Assurance

Stop manual testing with LLM judges and custom metrics. Systematically evaluate every change to ensure consistent improvements in your AI applications.


## Running Anywhere[​](#running-anywhere)


MLflow can be used in a variety of environments, including your local environment, on-premises clusters, cloud platforms, and managed services. Being an open-source platform, MLflow is **vendor-neutral**; no matter where you are doing machine learning, you have access to the MLflow's core capabilities sets such as tracking, evaluation, observability, and more.


[![Databricks Logo](https://mlflow.org/docs/latest/assets/images/databricks-logo-0d41838793b124a124f8a8a4cc86c7d2.png)](https://docs.databricks.com/aws/en/mlflow3/genai/)[![Amazon SageMaker Logo](data:image/png;base64,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)](https://aws.amazon.com/sagemaker-ai/experiments/)[![Azure Machine Learning Logo](https://mlflow.org/docs/latest/assets/images/azure-ml-logo-92b5684b6330ac456815e6dc3233bbd8.png)](https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow?view=azureml-api-2)[![Nebius Logo](data:image/png;base64,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)](https://nebius.com/services/managed-mlflow)[![Kubernetes Logo](https://mlflow.org/docs/latest/assets/images/kubernetes-logo-0728374966fe59ee08e213e966513d00.png)](https://mlflow.org/docs/latest/ml/tracking/)
## Requesting Features[​](#requesting-features)


Your feedback drives our roadmap! Vote on the most requested features (👍) and share your ideas to help us build what matters most to you.


### Feature requests

Loading feature requests...

---

## MLflow API Docs
<a id="MLflow-API-Docs"></a>

- 元URL: https://mlflow.org/docs/latest/api_reference/index.html

- [Documentation](#)
- MLflow API Docs






# MLflow API Docs[#mlflow-api-docs](#mlflow-api-docs)


This page hosts the API documentation for MLflow.



- [Python API](https://mlflow.org/docs/latest/api_reference/python_api/index.html)
- [TypeScript API](https://mlflow.org/docs/latest/api_reference/typescript_api/index.html)
- [Command-Line Interface](https://mlflow.org/docs/latest/api_reference/cli.html)
- [MLflow Authentication Python API](https://mlflow.org/docs/latest/api_reference/auth/python-api.html)
- [MLflow Authentication REST API](https://mlflow.org/docs/latest/api_reference/auth/rest-api.html)
- [R API](https://mlflow.org/docs/latest/api_reference/R-api.html)
- [Java API](https://mlflow.org/docs/latest/api_reference/java_api/index.html)
- [REST API](https://mlflow.org/docs/latest/api_reference/rest-api.html)

---

## Self Hosting Overview | MLflow
<a id="Self-Hosting-Overview-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/self-hosting/

#### _The most vendor-neutral MLOps/LLMOps platform in the world._

On this page# Self-Hosting MLflow


> The most vendor-neutral MLOps/LLMOps platform in the world.​


MLflow is fully open-source. Thousands of users and organizations run their own MLflow instances to meet their specific needs. Being open-source and trusted by the popular cloud providers, MLflow is the best choice for teams/organizations that worry about vendor lock-in.


## The Quickest Path: Run `mlflow` Command[​](#the-quickest-path-run-mlflow-command)


The easiest way to start MLflow server is to run the `mlflow` CLI command in your terminal. This is suitable for personal use or small teams.


First, install MLflow with:


bash```
pip install mlflow
```


Then, start the server with:


bash```
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000
```


This will start the server and UI at `http://localhost:5000`. You can connect the client to the server by setting the tracking URI:


python```
import mlflowmlflow.set_tracking_uri("http://localhost:5000")# Start tracking!# Open http://localhost:5000 in your browser to view the UI.
```


Now, you are ready to start your experiment!


- [Tracing QuickStart](https://mlflow.org/docs/latest/genai/tracing/quickstart/python-openai/)
- [LLM Evaluation Quickstart](https://mlflow.org/docs/latest/genai/eval-monitor/quickstart/)
- [Prompt Management Quickstart](https://mlflow.org/docs/latest/genai/prompt-registry/#getting-started)
- [Model Training Quickstart](https://mlflow.org/docs/latest/ml/tracking/quickstart/)


tipThe `--backend-store-uri` option is not mandatory, but highly recommended for better performance and reliability. Check out [Backend Store](https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/).


## Other Deployment Options[​](#other-deployment-options)


### Docker Compose[​](#docker-compose)


The MLflow repository includes a ready-to-run Compose project under `docker-compose/` that provisions MLflow, PostgreSQL, and MinIO.


bash```
git clone https://github.com/mlflow/mlflow.gitcd docker-composecp .env.dev.example .envdocker compose up -d
```


Read the instructions [here](https://github.com/mlflow/mlflow/tree/master/docker-compose) for more details and configuration options for the docker compose bundle.


### Kubernetes[​](#kubernetes)


To deploy on Kubernetes, use the MLflow Helm chart provided by [Bitnami](https://artifacthub.io/packages/helm/bitnami/mlflow) or [Community Helm Charts](https://artifacthub.io/packages/helm/community-charts/mlflow).


### Cloud Services[​](#cloud-services)


If you are looking for production-scale deployments without maintenance costs, MLflow is also available as managed services from popular cloud providers.


- [Databricks](https://www.databricks.com/product/managed-mlflow)
- [AWS Sagemaker](https://aws.amazon.com/sagemaker/ai/experiments/)
- [Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow?view=azureml-api-2)
- [Nebius](https://nebius.com/services/managed-mlflow)
- [GCP (GKE)](https://gke-ai-labs.dev/docs/tutorials/frameworks-and-pipelines/mlflow/)


## Architecture[​](#architecture)


MLflow, at a high level, consists of the following components:


1. **Tracking Server**: The lightweight FastAPI server that serves the MLflow UI and API.
2. **Backend Store**: The Backend Store is relational database (or file system) that stores the metadata of the experiments, runs, traces, etc.
3. **Artifact Store**: The Artifact Store is responsible for storing the large artifacts such as model weights, images, etc.


Each component is designed to be pluggable, so you can customize it to meet your needs. For example, you can start with a single host mode with SQLite backend and local file system for storing artifacts. To scale up, you can switch backend store to PostgreSQL cluster and point artifact store to cloud storage such as S3, GCS, or Azure Blob Storage.


To learn more about the architecture and available backend options, see [Architecture](https://mlflow.org/docs/latest/self-hosting/architecture/overview/).


## Access Control & Security[​](#access-control--security)


MLflow support [username/password login](https://mlflow.org/docs/latest/self-hosting/security/basic-http-auth/) via basic HTTP authentication, [SSO (Single Sign-On)](https://mlflow.org/docs/latest/self-hosting/security/sso/), and [custom authentication plugins](https://mlflow.org/docs/latest/self-hosting/security/custom/).


MLflow also provides built-in [network protection](https://mlflow.org/docs/latest/self-hosting/security/network/) middleware to protect your tracking server from network exposure.


Try Managed MLflowNeed highly secure MLflow server? Check out [Databricks Managed MLflow](https://www.databricks.com/product/managed-mlflow) to get fully managed MLflow servers with unified governance and security.


## FAQs[​](#faqs)


See [Troubleshooting & FAQs](https://mlflow.org/docs/latest/self-hosting/troubleshooting/) for more information.

---

## Community | MLflow
<a id="Community-MLflow"></a>

- 元URL: https://mlflow.org/docs/latest/community/

Welcome to the MLflow community! Connect with thousands of data scientists, ML engineers, and practitioners who are building the future of machine learning together.

On this page# Community


Welcome to the MLflow community! Connect with thousands of data scientists, ML engineers, and practitioners who are building the future of machine learning together.


## 🤝 Community Resources[​](#-community-resources)


Join the conversation and get help from our vibrant community:


[### GitHub

Explore the codebase, contribute, and report issues

Visit GitHub →](https://github.com/mlflow/mlflow)[### Slack

Connect with MLflow users and contributors in real-time

Join Slack →](https://mlflow.org/slack)[![X](https://mlflow.org/docs/latest/images/logos/x-logo-black.png)![X](https://mlflow.org/docs/latest/images/logos/x-logo-white.png)### X

Follow us for the latest updates and news

Follow us →](https://x.com/mlflow)[### LinkedIn

Connect with us on LinkedIn for professional updates

Connect →](https://www.linkedin.com/company/mlflow-org)[### Stack Overflow

Get help with technical questions using the mlflow tag

Ask questions →](https://stackoverflow.com/questions/tagged/mlflow)
## 🚀 Get Involved[​](#-get-involved)


There are many ways to contribute to the MLflow ecosystem:


[### Contributing Guide

Learn how to contribute code, documentation, and more to MLflow

Start contributing →](https://github.com/mlflow/mlflow/blob/master/CONTRIBUTING.md)[### MLflow Blog

Stay updated with the latest developments and best practices

Read blog →](https://mlflow.org/blog/index.html)[### Ambassador Program

Become a community leader and advocate for MLflow

Learn more →](https://mlflow.org/ambassadors)[### Report Issues

Help us improve MLflow by reporting bugs or requesting features

Report issue →](https://github.com/mlflow/mlflow/issues/new/choose)
## 📣 Announcements[​](#-announcements)


Stay informed about MLflow updates, releases, and community news:


[### Latest Releases

Check out the newest features and bug fixes in our GitHub releases

View releases →](https://github.com/mlflow/mlflow/releases)[### Community Events

Join us for office hours, webinars, and community meetups

See events →](https://lu.ma/mlflow?k=c)

**Join thousands of ML practitioners building with MLflow!**

Have questions? Start with our [Slack community](https://mlflow.org/slack) or check out the [GitHub repository](https://github.com/mlflow/mlflow).
