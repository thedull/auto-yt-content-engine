# #1 Playwright Automation Using TypeScript Full Course 2026 | Playwright TypeScript Beginner Tutorial

> **Source:** [#1 Playwright Automation Using TypeScript Full Course 2026 | Playwright TypeScript Beginner Tutorial](https://www.youtube.com/watch?v=788GvvcfwTY) — [Testers Talk](https://www.youtube.com/@testerstalk) · 2025-01-08 · 8:55:10
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- An end-to-end Playwright + TypeScript course by **Bakkappa N (Testers Talk)** that takes you from zero install through advanced runner features such as parallelism, retries, multiple reporters, and Allure integration.
- Chapter 1 covers what Playwright is, its architecture (client + Node.js server, CDP + WebSocket), comparisons with Cypress and Selenium, install via VS Code extension or `npm init playwright@latest`, default folder structure, headed vs headless modes, the Test Explorer, recording with **Codegen** and the **Record Cursor**, and writing your first test.
- Chapter 2 dives into capturing screenshots (element/page/full-page), all locator strategies (`getByRole`, `getByLabel`, `getByAltText`, `getByTestId`, `getByText`, `getByPlaceholder`, `getByTitle`, XPath, CSS), hooks (`beforeAll`/`beforeEach`/`afterAll`/`afterEach`), drop-downs, iframes, drag-and-drop, mouse and keyboard actions, date pickers, hard vs soft assertions, watch mode, the Playwright UI, and Trace Viewer.
- Chapter 3 covers test annotations (`skip`, `only`), grouping with `describe`, tagging, repeating tests, automatic retries, parameterizing tests with `for…of`, visual comparison with `toHaveScreenshot`, and timeouts (test, assertion, action, global).
- Chapter 4 covers the `tsconfig.json` setup, multiple browser contexts/tabs, rerunning only failed tests with `--last-failed`, handling alerts/confirms/prompts via `page.once('dialog', …)`, generating JSON/JUnit/list/dot/Allure reports, video recording, parallel execution, text/attribute extraction, iterating matching elements, and working with checkboxes and radio buttons.
- The course closes by previewing Chapter 5 (data-driven testing with JSON/Excel/CSV, Page Object Model, fixtures, viewports, multiple environments), and all source code is published in the speaker's GitHub repo `playwright-typescript-tutorial-full-course`.

## Course introduction

Hi friends, this is **Bakkappa N (Testers Talk)**. In this Playwright with TypeScript full course, we will deep-dive into the powerful end-to-end testing framework and you will learn how to leverage Playwright to write robust, clean, and scalable tests for your application. The course takes you from setting up the Playwright + TypeScript test automation environment from scratch to the advanced level. Each topic is illustrated with an example, and the code is available in the GitHub repository. By the end you will be able to build and maintain a Playwright automation framework and write efficient end-to-end tests for your web applications.

---

# Chapter 1 — Playwright fundamentals and setup

This chapter covers what Playwright is, its architecture, the differences between Playwright, Cypress, and Selenium, environment setup, writing the first test, debugging, running, checking the test report, and using Codegen to record and play tests.

## What is Playwright?

**Playwright** is an open-source automation testing tool/library used to test end-to-end modern web applications and mobile applications in headed or headless mode, and you can also test APIs with it.

### Advantages

- **Cross-browser testing** — Chrome, Edge, Chromium, Firefox, WebKit (Safari).
- **Cross-platform testing** — Windows, Linux, macOS.
- **Cross-language support** — TypeScript, JavaScript, Python, .NET, Java.
- **Mobile web emulation** — by setting the viewport you can run mobile-web tests in Chrome or Safari.
- **Automatic waiting** — Playwright waits until an element is visible/enabled before performing the action.
- **Trace Viewer** — captures live DOM, per-step screenshots, and a video of the run for failure analysis.
- **Reports** — HTML report by default plus many other formats.
- **Parallel execution** — built-in.
- **No trade-off, no limit** — same-origin and multi-domain workflows both supported.
- **Dynamic wait assertions** — assertions auto-wait until expected text/element appears.
- **Faster and reliable** — much faster than Selenium/Cypress and stable across repeated runs.
- **State saving** — log in once, reuse the storage state across tests.
- **Powerful tooling** — **Codegen** records actions into TypeScript/JS/Python/.NET/Java; **Playwright Inspector** identifies locators; **Trace Viewer** investigates failures.
- **No flaky tests**, thanks to auto-waits and dynamic assertions.

### Limitations

- High **resource consumption** when running parallel tests on limited hardware.
- No support for **desktop application** automation.
- No support for **legacy browsers** like Internet Explorer.
- Smaller community compared to Selenium WebDriver (Playwright is ~5 years old; Selenium has been around for 20).

## Playwright architecture

Two components: the **client** (your test code in TypeScript/JS/Python/.NET/Java) and the **Playwright Node.js server**. The client serializes test commands to JSON and sends them over the **WebSocket** protocol to the server. The server then talks to the browser engines using the **Chrome DevTools Protocol (CDP)** for Chromium-based browsers (and equivalent protocols for Firefox/WebKit). Test execution results flow back to the client.

## Playwright vs Cypress vs Selenium

| Feature | Playwright | Cypress | Selenium |
| --- | --- | --- | --- |
| Setup complexity | Easy with JS/TS | Simple, fast (JS only) | High (pom.xml deps) |
| Languages | TS, JS, Python, .NET, Java | TS, JS only | Java, Python, JS, .NET, Ruby, PHP (no TS) |
| Speed | Very fast, headless + parallel by default | Fast but runs inside the browser | Slow, more flaky |
| Browsers | Chromium, Chrome, Edge, Firefox, WebKit | Chrome, Edge, Electron | Most browsers |
| Parallel | Built-in | Plugins required | TestNG + Selenium Grid |
| Debugging | Detailed (Trace Viewer) | Detailed | Limited |
| Cross-browser | Full | No Firefox/Safari | Full |
| Community | Rapidly growing | Strong (esp. JS) | Largest, most mature |

## Software prerequisites

Mandatory: an OS, **Node.js**, and **VS Code** (TypeScript needs no separate install). For repos and CI/CD you'll also use **Git/GitHub**. The course later uses **Postman** for manual API testing, the Playwright API for automation, and **Android Studio** for mobile app testing.

## Installing Node.js and VS Code

Download Node.js from `nodejs.org` (pre-built installer matching your OS/architecture). Verify with `node -v` in your terminal — Bakkappa is on Node 22.10.0. Install VS Code from `code.visualstudio.com` and accept the defaults.

## Installing Playwright in VS Code

1. Install the **Playwright Test for VSCode** extension from Microsoft.
2. Open an empty folder.
3. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) and run **Install Playwright**.
4. Choose browsers (Chromium, Firefox, WebKit), language (TypeScript), and untick the GitHub Actions option for now. The terminal downloads the browser binaries; "Happy hacking" means you're done. Note the printed important commands for daily use.

