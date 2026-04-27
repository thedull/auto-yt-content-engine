# The Ultimate MCP Crash Course - Build From Scratch

> **Source:** [The Ultimate MCP Crash Course - Build From Scratch](https://www.youtube.com/watch?v=ZoZxQwp1PiM) — [Web Dev Simplified](https://www.youtube.com/@WebDevSimplified) · 2025-07-15 · 1:15:25
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- **MCP (Model Context Protocol)** is a communication protocol — like REST or GraphQL — that defines how an MCP client and an MCP server send messages back and forth.
- An MCP server is built from four primitives: **tools** (callable functions), **resources** (data), **prompts** (pre-formatted prompt templates), and **samplings** (server-to-client AI requests). Tools and resources are the most-used.
- The walkthrough builds a complete MCP server in **TypeScript** using the official `@modelcontextprotocol/sdk` plus **Zod** for schemas, with a JSON file as a fake database.
- It demonstrates testing the server with the **MCP Inspector**, then wiring it up to **GitHub Copilot** inside VS Code via an `mcp.json` config.
- The second half builds a **custom MCP client** as a CLI using `@inquirer/prompts`, the **Vercel AI SDK** (`ai` + `@ai-sdk/google`), and **Gemini 2.0 Flash** as the LLM, including handling sampling requests from the server.

## What MCP Is

MCP is incredibly popular right now. Everyone's talking about it, but no one's going in-depth enough on how it works and what it means for you. In this video, Kyle from **Web Dev Simplified** explains everything you need to know about MCP, shows how to create your very own MCP server that you can hook up to any MCP client, and then shows how to create your very own MCP client that can hook up to any server out there — whether you created it or someone else created it.

There's a really nice site for MCP (linked in the description) that goes over a lot of really good information on what MCP is and how it works. But really, **MCP is just a protocol**. It stands for **model context protocol**, and it's a protocol similar to a REST API or a GraphQL API. It allows you to communicate between an MCP server and an MCP client. Essentially, it tells you how the client and server should communicate with each other so they both know how to send messages back and forth. **One client can hook up to as many MCP servers as it wants.**

It's just a language that you can use on your client to communicate with a server, and that the server can use to send information back to the client, so they know how to work with each other properly to do all these really cool different things.

## The Four Primitives of an MCP Server

Inside an MCP server there are essentially four main things, but two of them are the most important. They are **tools**, **resources**, **prompts**, and **samplings**. Of those four, tools and resources are by far the most used, with tools probably being the most used hands down.

### Tools

**Tools** are essentially a way for a client to call code on the server. For example, with an MCP server for Excel, you could have a tool that creates an Excel document. As a user using an AI chat program, you'd say "create me an Excel sheet that has this information." The AI knows there's an MCP server for Excel that has a tool for creating an Excel sheet, so it calls that tool.

These tools can be as simple or as complex as you want — from creating an Excel sheet to doing complicated data computation in an Excel sheet to create charts. **Tools are just a way for the AI to call functions and do things inside whatever program this MCP wraps around.**

### Resources

A **resource** is quite a bit simpler — it's just a set of data. This could be a database, files on your file system, images, anything that contains data. It's something you have access to on a particular MCP server. For an Excel MCP server, resources could be the rows inside Excel tables, the Excel files themselves, or charts. For a web application, MCP resources are probably going to be database records or files that users have uploaded.

### Prompts

A **prompt** is a pre-created prompt that you can ask your MCP server for, and it'll send down a really well-formatted prompt for you to do specific tasks. This is not as useful because you can already have tools that do some of this for you, but if you specifically want to create a prompt that helps a user with something, you can create a prompt on the server, and they can ask for it and use it inside their AI client.

### Samplings

**Samplings** are kind of the opposite of everything else. Normally the AI client talks to the server. But samplings are when **the server wants to get information from an AI** and asks, "Hey, I need additional information. Can you run this prompt on your AI and then send the result back to me?" It's just the reverse of everything else.

That's pretty much all there is to model context protocol when it comes to server-client communication.

## Project Setup

We don't have to start entirely from scratch because the model context protocol site has SDKs for pretty much every language. In this case, we use the **TypeScript SDK**. Scrolling down on the SDK page, you'll find the installation step.

The starting code includes a basic `tsconfig` file (copied from the model context protocol site — just a simple Node.js TypeScript project setup) and a `package.json` with a few dev dependencies:

- `@types/node`
- `tsx` (lets us run a `dev` command that restarts the server when files change)
- `typescript`

If you were using JavaScript, you wouldn't need any of these dev dependencies or the `tsconfig`.

Three scripts are configured:

- `build` — converts TypeScript to JavaScript.
- `build:watch` — recreates those files every time something changes.
- `dev` — quickly works through the process and automatically refreshes on changes.

## Creating the MCP Server

Inside our application, we create a new MCP server:

```ts
const server = new McpServer({...})
```

We import `McpServer` from `@modelcontextprotocol/sdk/server/mcp`. We give it a name (e.g. `"test"` — you'd call it `"Excel"` for an Excel-based server) and a version (`"1.0.0"`).

We also have a `capabilities` section that says what our server is capable of. In our case: **resources**, **tools**, and **prompts**. We don't specify samplings as a capability because samplings are sent from the server to the client, so the client needs to support it, not us. To declare a capability, we just pass it an empty object.

Next, we create an async `main` function and call it at the bottom. To use an MCP server/client relationship, you need to specify the **transport protocol**. There are technically three, but really only two main ones:

- **Standard input/output (stdio)** — uses standard IO communication through a terminal. Great when the application is running locally on the same machine as the client. In our case, **GitHub Copilot** is running on the computer and our program is also running on the computer, so we can use stdio.
- **HTTP streaming** — great if you have a web application streaming this down to another web application that's not on the same network.
- **Server-sent events** — deprecated, replaced by HTTP streaming.

For the most part, all the code stays exactly the same no matter which transport you use; it just depends on whether your application is local or remote. We use `StdioServerTransport` and call `await server.connect(transport)`. Now we have an MCP server hooked up to a transport layer — it just doesn't do anything yet.

## Testing with the MCP Inspector

Before implementing complex stuff, we want to make sure what we've written actually works. We download a tool from the model context protocol team that lets us inspect everything inside our server — **it's like Postman but for MCP**. Install it as a dev dependency: `@modelcontextprotocol/inspector`.

Then we add a `package.json` script:

```
"server:inspect": "DANGEROUSLY_OMIT_AUTH=true npx @modelcontextprotocol/inspector npm run server:dev"
```

The `DANGEROUSLY_OMIT_AUTH=true` env variable is set just for testing convenience. Normally when you make changes, you have to restart the inspector, which gives you a brand new auth token and you have to manually reopen the website. Setting this to true gets rid of that auth token so we don't have to worry about restarting.

Running `npm run server:inspect` starts the inspector. We get a warning about omitting the auth token, then a URL. Opening it shows the transport type (stdio), the command (`npm run server:dev`), and a Connect button. After connecting, the **Ping Server** button runs the ping command and returns an empty response — exactly what you're supposed to get from a ping.

So we have a server, it's running, we can connect — we just don't have any tools, prompts, or resources yet.

## Building the First Tool: `create_user`

To create a tool, we use `server.tool()`. Every tool needs a **name** — `"create-user"` — which the AI will see. Next, a **description** the AI uses to determine what the function does: `"Create a new user in the database"`.

Then we pass along the parameters using **Zod**. (You can use JSON schema or Zod with this library, but Zod is much easier to work with.) After installing `zod`:

```ts
{
  name: z.string(),
  email: z.string(),
  address: z.string(),
  phone: z.string(),
}
```

Next come the **annotations**, which provide hints to the AI:

- **title** — a more human-readable string for the user (e.g. `"Create User"`).
- **readOnlyHint** — false here, since this creates data. Helps the AI know this manipulates data.
- **destructiveHint** — false here, since it doesn't delete data. If destructive, the AI may warn the user.
- **idempotentHint** — false here, because running it multiple times with the same input creates multiple users. (Think: is this a pure function?)
- **openWorldHint** — true here, because we're interacting with a fake database that's external to the application.

These annotations are all **optional**. The reason for passing them along is to give the AI the best possible chance of using the tool well.

Finally, the function itself receives the params. To interact with a user database, we need a database. Here, we just use a **`users.json` file** with three placeholder users. It could be a real database or an API request — it doesn't matter how you interact with your data.

The function is wrapped in a try/catch so we can return an error to the AI. AIs expect a very specific response: an object with a `content` array. Each content item has a `type` (here `"text"`) and the text. On error: `"Failed to save user"`. On success: `"User ${id} created successfully"`.

Inside the `try`, we call a `createUser` helper that returns an ID. The helper:

1. Uses an experimental Node.js feature to **dynamically import a JSON file**: `await import("./data/users.json", { with: { type: "json" } })` — then `.then(m => m.default)` to grab the array.
2. Computes `id = users.length + 1` and pushes the new user.
3. Uses `fs/promises.writeFile` to write `JSON.stringify(users, null, 2)` back to `src/data/users.json`. (The path here is relative to the root directory, while the dynamic import was relative to the file.)
4. Returns the ID.

### Testing the tool

In the inspector, after restarting (which is easy because we removed the auth section), connect, then **List Tools**. We see `create-user` with its description. Filling in fields — name `Kyle`, email `test@test.com`, address `bogus`, phone `random numbers` — and clicking **Run Tool** returns "user 4 created successfully," and `users.json` now contains user 4.

## Hooking the Server into GitHub Copilot

In VS Code, hitting **Ctrl+Shift+P** and searching MCP shows **List Servers** and **Add Server**. We click **Add Server**. The options include stdio, HTTP, npm packages that export this configuration, Python, and Docker. We pick stdio and the command `npm run server:dev`. Name: `test-mcp-video-server` (the name doesn't matter).

We save it inside workspace settings. This creates a `.vscode/mcp.json` with all the server info, including a tool count.

### Adding debug support

We can add a `dev` option to the config to enable debugging. We set:

- `debug.type` to `"node"` (only `node` and `python` are currently supported).
- The command must match the type, so we change it from `npm` to `node` running `build/server.js`.
- `cwd` to the workspace folder.
- A `watch` glob for `build/**/*.js` so it refreshes during debugging.

We also need to actually run `npm run server:build:watch` so the build folder is populated. The build folder gets a `server.js`, which is what's hooked up. You may need to click the **Restart** button on the server. The nice thing is the output panel shows all the communication between server and client — "here I exist," "give me all your tools," etc.

### Calling the tool from Copilot

You may need to restart Copilot the first time. To run a tool directly, hit `#` inside GitHub Copilot and type `create-user`. Pressing enter, Copilot says it needs specific parameters and shows fields for name, email, address, phone. Clicking **Continue** runs the command — Copilot reports user 5 was created successfully, with the input and the response shown. `users.json` now has user 5.

You can also call indirectly: "Can you please create a new user for me with the name Kyle, the email `test@test.com`, the address `1234 Main Street`, and some random numbers for the phone." Copilot detects the `create-user` function, fills in everything, and on **Continue** creates the user.

## Adding Resources

To create a resource, use `server.resource()`. We pass a name (`"users"`), a **URI**, and properties.

The URI is a unique identifier you create yourself, but it must match a URL-like protocol format. It doesn't have to be HTTP — it could be `file://`, or your own custom scheme like `users://all`. Depending on your application, you may have your own standards or schemas. We use `users://all` here as a custom protocol.

Then additional properties:

- `description` — `"Get all users data from the database"`.
- `title` — `"Users"` (human-readable).
- `mimeType` — `"application/json"`, telling the application what type of data is returned.

The function takes a URI and returns a `contents` array (note: `contents`, not `content` — Kyle hits this typo on first run). Each item has:

- `uri` — `uri.href` (the URL of the resource being accessed).
- `text` — `JSON.stringify(users)`.
- `mimeType` — `"application/json"`.

We reuse the dynamic JSON import from the `createUser` helper to load all users.

### Testing resources in the inspector

After restarting, the inspector now lists resources. Opening `users` returns `users://all` with all user data as JSON.

### Resources in Copilot

In GitHub Copilot, you click **Add Context**. But resources don't show up at first. The reason: when an MCP server starts up, it asks the server, "What are all your resources and tools?" Our server already started before resources existed, so the client only knows about the tool. Restarting the server alone doesn't fix it; **restarting VS Code entirely** does. After that, **Add Context > MCP Resources** shows the `users` resource. Adding it as context, you can ask "What is the name of the user with the ID 4?" — and Copilot answers "Kyle."

### Resource templates: getting a user by ID

Getting a user by ID is something common. We expose it as a **resource template**:

```ts
server.resource(
  "user-details",
  new ResourceTemplate("users://{userId}/profile", { list: undefined }),
  { description: "Get a user's details from the database", title: "User Details", mimeType: "application/json" },
  async (uri, { userId }) => { ... }
)
```

The dynamic part lives inside `{userId}`. `list: undefined` ignores the matching-all-resources feature — we don't care about it.

In the function, in addition to the URI, we get the params object. `userId` is a `string | string[]`. We find the user with `users.find(u => u.id === parseInt(userId as string))`. If no user, return `contents` with text `"Error: User not found"`. Otherwise return the matching user as JSON.

In the inspector, after restart, we see **User Details** under resources. It asks for a `userId` value. Entering `4`, it returns the user. Asking "What is this user's information?" prints the user's data. This makes it easy to attach specific records into queries — e.g. "make a sale for this user" — and the AI can do different things with the data on the back end.

## Adding Prompts

Prompts are much less used than tools and resources but still handy. Use `server.prompt()`, passing a name (`"generate-fake-user"`), a description (`"Generate a fake user based on a given name"`), and parameters (`{ name: z.string() }`).

The function takes the params and returns an array of **messages** — these are the messages we want our AI to run. We have one message with `role: "user"` and `content: { type: "text", text: "Generate a fake user with the name ${name}. The user should have a realistic email address and phone number." }`.

This is a really powerful way to create really complicated prompts from very small amounts of information.

### Testing prompts

In the inspector after restart, we have a **Prompts** section. We list our prompt, give it a name like `Kyle`, click **Get Prompt** — it returns the exact prompt with the name interpolated.

### Running prompts in Copilot

Use a slash command in Copilot. We see `/mcp.test-mcp-video-server.generate-fake-user`. We give it the name `Sally`. Copilot shows the prompt: "Generate a fake user with the name Sally. The user should have a realistic email address and phone number." Hitting enter, the AI generates user info and even asks, "Would you like that to be added to your data?" Saying yes, it directly inserts the user into our JSON file.

In Kyle's setup, the AI directly read the database file and inserted the user there rather than calling `create-user`. In a real application without database file access in the project, it would use the `create-user` tool.

## Adding Sampling: `create-random-user`

Sampling bridges client and server. We do sampling inside a tool. New tool: `create-random-user`, description "Create a random user with fake data," with no params. Same annotations: not read-only, not destructive, not idempotent, open-world true.

Inside the async function, we want random fake user data. We could write a program — or just have the AI generate it. **Sampling lets us tell the AI: I have a prompt I want you to run, and then I want you to send me the result.**

We call `server.server.request(...)`. The method is `"sampling/createMessage"`. (Elicitation lets you ask the user for additional info; sampling lets you say "run this prompt on your AI.") Params include `messages` (an array with role `"user"` and a text content "Generate fake user data. The user should have a realistic name, email address, and phone number. Return this data as a JSON object with no other text or formatter so it can be used with `JSON.parse`.") and `maxTokens: 1024`. The schema for the result is `CreateMessageResultSchema`.

The result has a `content`. If `res.content.type !== "text"`, return `"Failed to create the user"`. Otherwise, in a try/catch:

```ts
const fakeUser = JSON.parse(
  res.content.text.trim().replace(/^```json/, "").replace(/```$/, "")
)
```

We trim and strip Markdown code fences because AI tools often wrap responses in Markdown. Then we call `await createUser(fakeUser)` and return `"User ${id} created successfully"`.

The whole point isn't really to be useful — you don't write code like this often — it's to demonstrate sampling.

### Debugging sampling

Testing in Copilot, the AI fails repeatedly to generate random data. After lots of debugging, Kyle realizes the **trim was in the wrong place** — placed after `JSON.parse`, so it was trimming an object. Moving the `trim()` before `JSON.parse` (as part of the chain on `res.content.text`) fixes it. Now `create-random-user` works: it sends a request to the AI, gets fake data back, calls `createUser`, and reports user 8 created. Inspecting `users.json`, user 8 has all the AI-generated info — none of which Kyle typed.

That's the basics of setting up an MCP server. You'd integrate it with your own project.

## Building the MCP Client

Now we create `client.ts`. (Normally you wouldn't keep client and server in the same project, but we're putting them side by side for testing.)

We import `Client` from `@modelcontextprotocol/sdk/client/index` and create a new client with name `"test-client-video"`, version `"1.0.0"`, and `capabilities: { sampling: {} }`. Sampling is a client capability because the server asks the client for info.

For transport, we use `StdioClientTransport` with `command: "node"`, `args: ["build/server.js"]`, and `stderr: "ignore"`. We ignore standard error because we use Node's experimental JSON import feature, which prints an experimental-warning to stderr that we don't want cluttering our CLI.

In an async `main` function:

```ts
await mcp.connect(transport)
const [tools, prompts, resources, resourceTemplates] = await Promise.all([
  mcp.listTools(),
  mcp.listPrompts(),
  mcp.listResources(),
  mcp.listResourceTemplates(),
])
```

This gets everything the server is capable of.

### CLI menu with Inquirer

We install **`@inquirer/prompts`** and **`dotenv`**, and create a `.env` file with a Gemini API key. We chose Gemini because it has a free tier.

After logging "You are connected.", we set up an infinite while loop — our main menu with options: `query` (call the AI directly), `tool`, `resource`, `prompt`. The `select` function from `@inquirer/prompts` shows them as choices with the message "What would you like to do?" Then a switch on the option.

### Handling tools

For the tool case, we use `select` again with all tools mapped to `{ name: tool.annotations?.title || tool.name, value: tool.name, description: tool.description }`. We find the tool by name and call `handleTool(tool)`.

We add a `client:dev` script: `tsx src/client.ts`. Running `npm run client:dev`, we see the menu, pick **Tools**, see our two tools with human-readable names and descriptions.

`handleTool` uses `mcp.callTool({ name, arguments })`. To collect args, we loop through `tool.inputSchema.properties` (default `{}`) — for each `[key, value]`, we call `await input({ message: \`Enter value for ${key} (${(value as { type: string }).type}):\` })`. Then we cast the result and log `(res.content as [{ text: string }])[0].text`.

Testing: Tools > create-user, name Kyle, email `test@test.com`, address random numbers, phone random letters. "User 9 successfully created" and `users.json` shows user 9.

### Handling resources

Resources case: we map both `resources` and `resourceTemplates`, taking name + uri (or `uriTemplate` for templates) + description, and select. We also do null check — if not found, log "Resource not found"; otherwise call `handleResource(uri)`.

`handleResource` needs to substitute dynamic parameters. We start with `let finalUri = uri` and use a regex like `/\{[^}]+\}/g` (matches text between `{` and `}`) to find param matches via `uri.match(regex)`. If `paramMatches !== null`, for each `paramMatch`:

```ts
const paramName = paramMatch.replace("{", "").replace("}", "")
const paramValue = await input({ message: \`Enter value for ${paramName}:\` })
finalUri = finalUri.replace(paramMatch, paramValue)
```

Then `await mcp.readResource({ uri: finalUri })`. The result's `contents[0].text` (cast to string) is JSON. We `JSON.parse` it and `JSON.stringify(obj, null, 2)` to pretty-print, since the data comes back minified.

Testing: Resources > Users prints all users prettily. User Details > userId `3` prints user 3.

### Handling prompts

Same shape: select a prompt, find it, call `handlePrompt(prompt)`. The difference: `prompt.arguments` is an array, not an object, so we loop through it and ask `await input({ message: \`Enter value for ${arg.name}:\` })`.

Then `const response = await mcp.getPrompt({ name: prompt.name, arguments: args })`. `response.messages` is an array; we loop and call `await handleServerMessagePrompt(message)`.

`handleServerMessagePrompt(message)` ignores any message whose `content.type` is not `"text"` (we don't handle images). It logs the prompt text and calls `confirm({ message: "Would you like to run the above prompt?", default: true })`. If the user says no, return; otherwise, run the prompt against an AI.

We install `ai` and `@ai-sdk/google` because we're using Gemini. Instead of importing `google` directly, we import `createGoogleGenerativeAI` and call:

```ts
const google = createGoogleGenerativeAI({ apiKey: process.env.GEMINI_API_KEY })
const { text } = await generateText({
  model: google("gemini-2.0-flash"),
  prompt: message.content.text,
})
return text
```

Testing: Prompts > generate-fake-user, name Bob. "Generate a fake user with the name Bob…" — confirm yes. We hit an error because we forgot `import "dotenv/config"` at the top. Adding it, retry — Gemini returns a fake user. (You can hook up whatever AI you want.)

### Handling queries (with tools)

For the `query` case, we call `handleQuery(tools)`. `handleQuery` asks for the user's prompt with `input`, then:

```ts
const { text, toolResults } = await generateText({
  model: google("gemini-2.0-flash"),
  prompt: query,
  tools: tools.reduce((obj, tool) => ({
    ...obj,
    [tool.name]: {
      description: tool.description,
      parameters: jsonSchema(tool.inputSchema),
      execute: async (args: Record<string, any>) => {
        return await mcp.callTool({ name: tool.name, arguments: args })
      },
    },
  }), {} as ToolSet),
})
```

The `tools` argument needs to be an object, so we `reduce` the array. The schema needs to be wrapped with the `jsonSchema` helper from the AI library. The `execute` function says: when the AI wants to call a tool, run this — it just calls `mcp.callTool` and returns the result.

Finally, we log the result:

```ts
console.log(
  text || (toolResults[0] as any)?.result.content[0].text || "No text generated"
)
```

We use `// @ts-expect-error` to ignore TypeScript strictness on the dynamic types.

Testing: Query > "How are you?" — random AI response. Query > "Can you create a random user with the name Kyle?" — "I cannot fulfill this request. `create-random-user` does not accept any arguments." Query > "Just create a random user" — fails with "method not found" because we still haven't implemented sampling on the client.

Before that: Query > "Create a user with the name Kyle, email `test@test.com`, address random address, phone random phone." — user 10 created. The AI used the tool indirectly without us telling it to.

### Handling sampling on the client

Sampling isn't built into the library directly, but it's relatively easy. We use `mcp.setRequestHandler(CreateMessageRequestSchema, async (request) => { ... })`. The request will be in the sampling/createMessage format the server sends.

We loop through `request.params.messages`. For each `message`, we call `handleServerMessagePrompt(message)`, which returns a string or undefined. We collect them:

```ts
const texts: string[] = []
for (const message of request.params.messages) {
  const text = await handleServerMessagePrompt(message)
  if (text != null) texts.push(text)
}
```

Then we send the response back to the MCP server:

```ts
return {
  role: "user",
  model: "gemini-2.0-flash",
  stopReason: "endTurn",
  content: { type: "text", text: texts.join("\n") },
}
```

`stopReason: "endTurn"` says this is the end of the client's interactions and it's back to the server.

Testing: Tools > create-random-user. Immediately we get a sampling request: "Generate fake user data. The user should have a realistic name, email address... Would you like to run the above prompt?" This is coming from server to sample our AI. Yes — the result is sent back to the server, the server creates user 11. Opening `users.json`, user 11 is there. The format wasn't exactly what was expected, but it's good enough for the use case. In a real-world application you'd have schema validation before saving. This was purely for testing — to show the interactions between clients and servers.

## Wrap-up

If you enjoyed this video and want to see more AI-related content, let Kyle know in the comments. He links a massive 10+ hour project with tons of AI features. Thanks for watching.
