# What is MCP? Integrate AI Agents with Databases & APIs

> **Source:** [IBM Technology — What is MCP? Integrate AI Agents with Databases & APIs](https://www.youtube.com/watch?v=eur8dUO9mvE)
> **Channel:** [IBM Technology](https://www.youtube.com/@IBMTechnology)
> **Uploaded:** 2025-02-19 · **Duration:** 3:46

## TL;DR

**MCP (Model Context Protocol)** is a new open-source standard for connecting AI agents to external data sources such as **databases**, **APIs**, and **local files/code**. It defines three core components — a **host** (which contains one or more **clients**), a **server**, and a **transport-layer protocol** that links them. The host (e.g., a chat app or IDE code assistant) asks the MCP server which tools are available, forwards that list plus the user's question to an **LLM**, then executes whichever tool the LLM selects by calling the appropriate MCP server. The server runs the actual database query, API call, or code execution and returns the result, which the LLM uses to produce the final answer. MCP is recommended for anyone building — or whose clients are building — agents.

## Introduction to MCP

If you're building AI agents, you've probably heard about **MCP**, or **Model Context Protocol**. MCP is a new **open source standard** to connect your agents to data sources such as **databases** or **APIs**.

## Core Components of MCP

MCP consists of multiple components. The most important ones are:

- The **host**
- The **client**
- The **server**

So let's break it down.

### The MCP Host and Client

At the very top you would have your **MCP host**. Your MCP host will include an **MCP client** — and it could also include **multiple clients**.

The MCP host could be:

- An application such as a **chat app**
- A **code assistant in your IDE**
- And much more

### The MCP Server

The MCP host will connect to an **MCP server**. It can actually connect to **multiple MCP servers** as well. It doesn't matter how many MCP servers you connect to your MCP host or client.

### The MCP Protocol (Transport Layer)

The MCP host and servers will connect to each other through the **MCP protocol**. The MCP protocol is a **transport layer in the middle**.

Whenever your MCP host or client needs a tool, it's going to connect to the MCP server. The MCP server will then connect to, for example:

- A **database** — and it doesn't matter if this is a **relational database** or a **NoSQL database**
- **APIs** — and the API standard doesn't really matter either
- **Data sources** such as a **local file type** or **code** — especially useful when you're building something like a code assistant in your IDE

## MCP in Practice: An Example

Let's look at an example of how to use MCP in practice. We still have the three components:

- Our **MCP host and client**
- A **large language model (LLM)**
- Our **MCP servers** — these could be multiple MCP servers or just a single one

### Step-by-Step Flow

Let's assume our MCP client and host is a **chat app**, and you ask a question such as:

- *"What is the weather like in a certain location?"*
- *"How many customers do I have?"*

The flow proceeds as follows:

1. **Retrieve available tools** — The MCP host will need to retrieve tools from the MCP server. The MCP server will then respond and tell which tools are available.
2. **Send question + tools to the LLM** — From the MCP host, you would then connect to the large language model and send over your question plus the available tools.
3. **LLM selects tools** — If all is well, the LLM will reply and tell you which tools to use.
4. **Call the MCP server(s)** — Once the MCP host and client know which tools to use, it knows which MCP servers to call. When it calls the MCP server in order to get a tool result, the MCP server will be responsible for **executing something that goes to a database, to an API, or a local piece of code**. There could also be **subsequent calls** to MCP servers.
5. **Return the response** — The MCP server will reply with a response, which you can send back to the LLM.
6. **Final answer** — Finally, you should be able to get your final answer based on the question that you asked in the chat application.

## Why MCP Matters

If you are building agents, I'd really advise you to **look at the MCP protocol**. The MCP protocol is a new standard which will help you to connect your data sources — via an MCP server — to any agent.

Even though you might not be building agents yourself, your **client** might be building agents.
