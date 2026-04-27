# LangGraph vs LangChain vs LangFlow vs LangSmith: Which One To Use & Why?

> **Source:** [LangGraph vs LangChain vs LangFlow vs LangSmith : Which One To Use & Why?](https://www.youtube.com/watch?v=ldBsvhjEREc) — [FuturMinds](https://www.youtube.com/@FuturMinds) · 2024-08-22 · 9:44
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **LangChain** is an open-source framework for building LLM applications, providing abstractions for prompts, chains, indexes, memory, and agents.
- **LangGraph** is built on top of LangChain to manage agents and multi-agent workflows using a graph of state, nodes, and edges with cyclical decision-making.
- **LangFlow** is a drag-and-drop visual interface (built on LangChain) for prototyping LLM workflows quickly — not generally meant for production.
- **LangSmith** assists across the entire LLM application lifecycle (prototyping, beta testing, production) with monitoring, evaluation, and tracing — and works with any LLM framework, not just LangChain.
- Use LangChain for prompt chaining, LangGraph for multi-agent / cyclical workflows, LangFlow for quick prototyping/MVPs, and LangSmith for observability and evaluation.

## Introduction

If you're working on language models like **GPT-4** or **Llama 3** and want to build powerful AI applications, you have probably come across **LangChain**, **LangGraph**, **LangFlow**, and **LangSmith**. But how do they differ, and which one should you use? I'll explain everything you need to know with examples.

In this video we'll explore what each technology is, how they are used, compare them with each other, and also answer the most common questions developers have. By the end of this video you will be clear on which one fits your needs best.

If you are interested in learning and building cool tech and AI-related stuff, consider subscribing to this channel and hit the bell icon so that you don't miss any updates. Let's get started.

## LangChain

Let's talk about LangChain first. Let's understand LangChain with the help of an example.

Say you want to build an application that will use:

- **GPT-4** to generate an initial response
- **Llama 3** to refine that response
- An **agent** that decides whether to fetch external data or generate a response based on the query
- **Memory** to store previous interactions with the user

Without LangChain, you would need to manually manage all of these components and write a lot of code to handle the logic, API calls, and memory. The code would look like this: you'll need to write a function to make an API call to GPT-4, another function to make an API call to Llama 3, then you'll need to create your own memory and manage it and update it, and you'll need to write your own code to create agents and all the related tools that the agent would use.

You can easily see the challenges with this approach. There will be lots of boilerplate code, and you'll need to manage all the API calls and manually code the agent's decision-making process. As the logic grows complex, the code becomes harder to maintain and scale. That's where LangChain comes into the picture.

**LangChain** is an open-source framework for building applications powered by language models, helping developers chain prompts, interact with external data, and build applications that remember context. Let's break down the key features that make LangChain so powerful:

- **Abstractions** — LangChain makes it easier to work with LLMs by providing pre-built steps and concepts that you can chain together.
- **LLM support** — It supports almost any LLM, whether it's closed-source models like GPT-4 or open-source ones like Llama 3. You just need to plug in your API key.
- **Prompts** — LangChain has prompt templates so you don't need to hardcode any query. You can customize prompts dynamically for different tasks.
- **Chains** — Chains are the heart of LangChain. You can connect different tasks like calling an LLM, retrieving data, and processing responses in one seamless workflow.
- **Indexes** — LangChain lets you use indexes like document loaders and vector databases to pull in external data, so your models aren't limited to what they were trained on.
- **Memory** — One big advantage: LangChain enables your application to remember past interactions, adding long-term memory to your workflows.
- **Agents** — These components use the LLM as a reasoning engine to decide the next step in a workflow, making your application more dynamic and responsive.

So in our example, this is how the code would look like with LangChain. First we'll need to import LangChain, and then we can just use the **memory** class from LangChain to create and update memory. Then use the **agent** class to create agents, and then use **sequential chain** to create chains and connect various functions.

## LangGraph

Next let's talk about **LangGraph**. LangGraph is built on top of LangChain to manage agents and their workflows. This library enables developers to create agents and multi-agent workflows. It is an open-source library and so it's free to use.

So how is it different from LangChain? While LangChain is great for prompt chaining, LangGraph excels at handling multiple agents in more structured workflows. If you're building a system where multiple agents interact to solve complex problems — for example, task automation or research assistants — you can consider using LangGraph.

LangGraph has a concept of a **graph**, which has three core components:

1. **State** — The state is a shared data structure that represents the current snapshot of the application. It maintains information that can be updated and accessed by different parts of the graph. A typical state might include user inputs, agent outcomes, and a list of actions taken throughout the workflow.
2. **Nodes** — Nodes represent the individual components or actions within the graph. Each node can perform a specific task, such as executing an LLM, running a function, or interacting with external tools.
3. **Edges** — Edges connect nodes and define the flow of execution within the graph. They determine how data moves from one node to another. This is not a directed graph, which means nodes can make decisions about which node they want to call next, and they can talk to each other back and forth.

You can use LangGraph when you need to create agents that require **cyclical interactions** and decision-making processes. It is also ideal for scenarios where multiple agents need to collaborate and work together.

Using LangGraph in your application is really straightforward — you just need to download the package, then import it in your project, and then start using the classes provided by this library.

## LangFlow

Next let's talk about **LangFlow**. Imagine building AI-powered apps like chatbots or data processing tools without having to write code. Well, LangFlow makes that possible with its **drag-and-drop interface**.

LangFlow is built on top of LangChain and provides a visual interface to build and experiment with LangChain flows. It's perfect for prototyping LLM applications, and it allows users to quickly design workflows, chains, and agents and test them. It is mostly **not intended to be used in production**, but rather for prototyping. It's perfect for teams looking to create minimum viable products quickly. You can consider other tools like **Relevance.ai** or **Dify** as well.

There are a couple of ways you can use LangFlow:

- **DataStax LangFlow** — Of course this is not going to be free, but this is one option.
- **Self-hosted** — Install it locally or host it on your cloud server. You can find all these instructions in the LangFlow documentation.

Once it's hosted on your cloud server or DataStax, you can access LangFlow on a UI where you can drag and drop various tools and services, connect them together, and create an entire AI workflow. You can then access this workflow using APIs from anywhere else — so if you have a separate application from where you want to trigger this workflow, you can do that. You can find all the information on how to use this API or the CLI in the LangFlow documentation. You can find the link to that documentation in the description.

## LangSmith

Finally, let's talk about **LangSmith**. Building your LLM-based application is one part, but deploying and testing and making sure that all of your agents and LLM calls are working as expected — that they're not overdoing something and they are returning the results as expected, while also monitoring the number of tokens that are used in each request — is really important. Without that, publishing your application to the general public is kind of risky. That's where LangSmith comes into the picture.

LangSmith is designed to assist you at all stages of the LLM application's life cycle. This includes **prototyping**, **beta testing**, and **production**. While LangChain focuses on building applications, LangSmith ensures those applications perform well by offering robust monitoring and evaluation tools. **Langfuse** and **Phoenix** are other free open-source alternatives if you want to explore.

LangSmith is designed to be independent, so you can use it with any LLM framework — using LangChain is not necessary. Which means you can connect LangSmith with LangChain and LangGraph. It provides deeper insights into how the workflows are performing, helping developers find and fix issues.

Now, when should you not use LangSmith? If your application is straightforward and doesn't require extensive monitoring or testing, the overhead of LangSmith may not be necessary.

Using LangSmith in your project is really straightforward. All you need to do is:

1. Install LangSmith and import it in your project.
2. Set up two environment variables.
3. Start logging your traces from your application by using the `@traceable` annotation.

LangSmith will receive all of these traces, and in the LangSmith dashboard you'll be able to see all the details on how many tokens were used, how many calls were made, the total cost, error rate, and latency details. You can also monitor trends — the number of calls, the number of tokens, the latencies, etc. — using all these graphs.

## Wrap-up

I'll link a video from LangChain in the description if you want to get into more details about the features — you can go through that video.

I hope this video gave a lot of clarity on which tool is meant for what and when to use which. If you found this video helpful, please like and subscribe for more content like this. If you want me to create a video on a particular topic, please let me know in the comments. Thank you for watching, and see you next time.
