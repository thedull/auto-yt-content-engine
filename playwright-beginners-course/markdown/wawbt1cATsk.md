# Playwright with TypeScript: Learn Playwright Automation Tutorial from Scratch [6 Hours]

> **Source:** [Playwright with TypeScript : Learn Playwright Automation Tutorial from Scratch [6 Hours]](https://www.youtube.com/watch?v=wawbt1cATsk) — [TestMu AI (Formerly LambdaTest)](https://www.youtube.com/@TestMuAI) · 2022-09-01 · 5:41:27
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- Comprehensive multi-part Playwright + TypeScript course taught by Kaushik for LambdaTest, covering installation through cross-browser execution on the LambdaTest cloud grid.
- Walks through writing tests with the **Playwright Test Runner**: launching browsers, contexts, and pages; the codegen recorder; configuring **HTML/JSON/dot reporters**, screenshots, video, and retries; and the auto-wait mechanism.
- Demonstrates basic interactions (inputs, buttons, checkboxes), web-first **expect** assertions, alerts (JS and Bootstrap modals), dropdowns (`selectOption` + custom Bootstrap lists), frames (including nested) and multi-tab handling.
- Builds a date-picker handler using the **moment** library, a file upload/download workflow with `setInputFiles` and the `download` event, and ends with a **Page Object Model** refactor using **playwright fixtures** plus JSON test data.
- Final section integrates with **LambdaTest** cloud: `chromium.connect`, runtime capability modification per project, marking pass/fail via `evaluate`, and toggling between local and cloud execution from the same fixture.

## Installation and First Test

Hey guys, my name is Kaushik and welcome to LambdaTest. I am very excited to start a new series on **Playwright**. In this first video we will learn what Playwright is, how to set up VS Code, install Playwright, and execute the sample test script bundled with the Playwright setup.

**Playwright** is a Node.js library used to automate **Chromium**, **Firefox**, and **WebKit** with a single API. It is built to enable cross-browser web testing. WebKit is the browser engine developed by Apple and is used in Safari and the iOS web browser. Playwright by Microsoft is a fork of **Puppeteer** (a Node library that automates Chromium with a JavaScript API, mostly used by developers). By default Playwright runs in **headless** mode.

Playwright has many capabilities:

- Handles multiple pages, multiple domains, iframes, window/alert handling — everything is bundled within the API.
- Network interception for stubbing and mocking requests.
- Emulation of mobile devices, geolocations, and permissions (emulation only — we cannot run native Android or iOS apps, but we can connect a physical Android device and execute tests in the Android Chromium browser).
- Native input support: keyboard and mouse actions (drag-and-drop, hover, etc.) similar to Selenium's `Actions` class.
- Upload and download of any kind of file.
- Component-based testing (added in version 1.22).
- Its own test runner — **Playwright Test** — which makes screenshots, videos, etc. a single configuration.
- Docker support.

### Prerequisites and setup

We need **Node.js** (anything above 14), **VS Code**, and the Playwright VS Code extension. Create a folder called `learn-playwright`, open it in VS Code with `code .`, install the Playwright extension by Microsoft from the Extensions panel, then open the command palette with Ctrl+Shift+P and run **Install Playwright**. Choose Chromium, Firefox, and WebKit; skip the GitHub Actions option since we will mostly run on LambdaTest or locally.

Without the extension you would manually run `npm init -y`, add dependencies, and install browsers via `npx playwright install`. The extension makes life much easier.

The installation creates a `tests` folder with an `example.spec.ts`. Click the green icon next to a test to run it. By default it runs headless — we don't see the browser. To fix that, open `playwright.config.ts` and set:

```
use: { headless: false }
```

Run again and you'll see the Chromium browser launch and complete the test — insanely fast.

If you have a basic knowledge of JavaScript or TypeScript, learning Playwright is going to be really fun and easy.

## Launching the Browser, Contexts, and Pages

In this section we learn to launch Chromium, write a simple login script, and understand the important concept of **context** vs **new page**.

Delete `example.spec.ts`. In `playwright.config.ts`, strip everything except the default `defineConfig` export (this is your global configuration). Create `tests/login.test.ts`.

Use the **test block** from Playwright's inbuilt test runner (similar to Mocha/Jasmine's `describe`/`it`):

