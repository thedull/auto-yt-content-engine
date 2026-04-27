# Mastra: The AI Framework That Changes Everything

> **Source:** [Mastra: The AI Framework That Changes Everything](https://www.youtube.com/watch?v=_dG8iZgmicQ) — [Better Stack](https://www.youtube.com/@betterstack) · 2025-10-16 · 5:20
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **Mastra** is a TypeScript framework that makes it easy to build AI agents, with built-in support for **MCP servers**, custom tools, workflows, RAG, storage, evals, and observability.
- This walkthrough sticks to the basics: creating an agent, registering it, adding tools, memory, MCP integrations, and exposing it via API.
- Agents are created by instantiating the `Agent` class with a name, model, and system prompt — then registered in `index.ts` on the `Mastra` class.
- Tools are defined with `createTool` from `@mastra/core` using **Zod** schemas; memory is added via the `Memory` class with a storage backend like **LibSQLStore**.
- **Working memory** with a template lets the agent persist preferences (e.g. preferred name, currency) and use them in answers.
- MCP servers (like **Firecrawl**) plug into agents via the `MCPClient` from `@mastra/mcp`.
- For programmatic use, Mastra exposes Swagger-documented API endpoints and a `mastra-client` for cleaner responses.

## What Mastra is and why it matters

This is **Mastra AI**, a framework that makes it incredibly easy to build an AI agent in **TypeScript** that comes with MCP servers, custom tools, and so much more. If you've seen my video on the **Claude Agent SDK**, Mastra blows it out of the water. But does it do too much?

Mastra supports workflows, RAG, different storage options, evals, and observability. It's kind of overwhelming — or is it? Let's break things down. And before we do, don't forget to hit the subscribe button.

For this video, we'll focus on the very basics of agents. Let me know in the comments if you want me to do a video on workflows.

## Installing Mastra and project layout

After installing Mastra using the CLI, you'll see a lot of dependencies in `package.json`, which we'll go through later. For now, let's look at the files.

Inside the Mastra directory, delete the **workflows** folder, **weather tools**, and the **weather agent**, because we're going to create a new file called `financial-agent`.

## Creating the financial agent

In `financial-agent`, first import `Agent` from `@mastra/core/agent`. Then create a constant variable with the name of our agent that instantiates the **Agent** class. Give it:

- A **name**
- A **model**, which you can get from the list of available models that Mastra supports
- **Instructions**, which act as the system prompt — for now, something like "always respond with I don't know"

Thanks to **Whisper Flow**, we have the text in place. This is all you need to create a basic agent.

## Registering the agent

Next, register the agent by going to `index.ts`. Delete the code related to the weather agent. Then import `Mastra` from `@mastra/core` and export a variable (also named `mastra`) that instantiates the **Mastra** class. Import our agent and add it as an argument.

Now if we run the dev script, we should see our agent in the **Mastra playground** and we can communicate with it — well, almost communicate with it. Let's give it a more detailed system prompt that contains the **role definition**, **core capabilities**, and much more — all provided by the **Mastra 101 course** — which now gives a much more useful answer.

## Adding a custom tool

Next, add a file to the `tools` folder called `get-transactions-tool`. (Yes, I've spelled "transactions" wrong, but anyway.)

Import the `createTool` function from `@mastra/core`, which we use to create a tool called `getTransactions`. Give it:

- An **ID**
- A **description**
- An **output schema**, defined with **Zod**
- A function to **execute**

Then create the `getTransactions` function, which will simply return some fake data. In our agent, add a new `tools` field and add our transactions tool, which should now show in the playground.

So I can ask a question like "how much did I spend on Whimo?" and it should use the tool to give me the exact amount. But if I then ask "what is 2x that amount?" it gives an incorrect answer — because my agent doesn't have any memory.

## Adding memory

To fix that, add a `memory` field to our agent and create a new **Memory** class from `@mastra/memory`. Add a `storage` field for where we want the memory to be stored. For now, instantiate the **LibSQLStore** class from `@mastra/libsql` and store the data in memory. Of course, Mastra provides many other options.

Now Mastra will save our chats. If we ask "how much did I spend on Amazon?" we get a response, and then if I ask "what is 2x that amount?" it remembers the amount we asked for and gives the correct value.

### Working memory with a template

We can do some really cool things here, like add **working memory** with a template, which shows in the memory tab of the playground.

If I say "my preferred name is Pogo and my preferred currency is pounds," the agent uses a tool to visibly add those values. Then when I ask "what's my name and how much did I spend on Whimo?" it adds those values to memory and returns my name as well as how much I spent in my preferred currency.

## Plugging in MCP servers

We can also add tools from **MCP servers** using the **MCPClient** from `@mastra/mcp`. For example, I'm using the **Firecrawl** MCP server. Then use the `getTools` function to add the tools to my agent. Now we can see the list of tools, which we can use to scrape information from any website.

## Using your agent outside the playground

Of course, you won't be using your agent in the playground the whole time. Mastra provides documentation for all the API endpoints in **Swagger**, making it easy to communicate with my agent via API endpoints — but the response is a bit difficult to read.

Instead, we could create a **Mastra client** using the port provided by Mastra, then grab our agent and give it a prompt, which returns this value. Of course, you could customize the server to run on a different port.

## Closing thoughts

That is how you can create a super basic agent with Mastra. Of course, there's so much more you can do with this framework, but I think this is the future of working with AI. We're no longer going to use general-purpose models, but instead mold them to our specific needs to make us more productive, especially as developers.

Mastra is already being used to build **data dashboards**, **design electrical systems**, and create **AI vet assistants**.

What do you think of Mastra AI? Are you going to use it to build a custom agent? Let me know in the comments. And again, don't forget to subscribe.
