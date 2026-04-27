# LangChain vs LangGraph: A Tale of Two Frameworks

> **Source:** [LangChain vs LangGraph: A Tale of Two Frameworks](https://www.youtube.com/watch?v=qAF1NjEVHhY) — [IBM Technology](https://www.youtube.com/@IBMTechnology) · 2024-11-04 · 9:54
> *Transcript generated via `youtube-captions (en-US)`.*

## TL;DR

- **LangChain** and **LangGraph** are both open source frameworks for building applications with large language models, but they target different workflow shapes.
- **LangChain** chains together high-level components (document loaders, text splitters, prompts, LLMs, memory, agents) to execute a sequence of functions — essentially a directed acyclic graph (DAG) of forward-moving steps.
- **LangGraph** is a specialized library within the LangChain ecosystem for building **stateful, multi-agent systems** with **nonlinear, looping workflows**, modeled as nodes, edges, and shared state.
- LangChain has limited persistent state across runs (with memory components for some interaction state); LangGraph treats **state as a core component** that all nodes can access and modify.
- Use **LangChain** for sequential pipelines like retrieve → summarize → answer; use **LangGraph** for complex, adaptive systems like virtual assistants that maintain context over long conversations and route between many actions.

## What is LangChain?

At its core, **LangChain** is a way to build **LLM-powered applications** by executing a sequence of functions in a chain.

Imagine we're building an application, and the first thing it needs to do is retrieve some data from a website. Once we've done that, we move on to stage two: summarize the data we retrieved. Then finally, we use that summary to do something — specifically, to answer user questions. So the workflow is **retrieve, summarize, and answer**, and we can use LangChain to help us do this.

### The retrieve component

The retrieve component might consist of a LangChain component called a **document loader**, which is used to fetch and load content from various data sources. If some of those documents are large, we might choose to use a **text splitter**, another LangChain component that splits text into smaller, semantically meaningful chunks.

### The summarize component

To summarize, we would use a **chain**, and the chain orchestrates the summarization process. That might include constructing a **prompt component** to instruct an LLM to perform the summarization, and an **LLM component** to pass that request to the large language model of our choosing.

### The answer component

For answer, we would build another chain. This chain might include a **memory component** — another component of LangChain — used to store conversation history and context. We'd throw in another prompt component and another LLM component to generate the answer based on the summary and the recorded context.

The cool thing here is that the LLM used for the answer component may be a completely different large language model from the one used in the summarize component. LangChain's modular architecture lets us build complex workflows by combining these high-level components.

## What is LangGraph?

**LangGraph** is a specialized library within the LangChain ecosystem, specifically designed for building **stateful multi-agent systems** that can handle **complex, nonlinear workflows**.

Consider a **task management assistant agent**. The workflow involves processing user input, and from there we want to be able to **add tasks**, **complete tasks**, and **summarize tasks**. That's the architecture of what we're trying to build.

### Nodes, edges, and state

LangGraph helps us create this as a **graph structure**, where each action is a **node** — add tasks, complete tasks, summarize are all nodes — and the transitions between them are known as **edges**.

The central node here is the **process input node**. That's where the user input comes in, and it uses an LLM component to understand user intent and route to the appropriate action node.

There's another component that's quite central to this: the **state component**. The state component is used to maintain the task list across all interactions:

- The **add tasks** node adds new tasks to the state.
- The **complete task** node marks tasks as finished.
- The **summarize** node uses an LLM to generate an overview of current tasks.

All nodes can access and modify the state, allowing for contextual, stateful interactions. The graph structure lets the assistant handle various user requests in any order, always returning back to the process input node after the action is complete. LangGraph's architecture lets us create flexible, stateful agents that can maintain context over extended interactions.

## Direct comparison

Let's directly compare LangChain and LangGraph across a number of dimensions.

### Primary focus

- **LangGraph**: create and manage **multi-agent systems and workflows**.
- **LangChain**: provide an abstraction layer for **chaining LLM operations** into large language model applications.

### Structure

**LangChain** adopts — no surprise here — a **chain structure**, which acts as a **DAG** (directed acyclic graph). Tasks are executed in a specific order, always moving forward. For example, we start with task one, then branch to tasks two and three, and come back to a central task four. This process is great when you know the exact sequence of steps that are needed.

**LangGraph's** graph structure, on the other hand, is different because it allows for **loops and revisiting previous states**. We might have state A which can go backwards and forwards with state B and state C. This is beneficial for interactive systems where the next step might depend on evolving conditions or user input.

### Components

**LangChain** uses a bunch of components, many of which we've already mentioned:

- **Memory**
- **Prompt**
- **LLM** (how we actually pass things to the large language model)
- **Agent** (forms chains between all of these things)

**LangGraph** uses a different set of components:

- **Nodes**
- **Edges**
- **States**

These are all part of a graph.

### State management

**LangChain** has somewhat limited state management capabilities. It can pass information forth through the chain, but it doesn't easily maintain a persistent state across multiple runs. That said, LangChain does have memory components that can maintain some state across interactions.

**LangGraph's** state management is more robust, because state is a core component that all nodes can access and modify, allowing for more complex, context-aware behaviors.

### Use cases

**LangChain** really excels at sequential tasks — like a process that retrieves data, then processes it, then outputs a result. That said, LangChain is able to handle non-sequential tasks to some extent with its agents feature.

**LangGraph's** wheelhouse is scenarios that have a much more complex nature: complex systems requiring ongoing interaction and adaptation. For example, a virtual assistant that needs to maintain context over long conversations and handle varying types of requests.

## Wrap-up

So that's **LangChain** and **LangGraph** — two powerful frameworks for building applications that make use of large language models.