```
import { test } from '@playwright/test';

test('login test demo', async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  ...
});
```

Playwright supports **async/await** out of the box — recommended over `.then().catch()`.

- `chromium.launch()` launches the Chromium browser engine. Chrome, Brave, and the new Microsoft Edge are all built on Chromium.
- `browser.newContext()` creates a new browser **context**. Multiple contexts don't share cookies or cache. Think of a context as an incognito session.
- `context.newPage()` creates a new tab within a context.

For our test demonstration we use a LambdaTest e-commerce playground. Use `await page.goto(url)`. Always use `await` before each step (about 95% of the time) — without it, promises become a mess.

To hover over **My Account** we cannot use `text=My Account` because three elements share that text and the first is hidden. So we write an XPath:

```
await page.hover("//a/span[text()='My Account'][1]");
```

For unique text like **Login** we can use a text selector:

```
await page.click("text=Login");
// or shorthand:
await page.click("'Login'");
```

In Playwright, finding a locator is one function — at runtime it figures out whether you passed a CSS, ID, or XPath.

To run, set `testMatch: ['login.test.ts']` in the config and execute `npx playwright test`. (We use `npx`, not `npm`, because `npx` executes the locally downloaded packages.)

Type into inputs with `page.fill(locator, value)`. There is also a `type` function — the difference is that `fill` clears the existing value and dumps the entire string instantly, while `type` types one character at a time (useful when you want to append). Click with `page.click(locator)`.

Compared to Selenium: `page.goto` is `driver.get`; `hover` replaces the `Actions` mouse-over; `click` and `fill` are like `element.click()` and `sendKeys`.

`page.waitForTimeout(5000)` is the equivalent of `Thread.sleep` — useful for demonstration but avoid it in real tests.

### Why context matters

If we open a second tab via `context.newPage()`, the session and cache are carried forward — the new tab is logged in. But if we create a fresh context with `browser.newContext()`, that context is essentially incognito. From a new context's `newPage()`, the user is not logged in.

This is the beauty of Playwright: you can do parallel things in different contexts simultaneously, and each `page.click` or `newPage.click` operates on its own context.

## Codegen, Reporters, Retries, and Auto-Wait

Without writing a single line of code we can record a test using `npx playwright codegen`. This launches a browser with the **Playwright Inspector**. Paste the URL, perform the actions (mouse-over, click, fill, etc.), then copy the generated code into a new test file.

The generated code uses a `page` parameter — this is the **fixture** concept (covered later). It means we don't have to write the launch/context/newPage lines every time.

The Playwright Test Recorder cannot capture every action — for example mouse-hovers may need to be added manually — but compared to Selenium IDE it is really good. The recorder also produces locators in Playwright's locator engine; you cannot find these directly in DevTools, but Playwright has its own way (covered later).

### Reporters

In `playwright.config.ts`:

```
reporter: [
  ['dot'],
  ['json', { outputFile: 'jsonReports/jsonReport.json' }],
  ['html', { open: 'always' }]   // 'always' | 'never' | 'on-failure'
]
```

Run the test and a `playwright-report/index.html` is generated. The dot reporter shows a green dot per pass and red per fail in the terminal. The HTML report shows steps, before/after hooks (the auto-opened browser context), and standard output.

### Screenshots, video, and retries

```
use: {
  screenshot: 'on',           // 'off' | 'on' | 'only-on-failure'
  video: 'on'                 // 'off' | 'on' | 'on-first-retry' | 'retain-on-failure'
}
retries: 2
```

With `retries`, on failure Playwright reruns the test the specified number of times — the report shows the original run plus each retry. This is similar to TestNG's retry but requires only configuration, not code.

