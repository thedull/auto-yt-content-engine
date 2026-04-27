# Building AI Agents with Claude Agent SDK, Google ADK, LangChain, and LangGraph (JS/TS) — Research Summary

> **Scope:** 20 YouTube videos on agent SDKs and frameworks (Claude Agent SDK, Google ADK, LangChain, LangGraph, MCP), ranked by views + likes.
> Generated 2026-04-26.

## Sources

- [Agentic Framework LangGraph explained in 8 minutes | Beginners Guide](https://www.youtube.com/watch?v=1Q_MDOWaljk) — W.W. AI Adventures · 2024-12-23 · 8:04
- [What is LangChain?](https://www.youtube.com/watch?v=1bUy-1hGZpI) — IBM Technology · 2024-03-15 · 8:07
- [Claude's Model Context Protocol is here... Let's test it](https://www.youtube.com/watch?v=HyzlYwjoXOQ) — Fireship · 2025-03-31 · 8:08
- [What are Deep Agents?](https://www.youtube.com/watch?v=IVts6ztrkFg) — LangChain · 2025-11-24 · 7:42
- [MCP Tutorial: Build Your First MCP Server and Client from Scratch (Free Labs)](https://www.youtube.com/watch?v=RhTiAOGwbYE) — KodeKloud · 2025-07-21 · 40:14
- [The Ultimate MCP Crash Course - Build From Scratch](https://www.youtube.com/watch?v=ZoZxQwp1PiM) — Web Dev Simplified · 2025-07-15 · 1:15:25
- [Mastra: The AI Framework That Changes Everything](https://www.youtube.com/watch?v=_dG8iZgmicQ) — Better Stack · 2025-10-16 · 5:20
- [Google Agent Development Kit (ADK): How to deploy Your First Agent to Vertex AI Agent Engine](https://www.youtube.com/watch?v=bPtKnDIVEsg) — aiwithbrandon · 2025-04-19 · 37:13
- [LangGraph Explained for Beginners](https://www.youtube.com/watch?v=cUfLrn3TM3M) — KodeKloud · 2025-08-22 · 13:21
- [What is MCP? Integrate AI Agents with Databases & APIs](https://www.youtube.com/watch?v=eur8dUO9mvE) — IBM Technology · 2025-02-19 · 3:46
- [Claude Agents SDK BEATS all Agent Framework! (Beginners Guide)](https://www.youtube.com/watch?v=i6N8oQQ0tUE) — Mervin Praison · 2025-10-04 · 7:04
- [LangGraph Complete Course for Beginners – Complex AI Agents with Python](https://www.youtube.com/watch?v=jGg_1h0qzaM) — freeCodeCamp.org · 2025-05-20 · 3:09:51
- [MCP Tutorial: Build Your First MCP Server](https://www.youtube.com/watch?v=jLM6n4mdRuA) — codebasics · 2025-04-18 · 13:52
- [Context Engineering Clearly Explained](https://www.youtube.com/watch?v=jLuwLJBQkIs) — Tina Huang · 2025-08-01 · 12:48
- [LangGraph vs LangChain vs LangFlow vs LangSmith : Which One To Use & Why?](https://www.youtube.com/watch?v=ldBsvhjEREc) — FuturMinds · 2024-08-22 · 9:44
- [LangChain vs LangGraph: A Tale of Two Frameworks](https://www.youtube.com/watch?v=qAF1NjEVHhY) — IBM Technology · 2024-11-04 · 9:54
- [Model Context Protocol Clearly Explained | MCP Beyond the Hype](https://www.youtube.com/watch?v=tzrwxLNHtRY) — codebasics · 2025-03-20 · 15:04
- [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0) — Zen van Riel · 2025-11-20 · 11:45
- [LangChain Explained in 10 Minutes (Components Breakdown + Build Your First AI Chatbot)](https://www.youtube.com/watch?v=xTmU8ZImUO8) — KodeKloud · 2025-08-19 · 12:27
- [LangChain Master Class For Beginners 2024 [+20 Examples, LangChain V0.2]](https://www.youtube.com/watch?v=yF9kGESAi3M) — aiwithbrandon · 2024-06-22 · 3:17:50

## Themes

**The agentic loop is the universal primitive.** Across the corpus, every framework — whether Claude Agent SDK, LangGraph, Mastra, ADK, or "no framework at all" — ultimately implements the same shape: an LLM is called with a system prompt plus a list of tools described as JSON schemas, the model returns structured tool-call requests, host code validates and executes them, and the result is fed back until a stop condition is met. [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0) reduces it to "a `for` loop"; [LangGraph Explained for Beginners](https://www.youtube.com/watch?v=cUfLrn3TM3M) and [LangGraph Complete Course for Beginners](https://www.youtube.com/watch?v=jGg_1h0qzaM) rebuild the same loop as a graph with looping conditional edges; [Claude Agents SDK BEATS all Agent Framework!](https://www.youtube.com/watch?v=i6N8oQQ0tUE) hides it inside a `query()` call but still exposes `allowed_tools`, permission modes, and tool results.

**MCP is the connective tissue.** Seven of the twenty videos focus directly on Model Context Protocol, and several others integrate it. The pattern is the same: a server exposes `tools`, `resources`, and `prompts` (with optional `sampling`); a client (Claude Desktop, Cursor, GitHub Copilot, custom CLI) connects via stdio or HTTP; Zod or JSON Schema validates arguments so the LLM cannot hallucinate parameters. [The Ultimate MCP Crash Course](https://www.youtube.com/watch?v=ZoZxQwp1PiM), [Claude's Model Context Protocol is here](https://www.youtube.com/watch?v=HyzlYwjoXOQ), [MCP Tutorial: Build Your First MCP Server and Client](https://www.youtube.com/watch?v=RhTiAOGwbYE), [Model Context Protocol Clearly Explained](https://www.youtube.com/watch?v=tzrwxLNHtRY), and [What is MCP?](https://www.youtube.com/watch?v=eur8dUO9mvE) all converge on this architecture. MCP is repeatedly described as the "USB-C port for AI."

**Graphs vs. chains: the LangChain/LangGraph split.** A whole sub-cluster of videos defines its identity by contrasting linear chains with stateful graphs. [LangChain vs LangGraph](https://www.youtube.com/watch?v=qAF1NjEVHhY), [LangGraph vs LangChain vs LangFlow vs LangSmith](https://www.youtube.com/watch?v=ldBsvhjEREc), [Agentic Framework LangGraph explained in 8 minutes](https://www.youtube.com/watch?v=1Q_MDOWaljk), and [LangGraph Explained for Beginners](https://www.youtube.com/watch?v=cUfLrn3TM3M) all draw the same line: chains for deterministic DAG pipelines (retrieve → summarize → answer), graphs for cyclic, stateful, multi-agent flows where the LLM picks the next node.

**Context engineering replaces prompt engineering for agents.** [Context Engineering Clearly Explained](https://www.youtube.com/watch?v=jLuwLJBQkIs) and [What are Deep Agents?](https://www.youtube.com/watch?v=IVts6ztrkFg) push the same theme: as agents run for tens or hundreds of tool calls, the bottleneck becomes packing the right info into the context window. Deep Agents formalizes this with file-system offloading, planning tools, and sub-agent delegation — the same atomic toolkit Claude Code itself uses.

**TypeScript/JavaScript is a first-class option but Python dominates the tutorial corpus.** Native TS/JS demos appear in [The Ultimate MCP Crash Course](https://www.youtube.com/watch?v=ZoZxQwp1PiM) (`@modelcontextprotocol/sdk`), [Claude's Model Context Protocol is here](https://www.youtube.com/watch?v=HyzlYwjoXOQ) (Deno), and [Mastra](https://www.youtube.com/watch?v=_dG8iZgmicQ) (`@mastra/core`). Almost every other video uses Python, while noting that LangChain, LangGraph, ADK, and the MCP SDK ship JS counterparts.

**Working memory, persistence, and human-in-the-loop are now table-stakes.** Memory shows up in [LangChain Master Class](https://www.youtube.com/watch?v=yF9kGESAi3M) (Firestore-backed history), [Mastra](https://www.youtube.com/watch?v=_dG8iZgmicQ) (LibSQLStore + working-memory templates), [LangGraph Complete Course](https://www.youtube.com/watch?v=jGg_1h0qzaM) (`add_messages` reducer), and [What are Deep Agents?](https://www.youtube.com/watch?v=IVts6ztrkFg). Human-in-the-loop is highlighted by [Agentic Framework LangGraph](https://www.youtube.com/watch?v=1Q_MDOWaljk) and the freeCodeCamp Drafter project.

## Consensus

- **MCP servers expose three core primitives — tools, resources, prompts (plus sampling).** Backed by [The Ultimate MCP Crash Course](https://www.youtube.com/watch?v=ZoZxQwp1PiM), [MCP Tutorial: Build Your First MCP Server and Client](https://www.youtube.com/watch?v=RhTiAOGwbYE), [Model Context Protocol Clearly Explained](https://www.youtube.com/watch?v=tzrwxLNHtRY), [Claude's MCP is here](https://www.youtube.com/watch?v=HyzlYwjoXOQ), [What is MCP?](https://www.youtube.com/watch?v=eur8dUO9mvE), [MCP Tutorial: Build Your First MCP Server](https://www.youtube.com/watch?v=jLM6n4mdRuA). Tools are the most-used; resources are read-only (GET-like); prompts are templated user/system messages.
- **Zod is the de facto schema validator for TS-based agents and MCP servers.** [The Ultimate MCP Crash Course](https://www.youtube.com/watch?v=ZoZxQwp1PiM), [Claude's MCP is here](https://www.youtube.com/watch?v=HyzlYwjoXOQ), and [Mastra](https://www.youtube.com/watch?v=_dG8iZgmicQ) all use Zod to prevent the LLM from hallucinating parameters.
- **stdio is the right transport for local clients; HTTP/SSE for remote.** Stated in [The Ultimate MCP Crash Course](https://www.youtube.com/watch?v=ZoZxQwp1PiM), [Claude's MCP is here](https://www.youtube.com/watch?v=HyzlYwjoXOQ), [MCP Tutorial: Build Your First MCP Server and Client](https://www.youtube.com/watch?v=RhTiAOGwbYE), and [MCP Tutorial: Build Your First MCP Server](https://www.youtube.com/watch?v=jLM6n4mdRuA). SSE is described as deprecated in favor of HTTP streaming.
- **LangChain is for sequential DAG-style pipelines; LangGraph is for stateful, cyclic agents.** Agreed by [LangChain vs LangGraph](https://www.youtube.com/watch?v=qAF1NjEVHhY), [LangGraph vs LangChain vs LangFlow vs LangSmith](https://www.youtube.com/watch?v=ldBsvhjEREc), [LangGraph Explained for Beginners](https://www.youtube.com/watch?v=cUfLrn3TM3M), [Agentic Framework LangGraph explained in 8 minutes](https://www.youtube.com/watch?v=1Q_MDOWaljk), [LangGraph Complete Course](https://www.youtube.com/watch?v=jGg_1h0qzaM). The crossover threshold is "do you need a state graph with loops?"
- **Tools are described to the LLM via name + description + JSON-Schema parameters.** Whether the framework is Claude Agent SDK, LangChain `Tool`/`StructuredTool`, MCP `server.tool`, Mastra `createTool`, ADK, or hand-rolled — confirmed across [LangChain Master Class](https://www.youtube.com/watch?v=yF9kGESAi3M), [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0), [Claude Agents SDK BEATS](https://www.youtube.com/watch?v=i6N8oQQ0tUE), [Mastra](https://www.youtube.com/watch?v=_dG8iZgmicQ), and [Google ADK](https://www.youtube.com/watch?v=bPtKnDIVEsg). The docstring/description is what the model reads to choose tools.
- **The LLM never executes code; the host runtime does.** Explicit in [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0), and implied by every MCP tutorial — the model emits structured JSON; the server/host validates and runs.
- **You can swap LLM providers behind a stable agent interface.** [Google ADK](https://www.youtube.com/watch?v=bPtKnDIVEsg), [LangChain Explained in 10 Minutes](https://www.youtube.com/watch?v=xTmU8ZImUO8), [What is LangChain?](https://www.youtube.com/watch?v=1bUy-1hGZpI), [Mastra](https://www.youtube.com/watch?v=_dG8iZgmicQ), and [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0) (via OpenRouter) all stress provider-agnostic design.
- **MCP Inspector is the standard testing tool for MCP servers.** [The Ultimate MCP Crash Course](https://www.youtube.com/watch?v=ZoZxQwp1PiM), [MCP Tutorial: Build Your First MCP Server and Client](https://www.youtube.com/watch?v=RhTiAOGwbYE), and [MCP Tutorial: Build Your First MCP Server](https://www.youtube.com/watch?v=jLM6n4mdRuA) all use it ("Postman for MCP").

## Examples

### Example 1: Minimal MCP server in TypeScript with a Zod-validated tool

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";
import { z } from "zod";

const server = new McpServer({ name: "test", version: "1.0.0" }, {
  capabilities: { resources: {}, tools: {}, prompts: {} },
});

server.tool(
  "create-user",
  "Create a new user in the database",
  { name: z.string(), email: z.string(), address: z.string(), phone: z.string() },
  { title: "Create User", readOnlyHint: false, destructiveHint: false,
    idempotentHint: false, openWorldHint: true },
  async (params) => {
    try {
      const id = await createUser(params); // writes to users.json
      return { content: [{ type: "text", text: `User ${id} created successfully` }] };
    } catch {
      return { content: [{ type: "text", text: "Failed to save user" }] };
    }
  },
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

— from [The Ultimate MCP Crash Course - Build From Scratch](https://www.youtube.com/watch?v=ZoZxQwp1PiM)

### Example 2: Mastra TypeScript agent with tool, memory, and MCP integration

```ts
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core";
import { Memory } from "@mastra/memory";
import { LibSQLStore } from "@mastra/libsql";
import { MCPClient } from "@mastra/mcp";
import { z } from "zod";

const getTransactions = createTool({
  id: "getTransactions",
  description: "Fetch the user's recent transactions",
  outputSchema: z.array(z.object({ merchant: z.string(), amount: z.number() })),
  execute: async () => fakeTransactions,
});

const mcp = new MCPClient({ servers: { firecrawl: { /* ... */ } } });

export const financialAgent = new Agent({
  name: "financial-agent",
  model: openai("gpt-4o"),
  instructions: "You are a personal-finance assistant...",
  tools: { getTransactions, ...(await mcp.getTools()) },
  memory: new Memory({ storage: new LibSQLStore({ url: "file:./memory.db" }) }),
});
```

Registered on `Mastra` in `index.ts`, then served with Swagger-documented endpoints and consumed via `mastra-client`.

— from [Mastra: The AI Framework That Changes Everything](https://www.youtube.com/watch?v=_dG8iZgmicQ)

### Example 3: Claude Agent SDK — agent with allowed tools and an in-process MCP server

```python
from claude_agent_sdk import query, ClaudeAgentOptions, tool, create_sdk_mcp_server

@tool(name="greet", description="Greet a user. When provided with the name, "
                                 "automatically responds saying hello with the name.")
def greet(name: str) -> str:
    return f"Hello {name}"

server = create_sdk_mcp_server(name="my_tools", version="1.0.0", tools=[greet])

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "mcp__tools__greet"],
    permission_mode="acceptEdits",
    mcp_servers={"my_tools": server},
    system_prompt="You are an expert Python developer.",
    cwd="/tmp/agent",
)

async for msg in query(prompt="greet Mervin", options=options):
    print(msg)
```

The SDK embeds Claude Code itself; the same `query()` shape exists for the JS/TS SDK. The MCP-name convention `mcp__<server>__<tool>` is how allowed-tools wires up custom callables.

— from [Claude Agents SDK BEATS all Agent Framework! (Beginners Guide)](https://www.youtube.com/watch?v=i6N8oQQ0tUE)

### Example 4: LangGraph ReAct agent — `StateGraph` + `ToolNode` + conditional edge

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Look up the current weather for a city."""
    return f"It's sunny in {city}."

def call_model(state):
    return {"messages": [llm.bind_tools([get_weather]).invoke(state["messages"])]}

def should_continue(state):
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode([get_weather]))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")
app = graph.compile()
```

Same pattern is available in `@langchain/langgraph` for JS/TS.

— from [Agentic Framework LangGraph explained in 8 minutes | Beginners Guide](https://www.youtube.com/watch?v=1Q_MDOWaljk) and [LangGraph Complete Course for Beginners](https://www.youtube.com/watch?v=jGg_1h0qzaM)

### Example 5: Hand-rolled agentic loop without a framework

```python
tools = [
    {"name": "create_calendar_reminder", "description": "...", "parameters": {...}},
    {"name": "create_decision_record",   "description": "...", "parameters": {...}},
    {"name": "generate_incident_report", "description": "...", "parameters": {...}},
]

messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": transcript}]

while True:
    resp = client.chat.completions.create(model="anthropic/claude-...",
                                          messages=messages, tools=tools)
    calls = resp.choices[0].message.tool_calls
    if not calls:
        break
    for call in calls:
        result = tool_registry.execute(call.name, call.arguments)  # plain Python
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

summary = client.chat.completions.create(model=..., messages=messages + [SUMMARY_PROMPT])
```

The author's case: Octomind dropped LangChain after 12 months in production; the loop is "really just a `for` loop" with JSON-defined tool calls and Python as the control center.

— from [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0)

### Example 6: Google ADK agent definition + Vertex AI Agent Engine deployment

```python
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def get_stock_price(ticker: str) -> dict:
    """Return the current price for a stock ticker."""
    ...

root_agent = LlmAgent(
    name="finance_agent",
    model="gemini-2.0-flash",      # or OpenAI / Claude — model-agnostic
    instruction="You answer finance questions using the get_stock_price tool.",
    tools=[FunctionTool(func=get_stock_price)],
)
```

Deployment: build locally → create GCP project → enable Vertex AI + storage bucket → `gcloud` config → Poetry script that pushes the agent to Agent Engine. Once deployed, the agent is invoked through `deployments` (the package) and `sessions` (conversations), at ~$0.11/hr per core+GB. Agent Engine is framework-agnostic — it can host LangChain, CrewAI, LlamaIndex, or ADK agents.

— from [Google Agent Development Kit (ADK): How to deploy Your First Agent to Vertex AI Agent Engine](https://www.youtube.com/watch?v=bPtKnDIVEsg)

### Example 7: MCP server registered with Claude Desktop via stdio config

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "horse-tender": {
      "command": "deno",
      "args": ["run", "-A", "main.ts"]
    },
    "atl-leave": {
      "command": "uv",
      "args": ["run", "main.py"]
    }
  }
}
```

The client reads this config on launch, calls `list_tools` / `list_resources` / `list_prompts` on each server, feeds those descriptions to the LLM, and routes tool calls back to the right server. Same `mcp.json` shape is used by VS Code / GitHub Copilot and Roo Code.

— from [Claude's Model Context Protocol is here... Let's test it](https://www.youtube.com/watch?v=HyzlYwjoXOQ) and [MCP Tutorial: Build Your First MCP Server](https://www.youtube.com/watch?v=jLM6n4mdRuA)

### Example 8: LangChain LCEL chain (pipe operator) and tool-augmented agent

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool

prompt = ChatPromptTemplate.from_messages([("system", "..."), ("user", "{q}")])
chain = prompt | ChatOpenAI(model="gpt-4o") | StrOutputParser()

tools = [
    Tool(name="time", func=lambda _: datetime.now().isoformat(),
         description="Returns the current time"),
    Tool(name="wikipedia", func=wiki_search,
         description="Search Wikipedia for a topic"),
]
agent = create_react_agent(ChatOpenAI(model="gpt-4o"), tools, react_prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

The same LCEL `|` composition supports `RunnableParallel` (concurrent branches) and `RunnableBranch` (conditional flow). Tool creation has three levels: `Tool`, `StructuredTool` (with Pydantic schema), and subclassing `BaseTool`.

— from [LangChain Master Class For Beginners 2024](https://www.youtube.com/watch?v=yF9kGESAi3M) and [LangChain Explained in 10 Minutes](https://www.youtube.com/watch?v=xTmU8ZImUO8)

## Disagreements / Open questions

- **Frameworks vs. raw API calls.** [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0) argues frameworks are "costly and complex abstractions" that teach the wrong mental model and that Octomind dropped LangChain in production. Most other videos ([LangChain Master Class](https://www.youtube.com/watch?v=yF9kGESAi3M), [What is LangChain?](https://www.youtube.com/watch?v=1bUy-1hGZpI), [LangChain Explained in 10 Minutes](https://www.youtube.com/watch?v=xTmU8ZImUO8)) defend frameworks as the way to avoid rewriting glue code per provider. The skeptic side is stronger when scoped to long-lived production agents; the framework side is stronger for prototyping and for teams who need RAG/memory/observability out of the box.
- **Is Claude Agent SDK the strongest agent framework?** [Claude Agents SDK BEATS all Agent Framework!](https://www.youtube.com/watch?v=i6N8oQQ0tUE) claims it's the best because it embeds the entire Claude Code runtime. [Mastra: The AI Framework That Changes Everything](https://www.youtube.com/watch?v=_dG8iZgmicQ) explicitly says Mastra "blows it out of the water" because Mastra also bundles workflows, RAG, evals, and observability. No video presents head-to-head benchmarks — both claims are vibes-based.
- **Is the LangChain "hype train" still on the rails?** [What is LangChain?](https://www.youtube.com/watch?v=1bUy-1hGZpI) admits the hype has "cooled a little" but argues the utility remains. [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0) is openly hostile. The LangChain-published [What are Deep Agents?](https://www.youtube.com/watch?v=IVts6ztrkFg) implicitly accepts the criticism by pivoting to opinionated harnesses on top of LangGraph rather than chains.
- **MCP transport: stdio default for local, but the cloud story is unsettled.** Multiple videos mention SSE → HTTP streaming migration; remote MCP server hosting and auth are still presented as evolving.
- **Will MCP Anthropic-CEO claims hold?** [Claude's MCP is here](https://www.youtube.com/watch?v=HyzlYwjoXOQ) directly disputes the "90% of code AI-written within 6 months" claim with skepticism; no other video in the corpus addresses the prediction either way.

## Gaps

- **Native JS/TS examples for LangGraph and Google ADK.** Both ship JS SDKs, but every LangGraph and ADK tutorial in the corpus is Python-only. A viewer wanting a TS-first agent has to extrapolate.
- **Production hardening.** Almost no coverage of evals, regression testing, prompt-injection defenses, sandboxing tool execution, rate-limit handling, or cost monitoring at scale. Mastra mentions evals/observability as features but doesn't demo them.
- **Multi-agent orchestration in depth.** Several videos name-drop multi-agent (CrewAI, AutoGen, LangGraph multi-agent) but none of the 20 walks through a real multi-agent system with hand-off, supervisor patterns, or shared memory.
- **Authentication and authorization for MCP.** The crash courses use `DANGEROUSLY_OMIT_AUTH=true`; production auth, OAuth, and per-tool RBAC are largely unaddressed.
- **Streaming UX.** Streaming is mentioned as a LangGraph feature but no video demonstrates a streaming UI built on top of any of these SDKs.
- **Cost and latency comparisons.** No video benchmarks the same agent built on Claude Agent SDK vs. LangGraph vs. Mastra vs. raw API calls.
- **Deep Agents in JS/TS.** The new Deep Agents package and CLI ([What are Deep Agents?](https://www.youtube.com/watch?v=IVts6ztrkFg)) is Python-first; whether it has, or will have, a TS counterpart is not discussed.
- **Migration paths.** No video shows how to move an existing LangChain v0.2 codebase to LangGraph, or a LangChain agent to Claude Agent SDK / Mastra.
