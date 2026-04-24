# Playwright Web Scraping + CAPTCHA Bypass Tutorial

> **Source:** [Playwright Web Scraping + CAPTCHA Bypass Tutorial](https://www.youtube.com/watch?v=RGR5Xj0Qqfs) — [Python Simplified](https://www.youtube.com/@PythonSimplified) · 2025-02-07 · 20:31
> *Transcript generated via `youtube-captions (en-CA)`.*

## TL;DR

- A beginner-friendly walkthrough of **Playwright** in Python: launching a browser, opening a page, taking screenshots, and selecting elements.
- Builds a mini-project that searches **arXiv** for "Neural Network" papers and downloads 50 PDFs automatically using **urllib**.
- Demonstrates headless vs. visible browsing using the **Gecko WebDriver** with `headless=False` and a `slow_mo` delay.
- Covers element selection strategies: `get_by_placeholder`, `get_by_role`, `get_by_text`, `nth`, and **XPath** with `contains()`.
- Shows how to bypass **CAPTCHAs** and **Cloudflare** protection on sites like Walmart and Geektime using **Bright Data's Web Unlocker** API as a proxy.
- Practical gotcha: when proxying through Web Unlocker, scrape the **HTTP** version of a site rather than HTTPS.

## Intro: what we're building

Hello everyone. In a recent poll, 47% of you voted for a **web scraping and CAPTCHA solving tutorial using Playwright**, and since your wish is my command, that's exactly what we'll do today.

In addition to learning the basics of Playwright, we will create a mini project: downloading a whole bunch of research papers using code only — no hands. The cherry on top is a state-of-the-art CAPTCHA solving system. So if you're ready, let's roll.

## Playwright basics: launching a browser

Let's begin with the basic syntax. First, import the `sync_playwright` class, then initialize it with `sync_playwright()` followed by calling the `start` method on it. Assign this expression to `pw`, as in Playwright.

To access a website through our code, we first need a browser object. In my case `pw.firefox`, on which we call the `launch` method, then assign it to `browser`. Since we are initializing a browser object, we also need to collapse it as soon as we are done — so at the very bottom of our code we call `browser.close()`.

In between, start with a new tab, which we can do with `browser.new_page()`, assigned to `page`. Then we use this tab to navigate to any kind of website with `page.goto("http://google.com")`.

To make sure everything worked, print the content of the page with `print(page.content())`, which prints the entire source code. Additionally, print `page.title()`, and take a screenshot of the page with `page.screenshot(path="example.png")`. You can choose any kind of name.

## Setting up the environment

In a WSL terminal, create a clean working environment:

- `conda create -n scraper` and install Python 3.11 in it.
- `conda activate scraper` to enter the new environment.
- `pip install pytest-playwright` to install Playwright.
- `playwright install` to install Playwright's browsers — even though you can select a specific browser like Firefox, I'll just install all of them. Why not?
- `playwright install --deps` to install the OS-level dependencies as well.

Now Playwright is officially installed and we can run our code with `python3 quickstart.py`. Beautiful — here's our source code (you can verify it later, it's very long), and here is our page title which is **Google**. Yay!

The screenshot ends up in the project folder as `example.png` — everything worked like a charm. The only problem is we didn't actually see a Firefox browser popping and navigating to Google. In technical terms, we've done something called **headless browsing**, where we fetch results without observing the actual process.

## Seeing the browser: WebDriver, headless=False, and slow_mo

If you'd like to physically see how your browser is being automated, you'll need a **WebDriver**. In the case of Firefox, it is called the **Gecko driver**, and you can find it on GitHub. Navigate to the release section and choose the release that best suits your operating system — in my case, Linux 64. Extract it in the same folder as our `quickstart` script (just drag and drop).

Once we have a WebDriver, the only changes in code are inside our Firefox `launch` method:

- Add `headless=False` so the browser actually pops up.
- Add `slow_mo=2000` (milliseconds) so the WebDriver waits at least two seconds before it collapses. Without this slow motion, you may not even see it.

Save and rerun. Beautiful — here's our Firefox WebDriver. It pops and is gone after two seconds. Same results as before, just much more visual. We're done with the quick start and can move on to selecting elements.

## Selecting elements on arXiv

Let's say we'd like to scrape research papers from a site named **arXiv** (that's how they spell it). Navigate to `arxiv.org/search` and let's have a look at the source code. Right-click and select **Inspect**, then click the arrow button and highlight the input field — in our case, an `input` element that has the placeholder text **"search term"**.

Quickly copy that placeholder text. Back in our code, update the URL from `google.com` to `arxiv.org/search`, then select the input with `page.get_by_placeholder("search term")`. While we're here, let's fill it: call the `fill` method and pass the text **"Neural Network"**.

Now we need to submit it. Back in the browser, the search element is a button with the inner text **Search**. So we add another selector: `page.get_by_role("button")`. But we're not just looking for any button — we want a special one — so we chain it with `get_by_text("Search")` (with a capital S, I believe — yes, capital S).

Once we have our button, call the `click` method on it. To keep our terminal nice and neat, get rid of the `page.content` print statement, save, and run.

There you go. Here's our arXiv page, here's our Neural Network search term — and oh no, something is wrong with our button. It looks like instead of selecting a single button, we selected two of them: a red one at the very top, and a blue one right below it.

So how do we click the second button and ignore the first? Right before `click`, add another method called `nth`, which receives an index. In our case, the index of the second button is **1**, because we start counting from zero. Save it. This time it works. **No hands.** We are successfully searching and navigating to a new page.

## Locating PDF links with XPath

Now let's say we want to download all the PDF documents from the search results. Inspecting the PDF link, we can see we're dealing with a bunch of anchor elements, and they all share a similar URL — they all start with `arxiv.org/pdf`.

To select all of them, we'll use **XPath**, which is probably the most accurate way of describing elements. It can target elements that have specific property values — for example, all the paragraphs that have the class of `authors`. Another benefit of XPath over other selectors is that it accepts approximate values, so we can target elements that **start with**, **end with**, or simply **contain** a specific set of characters — exactly what we are looking for here.

In our code:

```python
links = page.locator("xpath=//a[contains(@href, 'arxiv.org/pdf')]")
```

The `contains` function receives two arguments: the property `href`, and the pattern (a substring) to match.

To make sure it worked, print them:

```python
for link in links:
    print(link.get_attribute("href"))
```

Spoiler alert: the first time this won't work — and we'll see shortly why. Before we run, let's also turn off the slow motion since we already know it works.

Run it, and we get a `TypeError`: a locator object is not iterable. Turn it into one by calling `.all()` on the locator. Save and rerun, and now we get a whole bunch of anchor elements back — a very big list. Copy one to make sure you get a scientific article back, scroll down, and yes, it relates to neural networks.

## Downloading the PDFs with urllib

The only task left is downloading all these PDFs and storing them on our system. Create a new directory with `mkdir data`. Instead of printing the address attribute, assign it to a local variable named `url`.

Then use a library named **urllib** to download all these URLs as files. At the top of our code:

```python
from urllib.request import urlretrieve
```

Call it at the bottom of the for loop. `urlretrieve` receives two arguments: the URL itself, and the filename. The filename starts with `data/`, then we concatenate something unique — how about the serial number at the end of the URL (e.g. `13763`)? I sure hope it's unique.

We focus on the last five characters of our URL, then concatenate `.pdf`:

```python
urlretrieve(url, "data/" + url[-5:] + ".pdf")
```

Save and run. This one takes a bit of time because we're downloading 50 articles. Done — navigate to the project folder, refresh, and the `data` directory has a whole bunch of PDF files. Open one: an article about neural networks. Try the first one: a PDF research paper. Try one in the middle: also a research paper. Fantastic — they are all research papers. Amazing.

We're done with the introduction to Playwright. Let's move on to something a bit more professional.

## When sites fight back: CAPTCHAs and Cloudflare

So far we've been dealing with a very forgiving website. It never blocked our IP and it never stopped us with a CAPTCHA. But what happens if we're scraping a site that does?

For example, here's one that uses **Cloudflare protection** — essentially, it will always know that we're not human. Or another example: a popular website like **Walmart.com** that just slaps us with a CAPTCHA as soon as we try to access it.

But it's not going to stop us. We'll use a very powerful tool named **Web Unlocker**. This tool uses a combination of **proxies**, **CAPTCHA solvers**, and all kinds of goodies to bypass site security.

## Setting up Bright Data's Web Unlocker

Navigate to **brightdata.com** using the link in the description — it gives you **$15 of credits**, which is far more than what you need to follow along with this tutorial. I've been using the Web Unlocker for about a week and so far it cost me like **$0.15** or something ridiculous.

Steps inside the Bright Data dashboard:

- Click **Product** → **Web Unlocker API**, scroll down, and start your free trial. Log in (we will not change our password this time).
- Click **Proxies and Scraping**, scroll down, and **Get started** on the Web Unlocker API.
- Choose a name for your zone — let's say "Maria's Zone".
- Make sure the **CAPTCHA solver** is enabled.
- If you're scraping one of the listed extra-problematic domains, enable the **premium domain** section. I'm not, so I'll just click **Add** and confirm.
- Generate an **API key** from account settings: click **Add token**, give yourself administrative privileges, and click **Save**. Usually you'd save it on your system in a secure place; in my case it doesn't matter because I'll delete this token as soon as I'm done filming.

Once you're done, click **Proxies and Scraping** → **Maria's Zone**, and all the credentials you need are under the **access details** section.

## Wiring proxies into Playwright

Back in our code, create a new dictionary named `proxies` with three keys:

- `server` — the **host** from Bright Data's access details.
- `username` — the long username string.
- `password`.

Then specify the proxies when launching the Firefox browser by adding a `proxy=proxies` property to `launch`.

Two more things added off camera: I located the search input and filled it with the text "testing". Then, instead of clicking a button or submitting a form, I simply press the **Enter** key, which works just as well.

One more thing to notice: since we're using a bunch of proxies and some security-bypassing mechanisms, it makes sense to scrape the **HTTP** version of a site rather than the **HTTPS** version. Make sure you do so with `http`.

## Bypassing Walmart's CAPTCHA

Save and run. There you go — here's the ugly HTTP version of Walmart. We have a bit of a delay (slow motion set to five seconds). Here's our "testing" text, and we are navigating to a new page. Amazing — we now know exactly how to use proxies.

## Bypassing Cloudflare on Geektime

Let's try them on the other site we've been trying to scrape — the one with Cloudflare protection. Instead of `walmart.com`, it was something with "geeks"... let me check. Okay, it was **Geektime** — `geektime.co.il`. Save it. Save it! No! Come on, save it. Let's give it another run.

Okay, it pops here for some reason and — yay! — we don't have this Cloudflare page that prevents us from doing anything on the website.

So folks, congratulations. We now know exactly how to bypass CAPTCHAs and annoying bot-detecting mechanisms.

## Outro

My question to you: what kind of challenges are you facing with web scraping? I'm sure this tutorial solved a lot of them, but what other blockers are you facing? Let me know all your nightmare scenarios in the comments below and in my next tutorial I will try to tackle them.

Thank you so much for watching. If you found this video helpful, share it with the world and don't forget to leave a huge thumbs up and all kinds of comments — especially comments about your web scraping challenges. If you'd like to see more videos like this, subscribe and turn on the notification bell. I'll see you soon in an awesome tutorial. In the meanwhile, bye bye!