### Auto-wait

Playwright's actions automatically wait for the element to be **attached**, **visible**, **stable**, **receiving events**, and **enabled** before clicking. For `fill`, it also waits for **editable**. This eliminates most explicit waits.

## Inputs, Buttons, Checkboxes, and Web-First Assertions

Use `page.locator(selector)` to define a reusable locator (no `await` needed when only finding — only when acting). Examples:

- `await messageInput.scrollIntoViewIfNeeded()` — manual scroll if Playwright's auto-scroll isn't enough.
- `await messageInput.getAttribute('placeholder')` — read an attribute.
- `await messageInput.inputValue()` — read whatever value is in an input. Don't confuse with `getAttribute`.
- `await messageInput.type('hi kaushik')`.

Web-first assertions use `expect`:

```
await expect(messageInput).toHaveAttribute('placeholder', 'Please enter your Message');
await expect(result).toHaveText('667');
await expect(locator).toContainText('partial');
```

These are auto-retrying assertions — internally they keep polling until the condition is true or times out.

For checkboxes:

```
const singleCheckbox = page.locator('#isAgeSelected');
await expect(singleCheckbox).not.toBeChecked();   // negate with .not
await singleCheckbox.check();
await expect(singleCheckbox).toBeChecked();
```

Use `check()` for checkboxes (or `click()` — both work).

`test.only` runs only that test in a file. Multiple `test()` blocks each open and close their own browser instance — they are independent tests.

## Alerts (JS and Modal)

JavaScript alerts cannot be inspected in DevTools, so we cannot find a locator for them. Playwright handles them via an **event listener** — register first, then trigger the action:

```
page.on('dialog', async alert => {
  console.log(await alert.message());        // text inside the alert
  console.log(await alert.defaultValue());   // for prompt alerts
  await alert.accept('Kaushik');             // accept; pass text for prompt
  // or: await alert.dismiss();
});
await page.locator('button:has-text("Click Me")').nth(0).click();
```

Note: by default, `page.locator` is **strict** — it errors with "strict mode violation" if multiple elements match. Use `.nth(index)` to pick one and disable strictness for that call.

For **bootstrap/modal** alerts, the alert is just a regular DOM element — find it and click. No event listener needed.

For the prompt alert, `alert.accept(text)` enters text and accepts. `defaultValue()` reads the placeholder text.

## Dropdowns

For an HTML `<select>`, use `selectOption`:

```
await page.selectOption('#select-demo', { label: 'Tuesday' });
await page.selectOption('#select-demo', { value: 'Friday' });
await page.selectOption('#select-demo', { index: 4 });
```

For multi-select, pass an array:

```
await page.selectOption('#multi-select', [
  { label: 'Texas' },
  { index: 2 },
  { value: 'Washington' }
]);
```

For Bootstrap/jQuery dropdowns (not real `<select>`), click to open then use a chained locator:

```
async function selectCountry(country: string) {
  await page.click('#country + span');
  await page.locator('ul#select2-country-results')
            .locator('li', { hasText: country })
            .click();
}
```

This locator-from-locator chain plus the `hasText` option is one of Playwright's standout features.

### Slow-motion mode

For debugging:

```
use: { launchOptions: { slowMo: 1000 } }
```

Each action runs with a 1-second pause.

## Frames and Multi-Tab Handling

A **frame** is an HTML document inside another HTML document (an `<iframe>`). Pages can contain multiple, even **nested**, frames.

`await page.frames().length` gives the number of frames on the page. To interact with a frame:

```
const myFrame = page.frame('frame-name');   // by name attribute
await myFrame?.fill('input[name="fname"]', 'Kaushik');
```

The `?.` is the **nullish operator** — `frame()` returns `null` if the frame isn't found, so the chain only runs if the frame exists.

The newer API is `frameLocator`:

```
const frame = page.frameLocator('iframe#first-fr');
await frame.locator('input[name="fname"]').fill('Kaushik');
```

