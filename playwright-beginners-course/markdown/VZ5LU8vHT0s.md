# Playwright Python 1 | Getting Started

> **Source:** [Playwright Python 1 | Getting Started](https://www.youtube.com/watch?v=VZ5LU8vHT0s) — [Automation Step by Step](https://www.youtube.com/@RaghavPal) · 2025-06-05 · 43:51
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A complete beginner-friendly walkthrough of getting **Playwright with Python** up and running, starting from scratch with no prior Python or programming knowledge required.
- Covers what **Playwright** is, the browsers and operating systems it supports, headed vs. headless modes, mobile emulation, and scraping use cases.
- Walks through installing **Python**, setting up `PATH` environment variables, creating a project folder, and isolating dependencies inside a Python **virtual environment** (`venv`).
- Installs Playwright with `pip install playwright`, then runs `playwright install` to download Chromium, Firefox, and WebKit browsers.
- Sets up **VS Code** as the IDE (via the portable zip), installs the Microsoft Python extension, and demonstrates using AI tools like ChatGPT and GitHub Copilot to generate code.
- Ends by writing and running a first Playwright script that opens `google.com`, prints the page title, and closes the browser.

## What is Playwright and what can it do

Hello and welcome. I'm Raghav and in this session we are going to start working with **Playwright** with Python. We will go step by step and start from scratch — no need to worry if you are a complete beginner or if you have never done programming before.

In very simple words, Playwright is an **automation tool** for testing websites in an automated way. You can test your websites or use cases on your web applications end-to-end like a user scenario — however a user would interact with your site, you can automate that process with Playwright.

It works with all the major browsers — **Chrome**, **Firefox**, **Safari**, and **Edge**. When you run your tests, you can run them in:

- **Headed mode** — the browser comes up on the screen and you see everything happening on it.
- **Headless mode** — the physical browser does not come up; everything happens in the back end. This saves memory and avoids distracting you from your work.

Playwright runs on **Windows**, **Linux**, and **Mac**. It also offers a **command-line mode**, so you can run your tests from the terminal and integrate testing into a **CI/CD** process using tools like **Jenkins**, **Azure**, or **GitHub Actions**.

It also supports **mobile emulation** — if you've created tests for desktop browsers and want to verify how they behave on mobile, you can emulate that. Beyond testing, Playwright lets you do things like **scraping**, for example visiting a website and capturing all its links into a script or file. Essentially, all browser actions can be automated with Playwright.

## Checking your system

Before we do hands-on, let's make sure your system is ready:

- At least **4 GB of RAM**. On Windows, go to *This PC → Properties* to check. On Mac, click the Apple icon → *About This Mac*.
- At least **1.5 GB of free disk space** (1.5–2 GB is comfortable, since we'll install libraries and create our project).
- A **stable internet connection** for downloads and running tests.

You can also find these requirements on the official Playwright documentation — search for "playwright python system requirements", select Python under platforms and languages, and the system requirements page lists the latest specs.

## Installing Python

First, check if Python is already on your system. On Windows, press the Windows key, type `cmd`, hit Enter, and run:

```
python --version
pip --version
```

The same commands work on Mac — open the terminal via `Cmd + Space` → "terminal" → Enter, and run the same commands.

If Python is not installed, download it from **python.org**. Search for "download python", go to `python.org/downloads`, and click the *Download Python* button — it picks the right installer for your operating system. You can also browse all releases by clicking your operating system, where you'll find installers, embedded packages, and zip files.

Before installing, you can create a folder where Python will live. In this walkthrough, the installation goes into `D:\tools\Python`.

Run the `.exe` installer:

- You can click **Install Now** to install at the default location, **or** choose **Customize installation** to control the path.
- **Make sure to check "Add Python to PATH"** — otherwise you'll have to set it manually.
- During customize installation, you can uncheck Documentation if you don't need it, then browse to your chosen install location (here, `D:\tools\Python`).

Playwright requires **Python 3.8 or higher** for the latest version, so go with that or newer.

After installing, the existing command line still uses the old session — exit and open a fresh one. To verify environment variables, press the Windows key and type "environment", then choose **Edit environment variables for your account** (or right-click *This PC → Properties* and search "env" there). The Environment Variables window has two sections: **user variables** and **system variables**. Editing at user level is enough if you don't have system-level permission. Edit the `Path` variable and confirm two folders are present:

- The Python folder
- The Python `Scripts` folder

Open a new command line and run `python --version` and `pip --version` — both should now report versions. **pip** is the installer for Python and manages Python packages.

## Creating a project folder and a virtual environment

Now let's set up Playwright. The recommended workflow:

1. Create a separate folder for your Playwright project.
2. Install Playwright inside it (within a virtual environment).
3. Optionally choose an IDE, or stay with command line and a text editor.

Manually create a folder, e.g. `D:\projects\playwright-demo-1`. You can name it anything. Then open this folder on the command line. The reason: we'll create a **Python virtual environment** within this folder and install all required libraries inside it. Benefits:

- All project requirements stay inside the folder, **not at system level** — so other projects can't interfere.
- The folder is fully portable. Move it to another machine or upload it to the cloud and it carries all its libraries with it.

Open command prompt (or terminal on Mac), navigate to the project. On Windows, since the project is on `D:` drive (the default is `C:`), switch with:

```
D:
cd D:\projects\playwright-demo-1
```

A handy Windows shortcut: open the folder in Explorer, type `cmd` into the address bar, and hit Enter — it opens the command prompt at that location.

Now create the virtual environment:

```
python -m venv venv
```

Whatever you name it (here `venv`) is just the environment folder name. This creates the venv but doesn't activate it. To activate:

- **Mac / Linux**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

You can press **Tab** for autocompletion to confirm paths are right. Once activated, the prompt is prefixed with the environment name — that means the environment is active and any installs will go inside it.

## Installing Playwright

With the venv activated, install Playwright:

```
pip install playwright
```

Verify it's inside the project: open `venv/Lib/site-packages` (or the equivalent on Mac/Linux) and you'll find `playwright` installed there.

A couple of notes:

- To **upgrade** Playwright later: `pip install playwright -U`.
- The official docs actually recommend pairing Playwright with **pytest** via `pip install pytest-playwright`. With pytest, test files use a `test_` prefix (e.g. `test_example.py`) so the `pytest` command discovers and runs them. We're not using pytest in this session — that's covered in the second session.

Next, install the browsers:

```
playwright install
```

You'll see it download and set up **Chromium** (including the headless version), **Firefox**, and **WebKit** (for Safari). Once done, verify with:

```
playwright --version
```

or:

```
python -m playwright --version
```

We're now ready with Playwright and all browsers.

## Choosing an IDE — VS Code

From here, you can use any IDE or even a plain text editor. An IDE gives you code completion, auto-suggestion, autocorrection, error highlighting, plugins, and the ability to run code directly — so it's strongly recommended.

If you don't have a preference, **VS Code (Visual Studio Code)** is a great starting point. There's also a VS Code playlist on the presenter's site **automationstepbystep.com** that walks through it in seven steps.

To install: search "VS code download" → `code.visualstudio.com/download`. You'll find:

- **User installer** — installs for the current user.
- **System installer** — installs for the entire system.
- **Zip file** — unzip and run from any folder, no system install needed.

Make sure to pick the right architecture (`x64` vs `ARM64`). To check on Windows, right-click *This PC → Properties* and look for the operating system spec. The walkthrough uses the 64-bit zip.

To use the zip: create a folder (e.g. `D:\tools\VS Code`), right-click the downloaded zip → *Extract All* → choose your folder → Extract. After unzipping, open the folder and double-click the `Code.exe` (the application file). On Mac, the steps are the same: zip + unzip + run, or use the Mac installer.

When VS Code opens, you'll see sections for **Explorer**, **Search**, **Source Control**, **Run and Debug**, and **Extensions**. Open your project either via *File → Open Folder*, or by dragging and dropping the project folder into the Explorer pane. Trust the project when prompted, and you'll see your environment folder and project files appear.

In the Explorer panel, you'll find buttons for new file, new folder, refresh, and collapse.

## Writing the first Playwright test

We need a Python file with a `.py` extension. Click the new file button in Explorer and name it `first_test.py`. As a Python file, VS Code detects the language and offers to install the **Microsoft Python extension** — it gives extra features like code completion, auto-suggestions, and debugging. You can also install it from the Extensions panel by searching "Python" and picking the official Microsoft one.

Once the Python extension is on, you'll see "Python" in the status bar. Click it to access settings like **autoimport completion** and **type checking**, which you can toggle on or off.

### Generating the code with AI

You don't have to type the code from scratch. You can use the built-in **Copilot** in VS Code, or any AI tool — ChatGPT, Gemini, Copilot — and prompt it with:

> write playwright python code to open google.com and print the title

It will produce a full script that wraps the logic in a function and runs it. You can copy the meaningful part into `first_test.py`. If the import line is missing, add:

```python
from playwright.sync_api import sync_playwright
```

To improve readability, increase the font in *Settings → search "font" → Font Size*. You can also change the theme via the gear icon → *Color Theme* (e.g. *Default Light*).

### Formatting and Copilot extras

To format the file: right-click → look for the **Command Palette** option (or press `Ctrl + Shift + P`, or *View → Command Palette*) and run **Format Document**. You can also press `Shift + Alt + F`. For Python-specific formatting, install a Python formatter from Extensions.

Python uses **indentation** rather than brackets to denote blocks — everything indented under a statement is part of that block.

For Copilot specifically: open Command Palette and search "copilot". You can sign in with a GitHub account (optional). Once signed in, you can right-click your code and ask Copilot to explain it, fix it, review and comment, generate docs, or generate tests.

### Walking through the script line by line

The final script:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.google.com")
    print(page.title())
    browser.close()
```

Line by line:

- `from playwright.sync_api import sync_playwright` — imports the Playwright library so we can use it in our code.
- `with sync_playwright() as p:` — starts Playwright. Everything inside this `with` block uses Playwright, and `p` gives access to the browsers. When the block ends, Playwright autocloses and cleans up the browser.
- `p.chromium.launch(headless=False)` — starts the **Chrome browser** in headed mode (visible on screen). Try `headless=True` to hide the browser.
- `browser.new_page()` — opens a new tab on the browser.
- `page.goto("https://www.google.com")` — navigates to that website.
- `print(page.title())` — gets the page's title and prints it to the console.
- `browser.close()` — closes the browser at the end.

So in summary: import Playwright → start Playwright → launch the browser → open a tab → visit `google.com` → get the title → print it → close the browser.

## Running the test

Run the file with:

```
python first_test.py
```

You can run it from the command line in the project folder, or — since we're in VS Code — use the **integrated terminal**. Open it via *View → Terminal*, or press `` Ctrl + ` `` (the backtick key, top-right of the keyboard, sharing a key with the tilde). The terminal opens at the project folder by default.

You can also bump the terminal font size in *Settings → Terminal Font*.

Save your file (and the project), then in the terminal:

```
python first_test.py
```

Press Tab to autocomplete the filename, and hit Enter. The browser opens, navigates to `google.com`, prints the title to the console, and closes. The code works.

You'll also see a **Run button** in the top right of the editor — that comes from the Python plugin. Clicking it runs the same command. That works too.

## Wrap-up

That's how you can run your first **Playwright Python** test. I hope this was useful. I'll see you in the next session. Thank you for watching and never stop learning.
