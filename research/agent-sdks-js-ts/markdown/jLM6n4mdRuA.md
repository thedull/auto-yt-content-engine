# MCP Tutorial: Build Your First MCP Server

> **Source:** [MCP Tutorial: Build Your First MCP Server](https://www.youtube.com/watch?v=jLM6n4mdRuA) — [codebasics](https://www.youtube.com/@codebasics) · 2025-04-18 · 13:52
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- Walks through building a beginner-friendly **MCP server** for a real-life HR use case at **ATL Technologies** (leave management for HR manager Yupta).
- Uses the **MCP Python SDK** (`pip install mcp`) plus **UV** as the Python package manager to scaffold the project.
- Server exposes three tools — `get_leave_balance`, `apply_leave`, `get_leave_history` — backed by a mock employee database with two records.
- Connects the server to **Claude Desktop** as a generic MCP client by running `uv run mcp install main.py`, which registers the server in Claude's config.
- Demonstrates how Claude maps natural-language HR questions to the right tool calls and arguments, including parsing "4th July" into the expected date format using the function's docstring.
- Notes a common typer library error and the fix (`pip install --upgrade typer`).

## The use case: an HR agent for ATL Technologies

In this video, we are going to build a beginner-friendly first **MCP server** for a real-life use case at my company, **ATL Technologies**. Here is my team, and we have this person who is an HR manager — her name is **Yupta**. For Yupta, we want to build an HR agent which can help her with employee leave management.

The server is going to look something like this: we have an ATL employees database where you have information on their leaves, leave history, and so on. We are going to build an MCP server which will access this database. Then we will have an **MCP client**.

Usually for the MCP client, I would want something like an "ATL ChatGPT" — an internal chatbot that acts as an HR assistant to our HR manager and can help her do leave management. But since we don't want this to be a two-hour-long tutorial, I will use a generic MCP client called **Claude Desktop**. This client will make a call to our MCP server that we are building. So it's a very simple architecture.

## Installing the prerequisites

Let's install a couple of things:

- **Claude Desktop** — just Google "install Claude Desktop", click on whatever is your OS, and install it. That's pretty self-explanatory.
- **MCP Python SDK** — in your command prompt, run `pip install mcp`.
- **UV**, a Python package manager, which we will use to set up our project. Run `pip install uv`, or on Windows you can copy-paste the install command from the documentation and run it in the Windows command prompt. I installed it through the Windows command prompt. Installing software like this is pretty common-sense nowadays, so I'm hoping you will have success installing UV.

## Scaffolding the project with UV

I'm in this directory `cc/code/course/genai`, where I will build the project. You can just say:

```
uv init my-first-mcp-server
```

and it will initialize the project. Then go to that directory and you will see all the files. I have **PyCharm** open as my code editor, and you can see we have `my-first-mcp-server` with a `main.py` file, a `pyproject.toml`, a README — it just created a basic skeleton.

Now go to the page on **PyPI** for the `mcp` project, where you will see the basic help. They have a basic server example which can do the addition of two numbers. What you can do is give that code to **ChatGPT** and ask ChatGPT to generate the code for leave management.

Folks, we live in an era where you have to use AI to generate code that will make you more productive. So that's what I did: I took that code, gave it to ChatGPT, and asked it to create an MCP server for leave management. It created this particular server for me. I gave it some further prompts, made some changes, and my server is kind of ready. So I'm just going to copy-paste this code in.

## Walking through the server code

The way it works:

- You import the **`FastMCP`** class from the `mcp` module.
- You use a mock database (I'm not going to connect it with my real database). The mock database has only two employees:
  - **Employee 1** has 18 leaves and a list of leaves already taken.
  - **Employee 2** has 20 leaves (four weeks) and has not taken any leaves so far.
- You create an MCP server by creating an object of the `FastMCP` class.

Remember that in an MCP server you can have **tools, resources, and prompts**. Here we are going to have mainly tools.

### The three tools

1. **`get_leave_balance`** — pass in an employee ID, and `dict.get` will fetch that key from the dictionary, returning the employee object. From that object, you get the balance. So it will say, for example, "Employee ID E001 has 18 days leave left."
2. **`apply_leave`** — applies for a leave. It also takes leave dates. You can see this instruction in the docstring. By the way, this docstring is very, very important. Make sure you are writing a very detailed docstring, because it will guide the LLM and the MCP client to make the correct function call.
3. **`get_leave_history`** — for, say, employee ID E001, you want to know the days they have taken leave; this returns those.

The last entry is a **resource** — it's just a greeting. It will say "Hello, how can I help you?" etc.

You can run it: if you want to right-click and run the server through the editor, you can do that, but we are going to run it a little differently. So even if you don't have that option, it should work.

This code is very simple — it's your first server. I want to give you an experience of how this thing works. We are not designing 10,000 lines of code here. So I hope you get it.

## Installing the server into Claude Desktop

Now the server code is ready. As a next step, you run this command in your project directory:

```
uv run mcp install main.py
```

(`main.py` is my file name.) When you do that, you'll see "successfully installed leave-manager in `claude_desktop_config.py`" — it added this server (or installed this server) into my Claude config.

I already installed Claude Desktop, so let's run Claude Desktop now. When I open it, it is initializing the server and you can see all three tools.

### If the tools don't show up

There could be a reason where you don't see these tools. For that:

- **Enable developer mode** — there's an option somewhere to enable developer mode. I have already enabled it, so I'm not seeing the option. Just go figure that out.
- Once you have enabled developer mode, go to **File → Settings**, and in the Settings you will see a **Developer** section. I'm seeing the **leave-manager** tab there. When you click **Edit Config**, you'll see this JSON file — you can open it in your editor.

In that JSON file, I see my **leave-manager** entry. When I ran the `uv run mcp install` command, it actually added this entry into my Claude Desktop configuration. So Claude Desktop now knows that it has an MCP server called leave-manager, and to run it, it has to use the `uv` command. UV is already installed on my computer. UV is a Python project manager, and you have to run it with this particular command and this is the file.

So when Claude Desktop starts, it will notice this configuration and it will internally start this particular MCP server.

## How the client and server connect

Going back to our diagram: the MCP client (my Claude Desktop) has access to that config file, where it says "MCP servers." It has access to my leave-manager server, and the leave-manager server is running. So now when I ask a question, it will be able to pull information from the ATL database.

All the tools that are available — if you look at my code, I have:

- First tool: `get_leave_balance`
- Second tool: `apply_leave`
- Third tool: `get_leave_history`

Those tools are visible in Claude Desktop. If you look at the tools icon, you see "get leave," "apply leave" — everything is visible there.

### Common installation hiccup

Sometimes people may face issues with installation. I was also facing one issue with the **typer** library. If you are getting any "type str" error, just run:

```
pip install --upgrade typer
```

After that, the error will go away and you will be able to see all these tools.

## Demoing the HR agent in Claude Desktop

Now let me ask some questions. Let's say I'm an HR manager at ATL and I want to know **how many leaves are available for employee E001**.

When I do that, Claude Desktop is smart and it knows this is not a generic internet question — it needs to call an available tool. It figures out it needs to call `get_leave_balance`. It figured this out because it's a language model — **Claude 3.7** is a language model and knows how to map a user question to an appropriate function and supply the appropriate argument. When I say E001, it supplies that as the `employee_id` argument. It tells me 18 days. E001 has 18 days.

I can also say, for the same person, **let me know the exact dates when they took leave**. You're asking the question as if an ATL HR human would ask it, and it understands. It has context — when I say "same person," it knows I'm talking about E001. For that person, it tells me they took leave on **Christmas Day and January 1st**. If you look at the data, that is Christmas Day. How cool is this?

I can also apply for a leave. Let's say employee ID **E002** would like to apply for **4th July** — 4th July is a holiday in the US, July holiday — please apply for this leave. You can have typos like this — it's okay, it's a language model. Once again, from that input question it figures out that it needs to call `apply_leave`, along with the parameter `employee_id` and the leave date. It is so smart — I just said "4th July" and it figured out it is **7/4/2025**.

How did it convert "4th July" into this format? Using the docstring. That's why I said the docstring is important. Claude knows that the `apply_leave` function expects these leave dates in this particular format, and therefore it converted that.

So "Allow for this chat" — it is going to apply for these leaves, and it has successfully applied for them.

Now I can ask: **how many leave days are remaining for E002?** It says it has 19 days of leave. **Tell me the days of leave** — for the same person, it understands the context. For E002, it tells me 4th July. That is the answer I expect — only one day leave scheduled.

## Wrap-up

All right folks — that's it, we just built our first MCP server. I'm going to provide access to all of this code, so please go ahead and try it.
