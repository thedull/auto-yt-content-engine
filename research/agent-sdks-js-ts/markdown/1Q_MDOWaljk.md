# Agentic Framework LangGraph Explained in 8 Minutes — Beginner's Guide

> **Source:** [Agentic Framework LangGraph explained in 8 minutes | Beginners Guide](https://www.youtube.com/watch?v=1Q_MDOWaljk) — [W.W. AI Adventures](https://www.youtube.com/@WW_AI_Adventures) · 2024-12-23 · 8:04
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **LangGraph** is an AI-agent-building framework from **LangChain** that lets language models control what happens next, available in Python and JavaScript.
- It's a flexible alternative to **CrewAI** and **Microsoft AutoGen**, with native support for streaming, async execution, persistence, fault-tolerant tool calls, and **human-in-the-loop** workflows.
- The core building blocks are **nodes** (code to execute), **edges** (which node runs next), **conditional edges** (decide based on state), and **state** (carries inputs, outputs, and variables between nodes).
- LangGraph supports any architecture you want to build, including **routers**, **ReAct agents**, and **reflection** patterns.
- The walkthrough builds a small ReAct weather agent using `StateGraph`, a `@tool`-decorated `get_weather` function, a prebuilt `ToolNode`, a prompt node, and a conditional edge that routes to tools or ends execution.

## What LangGraph is and why use it

Welcome to this beginner tutorial on **LangGraph**, where we're going to cover the theory and then a practical example of how you can get stuck in. So LangGraph — what is it, why should you use it, and how do you use it?

LangGraph is an **AI agent building framework** built by **LangChain**. It's highly flexible and it allows you to connect language models together in a way that the LLM can control what happens next. It's supported in two major programming languages, **Python** and **JavaScript**, and it was released last October. Since then it's been increasing in popularity as an alternative to other agent-building frameworks like **CrewAI** and **Microsoft AutoGen**.

## Example: a banking customer-support agent

Let's take a look at an example of how it might be used. Take a customer support agent who asks a question to an online website chatbot for a bank. The chatbot agent might then look up the customer information, update the customer details based on the conversation, and then want to make a transaction for the customer. But because this is a large transaction, we might want verification from a real person before it goes ahead.

LangGraph supports this with **human-in-the-loop execution**, where the transaction can be authorized first before the conversation with the customer can continue.

## Where LangGraph could be useful

What are some other applications where LangGraph could be highly useful?

- **Copywriting** — gathering information from across the internet and putting it together into a single article or report.
- **Custom analytics** — creating figures, dashboards, or extracting information from a database.
- **Customer service assistance** — answering questions via email, WhatsApp, SMS, or voice.
- **Personalized recommendations** — using previous interactions with the customer to infer what they prefer.
- **Research** — making sure you stay up to date with the latest trends or any new articles that have been released.
- **Personal marketing** — tailoring communications to each customer based on their personal characteristics.

## Features that make LangGraph stand out

What are some features that make LangGraph particularly useful as an agentic framework?

- **Streaming** straight out of the box, with either tokens or messages.
- **Async / multiple execution** at the same time.
- **Persistence with a database**, so you don't need to persist your state between invocations.
- **Fault-tolerant tool calls**, so it can handle failures with external APIs.
- **Human-in-the-loop execution**, as we've seen.
- Because of the way it handles state, it makes it quite easy to decide what the next actions should be.

## Core building blocks

Let's take a look at the core building blocks of LangGraph that allow you to customize it for your use case:

- **Nodes** contain the code you want to execute.
- **Edges** connect nodes and determine which node should be executed next.
- **Conditional edges** decide, based on what's happened so far, which node should be executed next.
- **State** ties everything together — it stores our inputs, outputs, and any variables created to pass information between nodes.

### How they interact

Let's see how all these components interact together in another example. Take another customer service agent who asks a question to our agent. The input message is stored in our state, which is also storing some custom information about the shop — for example, the opening hours.

Our graph is then executed: the state goes into the start of the graph and is passed to the first node, where a call to a language model is made and a new message is added to the graph state. After this the flow of execution moves to the end node, the final state is returned, and we can return the output message to the user.

This is a very basic example, but LangGraph supports any architecture you'd like to build, including:

- **Router** — a conditional edge chooses which prompt should be executed based on the input to the graph.
- **ReAct agent** — a language model decides which tools should be executed, we execute those tools as code locally, and the responses are passed back into the language model for it to decide the next steps.
- **Reflection** — one language model generates an output and another reviews that output, identifying any mistakes and passing feedback to the first to correct them.

## Building it in code: a ReAct weather agent

Now that we've covered the theory, let's take a look at how we can build these architectures in code.

### Install the requirements

First, we need to install the requirements. If you've cloned the repository you can do this with `pip install -r requirements`. If you haven't cloned the repository, you can install the two packages **`langgraph`** and **`langchain-openai`**.

If you're following along, you're also going to need an **OpenAI API key** for this tutorial. You can get one by logging in to your OpenAI account and going to **platform.openai.com**, then to the **API Keys** tab and clicking **Create new secret key**.

### Set up state and graph

First we need to import all the classes and functions that we'll need for this tutorial. We're then going to create our **graph state**, where we store all of the inputs, outputs, and variables we're going to need to access during the graph execution.

We can then create our graph with the prebuilt **`StateGraph`** class.

### Define a tool and bind it to the model

As this is a **ReAct agent**, we're going to need tools. This agent will only be doing one thing: retrieving the weather at a particular location. We create a tool with the **`@tool`** decorator provided by LangChain. You don't need to use LangChain, but we're going to use it here for convenience.

I'm then creating a language model class with **`ChatOpenAI`** and putting in the API key that I retrieved earlier. I'm then binding the tools I've created — the `get_weather` function — to this language model, so the language model knows that this tool is available to use.

### Add the tool node

In order to provide these tools within the graph, we need to create a node, and we can do this with a prebuilt node provided by LangGraph called **`ToolNode`**. So we create that and add the node, naming it `tool_node`, to our existing graph.

### Add the prompt node

Now that we've got our tool, we need the main entry node where we call our language model to see if we need to perform any tool calls. I'm calling this **`prompt_node`**. All that happens within this node is that we invoke our language model and add the response message into the graph state.

When we respond with messages in a list, we then update the messages in the graph state with all of the new messages that have been returned. This happens automatically — this is the way state works in LangGraph.

### Wire it together with a conditional edge

To connect it up together, we create a **conditional edge**: depending on the output of the previous prompt node, if there are any tool calls we send execution to the tool node; if there are no tool calls, we end execution and return our response to the user.

We're also setting the **entry point** of our graph, which connects the start node to our prompt node.

### Compile and invoke

Finally, I compile the graph and invoke it with *"what's the weather in Yorkshire?"* — and as expected, we're getting out that the weather in New Yorkshire is currently cold and wet.

## Wrap-up

If you're interested in learning more, I have another video on building a research agent. If you really liked this video, I'd appreciate it if you liked and subscribed, as it will motivate me to do more of this content. Thanks for watching — have a good day.
