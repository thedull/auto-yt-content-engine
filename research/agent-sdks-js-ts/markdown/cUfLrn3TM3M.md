# LangGraph Explained for Beginners

> **Source:** [LangGraph Explained for Beginners](https://www.youtube.com/watch?v=cUfLrn3TM3M) — [KodeKloud](https://www.youtube.com/@KodeKloud) · 2025-08-22 · 13:21
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **LangGraph** is an extension of **LangChain** that adds graph-based orchestration for more complex, non-deterministic agentic workflows.
- The core differentiator is the **state graph**, which lets you define **nodes** (units of computation) and **edges** (transitions, including conditional ones) with a shared persistent **state**.
- LangChain is fine for simple, deterministic tasks like a policy chatbot; LangGraph shines on multi-step research, evaluation, and looping workflows.
- A **deep research assistant** is the running example: search, scrape, evaluate trustworthiness (75% threshold), extract facts, and generate a report.
- The hands-on lab walks through sequential vs stateful processing, state graphs, node types, edge routing, loops, tool integration, memory accumulation, and a final research assistant.
- LangGraph lets you focus on **architecture and problem solving** instead of writing custom orchestration code.

## LangChain vs LangGraph: When to use which

**LangGraph** is an extension of **LangChain** that builds on top of LangChain's foundation to give additional features. And you might be wondering, wait, why not just use LangChain? Why are you making this more complicated for me? Well, that's good — because *complicated* is the perfect word to capture the essence of understanding the true difference between LangChain and LangGraph.

So, you might be asking the question: what's the true difference between LangChain and LangGraph?

If you're building a simple chatbot that answers customer questions based on a company's policies, LangChain will most likely suffice in getting the job done, since it's built for simple and deterministic tasks. However, some business requirements go way beyond a simple company chatbot.

Let's say you're asked to build a **deep research assistant** for your company that helps you go through a large swath of information gathered from various sources. In this case, the use case is a lot more complicated than a chatbot, and using LangGraph will start to make more and more sense.

One way to look at it: the threshold for changing from LangChain to LangGraph really comes down to a component called the **state graph**. Essentially, when you use a state graph you have the ability to add what's called **nodes** and **edges**.

- A **node** is an individual unit of computation — think of a function that you can call.
- An **edge** is a transition between these nodes that can either pass through or be conditional.

## Example: A Deep Research Assistant

Let's go back to the deep research assistant as an example to understand the difference with a little bit more granularity. Suppose the business requirements for the deep research assistant were to:

1. First, browse the web and find relevant details about a given topic — say, **Tesla's earnings call**.
2. Then, read and comprehend all new sources from blogs, forums, research papers, and social media.
3. Decide if the information contained is trustworthy and useful. Each source needs to surpass **75%** in order for it to be deemed trustworthy.
4. Finally, gather all the credible data and build a report.

### The traditional approach

In traditional software development, you not only have to write code that:

1. First fetches a set of links using a search engine API.
2. Loops through these links manually.
3. Scrapes the content and feeds it to a large language model.
4. Evaluates the score for each source.
5. Checks the score and only uses sources that surpass 75%.
6. Analyzes and stores these facts into a report.

You not only have to write all of this code individually but also orchestrate the sequence of how it will run in order to maintain it.

### The LangGraph approach

Now with LangGraph, the steps look a little more streamlined. The entire process can be run using a graph where each **node** is responsible for a very specific task and each **edge** determines the flow or execution steps. So in our case, we need to create nodes for the following tasks:

1. A node to **search and gather sources**.
2. A node to **scrape and clean content**.
3. A node to **evaluate trustworthiness** using an LLM.
4. A node to **extract factual statements** from the sources.
5. A node that **generates a report**.

Once all these nodes and edges are configured and compiled, LangGraph will orchestrate them by executing them based on how it's configured. So for a deep research assistant, the graph will look something like this: a starting node that serves as the entry point, all the nodes and edges that do individual tasks, and finally an end node that terminates the workflow.

## What makes LangGraph special: the State Graph

What makes LangGraph special is what's called a **state graph**, meaning all nodes have a shared state. A **state** essentially serves as a **persistent memory for the workflow** to store pertinent information at all different parts of the workflow.

So in our case of the deep research assistant, the state might look something like this:

```python
class ResearchState:
    topic: str
    remaining_urls: list[str]
    current_url: Optional[str]
    content: Optional[str]
    current_score: Optional[int]
    facts: list[str]
```

### Step-by-step execution

Now that we have the state and the graph, let's actually see how LangGraph would execute them step by step. The topic in this case will be **Tesla's earnings call**.

- The **first node** that gathers new sources and sites looks at the `topic` state and gathers information about Tesla's earnings call. It then populates all the results it got into a state variable called `remaining_urls`.
- The **next node** scrapes and cleans the content from each URL and populates the state variables `current_url` and `content` so they can be further processed by later nodes.
- The **next node** evaluates the trustworthiness of the information that was gathered, scores it properly, and appends it to the state variable `current_score`.
- Once all the URLs are scraped and scored properly, the workflow goes to the **next node** that extracts factual statements from all these sources.
- Finally, the **last node** generates a report based on the facts that are given within the state graph.

As you can see, the **state graph plays a critical role in persisting information** within the workflow, and it's an important piece in orchestrating the workflow. It's through this graph nature in LangGraph that you get additional features like **loops**, **conditional branching**, and **state management** that help you build a more complicated application than what LangChain might offer out of the box.

As enterprise adoption of agentic software grows, tools like LangChain are a natural progression toward workflow automation, and understanding when and how to use LangGraph can help you solve very interesting problems without having to write unnecessary code. LangGraph really just helps you focus on **architecture and problem solving** rather than how to implement the orchestration and how each component should run.

## Hands-on Lab: Building the research assistant

Now that we've covered the conceptual elements of LangGraph, let's look at how it works on a practical level. We can look over at this lab specifically geared toward how to use LangGraph.

### Installation

Go ahead and copy the installation command from the first section. We're setting up our complete LangGraph stack here. This includes:

- **LangGraph** itself
- **LangChain** core packages
- State management tools
- Most importantly, **DuckDuckGo** for free web searching — no API keys needed, perfect for our lab
- **BeautifulSoup** for web scraping
- The **OpenAI** integration through our proxy server

Run the installation. On the right side of your screen, you have **VS Code** where we'll be reviewing and running our code. Navigate to the `/root/code` directory and you'll see folders for each task we'll be working through.

### Task 2: Sequential vs Stateful processing

Let's start with understanding sequential versus stateful processing. Open the **task 2** folder. You'll see three Python files there.

**`sequential_chain.py`** — This demonstrates a traditional LangChain approach. Notice how it creates an LLM instance using `ChatOpenAI` with our proxy configuration. The chain processes three steps independently:

1. First it greets a person named Alice.
2. Then it says goodbye.
3. Finally, it tests memory by asking what the person's name was.

But look closely at line 36 — the farewell prompt doesn't even receive the name. And predictably, the memory check has no idea, because each step is completely independent.

**`stateful_graph.py`** — This is where things get interesting. Look at how it defines a `ConversationState` class using **TypedDict** starting at line 13. This state structure persists throughout the workflow. The graph has three nodes:

- `greet_person`
- `say_farewell`
- `check_memory`

Notice how the farewell function on line 42 can actually use the name from state. It says goodbye to Alice by name because the state is preserved.

Run them in your terminal:

- Run `python sequential_chain.py`. Each step is independent. The greeting mentions Alice, but the farewell is generic, and there's no memory of the name.
- Run the stateful graph script. The farewell specifically mentions Alice because the state was preserved, and the memory test confirms the name is still accessible.
- Finally, run the comparison script to see both approaches side by side.

### Task 3: State Graph deep dive

Now let's dive into **state graph**, which is really the heart of LangGraph. Open the **task 3** folder and look at `state_graph_demo`. This **shopping cart** example perfectly illustrates state persistence and accumulation.

The code defines a `CartState` with `items`, `total`, and `status` fields. Watch how each node doesn't replace state, but adds to it:

- The `add_apple` function (line 18) takes the existing items list and adds apple to it. It doesn't replace the list — it creates a new list with the existing items plus the apple.
- The `add_banana` function does the same thing, adding to the accumulated state.

Run the demo and watch the output carefully. You'll see the state grows at each step:

1. First, the cart is empty.
2. Then it has an apple with **$5** in total.
3. Then both apple and banana with an **$8** total.
4. Finally, the checkout adds a **paid** status.

The status persisted and accumulated throughout the entire workflow.

### Task 4: Nodes in detail

Open **task 4** and examine `nodes_demo`. The code demonstrates four different node types:

- **Simple function nodes** — Just transform data. They might uppercase text or perform calculations.
- **LLM-powered nodes** — Use language models to generate content or make decisions.
- **Tool-using nodes** — Reach out to external services like web searches or databases.
- **Conditional nodes** — Examine the state and decide where the workflow should go next.

Run the nodes demo. Each node serves a specific purpose, but they all follow the same pattern: receive state, process it according to their function, and return updates. They're like specialized team members, each with a unique skill.

### Task 5: Edges and routing

Open **task 5** and look at `edge_routing_demo`. This demonstrates how to control workflow with **conditional routing**. The router function examines the state and makes decisions about which path to take. Look for the `add_conditional_edges` call — this is where the intelligence happens. Based on the router's decision, the workflow follows different paths.

Run the demo. Watch how the workflow chooses different paths based on conditions. This conditional routing transforms a simple pipeline into an intelligent system that can adapt to different situations.

### Task 6: Loops and iterations

Now let's explore **loops and iterations**. Open **task 6** and examine `loops_demo`. The key here is the `should_continue` function. It checks both an iterator counter and the quality score to decide whether to loop back or proceed. This prevents infinite loops while allowing iterative refinement.

It's like doing research yourself: you search, evaluate what you found, and if it's not good enough, you search again with better keywords.

Run the loops demo. Notice how it searches, evaluates quality, and loops back if needed — up to a maximum of three iterations. Each iteration can be different: the search query can be refined based on what was learned previously.

### Task 7: Tool integration

**Tool integration** is what connects your workflow to the real world. Open **task 7** and look at `tools_demo`. The `search_tool_node` function shows how to integrate **DuckDuckGo**. It takes a query from state, searches the web using **DDGS**, processes the results to extract relevant information, and adds them back to state.

The beauty is that, to the workflow, this tool node looks just like any other node. Watch how seamlessly external web search is integrated into the workflow — no special handling needed. It's just another node doing its job.

### Task 8: Memory and state accumulation

For memory and state accumulation, open **task 8** and examine `memory_demo`. This demonstrates how state builds knowledge over time. The `MemoryState` class defines lists that accumulate data: questions, search results, key points. Each node adds to these lists rather than replacing them.

Look at the **accumulator pattern**. It reads existing data, generates new data, combines them, and returns the accumulated result.

Run the memory demo. See how the knowledge builds up step by step:

- Questions are generated and stored.
- Search results are added without removing the questions.
- Key points are extracted and added alongside the existing data.
- Finally, everything is synthesized into a report while preserving all the intermediate data.

### Task 9: The complete research assistant

Finally, let's look at the **complete research assistant**. Open **task 9** and examine the research assistant file. This brings everything together. The `ResearchState` includes all the fields we need:

- `topic`
- `questions`
- `search_results`
- `findings`
- `iteration_count`
- `quality_score`
- `final_report`

The workflow includes nodes for each step of the research process, conditional edges for quality-based routing, and a loop that allows iterative refinement. There's also a **Streamlit** app file that provides an interactive web interface — if you want to see the workflow visualized in real time, you can run that command. But let's run the command-line version first.

Give it a research topic and watch the entire workflow execute. You'll see it:

- Generate multiple research questions based on the topic.
- Search for information on each question.
- Evaluate the quality of what it found.
- Potentially loop back with refined searches if needed.
- Finally synthesize everything into a comprehensive report.

## Why this matters

What you've built here is fundamentally different from a simple chatbot. This assistant can **adapt its approach based on what it discovers**, refine its searches based on initial results, and build comprehensive knowledge from multiple sources.

Each component we explored plays a crucial role in creating this intelligent system:

- **State graph** for workflow management
- **Nodes** for processing
- **Edges** for routing
- **Loops** for refinement
- **Tools** for external data
- **Memory** for accumulating knowledge

The validation happening behind the scenes confirms each step is working correctly. You've successfully built a production-ready AI research assistant using LangGraph's powerful workflow capabilities.