For **nested frames**, just chain another `frameLocator` from the parent:

```
const innerFrame = frame.frameLocator('iframe[src="inner-frame"]');
await innerFrame.locator('input[name="email"]').fill('test@gmail.com');
```

Compared to Selenium there is no `switchToParentFrame` or `switchToDefaultContent` — use `page` for the page and the frame object for the frame.

### Multi-tab / pop-up windows

When clicking a link opens a new tab, use a **race** between the listener and the click:

```
const [newWindow] = await Promise.all([
  page.waitForEvent('popup'),
  page.click("text='Follow on Twitter'")
]);
console.log(await newWindow.url());
```

Inside `Promise.all` you do **not** put `await` before each call.

For multiple new windows, use `multiPage.context().pages()` to grab all pages, and `await multiPage.waitForLoadState('networkidle')` so you wait until everything finishes loading. Then loop and identify each page by URL:

```
let facebookPage: Page;
for (let i = 0; i < pages.length; i++) {
  const url = await pages[i].url();
  if (url.includes('facebook.com')) facebookPage = pages[i];
}
const text = await facebookPage.locator('h1').textContent();
```

`waitForLoadState` accepts `'load'`, `'domcontentloaded'`, or `'networkidle'`.

## Date Pickers (Calendar) with the moment Library

Two ways to handle date pickers.

**1. Type the date directly** if the input is `type="date"`:

```
let date = '1994-12-04';   // YYYY-MM-DD format expected by date inputs
await page.fill('#birthday', date);
```

A wrong format throws "malformed value". Use DevTools: `document.getElementById('birthday').value` shows the format the field stores.

**2. Click through a custom date picker** using previous/next arrows. Combine with the **moment** library to determine if the target month is before or after the current month:

```
import moment from 'moment';

async function selectDate(date: number, monthYear: string) {
  await page.click("input[placeholder='Start date']");
  const mmy   = page.locator("(//table[@class='table-condensed']//th[@class='datepicker-switch'])[1]");
  const prev  = page.locator("(//th[@class='prev'])[1]");
  const next  = page.locator("(//th[@class='next'])[1]");

  while (await mmy.textContent() != monthYear) {
    const isBefore = moment(monthYear, 'MMMM YYYY').isBefore();
    if (isBefore) await prev.click();
    else          await next.click();
  }
  await page.click(`//td[@class='day' and text()='${date}']`);
}
```

Note: distinguish `td.day` (current month) from `td.new` (next month) when both contain the same day number. Wrap the logic in a reusable function and call it for any date.

## Upload and Download

### Download

Use a `Promise.all` race between the `download` event and the click:

```
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('#linkToDownload')
]);
const filename = download.suggestedFilename();
await download.saveAs(filename);
```

Downloaded files are deleted when the browser context closes — `saveAs` persists them. `saveAs` also waits until the download completes.

### Upload

The simplest method (when you can find an `<input type="file">` element):

```
await page.setInputFiles("input[type='file']", [
  './uploads/apple.png',
  './uploads/mango.png'
]);
```

Do not click the file input — just set the files. Multiple-file upload requires the input to have the `multiple` attribute.

If the input is hidden or replaced by JavaScript, use the `filechooser` event:

```
const [uploadFiles] = await Promise.all([
  page.waitForEvent('filechooser'),
  page.click("input[type='file']")
]);
console.log(uploadFiles.isMultiple());
await uploadFiles.setFiles(['./uploads/apple.png', './uploads/mango.png']);
```

## Page Object Model (POM)

POM is a design pattern that creates an **object repository** for storing all elements, reducing duplication and improving maintenance. Each web page becomes a class file.

For the LambdaTest e-commerce playground we create classes per page in a `pages/` folder: `RegisterPage`, `LoginPage`, `HomePage`, `SpecialHotPage`. Each class follows the same shape:

```
import { Page } from '@playwright/test';

export default class RegisterPage {
  constructor(public page: Page) {}

