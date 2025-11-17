# MLflow-Databricks

- 抽出日時: 2025-11-12 10:56
- 件数: 2

## 目次
1. [MLflow for ML model lifecycle | Databricks on AWS](#MLflow-for-ML-model-lifecycle-Databricks-on-AWS)
2. [MLflow 3 for GenAI | Databricks on AWS](#MLflow-3-for-GenAI-Databricks-on-AWS)


---

## MLflow for ML model lifecycle | Databricks on AWS
<a id="MLflow-for-ML-model-lifecycle-Databricks-on-AWS"></a>

- 元URL: https://docs.databricks.com/aws/en/mlflow/

Learn how Databricks uses MLflow to manage the end-to-end machine learning lifecycle.

On this page# MLflow for ML model lifecycle


This article describes how MLflow on Databricks is used to develop high-quality generative AI agents and machine learning models.


noteIf you're just getting started with  Databricks , consider trying MLflow on [Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition).


## What is MLflow?[​](#what-is-mlflow)


MLflow is an open source platform for developing models and generative AI applications. It has the following primary components:


- Tracking: Allows you to track experiments to record and compare parameters and results.
- Models: Allow you to manage and deploy models from various ML libraries to various model serving and inference platforms.
- Model Registry: Allows you to manage the model deployment process from staging to production, with model versioning and annotation capabilities.
- AI agent evaluation and tracing: Allows you to develop high-quality AI agents by helping you compare, evaluate, and troubleshoot agents.


MLflow supports [Java](https://www.mlflow.org/docs/latest/java_api/index.html), [Python](https://www.mlflow.org/docs/latest/python_api/index.html), [R](https://www.mlflow.org/docs/latest/R-api.html), and [REST](https://docs.databricks.com/api/workspace/experiments) APIs.


## MLflow 3[​](#mlflow-3)


MLflow 3 on  Databricks  delivers state-of-the-art experiment tracking, observability, and performance evaluation for machine learning models, generative AI applications, and agents on the Databricks lakehouse. Using MLflow 3 on  Databricks , you can:


- Centrally track and analyze the performance of your models, AI applications, and agents across all environments, from interactive queries in a development notebook through production batch or real-time serving deployments.


![Model tracking UI.](https://docs.databricks.com/aws/en/assets/images/mlflow-model-tracking-ui-719f2224cc10087b4371b8d4496c066a.png)
- Orchestrate evaluation and deployment workflows using  Unity Catalog  and access comprehensive status logs for each version of your model, AI application, or agent.


![A complex deployment job that includes staged rollout and metrics collection.](https://docs.databricks.com/aws/en/assets/images/complex-deployment-job-9ea629abdeae12c52b0fd7f079d78a7e.png)
- View and access model metrics and parameters from the model version page in  Unity Catalog  and from the REST API.


![Model version page in Unity Catalog showing metrics from multiple runs.](https://docs.databricks.com/aws/en/assets/images/uc-model-version-page-674574ad9423349aee3915e8a7a92e3d.png)
- Annotate requests and responses (*traces*) for all of your gen AI applications and agents, enabling human experts and automated techniques (such as LLM-as-a-judge) to provide rich feedback. You can leverage this feedback to assess and compare the performance of application versions and to build datasets for improving quality.


![Traces tab of model page showing details of multiple traces.](https://docs.databricks.com/aws/en/assets/images/model-details-traces-2207f67728bcd54d2d95a640dae97d38.png)


These capabilities simplify and streamline evaluation, deployment, debugging, and monitoring for all of your AI initiatives.


MLflow 3 also introduces the concepts of Logged Models and Deployment Jobs.


- [Logged Models](https://docs.databricks.com/aws/en/mlflow/logged-model) help you track a model's progress throughout its lifecycle. When you log a model using `log_model()`, a `LoggedModel` is created that persists throughout the model's lifecycle, across different environments and runs, and contains links to artifacts such as metadata, metrics, parameters, and the code used to generate the model. You can use the Logged Model to compare models against each other, find the most performant model, and track down information during debugging.
- [Deployment jobs](https://docs.databricks.com/aws/en/mlflow/deployment-job) can be used to manage the model lifecycle, including steps like evaluation, approval, and deployment. These model workflows are governed by  Unity Catalog , and all events are saved to an activity log that is available on the model version page in  Unity Catalog .


See the following articles to install and get started using MLflow 3.


- [Get started with MLflow 3 for models](https://docs.databricks.com/aws/en/mlflow/mlflow-3-install).
- [Track and compare models using MLflow Logged Models](https://docs.databricks.com/aws/en/mlflow/logged-model).
- [Model Registry improvements with MLflow 3](https://docs.databricks.com/aws/en/mlflow/model-registry-3).
- [MLflow 3 deployment jobs](https://docs.databricks.com/aws/en/mlflow/deployment-job).


## Databricks-managed MLflow[​](#databricks-managed-mlflow)


Databricks provides a fully managed and hosted version of MLflow, building on the open source experience to make it more robust and scalable for enterprise use.


The following diagram shows how Databricks integrates with MLflow to train and deploy machine learning models.


![MLflow integrates with Databricks to manage the ML lifecycle.](https://docs.databricks.com/aws/en/assets/images/mlflow-databricks-integration-ml-fed171835b9207db06e6b4867731a3fe.png)


Databricks-managed MLflow is built on Unity Catalog and the Cloud Data Lake to unify all your data and AI assets in the ML lifecycle:


1. **Feature store:** Databricks automated feature lookups simplifies integration and reduces mistakes.
2. **Train models:** Use Mosaic AI to train models or fine-tune foundation models.
3. **Tracking**: MLflow tracks training by logging parameters, metrics, and artifacts to evaluate and compare model performance.
4. **Model Registry:** MLflow Model Registry, integrated with  Unity Catalog  centralizes AI models and artifacts.
5. **Model Serving:** Mosaic AI Model Serving deploys models to a REST API endpoint.
6. **Monitoring:** Mosaic AI Model Serving automatically captures requests and responses to monitor and debug models. MLflow augments this data with trace data for each request.


## Model training[​](#model-training)


MLflow Models are at the core of AI and ML development on Databricks. MLflow Models are a standardized format for packaging machine learning models and generative AI agents. The standardized format ensures that models and agents can be used by downstream tools and workflows on Databricks.


- MLflow documentation - [Models](https://mlflow.org/docs/latest/models.html).


Databricks provides features to help you train different kinds of ML models.


- [Train AI models using Mosaic AI](https://docs.databricks.com/aws/en/machine-learning/train-model/).


## Experiment tracking[​](#experiment-tracking)


Databricks uses MLflow experiments as organizational units to track your work while developing models.


Experiment tracking lets you log and manage parameters, metrics, artifacts, and code versions during machine learning training and agent development. Organizing logs into experiments and runs allows you to compare models, analyze performance, and iterate more easily.


- [Experiment tracking using Databricks](https://docs.databricks.com/aws/en/mlflow/tracking).
- See MLflow documentation for general information on [runs and experiment tracking](https://mlflow.org/docs/latest/tracking.html).


## Model Registry with Unity Catalog[​](#model-registry-with-unity-catalog)


MLflow Model Registry is a centralized model repository, UI, and set of APIs for managing the model deployment process.


Databricks integrates Model Registry with  Unity Catalog  to provide centralized governance for models.  Unity Catalog  integration allows you to access models across workspaces, track model lineage, and discover models for reuse.


- [Manage models using Databricks Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/).
- See MLflow documentation for general information on [Model Registry](https://mlflow.org/docs/latest/model-registry.html).


## Model Serving[​](#model-serving)


Databricks Model Serving is tightly integrated with MLflow Model Registry and provides a unified, scalable interface for deploying, governing, and querying AI models. Each model you serve is available as a REST API that you can integrate into web or client applications.


While they are distinct components, Model Serving heavily relies on MLflow Model Registry to handle model versioning, dependency management, validation, and governance.


- [Model Serving using Databricks](https://docs.databricks.com/aws/en/machine-learning/model-serving/).


## AI agent development and evaluation[​](#ai-agent-development-and-evaluation)


For AI agent development, Databricks integrates with MLflow similarly to ML model development. However, there are a few key differences:


- To create AI agents on Databricks, use [Mosaic AI Agent Framework](https://docs.databricks.com/aws/en/generative-ai/agent-framework/build-genai-apps), which relies on MLflow to track agent code, performance metrics, and agent traces.
- To evaluate agents on Databricks, use [Mosaic AI Agent Evaluation](https://docs.databricks.com/aws/en/generative-ai/agent-evaluation/), which relies on MLflow to track evaluation results.
- MLflow tracking for agents also includes [MLflow Tracing](https://mlflow.org/docs/latest/llms/tracing/index.html). MLflow Tracing allows you to see detailed information about the execution of your agent's services. Tracing records the inputs, outputs, and metadata associated with each intermediate step of a request, letting you quickly find the source of unexpected behavior in agents.


The following diagram shows how Databricks integrates with MLflow to create and deploy AI agents.


![MLflow integrates with Databricks to manage the gen AI app lifecycle.](https://docs.databricks.com/aws/en/assets/images/mlflow-databricks-integration-agents-a5dc523cac9f98bf702ca836c46eea68.png)


Databricks-managed MLflow is built on Unity Catalog and the Cloud Data Lake to unify all your data and AI assets in the gen AI app lifecycle:


1. **Vector & feature store:** Databricks automated vector and feature lookups simplify integration and reduce mistakes.
2. **Create and evaluate AI agents:** Mosaic AI Agent Framework and Agent Evaluation help you create agents and evaluate their output.
3. **Tracking & tracing:** MLflow tracing captures detailed agent execution information for enhanced generative AI observability.
4. **Model Registry:** MLflow Model Registry, integrated with  Unity Catalog  centralizes AI models and artifacts.
5. **Model Serving:** Mosaic AI Model Serving deploys models to a REST API endpoint.
6. **Monitoring:** MLflow automatically captures requests and responses to monitor and debug models.


## Open source vs. Databricks-managed MLflow features[​](#open-source-vs-databricks-managed-mlflow-features)


For general MLflow concepts, APIs, and features shared between open source and Databricks-managed versions, refer to [MLflow documentation](https://mlflow.org/docs/latest/index.html). For features exclusive to Databricks-managed MLflow, see Databricks documentation.


The following table highlights the key differences between open source MLflow and Databricks-managed MLflow and provides documentation links to help you learn more:


Feature

Availability on open source MLflow

Availability on Databricks-managed MLflow

Security

User must provide their own security governance layer

[Databricks enterprise-grade security](https://docs.databricks.com/aws/en/security/)

Disaster recovery

Unavailable

[Databricks disaster recovery](https://docs.databricks.com/aws/en/admin/disaster-recovery)

Experiment tracking

[MLflow Tracking API](https://mlflow.org/docs/latest/tracking.html)

MLflow Tracking API integrated with [Databricks advanced experiment tracking](https://docs.databricks.com/aws/en/mlflow/tracking)

Model Registry

[MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)

[MLflow Model Registry integrated with Databricks Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)

Unity Catalog integration

Open source integration with Unity Catalog

[Databricks Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)

Model deployment

User-configured integrations with external serving solutions (SageMaker, Kubernetes, container services, and so on)

[Databricks Model Serving](https://docs.databricks.com/aws/en/machine-learning/model-serving/) and external serving solutions

AI agents

[MLflow LLM development](https://mlflow.org/docs/2.10.2/llms/index.html)

MLflow LLM development integrated with [Mosaic AI Agent Framework](https://docs.databricks.com/aws/en/generative-ai/agent-framework/build-genai-apps) and [Agent Evaluation](https://docs.databricks.com/aws/en/generative-ai/agent-evaluation/)

Encryption

Unavailable

Encryption using [customer-managed keys](https://docs.databricks.com/aws/en/security/keys/)


noteOpen source telemetry collection was introduced in MLflow 3.2.0, and is **disabled on Databricks by default**. For more details, refer to the [MLflow usage tracking documentation](https://mlflow.org/docs/latest/community/usage-tracking/).

---

## MLflow 3 for GenAI | Databricks on AWS
<a id="MLflow-3-for-GenAI-Databricks-on-AWS"></a>

- 元URL: https://docs.databricks.com/aws/en/mlflow3/genai/

Measure, improve, and monitor quality throughout the GenAI application lifecycle using AI-powered metrics and comprehensive trace observability.

On this page# MLflow 3 for GenAI


This page describes how MLflow 3 for GenAI, integrated with the Databricks platform, helps you build production-grade GenAI apps.


Traditional software and ML tests aren't built for GenAI's free-form language, making it difficult for teams to measure and improve quality. MLflow 3 solves this by combining AI-powered metrics that reliably measure GenAI quality with comprehensive trace observability, enabling you to measure, improve, and monitor quality throughout the entire application lifecycle.


When you use MLflow 3 for GenAI on Databricks, you get all of the advantages of the Databricks platform, including the following:


- **Unified platform**. The entire GenAI development process in one place, from development debugging to production monitoring.
- **Open and flexible**. Use any LLM provider and any framework.
- **Enterprise-ready**. The Databricks platform provides enterprise security, scale, and governance.


Agent Evaluation SDK methods are integrated with Databricks-managed MLflow 3. For information about agent evaluation in MLflow 2, see [Mosaic AI Agent Evaluation  (MLflow 2)](https://docs.databricks.com/aws/en/generative-ai/agent-evaluation/) and the [migration guide](https://docs.databricks.com/aws/en/mlflow3/genai/agent-eval-migration).


For a set of tutorials to get you started, see [Get started with MLflow 3 for GenAI](#get-started).


noteOpen source telemetry collection was introduced in MLflow 3.2.0, and is **disabled on Databricks by default**. For more details, refer to the [MLflow usage tracking documentation](https://mlflow.org/docs/latest/community/usage-tracking/).


## Observe and debug GenAI apps with tracing[​](#observe-and-debug-genai-apps-with-tracing)


See exactly what your GenAI application is doing with comprehensive observability that captures every step of execution. You need only add a single line of code, and MLflow Tracing captures all prompts, retrievals, tool calls, responses, latency, and token counts throughout your application.


Python```
# Just add one line to capture everythingmlflow.autolog()# Your existing code works unchangedresponse = client.chat.completions.create(...)# Traces are automatically captured!
```


![Evaluation Comparison](https://assets.docs.databricks.com/_static/images/mlflow3-genai/eval-comparison.gif)


Feature

Description

[**Automatic instrumentation**](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/automatic)

One-line instrumentation for 20+ libraries including OpenAI, LangChain, LlamaIndex, Anthropic, and DSPy.

[**Review your app's behavior and performance**](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/observe-with-traces/)

Complete execution visibility allows you to capture prompts, retrievals, tool calls, responses, latency, and costs.

[**Production observability**](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing)

Use the same instrumentation in development and production environments for consistent evaluation.

[**OpenTelemetry compatibility**](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/integrations/open-telemetry)

Export traces anywhere while maintaining full data ownership and integration flexibility.


## Automated quality evaluation of GenAI apps[​](#automated-quality-evaluation-of-genai-apps)


Replace manual testing with automated evaluation using built-in and custom LLM Judges that match human expertise and can be applied in both development and production.


Feature

Description

[**Built-in scorers**](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/predefined-judge-scorers)

Ready-to-use scorers that assess safety, hallucinations, relevance, correctness, and retrieval quality.

[**Custom scorers**](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-judge/)

Create tailored judges that enforce your specific business requirements and align with domain expert judgment.


## Turn production data into improvements[​](#turn-production-data-into-improvements)


Every production interaction becomes an opportunity to improve with integrated feedback and evaluation workflows.


![Trace Summary](https://assets.docs.databricks.com/_static/images/mlflow3-genai/trace-summary.gif)


Feature

Description

[**Expert feedback collection**](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/expert-feedback/label-existing-traces)

The Review App provides a structured process and UI for collecting domain expert feedback including ratings, corrections, and guidelines on real interactions with your application.

[**Live app testing**](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/expert-feedback/live-app-testing)

The Review App's Chat UI allows subject matter experts to chat with your app and provide instant feedback for continuous improvement.

[**Evaluation datasets from production**](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset)

Evaluation datasets enable consistent, repeatable evaluation. Problematic production traces become test cases for continuous improvement and regression testing.

[**User feedback collection**](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/collect-user-feedback/)

Capture and link user feedback to specific traces for debugging and quality improvement insights. Collect thumbs up/down and comments programmatically from your deployed application.

[**Evaluate and improve quality with traces**](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/quality-with-traces)

Analyze traces to identify quality issues, create evaluation datasets from trace data, implement targeted improvements, and measure the impact of your changes.


## Manage your GenAI application lifecycle[​](#manage-your-genai-application-lifecycle)


Version, track, and govern your entire GenAI application with enterprise-grade lifecycle management and governance tools.


Feature

Description

[**Application versioning**](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/track-application-versions-with-mlflow)

Track code, parameters, and evaluation metrics for each version.

[**Production trace linking**](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions)

Link traces, evaluations, and feedback to specific application versions.

[**Prompt Registry**](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/)

Centralized management for versioning and sharing prompts across your organization with A/B testing capabilities and  Unity Catalog  integration.

**Enterprise integration**

[Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/). Unified governance for all AI assets with enterprise security, access control, and compliance features.

[Data intelligence](https://docs.databricks.com/aws/en/ai-bi/). Connect your GenAI data to your business data in the Databricks Lakehouse and deliver custom analytics to your business stakeholders.

[Mosaic AI Agent Serving](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing). Deploy agents to production with scaling and operational rigor.


## []() Get started with MLflow 3 for GenAI[​](#-get-started-with-mlflow-3-for-genai)


Start building better GenAI applications with comprehensive observability and evaluation tools.


Task

Description

[**Quick start guide**](https://docs.databricks.com/aws/en/mlflow3/genai/getting-started/)

Get up and running in minutes with step-by-step instructions for instrumenting your first application.

[**Databricks Notebook setup**](https://docs.databricks.com/aws/en/mlflow3/genai/getting-started/tracing/tracing-notebook)

Start in a managed environment with pre-configured dependencies and instant access to MLflow 3 features.

[**Local IDE development**](https://docs.databricks.com/aws/en/mlflow3/genai/getting-started/tracing/tracing-ide)

Develop on your local machine with full MLflow 3 capabilities and seamless cloud integration.

[**Data Intelligence integration**](https://docs.databricks.com/en/ai-bi/index.html)

Connect your GenAI data to business data in the Databricks Lakehouse for custom analytics and insights.