## Default folder structure

- `node_modules` — dependencies and inbuilt JS/TS files.
- `tests/` and `tests-examples/` — `*.spec.ts` files; each spec contains one or more `test(...)` blocks.
- `.gitignore` — Microsoft pre-fills folders that should not be committed.
- `package.json` — metadata, dependencies, and runnable scripts.
- `package-lock.json` — exact dependency tree, versions, and download URLs (generated by `npm`).
- `playwright.config.ts` — central config: `testDir`, `retries`, `workers`, `reporter`, `projects`, etc. The `projects` array determines which browsers each test runs against (by default each test runs once per project).

## Test Explorer

In VS Code's testing icon you can run individual tests, run a whole spec, or run everything; debug with breakpoints; filter by status (only failing, only executed); and use fuzzy match on titles. Clearing results and collapsing the tree are first-class actions.

## Setting up via the command line

Create an empty folder, open a terminal there, and run `npm init playwright@latest`. It asks for language (TypeScript), tests folder name (default `tests`), GitHub Actions (yes/no), and whether to install browsers. With three projects enabled by default, Playwright runs the default two example tests across Chromium/Firefox/WebKit (six total runs).

## Recording your first test

In Test Explorer expand **Playwright** and click **Record new**. Playwright opens a browser plus a generated spec. Navigate to `github.com`, click sign in, type a fake username/password, click **Sign in**, and use the **`ab`** assert icon to validate the "incorrect username or password" message. The generated code is saved as `test-1.spec.ts`; rename it (e.g. `record_test.spec.ts`) and run it.

## Running on different browsers

In Test Explorer pick the **chromium**, **firefox**, **webkit**, **Google Chrome** (branded), or **Microsoft Edge** project. To use the branded browsers, comment out the default `chromium`/`firefox`/`webkit` blocks in `playwright.config.ts` and uncomment the desktop Chrome/Edge entries. The HTML report shows which project each run used.

## Generating a readable HTML report with steps

