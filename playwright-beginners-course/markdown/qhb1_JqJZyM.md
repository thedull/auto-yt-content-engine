# Playwright with JavaScript Full Course | Beginner to Advanced

> **Source:** [Playwright with JavaScript Full Course | Beginner to Advanced](https://www.youtube.com/watch?v=qhb1_JqJZyM) — [Testing Funda by Zeeshan Asghar](https://www.youtube.com/@TestingFunda) · 2024-01-30 · 9:55:25
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A full ~10-hour Playwright + JavaScript course covering everything from installation through advanced patterns like API mocking, fixtures, Allure reporting, device emulation, and the Page Object Model.
- Walks through **Playwright** as Microsoft's modern end-to-end test framework: cross-browser (Chromium, WebKit, Firefox), cross-platform, multi-language, with auto-wait, web-first assertions, and powerful tooling (**Codegen**, **Inspector**, **Trace Viewer**).
- Covers core interactions in depth: locators (built-in, CSS, XPath, **Selector Hub**), radios/checkboxes, dropdowns, multi-select, autocomplete, file upload, basic auth, iframes (single and nested), broken images.
- Goes deep on assertions (**auto-retrying**, **non-auto-retrying**, **negating**, **soft**), annotations, grouping with `test.describe`, and data-driven testing using JSON.
- Full REST API automation chapter: **GET, POST, PUT, PATCH, DELETE**, plus **API chaining** and **API mocking**.
- Advanced wrap-up: **fixtures**, **Allure reports**, **device emulation**, **geolocation emulation**, and finally the **Page Object Model (POM)** design pattern.

## Introduction to Playwright

Hello everyone and welcome to this Playwright series. In this series we will be learning Playwright step by step, and this is the first video — an introduction to Playwright.

**Playwright** is very popular these days and is backed by **Microsoft**. To learn what it is, go to google.com, search for "playwright", and click the official website. You'll see the tagline: *"Playwright enables reliable end-to-end testing for modern web applications."* That means you can automate web applications end-to-end — both the UI and the APIs.

Playwright supports multiple languages. At the top of the docs you can choose **Node.js**, **Python**, **Java**, or **.NET**, and the documentation, API reference, community section, and official GitHub repo all switch to match. For example, switching to Python takes you to `microsoft/playwright-python`; switching back to Node.js takes you to the Node implementation.

You can also join the Playwright **Discord** from the home page. The Discord has help, videos, articles, and events. You can change the docs theme if you don't like dark mode, and there's a search box for any specific thing.

### Key features

- **Any browser, any platform, one API.** Cross-browser support including all Chromium browsers, WebKit, and Firefox. Cross-platform on Windows, Linux, and Mac. Multi-language support. You can also test mobile via native mobile emulation of Google Chrome for Android and Mobile Safari.
- **Resilient, no flaky tests.** Auto-wait and **web-first assertions** — assertions are created specifically for the dynamic web; checks are automatically retried until the necessary conditions are met.
- **Tracing** to debug failures.
- **No trade-offs, no limits.** Easy to work with multiple tabs, multiple origins, and multiple users in a single test. Easy event handling — hover elements, interact with dynamic controls. Handles different test frames like Shadow DOM with ease.
- **Full isolation, fast execution.** Browser contexts, login once, reuse.
- **Powerful tooling.** **Codegen** generates tests by recording your actions and saves them in any supported language. **Playwright Inspector** lets you inspect the page, generate locators, step through test execution, see click points, and explore execution logs. **Trace Viewer** captures everything to investigate why a test failed — screencasts, live DOM snapshots, action explorer, test source, and more.

To summarize: Playwright is by Microsoft, supports multiple languages, multiple browsers, has features like auto-wait, web-first assertions, tracing, multiple origins, multi-tab, and Shadow DOM support, and has powerful tooling like Codegen, Inspector, and Trace Viewer.

## Installing Playwright with JavaScript

In this tutorial we will install Playwright with JavaScript using different methods.

On the Playwright website, ensure **Node.js** is selected, then go to **Docs → Install Playwright**. You'll see different install commands: **npm**, **yarn**, and **pnpm**.

### Prerequisites

- **Node.js** — download from nodejs.org for your OS.
- An editor — this series uses **Visual Studio Code** from code.visualstudio.com, available for Windows 8/10/11, Linux, and Mac.

Verify Node is installed by opening a command prompt and running `node -v`. If Node is configured properly it will display the installed version. Verify npm with `npm -v`.

### Installing via npm init

Create a new folder on the desktop called `playwright install`. Open it in VS Code, then open the integrated terminal and run:

```
npm init playwright@latest
```

The installer asks several questions:

- TypeScript or JavaScript? Choose **JavaScript**.
- Where to put end-to-end tests? Default is `tests`.
- Add a GitHub Actions workflow? Optional.
- Install Playwright browsers? **Yes**.

It installs the framework plus Chromium, Firefox, and WebKit browsers, and creates a default project structure: `tests/` (with `example.spec.js`), `tests-examples/`, `playwright.config.js`, `package.json`, and `package-lock.json`.

### Installing into an existing project

If you already have a Node project and just want to add Playwright, run:

```
npm install -D @playwright/test
npx playwright install
```

The first command installs Playwright as a dev dependency; the second installs the browser binaries. You can then create your own `tests` folder and write spec files manually.

### Verifying the install

Open `package.json` to confirm `@playwright/test` appears under `devDependencies`. Open `playwright.config.js` — this is the central configuration file. Open the example test under `tests/example.spec.js` to see a sample.

## Running Playwright tests

In this tutorial we'll learn the different ways to run Playwright tests.

### Common run commands

- `npx playwright test` — run **all** tests.
- `npx playwright test <filename>` — run a **single** test file.
- `npx playwright test --project=chromium` — run only on Chromium.
- `npx playwright test --headed` — run in **headed** mode so you can see the browser.
- `npx playwright test --debug` — run in **debug** mode (opens Inspector).
- `npx playwright test --ui` — run in **UI mode**, an interactive runner introduced in newer versions.
- `npx playwright show-report` — open the HTML report after a run.

### Test report

After execution, Playwright prints a summary in the terminal showing how many tests passed across browsers (e.g. 6 passed for Chromium, Firefox, WebKit). Run `npx playwright show-report` to open the HTML report in the browser. Reports include each test, browser, duration, and screenshots/traces on failure.

### UI mode

UI mode (`--ui`) opens an interactive watch-mode runner. You can pick individual tests, see locators highlighted in real time, time-travel through actions, view network requests, and re-run on file change. This is one of the best ways to develop and debug tests.

## Generating tests with Codegen

In Playwright we can generate test scripts using **Codegen**, similar to Selenium IDE. The command is simple:

```
npx playwright codegen
```

For options run `npx playwright codegen --help`. You can pass a URL (`npx playwright codegen https://example.com`), pick a target browser (`--browser=firefox`), set viewport, set device emulation, save to a file (`-o test.spec.js`), or pick the language (`--target=javascript`).

When you run it, Playwright opens two windows: the browser to record actions in, and the **Inspector** which shows the generated code in real time. As you click, type, and navigate, the script is generated. When done, copy the code into your spec file.

## Playwright locators

Locators play a really important role when finding elements, and in Playwright they're especially important because of **auto-waiting and retrying**.

Common built-in locators:

- `page.getByRole(role)` — locate by ARIA role.
- `page.getByText(text)` — locate by visible text.
- `page.getByLabel(label)` — locate a form control by its associated label.
- `page.getByPlaceholder(placeholder)` — locate an input by its placeholder.
- `page.getByAltText(text)` — locate by alt text (typically images).
- `page.getByTitle(title)` — locate by `title` attribute.
- `page.getByTestId(id)` — locate by `data-testid`.

These built-in locators are recommended because they reflect what users see and are resilient to DOM changes. The official docs walk through each with examples.

## CSS and XPath locators (and Selector Hub)

You can also locate elements with **CSS** and **XPath** using `page.locator()`. For example:

```js
page.locator('css=button#submit')
page.locator('xpath=//button[@id="submit"]')
// or simply
page.locator('button#submit')      // CSS by default
page.locator('//button[@id="submit"]') // XPath if it starts with //
```

This tutorial also recommends the **Selector Hub** browser extension, which helps you build and verify CSS/XPath selectors directly on the page. Install the extension, open DevTools, and use the SelectorHub tab to test selectors live, see matches, and copy them into your test.

## Trace Viewer

**Trace Viewer** is a UI tool to explore recorded Playwright traces after execution.

A **trace** is a file that records all the actions your code took while interacting with the page — including DOM snapshots, screencasts, network requests, console logs, and source. To enable it, set `trace: 'on'` (or `'on-first-retry'`, `'retain-on-failure'`) in `playwright.config.js`.

After running tests, traces are saved under `test-results/`. Open one with:

```
npx playwright show-trace path/to/trace.zip
```

Inside the viewer you can scrub the timeline, see the page state before and after each action, inspect the action that was performed, and view network and console panes. This is the best tool for diagnosing flaky or failing tests.

## Handling radio buttons and checkboxes

This section uses the demoqa.com automation practice form (a student registration form) which has both radio buttons (Gender) and checkboxes (Hobbies).

- **Radio button**: only one option can be selected at a time. Locate it (e.g. `page.getByLabel('Male')`) and call `.check()`. Use `.isChecked()` to assert.
- **Checkbox**: multiple options can be selected. Same `.check()` / `.uncheck()` / `.isChecked()` API.

You can also iterate a group of checkboxes — locate all of them, loop, and check based on a condition.

## Handling dropdowns

Single-select dropdowns (`<select>`) are handled with `selectOption`. You can select by:

- **Value**: `page.locator('#dropdown').selectOption('value1')`
- **Label**: `page.locator('#dropdown').selectOption({ label: 'Option Text' })`
- **Index**: `page.locator('#dropdown').selectOption({ index: 2 })`

You can also enumerate options (`locator('option').allTextContents()`) for assertions.

## Multi-select dropdowns

For dropdowns with the `multiple` attribute you can pass an array to `selectOption`:

```js
await page.locator('#multi').selectOption(['value1', 'value2', 'value3'])
```

The tutorial walks through a demo practice site to verify each value gets selected.

## Autocomplete / autosuggest fields

Autocomplete is similar in spirit to a dropdown but the options appear dynamically as you type. Strategy:

1. Type into the input.
2. Wait for the suggestion list to appear.
3. Locate the suggestion you want and click it (often by text).

The tutorial demonstrates this on a practice website with a country autocomplete and shows multiple ways: clicking from the suggestion list, using keyboard navigation (`ArrowDown` then `Enter`), and matching by partial text.

## Uploading files

File upload is straightforward in Playwright. Use `setInputFiles` on a file `<input>`:

```js
await page.locator('input[type="file"]').setInputFiles('path/to/file.pdf')
// multiple files
await page.locator('input[type="file"]').setInputFiles(['file1.pdf', 'file2.pdf'])
// clear
await page.locator('input[type="file"]').setInputFiles([])
```

The Playwright docs under **Actions** show the official upload examples.

## Basic authentication

The tutorial uses the famous **the-internet.herokuapp.com** site, which has a basic authentication page where username and password are both `admin`.

Multiple ways to handle basic auth:

1. **Pass credentials in the URL**: `https://admin:admin@the-internet.herokuapp.com/basic_auth` — works for quick checks but exposes credentials.
2. **`httpCredentials` in `playwright.config.js`** — set `use: { httpCredentials: { username: 'admin', password: 'admin' } }`. Cleaner and reusable.
3. **`browser.newContext({ httpCredentials: ... })`** — set per-context in code.

## Handling iframes

To interact with iframe content, locate the frame first with `frameLocator`, then locate elements inside:

```js
const frame = page.frameLocator('#frame-id')
await frame.locator('h1').textContent()
```

The tutorial demonstrates on the-internet.herokuapp.com `/iframe` page.

## Nested iframes

For nested iframes, chain `frameLocator` calls:

```js
const outer = page.frameLocator('#outer-frame')
const inner = outer.frameLocator('#inner-frame')
await inner.locator('button').click()
```

This walks through a demo with frames inside frames, proving how chaining handles arbitrary depth.

## Finding broken images

Broken images are an SEO and UX problem. The tutorial uses the-internet.herokuapp.com `/broken_images` page.

The approach: listen to network responses and flag any image whose response status is `>= 400`. Alternative: query all `<img>` and check `naturalWidth === 0` for each:

```js
await page.evaluate(() => {
  return [...document.images].filter(img => !img.naturalWidth).map(img => img.src)
})
```

You can then assert on the count of broken images.

## Annotations

**Annotations** in Playwright let you mark tests with metadata and modifiers:

- `test.skip()` — skip a test (conditionally or unconditionally).
- `test.fail()` — mark as expected to fail.
- `test.fixme()` — mark as known broken; will be skipped.
- `test.slow()` — triple the default timeout for slow tests.
- `test.only()` — run only this test (useful while developing).

These can be applied per test or per `describe`. The official docs at playwright.dev list all annotations under the test API.

## Negating and soft assertions

Assertions are essential for verifying functionality. Previous tutorials covered **auto-retrying** assertions (web-first like `expect(locator).toBeVisible()`) and **non-auto-retrying** assertions (`expect(value).toBe(...)`). Two more types:

- **Negating assertions**: `expect(locator).not.toBeVisible()` — assert the opposite. Available on essentially every matcher via `.not`.
- **Soft assertions**: `expect.soft(locator).toBeVisible()` — failures don't stop the test, so you can collect multiple failures in one run. The test still fails at the end, but you see all the issues at once.

Use soft assertions when you want a complete picture of what's broken; use hard assertions when later steps depend on the assertion holding.

## REST API: GET method

Playwright can automate and test REST APIs directly without a browser. This section uses a demo API site.

```js
import { test, expect } from '@playwright/test'

test('GET request', async ({ request }) => {
  const response = await request.get('https://api.example.com/users/1')
  expect(response.status()).toBe(200)
  const body = await response.json()
  expect(body.id).toBe(1)
})
```

Key APIs: `request.get(url)`, `response.status()`, `response.ok()`, `response.json()`, `response.text()`, `response.headers()`.

## REST API: POST method

POST differs from GET because you usually need to send headers and a body:

```js
test('POST request', async ({ request }) => {
  const response = await request.post('https://api.example.com/users', {
    headers: { 'Content-Type': 'application/json' },
    data: { name: 'John', job: 'tester' }
  })
  expect(response.status()).toBe(201)
  const body = await response.json()
  expect(body.name).toBe('John')
})
```

You assert the status code (201 Created for resources) and then validate fields in the response body.

## REST API: PUT method

PUT updates an existing record. Same shape as POST but a different verb and the URL targets a specific resource:

```js
const response = await request.put('https://api.example.com/users/2', {
  data: { name: 'Jane', job: 'lead' }
})
expect(response.status()).toBe(200)
```

## REST API: PATCH method

PATCH is similar to PUT — both update a record — but PATCH is for **partial** updates while PUT replaces the entire record.

```js
const response = await request.patch('https://api.example.com/users/2', {
  data: { job: 'manager' }
})
expect(response.status()).toBe(200)
```

## REST API: DELETE method

DELETE removes a record. The expected status is typically 204 No Content:

```js
const response = await request.delete('https://api.example.com/users/2')
expect(response.status()).toBe(204)
```

## API chaining

**API chaining** means extracting a value from one API response and passing it to subsequent APIs. Real-world example: create a user with POST, capture the returned `id`, then GET/PUT/DELETE that user using the captured id.

```js
test('chain', async ({ request }) => {
  const created = await request.post('/users', { data: { name: 'A' } })
  const { id } = await created.json()

  const fetched = await request.get(`/users/${id}`)
  expect(fetched.status()).toBe(200)

  await request.delete(`/users/${id}`)
})
```

## API mocking

**API mocking** (also called API virtualization) is a software technique that simulates the behavior of an actual API. Why mock?

- The real API isn't ready or is unstable.
- You need predictable test data.
- You want to test edge cases (errors, timeouts) the real API rarely produces.
- You want to isolate the frontend from backend flakiness.

Playwright mocks via `page.route()`:

```js
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Mocked' }])
  })
})
```

Any request matching the pattern is intercepted and the fulfillment is returned to the page instead of hitting the network.

## Data-driven testing with JSON

**Data-driven testing** (data parameterization) means running the same test with multiple sets of data — for example, registering with many username/password combinations.

Approach: keep test data in a JSON file (e.g. `data/users.json`), import it, and loop through the entries inside a `test.describe`:

```js
import data from '../data/users.json'

for (const entry of data) {
  test(`register ${entry.username}`, async ({ page }) => {
    await page.goto('/register')
    await page.getByLabel('Username').fill(entry.username)
    await page.getByLabel('Password').fill(entry.password)
    await page.getByRole('button', { name: 'Register' }).click()
    await expect(page.getByText('Success')).toBeVisible()
  })
}
```

Each entry generates a separate, independent test in the report.

## Fixtures

**Fixtures** make automation easier and smoother. The analogy: imagine building a house — fixtures are like the pre-built walls and floors. They provide everything you need to get started quickly without worrying about the fundamentals.

In Playwright, fixtures provide test setup/teardown logic that's reusable across tests. Built-in fixtures include `page`, `browser`, `context`, `request`. You can define custom fixtures:

```js
import { test as base } from '@playwright/test'

export const test = base.extend({
  loggedInPage: async ({ page }, use) => {
    await page.goto('/login')
    await page.getByLabel('Username').fill('admin')
    await page.getByLabel('Password').fill('admin')
    await page.getByRole('button', { name: 'Sign in' }).click()
    await use(page)
    // teardown after the test
  }
})
```

Now any test that needs `loggedInPage` gets a pre-authenticated page. This eliminates duplicated login code across tests.

## Grouping tests with test.describe

So far each test has been independent. Imagine thousands of test cases scattered across a codebase — sorting through them is painful. **`test.describe`** groups related tests together:

```js
test.describe('User registration', () => {
  test('valid data', async ({ page }) => { /* ... */ })
  test('invalid email', async ({ page }) => { /* ... */ })
  test('weak password', async ({ page }) => { /* ... */ })
})
```

Benefits: cleaner reports (tests show under their group), shared `beforeAll`/`beforeEach` hooks scoped to the group, and the ability to run only one group with the `--grep` filter.

## Grouping tests by tag / file

Beyond `describe`, you can also group by:

- **File**: keep related tests in one spec file.
- **Tag in title**: `test('@smoke logs in', ...)` then run `npx playwright test --grep @smoke`.
- **Project** in `playwright.config.js`: define multiple projects (e.g. `smoke`, `regression`) each with their own `testMatch` glob, and run a project with `--project=smoke`.

The tutorial walks through configuring projects in `playwright.config.js` so that the same test file can be reused across browsers or environments.

## Allure reports

**Allure** reports are very popular and give richer visualization than the default Playwright HTML report. They show test history, severity, categories, attachments, steps, and trends.

Setup:

```
npm install -D @playwright/test allure-playwright
```

In `playwright.config.js`:

```js
reporter: [['line'], ['allure-playwright']]
```

Run tests, then generate and open the report:

```
npx playwright test
allure generate ./allure-results --clean
allure open
```

You'll need the Allure command-line tool installed (via Scoop on Windows, Homebrew on Mac, or npm). The report shows a dashboard, suites, graphs, behaviors, packages, and timeline views.

## Device emulation

Playwright can emulate mobile devices — viewport, user agent, touch, and more — via the `devices` import:

```js
import { devices } from '@playwright/test'

export default defineConfig({
  projects: [
    { name: 'iPhone 13', use: { ...devices['iPhone 13'] } },
    { name: 'Pixel 5',   use: { ...devices['Pixel 5'] } }
  ]
})
```

Run the project to test mobile rendering and touch behavior. The full device list is in the Playwright docs.

## Geolocation emulation

In addition to devices you can emulate **geolocation**. Useful when your app's behavior depends on location.

```js
use: {
  geolocation: { longitude: 12.4924, latitude: 41.8902 },  // Rome
  permissions: ['geolocation']
}
```

You can also set timezone (`timezoneId: 'Europe/Rome'`) and locale (`locale: 'it-IT'`). The tutorial demonstrates by visiting a maps page and confirming the emulated location is recognized.

## Page Object Model (POM)

The **Page Object Model** is a design pattern for organizing test code. Without it, login (or any common flow) gets repeated across many tests — and if the login UI changes, you have to update every test. This is the classic problem of **maintainability** and **code duplication**.

POM solves this by:

1. Creating a **page class** for each page (e.g. `LoginPage`) that holds locators and action methods.
2. Tests instantiate the page class and call methods (e.g. `loginPage.login(user, pass)`) instead of repeating selector code.

Example structure:

```
project/
├── pages/
│   └── login.page.js
└── tests/
    └── login.pom.spec.js
```

`pages/login.page.js`:

```js
export class LoginPage {
  constructor(page) {
    this.page = page
    this.username = page.getByLabel('Username')
    this.password = page.getByLabel('Password')
    this.submit   = page.getByRole('button', { name: 'Sign in' })
  }

  async goto(url) { await this.page.goto(url) }

  async login(user, pass) {
    await this.username.fill(user)
    await this.password.fill(pass)
    await this.submit.click()
  }
}
```

`tests/login.pom.spec.js`:

```js
import { test } from '@playwright/test'
import { LoginPage } from '../pages/login.page'

test('login works', async ({ page }) => {
  const loginPage = new LoginPage(page)
  await loginPage.goto('https://example.com/login')
  await loginPage.login('admin', 'admin')
})
```

Now if the login page changes, you update `LoginPage` once, and every test that uses it benefits. This is the foundation of maintainable test suites — tests describe **what** they do; page objects encapsulate **how**.

That's the end of the course. Each tutorial built on the previous one, taking you from installing Playwright through advanced patterns like API mocking, fixtures, Allure reporting, and the Page Object Model.
