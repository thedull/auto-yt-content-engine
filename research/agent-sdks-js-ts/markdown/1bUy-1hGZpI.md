# What is LangChain?

> **Source:** [What is LangChain?](https://www.youtube.com/watch?v=1bUy-1hGZpI) — [IBM Technology](https://www.youtube.com/@IBMTechnology) · 2024-03-15 · 8:07
> *Transcript generated via `youtube-captions (en-US)`.*

## TL;DR

- **LangChain** is an open source orchestration framework (Python and JavaScript) for building applications powered by large language models.
- It works by exposing **abstractions** — reusable building blocks like LLMs, prompts, chains, indexes, memory, and agents — that can be composed to minimize hand-written code.
- Launched by **Harrison Chase** in October 2022, it became the fastest-growing open source project on GitHub by June 2023.
- It supports nearly any LLM (closed-source like **GPT-4** or open-source like **Llama 2**), and integrates with vector databases, document loaders, and external tools.
- Common use cases include **chatbots, summarization, question answering, data augmentation, and virtual agents** that drive RPA workflows.
- Related frameworks include **LangServe** (chains as REST APIs) and **LangSmith** (monitoring, evaluation, debugging).

## Why LangChain exists

Stop me if you've heard this one before, but there are a lot of large language models available today, and they all have their own capabilities and specialties. What if I prefer to use one LLM to interpret some user queries in my business application, but a whole other LLM to author a response to those queries? That scenario is exactly what **LangChain** caters to.

LangChain is an **open source orchestration framework** for the development of applications that use large language models. It comes in both **Python** and **JavaScript** libraries. It's essentially a generic interface for nearly any LLM, giving you a centralized development environment to build your LLM applications and then integrate them with things like data sources and software workflows.

When it was launched by **Harrison Chase** in October 2022, LangChain enjoyed a meteoric rise — by June of the following year, it was the single fastest-growing open source project on GitHub. While the LangChain hype train has cooled a little, there's plenty of utility here.

## Abstractions: the core idea

LangChain streamlines the programming of LLM applications through something called **abstractions**. What does that mean? Think of your thermostat: it lets you control the temperature in your home without needing to understand all the complex circuitry — you just set the temperature. That's an abstraction.

LangChain's abstractions represent common steps and concepts necessary to work with language models, and they can be **chained together** to create applications, minimizing the amount of code required to execute complex NLP tasks.

## The LLM module

Nearly any LLM can be used in LangChain — you just need an API key. The **LLM class** is designed to provide a standard interface for all models, so you pick an LLM of your choice. That could be a closed-source one like **GPT-4** or an open-source one like **Llama 2** — or, this being LangChain, both.

## Prompts and prompt templates

**Prompts** are the instructions given to a large language model. The **prompt template** class in LangChain formalizes the composition of prompts without the need to manually hard-code context and queries.

A prompt template can contain:

- Instructions like *"Do not use technical terms in your response"* — that would be a good one.
- A set of examples to guide responses, known as **few-shot prompting**.
- A specified output format.

## Chains

**Chains**, as the name implies, are the core of LangChain's workflows. They combine LLMs with other components, creating applications by executing a sequence of functions.

For example, say an application needs to:

1. Retrieve data from a website.
2. Summarize the text it gets back.
3. Use that summary to answer user-submitted questions.

That's a **sequential chain** where the output of one function acts as the input to the next. Each function in the chain could use different prompts, different parameters, and even different models.

## Indexes: connecting LLMs to external data

To achieve certain tasks, LLMs might need to access specific external data sources that aren't part of their training data set — things like internal documents, emails, and so on. LangChain collectively refers to this sort of documentation as **indexes**, and there are a number of them.

### Document loaders

**Document loaders** work with third-party applications for importing data from sources like:

- File storage services such as **Dropbox** or **Google Drive**.
- Web content such as **YouTube transcripts**.
- Collaboration tools like **Airtable**.
- Databases like **Pandas** and **MongoDB**.

### Vector databases

There's also support for **vector databases**. Unlike traditional structured databases, vector databases represent data points by converting them into **vector embeddings** — numerical representations in the form of vectors with a fixed number of dimensions. You can store a lot of information in this format, and it's a very efficient means of retrieval.

### Text splitters

**Text splitters** can split text into small, semantically meaningful chunks that can then be combined using the methods and parameters of your choosing.

## Memory

LLMs, by default, don't really have any long-term memory of prior conversations — not unless you happen to pass the chat history in as an input to your query. LangChain solves this with simple utilities for adding **memory** into your application. You have options ranging from retaining the entire conversation, through to keeping just a **summarization** of the conversation so far.

## Agents

**Agents** can use a given language model as a **reasoning engine** to determine which actions to take. When building a chain for an agent, you'll want to include inputs like:

- A list of the available **tools** the agent should use.
- The **user input**, such as prompts and queries.
- Any other relevant **previously executed steps**.

## LangChain use cases

So how can we put all of this to work for our applications?

- **Chatbots.** LangChain can provide proper context for a chatbot's specific use case and integrate it into existing communication channels and workflows via APIs.
- **Summarization.** Language models can summarize many types of text — from complex academic papers and transcripts, to a digest of incoming emails.
- **Question answering.** Using specific documents or specialized knowledge bases, LLMs can retrieve the relevant information from storage and articulate helpful answers using information that would otherwise not have been in their training dataset.
- **Data augmentation.** LLMs can generate **synthetic data** for use in machine learning — for example, generating additional samples that closely resemble real data points in a training dataset.
- **Virtual agents.** Integrated with the right workflows, LangChain's agent modules can use an LLM to autonomously determine the next steps and take action using **RPA** (robotic process automation).

## The broader LangChain ecosystem

LangChain is open source and free to use. Related frameworks include:

- **LangServe** — for creating chains as REST APIs.
- **LangSmith** — tools to monitor, evaluate, and debug applications.

Essentially, LangChain's tools and APIs simplify the process of building applications that make use of large language models.
