# LangChain Master Class For Beginners 2024 (LangChain v0.2, 20+ Examples)

> **Source:** [LangChain Master Class For Beginners 2024 [+20 Examples, LangChain V0.2]](https://www.youtube.com/watch?v=yF9kGESAi3M) — [aiwithbrandon](https://www.youtube.com/@aiwithbrandon) · 2024-06-22 · 3:17:50
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A 3+ hour beginner-friendly walkthrough of **LangChain v0.2** built around 20+ runnable code examples in a Poetry-managed Python project.
- Five modules cover the LangChain core: **chat models**, **prompt templates**, **chains** (LCEL), **RAG** (retrieval augmented generation), and **agents + tools**.
- The chat models section ends with a Firebase/Firestore-backed chat history demo so conversations persist to the cloud across sessions.
- Chains are taught with LangChain Expression Language (LCEL) using the pipe operator, including parallel branches via `RunnableParallel` and conditional flow via `RunnableBranch`.
- The RAG module goes deep on text splitting, embeddings (OpenAI vs. Hugging Face), retriever search types (similarity, MMR, threshold), metadata sources, web scraping with the basic `WebBaseLoader` and **Firecrawl**, and full conversational RAG with a history-aware retriever.
- Agents are framed as state machines (action → observation → thought) using prompts like the **ReAct** prompt and tools that grant superpowers (current time, Wikipedia, Tavily search, Vector store lookup, math).
- Three tool-creation styles are covered: the simple `Tool` constructor, `StructuredTool` with a Pydantic argument schema, and full custom tools by subclassing `BaseTool`.

## Course outline and environment setup

Brandon opens by previewing the five modules — chat models, prompt templates, chains, RAG, and agents/tools — and recommends watching the whole thing on 2x first, then re-watching the section relevant to whatever project you're building. Source code is free in the video description, and there's a free Skool community with weekly coaching calls for support.

The setup uses **Python** plus **Poetry** for dependency management. The project ships with a `pyproject.toml` listing every dependency you need. Steps:

1. Install Python and Poetry.
2. Run `poetry install --no-root` from the repo to install all dependencies.
3. Run `poetry shell` to drop into the project's virtual environment — the prompt name shows you're in it.
4. Rename `.env.example` to `.env` and fill in API keys (OpenAI, Google, Firecrawl, etc.).

A quick VS Code / Cursor tip: the squiggly import errors are because the editor isn't pointing at the Poetry-managed interpreter. Run `poetry shell`, copy the path it prints, then in VS Code run **"Python: Select Interpreter" → Enter interpreter path** and paste it in. To leave the shell later, just type `exit`.

## Module 1: Chat models

A **chat model** is LangChain's abstraction over LLMs (ChatGPT, Claude, Gemini, etc.) — they all expose the same conversation-style API. The course pins LangChain version **0.2**; v0.1 features will be deprecated soon.

### Example 1: Basic chat model call

The three core steps:

1. Load environment variables (`load_dotenv`) so the OpenAI key is picked up. Under the hood `ChatOpenAI` reads `OPENAI_API_KEY` from the env automatically — you *can* pass it manually but storing it in `.env` is safer.
2. Create a model: `ChatOpenAI(model="gpt-4o")`. You can swap to `gpt-4`, `gpt-3.5-turbo`, etc.
3. Call `model.invoke("...")` — `invoke` is the magic word used everywhere in LangChain.

The full result includes content plus metadata (token counts, run id, finish reason). 99% of the time you just want `result.content`.

### Example 2: A real conversation with system / human / AI messages

Three message types matter:

- **SystemMessage** — broad context for the conversation (e.g. "You are a professional accountant"). Best practice / required: this comes first.
- **HumanMessage** — what the user says.
- **AIMessage** — what the assistant says back.

Build a `messages` list and pass it to `model.invoke(messages)`. To continue a conversation, append the AI's response and the next human turn to the same list — that's how you get context awareness for follow-ups like "now make it less formal" or "do the same for this email."

### Example 3: Different LLM providers

LangChain abstracts away provider differences. Swap `ChatOpenAI` for `ChatAnthropic` (Claude) or `ChatGoogleGenerativeAI` (Gemini) and the rest of the code is identical. This matters because models differ on price, speed, and capability — you'll want to pick the right one per task.

### Example 4: A real-time terminal chat loop

Maintain a `chat_history` list, seed it with a SystemMessage, then loop:

- Read `query = input(...)`. If it's `exit`, print history and break.
- Append `HumanMessage(query)` to history.
- `result = model.invoke(chat_history)`.
- Print `result.content`, append `AIMessage(result.content)` to history.

This feels exactly like the ChatGPT website but runs locally, and the saved history is a full transcript you could persist somewhere.

### Example 5: Persisting chat history to Firebase Firestore

Brandon's favorite chat-models example: save messages to the cloud so conversations resume across sessions. Setup steps:

1. Create a **Firebase** account at console.firebase.google.com and create a project.
2. In the console under **Build → Firestore Database**, click **Turn on**.
3. Copy your Firebase **project ID** from project settings.
4. Install the **Google Cloud CLI** locally (link in code comments).
5. Authenticate the local machine with `gcloud auth application-default login` so your code can reach the back end with default credentials.

In code: pick a `SESSION_ID` (e.g. `user_session_new`) and a `COLLECTION_NAME` (e.g. `chat_history`). Initialize a `firestore.Client(project=PROJECT_ID)`, then create `FirestoreChatMessageHistory(session_id, collection, client)`. The chat loop is the same as Example 4, except every `add_user_message` / `add_ai_message` call writes to Firestore in real time. Messages appear in the Firebase console as byte strings — that's just how Firestore stores them. Re-running with the same session ID loads existing history so the AI can refer back to "who we were just talking about."

LangChain has many other history backends (file-based, etc.) — Firestore is one option among many.

## Module 2: Prompt templates

A **prompt template** is fill-in-the-blank for prompts. You write a string with `{variable}` placeholders, wrap it in `ChatPromptTemplate`, and `invoke` it with a dict of values. The output is a messages array ready to pass to a chat model.

### Single and multiple placeholders

```python
template = "Tell me a joke about {topic}"
prompt_template = ChatPromptTemplate.from_template(template)
prompt = prompt_template.invoke({"topic": "cats"})
```

You can have any number of placeholders (`{topic}`, `{joke_count}`, etc.) — the input dict just needs all of them.

### System + human messages with placeholders

To control message types, use the **tuple format** with `from_messages`:

```python
messages = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} jokes."),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
```

**Important gotcha**: any message that needs string interpolation must be in tuple form. If you mix `HumanMessage("...")` instances with placeholders, the variables won't be replaced and you'll see literal `{topic}` in the output. Brandon spent a long time hitting this his first time.

### Wiring a prompt into a chat model

Example 2 ties it together: `prompt = prompt_template.invoke({...})`, then `result = model.invoke(prompt)`, then `print(result.content)`. Calling `invoke` twice in a row is exactly what chains will simplify next.

## Module 3: Chains (LangChain Expression Language)

Brandon's favorite section. A **chain** is a series of tasks where each one's output feeds the next. **LangChain Expression Language (LCEL)** lets you build a chain by piping pieces together with the `|` operator.

### Example 1: Basic chain

```python
chain = prompt_template | model | StrOutputParser()
result = chain.invoke({"topic": "lawyers", "joke_count": 3})
```

`StrOutputParser` plays the role of `result.content` — it pulls the string out of the model's response. Without it you get the full message object with metadata.

Compared to the manual approach (build prompt, invoke, save result, build next call, invoke again), the entire pipeline collapses to one expression.

### Example 2: Under the hood — Runnables, RunnableLambdas, RunnableSequence

LCEL is sugar over `RunnableSequence`. A **Runnable** is a task. A **RunnableLambda** wraps an arbitrary Python function as a Runnable so you can drop it in a chain. A **RunnableSequence** has `first`, `middle` (a list), and `last`. The chain `a | b | c | d` is identical to `RunnableSequence(first=a, middle=[b, c], last=d)`. Use LCEL 99% of the time.

### Example 3: Extending chains with custom logic

You can keep piping more steps:

```python
chain = prompt_template | model | StrOutputParser() | RunnableLambda(lambda x: x.upper()) | RunnableLambda(count_words)
```

Any pure Python you want — uppercase, count words, hit an external API — just wrap it in a `RunnableLambda`. It receives the previous step's output as input.

### Example 4: Parallel branches with RunnableParallel

For tasks that should run concurrently, use `RunnableParallel`. The example builds a Pros/Cons review of a MacBook Pro:

1. Initial chain: prompt → model → string. Output is a feature list.
2. `RunnableParallel(branches={"pros": pros_chain, "cons": cons_chain})` runs both analysis chains at the same time.
3. A final `RunnableLambda` receives `{"branches": {"pros": ..., "cons": ...}}` and formats both into a combined report.

This is how you'd write a "draft a LinkedIn post AND a Twitter post AND an email about this idea" workflow — three parallel branches saving wall-clock time vs. running them sequentially.

### Example 5: Conditional flow with RunnableBranch

For an if/elif/else over the previous step's output, use `RunnableBranch`. The customer-feedback example has a **classification chain** that labels feedback as positive / negative / neutral / escalate, and then a `RunnableBranch` picks the right reply chain based on that label:

```python
RunnableBranch(
    (lambda x: "positive" in x, positive_feedback_chain),
    (lambda x: "negative" in x, negative_feedback_chain),
    (lambda x: "neutral" in x, neutral_feedback_chain),
    escalate_feedback_chain,  # default
)
```

Plug it in as the final stage of a larger chain to dynamically dispatch to the appropriate response template.

## Module 4: Retrieval Augmented Generation (RAG)

LLMs have knowledge cutoffs and don't know about your private docs. **RAG** feeds external context into the prompt so the model can answer about PDFs, websites, source code, video transcripts, internal company docs, etc.

### How RAG works at a high level

The corpus is too large for any context window (e.g. a 10M-token Harry Potter PDF won't fit in 8K tokens). The fix is two-phase:

**Indexing phase**:

1. **Load** the source document (PDF, text, web page).
2. **Split** it into ~1000-token **chunks** (with optional overlap so sentences don't get cleaved).
3. **Embed** each chunk — convert it to a numerical vector. Similar text → similar vectors. (e.g. "dog" and "cat" sit close together, "house" sits far away.)
4. **Store** chunks + embeddings in a **vector store** like **Chroma**.

**Query phase**:

1. Embed the user's question with the *same* embedding model.
2. Use a **retriever** to find the top-K most similar chunks in the vector store.
3. Stuff those chunks into a prompt along with the question.
4. The LLM answers using the retrieved context.

### Example 1A/1B: RAG basics with Chroma

The corpus is *The Odyssey* as a `.txt`. Setup:

- Paths: `books/odyssey.txt` and a `db/chroma_db/` persistent directory.
- Skip the indexing step if `chroma_db/` already exists (embeddings cost money).
- Use `TextLoader` → `CharacterTextSplitter(chunk_size=1000, chunk_overlap=...)` → `OpenAIEmbeddings(model="text-embedding-3-small")` → `Chroma.from_documents(...)`.

Querying (1B):

- Re-instantiate `Chroma(persist_directory, embedding_function=...)`.
- Build a retriever: `vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 3, "score_threshold": 0.4})`.
- `retriever.invoke("Who is Odysseus's wife?")` returns relevant chunks. The top hit names **Penelope** as expected.

Tuning notes: `k` is the max documents returned; `score_threshold` is the minimum similarity. Set the threshold too high (e.g. 0.9) and you can get zero results.

### Example 2: Adding metadata to documents

LLMs hallucinate; metadata lets you cite sources. The setup loads multiple books from the `books/` folder, and on each loaded document sets `doc.metadata["source"] = book_filename`. Now retrieval results include the source book, e.g. asking "How did Juliet die?" returns the relevant chunk *plus* `source: romeo_and_juliet.txt`. You can extend metadata with chapter, speaker, page, etc. — whatever your corpus supports.

### Example 3: Text splitter deep dive

Five splitter strategies covered:

- **CharacterTextSplitter** — naive character-count splitting, good when content has no syntactic structure.
- **SentenceTransformersTokenTextSplitter** / sentence-based — splits on `.`, `?`, `!` so chunks are full sentences.
- **TokenTextSplitter** — splits at token boundaries; can chop words mid-token (not recommended for prose).
- **RecursiveCharacterTextSplitter** — Brandon's default recommendation. Tries to keep paragraphs and sentences intact within the size limit. Use this unless you have a reason not to.
- **CharacterTextSplitter with custom separator** — e.g. `\n\n` to split per paragraph. Useful when you know the structure but YMMV.

Each splitter is loaded into its own Chroma collection, then the same query is run against each so you can compare results.

### Example 4: Embeddings deep dive

Two embedding options compared:

- **OpenAI** — `text-embedding-3-small` (cheap, default), `text-embedding-3-large` (more dimensions, more accuracy, more cost), `text-embedding-ada-002` (older). Brandon uses 3-small almost always.
- **Hugging Face sentence-transformers** — runs locally, free, and roughly half a gigabyte of model weights. Trades performance for cost.

Same query against both vector stores: OpenAI returns more relevant chunks about Penelope, Hugging Face returns fewer but still gets there. Pick based on cost vs. quality.

### Example 5: Retriever search types

- `similarity_score_threshold` — top-K above a similarity threshold (the default in earlier examples).
- `similarity` — straight top-K with no threshold. Use when you know every query will be on-topic.
- `mmr` (Maximum Marginal Relevance) — top-K *with diversity*. Returns relevant chunks but spreads them out so you get more contextual variety. Tunable via `fetch_k` (initial pool size) and `lambda_mult` (0 = max diversity, 1 = max similarity).

Demo: "How did Juliet die?" — `similarity_score` returns the dagger scene; `mmr` mixes in surrounding paragraphs about her death scene for richer context.

### Example 6: One-off RAG — retrieve then generate

This first example wires retrieval to a chat model:

1. Build a query, retrieve top documents with `retriever.invoke(query)`.
2. Manually build a combined prompt: `f"Here are some documents that might help: {docs_text}\n\nQuestion: {query}"`.
3. `ChatOpenAI(model="gpt-4o").invoke([HumanMessage(combined_input)])`.
4. Print `result.content`.

Brandon snuck a `langchain_demo.txt` into the books directory, so the answer to "How can I learn more about LangChain?" comes back with "Watch Brandon's YouTube channel" sourced directly from that doc.

### Example 7: Conversational RAG with a history-aware retriever

The most complex but most useful RAG example. Two helper chains stack:

- **history-aware retriever** (`create_history_aware_retriever`) — given chat history + a new question, rephrases the question into a standalone search query, then runs the retriever. Built from a contextualization prompt + the LLM + the base retriever.
- **document chain** (`create_stuff_documents_chain`) — feeds retrieved docs plus chat history plus the question into a QA prompt with the LLM. The QA prompt says: "You are an assistant... Use the context. If you don't know, say so. Three sentences max."

Combine them with `create_retrieval_chain(history_aware_retriever, qa_chain)` to get a `rag_chain`. The chat loop maintains a `chat_history` list and on each turn:

```python
result = rag_chain.invoke({"input": query, "chat_history": chat_history})
chat_history.append(HumanMessage(query))
chat_history.append(AIMessage(result["answer"]))
```

Demo flow: "How can I learn more about LangChain?" → answer about Brandon's channel. "Who is Brandon again?" → resolves "Brandon" via chat history *and* re-queries the vector store, returning a synthesized answer.

### Example 8: Web scraping into a vector store

Two scrapers compared:

- **WebBaseLoader** — basic, free, scrapes raw HTML. The Apple homepage demo gets ~5 chunks; results are okay but mostly raw page text. Misses anything rendered by JavaScript.
- **Firecrawl** (`FireCrawlLoader`) — paid service with a free tier; turns websites into LLM-ready Markdown. Has `scrape` (one page) and `crawl` (whole site) modes — use `scrape` first or you'll burn tokens fast. The same Apple page yields 14 well-structured chunks with rich metadata, including JS-rendered content.

Recommendation: Firecrawl whenever you're scraping at scale, especially for content-heavy sites like Reddit.

## Module 5: Agents and tools

### What is an agent?

An **agent** is just an LLM with a specific prompt that guides its behavior, run as a state machine. The classic loop:

- **Action** — pick a tool, run it.
- **Observation** — read the tool's output.
- **Thought** — plan the next step.
- Repeat until you have a **final answer**.

### What is a tool?

A **tool** is code that gives the agent a superpower. Common categories:

- Search the internet (Tavily, SerpAPI, DuckDuckGo).
- Execute code (Python interpreter, plotting, data analysis).
- Talk to databases (SQL, vector stores).

Tools and agents are useless apart, which is why this module covers them together.

### Example 1: Basic agent + custom time tool

A minimal `get_current_time()` Python function (returns local time as `H:MM AM/PM`) is wrapped via:

```python
Tool(
    name="Time",
    func=get_current_time,
    description="Useful for when you need to know the current time.",
)
```

The agent uses the **ReAct** prompt pulled from LangChain Hub (`hwchase17/react`). Tip: the prompt repo is public; you can read the exact instructions that turn an LLM into a ReAct agent.

```python
agent = create_react_agent(llm=ChatOpenAI(model="gpt-4o"), tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
executor.invoke({"input": "What time is it?"})
```

In verbose mode you see the colored trace: thought → action (Time) → action input → observation (the time) → "I now know the final answer" → final answer. If a tool takes no parameters, accept `*args, **kwargs` to avoid weirdness when the LLM passes empty input.

### Example 2: Conversational ReAct with multiple tools

Adds a `search_wikipedia(query)` tool that returns a two-sentence Wikipedia summary, plus the time tool. Uses the **structured-chat** prompt instead of the bare ReAct prompt — it expects tool calls as JSON blobs and is built for conversational use.

`ConversationBufferMemory(memory_key="chat_history", return_messages=True)` wires chat history into the agent executor automatically, so multi-turn questions work:

- "Who is George Washington?" → agent picks Wikipedia, passes `"George Washington"` as the action input, returns a summary.
- "How old was he when he died?" — answers from memory without re-querying Wikipedia.
- "Who is Steve Jobs and how old was he when he died?" — two-part question; the agent chains its own reasoning to answer both halves.

### Example 3: Agent that talks to a vector store

Reuses the multi-book Chroma store from the RAG section. The trick: wrap the conversational RAG chain (`history_aware_retriever` + `qa_chain` → `rag_chain`) inside a custom tool whose `func` invokes the rag chain. The agent now has a "Answer Question" tool that can hit the vector store on demand.

Demo: "How can I learn more about LangChain?" → agent decides to call the tool → tool calls the RAG chain → vector store returns Brandon's blurb → agent replies. With `verbose=True` you can watch the agent decide, see the input go into the tool, see the retrieved context, and see the final synthesized answer.

### Tool deep dive 1: Tool constructor and StructuredTool

Three example functions: `greet_user(name)`, `reverse_string(text)`, and `concatenate_strings(a, b)`.

- The simple **`Tool`** constructor (name + description + func) works great for single-argument tools — the LLM is good at inferring the input.
- For multi-argument tools, use **`StructuredTool`** with a Pydantic `args_schema`:

```python
class ConcatStringsArgs(BaseModel):
    a: str = Field(description="The first string")
    b: str = Field(description="The second string")

StructuredTool.from_function(
    func=concatenate_strings,
    name="ConcatenateStrings",
    description="Concatenate two strings.",
    args_schema=ConcatStringsArgs,
)
```

This example uses the **`openai-tools-agent`** prompt, which specializes in tool-calling. The agent correctly routes "greet Alice" → `greet_user("Alice")`, "reverse hello" → `reverse_string("hello")`, and concatenation → `concatenate_strings(a=..., b=...)`.

### Tool deep dive 2: Maximum control via BaseTool

For the most control, subclass **`BaseTool`** and implement `_run` (sync) and/or `_arun` (async). You can:

- Define a Pydantic `args_schema` for inputs.
- Optionally type the return as a Pydantic model so LangChain re-runs the tool if the output doesn't validate.
- Read run-time managers if needed (rarely useful).

The example builds a `SimpleSearchTool` that calls **Tavily** (`TavilyClient(api_key=...)`) — Tavily is a free-tier-friendly LLM-targeted web search service (1000 calls/month free). Asking the agent "search for Apple intelligence" runs the search, returns titles + URLs + snippets, and the agent synthesizes a final answer from current web data.

A second `MultiplyNumbersTool` is included specifically because float multiplication tends to confuse the simple tool decorator path — `BaseTool` with a typed schema reliably parses string inputs into floats.

### What's next: multi-agent with CrewAI

Brandon ends by plugging **CrewAI**, his preferred framework for getting multiple agents to collaborate (e.g. a researcher agent feeding a writer agent). Single-agent + tools is the foundation; multi-agent setups scale that pattern. He has additional CrewAI deep-dive videos on his channel.

## Wrap-up

The course closes with a recap: chat models, prompt templates, chains, RAG, and agents/tools. All source code is free in the description, and Brandon points to his free Skool community and weekly coaching calls for follow-up help.
