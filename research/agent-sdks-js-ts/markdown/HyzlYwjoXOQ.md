# Claude's Model Context Protocol is here... Let's test it

> **Source:** [Claude's Model Context Protocol is here... Let's test it](https://www.youtube.com/watch?v=HyzlYwjoXOQ) — [Fireship](https://www.youtube.com/@Fireship) · 2025-03-31 · 8:08
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **Model Context Protocol (MCP)** is a new standard from **Anthropic** for giving large language models structured context — described as a "USB-C port for AI applications."
- MCP recently became an official standard in the **OpenAI Agents SDK**, signaling broad industry adoption.
- An MCP server exposes two main primitives to a client: **resources** (read-only data, like GET requests) and **tools** (actions with side effects, like POST requests).
- The video walks through building an MCP server in **Deno/TypeScript** that connects a **Postgres** database, a storage bucket, and an existing REST API, all hosted on **Sevalla**.
- The server is consumed by **Claude Desktop** as the MCP client, which can then fetch context, attach files/images, and call tools to mutate data — with **Zod** schema validation preventing hallucinated arguments.
- Anthropic's CEO claims 90% of coding will be AI-generated within 6 months and nearly all of it within a year — the host presses X to doubt and warns about agents wiping out customer data.

## MCP and the rise of the vibe coder

It seems like every developer in the world is getting down with **MCP** right now. Model Context Protocol is the hot new way to build APIs, and if you don't know what that is, you're NGMI. People are doing crazy things with it — like one developer who got Claude to design 3D art in **Blender** powered entirely on vibes. Just a few days ago, MCP became an official standard in the **OpenAI Agents SDK**.

If you're an OG subscriber to this channel, you probably know what a **REST API** is. You might even know about **GraphQL**, **RPC**, or maybe many years ago you used **SOAP**. When I was a kid, the software engineering gatekeepers told me I couldn't be a web developer unless I could explain the difference between these architectures and protocols. Well, now the turns have tabled and these gatekeepers have been utterly demolished, because we're all just vibe coders now — embracing the exponentials, pretending code doesn't even exist, and just chilling with LLMs until we get the end result we're looking for.

That being said, you can't call yourself a true vibe coder unless you know about Model Context Protocol.

## What MCP actually is

MCP is basically a new standard for building APIs that you can think of like a **USB-C port for AI applications**. It was designed by **Anthropic**, the team behind Claude, and provides a standard way to give large language models context. They're so bullish on this technology that the CEO of Anthropic said he expects virtually all code to be written by AI by the end of the year.

In today's video we'll actually build an MCP server and find out if it can truly make the world a better place by eliminating all white-collar jobs. It is March 31st, 2025, and you're watching The Code Report.

Contrary to popular belief, **Fireship** is still a tutorial channel. In today's video we'll take a storage bucket, a Postgres database, and a regular REST API, and then connect them all together with the Model Context Protocol. Not only will this allow Claude to have access to data it didn't have before, but it can also execute code on our server — like writing to the database or uploading files. People of the internet are already using it to do crazy stuff like automated stonk and shitcoin trading, industrial-scale web scraping, and as a tool to manage cloud infrastructure like your Kubernetes cluster.

## Hosting on Sevalla

Speaking of which, to build our own MCP server we'll need some cloud infrastructure, and one of the best places to do that is **Sevalla**, which itself is powered by **Google Kubernetes Engine** and **Cloudflare** under the hood. They were nice enough to sponsor this video, but the reason I like their platform so much is that it's far easier to use than something like AWS, but provides linear, predictable pricing — unlike most of the application and database hosting startups out there. And it's free to get started, which makes it perfect for this project.

## Architecture: clients, servers, resources, tools

Like other API architectures, MCP has a **client** and a **server**. The client in our case will be **Claude Desktop**, then we'll develop a server that maintains a connection with that client so the client and server can pass information back and forth via the **transport layer**.

In a REST API, you have a bunch of different HTTP verbs that you can send requests to via different URLs. But in the Model Context Protocol, we're really only concerned with two main things: **resources** and **tools**.

- A **resource** might be a file, a database query, or some other information the model can use for context. Conceptually you can think of it like a GET request in REST.
- A **tool** is an action that can be performed, like writing something to a database. So that'd be more like a POST request in REST.

What we do as developers is define tools and resources on the server so the LLM can automatically identify and use them when they have a prompt that needs them.

## The Horse Tender pivot

In my life I've been working on an app I consider my magnum opus called **Horse Tender**, but as it turns out, swiping left and right was a bad feature idea — because horses don't have fingers. So like every other failing startup in Silicon Valley right now, we're going to pivot to artificial intelligence.

Luckily we can leverage our existing data and servers. Here in Sevalla I have a **storage bucket** that contains all of the photos that my users uploaded. In addition, for user data we have a **Postgres database** with all the profile data for each one of our horses, as well as the relationships they form together. And then finally, I have a traditional **REST API written in TypeScript** that fetches this data for my web, iOS, and Android apps.

What's especially cool about my code is that it's in a Git repo hooked up to a CI/CD pipeline. That means after we write our Model Context Protocol server, we can push our code to the dev or staging branches to test it before it actually goes into production. Sevalla automatically handles all the deployments and cache busting for us.

## Building the MCP server in Deno

And now we're ready to jump into some code. Here I have a **Deno** project, and the first thing you'll notice is that I'm importing a class called `McpServer`. This comes from the official SDK, but if you're not using TypeScript they have a bunch of other languages like Python, Java, and so on. We'll also be using **Zod**, which is a tool used for schema validation that allows us to provide a specific data shape to the LLM so it doesn't just hallucinate a bunch of random crap.

### Adding a resource

After we create a server, we can start adding resources to it. The resource will first have a **name** like `horses-looking-for-love`, then the second argument is a **URI** for the resource, and finally the third argument is a **callback function** that we can use to fetch the data. In this example I'm writing a query to our Postgres database, which is hosted in the cloud on Sevalla and accessed on the server with the **postgres.js** library — but you could access any data here. When something is a resource, though, it should only be used for fetching data where there's no side effects or computations.

### Adding a tool

If you do have a side effect or computation, you should instead use a **tool**. For Horse Tender, we might want the AI to automatically create matches and set up dates between horses. We already have a RESTful API endpoint that can handle that, and we could actually leverage that code here — essentially creating an API for our API. In fact, many of these MCP servers are actually just APIs for APIs, and that sounds like dumb over-engineering, but having a protocol like this makes it a lot easier to plug and play between different models and just makes LLM apps more reliable in general.

Case in point: notice how I'm using **Zod** here to validate the shape of the data going into this function. That prevents the LLM from hallucinating random stuff. Basically when you prompt Claude, it's going to need to figure out the proper arguments to this function, so providing data types along with a description will make your MCP server far more reliable.

### Running the server

The final step is to run the server. In this case I'm going to use **standard IO** as the transport layer to use it locally, but if deployed to the cloud you can also use **server-sent events** or **HTTP**. Congratulations — you just built an MCP server.

## Connecting Claude Desktop as the client

But now the question is, how do we actually use it? You'll need a client that supports the Model Context Protocol, like **Claude Desktop**. There are many other MCP clients out there if you don't want to use Claude Desktop, like **Cursor** and **Wisor** for example, and you could even develop your own client — but that's an entirely separate topic.

Once installed, you can go to the developer settings, which will bring you to a config file where you can add multiple MCP servers. In the config file all you have to do is provide a command to run the actual server, which in our case would be the `deno` command for the `main.ts` file where we find our server code. You'll need to restart Claude, but then it should show your MCP server is running. In this case my horse is running, which means I should probably go and catch it.

Then you can go back to the prompt screen to attach it. That's going to fetch the resource from the server so Claude can use it as context in the next prompt. And because Claude is multimodal, you could also add PDFs, images, or anything else to the context really — like all the horse images in our Sevalla storage bucket.

## Prompting and tool use in action

Now magically you can prompt Claude about things specific to your application. If we want to find out which horses are single and ready to mingle, we can make a prompt like this and it will use the context that we just fetched from our database. Then if we want Claude to write to the database, we could make a prompt like this where it'll connect two horses from the context on a date. You'll need to grant a permission to do this, and then Claude will automatically figure out which data to send — based on the schema we validated with Zod — and it'll use our server tool to mutate data in the actual application.

## The bullish AI future (with a dose of doubt)

I can't imagine anything ever possibly going wrong here. Anthropic is extremely bullish on this being the future. Their CEO just said that **90% of coding will be done entirely by AI within the next 6 months**, and nearly all code will be AI-generated within a year. I'm going to go ahead and press X to doubt there, and I think it's only a matter of time before some AI agent accidentally wipes out billions of dollars in customer data or becomes self-aware and just deletes the data for fun.

That being said, there's all kinds of amazing tools being built with MCP right now, and you can check those out on the **awesome-mcp** repo. Just please make sure to vibe code responsibly.

Huge thanks to Sevalla for making this video possible and enjoy this $50 stimulus check to try out their awesome platform. This has been The Code Report — thanks for watching and I will see you in the next one.
