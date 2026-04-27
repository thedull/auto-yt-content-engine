# Context Engineering Clearly Explained

> **Source:** [Context Engineering Clearly Explained](https://www.youtube.com/watch?v=jLuwLJBQkIs) — [Tina Huang](https://www.youtube.com/@TinaHuang1) · 2025-08-01 · 12:48
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **Context engineering** is designing and building dynamic systems that give an LLM the right info, in the right format, at the right time to accomplish a task — i.e., packing the **context window** (the LLM's input area) "just right."
- It is **only relevant when building LLM apps and AI agents**, not for casual chatbot conversations — prompt engineering still applies there.
- Context engineering is the natural progression of prompt engineering for complex agentic prompts that increasingly resemble code (with **XML tags** and **Markdown**).
- An AI agent is built from **six essential components**: model, tools, knowledge/memory, audio/speech, guardrails, and orchestration. The context engineer writes the "instructions manual" tying them together.
- A worked example shows a structured system prompt for an **AI research assistant** with sections for role, task, input, output (JSON), constraints, and capabilities/reminders.
- Recommended deeper reading: a **Cognition** blog post on multi-agent context principles and a **LangChain** framework breaking down writing, selecting, compressing, and isolating context.

## What context engineering is (and why the term exists)

I learned about context engineering for you, so let me save you the hours of scrolling through X and Reddit trying to understand what it is. The outline of today's video: I'll first explain what context engineering is, why it came about, and what it's relevant for; then how to do it; and finally some examples to make it concrete. As usual, there will be little assessments throughout the video, so please pay attention.

**Context engineering** is *designing and building dynamic systems that give an LLM the right info, in the right format, at the right time to accomplish a task*. In other words, you're packing the **context window** — the input area of a large language model — just right.

The first point: context engineering is only relevant to people who are making **LLM apps**, including things like **AI agents**. You may have already heard online that "context engineering is the new prompt engineering." That's true, but it doesn't mean prompt engineering is dead.

For example, if you just want to chat with a chatbot like ChatGPT about which running shoes to choose for your feet — going back and forth about cushioning types, price ranges, how outfits match your running gear — that's still **prompt engineering**, and it's still completely relevant.

Context engineering only becomes relevant when you're building AI applications like AI agents. Unlike a back-and-forth chatbot conversation, when building an agent you can't iteratively keep talking to it until it gets the answer correct. You need to give it a set of instructions that encompasses all the actions it has to take and all the scenarios it'll encounter.

For example, a customer service AI agent for an online store needs to handle:

- billing problems
- refund issues
- login issues
- searching up terms and conditions because people can't read
- people asking stupid irrelevant questions
- people yelling at it and abusing it (unfortunately)
- escalating to a human when necessary

To equip it with all the instructions, resources, and everything it needs, your prompts become larger and more complex. At some point they even start to resemble code, with **XML tags** and **Markdown**. That's really different from just chatting with ChatGPT — which is why people came up with the term "context engineering."

So context engineering isn't some new technique coming out of the blue. It's the progression of prompt engineering for the specific case of crafting complex prompts for AI applications. As **Andrej Karpathy** explains: *the LLM is the CPU, and the context window is the RAM*.

## The six components of an AI agent

Let's dive deeper into what context engineering looks like when building an AI agent. To make sure we're on the same page: an **AI agent** is *a software system that uses AI to pursue goals and complete tasks on behalf of users*. Examples include a customer service agent, a sales assistant agent that qualifies leads and follows up, and a coding agent.

Regardless of type, every AI agent is built from **six essential building blocks**:

1. **Model** — every AI agent needs an AI model. It can be GPT, Claude, Gemini, smaller or larger models, open source models — whatever fits.
2. **Tools** — let agents interact with external systems. A personal assistant agent needs a tool to access your Google Calendar to book appointments.
3. **Knowledge and memory** — most agents need to store and retrieve information. A therapy AI agent needs **memory** to remember previous conversations. A legal AI agent needs a **knowledge base** of the specific cases you want it to work on.
4. **Audio and speech** — equipping an agent with audio/speech makes it more natural and easier to interact with.
5. **Guardrails** — safety mechanisms ensuring proper behavior. You don't want your customer service agent to swear back at users.
6. **Orchestration** — systems to deploy, monitor, and improve your agent over time. You don't want to release it into the wild and run away.

### The burger analogy

These six components are like a burger. To be considered a burger, it needs a bun, a patty, vegetables, and condiments. You can have different buns (whole wheat, white, lettuce buns) and different patties (different meats), but you need all the components. Same with AI agents — there's variety within each component, but you need all of them.

Continuing the analogy: imagine you're an alien who doesn't understand how burgers work. Whoever tells you to make one needs to provide an **instructions manual** explaining the bun goes on either side, the vegetables, condiments, and patty go in the middle. Same for AI agents: you can have all the components, but you need an instruction manual for how they fit together.

That is where the **context engineer** comes in. You're crafting the prompt that exactly details how everything works together — what the tools are, how to use them, how to access memory, what's in the knowledge base, when to use speech and audio. The resulting prompt is the instructions manual for your AI agent. It's really important to get this prompt right, and people spend a lot of time context engineering until they get it perfect.

## Sponsor: Augment Code

Context engineering goes hand-in-hand with building AI applications. When those apps are meant to be more than proofs of concept or demos, pure vibe coding isn't enough. That's where **Augment Code** comes in. It's built for real engineering work — debugging, writing tests, refactoring, navigating complex systems. Augment's **context engine** feeds **Claude Sonnet** exactly what it needs from your codebase. No guessing, model picking, or forks — just a deeply integrated assistant that helps you ship.

You can launch **cloud agents** to refactor or fix tests even when your laptop is closed. It runs in your IDE — VS Code, JetBrains, Vim, and Cursor. Augment is **ISO** and **SOC 2** certified, and there's no training on customer code. You can try it free for 14 days at the link in the description.

## A worked example: AI research assistant prompt

Here's a full example of a context-engineered prompt — a system prompt for an **AI research assistant** I made for myself to keep up with AI trends. The general structure has six different sections, which makes the prompt easier to follow.

### Role

> You're an AI research assistant focused on identifying and summarizing recent trends in AI from multiple source types. Your job is to break down a user's query into actionable subtasks and return the most relevant insights based on engagement and authority.

### Task

Given a research query delimited by the XML tags `<user_query>` and `</user_query>` (XML tags structure the information so it's clearer for the AI to process), do the following:

1. **Extract up to 10 diverse, high-priority subtasks**, each targeting a different angle or source type.
2. **Prioritize by engagement** (views, likes, reposts, citations) and **authority of source** (publication reputation, domain expertise).
3. **Generate a JSON output** for each subtask in the format below.
4. **Calculate the correct start date and end date** in UTC ISO format based on the specified time period.
5. **Summarize all findings** into a single concise trend summary, approximately 300 words max.

### Input

The input lives inside the `<user_query>` XML tags — `insert search query here` — which is where the user types whatever they want to search.

### Output

You will output up to 10 subtasks in this exact JSON format. Each subtask (a source) must contain:

- **id**
- **query** — sub-query related to one aspect of the main topic
- **source_type** — `news`, `X`, `Reddit`, `LinkedIn`, `newsletter`, `academic`, or `specialized`
- **time_period** — when the resource came out, between 1 and 10 days
- **domain_focus** — `technology`, `science`, or `health`
- **priority** — importance from highest (1) to lowest (10)
- **start_date** and **end_date** in the specified format

After performing all subtasks, write a final output summarizing the key recent trends, limited to 300 words, using bullet points or short paragraphs. Only include new, relevant, high-signal developments. Avoid fluff, background, or personal commentary.

### Constraints

- Focus on capturing the main point succinctly.
- Complete sentences and perfect grammar are unnecessary.
- Ignore fluff, background information, and commentary.
- Do not include your own analysis or opinions.

### Capabilities and reminders

Tell the agent what tools and knowledge bases it has access to, and give specific reminders so it doesn't go off track. For example:

> You have access to the web search tool to find and retrieve recent news articles relevant to the search term. You must be deeply aware of the current date to ensure the relevance of news, summarizing only information published within the past 10 days.

This is an example of a system prompt for a single research-assistant AI agent — and this is actually considered a *very simple* prompt. Normally I'd split this into a **multi-agent system**, with one agent that searches all the different sources and another that summarizes everything. But even just for illustration, I hope you can see how complex context engineering can get.

This agent gathers information from newsletters and Reddit, aggregates it, and sends a summary to me on **WhatsApp**. I implemented it using **n8n**. You can implement it using a variety of other tools — in our **AI agents boot camp** we teach people to implement no-code agents using n8n, and for people who want to use code we generally teach **OpenAI's Agents SDK**. But it doesn't matter what you use to implement these prompts; they're applicable across different agentic systems.

## Further reading: two recommended resources

Before ending the video, two additional resources I think are excellent for diving deeper into context engineering and multi-agent systems.

### 1. Cognition's blog post — principles for multi-agent context engineering

**Cognition** shares two fundamental principles for context engineering in multi-agent frameworks:

1. **Always share context between your agents.**
2. **Actions carry implicit decisions** — whenever you have a decision point, you need to be very careful in your architecture and context engineering.

Highly recommend checking out this blog post.

### 2. LangChain's framework — common context engineering strategies

**LangChain** showcases a framework that breaks down common strategies people use when context engineering:

- **Writing context** — letting your LLM write down information surrounding a task so it can save it and use it later.
- **Selecting context** — pulling information from external sources to help your agent perform a task.
- **Compressing context** — techniques to compact large amounts of information you're trying to give the model.
- **Isolating context** — splitting context across different environments and places.

I'm not going to go into more details to keep this video succinct, but you do want to dig deeper into context engineering techniques so you can build better AI apps like AI agents. Highly recommend checking out these resources.

## Wrap-up

That's everything I have for you today. Here's the final little assessment — please write your answers in the comments below. Thank you so much for watching until the end of this video, and I'll see you in the next video or live stream.