Wrap each phase of the test in `await test.step('navigating to URL', async () => { … })`. The HTML report then shows step names plus the underlying Playwright commands per step, which makes failure triage immediate. Intentionally failing the validation step demonstrates how the report pinpoints the failing step.

## Common terminology — async / await / test / page / expect

- `async` makes a function asynchronous; only inside an async function can you use `await`.
- `await` waits for a returned **promise** to resolve (success value) or reject (exception).
- `test` is a function that defines a single test case; it accepts a title and an async callback.
- `page` is the **browser page** object — your handle for navigation and interactions (`page.goto`, `page.click`, `page.fill`, …).
- `expect` is the assertion API — compare actual page state to expected text, titles, counts, visibility, etc.

## Writing your first test

Manual scenario: open Google → search "playright by tester stock" → click the first playlist link → assert the page title contains "YouTube". Steps in code:

1. Create `tests/chapter 1/02_first_test.spec.ts`.
2. `import { test, expect } from '@playwright/test';`.
3. `test('my first playright typescript test', async ({ page }) => { … });`.
4. `await page.goto('https://www.google.com/');`.
5. Use **Pick locator** (Test Explorer → Pick locator) to grab the search box selector, then `await page.getByLabel('Search').fill('playright by testers talk');`.
6. `await page.getByLabel('Search').press('Enter');`.
7. Click the first result link with `await page.getByRole('link', { name: 'playright by testers talk' }).first().click();`.
8. Assert with `await expect(page).toHaveTitle('YouTube');`.

The HTML report breaks down the run by step, shows which browser was used, and shows per-step duration.

## Record Cursor — adding new actions inside an existing test

Place the cursor where you want to insert actions and click **Record at cursor**. The opened browser lets you click web elements while Playwright generates `assertVisibility` / `assertText` calls based on the icons it overlays (eye-with-tick, `ab`, etc.). Generated assertions like `await expect(page.getByLabel('…')).toBeVisible();` and `…toContainText('…')` get inserted at the cursor.

## Running specific spec files and headed/headless

`npx playwright test tests/chapter\ 1/02_first_test.spec.ts` runs a single file. `npx playwright test tests-examples/example.spec.ts` runs the example. To toggle headed/headless globally, set `use: { headless: true | false }` in `playwright.config.ts`. Override per project from CLI by appending `--project=chromium|firefox|"Microsoft Edge"|"Google Chrome"`.

## Codegen

Run `npx playwright codegen`. Playwright opens both a browser and the **Playwright Inspector**. Every action you take in the browser becomes generated code in the inspector — including assertions added through the on-page icons. The inspector can also convert the generated code into other languages (JavaScript, Python, .NET, Java) or other test runners (Library, Pytest, etc.). Copy the code, paste it into a new spec file (e.g. `04_codegen_test.spec.ts`), give the test a meaningful title, and run.

---

# Chapter 2 — Locators, assertions, hooks, and runner features

Bakkappa describes Chapter 2 as covering screenshots, locator strategies, hard/soft assertions, hooks, Trace Viewer, watch mode, keyboard and mouse actions, and many more topics.

## Capturing screenshots

Three flavors:

- **Element**: `await page.locator('#elementId').screenshot({ path: './screenshots/element-screenshot.png' });`
- **Current visible page**: `await page.screenshot({ path: './screenshots/page-screenshot.png' });`
- **Full page**: `await page.screenshot({ path: './screenshots/full-page-screenshot.png', fullPage: true });`

Files appear under the `screenshots/` folder you create in the project root. You can also use `.jpeg` extensions.

## Adding screenshots to the HTML report

Set `use: { screenshot: 'on' | 'off' | 'only-on-failure' | 'on-first-retry' }` in `playwright.config.ts`. With `'only-on-failure'`, screenshots and an **errors** plus **screenshots** section appear only when a test fails. With `'on'`, every passing test gets a screenshot in its report.

## Locator strategies

Playwright supports many locator types — pick the most semantic one available:

- `page.getByRole('link' | 'button' | …, { name: '…' })`
- `page.getByLabel('Homepage', { exact: true }).first()` — uses `aria-label`/labels.
- `page.getByAltText('webuck full sized avatar')` — primarily for images via the `alt` attribute.
- `page.getByTestId('repositories')` — uses a custom attribute configured by `use: { testIdAttribute: 'data-tab-item' }` in `playwright.config.ts`.
- `page.getByText('Sign up')`.
- `page.getByPlaceholder('search')`.
- `page.locator('//input[@name="q"]')` for **XPath** (start with `//`) and `page.locator('input[name="q"]')` for **CSS selectors**.
- `page.getByTitle('Search')` when the element has a `title` attribute.

