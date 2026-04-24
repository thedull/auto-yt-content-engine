# Get Started with Playwright and VS Code (2025 edition)

> **Source:** [Get Started with Playwright and VS Code (2025 edition)](https://www.youtube.com/watch?v=WvsLGZnHmzw) — [Playwright](https://www.youtube.com/@Playwrightdev) · 2025-08-04 · 19:45
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- Walks through installing the **Playwright VS Code extension** by Microsoft and bootstrapping a project (browsers, TypeScript, optional GitHub Actions workflow).
- Tours the generated project: `tests/` folder, `playwright.config.ts`, the demo to-do app spec, and the HTML report / trace-on-first-retry defaults.
- Demonstrates running tests from the testing sidebar, toggling **Show Browser** vs headless mode, and using **Show Trace Viewer** for full action / DOM / network debugging.
- Shows the **pick locator** workflow, multi-browser projects (Chromium, Firefox, WebKit, mobile viewports), and closing browsers from the sidebar.
- Covers the **Fix with AI** sparkly icon for failing tests, **Record New** for `codegen`, and **Record at Cursor** for inserting steps mid-test.

## Installing the extension and initializing a project

Let's get started with **Playwright** using the **VS Code extension**. Open the Extensions panel and search for Playwright — make sure you choose the one by **Microsoft** — then install it. Once installed, you'll see there are no files yet; you've just got an extension, so now you need to use it to install Playwright itself.

Open the command palette and run **Install Playwright** (or just select it from the list). The installer asks which browsers you want: **Chromium**, **Firefox**, **WebKit** — you can pick all of them, or maybe only Chromium. It's up to you. We highly recommend **TypeScript**, but you can select **Use JavaScript** if you prefer. There's also an **Add GitHub Actions workflow** option, which is really cool because it adds a workflow for GitHub; if you're not using that, feel free to uncheck it.

Select the defaults and press OK. The browsers install and your project files are created for you.

## What's in the generated project

Let's take a quick look at what we have:

- A **`.github/`** folder with a **`playwright.yml`** workflow called *playwright tests*. On push or pull request of your branches, it runs your tests straight out of the box. Very easy setup — you just select that button and bang, it's done.
- A **`node_modules/`** folder containing `playwright`, `playwright-core`, etc.
- A **`tests/`** folder with an **`example.spec.ts`** — an example test you can play around with — plus a bigger demo to-do app test you can dive deep into.
- **`package-lock.json`** and **`package.json`** with `@playwright/test` and types for node.
- **`playwright.config.ts`** — your config, where everything is configurable.

In the config, the test directory is called `tests` (you could change that if you already had a test directory). **Fully parallel** is true, so it runs tests and files in parallel. Build and CI **retries**, **workers**, etc. can all be changed. The **HTML report** is included by default, so you get a nice report when your tests are passing or failing. **Trace** is set to *on first retry* — a trace viewer is created on the first retry, but you could change that to *always on* if you wanted.

Then you've got your **projects**. We installed Chromium, Firefox, and WebKit; in the config these are called *projects* because they're not just browsers — you could have setup projects, or **mobile viewports** (uncomment that block to test your application on mobile). Down below, you can uncomment the **web server** option to spin up a local `localhost:3000` as you run your tests.

## Running tests and toggling the browser

Now let's see Playwright in action. With the extension installed, you get a nice **Testing** toolbar. Click it and you'll see the example test. Run it from there or from the actual sidebar — you've got a **Test Results** section showing the tests have passed.

A separate browser window pops up with the actual test running. Why? Because down here you have **Show Browser** checked. If you uncheck **Show Browser** and run the test, the browser is gone — it runs in **headless mode**, just like you would on a CI environment. You have no UI; you can't see what's happening, but you can check the results in the test results section. Maybe that's a flow you want, because you don't need to see the browser open. But if you do, just click **Show Browser** and it will pop up.

## Speed and the Trace Viewer

Playwright is very, very fast. Drag and drop the **demo to-do app** into the test folder so we have another test. Run the first test — it opens the to-do app, does its thing, and that was really quick. Run it again — super fast.

As you play around with this, you might decide this browser plays things too fast and you can't keep track. You have another option: **Show Trace Viewer**. Click that instead, then run the test — now you have a full **trace**.

Over here you have **Actions**: *buy some cheese*, the `fill` on `getByPlaceholder`, then when you press Enter, *buy some cheese* is filled in. You've got the **action before / after**, so you can see how the page state changed versus what you're expecting, with the actual source code shown as you go along.

Other things you have:

- **Locator** picker — you can pick a locator and see, for example, a `getByTestId`. You can choose a different one by clicking around.
- **Aria snapshot** — if you're doing snapshot testing, the aria snapshot is here too. Copy it into your code and modify your test.
- **Call** — what you're expecting (e.g. to be empty), the time, parameters, return value.
- **Log** — what happened, plus errors if any (we had none because we were perfect tests).
- **Console** — console logs from your test or from the browser.
- **Network** — filter, change, look at different things, type in here, look at base CSS, see what's going on at each point. Select a specific area in time and scroll along, see when network requests come in. Focus on different points and see how the actions list changes.
- **Source** — the source code.
- **Attachments** — shown here if you have any.

You can also click a button to pop the page out into an actual **DOM snapshot** where you can inspect it, remove the box shadow, change styles (let's do red, for example), really play with things — this is you testing and debugging. You've also got settings; you could put it in **dark mode** or **display canvas content** if you needed.

## Projects and multi-browser runs

Remember our browsers are called **projects** in the config — Chromium, Firefox, and WebKit. If we uncomment a mobile project, we get another option in projects: **Mobile Chrome**. You can rename it to whatever you want — *mobile everything*, just to see the change reflected.

Then you can run the tests across all of them. Click **Show Browser**, run the simple example test, and you'll see those browsers pop up: Firefox appears on the other window, WebKit appears, the mobile one appears. A nice way of testing across the different browsers very quickly.

You can close all those browsers by clicking the **Close All Browsers** button in the sidebar.

## Reveal test output and the locator picker

**Reveal test** brings up the test results area in full screen. You can run tests from here too — to run only on Firefox, you can do it from the sidebar or here. If you close the output and then realize you want to see what's going on, just click **Reveal test output**. You can go back through other results and see what was going on at each point.

There's a little **Playwright** section here — that's the **locator picker**. We talked about it in the trace viewer, but you can also pick the locator from here.

Let's run a test to do it. Uncheck the other projects so just **Chromium** is working, and click on the demo to-do app — let's take the *editing* one. Click **Pick Locator**, and as you hover, it highlights all the locators: *getByText*, *getByText*, *getByRole heading name "todos"*, *getByText "Mark all as complete"*. Maybe that's the one you wanted. You can copy it, or select **Copy on Pick**. Maybe you want this locator, or maybe the aria one, depending on what you want to do in your test.

## Fix with AI when a test breaks

This is really great for debugging. Let's modify one of our tests so it fails. You'll see a **sparkly icon** here that you can click — it'll go ahead and fix the error for you.

> "This issue is in the *could should save edits on blur* test. It expects *buy some sausages* but actually gets *buy some cheese* twice. The problem is the test is setting a new text but checking for incorrect values."

AI might change things in the way you want, or the way you don't — because it's decided that if I want cheese, it's going to put cheese everywhere. Obviously it's not going to bring the sausages back. But it's a really good way, because my test is now going to pass and that's what I care about.

The sparkly icon won't appear unless you break a test. Look for the button and it's not there — until I go back and say *ice cream*. Let's *buy some ice cream*. Run the test, it fails, and the **Fix with AI** icon appears. Click it and it fixes the test.

You're in VS Code, so you can choose the model — for example **GPT-4.1** if you want. Make sure you're choosing models that are included. You can stop, change, cancel, etc. Accept the changes (I definitely prefer ice cream to cheese) and the test will now pass.

## Recording new tests with codegen

We might want to change things, improve things, and create new tests. We can do that by clicking **Record New**. That opens up a file called **`test-1.spec.ts`** — it's already done the import, created the test name, and is ready to record. You'll see *Playwright codegen is recording*.

The only thing is I don't have anything set up here, so I have to put in the URL each time. I don't have my demo to-do app open, so let me copy that URL. The first thing it generates is `await page.goto(URL)`.

Now let's say *buy some ice cream*, and *buy some chocolate* as well. You can see it's generated the textbox, *fill "buy some ice cream"*, *Enter*, *buy some chocolate*. Click on what we've selected — we've already bought some ice cream — and we can do **assertions**: assert *buy some chocolate is visible*, assert this is visible, delete something, make sure *buy some chocolate is visible*. We could also do other assertions. There's also the **aria snapshot** option.

We've got this great test that's just been written, with `toMatchAriaSnapshot` as well. Let's run that test and see if it passed. The browser window opens and it's really, really fast.

> "Are you ready? Watch this everyone. So super fast. Right. That's the beauty of Playwright. It's just too fast."

We can run the test using the **trace viewer** and go through all our actions — there's our ice cream, our enter — make this smaller to give more space, filter through, or scrub the timeline.

## Record at Cursor

Another thing I can do is **Record at Cursor**. Make sure your browser is open instead of the trace viewer, then put the cursor where you want and run the test first — that brings the test up. Close it, then **Record at Cursor**: the cursor is here, and I want to go here. Click on *Active*, click on *Completed*, assert that's there. This adds new actions into that part of the test. Then run the test and follow along as it does what it does.

This will all fail because I created steps in the middle of the test, but I could use AI to fix it and improve my tests as I go along.

## Wrapping up

VS Code extension, really, really cool. A really good way of getting your tests up and running and just playing around with things and seeing things in action. Have fun with the VS Code extension — generate tests, write tests, edit tests, play with tests, pick locators. It's all there. There's **update snapshots** for you, **run global setup on each one**, etc. Check that out: VS Code extension for Playwright. Thanks everyone — see you in the next video.
