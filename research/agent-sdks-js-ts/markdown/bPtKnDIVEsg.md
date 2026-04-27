# Google Agent Development Kit (ADK): How to Deploy Your First Agent to Vertex AI Agent Engine

> **Source:** [Google Agent Development Kit (ADK): How to deploy Your First Agent to Vertex AI Agent Engine](https://www.youtube.com/watch?v=bPtKnDIVEsg) — [aiwithbrandon](https://www.youtube.com/@aiwithbrandon) · 2025-04-19 · 37:13
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- Walks through deploying an agent built with **Google Agent Development Kit (ADK)** to **Vertex AI Agent Engine**, Google's managed agent deployment platform.
- ADK is Google's new open-source agent framework, comparable to LangChain, CrewAI, or LlamaIndex, and supports any model provider (Gemini, OpenAI, Claude, etc.).
- Agent Engine is pay-as-you-go (~11 cents/hour for 1 core + 1 GB), framework-agnostic, and exposes deployed agents like an API.
- Five steps: build the agent locally, create a GCP project, enable Vertex AI + create a storage bucket, install and configure the gcloud CLI, then deploy with a Poetry script.
- After deployment, you interact with the agent through **deployments** (the packaged agent) and **sessions** (conversations), and you can inspect everything via Cloud **Trace Explorer**.

## Core technologies: ADK and Vertex AI Agent Engine

Before diving into deployment, it helps to understand the two technologies in play.

**Agent Development Kit (ADK)** is Google's new agentic framework for building agents. If you've used **LangChain**, **CrewAI**, or **LlamaIndex**, the API will look very familiar — you pass in a model, give the agent a name, and provide instructions describing what it should do. A few notable points:

- ADK is **model-agnostic** — you can plug in OpenAI, Claude, or any other model, not just Gemini.
- It's completely free and open source, so you can read the source, download it, and submit pull requests.

**Vertex AI Agent Engine** is Google's platform for making agent deployment as easy as possible. Without something like this, deploying agents can be a ton of work, and Google has done a good job simplifying the process.

- Agent Engine is **framework-agnostic** — you can deploy a CrewAI agent, a LangChain agent, a LlamaIndex agent, or an ADK agent.
- Once deployed, you call the agent almost like a regular API.
- Pricing is **pay-as-you-go**: you only pay while the agent is running. You pay for tokens used plus CPU/memory. Running for an hour with one core and 1 GB RAM costs roughly **11 cents** — very affordable.

## The five steps to deploy an agent

At a high level, the workflow is:

1. **Create an agent** locally using ADK (Brandon provides a prebuilt one).
2. **Create a new project** in Google Cloud Platform.
3. **Enable AI resources** inside that project (Vertex AI + a Cloud Storage bucket).
4. **Install and configure the Google Cloud CLI** so your local machine can talk to GCP and Vertex AI.
5. **Deploy the agent** to Agent Engine using the provided script.

## Step 1: Overview of the ShortBot agent

The example agent is **ShortBot** — it takes in a message and rewrites it to be as short as possible while preserving meaning.

The structure looks like LangChain or CrewAI: you pass a name, model, description, and instructions, then attach tools. Tools are just normal Python functions with type-annotated parameters and a docstring describing what they do. Because this is a deployment tutorial, the underlying agent is intentionally simple.

**Setup instructions:**

- Download the source code (free link in the video description).
- Install **Poetry** (Brandon's package manager of choice). If you hit issues, his community can help walk you through it.
- Run `poetry install` to install all dependencies, including ADK and the deployment tools.
- Activate the Poetry environment.
- Run `adk web` to spin up ADK's local web UI for chatting with the agent.

> Note: `adk web` will not actually run until step 4 is complete, because the agent needs Vertex AI credentials (set up via the gcloud CLI).

In the web UI, the top left lists all your agents. You can send a message like "Hey, how was your weekend? Anything fun? Have fun with the family." The agent responds with the **original character count**, the **new character count**, and the **shortened message**. You can also drill into events to see the request, response, and any tool calls.

**Important folder convention:** ADK agents are defined as folders. Brandon's `ADK_shortbot` folder contains an `agent.py` file. The `name` field inside the agent **must match the folder/project name** — this tripped him up the first time he built an ADK agent.

## Step 2: Create a Google Cloud Platform project

1. Search for "GCP cloud" and click the link to Google Cloud.
2. If you don't already have an account, sign up. It's free; you may need to attach a payment method, but you won't be charged until you actually run something.
3. Click **Console** to enter the Cloud dashboard.
4. Click **New Project**, give it a memorable name (Brandon used `ADK shortbot YouTube`), pick your billing account, organization, and location, then **Create**.
5. Once the project is created, select it. You should see your new project name in the top left.

## Step 3: Enable Vertex AI and create a storage bucket

1. In the search bar at the top of the GCP console, type **Vertex AI** and click the result.
2. Click **Enable all recommended APIs**. This provisions Vertex AI Studio plus everything needed to use Agent Engine. Watch the bell icon in the top-right corner to see the services being enabled (compute, notebooks, dataflow, and more).
3. Create a **Cloud Storage bucket** to store deployed agents. Search for "bucket", go to **Cloud storage bucket**, and click **Create**.
4. Give the bucket the same name as your project (e.g. `ADK shortbot YouTube`).
5. Walk through the wizard accepting defaults. **Crucial:** keep **Enforce public access prevention** checked — you do not want the outside world reading from this bucket.
6. Continue through the soft delete and remaining options with defaults.

Bucket pricing is roughly **3 cents per GB per month**, and your usage will be tiny — likely pennies per month.

After the bucket is created, you need to record three pieces of info into your project's `.env` file:

- **GOOGLE_CLOUD_PROJECT** — your project ID (copy it from the GCP console).
- **GOOGLE_CLOUD_LOCATION** — Brandon recommends `us-central1`. There are about 30 AI-enabled regions, but `us-central1` works reliably.
- **GOOGLE_CLOUD_STORAGE_BUCKET** — the bucket name you just created.

## Step 4: Install and configure the Google Cloud CLI

Installing **gcloud** does two things: it lets your local agent reach Gemini through Vertex AI credentials, and it lets you deploy agents to the cloud.

The ADK quickstart guide explicitly walks you through this. Pick the right installer for your platform — Brandon used the **Apple Silicon** download for Mac. Run the install command shown on the page, then run `gcloud init` to add gcloud to your `PATH` so you can run it from anywhere.

Then:

1. Run `gcloud auth login` to authenticate. Accept all permissions when prompted.
2. Run `gcloud init`. It will ask which account to use (pick the one you just logged into) and which project to associate with this configuration. Choose option 1 to list your projects and pick the one you created in step 2.
3. Skip the default zone prompt for now.

You should see a "congrats, you're ready to use Google Cloud" message confirming the project is wired up. At this point `adk web` will work properly because your local environment has access to Vertex AI and your Gemini credentials.

## Step 5: Deploy the agent to Agent Engine

### Core concepts before you deploy

When you deploy, two things happen under the hood:

1. **Create the application** — ADK wraps your root agent into what it calls a **reasoning engine**. You pass in your root agent (`shortbot`) and enable tracing.
2. **Create the deployment** — call `agent_engine.create()` and pass the application, plus:
   - **`requirements`** — any Python packages your agent needs (e.g. a weather SDK if you were building a weather agent).
   - **`extra_packages`** — the local package(s) to bundle. In this project that's `ADK_shortbot`, since that folder contains the agent code.

Two terms to keep straight:

- **Deployment**: the bundle of agent code, dependencies, and instructions sitting in Agent Engine, ready to be invoked.
- **Session**: a single conversation with a deployed agent. Sessions are just message history — if there were tool calls, they'd show inside the session too.

### Running the deployment script

Brandon's script (defined in `pyproject.toml` as `deploy-remote`) routes to `deployment/remote.py`'s `main` function. The CLI supports several flags: create/list/delete deployments, list/get sessions, and send messages to sessions.

To deploy:

```
poetry run deploy-remote --create
```

This will:

1. Install all the dependencies declared in your project.
2. Use the bucket you configured in `.env` to upload the bundled agent (zipped code, instructions, and dependencies).
3. Hand everything to Agent Engine, which builds a container and starts the deployment.

You can follow real-time logs by clicking the link the script prints. Inside the storage bucket you can also see the agent engine folder filling up with `requirements.txt` and the agent's source. Deployment can take **up to 10 minutes** — get a coffee.

### Listing deployments

Once deployment finishes:

```
poetry run deploy-remote --list
```

This calls Agent Engine to enumerate every deployed agent. You should see your ShortBot deployment with its **resource ID**.

### Creating a session

A session needs:

- **resource ID** — which deployed agent to talk to.
- **user ID** — identifies the caller. This doesn't have to exist in any user database; Agent Engine just uses it later to let you list a specific user's conversations. If you don't pass one, the script uses `test_user` by default.

```
poetry run deploy-remote --create_session --resource_id <RESOURCE_ID>
```

The script prints back the new **session ID**, the user ID (`test_user`), and other session metadata.

### Sending messages

To chat with your deployed agent, you need the resource ID, user ID, session ID, and a message:

```
poetry run deploy-remote --send --resource_id <RESOURCE_ID> --user_id test_user --session_id <SESSION_ID> --message "Hey, how did your weekend go? Anything fun?"
```

Brandon's test result: the agent shortened a 38-character message down to 23 ("Hey, how was your weekend?"). The key point is **this is not running locally** — it's running fully in the cloud on Agent Engine.

## Bonus: viewing traces

Once you've sent some traffic through your agent, you can inspect what happened using **Cloud Trace Explorer**.

1. In the GCP search bar, type **traces** and click **Trace Explorer**.
2. You'll see invocations corresponding to each agent call. Click one to drill in.
3. The trace shows that **ADK shortbot** was called, what it did (e.g. it called an LLM), and the full LLM details — Brandon's example shows **Gemini Flash 2.0**, the system instruction ("Your message is shortening assistant..."), and the model's response.
4. You can filter — for example, only show LLM calls — to focus on what you care about.

Traces are a powerful next step for monitoring deployed agents in production: you can see what your agent is doing, whether it's behaving correctly, and where it's spending time or tokens.

## Wrap-up

By now you've created an ADK agent locally, set up a GCP project with Vertex AI and a Cloud Storage bucket, installed and authenticated the gcloud CLI, deployed your agent to Agent Engine, and chatted with it through sessions. You also know how to inspect deployments and traces.

The video description includes free source code, and Brandon teases an upcoming **ADK quickstart** and a full **ADK masterclass** on the same channel.
