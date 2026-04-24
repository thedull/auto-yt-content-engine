# Software Testing Course – Playwright, E2E, and AI Agents

> **Source:** [Software Testing Course – Playwright, E2E, and AI Agents](https://www.youtube.com/watch?v=jydYq7oAtD8) — [freeCodeCamp.org](https://www.youtube.com/@freecodecamp) · 2026-03-19 · 1:03:30
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A full beginner-to-practical software testing course by **Bo KS**, covering why testing matters, the testing pyramid, hands-on **Playwright** tests, and **AI-powered testing** with **KaneAI** from **TestMu**.
- Real-world case studies (Knight Capital, Therac-25, Boeing 737 Max) frame why bugs in production are 10–100x more expensive than catching them earlier.
- Hands-on Playwright walkthrough on a sample e-commerce app (**TechMart**): config, locators, actions, assertions, UI/API tests, headed and UI mode, mocking, edge cases, and accessibility checks.
- Demonstrates **KaneAI**: writing tests in plain English, autohealing, manual interaction recording, API testing, and cross-language code export.
- Closes with best practices: readable tests, independence, page-object pattern, CI/CD integration, and using traditional + AI testing together.

## Why testing matters

Before we write a single line of test code, let's talk about why testing matters. Writing tests takes time, and when you're under pressure to ship features it can feel like tests are slowing you down. But the cost of *not* testing is almost always higher than the cost of testing. Some real-world examples illustrate this:

- **Knight Capital (2012)** — one of the largest US trading firms deployed a software update to their trading system. A bug that wasn't caught in testing caused the system to make erratic trades. In just **45 minutes they lost $440 million**. The company never recovered and was eventually sold.
- **Therac-25** — a radiation therapy machine from the 1980s. Software bugs caused it to deliver massive radiation overdoses. Several people died and others were seriously injured. The bugs could have been caught with proper testing.
- **Boeing 737 Max** — software issues in the flight control system contributed to two fatal crashes. Inadequate testing of how the software would behave in certain scenarios was a major factor.

Most of us aren't building trading systems, medical devices, or airplanes — but bugs in everyday applications cost money too: a bug that causes users to abandon their shopping cart, a login issue that prevents customers from accessing your service, a data corruption bug that requires hours of manual cleanup, security vulnerabilities that lead to data breaches.

Studies consistently show that finding and fixing a bug in production is **10 to 100 times more expensive** than finding it during development. Production bugs require emergency debugging under pressure, hot-fix deployments, customer support costs, potential loss of user trust, and sometimes legal consequences. Think of testing as insurance for your code — a small upfront cost that avoids potentially massive costs later.

Testing isn't just about catching bugs. Good tests also:

- Serve as **documentation** for how your code should work.
- Give you confidence to **refactor** and improve code.
- Help **onboard new team members** faster.
- Enable **continuous integration and deployment**.
- Reduce the stress of releasing new features.

## The testing pyramid

One of the most important concepts in testing is the **testing pyramid**, popularized by **Mike Cohn**. Picture a pyramid with three levels:

- **Unit tests** at the bottom (the widest part) — fast, focused tests that check individual functions or components in isolation.
- **Integration tests** in the middle — verify that different parts of your system work together correctly.
- **End-to-end (E2E) tests** at the top (the smallest part) — test the entire application from the user's perspective.

The pyramid shape tells us we should have many unit tests, some integration tests, and even fewer end-to-end tests. As you move up the pyramid, tests become slower to run, more expensive to maintain, more brittle, and more prone to breaking. Unit tests run in milliseconds; E2E tests might take minutes.

### Unit tests

Unit tests focus on a single unit of code — usually a function, method, or class — tested in complete isolation. For example, if you have a function that calculates the total price of a shopping cart, a unit test would call that function with specific inputs and verify it returns the correct output. Unit tests are:

- **Fast** — you can run thousands in seconds.
- **Reliable** — they don't depend on any external systems.
- **Precise** — when they fail, you know exactly where the problem is.

A simple unit test in JavaScript would call a `calculateTotal` function with a known `items` array as input, then assert the returned total equals the expected value (e.g. 25).

### Integration tests

Integration tests verify that different components work together correctly. Examples:

- An API endpoint correctly reads from and writes to the database.
- The front end correctly communicates with the backend.
- A payment system integrates properly with a payment provider.

Integration tests catch bugs that unit tests miss — bugs that only appear when components interact. An API integration test might POST data to an endpoint, expect a 200 response status, then call `database.getCart()` and expect the items array to have length one with the new item present. It involves multiple components: the API endpoint, the database, and their interaction.

### End-to-end tests

E2E tests simulate real user behavior. They interact with your application through the same interface your users do — clicking buttons, filling forms, navigating pages. They're powerful because they test your entire system working together, but they're also slower, more complex, and more prone to breaking when your UI changes.

A Playwright E2E example for "user can complete a checkout" navigates to the homepage, clicks the element with text "add to cart", clicks "checkout", fills text fields by ID with an email and card number, clicks "place order", then asserts that an "order confirmed" element is visible. This walks through an entire user journey just like a real customer would.

### Other test types

Beyond the three main categories, there are specialized test types:

- **Smoke tests** — quick tests that verify basic functionality works (e.g. the application starts at all).
- **Regression tests** — ensure previously working features haven't broken after changes.
- **Performance tests** — measure how fast your application responds under load.
- **Security tests** — check for vulnerabilities like SQL injection or cross-site scripting.
- **Accessibility tests** — verify your application works for users with disabilities.

### What should I test?

A practical framework:

- Test the **happy path** — the main way users interact with your feature.
- Test **edge cases** — empty inputs, maximum values, special characters. You don't know what a user will really do, so cover the less common cases.
- Test **error handling** — what happens when things go wrong.
- Test **business-critical features** — where bugs would be the most costly.

You don't always need to test everything; focus on what matters most.

### Test-driven development (TDD)

You might have heard of **test-driven development (TDD)**: first write a failing test, then write the minimum code to make it pass, then refactor while keeping your tests green (passing). TDD can lead to better-designed code, but it's not always practical. Use it when it helps; don't force it when it doesn't.

**Summary:** the pyramid (many unit, some integration, fewer E2E); unit tests are fast and precise; integration tests verify components work together; E2E tests simulate real user behavior; focus your testing on what matters most.

## Hands-on with TechMart and Playwright setup

Now let's get hands-on. The course uses a sample e-commerce app called **TechMart** — a simple store where users can browse products, add items to a cart, and complete checkout. The full code is on GitHub (link in the original video description). To run it: go into the `sample-app` directory, run `npm install`, then `npm start`, and open the local URL in a browser.

TechMart has a homepage with product listings, a max-price filter, sorting, category navigation (electronics, accessories), product search, login (with demo account credentials), a cart page, checkout, and user registration — a real working application backed by an API.

To set up testing, navigate to `tests/traditional`. The course uses **Playwright**, one of the best testing frameworks available — created by Microsoft and supporting Chrome, Firefox, and Safari. Run `npm install` to install Playwright and its dependencies.

The `playwright.config.js` file tells Playwright:

- Where all your tests are located.
- Which browsers to test against (Chromium, Firefox, WebKit, Mobile Chrome, Mobile Safari, etc.).
- Where your local server runs and whether to start the application before the tests.
- Useful features like **screenshot on failure** and **video on failure** for debugging.

Before running tests, install the Playwright browsers with `npx playwright install`. Then `npm test` runs all 265 pre-created tests. To view the report: `npx playwright show-report` — it opens in your browser, shows every test grouped by browser (WebKit, Mobile Chrome, etc.), and lets you search and filter passed / failed / flaky / skipped tests.

## Test structure: homepage.spec.js

Every Playwright test file follows a similar structure. Walking through `homepage.spec.js`:

1. **Imports** — `import { test, expect } from '@playwright/test'`. `test` defines test cases; `expect` makes assertions.
2. **`test.describe('homepage', ...)`** — groups related tests together. The whole block contains all homepage tests.
3. **`test.beforeEach(...)`** — runs before every test in the block. Here it clears the cart and navigates to the homepage so every test starts from a clean slate.
4. **A test** — `test('description', async ({ page }) => { ... })`. The `page` object is like a remote control for the browser; you use it to navigate, click, type, and verify elements. A simple assertion checks the page title contains "techmart".

### Writing a test from scratch — search functionality

Adding `test('should filter products when searching', ...)` to the end of the file:

1. **Find the search input** — `const searchInput = page.locator('#search-input')`. `page.locator` finds elements using CSS selectors, text content, or other strategies.
2. **Type the search term** — `await searchInput.fill('keyboard')`. `fill` is an action that simulates a user typing. Other actions include `click` and `type`.
3. **Click the search button** — `await page.locator('#search-button').click()`, combining the locator and action in one line.
4. **Wait for the page to update** — `await page.waitForTimeout(500)`. Playwright also has other waiting mechanisms.
5. **Assert results** — get product cards via `page.locator('.product-card')`, expect the count to be 1 (only one keyboard product), and expect the visible product text to contain "keyboard".

That's the entire test.

### Locator strategies

Finding elements on a page is one of the most important skills in testing. You can locate by:

- **ID**
- **Class**
- **Text content** (e.g. `text=add to cart`)
- **Role / accessibility** (e.g. role of button with the name "login")
- **Placeholder text**
- **Combined CSS selectors**

Recommendation: prefer locators that are stable and meaningful. **IDs** and **`data-testid` attributes** are great. **Text content** works well for buttons and links. Avoid brittle selectors that depend on exact CSS structure.

## Shopping cart tests: action then verification

Looking at `cart.spec.js`, the test "should add item to cart" follows a key pattern with three pieces:

1. **Perform an action** — click "add to cart" on the first product.
2. **Verify immediate feedback** — the toast message appears.
3. **Verify the state change** — the cart count is updated.

This pattern — **action followed by verification** — is fundamental to good testing. Other tests in the file (navigating to the cart, etc.) follow the same pattern: navigate, verify immediate feedback, verify state change. When creating tests, this is a very good pattern to follow.

## Login form tests

In `login.spec.js`, the test "should log in successfully with valid credentials" runs from the login page (set in `beforeEach`):

1. Fill in valid demo credentials.
2. Submit the form (the action).
3. Verify feedback.
4. Verify the state change — redirected to the homepage.

An important note: even when there isn't an explicit `expect`, the test will still fail if a step doesn't work. For example, if `page.goto('/')` is expected as the redirect destination, the test fails when that URL is never reached.

The test "should show error for mismatched passwords" follows the same pattern but with a different password in the confirm field. It expects the error message to be visible and to read "passwords do not match". **Testing both success and failure scenarios is important.** Happy-path tests verify things work; error-handling tests verify things fail gracefully.

## Full E2E checkout

In `checkout.spec.js`, "should complete checkout successfully" is a long test because it walks the entire flow — filling out a multi-step form. It demonstrates:

- `fill` for text inputs.
- `selectOption` for dropdowns.
- Multiple assertions to verify the outcome at the end.

## API testing with Playwright

Playwright isn't just for UI testing — it can test APIs directly. In `api.spec.js`, with a base API URL defined:

- A GET to `/api/products` should return all products. The test awaits the request, expects `response.ok()` to be truthy and the status to be 200, awaits the JSON, expects it to be an array of products, and expects the length to be 6.
- "should add item to cart" — a POST sends data, the test expects an "added to cart" message, expects `data.length` to be 1, and verifies the product ID and quantity were added correctly.

API tests are faster than UI tests and great for testing back-end logic. **Combining UI and API tests gives you comprehensive coverage.**

## Running tests effectively

Different ways to run tests:

- `npm test` — runs all tests.
- `npm run test:headed` — runs in **headed mode**, opening a real browser so you can see what's happening. The first few tests are API tests so no browser pops up; later tests open the browser.
- `npm run test:ui` — opens **interactive UI mode** in Chrome for testing. Click play to run a block; gives much more information about your tests.
- `npx playwright test tests/cart.spec.js` — run a specific test file.
- `npx playwright test -g login` — run all tests matching the pattern (e.g. all tests with "login" in the name).
- `npm run test:report` — re-open the HTML report.

The course intentionally edits a test to expect "item added to cart" instead of "added to cart" to demo a failure. Because the suite runs across Chromium, Firefox, and WebKit, that one broken test fails on every browser. The report sorts failures to the top. Clicking into a failed test shows the expected substring, the actual string, the call log, the test code, the test steps, screenshots (when available), and an **error context** markdown file for additional debugging.

## Edge cases and error handling

The earlier tests cover the **happy path**, but real users do unexpected things — submit empty forms, double-click buttons, paste weird characters into search boxes. `edge-cases.spec.js` handles these:

- **Should handle empty search gracefully** — click the search button without typing. Expect product cards count to be 6 (all products still shown). Some apps would crash or show errors; ours shows all products.
- **Should show no results for nonsense search** — type random characters; expect 0 product cards.
- **Special characters / XSS** — search for HTML or JavaScript code. It should not execute. This is a basic **cross-site scripting (XSS)** check, one of the most common web vulnerabilities. Expect no results and the page still visible.
- Other tests cover whitespace-only searches, adding the same product multiple times, and not allowing checkout with an empty cart (fill out the form, attempt checkout, expect the empty-cart toast). You'd be surprised how many real e-commerce sites have shipped this bug.

The golden rule of edge-case testing: **think about what could go wrong, then write a test for it.**

## Mocking API responses

Sometimes you want to test how your application handles situations that are hard to reproduce naturally — what if the API is down, returns unexpected data, or a product is out of stock? Playwright lets you intercept network requests and return custom responses. This is **mocking**, and it's very powerful.

In `mocking.spec.js`, the key method is `page.route`, which intercepts any network request matching a URL pattern and decides what response to send back.

- **API down (500)** — return status 500 with body "Internal Server Error". Expect the product grid to be empty (0 product cards). Tests whether the app handles failure gracefully instead of showing a blank page or crashing.
- **Slow API (3-second delay)** — set a timeout before the route continues. Great for testing loading states: does your app show a spinner? Does it remain interactive while waiting? Eventually products should appear.
- **Out of stock** — return mock data with `stock: 0` for the wireless headphones. You don't have to modify the database — just mock the response. Expect two products and the "out of stock" indicator visible.
- **Add-to-cart failure** — selectively mock only the POST request, letting GET requests through normally. Selective mocking is powerful for testing specific failure points.

**When to mock:**

- Testing error states that are hard to reproduce.
- The real API is slow, flaky, or costs money per request.
- You need precise control over data.
- Testing third-party integrations you don't control.

**When *not* to mock:**

- When you need to verify the real API works (use integration tests for that).
- When mocking would make the test meaningless.

## Accessibility testing

A lot of people in the world live with some form of disability. If your website isn't accessible, you're excluding a huge number of potential users — and in many countries accessibility is the law. Playwright makes basic accessibility testing straightforward.

The most common accessibility issues:

- Missing alt text on images.
- Poor color contrast.
- Missing form labels.
- Keyboard navigation doesn't work.
- Screen readers can't understand the page structure.

Tests in `accessibility.spec.js`:

- **All images should have alt text** — checks every image. Screen readers depend on alt text; without it, the reader just says "image", which is useless.
- **All form inputs should have labels** — without labels, a blind user encounters a text box with no context — they don't know if it's for email, password, or search.
- **Page should have proper heading hierarchy** — screen reader users navigate by headings, jumping H1 → H2 → H3. Skipping from H1 to H3 is confusing — like a book with chapter 1 then chapter 3 and no chapter 2. Verifies headings don't skip levels.
- **Interactive elements are keyboard accessible** — many people with motor disabilities rely on keyboard navigation. If your buttons and links aren't reachable by pressing Tab, they're effectively invisible.

When the suite runs, most pass but a few fail — and that's a *good* thing. It means real accessibility issues were found that need fixing.

For more comprehensive accessibility testing:

- **Axe Core with Playwright** — automatically scans for **WCAG** violations.
- **Lighthouse CI** — Google's accessibility auditing tool.
- **pa11y** — command-line accessibility testing.

A single Axe-Core test can check for dozens of accessibility issues automatically.

**Recap of the three techniques:** test the unexpected (empty input, special characters, rapid interactions, error states); use mocking to control the test environment without modifying your backend; check accessibility for alt text, labels, heading structure, and keyboard navigation.

## Challenges of traditional testing

Now that you've seen how to write tests with Playwright, here are some honest challenges:

- **Significant learning curve** — you need a programming language (JavaScript, Python, etc.), the testing framework's API, CSS selectors and other locator strategies, async/await/promises, and best practices for reliable tests. Not everyone on a team has those skills.
- **Maintenance burden** — when your UI changes, selectors break, test flows need updating, assertions become invalid. A single UI redesign can break dozens of tests.
- **Flaky tests** — E2E tests sometimes pass and sometimes fail without code changes due to timing issues, network variability, browser inconsistencies, dynamic content. Flaky tests erode trust in your suite.
- **Writing tests takes time** — the checkout test alone was about 50 lines of code for one flow: identifying every form field, figuring out selectors, handling form submission, writing success assertions, and testing error cases. Multiply that by every feature.

## AI-powered testing

AI is transforming software development, and testing is no exception. **AI-powered testing** uses machine learning and natural language processing to:

- Generate tests from plain English descriptions.
- Automatically identify elements on the page.
- Maintain tests when the UI changes.
- Detect potential bugs and issues.

Instead of writing `page.locator('#first-name-field')` and a `fill`, you might just say "enter John in the first name field."

**Benefits:**

- **Accessibility** — team members who can't code can still write tests (QA analysts, product managers, stakeholders).
- **Speed** — describing a test in English is faster than coding it manually.
- **Maintenance** — AI can adapt to UI changes automatically.
- **Coverage** — more people creating tests means better coverage.

There are many ways to write tests with AI, including just asking ChatGPT for them. In this course, we use **KaneAI** from **TestMu** — a GenAI-native testing agent that lets you create and run tests using natural language. (TestMu provided a grant to make the course possible.)

What makes KaneAI interesting:

- Write tests in plain English.
- Supports web and mobile applications.
- Exports to multiple programming languages.
- **Autoheals** tests when the UI changes.
- Integrates with CI/CD pipelines.

Important caveat: **AI testing tools are powerful assistants but don't replace human judgment.** You still need to decide what to test, review AI-generated tests for accuracy, handle complex edge cases, and understand what the tests actually do. Think of AI testing tools as a productivity multiplier, not a replacement for testing knowledge.

## KaneAI walkthrough

KaneAI normally works against websites already live on production, so it needs a public URL. Since TechMart is on localhost, the course uses **cloudflared** to create a Cloudflare tunnel:

1. `brew install cloudflared`.
2. With the local server running, in another tab: `cloudflared tunnel --url localhost:3000`.
3. The output gives a public quick-tunnel URL that proxies to localhost.

If you already have your site hosted, this step is unnecessary.

### Authoring a test in plain English

On testmu.com, navigate to **KaneAI → Agent**. Choose desktop browser (mobile app and mobile browser are also available). The first prompt:

> First go to this website. Then make sure the title contains TechMart. Check that the text "Welcome to TechMart" is visible. Then scroll down and make sure at least four product cards are visible.

After clicking start, the agent shows a test plan on the left and a sample browser on the right. Approve the plan, and it executes: opens the website, verifies the welcome text, scrolls, verifies at least four product cards. After it finishes, save the test.

The saved test shows the steps: go to URL, check the heading contains "TechMart", assert title equals true, check the visible text, assert true, scroll, get a count, assert count >= 4. There's a code view too — KaneAI generates real Python code using **Selenium**. You don't have to touch the code, but it's there so the test can be re-run identically every time.

From the test summary you can execute the test again, automatically generate a description, set preconditions, add settings, add tags, view suggested issues (potential issues KaneAI flagged), and see version history. The course adds a "TechMart" tag and saves.

### A more interactive test

Second prompt:

> Go to the website. Click on the search input field. Type "keyboard" in the search box. Click the search button. Make sure only one product card is visible after searching, and that the product should be the mechanical keyboard.

Approve the plan, wait while the agent steps through, and save. Tests can be sorted into folders (e.g. a TechMart folder) for organization.

### Cross-language code export and downloading

By default KaneAI generates Python. From the **Code** tab, click **Generate new code** to choose another framework — for example, Playwright + JavaScript, the same stack covered earlier in the tutorial. (Playwright/JavaScript export is "coming soon" at the time of recording.) Generated code can be reviewed, customized, integrated into existing test suites, and run in CI/CD. The current Python code is already downloadable with one click.

### Autohealing

A KaneAI flagship feature: imagine a developer changes the ID of an input. In traditional testing this would break the test. KaneAI understands the **intent** of the test, not just the exact selector — when it can't find the original element, it looks for alternatives that match the original purpose. This dramatically reduces test maintenance.

### API testing in KaneAI

To add an API call inside a web test, click **Author browser test**, keep default options, and click **Author test** with **manual interaction** turned on. Manual interaction lets you either record a real browsing session as a test, or — in this case — type `/` to open special commands and pick **Add an API**.

Paste the URL `/api/products` as a GET request (this is essentially the curl command). You can configure parameters, authorization headers, body, and settings; for a simple GET none of that's needed. Click **Send**, then turn off manual interaction so the API request executes — it returns 200, a successful test. Save it. The description reads: "the user performed the necessary steps to execute an API request." The test passes if the request is successful. You can build comprehensive API tests this way and combine them with UI tests for complete coverage.

## Best practices

Best practices apply whether you're writing tests manually or using AI tools.

### Make your tests readable

Anyone looking at a test should understand: (1) what it's testing, (2) how it tests it, and (3) what the expected outcome is. Good test names help a lot — `should display error when password is too short` is way better than `test1`, `test2`, `test3`.

### Keep tests independent

One test should not depend on the outcome of another. Each test sets up its own data, cleans up after itself, and can run in any order.

### Use the page object pattern

For larger test suites, use the **page object pattern** — instead of interacting with elements directly, create objects that represent pages. This makes tests cleaner and maintenance easier.

### Integrate with CI/CD

Tests are most valuable when they run automatically. Integrate them into your CI/CD pipeline so they run on every code change. KaneAI makes this easy with its API — you can trigger test runs from **GitHub Actions**, **Jenkins**, or any CI tool.

### Automated tests don't replace all testing

You still need:

- **Exploratory testing** for finding unknown issues.
- **Usability testing** for user experience.
- **Security testing** by experts.

Automated tests catch regressions; humans find new problems.

### When to use which tool

**Traditional Playwright tests** when:

- You need precise control over test logic.
- You're testing complex edge cases.
- You want tests in your codebase.

**KaneAI** when:

- You want to prototype tests quickly.
- Non-developers need to create tests.
- You want reduced maintenance overhead.
- You need cross-browser testing at scale.

Many teams use both approaches together.

## Wrap-up and key takeaways

We started by understanding **why testing matters** — bugs are expensive and testing is your insurance against costly mistakes. We learned the **testing pyramid** — unit tests at the base, integration in the middle, E2E at the top, each serving a purpose; a healthy suite includes all three. We got hands-on with **Playwright**, writing tests for the TechMart application — navigating pages, interacting with elements, and verifying outcomes with assertions. And we explored **AI-powered testing with KaneAI** — natural language converted into working tests, with autohealing reducing maintenance.

Key takeaways:

- **Start testing now.** Don't wait until your application is complete. The sooner you start, the more value you get.
- **Focus on what matters.** You don't need to test everything — prioritize features where bugs would be most costly.
- **Use the right tool for the job.** Manual coding for precision; AI tools for speed and accessibility. They complement each other.
- **Integrate your tests into your workflow.** Tests that don't run regularly don't provide value. Automate your test execution.

Thanks for watching this course. Happy testing.