  async enterFirstName(firstName: string) {
    await this.page.type('#input-firstname', firstName);
  }
  // ...other field methods, click methods, assertions
}
```

The `public page: Page` constructor shorthand auto-assigns `this.page`. Methods only return locators where you want the test to assert against them (web-first assertions):

```
isSubscribeChecked() {
  return this.page.locator('#input-newsletter-no');
}
```

Test usage:

```
import RegisterPage from '../pages/RegisterPage';

test('register_01', async ({ page, baseURL }) => {
  await page.goto(`${baseURL}?route=account/register`);
  const register = new RegisterPage(page);
  await register.enterFirstName('Kaushik');
  // ... other fields
  await expect(register.isSubscribeChecked()).toBeChecked();
  await register.clickTermAndCondition();
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle' }),
    register.continueToRegister()
  ]);
});
```

The `baseURL` comes from `playwright.config.ts` — handy when only the route changes between pages.

When login is a **precondition** for another test (rather than the test itself), wrap the steps in a single `login(email, password)` method on `LoginPage` so other tests don't repeat all three calls.

Wrap related tests in `test.describe(...)` to group them.

## Playwright Fixtures

A **fixture** is the mechanism behind the `page` parameter we receive in every test — an object whose setup (browser, context, new page) and teardown (close) are managed for us by the Playwright Test runner. We can extend it with our own.

Create `fixture/myFixture.ts`:

```
import { test as myTest } from '@playwright/test';

type Kaushik = { age: number; email: string };

const myFixtureTest = myTest.extend<Kaushik>({
  age: 27,
  email: 'kaushik350@gmail.com'
});

export const test = myFixtureTest;
```

Now any test importing `test` from this file gets `age` and `email` as fixtures alongside `page`:

```
import { test } from './fixture/myFixture';

test('fixture demo', async ({ page, age, email }) => {
  console.log(age + 15, email.toUpperCase());
});
```

This is also why `test.use({ ... })` overrides the default fixtures — it reassigns values inside the same fixture system.

### POM via fixtures

Instead of constructing every page class inside every test, do it once in a fixture:

```
type Pages = {
  registerPage: RegisterPage;
  loginPage: LoginPage;
  homePage: HomePage;
  specialPage: SpecialHotPage;
};

const testPages = baseTest.extend<Pages>({
  registerPage: async ({ page }, use) => { await use(new RegisterPage(page)); },
  loginPage:    async ({ page }, use) => { await use(new LoginPage(page)); },
  homePage:     async ({ page }, use) => { await use(new HomePage(page)); },
  specialPage:  async ({ page }, use) => { await use(new SpecialHotPage(page)); }
});

export const test = testPages;
export const expect = testPages.expect;
```

Tests then declare only the pages they need:

```
test('login_02', async ({ page, baseURL, loginPage }) => {
  await page.goto(`${baseURL}?route=account/login`);
  await loginPage.login(email, password);
  expect(await page.title()).toBe('My Account');
});
```

Big tests with many pages now have far fewer imports and zero boilerplate construction.

### Externalizing test data

Move the strings out of the test file and into JSON:

```
// test-data/addToCart.testdata.json
{ "first_name": "Kaushik", "email": "kaushik04@gmail.com", "password": "Kaushik@123", "phone_number": "1234567890" }
```

```
import * as data from '../test-data/addToCart.testdata.json';
await register.enterFirstName(data.first_name);
```

TypeScript even gives autocomplete on the JSON keys.

## Cross-Browser Testing with `projects`

By default Playwright runs in Chromium. To override the browser for a single test:

```
test.use({ browserName: 'firefox' });
```

(Note: `test.use` cannot be called inside `test.describe` — move it outside.)

Playwright always runs against the **nightly** builds of the browsers — you are testing one release ahead.

For project-level configuration, use `projects` in `playwright.config.ts`:

```
projects: [
  { name: 'chrome',  use: { ...devices['Desktop Chrome'] } },
  { name: 'firefox', use: { ...devices['Desktop Firefox'] } }
]
```

`devices` is Playwright's catalog of browser/device emulation presets (Galaxy, iPhone, BlackBerry, etc. — all simulations, not real devices). With two projects, three test blocks become six test runs (three per browser).

Run a single project from the CLI:

```
npx playwright test --project=chrome
```

Workers control parallelism (`--workers=N`).

## Running Tests on the LambdaTest Cloud Grid

Two integration paths: the bare Playwright library, or with the Test Runner.

### Bare library

Replace `chromium.launch()` with `chromium.connect()` and pass capabilities through the WS endpoint:

```
const capabilities = {
  browserName: 'Chrome',
  browserVersion: 'latest',
  'LT:Options': {
    platform: 'Windows 10',
    build: 'Playwright Test Build',
    name: 'Playwright Test',
    user: process.env.LT_USERNAME,
    accessKey: process.env.LT_ACCESS_KEY,
    network: true, video: true, console: true
  }
};

