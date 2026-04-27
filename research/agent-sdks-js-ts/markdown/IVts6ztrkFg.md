# What are Deep Agents?

> **Source:** [What are Deep Agents?](https://www.youtube.com/watch?v=IVts6ztrkFg) — [LangChain](https://www.youtube.com/@LangChain) · 2025-11-24 · 7:42
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **Deep Agents** is a new open-source package from LangChain for building long-running, "deeper" agents like Claude Code, Manus, or Deep Research.
- The length of tasks an agent can complete is roughly doubling every seven months, pushing the need for agents that can sustain long trajectories.
- Successful long-running agents converge on a small number of **atomic tools**: file system access, a shell/bash tool, planning, and sub-agent delegation.
- Deep Agents is an **opinionated harness** built on top of **LangChain** (abstractions) and **LangGraph** (runtime), bundling these tools with detailed prompting.
- Version 0.2 adds pluggable backends (use your real file system, not just a virtual one) and middleware/hooks for things like context compression and prompt caching.
- The new **Deep Agents CLI** runs a deep agent on your local machine, similar to Claude Code, with skills, memory, a shell tool, and a web fetch tool.

## Why "deep" agents?

Hey, this is Lance. I want to talk a bit about the **Deep Agents** package that we recently released.

The length of tasks that an agent can take on is doubling every seven months, and we see numerous examples of popular long-running agents like **Claude Code**, **Deep Research**, and **Manus**. The average Manus task, for example, can be up to 50 different tool calls. So it's increasingly clear that agents are needed to do what we might consider deeper work — more challenging tasks that take longer periods of time. Hence the term "deep."

## The pattern: a few atomic, powerful tools

One of the interesting things you can see when you look at agents like Manus or Claude Code is that they don't actually use that many different tools. They focus on a small number of **atomic tools** that do some very basic but powerful actions.

Notably:

- **File system access** — tools for file manipulation.
- **A bash / shell tool** — to execute scripts.

This is extremely useful for **offloading context** over the course of long agent trajectories, and for performing actions through script execution.

Similarly, long-running agents typically involve some kind of **planning**. Claude Code has a planning tool. Manus also has the notion of planning.

Both Claude Code and Manus also use **sub-agents for context isolation**. If there's a specific task, you can spawn a sub-agent with its own independent context window. It can perform that task and return results back to the parent agent — an extremely useful way to preserve the parent's context window.

In all these cases, **prompting is still extremely relevant**. The Claude Code system prompt, for example, is publicly available — it's quite long and extensive.

So the recurring pattern is: a small number of atomic tools that can do a broad set of actions — sub-agent delegation for context isolation, planning for long-running tasks, and access to a computer through the file system and shell — all extremely general and useful, and guided by often fairly detailed prompting.

## How Deep Agents fits with LangChain and LangGraph

Because these tools are so general, we've rolled them into the **Deep Agents** package. It's fully open source and can be used to build many different types of agents.

How does this differ from LangChain and LangGraph?

- **LangGraph** provides a core agent **runtime**. This gives low-level infrastructure: checkpointing, memory, support for human-in-the-loop — all built into the LangGraph framework itself. Its abstractions are very simple, like nodes and edges, and can be used to build many different types of agents and workflows.
- **LangChain** provides generally useful **abstractions** — for accessing chat models, defining tools, and so on. It can be used to build many different types of agents.
- **Deep Agents** is an opinionated **agent harness** built on top of those two, implementing a specific set of tools (planning, sub-agent delegation, file system manipulation, bash / general code execution) baked in with opinionated prompting to govern how they should be used.

In short: LangGraph is extremely low-level. LangChain has general abstractions. Deep Agents is one particular, opinionated agent harness with a few specific tools built into it.

## Principles for working with Deep Agents

It is clear that agents are becoming autonomous quite quickly — the task length agents can undertake is doubling roughly every seven months. As models get increasingly capable, a small set of atomic tools turns out to be very general:

- The ability to use a **shell tool**.
- The ability to **manipulate files**.
- The ability to **delegate tasks** and **plan**.

So it's typically beneficial to move a lot of the complexity of your application into the **prompting itself**. We're seeing an increasingly narrow set of capable tools paired with highly sophisticated instructions. If you look at Claude Code, there are fewer than 20 tools but a very extensive system prompt instructing how to use those very general tools in the best way.

The second main idea is to **really use the file system**. Not only can the file system be used to offload context from the LM's context window — for example, write a plan and pull it back in later (we see that with Manus) — but it can also be used to **store scripts the agent can call**. We've seen this more recently with the idea of **Claude Skills**: give the agent access to a file system with directories of different skills, and it can call them via its bash tool. With access to a computer — effectively a file system and a bash tool — an agent can perform a very large number of actions.

And of course, **sub-agent delegation** can be very useful. For example, you see Claude call the **task tool** for certain things that are more token-heavy and are best isolated in their own context window.

## What's new: Deep Agents 0.2 and the CLI

We've launched the **Deep Agents CLI**, which is just a deep agent running on your local machine — much like Claude Code — with access to your local file system.

We've also launched **Deep Agents 0.2**, which introduces:

- **Pluggable backends** — rather than just using a virtual file system (which is just the LangGraph state object), you can actually use your local file system.
- **Middleware** — think of middleware as **hooks**: basic code that runs at specific points within the agent life cycle to do different things. Examples:
  - **Context compression**: once the messages list grows sufficiently long, apply compression to summarize it (we see this with Claude Code).
  - **Tool handlers** for file system tools as well as for the sub-agent tool.
  - **Prompt caching** — a very useful way to save latency and cost by caching input tokens that aren't changing across different agent invocations.

The CLI lets you run a custom deep agent directly from the terminal. It's a lot like Claude Code: it gives the deep agent access to your own file system with support for skills and memory.

## Wrap-up

Deep Agents is an opinionated agent harness built on top of LangChain and LangGraph. It uses a few atomic tools that we've seen very commonly with agents like Manus and Claude Code:

- Access to **sub-agents**.
- Use of the **file system**.
- Use of a **shell tool**.
- Use of **planning**.

It bakes all these into the harness for you, but it can be easily customized by adding your own instructions or even adding your own tools, with support for **MCP**.

We've also launched the **Deep Agent CLI** — a deep agent that can run locally on your machine with access to your local file system, much like Claude Code. In addition to the core tools built into the Deep Agents package, the CLI ships with support for **memory**, **skills**, a **shell tool**, a **web fetch tool**, and a few other things that are particularly useful when running locally on your own machine.

All this is fully open source, and we strongly encourage contributions and welcome any feedback. Thanks.
