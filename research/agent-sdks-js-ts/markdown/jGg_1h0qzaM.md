# LangGraph Complete Course for Beginners – Complex AI Agents with Python

> **Source:** [LangGraph Complete Course for Beginners – Complex AI Agents with Python](https://www.youtube.com/watch?v=jGg_1h0qzaM) — [freeCodeCamp.org](https://www.youtube.com/@freecodecamp) · 2025-05-20 · 3:09:51
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A complete beginner-friendly course on **LangGraph**, the Python library for building graph-based AI agent workflows, taught by Vaibhav (a robotics and AI student) for freeCodeCamp.
- Walks through the full conceptual vocabulary of LangGraph: **state**, **nodes**, **edges**, **conditional edges**, **start/end points**, **tools**, **tool nodes**, **state graphs**, **runnables**, and message types.
- Builds five progressively more complex graphs from a "Hello World" greeter to a sequential graph, a conditional/router graph, and a looping graph — solidifying syntax before any LLMs are introduced.
- Then constructs five AI agents: a simple LLM bot, a memory chatbot, a **ReAct** (reason + act) agent with tool calls, a human-in-the-loop **Drafter** project, and a full **Retrieval-Augmented Generation (RAG)** agent over a PDF.
- Heavy emphasis on practical habits: typed dictionaries, docstrings (which the LLM reads to choose tools), reducer functions like `add_messages`, and binding tools to a `chat_openai` model (GPT-4o).
- Each section ends with a hands-on exercise; all answer code is on the course's GitHub.

## Course Introduction

Welcome to this video course on **LangGraph**, the powerful Python library for building advanced conversational AI workflows. In this course, Vaibhav will teach you how to design, implement, and manage complex dialogue systems using a graph-based approach. By the end, you'll be equipped to build robust, scalable, conversational applications that leverage the full potential of large language models.

The instructor introduces himself as a robotics and AI student. The course assumes you have heard of LangGraph but have never coded in it. Because of that assumption, every concept is explained in as much detail as possible — if it feels slow at times, you can always speed up the playback. The course covers theory, builds a lot of graphs and AI agents, and provides exercises throughout. All exercise answers are on the GitHub repo.

## Section 1: Type Annotations

This is a brief, fully theoretical section. The reason it exists is that these annotations show up everywhere once you start coding LangGraph, and you should know what they mean before seeing them in agent code.

### Dictionaries vs. TypedDict

A regular Python dictionary like `movie = {"name": "Avengers Endgame", "year": 2019}` is flexible and efficient, but it has no way to enforce that the data conforms to a particular structure or data type. In larger projects this can be the source of subtle logical errors.

The solution is the **TypedDict**, used extensively in LangGraph (especially to define states). You implement it as a class:

- Subclass `TypedDict`
- Declare each key with its expected data type — e.g. `name: str`, `year: int`

Two main benefits: **type safety** (explicit data types reduce runtime errors) and **enhanced readability** (easier debugging if something goes wrong).

### Union

`Union[int, float]` says a value can be one of the listed types — and only those. A function that squares a number can accept either `int` or `float`, but a string would fail. The makers of LangChain and LangGraph use `Union` extensively throughout the libraries.

### Optional

`Optional[str]` is shorthand for "either a `str` or `None`." Useful when a parameter may be omitted: a `nice_message(name)` function can return `"hi there {name}"` if a name is provided, or fall back to `"hey random person"` if `None` is passed. It cannot be an int, bool, or anything else — only a string or `None`.

### Any

`Any` literally means the value can be anything — any data type, any structure. The simplest of the annotations.

### Lambda Functions

A **lambda** is a shortcut for writing small inline functions. Two examples are given:

1. A simple `square = lambda x: x*x`.
2. Using `map` with a lambda: `list(map(lambda x: x*x, nums))` — squares each element of a list. Far more efficient than a beginner-style `for` loop.

These annotations don't need to be memorized; just have a high-level understanding of each.

## Section 2: LangGraph Elements (Theory)

Before coding, the course walks through every fundamental element of LangGraph with analogies.

### State

The **state** is a shared data structure that holds the current information or context of the entire application — the application's memory. Nodes can access and modify it as they execute. **Analogy: the whiteboard in a meeting room** — everyone (the nodes) reads from and writes to the same whiteboard (the state).

### Node

A **node** is an individual function or operation that performs a specific task within the graph. Each node receives an input (typically the current state), processes it, and produces an updated state. **Analogy: a station on an assembly line** — each station does one specific job (attach, paint, inspect).

### Graph

The **graph** is the overarching structure that maps how different tasks (nodes) are connected and executed. It visually represents the workflow. **Analogy: a road map** — routes between cities with intersections offering choices on which path to take.

### Edges

**Edges** are the connections between nodes. They determine the flow of execution: which node should run next after the current one completes. **Analogy: a train track** connecting two stations in a specific direction; the train running on the track is the state.

### Conditional Edges

A **conditional edge** is a specialized connection that decides the next node based on a specific condition or logic applied to the current state. **Analogy: a traffic light** — green/red/yellow decides the next step. Conceptually, an `if/else` statement.

### Start and End Points

The **start node** is a virtual entry point — it does not perform operations, it just marks where the workflow begins (analogy: the starting line of a race). The **end node** signifies the conclusion of the workflow; when the application reaches it, execution stops (analogy: the finish line).

### Tools

**Tools** are specialized functions or utilities that nodes can use — for example, fetching data from an API. They enhance node capabilities. The difference between a tool and a node: a node is part of the graph structure, while tools are functionalities used within the nodes. **Analogy: tools in a toolbox** — each has a distinct purpose.

### Tool Node

A **tool node** is a special kind of node whose only job is to run a tool. It connects the tool's output back into the state so other nodes can use the information. **Analogy: an operator on the assembly line controlling a machine** (the tool) and feeding results back into the line.

### StateGraph

The **StateGraph** is one of the first elements you actually interact with. Its job is to build and compile the graph structure: it manages the nodes, the edges, the overall state, and ensures data flows correctly. **Analogy: a building's blueprint** — defines structure and flow.

### Runnable

A **runnable** is a standardized executable component that performs a specific task within an AI workflow — a fundamental building block for modular systems. The difference vs. a node: a runnable can represent various operations, while a node specifically receives a state, performs an action, and updates the state. **Analogy: a Lego brick** that snaps together with others to build complex structures.

### Message Types

The five most common message types:

- **HumanMessage** — input from a user.
- **AIMessage** — responses generated by AI models.
- **SystemMessage** — instructions or context for the model.
- **ToolMessage** — similar to a function message but specific to tool usage.
- **FunctionMessage** — represents a function call.

Anyone who has used an LLM API (e.g. OpenAI's) will recognize the system/AI/human trio.

## Section 3: First Coding Section — Five Graphs (No LLMs Yet)

Before introducing LLMs, the course builds five graphs to develop fluency with LangGraph syntax.

### Graph 1: The "Hello World" Greeter

A start point, one node, an end point. Imports: `Dict`, `TypedDict`, `StateGraph`.

Steps:

1. Define `class AgentState(TypedDict)` with one field `message: str`.
2. Write `def greeting_node(state: AgentState) -> AgentState`. The input and output type must both be the state, because the state must be returned (updated). Always include a **docstring** — when LLMs come into play, the docstring is what the LLM reads to know what a function does.
3. Inside, mutate `state["message"] = "hey " + state["message"] + ", how is your day going"` and return state.
4. Build the graph: `graph = StateGraph(AgentState)`, `graph.add_node("greeter", greeting_node)`, `graph.set_entry_point("greeter")`, `graph.set_finish_point("greeter")`, then `app = graph.compile()`.
5. Visualize with IPython, then run `result = app.invoke({"message": "Bob"})` → `"hey Bob, how is your day going"`.

> Just because the graph compiles without error doesn't mean it will run successfully — there can still be logical errors.

**Exercise:** Build a personalized compliment agent that says something like `"Bob, you're doing an amazing job learning LangGraph"` — concatenate the state, don't replace it.

### Graph 2: Multiple Inputs

Same structure (start → single node → end), but the state now carries multiple fields of different types: `values: list[int]`, `name: str`, `result: str`.

The single node `process_values` sums the integers and writes `f"Hi there {name}, your sum is equal to {sum(values)}"` into `result`. After invoking with `{"values": [1,2,3,4], "name": "Steve"}`, `answers["result"]` is `"Hi there Steve, your sum is equal to 10"`.

Important caution: if you don't pass a key as input, LangGraph initializes it to `None`. So a node that *reads* a state field that wasn't input would crash; a node that only *writes* to it works fine.

You can also access just `answers["result"]` for clean output instead of the full state dict. Adding `print(state)` before and after the action is a great way to see how the state evolves.

**Exercise:** Build a graph that takes a name, a list of integers, and an `operation` ("+" or "*"), and performs the matching operation inside one node (using an `if` statement).

### Graph 3: Sequential Graph (Two Nodes Connected by an Edge)

Adds the **`add_edge`** method. State: `name: str`, `age: str`, `final: str`.

`first_node` writes `state["final"] = f"Hi {state['name']}"`. `second_node` writes `state["final"] = f"You are {state['age']} years old"`.

A subtle logical error is planted deliberately: the second node *replaces* the first node's output. The fix is concatenation: `state["final"] = state["final"] + f". You are {state['age']} years old"`. **Lesson:** you can update state fields multiple times across nodes, but be careful not to accidentally clobber prior content.

Wiring:

- `graph.add_node("first_node", first_node)`, `graph.add_node("second_node", second_node)`
- `graph.set_entry_point("first_node")`
- `graph.add_edge("first_node", "second_node")` — the new directed edge
- `graph.set_finish_point("second_node")`

Invoking with `{"name": "Charlie", "age": "20"}` produces `"Hi Charlie. You are 20 years old"`.

**Exercise:** Three nodes in a sequence — name, age, and a list of skills — combined into something like `"Linda, welcome to the system. You are 31 years old and you have skills in Python, machine learning and LangGraph."` Hint: use `add_edge` twice.

### Graph 4: Conditional Graph (Router Pattern)

First implementation of conditional logic *across* the graph (not just within a node). Imports add `START` and `END` from `langgraph.graph` — an alternate, arguably easier way to set entry/finish points.

State: `number1: int`, `number2: int`, `operation: str`, `final_number: int`.

Three node functions:

- `adder` — sums the two numbers, returns updated state.
- `subtractor` — subtracts.
- `decide_next_node` — does **not** return state. It returns the *name of an edge* (`"addition_operation"` or `"subtraction_operation"`) based on whether `state["operation"]` equals `"+"` or `"-"`.

Because `decide_next_node` doesn't return state, registering it directly as a node fails. The trick: use `lambda state: state` as a pass-through function for the router node:

```
graph.add_node("router", lambda state: state)
```

The router only *compares*, never *assigns*, so the state passes through unchanged.

Wiring with the new `add_conditional_edges`:

- `graph.add_edge(START, "router")`
- `graph.add_conditional_edges("router", decide_next_node, {"addition_operation": "add_node", "subtraction_operation": "subtract_node"})`
- `graph.add_edge("add_node", END)`, `graph.add_edge("subtract_node", END)`

The path map `{edge_name: node_name}` is the dictionary that turns router return values into actual destinations.

Invoking with `{"number1": 10, "operation": "-", "number2": 5}` yields `final_number = 5`.

**Exercise:** Build the same pattern twice in one graph — four numbers, two operations, two outputs (the "monstrosity").

### Graph 5: Looping Graph

Now the goal is a **loop**. Plan first: start → `greeting_node` → `random_node` → conditional edge that loops back to `random_node` until five numbers are generated, then exits. Imports include `random`.

State: `name: str`, `numbers: list[int]`, `counter: int`.

Nodes:

- `greeting_node` sets `state["name"] = "hi there " + state["name"]` *and* sets `state["counter"] = 0` (a robustness measure: wipes out any garbage initial counter the user passed).
- `random_node` appends `random.randint(0, 10)` to `state["numbers"]` and increments `state["counter"]`.

Routing function `should_continue(state)`: if `counter < 5` return `"loop"`, else return `"exit"`.

Wiring:

- `graph.add_edge("greeting_node", "random_node")`
- `graph.add_conditional_edges("random_node", should_continue, {"loop": "random_node", "exit": END})`
- `graph.set_entry_point("greeting_node")`

The trajectory: greeting → random (×5) → end. Print statements during the loop confirm counter values 1–4 before the exit branch fires.

> There's more than one way to code a looping graph in LangGraph. This is one efficient way; with practice you'll find others.

**Exercise:** Build an automatic higher/lower guessing game graph (1–20 range, max 7 guesses, no human in the loop — the agent guesses by itself based on hints from a hint node).

## Section 4: AI Agents

Now LLMs enter the picture. The course builds five agents.

### Agent 1: Simple Bot

Not really an agent — the simplest possible LLM wrapper. Imports add `HumanMessage` from `langchain_core.messages`, `ChatOpenAI` from `langchain_openai`, and `dotenv.load_dotenv` to load API keys.

> LangGraph is built on top of LangChain. It's designed to leverage LangChain's robust, sophisticated libraries — using LangChain features inside LangGraph isn't betrayal, it's how it's designed.

Why an API key? Because we're calling an external LLM (GPT-4o). If you used a local LLM via Ollama, no API key would be needed.

State: `messages: list[HumanMessage]`. Initialize `llm = ChatOpenAI(model="gpt-4o")`. The instructor notes GPT-4o-mini is also extremely cheap — input/output tokens cost cents per thousand.

Process node: `response = llm.invoke(state["messages"])`, print, return state.

Wrap in a `while` loop that takes `input()`, sends it as a `HumanMessage`, and exits on `"exit"`. The bot replies, but if you say `"hi, I am Bob"` and then `"what is my name?"`, it responds `"I'm sorry, but I don't have the ability to know your name."` There is no memory yet — every call is a separate API request.

### Agent 2: Memory Chatbot

Adds `AIMessage` and the `Union` annotation. State changes to `messages: list[Union[HumanMessage, AIMessage]]` so both message types can live in the same list.

> All these AI agentic libraries — LangChain, LangGraph, Crew AI, Autogen — are great, but you really can build your own AI agentic system with just plain Python functions. That said, LangGraph offers a strong balance of control vs. boilerplate.

The process node now also appends the LLM's response as an `AIMessage`:

```
state["messages"].append(AIMessage(content=response.content))
```

`.content` extracts only the meaningful text, dropping token-count metadata.

Outside the graph, a `conversation_history` list is maintained, appended to with each `HumanMessage` *before* invoking, and replaced with `result["messages"]` *after* invoking. The full history (not just the latest message) is what's passed in each call — that's how the model "remembers."

Now `"my name is Steve"` followed by `"what is my name?"` correctly answers `"You are Steve."`

**Two remaining problems:**

1. **No persistence.** Exit the program and the in-memory state is wiped. The course's quick fix is to dump `conversation_history` to a `logging.txt` text file on exit (with `You:` and `AI:` lines). For real apps, use a database or vector database. Spelling errors are preserved verbatim — the human messages are stored unaltered, the AI cannot rewrite them.
2. **Unbounded growth.** Every turn the message list grows, costing more input tokens. Easy mitigation: drop the oldest user message once the list exceeds a threshold (e.g., 5). Drop from the front, not the back, since the latest is most relevant.

### Agent 3: ReAct Agent (Reasoning + Acting)

The classic LangGraph pattern: start → agent → conditional edge to either tools (loops back to agent) or end. Long subsection because of many new imports.

New imports explained:

- **`Annotated`** — adds metadata to a type without changing the data type. Example: `email: Annotated[str, "this has to be a valid email format"]`. The metadata is readable via `Email.__metadata__`.
- **`Sequence`** — a type annotation that automatically handles state updates for sequences (e.g., adding new messages to a chat history), avoiding manual list manipulation.
- **`BaseMessage`** — the parent class for all message types (HumanMessage, AIMessage, ToolMessage, SystemMessage all inherit from it).
- **`ToolMessage`** — message type passed back to the LLM after a tool has been called (carries content and tool_call_id).
- **`SystemMessage`** — message used to provide instructions to the LLM (e.g., "you are a helpful assistant").
- **`tool`, `ToolNode`** — the decorator and the prebuilt node from LangGraph for tool usage.
- **`add_messages`** — a **reducer function** from `langgraph.graph.message`.

> A **reducer function** is a rule that controls how updates from nodes are combined with the existing state. Without one, an update would replace the existing value entirely. `add_messages` appends instead of overwriting.

State: `messages: Annotated[Sequence[BaseMessage], add_messages]`.

Defining a tool:

```
@tool
def add(a: int, b: int):
    """This is an addition function that adds two numbers together."""
    return a + b
```

The decorator marks the function as a tool. **Docstrings are mandatory** — they're how the LLM understands what each tool does. (Removing the docstring throws an explicit error: *"function must have a docstring if description is not provided."*)

Bind tools to the model:

```
tools = [add]
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)
```

Agent node `model_call(state)` invokes the model with a `SystemMessage("you are my AI assistant, please answer my query to the best of your ability")` plus `state["messages"]`, then returns `{"messages": [response]}` — the concise update form, made safe by the `add_messages` reducer.

Conditional function `should_continue(state)`: looks at the last message's `tool_calls`; if empty, return `"end"`; otherwise return `"continue"`.

Wiring:

- `graph.add_node("our_agent", model_call)`, `graph.add_node("tools", ToolNode(tools=tools))`
- `graph.set_entry_point("our_agent")`
- `graph.add_conditional_edges("our_agent", should_continue, {"continue": "tools", "end": END})`
- `graph.add_edge("tools", "our_agent")` — closes the loop

A streaming helper function prints intermediate output cleanly. Examples:

- `"add 3 + 4"` → tool call `add(3, 4)` → `7`.
- `"add 34 + 21, add 3 + 4"` → tool called twice → 55 and 7.
- `"add 34 + 21, add 3 + 4, add 12 + 12"` → three tool calls, three results.

> Tool calls are also an indication that the LLM didn't use its own training data — LLMs don't actually know how to do math, they just guess the next token. The tool gives them real arithmetic. The LLM decides what arguments to pass.

Add `subtract` and `multiply` tools by appending to the `tools` list — no other changes. Test: `"add 40 + 12, multiply the result by 6, also tell me a joke please"` → 52, 312, plus a (predictable, dad-tier) joke. The robustness comes from the loop: after every tool call, control returns to the agent, which decides whether more tools are needed or whether to end. Even queries that need no tool work — the agent just answers directly.

### Agent 4: Drafter (Human-in-the-Loop Mini Project)

Scenario: a boss wants an AI agentic system that drafts emails/documents fast, with human-AI collaboration (continuous human feedback) and the ability to save the draft when the human is happy.

Graph differs from a ReAct agent: when the **save** tool is used, the flow ends directly instead of looping back to the agent. So the conditional edge after tools chooses between continue → agent and end → END.

A **global variable** `document_content` is used (the formal LangGraph way is **InjectedState**, which is out of scope for this beginner course).

Two tools:

- `update(content)` — sets `document_content = content` and returns confirmation including the new content.
- `save(filename)` — saves `document_content` to a `.txt` file. Robustness: if the filename doesn't end in `.txt`, append it. Wrapped in try/except for debugging.

The agent function `our_agent(state)`:

1. Builds a long, explicit `SystemMessage` ("You are Drafter, a helpful writing assistant... use the update tool... use the save tool to save... always show the current document state after modifications").
2. If `state["messages"]` is empty, prompts the user `"I'm ready to help you update a document. What would you like to create?"`. Otherwise prompts `"What would you like to do with the document?"`.
3. Wraps user input as a `HumanMessage`, invokes the model with system + state messages + new user message, prints the AI response and any tool messages (a print helper makes this readable), and returns `{"messages": [user_message, response]}`.

Conditional `should_continue(state)`: scans recent tool messages; if any tool message indicates the **save** tool was used (`"saved"` in content), return `"end"`. Otherwise return `"continue"`.

Wiring is the standard ReAct shape (agent ↔ tools loop) but the conditional edge from **tools** decides continue/end based on which tool ran.

Demo: drafts an email to "Tom" saying we can't make a meeting, then iteratively adds time/location, fixes the signature to "V", adds a new meeting time, reformats the greeting onto a new line, and finally saves. The agent generates a sensible filename like `unable_to_attend_meeting_email.txt` even though no filename was specified.

Robustness demo: if you say only `"write an email"`, the agent doesn't blindly call a tool — it asks `"sure, what would you like the email to say?"`. `bind_tools` gives the agent *access* to tools but doesn't force it to use them.

Suggested extensions: voice mode (OpenAI Whisper for STT, ElevenLabs for TTS), a GUI, or hooking up your own knowledge base.

### Agent 5: RAG Agent (Retrieval-Augmented Generation)

Graph: start → LLM → conditional edge → retriever agent → loop back to LLM, or end.

Setup imports include `PyPDFLoader`, `RecursiveCharacterTextSplitter`, `Chroma`, and OpenAI embeddings.

Initialize the model with `temperature=0` (deterministic; `1` would be more stochastic). Initialize an OpenAI embedding model — and **make sure the embedding model is compatible with your LLM** (different vector dimensions across providers cause problems).

Document used: a 9-page PDF about 2024 stock market performance. Loaded via `PyPDFLoader`, then chunked with `chunk_size=1000` and `chunk_overlap=200`. The overlap means consecutive chunks share ~200 tokens, preserving context across boundaries.

Chroma vector database is created in a local folder (`chroma_db`) under collection name `"stock_market"`. An `if not exists` check prevents re-creating on subsequent runs. Try/except surfaces creation errors.

The **retriever** uses `search_type="similarity"` and `k=5` (top 5 chunks). Default would be 4 — five is a reasonable middle ground.

Tool:

```
@tool
def retriever_tool(query: str) -> str:
    """This tool searches and returns the information from our document."""
```

It invokes the retriever; if no chunks are found, returns `"I found no relevant information in the document"`. Otherwise concatenates the top-5 chunk contents and returns them.

State follows the ReAct pattern: `messages: Annotated[Sequence[BaseMessage], add_messages]`.

`should_continue` checks for tool calls on the last message.

System prompt is large and explicit: *"You are an intelligent AI assistant who answers questions about the document loaded into your knowledge base... please always cite the specific parts of the document you use in your answers."* The citation requirement is to suppress hallucinations.

Two agents wired into the graph:

- The **LLM agent** node calls the model with the system message + state messages.
- The **retriever agent** node executes tool calls. If a tool call has the right name (`retriever_tool`), it runs it and packs results as a `ToolMessage`. If the tool name is invalid, it returns `"Incorrect tool name. Please retry and select the tool from list of available tools"` — guarding against the LLM hallucinating tool names.

Wiring:

- `graph.add_conditional_edges("llm", should_continue, {True: "retriever_agent", False: END})`
- `graph.add_edge("retriever_agent", "llm")`
- `graph.set_entry_point("llm")`

A `running_agent()` helper runs a `while True` loop accepting questions until the user types `exit` or `quit`.

Demo questions:

- `"How was the S&P 500 performing in 2024?"` → calls retriever, returns answer citing ~25% total return, ~23% increase, late-1990s comparison, "Magnificent 7" — values traceable to the actual PDF text.
- `"How did OpenAI perform in 2024?"` → retriever returns no matching chunks; LLM correctly answers `"The documents do not provide specific information about OpenAI stock performance"` — no hallucination, because OpenAI is not publicly traded.

That successfully demonstrates a working RAG graph in LangGraph.

## Closing

The course wraps up after the RAG agent. Although the course ends here, the journey in LangGraph is just beginning — there are countless AI projects and agent systems to build, including a personal "Jarvis." The instructor invites further questions on LinkedIn and thanks the viewer for watching.
