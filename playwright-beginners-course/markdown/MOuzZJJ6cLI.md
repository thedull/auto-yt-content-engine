# Playwright Java Tutorial: Learn To Use Playwright With Java (In 5 Hours)!

> **Source:** [Playwright Java Tutorial: Learn To Use Playwright With Java (In 5 Hours)!](https://www.youtube.com/watch?v=MOuzZJJ6cLI) — [TestMu AI (Formerly LambdaTest)](https://www.youtube.com/@TestMuAI) · 2023-12-29 · 5:02:43
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A complete 5-hour beginner-to-intermediate course on **Playwright with Java bindings**, covering installation, first scripts, locators, actions, screenshots, video recording, debugging, alerts, browser contexts, window handling, and CI integration.
- Walks through real test scenarios on the **LambdaTest e-commerce demo site** including login, registration, dropdowns, checkboxes, and assertions using Playwright's web-first assertion API.
- Demonstrates Playwright-specific tooling: **Codegen** for recording tests, **Playwright Inspector** for debugging and locator picking, and **trace viewer**.
- Shows how to run tests on the **LambdaTest cloud platform** using `playwright.chromium.connect()` with a CDP endpoint and capabilities.
- Integrates **TestNG** for parallel execution and reporting, then schedules tests with **Jenkins** using cron syntax for CI/CD.
- Closes with a **Page Object Model** mini-project that registers and logs in users, then runs in parallel on LambdaTest.

## What Playwright is and why use it

Playwright is a **Node.js library to automate Chromium, Firefox, and WebKit with a single API**, built to enable cross-browser testing. Chromium is the engine behind Chrome, Brave, and Arc; Firefox uses its own engine; and WebKit powers Safari.

Playwright was started by Microsoft as a fork of **Puppeteer** (a Node library that automates only Chromium with JavaScript, mostly headless). Playwright supports both headless and headed mode, and has multiple language bindings: **Node.js (JavaScript/TypeScript), Java, Python, and .NET**.

Key advantages:

- **Cross-browser** across Chromium, Firefox, and WebKit using one API. Comes with bundled browsers, but you can also point it at locally installed Chrome or Edge.
- Browser engines often run **n+1 ahead** of the released browsers, so you're testing against an upcoming Chromium version (e.g. engine 115 when installed Chrome is 114).
- **Cross-platform** (Windows, Linux, macOS) and CI-friendly (Jenkins, CircleCI, LambdaTest).
- **Mobile browser** support (Chrome on Android, Safari on iOS) — but no native APK support.
- **No flaky tests** thanks to built-in **auto-waits** and **web-first assertions**.
- **Tracing** with DOM snapshots, screenshots, and live video rendering.
- **No limits**: multiple tabs, multiple browsers, multiple users with independent contexts (cookies, cache).
- All tested events: drag-and-drop, hover, dropdowns, frames, **Shadow DOM**.
- **Powerful tooling**: **Codegen** (record in any language), **Playwright Inspector** (best-in-class debugger), **Trace Viewer**.

## Installing JDK, Maven, and Eclipse

Install **JDK 11** (download the x64 installer from Oracle). After installing, set the environment variables:

- **User variable**: `JAVA_HOME` = root of the JDK folder (e.g. `C:\Program Files\Java\jdk-11`).
- **System variable**: append the `bin` folder to `PATH`.

Verify with `java -version` in a fresh command prompt.

Install **Apache Maven** (binary zip, e.g. 3.9.1). Extract to `C:\`, then:

- **User variable**: `MAVEN_HOME` = root of the Maven folder.
- **System variable**: append `bin` to `PATH`.

Verify with `mvn -version`.

Install **Eclipse IDE for Java Developers** — download the zip, extract, and create a desktop shortcut to `eclipse.exe`. No installer needed. (IntelliJ IDEA also works; the playlist uses Eclipse for keyboard-shortcut familiarity.)

## First Playwright Java project

In Eclipse, create a new workspace, then **File → New → Maven Project → Create a simple project**. Give it a group ID (e.g. `lambdatest.playwright`) and artifact ID, then finish.

In `pom.xml`, paste the **properties**, **dependencies**, and **build** sections from the official Playwright Java docs:

- **Dependency**: `com.microsoft.playwright:playwright:1.32` (use a recently released version; the very latest may not be in Maven Central yet).
- **Maven Compiler Plugin** with source/target set to **11** (matching the installed JDK).

Save `pom.xml` and Maven will download Playwright plus its `driver` dependency.

### Launching a browser and writing the first test

Playwright's architecture is different from Selenium — there's no JSON-Wire driver. Instead, you create a **Playwright server instance**, then launch a **browser**, then a **context**, then a **page** (which is just a tab):

```java
Playwright playwright = Playwright.create();
Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions().setHeadless(false));
Page page = browser.newPage();
page.navigate("https://ecommerce-playground.lambdatest.io/");
```

By default, Playwright runs **headless** — you have to explicitly set `setHeadless(false)` to see the browser.

For a login flow, find elements with `page.locator(xpath)` or the newer locator helpers like `page.getByPlaceholder("E-Mail Address")`. Then call `.hover()`, `.click()`, `.type()`, `.fill()`, etc. Switch browsers by changing `chromium()` to `firefox()` or `webkit()`.

### Web-first assertions

Always import `PlaywrightAssertions.assertThat` statically and prefer **web-first assertions** over plain Java asserts:

```java
assertThat(page).hasTitle("Account Login");
```

The default timeout is 5 seconds. Failed assertions show clear messages like "expected to be X but received Y".

Always close `page`, `browser`, and `playwright` at the end (each `close()` has a different meaning, covered in later lectures).

## Interacting with input fields

`page.locator(...)` returns **single or multiple elements** with the same function — there's no separate `findElements`. If a locator matches multiple elements and you call an action on it, you get a **strict mode violation** error. Make the locator unique (e.g. `input#user-message` instead of `#user-message`).