const browser = await chromium.connect(
  `wss://cdp.lambdatest.com/playwright?capabilities=${encodeURIComponent(JSON.stringify(capabilities))}`
);
```

Use environment variables for credentials in real projects. Once connected, the test runs on LambdaTest — visible under **Automation → Builds**, with step-by-step actions, video, and network logs.

### With Test Runner via fixture override

Setting the WS endpoint in `config.use` clubs all tests into a single LambdaTest session — not what we want. Instead **override the page fixture** in `pomFixture.ts` so every test connects per-test, with the right capabilities and test name:

```
page: async ({}, use, testInfo) => {
  const fileName = path.basename(testInfo.file);
  if (testInfo.project.name.match(/lambdatest/)) {
    const caps = modifyCapabilities(testInfo.project.name, `${testInfo.title} - ${fileName}`);
    const browser = await chromium.connect(
      `wss://cdp.lambdatest.com/playwright?capabilities=${encodeURIComponent(JSON.stringify(caps))}`
    );
    const context = await browser.newContext(testInfo.project.use);
    const ltPage = await context.newPage();
    await use(ltPage);
    const status = testInfo.status === testInfo.expectedStatus ? 'passed' : 'failed';
    await ltPage.evaluate(_ => {}, `lambdatest_action: ${JSON.stringify({ action: 'setTestStatus', arguments: { status, remark: testInfo.error?.stack || '' } })}`);
    await ltPage.close();
    await context.close();
    await browser.close();
  } else {
    const browser = await chromium.launch();
    const ltPage = await browser.newPage();
    await use(ltPage);
    await ltPage.close();
    await browser.close();
  }
}
```

The `modifyCapabilities` helper splits the project name on `@lambdatest` (everything before is `browser:version:platform`) and rebuilds the capabilities object dynamically. The `evaluate` call sends a special `lambdatest_action` payload that LambdaTest reads to mark each test as passed/failed.

Project list using this convention:

```
projects: [
  { name: 'chrome:latest:MacOS Catalina@lambdatest', use: { ...} },
  { name: 'chrome:latest:Windows 10@lambdatest',     use: { ...} },
  { name: 'chrome',  use: { ...devices['Desktop Chrome'] } }   // local fallback
]
```

`@lambdatest` is **not** a keyword — it is just the substring the helper looks for to decide cloud vs. local. Run via `npx playwright test` (omit `--project=` to fan out across all projects).

After running, the LambdaTest dashboard shows individual results per browser/OS, each with its real test name, pass/fail status, and recorded video.

### Recap

- Local + library only: `chromium.connect` with capabilities — done.
- Local + Test Runner: override the `page` fixture, branch on the project name, use `modifyCapabilities` to mutate caps at runtime, and report status via `evaluate`. Pass `testInfo.title` as the LambdaTest test name when creating the new context.

The fixture override boilerplate is large, but you only write it once — copy-paste it and you are set.

That's it for this Playwright series. All source code is in the GitHub repository linked in the description. Thanks for watching — see you in the next one.
