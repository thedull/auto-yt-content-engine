# Model Context Protocol Clearly Explained: MCP Beyond the Hype

> **Source:** [Model Context Protocol Clearly Explained | MCP Beyond the Hype](https://www.youtube.com/watch?v=tzrwxLNHtRY) — [codebasics](https://www.youtube.com/@codebasics) · 2025-03-20 · 15:04
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **Model Context Protocol (MCP)** is a standardized way for LLMs to interact with tools and knowledge — described as the "USB-C moment" for AI.
- Without MCP, AI engineers write and maintain mountains of custom **glue code** for every tool integration; with MCP, that work is centralized and reused.
- An **MCP client** (like a chatbot) reads a server config, calls `list_tools`, `list_resources`, and `list_prompts` on each server, then feeds those descriptions to the LLM so it can pick the right tool.
- Each MCP server exposes three capabilities: **tools**, **resources**, and **prompts**, all conforming to a standard input schema.
- Servers can be implemented in **TypeScript** or **Python**, and internally just wrap existing APIs (e.g. Google Maps, Yahoo Finance) in a uniform protocol.
- We're still in early days — there's hype, real potential, and uncertainty about how MCP will evolve in practice.

## The evolution of AI applications

There has been a lot of hype around **Model Context Protocol**, and this video is an attempt to provide an extremely simple explanation of MCP, including technical details for AI application builders.

If you think about how AI applications are built, there's a clear evolution:

1. First we started with **LLMs without any tools**.
2. Then we started building **agentic frameworks** where the LLM gets help from tools and knowledge.
3. Now we're entering the realm of **standardized ways of interacting with these tools and knowledge**, so building AI applications becomes easier.

## The Jefferies equity research example

Imagine you're an equity research analyst working at a company like Jefferies, and you want to develop a report comparing **Nvidia** and **Tesla** stocks. The report contains:

- A company description at the beginning.
- Some financial metrics.
- A summary of those metrics.
- Recent news about the companies.

You're a tech-heavy person, so you ask your AI engineer friend at Jefferies to build an AI application that automatically generates this report.

Your AI engineer friend understands LLM capabilities. The LLM:

- **Can** pull the description of Nvidia and Tesla because it's part of the training data.
- **Cannot** pull the latest stock price.
- **Can** summarize information once it's been retrieved.

If you go to ChatGPT and type the question, it actually pulls information by **searching the web** — meaning ChatGPT (referring to GPT-4o) is itself an agent.

So you already know the answer: use **web search**, or call the **Yahoo Finance API** (a "tool"), to retrieve the latest information for the LLM to summarize.

## Glue code: the maintenance nightmare

The AI engineer builds an application where the LLM is the heart, interacting with:

- **Tools** like the Yahoo Finance API or web search.
- **Knowledge** like a private Jefferies database or PDF files.

To wire all that together, the engineer writes **glue code** — the code handling these interactions. This can be:

- An **agentic application** where the glue code is written by an agentic framework like **CrewAI** or **Agno**.
- A **workflow application** where the glue code lives directly in your Python code.

That's just one application. Imagine Jefferies building 20 such apps, and every company in the world building millions — that's a *lot* of glue code.

It's like having an old computer connected via separate wires to keyboards, mice, and other peripherals. Today, things have changed: you have a unified **USB-C port**, you can have a USB hub, and you connect all your devices through that one standard.

**That USB-C moment has arrived for AI — and that is Model Context Protocol.**

## How MCP changes the picture

With MCP, your LLM interacts through Model Context Protocol with different **MCP servers**. In the Jefferies example, Yahoo Finance might build an MCP server, Google Search might build another — each exposing tools, resources, and prompts.

A smart programmer might object: "We're still writing glue code, right?" The answer is yes — but the **ease** of writing that code is increasing, for two reasons:

1. **Maintenance.** In the old model, if Yahoo Finance changes its API, every team has to update their glue code. With MCP's standard protocol, writing and maintaining the code becomes easier.
2. **Centralization.** Yahoo Finance's own folks write the Yahoo Finance MCP server. Now 10,000 programmers worldwide don't have to write that code — they get a ready-made integration and save time.

## Inside an MCP client: list_tools and prompt construction

Suppose you're building a chatbot for your organization that needs to interact with the **Google Maps API** and the **Todoist** app — getting a location and automatically creating a to-do task. The Google Maps and Todoist teams have already built MCP servers.

In the MCP client (your chatbot), you have a **configuration** listing the available servers. When the chatbot starts:

1. For each server in the config, the client makes a `list_tools` call.
2. The Google Maps MCP server returns its capabilities — for example, "I can help you search places," with a detailed description.

That description is **very important** because it guides the LLM in choosing the right tool. The LLM has language intelligence, so just by reading the description it can figure out which tool to call. From the user's natural-language query, it can also extract required parameters like search query, latitude, and longitude.

For example, if you say "I'm going for a hiking trip from Lonavala to this place, show me the places," the LLM:

- Identifies **Lonavala** as a location and maps it to longitude/latitude.
- Determines it needs to call the `maps_search_places` function.

Beyond `search_places`, the client collects all tool descriptions across servers (Google Maps, Todoist, etc.). Once the LLM has all those details, the chatbot constructs a prompt like:

> Tool description: {combined tool descriptions of all available tools}
> Choose the appropriate tool based on the user question.

With the combined tool descriptions and this kind of prompt, the LLM is smart enough to figure out which tool to call, which parameters to extract, how to make the call, read the response, and serve it to the end user.

## Walking through Anthropic's Python SDK example

Using the **MCP client from Anthropic's Python SDK**: when it starts, it iterates through every server in its server configuration, calls `list_tools` on each, collects all tool descriptions, and bundles them into a prompt for the LLM.

Now look at the **MCP server from Google Maps**. When the client makes a `list_tools` request, the server handles it and returns all its tools — `search_places`, `geocode`, and so on.

The `search_places` tool eventually arrives at a function — written in **TypeScript** in this case (servers can be implemented in either TypeScript or Python). From the user question it derives the query, location, and other parameters, and then makes an actual **HTTP call to the Google Maps API**.

So MCP is **not replacing REST or HTTP** — it's a **wrapper**. Internally it calls the Google Maps API and returns the response in a standardized format.

## The standard input schema

If you look at the **input schema** for `search_places`, there's a standard way to provide:

- The tool description.
- The query parameters.

This `inputSchema`, description, and so on are part of the MCP standard. Anyone building an MCP server has to adhere to this schema. That's how MCP achieves a uniform, predictable way of communication.

The TypeScript schema spells out fields like `inputSchema`, type, required parameters, and more — it's worth reading through in the official docs.

## The three MCP server capabilities: tools, resources, prompts

Any MCP server exposes **three capabilities**: **tool**, **resource**, and **prompt**. The Python SDK has simple examples for each.

### Tools

A simple server with a single tool. Looking at the `list_tools` function, it exposes an array containing one tool — for example, `fetch` — with a standard description and standard input schema.

The implementation of `fetch` simply fetches a website by making an HTTP call and returning the information. Pretty straightforward.

### Resources

A **resource** is some kind of knowledge — databases, files, etc. Similar to `list_tools`, the server has a `list_resources` function. When the MCP client starts, it calls `list_tools`, `list_resources`, and `list_prompts` for each server, so it knows the full capabilities of every server it has access to.

In `list_resources`, you can expose a plain file — for example, a file on a drive or in **Amazon S3**.

### Prompts

Imagine you're building an MCP server for Yahoo Finance. As a developer, you know all the prompts AI engineers might need to interact with your API. Through your server, you can provide those prompts — making prompt-writing very easy for the MCP client.

So you have `list_prompts` returning an array of prompts. A simple prompt might take a `context` and a `topic`; the implementation just constructs a prompt string from those two inputs.

## Closing: still early days

That's it — that's Model Context Protocol.

There has been a lot of hype, but we're in early days. MCP has a lot of potential, but how it will evolve and how it will help AI engineers solve real problems is something we'll learn as time goes on.

Some people are super excited; the speaker is excited too, but cautions: we're in early days, there's hype, there's some reality, and we'll have to see how it evolves.

More technical tutorials are coming — including building actual MCP servers and clients. Questions welcome in the comments.