### `type` vs `fill`

- **`type`** binds to input event listeners — characters are typed one by one, triggering listeners.
- **`fill`** clears the existing value and injects all data at once without firing per-character events.

Use `type` when input event listeners matter; use `fill` for plain text fields that need to be filled fast.

### Other input APIs

- `locator.inputValue()` — read the current value of an input.
- `locator.getAttribute("placeholder")` — read any attribute.
- `assertThat(locator).hasAttribute("placeholder", "Enter First Name")` — preferred web-first assertion.
- `locator.clear()` — clear an input.
- `locator.check()` / `locator.uncheck()` for checkboxes; `assertThat(locator).isChecked()` and `.not().isChecked()` for assertions.

`check()` performs checkbox-specific actions internally; `click()` also works but is less idiomatic. Use `click()` when the visual checkbox isn't actually `type=checkbox` (some Bootstrap/Angular components fake it).

## Handling dropdowns

Two kinds of dropdowns exist:

1. **Native HTML `<select>`** — handled with `selectOption()`.
2. **jQuery / span-based dropdowns** — handled by clicking and selecting list items.

For native selects:

```java
Locator day = page.locator("select#select-demo");
day.selectOption("Wednesday");                                   // by label or value
day.selectOption(new SelectOption().setIndex(2));                // by index
day.selectOption(new String[]{"New Jersey", "Texas"});           // multi-select
```

Since version 1.29, Playwright matches by **value or label** by default. To enumerate options:

```java
Locator options = states.locator("option");
System.out.println(options.count());
options.allInnerTexts().forEach(System.out::println);
```

For **jQuery-style dropdowns**, click the visible span first, then click the matching list item:

```java
Locator country = page.locator(".select2-selection__rendered").first();
country.click();
page.locator("ul.select2-results__options li", new Page.LocatorOptions().setHasText("Denmark")).click();
```

`page.locator(...).first()` and `.last()` are how you target one element when the locator matches multiple.

## Screenshots

`page.screenshot(...)` returns a byte array (useful for embedding in extent reports as base64) or writes to disk:

```java
page.screenshot(new Page.ScreenshotOptions().setPath(Paths.get("./snaps/screenshot.png")));
page.screenshot(new Page.ScreenshotOptions().setFullPage(true).setPath(Paths.get("./snaps/full.jpeg")));
```

For element-level shots, use `Locator.ScreenshotOptions` (note the **different inner class** — locator screenshots use `Locator.ScreenshotOptions`, page screenshots use `Page.ScreenshotOptions`):

```java
header.screenshot(new Locator.ScreenshotOptions().setPath(Paths.get("./snaps/region.png")));
```

### Masking sensitive content

To hide credentials in screenshots:

```java
page.screenshot(new Page.ScreenshotOptions()
    .setMask(Arrays.asList(input))
    .setPath(Paths.get("./snaps/input.png")));
```

The masked region appears as a solid block in the saved image — useful for client demos.

### Hiding the caret

Set `setCaret(ScreenshotCaret.HIDE)` (or `ScreenshotCaret.INITIAL` to keep the blinking cursor) when capturing focused inputs.

You must close `page` and `playwright` for screenshots to be saved correctly.

## Codegen and video recording

### Codegen

Run from the project terminal:

```bash
mvn exec:java -e -D exec.mainClass=com.microsoft.playwright.CLI -D exec.args="codegen https://ecommerce-playground.lambdatest.io"
```

This launches a Chromium window plus the **Playwright Inspector** that records every action. You can switch the **Target** dropdown to generate Java, JavaScript, TypeScript, Python (Pytest), or .NET (NUnit/MSTest) code from the same recording.

Limitations: Codegen does **not record mouse hover or dropdown interactions**, so you'll need to add hovers and assertions manually.

### Recording videos

Set the video directory on the **browser context** (not on the browser directly):

```java
BrowserContext context = browser.newContext(new Browser.NewContextOptions()
    .setRecordVideoDir(Paths.get("videos/"))
    .setRecordVideoSize(1280, 720));
Page page = context.newPage();
```

Output is `.webm` format. Larger sizes give clearer video. Always close `page`, `context`, `browser`, and `playwright` to flush the file.

## Window and tab handling

A browser **popup model** (like a JavaScript modal) is not the same as a **browser window/tab**. Playwright treats every new tab as a `Page`. Instead of Selenium's `switchTo().window()`, you use **event listeners**:

```java
Page popup = page.waitForPopup(() -> {
    page.getByText("Follow on Twitter").click();
});
popup.waitForLoadState();
assertThat(popup).hasTitle("Twitter @lambdatest");
```

For **multiple new tabs at once** (e.g. "Follow All"), wait until a predicate matches the expected tab count:

```java
Page tabs = page.waitForPopup(new Page.WaitForPopupOptions().setPredicate(p -> {
    return page.context().pages().size() == 3;
}), () -> {
    page.getByText("Follow all").click();
});
List<Page> pages = page.context().pages();
pages.forEach(tab -> System.out.println(tab.title()));
```

You can interact with the original `page` and any popup at the same time — no switching needed.

## Browser contexts

A **browser context** is an independent browser session — like an incognito window. Cookies, cache, and storage are isolated.

- `browser.newPage()` opens a new tab in the **same context** — sessions persist.
- `browser.newContext()` opens a fresh context — a new "incognito" session with no shared data.
- `page.context().newPage()` (or `context.newPage()`) opens a new tab inside an existing context.

Use cases: log in as **admin in one context** and as a **regular user in another** simultaneously, or simulate chat applications with bot + user.

Some APIs are context-only: cookies, permissions, geolocation, route handlers, default timeouts. For these you must create a context explicitly.

You can run **multiple browsers** at once: `playwright.firefox().launch()` alongside `playwright.chromium().launch()`. Always close pages, contexts, and the playwright instance to free RAM.

## Debugging and the Playwright Inspector

Two debugging styles:

1. **Java-level debugging** in Eclipse — set breakpoints, step over/in, inspect variables. Good for Java values like assertion targets, but doesn't help find Playwright locators.
2. **Playwright Inspector** — Playwright-aware UI that highlights locators, lets you step through actions, and pick locators visually.