The instructor recommends his Medium articles (`medium.com/@testerstalk`) for deeper coverage of XPath/CSS.

## Hooks (precondition / postcondition setup)

Hooks are special functions that run before/after tests, ideal for preconditions (creating test data, opening DB connections) and cleanup. Four hooks:

- `test.beforeAll(async () => { … })` — once before any test in the file.
- `test.beforeEach(async ({ page }) => { … })` — before every test.
- `test.afterEach(async () => { … })` — after every test.
- `test.afterAll(async () => { … })` — once after all tests.

Order of execution for a two-test file: `beforeAll` → `beforeEach` → test1 → `afterEach` → `beforeEach` → test2 → `afterEach` → `afterAll`. Common pattern: move `await page.goto(URL)` into `beforeEach` instead of repeating it in each test.

## Drop-down lists

Use the `<select>` tag's `selectOption` method:

- By value attribute: `await page.getByLabel('Month').selectOption('3');`
- By visible text: `…selectOption('Aug');` (matches by leading characters).
- Validate all options: `await expect(page.locator('#month > option')).toHaveText(['Jan', 'Feb', …]);`. Adding an option that doesn't exist in the DOM (e.g. `'Playright'`) demonstrates the failure path.

## iframes and drag-and-drop

For elements inside an iframe, switch with `const iframe = page.frameLocator('.demo-frame');`, then use `iframe.locator('#draggable')`. To drag-and-drop:

```ts
const dragElement = iframe.locator('#draggable');
const dropElement = iframe.locator('#droppable');
await dragElement.dragTo(dropElement);
```

Without `frameLocator`, the test fails with a timeout because the elements are not in the top-level DOM.

## Mouse actions

After identifying an element, call `.click({ button: 'left' | 'middle' | 'right' })` for left/middle/right click. **Left** clicks the link, **middle** opens it in a new tab, **right** opens the context menu. Other actions: `.hover()` to mouse over, and `.dblclick()` for double-click (technically a click action, included for completeness). For repeated locators that match multiple elements, suffix `.first()` to avoid the strict-mode violation.

## Keyboard actions

For element-focused keys: `await element.press('Enter')`. For document-level keys: `await page.keyboard.press('Meta+A')` (macOS) or `'Control+A'` (Windows) to select all, then `await page.keyboard.press('Delete')`. The `press` method accepts every standard key name (Enter, Tab, Delete, PageUp, PageDown, etc.).

## Date picker

Hard-coded value: `await iframe.locator('#datepicker').fill('12/15/2024');`. To select today, click the input and target `.ui-datepicker-today`. To pick a past date, click `[title="Prev"]` then `text="15"`; for future dates, click `[title="Next"]` first.

## Assertions — hard vs soft

Hard assertions stop execution on failure; soft assertions keep going and report all failures at the end. To convert hard to soft, replace `expect(x)` with `expect.soft(x)`.

### Stability assertions

- `await expect(locator).toBeVisible();`
- `…toBeEditable();`
- `…toBeEnabled();`
- `…toBeEmpty();`
- `…toBeDisabled();`

### Value assertions

- `await expect(page).toHaveURL('https://…');`
- `await expect(page).toHaveTitle('YouTube');`
- `await expect(page.locator('span[id=title]').first()).toHaveText('Expected text');`
- `await expect(page.locator('span[id=title]')).toHaveCount(4);`

The instructor's Medium page lists more variants and edge cases.

## Watch mode

A simple toggle in Test Explorer (project-, spec-, or test-level) that re-runs the relevant tests automatically when you save the file — useful while iterating on a single test.

## Playwright UI

`npx playwright test --ui` opens a richer UI than Test Explorer. It shows captured frames at the top, an actions list on the left, and tabs on the right for **screenshots (before/after)**, **metadata** (duration, browser, viewport, action/event counts), **locator** picker (almost-live DOM), **source**, **call** (parameters), **log**, **errors**, **console**, **network**, and **attachments**. Filter by title or tag, run/stop everything, and toggle watch mode at any granularity.

## Trace Viewer

Enable with `use: { trace: 'on' | 'off' | 'on-first-retry' | 'on-first-failure' }` in `playwright.config.ts`. When traces are captured, the HTML report shows a third section ("traces") that opens a window equivalent to Playwright UI — same actions/metadata/before-after/log/console/network tabs. The "before/after" panes are an interactive snapshot of the DOM, not a flat image — you can hover and pick locators inside them.

