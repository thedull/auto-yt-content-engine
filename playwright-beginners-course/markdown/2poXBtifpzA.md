# #1 Playwright Tutorial Full Course 2026 | Playwright Testing Tutorial

> **Source:** [#1 Playwright Tutorial Full Course 2026 | Playwright Testing Tutorial](https://www.youtube.com/watch?v=2poXBtifpzA) — [Testers Talk](https://www.youtube.com/@testerstalk) · 2024-01-08 · 6:55:08
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A nearly 7-hour, end-to-end **Playwright** course in JavaScript by Testers Talk, covering everything from installation through page-object-model and video recording.
- Walks through both the **VS Code Playwright extension** workflow (Test Explorer, Codegen, Pick Locator, Record at Cursor) and the **command-line / npm init** workflow with `npx playwright test`.
- Detailed coverage of **locators** (`getByRole`, `getByLabel`, `getByAltText`, `getByTestId`, `getByText`, `getByTitle`, XPath, CSS, `getByPlaceholder`), **assertions** (hard and soft), **hooks** (`beforeEach`, `beforeAll`, `afterEach`, `afterAll`), and built-in HTML reporting.
- Covers practical UI scenarios: dropdowns, iframes, drag-and-drop, mouse and keyboard actions, date picker, screenshots, **traces**, **watch mode**, **retries**, **parallel execution**, **parameterization**, and **visual comparison testing**.
- Ends with framework topics: **environment files** via `dotenv`, **data-driven testing** with JSON and CSV, **multi-environment** test data, **Page Object Model**, **video recording**, and **maximizing/setting viewport** of the browser.

## Chapter 1 overview: getting started with Playwright

The course starts with an introduction to Playwright as an open-source automation testing tool used to perform end-to-end testing of modern web applications and mobile applications, in either headed or headless mode. The instructor previews chapter one, which covers what Playwright is, its advantages and limitations, the architecture, comparisons with Cypress and Selenium WebDriver, the software prerequisites (Visual Studio Code and Node.js), installation, the default folder structure, the Test Explorer, running tests across browsers (Chrome, Edge, WebKit, Firefox), recording tests in VS Code, generating the **Playwright HTML test report**, the **Record at Cursor** feature, common terminologies, writing the first test with **Pick Locator**, installing via the command prompt, running in headless or headed mode from the terminal, running specific spec files, running tests on different browsers, and using **Codegen** to record tests.

## What is Playwright: advantages and limitations

**Playwright** is an open-source automation testing tool used to perform end-to-end testing of modern web and mobile applications, in headed or headless mode.

Advantages:

- **Cross-browser testing** — runs tests in Chrome, Edge, Chromium, Firefox, and WebKit.
- **Cross-platform testing** — supports Windows, Linux, and macOS.
- **Cross programming language support** — JavaScript, TypeScript, Python, .NET, and Java.
- **Mobile emulation** — Google Chrome for Android and Mobile Safari (emulation only).
- **Auto-wait** — when performing actions on web elements, Playwright automatically waits for them, so you see very few flaky tests.
- **Tracing** — for a test with, say, ten steps you can see exactly what happened in each step, including network requests and responses.
- **Built-in reporting** — number of tests executed, passed, failed, and skipped.
- **Dynamic wait assertions** — built-in default wait that polls for an element before performing the assert; the wait can be modified.
- **Faster and more reliable** than Selenium and Cypress; running the same test 10 times yields the same result.
- **Powerful tooling** — Codegen for recording, Playwright Inspector for identifying elements, Trace Viewer for inspecting steps and network details.
- **No flaky tests** thanks to auto-wait and dynamic wait assertions.

Limitations:

- **Less community support** compared to Selenium WebDriver, since Playwright is newer.
- **Does not support legacy browsers** such as Internet Explorer 11.
- **Cannot test mobile apps on real devices** — only emulation is supported.

## Playwright architecture

When a test is triggered, three components and two protocols are involved.

Components:

1. **Client** — where the Playwright automation test is written (JavaScript, Java, Python, C#, etc.).
2. **Playwright server** — communicates between the client and the browser engines.
3. **Browser engines** — Chrome, Firefox, WebKit, etc.

Protocols:

- **WebSocket protocol** — used between the client and the Playwright server.
- **CDP (Chrome DevTools Protocol)** — used between the Playwright server and Chromium/Chrome. For Firefox and WebKit, Playwright has implemented its own equivalent protocol.

Workflow: the client converts the automation code into JSON format and sends it over a single WebSocket connection (established via WebSocket handshake) to the Playwright server, which then talks to the browser engines via CDP. All communication for all triggered tests happens over that single WebSocket connection — it is not closed between tests, which is why test failures and flakiness are very low.

## Playwright vs Cypress

| Feature | Playwright | Cypress |
| --- | --- | --- |
| Language support | JavaScript, TypeScript, Java, Python, C#/.NET | JavaScript only |
| Browser support | Multiple browsers + mobile emulation (Chrome, Safari) | Chrome, Edge, Firefox, Electron only |
| Framework | Mocha, Jest, Jasmine | Mocha only |
| Operating systems | Windows, Linux, Mac | Windows, Linux, Mac (10.9+) |
| Open source | Fully open source | Some features paid |
| Community support | Bit less (newer tool) | Strong community (older tool) |
| Mobile app testing on real devices | Not supported | Supported via cloud |
| Reporting | Generated within seconds | Needs third-party plugins |

## Playwright vs Selenium WebDriver

Differences:

- **Language support** — Playwright: JS, TS, Java, Python, C#/.NET. Selenium adds Ruby, Perl, PHP.
- **Browser support** — Playwright: Chrome, Edge, Firefox, Chromium, mobile Chrome and mobile Safari, plus WebKit. Selenium: Chrome, Edge, Firefox, Safari, Opera (no WebKit).
- **Frameworks** — Playwright: Jest, Jasmine, Mocha, Vitest. Selenium: Jasmine, Mocha, WebDriverIO, TestNG, JUnit, NUnit.
- **OS support** — Playwright: Windows, Linux, Mac. Selenium adds Solaris.
- **Open source** — both are open source. Playwright is from Microsoft; Selenium is community-developed.
- **Community** — Playwright has less community support; Selenium has very large community and well-established documentation.
- **Mobile app testing** — Playwright supports it. Selenium needs Appium.
- **Speed** — Playwright is much faster than Selenium.
- **Reporting** — Playwright provides built-in reporting. Selenium needs TestNG, ExtentReports, Allure, etc.
- **Auto-wait** — Playwright has it built in. Selenium needs custom code.
- **Architecture** — Playwright: headless browser with event-driven architecture. Selenium: four layers (client library, JSON Wire Protocol, browser drivers, browsers).
- **Prerequisites** — Playwright needs Node.js. Selenium needs APIs and drivers per browser.

## Software requirements

You need:

- **Node.js**
- **Visual Studio Code**
- The course uses **JavaScript** for tests.
- Any operating system: Windows, Mac, or Linux.

## Installing Node.js and VS Code

Node.js: go to google.com, search "download nodejs", click the official link, choose the right OS and bit-size (the instructor uses the 64-bit MSI on Windows). Run the installer, accept the license, click Next/Install/Finish. Verify in command prompt with `node -v` — it should print the installed version.

VS Code: search "download vs code", pick the official site, choose your OS, run the installer (Next/Next/Finish), then launch from Start menu.

## Installing Playwright via VS Code

Three simple steps:

1. Install the extension **Playwright Test for VS Code** (developed by Microsoft) from the Extensions sidebar.
2. Press `Ctrl+Shift+P`, type **Install Playwright**, and select it.
3. Pick Playwright configurations: select all browsers (Chromium, Firefox, WebKit), choose **JavaScript** (or TypeScript), uncheck "Add GitHub Actions workflow" if not needed, then click OK.

The extension installs the required Playwright libraries and plugins, downloads browser executables, and creates `package.json`, `package-lock.json`, `node_modules/`, a `tests/` folder, and a `tests-examples/` folder.

## Default Playwright folder structure

- `node_modules/` — JavaScript files and plugins required to run JS code and Playwright tests.
- `tests/` — contains `example.spec.js`, with two basic sample test cases provided by Microsoft.
- `tests-examples/` — contains `demo-todo-app.spec.js` with multiple advanced automation test cases that you can use to learn how to write tests.
- `package.json` — dependency details. Initially shows `@playwright/test` and `@types/node` plus their versions; any newly installed plugin is added here automatically.
- `playwright.config.js` — all Playwright configurations: where tests live, whether to run in parallel, retry counts, reporting, browsers (Chromium, Firefox, WebKit), headed/headless mode, and so on.

## Running Playwright tests in VS Code and the Test Explorer

Open `tests/example.spec.js` — it has two tests. Click the play icon next to a test, or right-click and select "Run Test" to execute it; the test runs in Chromium and the status appears.

The **Test Explorer** is the testing icon in the left sidebar. It lists all spec files and tests, and lets you:

- Switch the configuration (browser) at the top — default is Chromium; selecting Firefox runs all tests in Firefox.
- Run all tests, run a single spec, or run a single test.
- Debug tests at the project, spec, or single-test level.
- Filter tests by status (failed, executed), by active file, or by regex match.

To run in headed mode, add `headless: false` to `playwright.config.js`. The default is headless.

For sequential execution instead of parallel, set `fullyParallel: false` in the config.

## Running on branded browsers (Chrome and Edge)

Two ways:

1. **Test Explorer** — click the configuration arrow next to the testing icon and select WebKit, Edge, etc.
2. **`playwright.config.js`** — comment out the default project block (lines ~37–50 in the course example) and uncomment the Chrome/Edge project block (lines 63–66). Then run `example.spec.js` and tests execute in Edge or Chrome.

## Recording a test in VS Code (Codegen) and the HTML report

Manual scenario: open `github.com/<username>`, click Sign In, enter username and password, click the Sign in button, validate the displayed error message.

In VS Code, go to the testing tab, find the Playwright features in the lower left, and click **Record new**. A browser opens; enter the URL and perform the actions you want recorded. To validate the error text, use the assertion grid which has three options: **Assert visibility**, **Assert text**, and **Assert value**. Use Assert text and click the text element to capture; click Accept in the popup, then close the browser.

A `test-1.spec.ts` file is generated automatically (rename to `record-test.spec.js` if you prefer JS). The generated code navigates to the URL, clicks the sign-in link, fills the username and password text boxes, clicks the Sign in button, and validates the error text via `toContainText`.

Run the test — it passes. To prove it works, replace the expected text with something different and re-run; the assertion fails because actual and expected don't match.

The **Playwright HTML test report** is generated automatically in a `playwright-report/` folder; open `index.html` to see total tests, pass/fail/flaky/skipped counts, the spec name, test name, browser, and per-step timings. On a failed test, you see the expected vs received string and the step that failed.

## Record at Cursor

This feature lets you insert recorded code in the middle of an existing test, at the current cursor position. In the testing panel, check **Show browser** and click **Record at Cursor**. A browser opens; stop the recording, navigate to the URL, then resume recording. Place your cursor where you want code inserted, return to the browser, choose **Assert visibility**, click the element (e.g., the Sign in button), and code like `await expect(...).toBeVisible()` is inserted at the cursor position in the spec file.

## Commonly used Playwright terminologies

Five keywords:

- **`require`** — includes the Playwright module in the current JavaScript file.
- **`async`** — declares an async function. Each call returns a new promise that resolves with the value or is rejected with an exception (similar to try/catch).
- **`await`** — used inside an async function with expressions; you can write zero or more `await` expressions inside an async function.
- **`page`** — a browser context object used to open URLs and interact with the browser (perform actions on web elements).
- **`expect`** — an assertion library for JavaScript and TypeScript intended for use with the Jest test runner or Playwright Test, used to write assertions for end-to-end and component testing.

## First Playwright test using Pick Locator

Manual scenario: navigate to youtube.com, search for "Cypress by testers talk", click the Search icon, click the Cypress by testers talk playlist, validate the page tab title (which is `<video description> - YouTube`).

Steps:

1. Create `tests/firstTest.spec.js`.
2. Include the Playwright module: `const { test, expect } = require('@playwright/test');`.
3. Define a test named "validate YouTube title" with `test('validate YouTube title', async ({ page }) => { ... })`.
4. Inside, `await page.goto('https://www.youtube.com')`.
5. Use **Pick Locator** (in the testing panel) to find the search text box. Click it in the browser, press Enter to copy the locator into VS Code.
6. Click the search box: `await page.<locator>.click()`. Fill it with `await page.<locator>.fill('Cypress by testers talk')`.
7. Use Pick Locator again for the Search icon. Use `await expect(<locator>).toBeEnabled()` to assert it's enabled, then `.click()` it.
8. Pick the playlist locator and click it. Use `await page.waitForTimeout(5000)` for a 5-second explicit wait.
9. Validate the title with `await expect(page).toHaveTitle('<expected text> - YouTube')`.

Run the test — it passes. Modify the expected title to fail it and confirm the report shows the expected vs received strings.

## Installing Playwright via the command prompt

Two steps:

1. In an empty folder, open command prompt and run `npm init playwright@latest`.
2. Select Playwright configurations: choose **JavaScript** (or TypeScript), put end-to-end tests in `tests`, decline the GitHub Actions workflow, accept installing Playwright browsers (true).

This installs Playwright and downloads the browsers. Open the generated folder in VS Code and run `tests/example.spec.js` to verify.

## Running tests in headless mode and viewing the report from terminal/cmd

In the VS Code terminal (or command prompt), run `npx playwright test`. By default this runs all tests in `tests/`, in headless mode, across Chromium, Firefox, and WebKit — so two tests become six executions.

To open the report: `npx playwright show-report` — opens the HTML report showing all six runs grouped by browser, with per-test timing. WebKit ran fastest in the example; Firefox took ~13 seconds.

## Running tests in headed (UI) mode from command prompt

`npx playwright test --headed` runs the tests with the browser UI visible. The instructor demonstrates with `example.spec.js`, two tests across three browsers, two parallel workers. After the run, the HTML report opens automatically; if a test fails (one Firefox test failed in the demo due to load), pressing Ctrl+C and re-running showed all six passing.

## Running a specific spec file

To run only one spec file, append the file name: `npx playwright test --headed demo.spec.js`. The instructor copied `example.spec.js` to `demo.spec.js`, kept one test inside, renamed it to "demo 1 2 3", then ran only that file (which executes once per browser, so three runs total).

The same approach works for `example.spec.js`: `npx playwright test --headed example.spec.js` (six runs since it has two tests).

## Running on different browsers using `--project`

Use `--project=<browser>` to limit execution to a single browser:

- `npx playwright test --project=chromium` — runs all tests on Chromium.
- `npx playwright test --project=webkit` — runs all tests on WebKit.

In the example, three automation tests across two spec files run on the chosen browser, and the report shows the project name.

## Recording with Codegen from the command prompt

Run `npx playwright codegen`. Two windows open: a browser and the **Playwright Inspector**. Type a URL into the address bar, perform manual actions, and the Inspector shows the generated code in real time. The instructor demonstrates: navigate to youtube.com, search for "API testing by tester stock", **Assert visibility** on the search icon, click the icon, click the playlist, **Assert text** on the title.

Copy the generated code into a new spec file (`recordAndPlay.spec.js`), add an explicit wait `await page.waitForTimeout(5000)` to handle YouTube's slow load, and click on the search text box before filling. The instructor hits multiple timeouts (default per-test timeout is 30 seconds, set in the config) and recommends adding additional waits or improving internet connection for heavy applications like YouTube.

## Chapter 2 overview

Locators, capture element / page / full-page screenshot, hooks (preconditions and postconditions), adding screenshots to the report on failure, dropdowns, iframes, dates (today's date and custom dates), mouse and keyboard actions, drag-and-drop, hard and soft assertions, watch mode, and traces.

## Locators in Playwright

Multiple ways to identify a web element. The instructor goes through nine locator types:

- **`getByRole`** — `await page.getByRole('link', { name: 'videos' }).click()`. The role can be `link`, `button`, `checkbox`, `combobox`, `heading`, etc.
- **`getByLabel`** — `await page.getByLabel('Search', { exact: true }).press('Enter')`. Uses the `aria-label` attribute. Pass `exact: true` for exact match, or omit for partial.
- **`getByAltText`** — `await page.getByAltText('<alt-text>').click()`. Uses the `alt` attribute on images.
- **`getByTestId`** — uses a custom attribute (e.g., `autocomplete`) configured in `playwright.config.js` via `testIdAttribute: 'autocomplete'`. Then `await page.getByTestId('<value>').fill('testers talk')`.
- **`getByText`** — `await page.getByText('Cypress by')` for partial match, `await page.getByText('Cypress by testers talk', { exact: true })` for exact.
- **`getByTitle`** — uses the `title` attribute, e.g., `await page.getByTitle('Cypress by testers talk').click()`.
- **XPath** — `await page.locator('//textarea[@name="search_query"]').click()`. The `xpath=` prefix is optional.
- **CSS selector** — `await page.locator('textarea[name="search_query"]').click()`. The `css=` prefix is optional.
- **`getByPlaceholder`** — uses the `placeholder` attribute.

In each example, the instructor inspects the element in DevTools, extracts the relevant attribute, writes the locator, performs an action (click, fill, press Enter), and runs the test against google.com or github.com.

## Capturing screenshots

Three types: element screenshot, page screenshot, full-page screenshot.

Setup: create `tests/screenshots.spec.js`, copy the test skeleton, and create a `screenshots/` folder in the project.

- **Element screenshot** — identify the element with `await page.locator('#<id>').screenshot({ path: './screenshots/element.png' })`. The example uses YouTube's channel header `#channel-header`.
- **Page screenshot** — `await page.screenshot({ path: './screenshots/page.png' })` captures the current viewport.
- **Full-page screenshot** — `await page.screenshot({ path: './screenshots/full-page.png', fullPage: true })` captures the entire scrollable page.

Each screenshot is written to the `screenshots/` folder and can be opened to verify.

## Adding screenshots to the report on failure

By default, screenshots are not attached to the report whether the test passes or fails. To enable failure screenshots, edit `playwright.config.js` under the `use` block and add `screenshot: 'only-on-failure'`. Re-run a failing test (e.g., `firstTest.spec.js` with a wrong expected title) — the HTML report now includes a Screenshots section showing where the test failed.

## Hooks: `beforeEach`, `beforeAll`, `afterEach`, `afterAll`

Hooks are blocks of code that run before or after tests:

- **`beforeEach`** — runs before each test.
- **`beforeAll`** — runs once before all tests.
- **`afterEach`** — runs after each test.
- **`afterAll`** — runs once after all tests.

The instructor builds `tests/hooks.spec.js` with two tests, each navigating to YouTube and searching with different keywords. Repeated setup (e.g., `await page.goto(...)`) is moved into `test.beforeEach('run before each test', async ({ page }) => { ... })`. Other hooks are added with `console.log` messages to demonstrate ordering. `beforeAll` and `afterAll` should not use the `page` object.

The execution order is: `beforeAll` → `beforeEach` → test → `afterEach`, repeated per test, and finally `afterAll`. Verifying via the report's "stdout" tab shows this exact order.

Use cases include creating/cleaning test data, loading fixtures from CSV/Excel/JSON in `beforeAll`, and closing connections to external sources in `afterAll`.

## Handling dropdown lists

Two ways to select dropdown values: by **value** and by **visible text**. You can also verify a dropdown's selected value.

Manual scenario: facebook.com → Create new account → Month dropdown.

Build `tests/dropdownList.spec.js`. Navigate to facebook.com, click "Create new account" via `getByText`. Identify the month select with a CSS selector like `#<id>` and assign to a `dropdownList` variable.

- Select by value: `await dropdownList.selectOption('5')` selects May (Jan=1, Feb=2, ... May=5, June=6).
- Select by visible text: `await dropdownList.selectOption('Aug')` selects August.

Verify default value: `await expect(<element>).toHaveValue('12')` — December is selected by default. Pass a wrong value to confirm the test fails.

## iFrames and drag-and-drop

URL: `jqueryui.com/droppable`. Source = "Drag me to my target", destination = "Drop here". Both elements live inside an iframe.

Build `tests/iframeDragAndDrop.spec.js`:

1. Navigate to the URL.
2. Identify the iframe via class: `const iframeElement = page.frameLocator('.demo-frame')`.
3. Source: `const dragElement = iframeElement.locator('#draggable')`.
4. Destination: `const dropElement = iframeElement.locator('#droppable')`.
5. Perform the drag: `await dragElement.dragTo(dropElement)`.
6. Add `await page.waitForTimeout(...)` to observe.

The test successfully drags the source onto the destination.

## Mouse actions

URL example: a Google search results page for "tester stock". Build `tests/mouseActions.spec.js`.

Identify the channel link with `getByRole('link', { name: 'testers talk' }).first()`. Then:

- Normal click: `.click()`.
- Double click: `.dblclick()`.
- Right click: `.click({ button: 'right' })`.
- Middle click: `.click({ button: 'middle' })` — opens the link in a new tab.
- Left click: `.click({ button: 'left' })`.
- Hover: `await page.locator('div[aria-label="Search by voice"]').hover()` — reveals tooltip text "Search by voice".

## Keyboard actions

Common keys: backspace, tab, enter, escape, insert, page down, page up, F1–F12, digits, A–Z, etc.

Build `tests/keyboardActions.spec.js`. Navigate to google.com, identify the search box with `[aria-label="Search"]`. Examples:

- Click and type: `.click().first()` then `.fill('playwright by tester stock').first()` (note: the instructor initially used `.press()` mistakenly instead of `.fill()`).
- Press Enter: `.press('Enter')` to fetch results.
- Select all: `.press('Control+A')`.
- Delete selected: `.press('Delete')`.
- Tab + Enter via the page-level keyboard: `await page.keyboard.press('Tab')` then `await page.keyboard.press('Enter')` — moves focus to "Search by voice" and triggers the alert.

## Date picker

URL: `jqueryui.com/datepicker`. The date field is inside an iframe.

Build `tests/datePicker.spec.js`:

1. Navigate to the URL.
2. Switch into iframe: `const frameElement = page.frameLocator('.demo-frame')`.
3. Identify the date field by class.

Three ways to pick a date:

- **Custom date by direct fill** — accepts MM/DD/YYYY: `await frameElement.locator('.<class>').fill('12/20/2023')`.
- **Today's date** — click the field to open the calendar. Today's date has a unique class ending in `ui-datepicker-today`. Use a CSS selector like `.<class-value>` to click today's cell.
- **Custom relative date (e.g., today - 3, today + 3)** — read the `data-date` attribute from the today's-date anchor: `let currentDateValue = await frameElement.locator('.<today-class> a').getAttribute('data-date')`. Compute the offset: `const customDate = parseInt(currentDateValue) - 3` (or `+ 3`). Build a CSS selector dynamically: `[data-date='${customDate.toString()}']` and click it. Remember to `await` the `getAttribute` call — missing `await` causes the wrong attribute to be returned.

## Assertions: hard and soft

**Hard assertion** — if the assertion fails, the test terminates immediately. **Soft assertion** — the test continues even if an assertion fails, and all failures are reported at the end.

Important assertion methods:

- `toHaveURL(<expected>)` — verify URL.
- `toHaveTitle(<expected>)` — verify page title.
- `toHaveText(<expected>)` — verify element text.
- `toBeEditable()` — element is editable.
- `toBeVisible()` — element is visible.
- `toBeEnabled()` — element is enabled.
- `toBeDisabled()` — element is disabled.
- `toBeEmpty()` / `not.toBeEmpty()` — element is (not) empty.
- `toHaveCount(<n>)` — locator matches `n` elements (must be a number, not a string).

Build `tests/assertions.spec.js`. The instructor demonstrates each method against google.com search results: assert URL, title, search-textbox text, editable/visible/enabled state, disabled (expected to fail because the box is enabled), empty (also expected to fail because the textbox has text — using `not.toBeEmpty()` makes it pass), and `toHaveCount(2)` for a CSS selector matching two elements (the third match is inside an iframe and excluded).

To convert any hard assertion into a soft assertion, call `expect.soft(...)` instead of `expect(...)`. Test execution continues and the final report shows multiple step failures.

## Watch mode

Watch mode automatically re-runs a test whenever its file is saved.

Open the Playwright Test Runner UI: `npx playwright test --ui`. Select a spec, click the **watch** icon (per-test) on the right. From then on, any save to that spec file triggers an automatic re-run. The instructor edits `assertions.spec.js`, adds a `console.log("assertions in playright test is running")`, saves, and the test re-runs immediately in the right pane.

## Traces

Traces add detailed information about the test-execution lifecycle to the report — actions, metadata, console logs, network details, and screenshots over time.

Enable in `playwright.config.js` under `use`: `trace: 'retain-on-failure'` (or `'on-first-retry'` if retries are enabled).

After running a failing test (e.g., `failedTest.spec.js`) with `npx playwright test --headed failedTest.spec.js`, the HTML report shows a **Traces** section. Click into it to see a timeline of screenshots, the test steps with before/after screenshots, **Metadata**, **Action**, **Call**, **Logs**, **Errors**, **Console**, **Network**, **Source**, and **Attachment** tabs.

## Chapter 3 overview

Annotations (skip and only), grouping and tagging, repeating tests, automatic retry, parallel testing, parameterized tests, and visual comparison testing.

## Skipping tests and running only selected tests

Build `tests/annotations.spec.js` with three tests "assertions in playright 1/2/3".

- To skip test 2: `test.skip('assertions in playright 2', async ({ page }) => { ... })`. The HTML report shows one skipped, two passed.
- To run only one test: `test.only('assertions in playright 1', ...)` — only that test runs.

## Grouping tests with `describe`

Build `tests/group.spec.js`. Use `test.describe('smoke testing', () => { test('test one', ...); test('test two', ...); })` and `test.describe('sanity testing', () => { test('test three', ...); })`. The Test Explorer shows the groups; you can run a group as a unit. In real projects, group tests by smoke, sanity, regression, etc.

## Tagging tests

Tag tests by appending `@<tag>` to the test description: `test('test one @tag1', ...)`, `test('test two @tag2', ...)`, `test('test three @tag1', ...)`.

Run by tag from the terminal: `npx playwright test --grep @tag1` runs the two `@tag1` tests; `--grep @tag2` runs the single `@tag2` test. Real projects use names like `@smoke`, `@sanity`, `@regression`.

## Running a test multiple times

Use `--repeat-each=<n>` to run a test N times to check stability:

`npx playwright test assertions.spec.js --repeat-each=2` runs once, then again. With `--repeat-each=3` it launches three browsers in parallel. The report shows three entries for the same test name.

## Retrying failed tests

In `playwright.config.js`, the top-level `retries` is split between pipeline (already 2 in the demo) and local. Set the local `retries: 1` to retry once on local runs, or `retries: 2` for two retries.

Run from terminal: `npx playwright test failedTest.spec.js`. With `retries: 1`, on failure the test runs again once and the report shows "Original" plus "Retry #1" tabs. With `retries: 2`, you also get "Retry #2".

## Parallel test execution

Set `fullyParallel: true` in `playwright.config.js` (under `defineConfig`). Then control concurrency via `--workers`:

`npx playwright test group.spec.js --workers=3` runs three tests at a time. With five total tests it triggers three, then two more. With `--workers=4` it triggers four browsers simultaneously and finishes faster (41 seconds in the demo).

## Parameterizing tests

Build `tests/parameterizeTest.spec.js`. Navigate to youtube.com, identify the search box via `getByPlaceholder('Search')`, click, fill with a search keyword, press Enter.

Define `const testParameters = ['playright by tester stock', 'Cypress by tester stock', 'JavaScript by tester stock']`.

Wrap the test in a `for...of` loop:

```js
for (const searchKeyword of testParameters) {
  test(`parameterize tests in playright ${searchKeyword}`, async ({ page }) => {
    // ... use ${searchKeyword} in fill()
  });
}
```

The same test runs three times with the keyword interpolated into both the description and the `fill()` call. The report shows three separate test entries.

## Visual comparison testing

Compares the current screenshot to a reference snapshot saved on the first run.

Build `tests/visualTesting.spec.js`. Navigate to `github.com/login`, wait, then call `await expect(page).toHaveScreenshot('githubPage.png')`.

First run fails with "snapshot does not exist" — this is expected; Playwright now saves a baseline under `tests/visualTesting.spec.js-snapshots/githubPage-<browser>-<os>.png` (e.g., `-chromium-win32`). Subsequent runs compare against that baseline and pass.

To force a difference: identify the username textbox by ID with a CSS selector and `.fill('testers stock')`. Take a second screenshot after the action with the same `toHaveScreenshot` call. The second comparison fails; the report includes a new **Image mismatch** section showing actual, expected, and diff images.

## Chapter 4 overview

Environment files, JSON and CSV data-driven testing, multi-environment test data, Page Object Model, video recording, and full-screen browser.

## Environment file with `dotenv`

Install: `npm install dotenv --save`. Verify the dependency appears in `package.json`.

Build `tests/readEnvFile.spec.js`. The test goes to a URL, identifies Google's search box by ID, clicks, fills with "playright by tester stock", presses Enter.

Create a `.env` file in the project root:

```
ENVIRONMENT=qa
URL=https://www.google.com
USER_NAME=testers
PASSWORD=secret
```

Read in the test with `process.env.URL`, `process.env.USER_NAME`, `process.env.PASSWORD`.

To enable `.env` loading, uncomment the `require('dotenv').config()` line (around line 8) in `playwright.config.js`. Without this, you get "expected string but got undefined".

## Data-driven testing with a JSON file

Build `tests/dataDrivenTestingJson.spec.js`. The test reuses the env-file pattern: navigate to the URL, search with a keyword.

Create `test-data/qa/google.json`:

```json
{
  "moduleOneTestData": {
    "skill1": "playright by tester stock",
    "skill2": "Cypress by tester stock",
    "skill3": "JavaScript by tester stock"
  }
}
```

In the spec, `import moduleOneTestData from '../test-data/qa/google.json';` and use `moduleOneTestData.skill1` (or `.skill2`, `.skill3`) in the fill.

For true data-driven execution, wrap the test in `for (const [key, value] of Object.entries(moduleOneTestData))` and reference `${value}` in both the test title and the fill. The same test runs three times with three different search keywords.

## Data-driven testing with a CSV file

Install: `npm install csv-parse`. Verify the dependency in `package.json`.

Create `test-data/qa/testdata.csv`:

```
"testCaseID","skill1","skill2"
"TC_01","playright by tester stock","Cypress by tester stock"
"TC_02","postman by tester stock","rest assured by tester stock"
```

In `tests/dataDrivenTestingCsv.spec.js`:

```js
import fs from 'fs';
import path from 'path';
import { parse } from 'csv-parse/sync';

const records = parse(fs.readFileSync(path.join(__dirname, '../test-data/qa/testdata.csv')), {
  columns: true,
  skip_empty_lines: true,
});

for (const record of records) {
  test(`data driven csv ${record.testCaseID}`, async ({ page }) => {
    // navigate to google.com
    // fill with record.skill1 (or record.skill2)
    // press Enter
  });
}
```

The test runs once per CSV row and uses the chosen column. Switching the fill from `record.skill1` to `record.skill2` makes the test search with the alternate column values.

## Running tests on multiple environments

Create environment-specific data files: `test-data/qa/google.json` and `test-data/stage/google.json`, each with its own object name (`qaTestData` and `stageTestData`) and different keywords (e.g., qa: `playright by tester stock`; stage: `API testing by tester stock`, `specflow by tester stock`).

In `tests/readDataBasedOnEnvironment.spec.js`, import both files. Wrap tests in `test.describe('module one test', () => { ... })` and use `test.beforeAll('running before all test', async () => { ... })` to read `process.env.ENVIRONMENT`:

```js
let testData = null;
if (process.env.ENVIRONMENT === 'qa') {
  testData = qaTestData;
} else {
  testData = stageTestData;
}
```

Inside the test, fill with `testData.skill1` (or `.skill2`). Switch environments by editing `.env` (`ENVIRONMENT=qa` vs `ENVIRONMENT=stage`) — the test now picks data from the matching folder.

## Page Object Model (POM)

Why POM: hard-coded locators in 100 tests become a maintenance nightmare if the developer changes the DOM. POM is a design pattern that creates an object repository for web-page elements; each web page corresponds to a page class containing its locators and methods.

Advantages: cleaner, easier-to-understand code; object repository independent of test scripts; tests are optimized because abstraction methods live in the page classes.

Disadvantages: more time and effort up front (less later); the POM is project-specific.

A sample page object class includes the Playwright module, an exported class with a constructor that initializes the page object and declares all element locators, and abstraction methods that perform actions on those elements. A POM test imports the playwright module and the page classes, instantiates the page objects with `page` as the parameter, and calls the page methods.

Manual scenario for the demo: google.com → search "playright by tester stock" → press Enter → result page → click the "playright by tester stock" link → playlist page → click the first video.

Create `pages/homePage.js`, `pages/resultPage.js`, `pages/playlistPage.js`.

`homePage.js` skeleton:

```js
const { expect } = require('@playwright/test');

exports.homePage = class homePage {
  /** @param {import('@playwright/test').Page} page */
  constructor(page) {
    this.page = page;
    this.searchTextBox = page.locator('#<id>');
  }

  async goTo() {
    await this.page.goto('https://www.google.com');
  }

  async searchKeywords(searchKeyword) {
    await this.searchTextBox.click();
    await this.searchTextBox.fill(searchKeyword);
    await this.searchTextBox.press('Enter');
  }
};
```

`resultPage.js` is the same skeleton with `playlistLink = page.getByRole('link', { name: 'playright by tester stock' })` and a `clickOnPlaylist()` method that calls `.first().click()`.

`playlistPage.js` defines `videoLink = page.locator('#container #thumbnail')` (matching ~20 elements) and a `clickOnVideo()` method that does `.first().click()`.

The spec `tests/pageObjectTest.spec.js`:

```js
const { test } = require('@playwright/test');
const { homePage } = require('../pages/homePage');
const { resultPage } = require('../pages/resultPage');
const { playlistPage } = require('../pages/playlistPage');

test('page object model in playright', async ({ page }) => {
  const home = new homePage(page);
  await home.goTo();
  await home.searchKeywords('playright by tester stock');

  const result = new resultPage(page);
  await result.clickOnPlaylist();

  const playlist = new playlistPage(page);
  await playlist.clickOnVideo();

  await page.waitForTimeout(2000);
});
```

YouTube is heavy to load — additional waits or removing the `toBeEnabled` assertion may be needed for the video click to succeed.

## Video recording of test execution

Enable in `playwright.config.js` under `use`:

```js
video: {
  mode: 'retain-on-failure',  // or 'on-first-retry', or 'on'
  size: { width: 640, height: 480 }
}
```

Run a failing spec — the report's per-test view now shows a Video section in addition to errors, steps, screenshots, and traces. Setting `mode: 'on'` records every test (passing or failing) — the instructor demonstrates this with `pageObjectTest.spec.js` (after adding a 4-second wait to make it pass) and confirms the video attaches to the report.

## Maximizing the browser / setting viewport size

Two ways: change `playwright.config.js`, or set the viewport in code before navigation:

```js
await page.setViewportSize({ width: 1366, height: 728 });
await page.goto(...);
```

To find your screen's outer dimensions, open the browser console and type `outerWidth` and `outerHeight`. Re-run the spec — the browser opens at the specified size and runs full-screen.