Add `page.pause()` in your code to launch the Inspector. In Java, by default the Inspector window is empty — to attach the source view, you need a **Maven debug profile**:

In `pom.xml` add a `<profiles>` section with a `debug` profile that uses `exec-maven-plugin` to run a specific main class. Then in the terminal:

```bash
set PLAYWRIGHT_JAVA_SRC=src/main/java
set PWDEBUG=1
mvn test -P debug
```

`PWDEBUG=1` disables the default 30-second timeout. With this setup, the Inspector shows your source code, highlights the active line, and lets you step through. Use the **pick locator** button to grab Playwright-specific locators (`getByRole`, `getByPlaceholder`, etc.) that aren't visible in Chrome DevTools.

The Inspector also includes a **Record** mode and a Target dropdown that copies your recorded actions in any supported language.

This only works for files in `src/main/java`, not `src/test/java`.

## JavaScript alerts and HTTP authentication

Three alert types:

- **Simple alert** — single OK button.
- **Confirmation** — OK / Cancel.
- **Prompt** — text input with OK / Cancel.

By default, **Playwright auto-dismisses any alert that isn't handled**. To handle one explicitly:

```java
page.onceDialog(alert -> {
    System.out.println(alert.message());
    System.out.println(alert.defaultValue());     // for prompts
    alert.accept("My Name");                       // or alert.dismiss()
});
button.click();
```

`alert.type()` returns `"alert"`, `"confirm"`, `"prompt"`, or `"beforeunload"`.

### `onceDialog` vs `onDialog`

- **`onceDialog`** registers a handler for a single dialog, then destroys the listener.
- **`onDialog`** is global — it stays registered and handles every dialog the same way. Useful only when one action fits all (e.g. always accept). Removing it requires `page.offDialog(...)` with a consumer reference. Prefer `onceDialog` for most cases.

### HTTP basic authentication

Despite looking similar, browser HTTP auth prompts are **not JavaScript alerts** — they're handled via the context:

```java
BrowserContext context = browser.newContext(new Browser.NewContextOptions()
    .setHttpCredentials("admin", "admin"));
Page page = context.newPage();
page.navigate("https://the-internet.herokuapp.com/basic_auth");
```

### Toast notifications

Toast messages are just regular DOM elements — locate them with `page.locator(...)` and assert visibility, no dialog API needed.

## Running tests on LambdaTest cloud

To run on LambdaTest's cloud Selenium grid for Playwright, build a **capabilities JSON** and connect via the CDP endpoint:

```java
JsonObject capabilities = new JsonObject();
JsonObject ltOptions = new JsonObject();
capabilities.addProperty("browserName", "Chrome");           // or pw-firefox, pw-webkit
capabilities.addProperty("browserVersion", "latest");
ltOptions.addProperty("platform", "Windows 10");
ltOptions.addProperty("name", "Playwright Test");
ltOptions.addProperty("build", "Playwright Java Build");
ltOptions.addProperty("user", USERNAME);
ltOptions.addProperty("accessKey", ACCESS_KEY);
capabilities.add("LT:Options", ltOptions);

Playwright playwright = Playwright.create();
Browser browser = playwright.chromium().connect(
    "wss://cdp.lambdatest.com/playwright?capabilities=" +
    URLEncoder.encode(capabilities.toString(), "utf-8")
);
```

Use **`connect()` instead of `launch()`** — even when targeting Firefox or WebKit, you still call `playwright.chromium().connect(...)` and let the cloud spin up the right browser.

After the test, mark status with `page.evaluate("_ => {}", "lambdatest_action: ..."")` so the LambdaTest dashboard shows pass/fail.

Get credentials from **Account Settings → Password & Security**. Use the **LambdaTest Capabilities Generator** to scaffold capabilities for any browser/OS combination.

### TestNG integration

