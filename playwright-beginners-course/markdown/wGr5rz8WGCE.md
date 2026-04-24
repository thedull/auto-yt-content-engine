# What is Playwright? (Playwright introduction tutorial, features & demo)

> **Source:** [What is Playwright? (🎭 Playwright introduction tutorial, features & demo)](https://www.youtube.com/watch?v=wGr5rz8WGCE) — [Testopic](https://www.youtube.com/@Testopic) · 2021-06-02 · 12:18
> *Transcript generated via `youtube-captions (en)`.*

## TL;DR

- **Playwright** is a free, open-source **Node.js** library for browser automation, backed by Microsoft and built by ex-Puppeteer engineers.
- It supports three browser engines (covering Chrome, Edge, Safari, Firefox, Opera) and four/five languages: TypeScript/JavaScript, Java, Python (sync and async), and C#.
- Installation is just three pieces: **Node.js**, **Visual Studio Code**, and `npm i -D playwright`.
- The built-in **codegen** inspector records your browser actions and outputs runnable scripts in any supported language — no coding required.
- Every Playwright script follows the same structure: **Browser → Context → Page** (analogous to a real browser, a window, and a tab).
- Playwright can take screenshots, record videos of test runs, and runs **headless by default** (toggle with `headless: false`).

## What Playwright is

Hello clever people! I hope you're having an amazing day. I'm Victor, and in the next 15 minutes I'll help you get started with a cool new automation tool called **Playwright**. By the end of this video you'll know what Playwright is, how to install it and its dependencies, how to generate automation scripts without writing a single line of code, how to interact with elements on the screen, and how to take screenshots or record the whole thing as a video.

We'll be seeing some code, but I'll take you through it step by step. And it's going to be mostly auto-generated, so don't worry if you don't speak code.

So, let's get it on! First, allow me to attempt the shortest Playwright introduction ever:

Playwright is essentially a **Node.js library** made for browser automation. It's free, open-source, and it's backed up by **Microsoft**.

Some of the team members used to work for Google on a different automation tool called **Puppeteer**. In the meantime, they moved to Microsoft and became the Playwright team — so they have plenty of experience.

They are incredibly responsive with resolving bugs and answering questions. They have a usual triage time of less than 48 hours and have already addressed more than **1600 issues**.

A small disclaimer: this video is not sponsored and I don't have any affiliation with the team — I just really like the tool they are building.

## Browser and language support

Playwright supports **3 browser engines** that together cover all the popular browsers like Google Chrome, Microsoft Edge, Apple Safari, Opera, and Mozilla Firefox.

It can be used with the most popular languages out there, like:

- **TypeScript & JavaScript**
- **C#**
- **Java**
- **Python**

It also has some cool perks. It can:

- Automatically download the browsers it needs
- Record videos of your tests
- Intercept and modify network requests
- Emulate devices, location, locale, timezone, etc.
- Provide a built-in **Code Generator** and **Debugger** (which I'll show you in a minute)

In a nutshell, Playwright is awesome.

## Installing Playwright

Let's get on with installing it. It's a fairly easy process. We only need 3 things: **Node.js**, **Playwright**, and a **code editor**. As an operating system, I'll be using Windows. You'll be fine with Linux or macOS, as Playwright is compatible with those as well.

**1. Install Node.js.** Go to nodejs.org and click the **LTS** version. We'll just do a next-next-next install with most of the default setup. It's a quick installation.

**2. Install Visual Studio Code.** By going to code.visualstudio.com we can start the installation for **Visual Studio Code**. It's going to be another next-next-next installation.

**3. Create a project folder.** Once Visual Studio Code is installed, we'll need a new folder. Visual Studio basically works with folders as projects, so just create a new folder for this project. It's going to be `playwright-test`. Once we have this, we can open it up from VS Code: **File > Open Folder > Select Folder**.

**4. Install Playwright.** Now, all there is to do is install Playwright, which we can easily do by starting a console: **Terminal > New Terminal**. Write:

```
npm i -D playwright
```

`-D` stands for Dev. It's going to take a minute or so.

That was it with the installation process. Let me know in the comments below if you ever used a code editor or an IDE before, and if so, which one do you prefer. Let's continue with creating a simple automation script.

## Generating a script with codegen

Let's create a new file. Right-click → New File. We'll call it `hello-playwright.js`.

I promised you we won't be writing any code, so this is the perfect moment to start **Playwright's inspector**. We can do that by writing:

```
npx playwright codegen
```

We can launch this directly, or we can give it a website — let's say `http://wikipedia.org`.

It's going to start a browser window and the actual inspector. We can see the browser window on one side and the inspector on the other. This is already recording, so each time we do an action in the browser window, we will see a new line of code in the inspector.

So let's say we want to automate wikipedia.org. Let's go to **English → Final Fantasy IX → Combat and character progression**.

Let's take a look at the generated script on the right side. It has generated **JavaScript code** because JavaScript is selected by default, but we can select any of the 4 languages it supports (actually 5): **JavaScript, Java, Python, async Python, and C#**. The structure is going to be the same for any language.

If we look at the code for just a bit, it first starts a browser, it then starts the context, then starts a page, and then it navigates to the Wikipedia website, it then clicks on the English language link, and so on. If we change this to **Java**, even after we recorded everything, then we will see the same structure again — it first starts the browser, then starts the context, then starts a new page.

Any Playwright script that starts from scratch is going to start the same: **Browser → Context → Page**. We'll go through these in just a minute.

So let's go to JavaScript, copy everything, and go to our code editor. Paste everything here. Amazing — you can already run this.

## Browser, Context, Page explained

But before that, let's take a minute and understand what happens in detail.

As I mentioned, the first thing it does is start the **browser**. The browser in Playwright is similar to a real-life browser, so think about this as starting a new browser window.

It then goes on to start a new **context**. It's kind of like starting a new window inside an existing browser. We already have this browser, and we use it to launch a new completely independent window. If you start 5 contexts, for example, they are going to be completely independent of each other.

And then, we have a new **page** — a tab.

So: **browser ... window ... tab**. Just like in real life.

Then you are going to find some familiar actions. We opened up Wikipedia, we clicked the English Language articles, then we went to the Final Fantasy IX article, and we clicked on the Combat and character progression link.

Let's see what we have here by running it. We'll run it using this simple command:

```
node hello-playwright.js
```

We see the browser running, clicking ... and that's it. I hope you caught it.

## Taking screenshots

Let's modify it a bit. Let's see what it can do for us. For example, we can easily take a screenshot:

```js
page.screenshot({ path: 'wiki_screen.png' })
```

We just have to give it a path to the screenshot. Let's call this one `wiki_screen.png`. And let's run it again using the same command.

Let's see what happened. We'll just go to our File Explorer, and we see the new screenshot here. We'll see exactly what we expect — it actually navigated to the anchor that we clicked last.

## Recording videos

Another cool thing that Playwright can do is **record videos** of the whole execution. For this, we just need to change the properties of the **context**. If we go to the context, we create a new object and we say `recordVideo`. We just have to give it a path through the `dir` property, so let's say `videos`.

```js
const context = await browser.newContext({
  recordVideo: { dir: 'videos' }
});
```

Save and run it again. At the end, we should see ... yes, we have a new `videos` folder, and it has a file in it. Let me open it in Explorer.

If we go to Videos, we see this video. Let's run it, and, as expected, everything that Playwright does is actually recorded.

## Headless mode

Before we finish off, I want to show you just one more thing. **Playwright is headless by default.** This means that the browser runs, but you can't see it.

In our case, because we took the code from the Inspector — which generates the code automatically — they actually added this automatically for us:

```js
headless: false
```

This means that the browser won't actually run headlessly. But if we flip it back on — let's say I delete this `videos` folder so that we know it actually runs — and run it again, you can see it created Videos again... and it finished. I just wanted to show you how a headless run looks like ... You don't see anything :)

## Wrap-up

That's it. Let me know in the comments below if you plan on using Playwright in the future, and for what kind of project.

I maintain a small newsletter about Playwright, so make sure to head over to **testopic.com/playwright** if you want to be updated when I post a new video, cheatsheets, or other interesting stuff about this amazing tool.

Cheers, and have a good one!