---

# Chapter 3 — Annotations, grouping, tags, retries, parameterization, visual testing, timeouts

This chapter introduces annotations, grouping, tagging, repeat/retry execution, parameterizing tests, visual testing, and timeouts.

## Annotations: skip and only

`test.skip('test 1', …)` skips a test (deprecated, known bug, etc.). `test.only('test 3', …)` runs *only* that test in the file. Output confirms with "1 skipped, 1 passed" or runs only the marked test.

## Grouping tests with `describe`

```ts
test.describe('smoke testing', () => {
  test('test 1', async ({ page }) => { … });
});
test.describe('regression testing', () => {
  test('test 2', async ({ page }) => { … });
  test('test 3', async ({ page }) => { … });
});
```

Run a group from Test Explorer by clicking its play arrow.

## Tags

Add an options object after the title:

```ts
test('my first playright typescript test 1', { tag: ['@smoke testing'] }, async ({ page }) => { … });
test('my first playright typescript test 2', { tag: ['@smoke testing', '@regression testing'] }, async ({ page }) => { … });
```

Run by tag with `npx playwright test --grep "@smoke testing"` or `--grep "@regression testing"`.

## Repeating the same test

`npx playwright test tests/chapter\ 1/02_first_test.spec.ts --repeat-each=3` runs each test 3 times (10 tests × 3 = 30 runs). With multiple workers, executions happen in parallel.

## Retries

Set `retries: [ciCount, localCount]` in `playwright.config.ts` (e.g. `retries: 2` for one parameter, or two-element handling for CI vs local). After a failure, the HTML report adds a separate **retry** tab per attempt with full logs.

## Parameterizing tests

```ts
const searchKeywords = ['playright by testers talk', 'cypress by testers talk', 'API testing by testers talk'];
for (const searchKeyword of searchKeywords) {
  test(`parameterize tests in playright ${searchKeyword}`, async ({ page }) => {
    await page.goto('https://www.google.com');
    await page.getByLabel('Search').fill(searchKeyword);
    await page.getByLabel('Search').press('Enter');
    await page.getByRole('link', { name: searchKeyword }).first().click();
    await expect(page).toHaveTitle(new RegExp(searchKeyword));
  });
}
```

The HTML report lists three runs, one per keyword.

## Visual testing

Use `await expect(page).toHaveScreenshot('github-login-page.png');` for the page or `await expect(element).toHaveScreenshot('github-login-form.png');` for an element. **First run always fails** with "snapshot does not exist" — Playwright generates the baseline under `<spec>-snapshots/`. Re-run to pass. If actual and expected differ (e.g. user typed into a field), the report adds an **image mismatch** section with side-by-side screenshots and a diff overlay highlighting the changes.

## Timeouts

Frequently used timeouts in `playwright.config.ts`:

- `timeout: 60_000` — global per-test timeout.
- `expect: { timeout: 10_000 }` — global assertion timeout.
- `use: { actionTimeout: 10_000 }` — per-action timeout.
- `globalTimeout: 60 * 60 * 1000` — total suite timeout (e.g. 1 hour).

Per-test override: `test.setTimeout(60_000)` inside the test (overrides the global). Per-assertion override: `await expect(page).toHaveTitle('YouTube', { timeout: 5_000 });`. Per-action override: `await page.getByRole('link', { name: '…' }).click({ timeout: 5_000 });`. Failures surface as `Test timeout of 60000ms exceeded` or `Timed out 10000ms waiting for expect(…)`.

---

# Chapter 4 — `tsconfig`, multi-browser, alerts, reporting, parallelism, attributes, iteration, checkboxes

This chapter covers the TypeScript config, multiple browser sessions, rerunning failed tests, alerts/popups, reporters, parallel execution, and checkbox/radio handling.

## `tsconfig.json`

Not strictly required, but recommended when using TypeScript. It centralizes compiler options (`target`, `strict`), file/dir include/exclude lists (e.g. include `src` and `tests`), and integrates cleanly with build tools like webpack. Improves IDE features (type-checking, autocomplete, error reporting). Create it in the project root and add a sibling `src/` folder for shared code (page objects, data-driven helpers, etc.) — the spec files stay under `tests/`.

## Multiple browser sessions / tabs

The default `page` is one tab in one browser context. To open a separate session:

```ts
const context = await browser.newContext();
const page2 = await context.newPage();
await page2.goto('https://www.google.com/');
// new tab in the SAME context:
const newTab = await context.newPage();
await newTab.goto('https://www.google.com/');
```

