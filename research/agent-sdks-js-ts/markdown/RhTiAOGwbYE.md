# MCP Tutorial: Build Your First MCP Server and Client from Scratch (Free Labs)

> **Source:** [MCP Tutorial: Build Your First MCP Server and Client from Scratch (Free Labs)](https://www.youtube.com/watch?v=RhTiAOGwbYE) — [KodeKloud](https://www.youtube.com/@KodeKloud) · 2025-07-21 · 40:14
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A no-BS, hands-on introduction to the **Model Context Protocol (MCP)** for absolute beginners, motivated by the limits of plain LLMs that can only return text and cannot take action.
- Walks from "why we need MCP" through **AI agents**, then through MCP architecture: **tools**, **resources**, and **prompts** on the server side, and **roots**, **sampling**, and **elicitation** on the client side.
- Demonstrates how to use an existing MCP server inside an IDE (**Roo Code** in a VS Code lab), connecting via `mcp.json` with **stdio** or **HTTP** transports.
- Builds a flight-booking MCP server from scratch in Python with the **FastMCP** SDK, using `@mcp.resource`, `@mcp.tool`, and `@mcp.prompt` decorators.
- Introduces the **MCP Inspector** for testing servers and shows a minimal FastMCP **client** that lists tools, calls a tool, reads a resource, and fetches prompts.
- Ends with the role of **context** for server-to-client messages (progress, info, debug) and previews a follow-up on building AI agents with **LangGraph**.

## Why MCP is needed: from LLMs to AI agents

**Model Context Protocol** — what exactly is it and why is everyone talking about it? This video is a crisp, hands-on introduction for absolute beginners. No prior knowledge required. We'll cover why MCPs are needed in the first place, what MCPs are, the MCP architecture, how to use an existing MCP server, and finally how to build an MCP server and client from scratch. You'll also gain access to a hands-on lab environment with exercises and resources to follow along.

Let's start with something we already know — **ChatGPT**. When you send a message to GPT (the LLM), it responds with generated text or other forms like image, audio, or video. But suppose we were building a "flight GPT" app and I say, "I would like to fly to North London — book a flight for me." LLMs can only respond with generated text or other supported formats. They can't perform any action on their own.

In our application, when I say "I would like to fly to North London," my application should be able to:

- Interact with third-party flight services and retrieve flight details.
- Compare those details against my preferences (cheap vs. luxury, seat preferences, meal preferences).
- Make a decision and not stop until it has retrieved enough information.
- Book the flight and tell me the flight details.

So we need something magical to do that for us. Those are called **AI agents**. An AI agent can interact with third-party tools, has its own memory, interacts with an LLM, and goes back and forth until the task is complete.

If you've ever built workflows in the past — long-running automation scripts like the old **VMware vRealize Orchestrator**, **Microsoft System Center Orchestrator**, modern tools like **Zapier**, or just a series of Python scripts duct-taped together — then you already know how an AI agent works, except now the agent relies on **LLMs** to make decisions: which route to take in a conditional, how many times to iterate in a loop, what third-party tools to interact with, how to process user input, and when the goal is achieved. So an AI agent is just like your old automation script, except now it can think.

## A typical AI agent workflow

A typical AI agent workflow looks like this:

1. The user sends a request to the AI agent.
2. The AI agent interacts with the LLM to extract the right details from the user's input (different users phrase things differently). The agent asks, "Here is the user's input. What does the user mean?" The LLM responds, "The destination is London."
3. The AI agent asks the LLM which third-party tools to interact with. There may be airlines, hotels, rental cars, or other databases. The LLM identifies that flights are the third parties.
4. The AI agent calls the airlines and retrieves flight details.
5. The agent asks the LLM what to do next. The LLM says, "Fetch the preferences from the database."
6. The agent fetches preferences from the database and sends everything to the LLM to make a decision.
7. The LLM identifies the right flight and returns it to the agent.
8. The agent books the flight and sends details back to the user.

A super simplified version of this AI agent in Python (without any framework) would interact with the user, call the LLM to extract origin/destination/date, fetch flight details from third-party sites, fetch preferences from memory, send everything to the LLM for a decision, and finally book the flight via a third-party call. Frameworks like **LangChain** and **LangGraph** make this workflow better — covered in upcoming videos. Note: all code shown in this video is pseudo-code; refer to the actual code in the labs.

## Tools and the explosion of API formats

An agent interacts with third-party platforms through what are known as **tools**. A tool allows the agent to interact with another platform. In our pseudo-code, inside the `fetch_flight_details` function, you'll see a tool call for each airline — passing in query parameters like origin, destination, and date — and we append the results.

If you look closely, each call is different:

- The first one is `API/flights`.
- The second is `flights/list`.
- The third is `list-flights`.

Their responses are different too. Each airline has its own API standard. There are hundreds of airline sites and millions of other third-party sites. If I want my application to interact with all of them, do I need to write all of that code myself? We're in the AI world — I shouldn't have to. So why can't AI just do that for me? Enter **MCPs**, or **Model Context Protocols**. Think of MCPs as a guide for AIs to choose the right APIs and interact with third-party platforms. MCPs provide agents the context they need to interact with third-party platforms.

## MCP architecture and use cases

MCPs follow a **client-server architecture**. Agents use the **MCP client** to interact with a server. MCP clients are usually embedded in coding agents and IDEs like **Cursor**, **Windsurf**, **Claude Code**, or **Claude Desktop**. We could then get these agents to connect to local databases like **MongoDB** or to browser tools.

Sample use cases:

- **UI debugging without MCP**: Ask the AI agent about a recent UI problem; it goes through Git history, backend, and frontend code, and identifies the offending commit.
- **Browser MCP server**: While developing front-end web apps, a browser MCP server gives the AI agent access to console logs and HTML elements to troubleshoot front-end issues.
- **Data engineering**: By giving an MCP server read-only access to data via **Stripe**, **BigQuery**, and **Data Studio** MCP servers, you can ask specific questions about missing data and transactions, and the agent digs into root causes by combining information from these sources.

Who builds MCP servers? If I owned a business or application and wanted AI agents to interact with my app, I would build and maintain my own MCP server. Many vendors are announcing MCP servers for their services. The **Model Context Protocol** repository on GitHub lists official integrations. MCP servers can be built by anyone who knows how the APIs work. For companies that haven't built official servers, community members have built their own — use them at your own risk, since there's no guarantee they're tested or up to date.

## What MCP actually is: a specification

**MCP** stands for **Model Context Protocol**:

- **Model** — the AI itself, the LLMs.
- **Context** — giving the model context about a third party.
- **Protocol** — a set of standards.

So MCP is just a set of standards defining how AI applications can work with each other. At **modelcontextprotocol.io**, under specification, you'll find rules such as:

- Communication between server and client must use **JSON-RPC** format.
- The connection must be **stateful**.
- The MCP server must offer any of: **resources**, **prompts**, and **tools** to clients.
- Clients must offer **sampling**, **roots**, and **elicitation** features to servers.

Anyone can build an MCP server as long as they adhere to these standards. If a server follows the spec, any client can use it.

## The lab environment and Roo Code

The lab interface has instructions on the left and a **VS Code Server** on the right with terminal access — an actual system hosted on the labs. We'll get started with the **Roo Code** AI assistant, a VS Code extension that's an alternative to Cursor or Windsurf. Click the kangaroo button to get a chat interface.

Configuration steps in the lab:

1. Open a new terminal in VS Code and inspect `.bash_profile` to find the **OpenAI base URL** and **OpenAI API key** provided by the lab.
2. In Roo Code, set the API provider to **OpenAI Compatible**, paste the base URL, paste the API key, and set the model to the **DeepSeek free model** as given.
3. Click **Let's Go** to set up Roo Code, then test with the sample prompt to confirm responses.

## MCP architecture deep dive: tools, resources, and prompts

To truly understand an MCP server, first imagine MCP servers don't exist and I'm building a client to interact with a server. What would I need?

**Tools.** I'd need to know what APIs and capabilities the server supports — usually from API documentation. In MCP, the server lists all capabilities as a list of **tools** in a specific format. Each tool should have a description, an input schema, and an output schema.

**Resources.** I may need data such as refund policies, city guides, or FAQs to support decision-making. For example, if the user prefers only flight providers offering refunds, that information helps. These are **resources**. The MCP spec defines a clear structure: a **URI** pointing to the resource, a **name**, **title**, and **description**. The URI could be HTTPS, a file on the file system, or a Git repository.

**Prompts.** Using tools, the agent calls the LLM. You could leave it to the agent's developer to craft the prompt, but as the MCP server developer you know the better prompt — for example: *"You are a travel assistant. When the user asks about flights, you must call the `search_flights` tool with origin, destination, and date, format all dates as YYYY-MM-DD, and be helpful and concise."* These are **prompts** — the third type of entity an MCP server can expose. The spec defines a format with a name, title, description, and arguments per prompt.

## Transport: JSON-RPC, stdio, and HTTP

How do server and client communicate? Via **JSON-RPC**:

- **JSON** — JSON.
- **RPC** — Remote Procedure Call.

Together, JSON-RPC defines how a client can invoke a method remotely, pass parameters, and receive a response. For example, a server has an `add` method; a client invokes it remotely.

A client request includes:

- `jsonrpc` version (must be `"2.0"`).
- `method` — the method to call on the server.
- `params` — list of parameters.
- `id` — a number.

A server response includes:

- `jsonrpc` version (`"2.0"`).
- `result`.
- `id`.
- An optional `error` field.

JSON-RPC is intentionally simple and **stateless**, and it does not define how data is transmitted — that's up to us: HTTP, WebSockets, TCP/UDP, Unix sockets, message queues, **stdio**, etc. **MCP supports HTTP and stdio** as transport mechanisms.

## Using an existing MCP server

In the past, you wrote code to interact with an API server directly. With MCP, you call the MCP server and the MCP server handles the API endpoint. Your tool can query the MCP server to discover its capabilities, then make a tool call.

Where is the MCP server hosted?

- **Locally** — run a local instance and connect via **stdio** or HTTP.
- **Remote** — hosted by your organization (single internal MCP server) or by a vendor for AI agents to interact with their service. In that case, connect via HTTP.

To configure an MCP server locally in IDEs like Cursor, Windsurf, or Claude Code, they ship with an `mcp.json` file. It has a top-level `mcpServers` object containing a list of servers. For a `flight-mcp` server, you provide the **command** and **arguments** to start it, plus optional environment variables. The IDE then starts an instance of the MCP server in **stdio mode** — the simplest, fastest way for two local processes to talk without HTTP or sockets. Once connected, the agent lists available tools and you can chat with it.

If you run your own server instance (perhaps to share between multiple IDEs), start the server first, then configure the client to connect via HTTP using a URL. For a remotely hosted vendor server, change the URL to point to the remote endpoint — but take care of **authentication, authorization, data privacy, and trustworthiness**, because you're sending data to an external party.

If you're building your own AI agent or app, use the **Python SDK** and integrate the MCP server interaction into your app.

## Lab: connecting to an existing MCP server

The lab walks through:

- A multiple-choice question on transport modes — answer: **HTTP and stdio**.
- Identifying files in the `flight-booking-server` directory — answer: **`server.py` and `pyproject.toml`**.
- Exploring `server.py` (no need to fully understand yet).
- Confirming Roo Code is working with a test prompt.
- Connecting to the MCP server: in Roo Code, open **MCP servers** at the top, click **Edit Project MCP**, and paste the provided MCP configuration. The command is `uv` with arguments `run python server.py`. Refresh MCP servers; the server appears with a green status indicator and exposes its tools and resources.
- Activating and testing: a sample prompt asks Roo Code to *"Search for flights from LAX to JFK using the flight booking server."* Roo Code requests approval, you approve, and it completes the task — confirming the MCP server works.

## Building an MCP server: the design

For our flight-booking use case, the three components map to:

- **Resources** — list of airports and details, flight statuses, gates, weather, booking information, gate information, policies, loyalty programs.
- **Tools** — search for flights, get flight details, create and edit bookings, check in, select seats, add baggage.
- **Prompts** — finding the best flight, optimizing budget, handling disruption.

The Model Context Protocol site has handy SDKs alongside the spec, under the **SDK** section.

## Building with the Python SDK (FastMCP)

The overall approach with the Python SDK:

1. Import the **FastMCP** library and initialize an MCP server.
2. Define **tools**, **resources**, and **prompts**.
3. Run the server, specifying a **transport** — `stdio` or HTTP. Default is stdio; switch to HTTP if needed.

**Resources** are normal functions. For example, `get_airport_info` returns airport coords. Add an `@mcp.resource` decorator to make it a resource. Other resources follow the same pattern.

**Tools** are functions that accept parameters from clients, look up an internal database, and return results. Adding `@mcp.tool` makes it an MCP tool.

**Prompts** are predefined prompts that help the AI select the best flight based on conditions. The MCP server developer knows best how to prompt. Annotate the function with `@mcp.prompt`.

When creating the FastMCP server, options include a **stateful server** (default) or a **stateless server** by passing `stateless_http=True`. While running, set transport to `stdio` or `http` and specify host and port — or more specifically, use **streamable HTTP** that can stream output.

## Lab: building the MCP server

The lab includes multiple-choice review questions — for example, the three main features exposed by an MCP server are **resources, tools, and prompts** (not transport protocols).

Hands-on tasks:

1. **Initialize the project**: `cd /home/lab` and run `uv init flight-booking-server`. This creates a directory with `main.py` and a README.
2. **Add the MCP CLI**: `cd flight-booking-server && uv add mcp[cli]` — installs everything needed to build the MCP server.
3. **Add `@mcp.resource`**: in `server.py`, find `get_airports` and add `@mcp.resource("file://airports")` above it.
4. **Add `@mcp.tool`**: do the same for `search_flights` and `create_booking`. The Solutions tab is available if you get stuck.
5. **Add `@mcp.prompt`**: annotate the prompt functions.
6. **Wire up to Roo Code**: open the MCP servers panel, click **Edit Project MCP**, paste the provided `mcp.json` referencing `flight-booking` with command/arguments and the working directory matching the project. Save, refresh MCP servers, confirm a green status, and inspect tools and resources (you should see the `file://airports` resource).
7. **Test**: a prompt asks Roo Code to find flights — it requests permission to use the MCP tool, you approve, and it returns two flights from **LAX** to **JFK** with their details, confirming the server is being used.

## The MCP Inspector

Before writing a client, you can test the server with the **MCP Inspector**:

- Start it with `npx @modelcontextprotocol/inspector`.
- The command starts a web server; open the URL printed in the output.
- The MCP Inspector is a web interface where you provide the URL of your MCP server and then list **prompts**, **tools**, and **resources** using the navigation bar.

## Building an MCP client

A lot of agents support MCP clients automatically — IDE tools like Cursor and Claude Code only need an `mcp.json` pointing to the servers. But if you're building your own AI agent, you may want to build the client from scratch.

A super-simple FastMCP client example:

- Use the same FastMCP client library.
- Connect to the server running on **port 8080** over HTTP.
- List available tools with `list_tools`.
- Call a specific tool, e.g. `search_flights`, passing origin and destination.
- Read a particular resource using `read_resource`.
- Get prompts using `get_prompts`.

## Server-side context: progress, info, and debug

On the server side we have **resources, tools, and prompts**; on the client side we have **roots, sampling, and elicitation**. But first — **context**.

Context allows the server to talk back to the client — for updates, progress sharing, etc. If the client initiates a long-running booking, the server may want to send periodic updates before the actual response. To use context:

- Import `Context` on your server.
- Use `info` to send information-level messages to the client.
- Call `report_progress` to send progress updates.
- Use `debug` to send debug messages.

## Client-side features: roots, sampling, elicitation

**Roots.** Think of roots as folders on the client machine that the MCP server is allowed to see or interact with — like shared folders the client exposes to the server from its local file system. Some MCP tools — code linters, compilers, file readers — need access to real files. For security, the server shouldn't have access to the entire machine, so the client says, "Here are the safe folders (roots) I'm willing to expose." On the client side, define allowed roots and pass them when creating the client session. On the server side, use `context.session.list_roots()` to retrieve the allowed list.

**Sampling.** Sometimes the server wants to interact with the LLM — for example, to summarize resources. The server does **not** call the LLM directly, because the server may be used by different clients and the client should control model selection, token limits, etc. The server is purely logic and tool definitions; the client takes charge of LLM interactions. To implement: define a **sampling handler** function on the client and pass it when creating the client object. On the server side, use `context.session.create_message()` to send a sampling message and return the response.

**Elicitation.** Sometimes the server wants to interact with the end user for more information — for example, asking for confirmation before booking the best flight. To implement: on the server side, call the elicitation method with a message to the client; the client must have an **elicitation callback handler** defined that fetches a response from the user, and you specify that handler when creating the client session.

## What's next

That's all for this video. In the next video, we'll discuss **AI agents in action** and build our own custom AI agent using **LangGraph**. Subscribe to be notified when the new video is out.
