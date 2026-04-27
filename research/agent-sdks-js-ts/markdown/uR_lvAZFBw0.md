# Why Top AI Engineers Don't Use LangChain

> **Source:** [Why Top AI Engineers Don't Use LangChain](https://www.youtube.com/watch?v=uR_lvAZFBw0) — [Zen van Riel](https://www.youtube.com/@zenvanriel) · 2025-11-20 · 11:45
> *Transcript generated via `youtube-captions (en)`.*

## TL;DR

- Most successful AI companies, according to **Anthropic**, don't rely on frameworks to build agents — and **Octomind** dropped **LangChain** after 12 months in production, ending up with simpler and cheaper code.
- The top 10% of AI engineers just write good Python and call the **LLM APIs** directly, skipping costly and complex framework abstractions.
- An **agentic loop** is really just a `for` loop: Python calls the LLM with a system prompt, transcript, and a list of tools; the LLM responds with structured JSON requesting tool calls; Python validates inputs and executes them.
- The LLM never executes code — it only outputs text. **Python is the control center**, which is what makes agent systems safe and reliable.
- The demo app processes meeting transcripts with multiple tools (calendar reminder, decision record, incident report), can call several at once, and finishes by asking the LLM to summarize what was done.
- Use a strong cloud model (e.g. **Claude** via **OpenRouter**) for tool calling — small local models struggle with the context demands.

## Why frameworks aren't worth it

Most successful AI companies don't use frameworks to build AI agents, according to **Anthropic**. **Octomind** dropped **LangChain** after 12 months of production and their own code became simpler and even cheaper to run. The reason is clear: most AI frameworks are just costly and complex abstractions. Relying on them is dangerous because they can teach you the wrong things and leave you stuck and frustrated.

In this video you'll learn how to build real AI agents using the approach the top 10% of engineers use — simply writing good Python code and calling the AI APIs directly. No complex frameworks required.

## The demo transcript application

The demo is an application where you create a recording, paste a text transcript (a fictional meeting in this case), and then process it with an AI agent. The agent can process the transcript in multiple ways: it can decide to create a **calendar invite** (one of the tools available to it), but it can also create a **decision record** or an **incident report** depending on the content of the meeting.

In one run, the agent results show a brief summary: "I found a project planning meeting transcript about implementing a new user dashboard. I've created a calendar reminder for November 20th." You can then download the resulting **ICS file** and add it to your calendar. The solution is free in the link in the description, and it's up to you to customize it — for example, so that the calendar invite is automatically added to your Google Calendar.

## How the agentic loop really works

To understand how the agent calls tools independently, here's the simplest diagram on the web that actually shows the agentic loop.

You have some deterministic, normal Python code that calls a language model via the regular language model APIs — for example, this is how you call **GPT** or **Claude** using the regular SDKs. The Python code passes a **system prompt** that explains the model is supposed to process the transcript, and of course passes the transcript itself to the model.

The main difference with a regular AI app is that an agentic application also gives the language model a **set of tools** it is able to request to be called. For example, a calendar tool with a description of when the tool should be called (e.g. "if the meeting contains certain things that have to be followed up on"), together with the tool name and a couple of parameters the model has to fill out in its response.

This is important to realize: **the language model cannot call any code or execute it on its own**. The only thing a language model does, as the name suggests, is output text — output language back to your Python code. The great part is that the text can be structured (e.g. as JSON) so your Python code can interpret and process it. The model might say, "OK, I want you to call the calendar tool with these 10 parameters." At that point your Python code can safely validate all the parameters and process the tool.

In this diagram, **Python is responsible for calling the tool**. Whether the tool runs Python functions, calls an external API, or even uses an **MCP server**, you have to realize it's Python doing the real code execution — not the language model.

## Why writing it yourself wins

If you write good Python code, your agentic application will be much more reliable. Instead of messing around with frameworks that try to implement abstractions around this loop, doing it yourself gives you much better control over what happens inside your application — because often it's not just a single back-and-forth between the model and Python.

Sometimes you need to go back to the language model. You can create a new request that says, "Hey, I called the tool and here is the result, can you summarize it for the end users so we can communicate what we did together?" That's why the demo app shows a nice summary transcript at the end. The LLM is being used in two ways:

1. The language model decides which tools to use, but the Python code validates inputs and calls the tools.
2. A large language model is then used to summarize what's been done, or to keep calling tools until some desired end state is reached.

This is what we call **the agentic loop**. For example, if you want to create a research agent, it might call **Wikipedia** and then, based on the results, call 10 different new web pages until a certain end goal is reached. All of that is really just a `for` loop of the diagram. You don't need difficult frameworks to abstract that away from you — all you need is to get good at Python.

## Walking through the codebase

Looking at the running application: for these agentic applications you really want to use a strong language model. Passing all the possible tool calls uses up a lot of context, and small, weaker local models don't really work that well. In this case the demo uses **Claude**, a great cloud-based model that handles tool calling very well, accessed via **OpenRouter** — OpenRouter uses the standardized **OpenAI API** so you can write one Python codebase and switch language models very quickly to experiment.

Instead of pasting the same transcript as before, here's another one: a meeting that talks about an incident that recently happened at this company. The point of this example is to show that the language model can decide to call **multiple tools at once** if that makes sense for the input.

When the request is processed, a huge JSON object is passed to the AI API. It contains descriptions for the different functions the LLM can call: `create decision record`, `generate incident report`, and the familiar `create calendar reminder`. For each of these tools (all in the `tools` array) you can see it's not just a name — it's a **description** explaining when the tool should be called, plus the **parameters** the LLM needs to pass back to the Python code so the tool can be invoked successfully.

Scrolling up, you see the standard system/user prompting any LLM app has. The system message says something like, "You are a meeting transcript processor that processes transcripts and extracts structured information... You can call multiple tools for the same transcript if appropriate, etc." The user prompt is the entire transcript.

## Phase 1: tool selection

After the request is sent, the LLM selects two tool calls. In the `agent.py` code, the "tool calls selected" object is just what's returned from the API. You can inspect this object, check that all parameters are present, and handle the tool calling later in Python. Here it returns `generate incident report` with arguments and `create calendar reminder` with arguments.

## Phase 2: tool execution

On line 126, there's an `execute_tools` method. Tools are executed via `tool_registry.execute(...)`. The repo includes wrapper code that ensures every exposed tool has an `execute` method. For example, the calendar tool's `execute` method takes a tool input and creates an **ICS calendar file**. You can replace this code so it calls the actual Google API to add a calendar invite into your real calendar — or change it however you like.

The point: at this point you just have a regular Python object you can manipulate and send over to an API. **There's nothing AI about this anymore.** That's how you make a super-reliable codebase: you can put error handling and safety checks right here, before the actual calendar invite is created.

In this run, two tools execute — the calendar reminder and the incident report. Refreshing the web page, you can scroll down to find an incident report you can copy and send to your team along with the ICS file. So both tools were called by the language model. That's the nice part of this agentic style: the model decides which tools to use, and sometimes you need multiple tools for the best solution.

## Phase 3: summary generation

The app also has a summary generation phase. Phase three passes a system prompt to the language model that explains everything that was done. The tool calls that have been made are passed back to the LLM. It's not very readable — it's basically a dump of the JSON object — but it gives the model a good idea of the tool calling that was actually executed on the Python side. The model then creates a simple summary for the user, e.g. "I found a critical incident response call in your transcript... I created a detailed incident report and set up a calendar reminder."

Again, **it's not really the AI model that's been doing that** — the Python code has. But by giving the summary of those actions back to the LLM, it can produce a final summary and pass it on to the user.

## The mental model: Python is the control center

The important mental model is that these AI systems don't execute code all on their own. **It's Python that's usually executing code based on instructions from the language model.** When you read news about AI models going rogue and breaking systems, you have to realize it's not the language model doing that — the model just outputs instructions, and there's regular code parsing that instruction and executing it.

This means that if you're good at Python, you can write much safer AI applications than people would think when they assume everything is being executed autonomously by an LLM. This realization — that **Python is your control center** for these agent systems — is super important, and it's why you should try all of this without a complex framework like **LangChain**. Frameworks abstract all of this away from you, making you think you're building a very smart system, when in the end it's usually just a `for` loop with JSON-defined function calls.

## Next steps

You'll learn a lot watching the video, but to truly get ahead you have to exercise with the transcript app linked in the description. If you want to get ahead with your AI career, you can also join the AI engineering community where the author helps others land high-paying roles and learn the skills needed for the future.