Add the TestNG dependency to `pom.xml`. Create a `PlaywrightConnection` base class with `createConnection()` and `closeConnection()` methods, called in `@BeforeMethod` and `@AfterMethod`. Tests extend this class and use `driver.getPage()` to access the `Page` object.

The pattern: encapsulate connection logic and capabilities in helper classes (`Capabilities`, `Driver`, `PlaywrightConnection`) so test classes stay focused on the scenario.

## Jenkins integration

**Jenkins** is open-source CI/CD that lets you schedule test runs (e.g. nightly at 4 AM and 10 PM).

### Installation

Download the **LTS Generic Java package** (`.war` file). Run with:

```bash
java -jar jenkins.war
```

Visit `http://localhost:8080`, unlock with the secret in the printed file path, install suggested plugins, and create an admin user.

Install the **Maven Integration plugin** from Manage Jenkins → Plugins → Available Plugins.

### Surefire and Maven goals

Add the **maven-surefire-plugin** to `pom.xml` pointing at your `testng.xml` so `mvn test` runs the suite without Eclipse:

```bash
cd path/to/project
mvn clean
mvn test
```

### Configuring Jenkins

Manage Jenkins → Tools → add a Maven installation (point at `MAVEN_HOME`) and a JDK installation (point at `JAVA_HOME`).

Create a **New Item → Maven Project**:

- Source: local path (or Git URL — push your code to GitHub for the real-world setup).
- Goals: `clean test`.
- **Build Triggers → Build Periodically**: cron syntax `MINUTE HOUR DAY_OF_MONTH MONTH DAY_OF_WEEK`.
  - `53 10 * * *` runs daily at 10:53.
  - `H/15 * * * *` runs every 15 minutes.
  - `* * * * 1-5` runs weekdays only.

Build now to verify. The console output shows Maven downloading dependencies, running TestNG, and reporting results.

## Putting it all together: Page Object Model mini-project

Final lesson combines everything into a small POM project that registers and logs in users on the LambdaTest e-commerce demo.

### Structure

Create `com.lambdatest.lt.pages` and add classes for each screen/component:

- **`HeaderSection`** — the static header reused on every page. Has `clickLogin()`, `clickRegister()`, and a private `getMyAccount()` that returns the visible "My Account" locator (using `>> visible=true` or `.last()` to skip the duplicate hidden one).
- **`RegisterAccountPage`** — `clickContinue()`, `isWarningVisible()`, `isMandatoryWarningMessageVisible()` (returns count), `registerUserAccount(firstName, lastName, email, telephone, password)`, `isRegisterSuccess()`.
- **`LoginPage`** — `loginAsUser(email, password)`.

Each page class takes a `Page` in its constructor and stores it as a private field.

### Using `getByLabel`

Where the HTML pairs `<label>` with its `<input>` correctly, you can fill fields by their visible label:

```java
page.getByLabel("First Name").fill(firstName);
page.getByLabel("E-Mail").fill(email);
page.getByLabel("Password", new Page.GetByLabelOptions().setExact(true)).fill(password);
```

`setExact(true)` avoids the strict-mode violation between **Password** and **Password Confirm**.

### Generating unique emails

The demo site rejects duplicate emails. Generate a fresh one each run:

```java
String email = "kosik" + new Date().getTime() + "@mail.com";
```

(For richer fake data, use the **Faker** library.)

### Tests and parallel execution

Two TestNG test classes — `RegisterUserTC` and `LoginUserTC` — each extending `PlaywrightConnection`. Convert both to a single `both-testng.xml` with `parallel="classes"` and a thread count. Change the LambdaTest `name` capability to `"parallel demo"` so the runs group under a new dashboard tile.

Running on the LambdaTest free tier permits up to **3 parallel sessions** (5 with paid tiers); both test classes run side by side in different cloud browsers and both pass — register-success on one, login-success on the other. Videos are recorded automatically; screenshots can be enabled in capabilities.

### Closing notes

The full source is available on the presenter's GitHub under the **Lambda Test Playwright Java** repository, with all video links in the descriptions. The series concludes here, with an invitation to ping questions in the comments.
