# Claude Agents SDK BEATS all Agent Framework! (Beginners Guide)

> **Source:** [Claude Agents SDK BEATS all Agent Framework! (Beginners Guide)](https://www.youtube.com/watch?v=i6N8oQQ0tUE) — [Mervin Praison](https://www.youtube.com/@MervinPraison) · 2025-10-04 · 7:04
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **Claude Agent SDK** lets you embed **Claude Code** inside your own Python application to create AI agents that solve complex tasks.
- Walks through four progressively richer examples: a basic agent, an agent using **internal tools** (read/write), an agent with **custom tools** via an **MCP server**, and an agent with extra **Claude Agent options**.
- Setup is just two installs (`claude-code` CLI and `pip install claude-agent-sdk`) plus exporting your `ANTHROPIC_API_KEY` from `platform.claude.com`.
- The core API is the `query` function; richer behavior comes from passing a `ClaudeAgentOptions` object that toggles `allowed_tools`, `permission_mode`, `mcp_servers`, `system_prompt`, `cwd`, etc.
- The author argues Claude Agent SDK beats other agent frameworks because Claude Code is itself autonomous, configurable, and extendable, and the SDK exposes that whole stack as an agent system.

## What the Claude Agent SDK is for

**Claude Agent SDK** lets you create different AI agents and solve complex tasks. Anthropic released the Agent SDK so you can interact with **Claude Code** programmatically. Claude Code is one of the most advanced CLI tools — it can build features from descriptions, debug and fix issues, navigate any codebase, and automate tasks. With the Claude Agent SDK, you can integrate Claude Code inside your own application.

This guide walks through, step by step, how to make your AI application Claude-powered: a basic agent, an agent with internal tools, an agent with custom tools, and Claude Code options.

## Installation and setup

Open a terminal on your computer and run these commands (the author notes the code and commands will be in the video description):

- Install Claude Code via the install command shown in the terminal.
- `pip install claude-agent-sdk` — the main package used to interact with Claude Code.
- `export ANTHROPIC_API_KEY=...` — generate this API key from `platform.claude.com` under **API keys**, paste it after the `=`, and press enter.

Then create a file called `app.py` and open it.

## Step 1: A basic agent

The minimal program looks like this:

- `import asyncio`
- `from claude_agent_sdk import query`
- Define an `async def main()` that asks the question **"Hello, how are you?"** and prints each message it receives.
- The print step runs in a loop that keeps printing as and when it receives a response from the agent. The `query` function is effectively the agent itself.
- Finally, kick it off with `asyncio.run(main())`.

That is literally all the code needed to integrate the Claude Agent SDK into a Python application. Run it with `python app.py`.

In the output you first see a **system message** listing all available tools and commands. Then the **assistant message** comes back: *"Hello, I'm doing well. Thank you. How can I help you today?"* The final block shows total input tokens, output tokens, and total cost.

## Step 2: An agent that uses internal tools

Now change the prompt to: **"Create a file called `greeting.txt` with 'hello Mervin' as the content."** This is a beginner-friendly example of letting the agent use built-in tools.

Key changes:

- Import an extra class: **`ClaudeAgentOptions`**.
- Construct an `options` object that:
  - sets `allowed_tools` to the two tools **`Read`** and **`Write`**, and
  - sets `permission_mode` to **`acceptEdits`**, which lets the agent edit `greeting.txt`.
- Pass this `options` argument into the `query(...)` call. The query function is the single agent, and the options configure it.

That is how you wire up internal tools and permissions. Run `python <file>.py` and watch the output:

1. A system message gets added by default.
2. The agent uses **Claude Sonnet 4.5** and decides to call the `Write` tool with the file path and the content "hello Mervin".
3. It uses a bash command to write `greeting.txt` and reports back that the file was created.

Verifying on disk, `greeting.txt` exists and contains `hello Mervin`.

## Step 3: Adding a custom tool via MCP

To add a custom tool, you set it up as an **MCP server**. In the `options` object, declare an allowed tool named `mcp__tools__greet` and assign an MCP server.

You import two extra symbols from the SDK:

- **`tool`** — to declare a tool.
- **`create_sdk_mcp_server`** — to register the server.

Then:

- Define a small function `greet` decorated as a tool. The tool name is **`greet`** and its description is *"Greet a user. When provided with the name, automatically responds saying hello with the name."* Inside, it just returns a hello string. You can wire this same pattern up to any API or custom tools you have.
- Set up the MCP server: `create_sdk_mcp_server(name="my_tools", version=..., tools=[greet])`.
- Assign that server to `mcp_servers` in the options and allow the `mcp__tools__greet` tool.

The whole file is about **31 lines of code**. The query asks the agent to *"greet Mervin."* Run `python custom_tools.py` and:

- A system message appears, then an assistant message.
- The agent makes a tool call to the custom tool.
- The final response is **"Hello Mervin Praison"** — exactly what the custom `greet` tool returned.

## Step 4: Claude Agent options

The fourth example showcases additional **Claude Agent options**:

- **`system_prompt`**: *"You are an expert Python developer."*
- **`permission_mode`**: `acceptEdits`.
- **`cwd`**: the path where the agent should save its files.

The query is: *"Create a Python web server."* These options are passed into `query(...)` along with the message-printing loop.

The author notes that the official Claude docs list **all available options** for the Claude Agent — only three of them are used here. Run the file with `python <file>.py`:

1. The agent says it will create a simple Python web server.
2. It writes the code to a temporary location at `server.py`.
3. It reports the file was created successfully, and you can see the generated custom-server code.

## Why this beats other agent frameworks

The author's closing argument: Claude Code by itself is already powerful, **completely autonomous, configurable, and extendable**. Wrapping that whole capability as an agentic system through the Claude Agent SDK is what makes it unique compared to other agent frameworks.

This was just a beginner's guide; more videos on the Claude Agent SDK are planned. The author also points to a companion video on the **OpenAI Agents SDK** linked from this one.