The test signature receives `({ page, browser })`. Each `newContext` gives an isolated session; each `newPage` on a context is a tab in that session.

## Rerun only failed tests

Playwright records `test-results/.last-run.json`. After a failed run, `npx playwright test --last-failed` reruns only the previously failing tests.

## Alerts, confirms, and prompts

By default Playwright auto-dismisses dialogs. Use `page.once('dialog', dialog => …)` to handle them:

```ts
page.once('dialog', dialog => {
  console.log(`alert message is ${dialog.message()}`);
  console.log(`dialog type is ${dialog.type()}`);
  dialog.accept();          // OK; .dismiss() for Cancel
});
await page.getByText('See an example alert', { exact: true }).click();
```

For prompts, use the async listener form to type into the prompt before accepting:

```ts
page.once('dialog', async dialog => {
  console.log(dialog.message());
  await dialog.accept('Playwright');
});
```

`dialog.type()` returns `'alert' | 'confirm' | 'prompt'`.

## Reporters

In `playwright.config.ts` set `reporter: [['html'], ['json', { outputFile: 'json-test-report.json' }], ['junit', { outputFile: 'junit-test-report.xml' }], ['list'], ['dot']]`. JSON shows nested `suites` matching your `describe` groups. JUnit XML lists each spec under `testsuite` with timestamp, browser, totals, durations, and full stack traces — useful for CI pipelines. `list` prints per-test status with duration in the console; `dot` prints `.` for pass, `F` for fail.

## Allure report

Two extra plugins: `npm install --save-dev allure-commandline` and `npm install --save-dev allure-playwright`. Add `'allure-playwright'` to the `reporter` array. After running tests, an `allure-results/` folder appears. Run `allure generate allure-results --clean` (creates `allure-report/`) and then `allure open` to view. The report shows pass/fail percentages with color coding, suites grouped by browser → spec → describe → test, attached traces, screenshots, and recorded videos for each test (including failures).

## Video recording

Set `use: { video: 'on' | 'off' | 'on-first-retry' | 'retain-on-failure' }`. The video appears as an additional section in the HTML report after **traces** — playable inline.

## Parallel execution

Two knobs: `fullyParallel: true` and `workers: <n>` in `playwright.config.ts`. CLI override: `--workers=4`. With four workers, four browsers spawn simultaneously and four tests run at once — the dock/taskbar makes this visible.

## Get text and get attribute

- `const text = await page.locator('span[itemprop="name"]').textContent();` — alternatively `.innerText()`.
- Trim with `text.trim()`.
- Assert with `expect(finalName).toBe('testerstock');`.
- Read an attribute: `const value = await page.getByTestId('repositories').first().getAttribute('data-selected-links');` — the `testIdAttribute` is set via `playwright.config.ts`.

## Iterating over matching elements

Three approaches. The instructor's example: list each repo name on his GitHub profile.

1. **`for…of` with the `$$` array helper**:
   ```ts
   const repositoryLinks = await $$('span.repo');
   for (const repositoryLink of repositoryLinks) {
     const text = await repositoryLink.textContent();
     console.log(`Text from first loop: ${text}`);
   }
   ```
2. **Index-based `for` loop** using the same array and `[index].textContent()`.
3. **Locator + count + `nth(index)`**:
   ```ts
   const repositoryLinks2 = page.locator('span.repo');
   const count = await repositoryLinks2.count();
   for (let i = 0; i < count; i++) {
     const text = await repositoryLinks2.nth(i).textContent();
     console.log(`Text from third for loop: ${text}`);
   }
   ```

Each loop prints the same six repository names — pick the form that fits the surrounding code.

## Checkboxes and radio buttons

Same API for both. Inside an iframe (jQuery UI demo):

```ts
const iframe = page.frameLocator('iframe.demo-frame');
const radio = iframe.locator('label[for="radio-1"]');
await expect(radio).not.toBeChecked();
await radio.check();
await expect(radio).toBeChecked();
```

Use `.check()` to tick and `.uncheck()` to clear; `.toBeChecked()` for assertions, with `.not` for the negation.

---

# Chapter 5 preview — what's coming next

The course continues with: data-driven testing using **JSON**, **Excel**, and **CSV** files; implementing the **Page Object Model** design pattern; **fixtures**; setting **viewport size**; and running tests across **multiple environments**.

The full source code for every example shown is published in the speaker's GitHub repository, searchable as `playwright-typescript-tutorial-full-course` under `@testerstalk`.
