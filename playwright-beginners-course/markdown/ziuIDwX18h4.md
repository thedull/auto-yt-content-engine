# Playwright with TypeScript | Setup Environment & Writing Tests (Session 1)

> **Source:** [Playwright with TypeScript | Setup Environment & Writing Tests ( Session 1)](https://www.youtube.com/watch?v=ziuIDwX18h4) — [SDET- QA](https://www.youtube.com/@sdetpavan) · 2025-10-06 · 1:37:40
> *Transcript generated via `youtube-captions (en)`.*

## TL;DR

- Walks through the prerequisites (**Node.js**, **VS Code**) and the single-command install (`npm init playwright@latest`) for setting up a Playwright + TypeScript project.
- Explains the generated folder structure: `node_modules`, `tests/`, `playwright.config.ts`, and `package.json`, drawing comparisons to Maven's `pom.xml`.
- Demonstrates writing a first **spec file** using the `test` and `expect` functions imported from `@playwright/test`, including page navigation and assertions like `toHaveTitle` and `toHaveURL`.
- Deep dive into **synchronous vs asynchronous** behavior, **promises**, and the proper use of `async`/`await` in Playwright tests.
- Tours the most important run commands: default headless run, `--headed`, `--ui`, `--debug`, `--project`, `-g` title filter, running specific files, and viewing the **HTML report** with `npx playwright show-report`.
- Closes with a high-level look at **Playwright architecture**, contrasting its **WebSocket** protocol with Selenium's W3C/HTTP-per-command model and explaining why Playwright is faster.

## Getting started and documentation

Today's class kicks off **Playwright automation**. The plan: set up the environment, understand the project files, and write a basic test. The official docs at **playwright.dev** are detailed and step by step — they cover installation, writing tests, generating tests, the trace viewer, CI setup, and every command. The instructor recommends going through the documentation in parallel with the sessions.

Playwright supports multiple languages (Python, Java, .NET, Node.js). Node.js covers both **TypeScript** and **JavaScript** — if you can write TypeScript, you can write JavaScript essentially the same way. This series uses TypeScript.

## Prerequisites: Node.js and VS Code

Playwright is a Node.js-based project, so two prerequisites are mandatory:

1. **Node.js** — required for any JavaScript/TypeScript project. Download the installer from the Node.js website (an MSI on Windows). Click through the installation; by default it lands in `Program Files\NodeJS` and brings **npm** along with it. Verify with `node --version` in the command prompt. **npm** (node package manager) is what installs every package, including Playwright.
2. **VS Code editor** — open source, used for writing and executing automation code.

You do **not** need a separate TypeScript installation to use Playwright. Playwright pulls in the necessary packages on its own. You only need TypeScript installed separately if you're practicing TypeScript independently of Playwright.

## Installing Playwright

Once Node.js and VS Code are ready, create a new folder anywhere (the instructor uses `pw-demos` under the automation directory) and open it in VS Code. The folder starts completely empty — not yet mapped to any TypeScript or Playwright project.

Open a terminal inside VS Code and run the single install command:

```
npm init playwright@latest
```

The `@latest` is the version specifier; you can pin an older version by replacing it. The installer asks several questions interactively:

- **TypeScript or JavaScript?** TypeScript is selected by default — press Enter.
- **Where to put your end-to-end tests?** Default is the `tests` folder. Accept it.
- **Add a GitHub Actions workflow?** Default is `false`. Leave it off for now; this can be enabled later to automate commit-and-push workflows.
- **Install Playwright browsers?** Default is `true`. Confirm with yes. Playwright ships with its own **Chromium**, **WebKit**, and **Firefox** browsers. (You can install browsers later manually with `npx playwright install`.)

When you see **"Happy hacking!"**, Playwright has been installed successfully. Installation is **per-project** — every new project folder needs its own `npm init playwright@latest` run.

## The generated project structure

As soon as the install completes, the folder contains:

- **node_modules** — all Playwright-related packages, including `playwright` and `@playwright/test`.
- **tests/** — where your tests live. A sample `example.spec.ts` is provided.
- **playwright.config.ts** — the Playwright configuration file.
- **package.json** — the Node.js project manifest, analogous to **`pom.xml`** in a Maven/Java project. It lists dependencies (currently just Playwright). Any extra dependencies you add later go here too.

### The `playwright.config.ts` file

This is the configuration center. Out of the box it configures three browsers — **Chromium**, **Firefox**, and **WebKit** — each treated as a **worker**. If you don't want all three to run, comment out the ones you don't need. The config also lets you enable mobile profiles (mobile Chrome, mobile Safari) and other browsers (Microsoft Edge, Google Chrome).

Other settings configured here include:

- **Test directory** — by default `./tests`, which is why Playwright searches there for spec files.
- **Parallel execution** toggle.
- **CI environment** options — number of processes, number of workers.
- **Reporter** configuration.

These will be revisited in detail in later sessions.

### Spec file naming

Test files inside the `tests/` folder must end with `.spec.ts` (or `.spec.js` if using JavaScript). The base name can be anything — `mytest.spec.ts`, `login.spec.ts`, etc. — but the `.spec.ts` extension is what Playwright uses to discover tests.

You can verify which version of Playwright is installed via:

```
npx playwright --version
```

Quick clarification on the tooling: **npm** is the **node package manager** used to install packages. **npx** is the **node package executor** used to run them. So you install with `npm` and execute with `npx`.

## Writing your first test

Right-click the `tests` folder, create a new file `mytest.spec.ts`, and start writing. Every Playwright test needs two built-in functions imported from the Playwright module:

- **`test`** — used to define a test case.
- **`expect`** — used to add assertions/validations.

Both come from the `@playwright/test` package, which lives under `node_modules` thanks to the install step. The mandatory first line of any spec file is:

```typescript
import { test, expect } from '@playwright/test';
```

The basic test syntax takes two parameters — a **title** and a **function** (typically an arrow function) containing the steps:

```typescript
test('title of the test', async ({ page }) => {
  // steps go here
});
```

You can put any number of `test(...)` blocks inside a single file.

### The `page` fixture

Playwright provides several **fixtures** — predefined global variables accessible everywhere in the project. The two main ones are **`page`** and **`browser`** (others exist and will be covered later). A fixture isn't accessed by just naming it — it must be **wrapped in curly braces** when destructured into the arrow function's parameter:

```typescript
async ({ page }) => { ... }
```

The `page` fixture represents a single page inside the browser (a `browser` is the larger container; a `page` is a subset). Since launching a URL, capturing a title, validating elements — every action and validation — happens on a page, the `page` fixture is what you'll use most.

### Launching a URL and asserting the title

Inside the function, the first step is typically navigation. Use `page.goto(...)`:

```typescript
await page.goto('https://...');
```

Note that no browser is specified — by default Playwright runs the test on **all browsers configured in `playwright.config.ts`** (Chromium, Firefox, WebKit). You can override this at runtime with command-line flags shown later.

To verify the page title, use the `expect` function with the `toHaveTitle` assertion:

```typescript
await expect(page).toHaveTitle('My Shop');
```

This passes if the page title matches the expected string at runtime, otherwise it fails. The assertion does **not** print the title — it only validates it. To capture and log the title, use `page.title()`, which returns a `Promise<string>`:

```typescript
const title: string = await page.title();
console.log(title);
```

## Synchronous vs asynchronous, promises, async/await

This is the most important conceptual block of the session, and a common interview question.

### Synchronous nature

In **synchronous** execution, step 1 finishes before step 2 starts, and so on. Java and Python follow strictly synchronous execution. In JavaScript/TypeScript, certain statements like `console.log(1); console.log(2);` also execute synchronously because they don't perform any background task.

### Asynchronous nature

In **asynchronous** execution, step 1 kicks off some background task (database call, file I/O, browser launch, network navigation) and step 2 starts immediately without waiting for step 1 to finish. Step 3 follows, and so on — all in parallel. JavaScript/TypeScript follow asynchronous behavior whenever a statement involves an external resource or background activity.

### The problem and the promise

Sometimes step 2 depends on step 1's result — for example, fetching a user from a DB in step 1 and checking whether that user is active in step 2. In that scenario, step 2 must wait for step 1 to complete. This is where **promises** come in.

A **promise** is the assurance returned by an asynchronous task. It can be:

- **Resolved** — the background task completed successfully.
- **Rejected** — the background task failed.

The analogy: someone *promising* to give you an item is giving you an assurance — that assurance is the promise. The actual delivery may succeed (resolved) or fail (rejected).

### `await` and `async`

To make a step wait for the previous step's promise to settle, prefix it with **`await`**:

```typescript
await page.goto('...');
await expect(page).toHaveTitle('My Shop');
```

If the awaited promise resolves, the next step continues. If it gets rejected, Playwright waits up to 30 seconds, throws an error, and skips the remaining steps.

`await` is **only** needed for statements that return a promise. `console.log` returns nothing — no promise, no `await` required. A pure variable assignment like `let title = ...` doesn't need `await` itself, but the right-hand side `page.title()` does:

```typescript
let title: string = await page.title();
console.log(title);   // no await needed
```

The second rule: any function that uses `await` inside it **must be marked `async`**. There is a strong relationship between `async` and `await` — one without the other doesn't work. So the arrow function passed to `test` is declared as:

```typescript
async ({ page }) => { ... }
```

### What happens if you forget `await`?

The instructor demonstrates this. Without `await` on `page.title()`, TypeScript itself complains: *"Type 'Promise<string>' is not assignable to type 'string'."* If you bypass the type by inlining the call into a `console.log`, the output prints `Promise { <pending> }` because the assertion below it (which does have `await`) finishes first while the title promise is still in flight. Adding `await` fixes it — the actual title prints.

### One assertion per test

Best practice is **one assertion per test function**. If you put multiple assertions and the first fails, the remaining ones are skipped (a *hard assertion*). For multiple validations, either split into multiple tests or use **soft assertions** (covered in a later session). Splitting is preferred.

## Running tests

### Default run — all tests, all browsers, headless

```
npx playwright test
```

This runs **every** spec file in the `tests/` folder. The output reports something like *"Running 9 tests using 8 workers"*. Two key concepts:

- **Headless mode** is the default — no UI is shown. Tests execute entirely in the background.
- A **worker** is one browser instance. With three configured browsers, every single test counts as three runs (one per browser). So one test file with one test produces three executions.

After deleting the sample folders to leave just one test, the output becomes the much clearer *"Running 3 tests using 3 workers"*.

### Headed mode — see the browsers

```
npx playwright test --headed
```

All three browser windows open in parallel and run the test visibly. Execution is fast.

### The HTML report

Playwright always produces an HTML report (and a JSON last-run result under `test-results/`). To open the HTML report in your browser:

```
npx playwright show-report
```

It runs on a local server, lists every test grouped by browser project (chromium / firefox / webkit), shows total time, expanded steps, and pass/fail counts (passed, failed, flaky, skipped).

### Running a specific test file

```
npx playwright test mytest.spec.ts
```

Pass multiple files with spaces:

```
npx playwright test mytest.spec.ts mytest2.spec.ts
```

### Running on a specific browser

Use `--project` to override the configured browsers at runtime:

```
npx playwright test mytest.spec.ts --project=chromium
```

The test runs only on Chromium, regardless of how many projects are in `playwright.config.ts`.

### Filtering by test title with `-g`

`-g` (global) matches tests whose **title** contains the keyword:

```
npx playwright test -g verify
```

If both `mytest.spec.ts` (titled *verify page title*) and `mytest2.spec.ts` (titled *verify page URL*) contain "verify", both run. Switching to `-g title` only runs the first test, since "title" only appears in that one. It's a contains-style match, not a regex.

### UI mode

```
npx playwright test --ui
```

Opens Playwright's UI window listing every spec and test. Click an arrow to run an individual test. The UI captures rich information per run — source view, call logs, errors, console, network — and supports **time travel** so you can step backward and forward through the recorded actions and see exactly how the test interacted with each element. (A dedicated session covers UI mode in more depth.) Internally, UI mode still runs in headless mode.

### Debug mode

```
npx playwright test mytest.spec.ts --debug
```

Opens an inspector window plus the browser, paused before execution. Each click of "step over" advances one statement so you can watch the URL load, the assertion run, and so on — repeated for each browser project. Useful for stepping through failures.

### Other run modes from the docs

Playwright's "Running and Debugging tests" docs section also covers running only previously failed tests and other variations. The instructor recommends practicing all of these: UI mode, debug mode, show report, headed/headless, single test, multiple tests, specific browser.

## A second test: verifying the URL

To demonstrate multiple files, the instructor copies the first spec into `mytest2.spec.ts` and changes the assertion. Instead of capturing the title, capture and validate the URL:

```typescript
const url = page.url();
console.log(url);
await expect(page).toHaveURL('https://...');
```

If you only care that *part* of the URL is present, use a regular expression. Wrapping a substring in slashes makes it a regex, so `/automation-practice/` matches any URL containing that fragment — anything before or after is ignored. The assertion passes as long as the substring is present.

## Playwright architecture vs Selenium

Every automation tool has an architecture — how it actually communicates with the browser. The Playwright docs include a clear comparison.

### Selenium

Selenium has **language bindings** for many languages (Java, Python, etc.). Your script's method calls travel over the **W3C protocol** to **browser drivers** — every browser has its own driver — which then talk to the actual browser via **HTTP calls**.

HTTP is request/response and **stateless**. For every method call, Selenium opens a connection, sends the request, gets the response, and closes the connection. Then for the next method (`get`, `getTitle`, etc.), it opens a new connection, runs the command, and closes it again. All that connection overhead, repeated per method, is what makes Selenium slower.

### Playwright

Playwright uses **WebSocket** instead. With WebSocket, the connection is opened **once** at the start of a test, all method calls flow over that single persistent connection, and the connection closes only after the test finishes. There are also **no browser-specific drivers** — Playwright talks to browsers directly.

The result: significantly faster execution because the per-method open/close cost disappears.

### Interview soundbite

> Selenium architecture uses the W3C protocol with HTTP request/response. Playwright architecture uses the WebSocket protocol, has no separate browser drivers, and Playwright itself talks directly to browsers — which is why it's faster.

## Wrap-up and homework

This was an introductory session — environment setup, a simple test, and the most-used run commands. The instructor will distribute a document covering async/await, why it's required, where it goes, and the full command list.

Practice tasks before the next session:

- Install Playwright fresh.
- Write and run a simple test.
- Try every command discussed: UI mode, debug mode, show report, headed mode, headless mode, single test, multiple tests, specific browser.
- Explore all the options.

Upcoming sessions will cover each topic in detail, step by step. *Have some patience and practice.*
