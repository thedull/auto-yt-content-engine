# Playwright Automation Tutorial for Beginners from Scratch

> **Source:** [Playwright Automation Tutorial for Beginners from Scratch](https://www.youtube.com/watch?v=pq20Gd4LXeI) — [Mukesh otwani](https://www.youtube.com/@Mukeshotwani) · 2024-09-02 · 8:17:30
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A consolidated 8+ hour beginner course on **Playwright with JavaScript**, combining Mukesh Otwani's individual lectures into a single video covering everything from environment setup to **Jenkins** + **GitHub** integration.
- Walks through installing **Node.js** and **VS Code** on Windows and Mac, installing Playwright (`npm init playwright@latest`), exploring the generated project (`playwright.config.js`, `tests/`), and running the first sample test in headless and headed modes across **Chromium**, **Firefox**, and **WebKit**.
- Teaches the test-writing fundamentals (`test`, `expect`, `test.only`, `test.skip`, `async/await`, fixtures), interacting with web elements via the new built-in locators (`getByPlaceholder`, `getByRole`, `getByText`, `page.locator`), and verifying error messages, titles, and URLs.
- Covers practical scenarios: viewport/maximize, screenshots/videos/traces via config, **Codegen** (test recorder), the **Playwright VS Code extension**, retries and flaky tests, dropdowns (single + multi-select), CLI options, hover, file upload (`setInputFiles`), keyboard actions (single keys + chords + arrow keys with shift hold), auto-suggestions/autocomplete, JavaScript alerts/confirms/prompts (via `page.on('dialog', ...)`), iframes (`frameLocator`), multiple tabs/windows (`browser.newContext` + `Promise.all` + `waitForEvent('page')`), and `waitForLoadState('networkidle')`.
- Builds toward an automation framework: **data-driven testing** from JSON files (`require`, `JSON.stringify`/`parse`, `test.describe` loop with template-literal IDs), generating **Allure reports** alongside the HTML report, and implementing the **Page Object Model** (login + home page classes with constructors, locators, and async methods).
- Closes with CI/CD: pushing the project to **GitHub** via both HTTPS (with personal access tokens) and SSH (with public/private key pairs), then running the suite in **Jenkins** — first against a locally-cloned workspace, then via the Git SCM plugin, finally parameterizing the spec file and browser as choice parameters.

## Course intro and how to use this 8-hour video

If you are planning to learn Playwright with JavaScript and don't know where to start, what to cover, or when to end, this video compiles all the essential lectures from the channel into one place. Mukesh has stitched together a dedicated series so you can go from "how to download and install" all the way to "integration with Jenkins and GitHub" in a single playlist-style video.

The video is long (over 8 hours), so use the chapter timestamps in the YouTube description to navigate. Skip ahead if you already have Node.js and VS Code installed; jump back if you need the OS-specific install steps for Windows or Mac.

**The most important advice**: do not try to watch this in one sitting. Decide how many chapters to watch each day (one, two, or three), and **practice immediately** after each chapter before moving on. If you only watch and never practice, you will not retain anything and you will not have the confidence to use Playwright on a real project. The moment you start practicing you will hit doubts — leave them in the comments and they will be addressed.

## What is Playwright and why it is getting popular

Playwright is an automation framework that helps you automate web applications. The official site is **playwright.dev**. It launched two years ago but has picked up a lot of growth because of the breadth of features it offers out of the box. It is not the only web automation tool in the market, but it offers more than most of its competitors.

Key features:

- **Multi-language**: Node.js / JavaScript, Python, Java, .NET. Outside of Selenium, very few other tools support this many languages — Cypress, for example, is JavaScript only.
- **Free and open source.** No cost to get started.
- **All major browsers**: all Chromium-based browsers (Chrome, Edge, Brave, etc.), Firefox, and WebKit (the Safari engine).
- **Cross-platform and cross-language**: Windows, Mac, Linux, locally and on CI, headed or headless.
- **Mobile emulation** of Chrome for Android and Mobile Safari (this is emulation, not native app testing).
- **No flaky tests** thanks to **auto-wait**: Playwright waits until each element is in an "actionable state" (attached, visible, stable, and able to receive events) before acting. You configure the timeout, but you don't need to sprinkle manual `sleep` calls.
- **Web-first assertions** that retry until the timeout expires; built-in assertions for URLs, pages, and elements, plus the ability to write your own.
- **Tracing**: capture screenshots, videos, and full traces of a test run.
- **No limits compared to Cypress**: multiple tabs and windows are supported, frames can be switched into with one line, Shadow DOM is auto-pierced, and there is no need for plugins.
- **Faster execution** because each test runs in its own isolated **browser context**.
- **"Login once"**: save authentication state to a context and reuse it across tests so you don't have to log in for every single one of your 100 test cases.
- **Powerful tooling**: Codegen (record and export to any supported language), Playwright Inspector, Trace Viewer.

The only prerequisite before starting is basic JavaScript: you need to understand `async/await`, `import`/`require`, variables, and basic data types. Mukesh has a separate JavaScript playlist for that. The official Playwright docs are good (Getting Started, Test, Guides, Migration, API reference for Test/Library/classes) and the GitHub repo is open for issues, contributions, and feature requests; there is also a Slack channel, a Stack Overflow tag, an official YouTube channel, and an Ambassadors program. **Learning to read the documentation is the single skill that lets you learn any tool from the internet.**

## Installing Node.js on Windows

First check whether Node.js is already installed by opening **CMD** and running `node -v`. If you see "node is not recognized as an internal or external command," you need to install it.

Search for "download nodejs" — the official site is **nodejs.org**. Node.js is **just a JavaScript runtime built on Chrome's V8 engine**; do not confuse Node.js with JavaScript itself.

Pick the **LTS version** (at the time of recording, 14.17.3; current was 16.5.0). The Windows installer is an MSI; Mac has PKG; Linux has tar.gz; there are Docker images too. Download the MSI, double-click, accept the agreement, leave the install path as `C:\Program Files\nodejs\`, leave the default features selected, and click Install.

After installing, open CMD again and verify both:

```bat
node -v
npm -v
```

`npm` stands for **node package manager** and you will use it many times. Run `npm --help` to see the commands; `npm help test` (and similar) opens the docs for a specific command.

If `node -v` fails after install, the PATH was not set automatically. Go to **My Computer → Properties → Advanced system settings → Environment Variables**, find the system `Path` variable, edit it, and confirm `C:\Program Files\nodejs\` is in the list. If not, add it manually and restart the system.

To run your first JavaScript file: create `hello.js` containing `console.log("hello world");`, open CMD, navigate to the folder (or right-click in the folder and "open command prompt here"), and run `node hello.js`.

## Installing VS Code on Windows

Search "download vs code" — the official site is **code.visualstudio.com**. Download the 64-bit System Installer for Windows 10, accept the agreement, accept the default install location (~300 MB required), and finish.

When VS Code opens, the left sidebar gives you Explorer, Search, Source Control, Run/Debug, and Extensions. The bottom-left gear is Settings. The Explorer tab needs a folder to be opened — use **Open Folder** and pick a folder you'll use for your work (e.g. the `JavaScript_examples` folder created in the previous lesson). Trust the author when prompted.

Create a new file `myFirstJsCode.js`, type `console.log` and notice the autosuggestions for `log`, `error`, `warn`, `info`, `assert`, `clear`, `count`, etc. Open a new integrated terminal and run `node myFirstJsCode.js`. The shortcut `log` + Tab autocompletes to `console.log()`, and the same trick works for `error`, `warn`, etc. In a browser console, `console.log`, `console.warn`, and `console.error` render with different styling; in the Node terminal you mostly see plain text.

## Installing Node.js on Mac

The Mac install is the same idea. Open Terminal and check `node --version`; if you get "command not found," go to nodejs.org → Download. Pre-built installer for macOS is the easiest path; pick the LTS (e.g. 14.x or 20.17.0), choose ARM64 if you are on M1/M2/M3, otherwise x64.

Save the PKG to Downloads, double-click, click Continue → Continue → Agree, confirm the destination (~257 MB needed), enter your system password, and click Install Software.

Note the install location: `/usr/local/bin/node` and `/usr/local/bin/npm`. The installer asks you to ensure `/usr/local/bin` is in your PATH (it normally is). Verify with `node --version` and `npm --version`.

## Installing VS Code on Mac

Search "visual studio code", go to **code.visualstudio.com**, and download the macOS build. The download is a zip file; double-click to unzip and you'll get the `Visual Studio Code.app` (it may be named `Visual Studio Code 2.app` if you already have a previous install). The first launch shows the release notes for the current build. The UI is the same as on Windows.

## Installing Playwright and exploring the folder structure

Confirm Node.js is installed (`node -v`) — anything above 14 works. Create a folder on the desktop, e.g. `playright_youtube`, and open it in VS Code via Open Folder. Open the integrated terminal (or system terminal/CMD) and confirm with `pwd` you are inside that folder.

Run the install command from the official Getting Started guide:

```bash
npm init playwright@latest
```

The `@latest` keeps you on the newest release; you can pin to `@1.27.1` (or any version) if you ever need to downgrade. The installer asks four questions:

1. **TypeScript or JavaScript?** Default is TypeScript; choose JavaScript for this series.
2. **Where to put your end-to-end tests?** Default `tests` folder — accept it.
3. **Add a GitHub Actions workflow?** Default `false` — say no for now (covered later).
4. **Install Playwright browsers?** Default `true` — say yes (this is what `npx playwright install` does manually later).

What you get:

- `package.json` — the heart of your dependency list. This is where you upgrade/downgrade Playwright and add other packages.
- `playwright.config.js` — the heart of your project configuration. Test directory, timeouts, parallel mode, reporter, projects/browsers, retries, mobile viewports, etc.
- `tests/example.spec.js` — a sample test that loads playwright.dev, asserts the title, clicks a link, and asserts a URL.
- `tests-examples/demo-todo-app.spec.js` — a longer end-to-end demo.
- `node_modules/` containing `@playwright/test` and `playwright-core`.

In `playwright.config.js`, the most important section to notice on day one is **projects**, which lists three browsers — Chromium (desktop Chrome), Firefox, and WebKit (desktop Safari). Every test runs in all three in parallel by default. Below that you can also enable mobile viewport projects.

To run the suite:

```bash
npx playwright test
```

This picks up every `*.spec.js` file under the `tests` directory and runs it in three browsers, in parallel, in headless mode. Three tests in three browsers = nine results.

To see the HTML report afterwards:

```bash
npx playwright show-report
```

The report is self-explanatory: pass/fail per browser, before/after hooks, individual steps, and timing. To watch the test run visibly, add `--headed`:

```bash
npx playwright test --headed
```

The default reporter is `html`. Other built-in reporters include `list`, `line`, `dot`, `json`, `junit`, GitHub Actions annotations, and several third-party reporters.

## Writing your first script

Delete the sample tests so you can build everything from scratch (delete `tests/example.spec.js` and the `tests-examples/` folder if you want a clean slate). Create `tests/sample.spec.js`.

You import what you need with `require` (a built-in Node function for including modules):

```javascript
const { test, expect } = require('@playwright/test');
```

`test` is the function that declares a test; `expect` is the function that writes assertions.

```javascript
test('my first test', async ({ page }) => {
  // page is an isolated page instance, created per test
});
```

You can declare additional tests in the same file. To run, `npx playwright test` picks up everything; in headed mode you'll see browsers spawn for each test/browser combination.

`expect` for non-page assertions:

```javascript
expect(12).toBe(12);          // pass
expect(100).toBe(101);        // fail
expect(2.0).toBe(2.0);        // pass
```

Run only one test in a file with `test.only(...)`. Skip a test with `test.skip(...)`. Other useful matchers shown: `toContain`, `toBeTruthy`, `toBeFalsy` (e.g. `expect("mukesh").toContain("mukesh")`, `expect("mukesh otwani".includes("ot")).toBeTruthy()`).

Then create `tests/google.spec.js` to do something real:

```javascript
const { test, expect } = require('@playwright/test');

test('verify application title', async ({ page }) => {
  await page.goto('https://google.com');
  const url = page.url();
  console.log('URL is ' + url);
  const title = await page.title();
  console.log('Title is ' + title);
  await expect(page).toHaveTitle('Google');
});
```

Notes from this section:

- Every Playwright method needs `await`. Without `async` on the function and `await` on each call, you get `unexpected reserved word await` and `name not resolved` errors.
- `page.goto` requires a protocol; `page.goto('www.google.com')` fails with `cannot navigate to invalid URL`.
- `expect(page).toHaveTitle(...)` is the page-level assertion; passing the wrong expected value retries up to the configured `expect` timeout (default 5,000 ms in `playwright.config.js`) before failing — which is the auto-wait at work.
- `console.log` output appears as **standard out** attached to the step in the HTML report.

## Interacting with web elements (login form)

Create `tests/login.spec.js` and target the OrangeHRM demo (`opensource-demo.orangehrmlive.com`). Credentials: `Admin` / `admin123`.

Strategies for locating elements:

- **Built-in locators (preferred when applicable)**: `page.getByPlaceholder('Username')`, `page.getByRole('button', { name: 'Login' })`, `page.getByLabel(...)`, `page.getByText(...)`, `page.getByAltText(...)`, `page.getByTitle(...)`, `page.getByTestId(...)`.
- **Traditional locators via `page.locator(...)`**: pass a CSS selector (`'input[name="password"]'`) or an XPath (`'//button[@type="submit"]'`). Playwright auto-detects XPath when the string starts with `//`.
- For complex selectors the **SelectorsHub** Chrome extension generates CSS, XPath, indexed XPath, and jQuery selectors and validates them in-page.

A complete login script looks like:

```javascript
await page.goto('https://opensource-demo.orangehrmlive.com/');
await page.getByPlaceholder('Username').type('Admin', { delay: 100 });
await page.locator('input[name="password"]').type('admin123', { delay: 200 });
await page.locator('//button[@type="submit"]').click();
await expect(page).toHaveURL(/dashboard/);
```

Run only this file in headed mode:

```bash
npx playwright test ./tests/login.spec.js --headed
```

Lessons learned in this lecture:

- The OrangeHRM demo occasionally renders in a non-English language; if your selector targets English text, the test will fail until the page comes back in English.
- A wrong password fails the `toHaveURL(/dashboard/)` assertion — every failure teaches you something.
- `await page.waitForTimeout(5000)` adds a hard wait; the docs themselves say "not recommended, only for debugging."
- For logout on this page, `page.getByAltText('profile picture')` matches **two** elements, triggering a **strict mode violation** in Playwright. Either tighten the selector to a unique element or use `.first()` / `.last()` / `.nth(...)` (covered later).
- The `delay` option on `type` slows the typing to mimic a human (`{ delay: 200 }` = 200 ms per character).

## Verifying error messages

Take any application with an inline error message (here, OrangeHRM with bad credentials shows "Invalid credentials"). Capture the message via:

```javascript
const errorMessage = await page.locator('//p[contains(@class,"alert-content-text")]').textContent();
```

`textContent()` returns a string for one element; `allTextContents()` returns an array of strings for multiple elements (useful for headers, lists, etc.).

Two assertion styles:

```javascript
// Partial match
expect(errorMessage.includes('Invalid')).toBeTruthy();

// Exact match
expect(errorMessage === 'Invalid credentials').toBeTruthy();
```

Drop one character ("Invalid credential" instead of "Invalid credentials") and the strict equality assertion fails — the report opens automatically on failure (this is the default; it can be customized to always or never open).

## Maximizing the screen / changing the viewport

Playwright has **no `maximize()` method** — there is no `fullScreen` or `maximize` on `page`. Instead, use **viewport**.

Read the current viewport with `page.viewportSize()` (returns `{ width, height }`). Default is `1280 x 720`. The site `whatismyviewport.com` shows the real browser size of your monitor (e.g. `1920 x 1080`).

Two ways to change it:

1. **Project-wide** in `playwright.config.js`:
   ```javascript
   use: {
     viewport: { width: 1920, height: 1080 },
   }
   ```
2. **Per spec file or per test**:
   ```javascript
   test.use({
     viewport: { width: 1500, height: 1000 },
   });
   ```

## Screenshots, videos, and trace files (no code required)

Three properties under `use:` in `playwright.config.js`:

```javascript
use: {
  screenshot: 'on',  // 'off' | 'on' | 'only-on-failure'
  video: 'on',       // also: 'on-first-retry', 'retain-on-failure', 'retry-with-video'
  trace: 'on',       // also: 'on-first-retry', 'retain-on-failure', 'retry-with-trace'
}
```

After running `npx playwright test`, the HTML report shows the captured screenshot, an embedded video, and — most importantly — the **Trace Viewer**, which gives you a full, step-by-step replay with **before/after snapshots** for every action, plus the network panel, console, and source location of each call. The trace makes failure analysis dramatically faster.

For ad-hoc captures there is also `page.screenshot({ path: 'foo.png', fullPage: true })` — works on the page or on a single element. You can return a buffer instead of writing to disk for use with custom reporters.

## Code generation (Codegen / Test Recorder)

```bash
npx playwright codegen
```

This opens a Chromium window plus the **Playwright Inspector**. Every action in the browser is recorded; the Inspector shows the generated code in your chosen target language (Test Runner JavaScript by default, plus Library JS, Java, Python (pytest), C# (NUnit), etc.). It's smart about locators — it favors `getByRole`, `getByPlaceholder`, `getByText`, etc. — and adds assertions on navigation automatically (e.g. `await expect(page).toHaveTitle(...)`).

Codegen options:

- `--target=python` (or `java`, `csharp`, `python-pytest`, etc.) controls the output language.
- `-b webkit` / `-b firefox` / `-b chromium` chooses the engine.
- `--channel=chrome` (or `chrome-beta`, `msedge`, `msedge-dev`, etc.) drives a branded browser.
- `--lang=fr-FR` sets locale.
- `-o tests/codegen.spec.js` writes the generated test directly to a file instead of clipboard-and-paste.

`npx playwright codegen --help` lists everything.

Mukesh's takeaway: Codegen is great for quickly prototyping or learning the API, but for a **robust framework** with Page Object Model, JSON fixtures, and dynamic data, you should write the code by hand for better selectors and assertions.

## Retries and flaky tests

Configure retries in `playwright.config.js`:

```javascript
retries: 2,
```

Or pass on the CLI:

```bash
npx playwright test --retries=3
```

Behavior:

- Pass first time → no retry.
- Fail first time → retry 1 → pass → marked as **flaky** in the report.
- Fail first time → retry 1 → fail → retry 2 → pass → flaky.
- All attempts fail → marked as failed.

Each retry waits up to the `expect` timeout (5,000 ms by default) per assertion. The HTML report adds Retry 1 / Retry 2 / etc. tabs and a separate "Flaky" category. Per-group retries are also possible once you start grouping tests with `test.describe`.

## Installing Playwright via the VS Code extension

There is an official **Playwright Test for VSCode** extension published by Microsoft. Install it from the Extensions panel. Once installed:

- A **Testing** tab appears in the sidebar.
- Open a fresh, empty folder, then **View → Command Palette → "Install Playwright"**, choose browsers (Chromium / Firefox / WebKit) and select "Use JavaScript". The extension creates `package.json`, `playwright.config.js`, the GitHub Actions YAML, and a sample `tests/example.spec.js`.
- In the Testing panel you can **Run** an entire spec file, a single test, or only the failing tests.
- The dropdown next to each test lets you pick the browser (Chromium, Firefox, WebKit) without editing the config.
- Debugging is built in. Inline play buttons appear next to each `test(...)` in the editor.

For local development this is the most ergonomic flow. For CI you still use the CLI.

## Handling dropdowns

Use `page.locator('#state').selectOption(...)` for `<select>` dropdowns. You can pick by:

- **Label** (visible text, recommended): `selectOption({ label: 'Goa' })`
- **Value** (the `value` attribute of the `<option>`): `selectOption({ value: 'Himachal Pradesh' })`
- **Index**: `selectOption({ index: 4 })` — note the hidden first option ("Select state") counts as index 0.

Preference order:

1. **Label** — least likely to change.
2. **Value** — can be changed by developers.
3. **Index** — most fragile (a state added/removed shifts everything).

To assert a dropdown contains a value without selecting:

```javascript
const value = await page.locator('#state').textContent();
await expect(value.includes('Kerala')).toBeTruthy();
```

Or iterate with `$$` (find all matching elements) and a manual loop:

```javascript
const elements = await page.$$('#state option');
let dropDownStatus = false;
for (let i = 0; i < elements.length; i++) {
  const value = await elements[i].textContent();
  console.log(value);
  if (value.includes('Rajasthan')) {
    dropDownStatus = true;
    break;
  }
}
await expect(dropDownStatus).toBeTruthy();
```

(Important detail: the variable must be declared **outside** the loop, otherwise the assertion runs against the first iteration's `false`.)

For multi-select (`<select multiple>`):

```javascript
await page.locator('#hobbies').selectOption(['Playing', 'Swimming']);
```

This handles dropdowns where the underlying tag is `<select>`. Non-`<select>` "fake dropdowns" (built from divs/spans) need a different approach (covered later).

## Running tests from the CLI

`npx playwright --version` shows the installed Playwright version (also visible in `package.json`).

`npx playwright test --help` documents every flag.

Common patterns:

```bash
# Run everything (all spec files, all configured browsers, headless, parallel)
npx playwright test

# Run a specific spec file (full path)
npx playwright test ./tests/sample.spec.js

# Run a specific spec file by basename only
npx playwright test sample

# Run multiple files
npx playwright test ./tests/sample.spec.js ./tests/verifyErrorMessage.spec.js

# Headed
npx playwright test --headed

# Specific project (browser)
npx playwright test --project=chromium
npx playwright test --project="Google Chrome"   # quotes needed because of the space

# Run a single test by title
npx playwright test sample --grep "my fourth test"
```

Default behavior is headless and parallel across every project listed in the config. Branded browsers (`channel: 'chrome'`, etc.) run an actual Chrome install; Chromium runs the Chromium engine bundled with Playwright. Tests run in **incognito** by default (fresh cookies/history per run).

## Hover

`page.locator(...).hover(options?)` performs a mouse hover, performing the same actionability checks as `click` (attached, visible, stable, receiving events), then scrolls if needed and moves the mouse to the element's center.

```javascript
await page.locator('//span[text()="Manage"]').hover();
await page.locator('//a[normalize-space()="Manage Courses"]').click();
```

Options on `hover`:

- `force: true` — skip the actionability checks.
- `modifiers: ['Alt', 'Control', 'Meta', 'Shift']` — hold modifier keys.
- `noWaitAfter: true` — don't wait for navigation after the hover.
- `position: { x, y }` — offset within the element (default is center).
- `timeout` — override the default action timeout.
- `trial: true` — perform actionability checks only, skip the action.

## Uploading files

Inspect the file `<input type="file">` element and call `setInputFiles` directly — **do not click the input**, which would open the OS file picker and is hard to handle.

```javascript
await page.locator('#file').setInputFiles('/Users/me/Desktop/image1.png');
await page.locator('#fileSubmit').click();
await expect(page.locator('h3')).toHaveText('File Uploaded!');
```

Make the path relative for portability — keep the upload assets inside the project (e.g. an `uploads/` folder next to the spec file) and reference them with a relative path: `../uploads/image1.png`.

For multiple files pass an array. To clear, pass an empty array `[]`. You can also upload from memory by passing an object with `name`, `mimeType`, and `buffer`.

## Keyboard actions

Two APIs:

- `page.keyboard.press('Enter')` — single key or chord (`'Meta+A'`, `'Control+C'`).
- `page.keyboard.type('hello')` — types text into the focused element.
- `page.keyboard.down('Shift')` and `page.keyboard.up('Shift')` — hold and release a key while doing other actions.

Available keys: `F1`–`F12`, `0`–`9`, `A`–`Z`, `Backquote`, `Minus`, `Equals`, `Backslash`, `Backspace`, `Tab`, `Delete`, `Escape`, `ArrowDown`, `End`, `Enter`, `Home`, `Insert`, `PageDown`, `PageUp`, `ArrowRight`, `ArrowUp`, etc., plus modifiers `Shift`, `Control`, `Alt`, `Meta` and variants like `ShiftLeft`.

For Mac use `Meta` for Cmd; for Windows/Linux use `Control`.

```javascript
// Single key
await page.locator('textarea[name="q"]').type('mukesh otwani');
await page.keyboard.press('Enter');

// Chord
await page.keyboard.press('Meta+A');     // select all on Mac
await page.keyboard.press('Backspace');  // delete selection

// Series: select all → copy → delete → paste
await page.keyboard.press('Meta+A');
await page.keyboard.press('Meta+C');
await page.keyboard.press('Backspace');
await page.keyboard.press('Meta+V');
```

To replicate the docs example — type "mukesh otwani!", then highlight just "otwani" with arrow keys + held Shift, then delete it:

```javascript
await page.locator('textarea[name="q"]').focus();
await page.keyboard.type('mukesh otwani!');
await page.keyboard.press('ArrowLeft');                  // off the trailing '!'
await page.keyboard.down('Shift');
for (let i = 0; i < 6; i++) {
  await page.keyboard.press('ArrowLeft');                // select 'otwani'
}
await page.keyboard.up('Shift');
await page.keyboard.press('Backspace');
```

## Auto-suggest / autocomplete

Two strategies for picking from a Google-style suggestion list. Both apply equally to MakeMyTrip, e-commerce search, etc.

**Strategy 1 — keyboard arrows:**

```javascript
await page.locator('textarea[name="q"]').type('mukesh otwani');
await page.waitForSelector('li[role="presentation"]');   // wait for suggestions to render
await page.keyboard.press('ArrowDown');
await page.keyboard.press('ArrowDown');
await page.keyboard.press('Enter');
```

Caveat: results can shift between manual testing and Playwright runs, so the second arrow-down may land on a different suggestion than you expected.

**Strategy 2 — match by text (recommended):**

```javascript
await page.locator('textarea[name="q"]').type('mukesh otwani');
await page.waitForSelector('li[role="presentation"]');
const elements = await page.$$('li[role="presentation"]');
for (let i = 0; i < elements.length; i++) {
  const text = await elements[i].textContent();
  if (text.includes('YouTube')) {
    await elements[i].click();
    break;
  }
}
```

This is robust to reordering of suggestions.

## JavaScript alerts, confirms, and prompts

JavaScript exposes three modal dialogs:

- `alert('message')` — one OK button.
- `confirm('message')` — OK and Cancel; returns `true` / `false`.
- `prompt('message')` — text input + OK/Cancel; returns the entered string or `null`.

By default Playwright **auto-accepts** dialogs; if you want to assert on them you must register a listener **before** the action that triggers the dialog:

```javascript
page.on('dialog', async (dialogWindow) => {
  expect(dialogWindow.type()).toContain('alert');     // 'alert' | 'confirm' | 'prompt'
  expect(dialogWindow.message()).toContain('I am a JS Alert');
  await dialogWindow.accept();
});

await page.locator('//button[text()="Click for JS Alert"]').click();
```

Methods on the dialog object:

- `accept(promptText?)` — clicks OK; for prompt dialogs you can pass the text to type before accepting (`await dialogWindow.accept('mukesh')`).
- `dismiss()` — clicks Cancel.
- `type()` and `message()` for assertions.

Running the same spec without overriding `--project` runs it in Chromium, Firefox, and WebKit in parallel — which is the headline cross-browser feature.

## Iframes

Inspect to confirm the target element lives inside an `<iframe>` (or a nested chain of frames). Trying to click an element inside a frame from `page.locator(...)` will fail with a 30-second timeout because the element is not on the top-level document.

Use **`page.frameLocator(...)`** to enter the frame, then chain locators and actions:

```javascript
const iframe = page.frameLocator('//frame[@name="packageListFrame"]');
await iframe.locator('//a[text()="java.applet"]').click();
```

`frameLocator` accepts CSS or XPath. The page used in the demo (Java SE docs) has three frames; you can locate by `name`, `title`, or `src`. Use `page.pause()` to drop into the Inspector to verify visually.

## Multiple tabs / windows

Single-page work uses `page` directly. To handle a second tab spawned by clicking a link with `target="_blank"`, you need a **browser context** and `Promise.all` listening for the `'page'` event:

```javascript
test('working with multiple tabs', async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://opensource-demo.orangehrmlive.com/');

  const [newPage] = await Promise.all([
    context.waitForEvent('page'),
    page.locator('(//a[contains(@href,"facebook")])[1]').click(),
  ]);

  await newPage.waitForTimeout(3000);
  await newPage.locator('input[name="email"]').nth(1).fill('mukesh@gmail.com');

  await newPage.close();
  await page.locator('#email1').fill('admin@email.com');
});
```

A **context** is an isolated browsing environment (its own cookies, storage, etc.). Multiple pages can live inside one context. The `Promise.all` ensures you wait simultaneously for both the click and the new-page event so you don't miss the popup.

If you `close()` the new tab and try to keep using a stale reference, you get `target page, context or browser has been closed`.

## `waitForLoadState('networkidle')`

If your page makes XHR/fetch requests that load critical content (like a checkbox grid populated from an API), Playwright's auto-wait does not know to wait for those calls. Example: counting six checkboxes on a registration page returns 0 because the checkboxes are not in the DOM yet at the moment of the count.

Fix:

```javascript
await page.getByText('New User Sign Up').click();
await page.waitForLoadState('networkidle');
const count = await page.locator('//input[@type="checkbox"]').count();
await expect(count).toBe(6);
```

`waitForLoadState` accepts `'load'`, `'domcontentloaded'`, or `'networkidle'`. Network idle waits until there are no pending network requests for at least 500 ms.

## Data from a JSON file (and data-driven testing)

Stop hardcoding test data inside specs — keep it in JSON, CSV, XML, Excel, or a database, and read it from your tests. JSON is the natural fit for JavaScript projects because Node has built-in support.

Create `testdata.json`:

```json
{
  "username": "mukesh@gmail.com",
  "password": "admin@123",
  "address": { "area": "HSR", "city": "Bangalore", "pin": 560034 },
  "interest": ["Cypress", "Java", "API"]
}
```

Read it in your spec:

```javascript
const playwrightTestData = require('../testdata.json');
const testData = JSON.parse(JSON.stringify(playwrightTestData));

await page.locator('//input[@id="email"]').fill(testData.username);
await page.locator('//input[@id="password"]').fill(testData.password);
// nested
await page.locator('//input[@id="area"]').fill(testData.address.area);
// arrays
await page.locator('//input[@id="interest"]').fill(testData.interest[1]); // "Java"
```

Out-of-bounds array indexes return `undefined`, which `fill()` rejects with "expected a string, got undefined."

**Data-driven testing** runs the same script over a list of records:

```json
[
  { "id": 1, "username": "mukesh1@gmail.com", "password": "p1" },
  { "id": 2, "username": "mukesh2@gmail.com", "password": "p2" },
  { "id": 3, "username": "mukesh3@gmail.com", "password": "p3" }
]
```

```javascript
const testData = JSON.parse(JSON.stringify(require('../testlogin.json')));

test.describe('data driven login test', () => {
  for (const data of testData) {
    test.describe(`login with users ${data.id}`, () => {
      test(`login test ${data.id}`, async ({ page }) => {
        await page.goto('...');
        await page.locator('//input[@id="email"]').fill(data.username);
        await page.locator('//input[@id="password"]').fill(data.password);
        await page.locator('//button[@type="submit"]').click();
      });
    });
  }
});
```

The template literal `` `login with users ${data.id}` `` is what avoids the "duplicate test title" error you get if every iteration uses the same string. The report shows three runs labelled by ID.

## Allure Report

Playwright ships with an `html` reporter (and `list`, `line`, `dot`, `json`, `junit`, GitHub Actions reporters). For richer dashboards there are third-party reporters; **Allure** is the most popular.

Install:

```bash
npm i -D allure-playwright
```

If npm complains about cache permissions, run `sudo npm cache clean --force` then re-run with `sudo` if it complains about permissions.

Use it from CLI:

```bash
npx playwright test --reporter=allure-playwright
```

Or add it project-wide in `playwright.config.js`:

```javascript
reporter: [['html'], ['allure-playwright']],
```

After running the tests, Playwright writes raw results into `allure-results/`. Generate the HTML report and open it:

```bash
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

The dashboard shows total runs, pass/fail/skipped/broken counts, suites by browser, categories, graphs (duration, severity, status, timeline), behaviors, and packages. Failed tests embed the screenshot and video automatically when you've enabled `screenshot: 'only-on-failure'` and `video: 'retain-on-failure'` (or `'on'`) in the config.

The full local workflow becomes a chain of three commands: run tests → generate report → open report. You can wrap them in a shell script or batch file, or call them from CI.

## Page Object Model in Playwright

POM is a **design pattern**, not a framework — a set of best practices for **reusability** and **maintenance**. It applies to Selenium, Cypress, WebdriverIO, and Playwright equally; once you understand it you can carry it across tools.

The core idea: for each page in your application (Login, Home, Payment, Category, etc.) create one JavaScript class that holds the **locators** for that page and the **methods** that act on those locators. Tests then instantiate those page classes and call their methods, instead of repeating selectors and actions in every spec.

Why:

- **Reusability** — write `loginToApplication(user, password)` once, call it from every test that needs a login.
- **Maintenance** — when a locator changes (e.g. `#email1` becomes `#email2`), update one place, not 100 specs.

### `pages/loginPage.js`

```javascript
const { expect } = require('@playwright/test');

class LoginPage {
  constructor(page) {
    this.page = page;
    this.username = '#email1';
    this.password = '//input[@placeholder="Enter Password"]';
    this.loginButton = '//button[text()="Sign In"]';
    this.header = '//h2[normalize-space()="Sign In"]';
  }

  async loginToApplication(user, password) {
    await this.page.fill(this.username, user);
    await this.page.fill(this.password, password);
    await this.page.click(this.loginButton);
  }

  async verifySignIn() {
    await expect(this.page.locator(this.header)).toBeVisible();
  }
}

module.exports = LoginPage;
```

### `pages/homePage.js`

```javascript
const { expect } = require('@playwright/test');

class HomePage {
  constructor(page) {
    this.page = page;
    this.menu = '//img[@alt="menu"]';
    this.logoutOption = '//a[normalize-space()="Sign out"]';
    this.manageOption = '//span[normalize-space()="Manage"]';
  }

  async logoutFromApplication() {
    await this.page.click(this.menu);
    await this.page.click(this.logoutOption);
  }

  async verifyManageOption() {
    await expect(this.page.locator(this.manageOption)).toBeVisible();
  }
}

module.exports = HomePage;
```

### `tests/loginApplication.spec.js`

```javascript
const { test } = require('@playwright/test');
const LoginPage = require('../pages/loginPage');
const HomePage = require('../pages/homePage');

test('login to application using POM', async ({ page }) => {
  await page.goto('https://...');
  const loginPage = new LoginPage(page);
  const homePage = new HomePage(page);

  await loginPage.loginToApplication('admin@email.com', 'admin@123');
  await homePage.verifyManageOption();
  await homePage.logoutFromApplication();
  await loginPage.verifySignIn();
});
```

Notes:

- **Always export the class** (`module.exports = LoginPage`) and **import** it (`require('../pages/loginPage')`) — without the export the import returns nothing.
- The `constructor(page)` receives the Playwright `page` fixture from each test (which is isolated per test) and stores it on `this.page`; every method then uses `this.page.fill(...)`, `this.page.click(...)`, etc.
- **Parameterize methods** instead of hardcoding test data inside the page (`async loginToApplication(user, password)`); the test still owns the credentials, ideally pulled from a JSON file as in the previous chapter.
- Use `await page.pause()` in tests to drop into the Inspector when debugging.

## Pushing the project to GitHub (HTTPS and SSH)

Two prerequisites: install Git on Mac/Windows (Mukesh has separate videos for both) and confirm with `git --version`.

### Create the repo

On GitHub, click `+` → **New repository**. Pick a meaningful name (`playwright-demo` in this demo), an optional description (`Playwright JS/TS for Web Automation`), public or private, and skip README/.gitignore/license for now since you'll add them locally.

### Add a `.gitignore`

In the project root, create `.gitignore` listing files you do not want tracked:

```
node_modules
playwright-report
test-results
allure-report
allure-results
.DS_Store
```

### Workflow over HTTPS

```bash
git init
git status                      # see what's not yet staged
git add .
git status                      # confirm what's staged
git commit -m "first code push"
git log                         # confirm the commit and copy the SHA
git branch -M main              # rename master → main (modern convention)
git remote add origin https://github.com/<user>/<repo>.git
git push -u origin main
```

If push fails with an authentication error, GitHub no longer accepts passwords — you need a **personal access token (PAT)**. Generate one under **Profile → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)**, name it (e.g. `mukesh-token-feb-2024`), set expiration (or "no expiration"), check the scopes you need (or check all if you want full control), and copy the token (you cannot view it again).

To make Git remember credentials:

```bash
git config --global credential.helper store
git push -u origin main         # username = your GitHub username, password = the token
```

On Mac the token ends up in **Keychain Access** under github.com.

### Workflow over SSH (recommended)

Generate a key pair:

```bash
ssh-keygen
```

Accept the default location (`~/.ssh/id_rsa`) — overwrite if prompted, no passphrase if you want non-interactive pushes. This produces `id_rsa` (private, stays on your machine) and `id_rsa.pub` (public).

Open `id_rsa.pub`, copy its contents, then in **GitHub → Settings → SSH and GPG keys → New SSH key**, give it a title (`mukesh-mac-feb-2024`) and paste. Now you can clone/push without passwords or tokens.

The push flow is identical to HTTPS except the remote URL uses the `git@github.com:user/repo.git` form:

```bash
git init
git add .
git commit -m "code push via SSH"
git branch -M main
git remote add origin git@github.com:<user>/<repo>.git
git push -u origin main
```

A good `README.md` describes preconditions ("Node 14+ should be installed"), how to clone, how to install (`npm install`), how to run tests (`npx playwright test`), and any project-specific commands.

## Running Playwright in Jenkins

Prerequisites: a working Jenkins install (Mukesh has a separate Jenkins series), Node.js installed on the agent that will execute the build, and your Playwright project either on the local file system or pushed to GitHub.

The official docs at **playwright.dev → Continuous Integration** cover GitHub Actions, Docker, Azure Pipelines, CircleCI, and Jenkins.

### Part 1 — Run a locally cloned project

Clone your repo into a fixed local folder (e.g. `C:\Users\me\Desktop\PWcode\playwright-demo`).

Create a new Jenkins **Freestyle project** named `playright-Github`, then add **Build Steps → Execute Windows batch command** (Mac/Linux: **Execute shell**).

First sanity check:

```bat
node --version
```

Build, confirm Jenkins prints your Node version. Then add the real steps:

```bat
cd C:\Users\me\Desktop\PWcode\playwright-demo
npm install
npx playwright install
```

These install dev dependencies (from `package.json`) and the browsers. Then in a second build step (or appended to the first):

```bat
cd C:\Users\me\Desktop\PWcode\playwright-demo
npx playwright test tests/example.spec.js --project=chromium --headed
```

A common mistake: each Windows batch command starts in the workspace root, so you must repeat the `cd` in every separate build step, or keep all commands in one step. If you forget, you get `error: project chromium --headed not found` because Playwright is being run from the wrong folder and can't find your `playwright.config.js`.

### Part 2 — Pull from GitHub via the Git SCM plugin

In the same job, configure **Source Code Management → Git**, paste the repo URL, add credentials if it's private, and set the branch (`*/main` or `*/master` depending on your repo). Now the cloned `cd` in your build step is unnecessary — Jenkins clones into its own workspace.

The build step becomes simply:

```bat
npm install
npx playwright install
npx playwright test tests/example.spec.js --project=chromium --headed
```

Jenkins clones into something like `C:\Users\me\.jenkins\workspace\playright-Github\`.

### Part 3 — Parameterized job

Hardcoding the spec file and browser into the build step means a new job for every variant. Better: tick **This project is parameterized** and add **Choice Parameter**s.

`SPEC_FILE`:
```
example.spec.js
login.spec.js
```

`BROWSER`:
```
chromium
firefox
webkit
all
```

Substitute them into the build step:

```bat
npm install
npx playwright install
npx playwright test tests/%SPEC_FILE% --project=%BROWSER% --headed
```

(On Linux/Mac shells use `$SPEC_FILE` and `$BROWSER` instead of `%...%`.) The job now shows **Build with Parameters** and presents two dropdowns at run time. **Be careful with spaces** — `--project=%BROWSER%--headed` (no space) fails because Playwright sees one mashed-together flag; keep a space before `--headed`.

### Recap

1. Confirm Jenkins is configured and the agent has Node.js.
2. Confirm the project runs locally with `npx playwright test`.
3. `npm install` → `npx playwright install` → `npx playwright test ... --project=... --headed`.
4. For ergonomics: parameterize `SPEC_FILE` and `BROWSER`.

The same recipe applies to GitHub Actions, Docker, Azure Pipelines, CircleCI, and any other CI: only the YAML/UI changes — the underlying Playwright commands stay the same. If you use Java + Maven, Python + pytest, or .NET, swap the install/run commands accordingly.
