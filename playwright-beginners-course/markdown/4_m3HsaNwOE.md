# Playwright Beginner Tutorial 1 | What is Playwright

> **Source:** [Playwright Beginner Tutorial 1 | What is Playwright](https://www.youtube.com/watch?v=4_m3HsaNwOE) — [Automation Step by Step](https://www.youtube.com/@RaghavPal) · 2022-08-29 · 13:04
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- Kick-off session of a step-by-step **Playwright** series aimed at complete beginners — no automation, testing, or coding background required.
- **Playwright** is a free and open-source test automation framework created by **Microsoft** for web browser applications (desktop and mobile web) and API testing.
- Supports four language bindings: **Node.js** (JavaScript/TypeScript), **Java**, **Python**, and **.NET** (C#).
- Cross-browser (**Chromium**, **WebKit**, **Firefox**), cross-platform (Windows, macOS, Linux), and supports CI/CD and Docker.
- Headline features include **auto-wait**, **built-in assertions**, parallel testing, multi-tab/multi-window support, iframe and shadow DOM handling, device emulation, geolocation, recording/debugging, screenshots/videos, and built-in reporters.
- Next session moves from theory to hands-on: prerequisites, installation, and running test cases.

## Welcome and series overview

Hello and welcome — I am **Raghav**, and welcome to this session and this series on **Playwright**. In this series we are going to learn Playwright step by step from scratch, so do not worry if you are a complete beginner, and do not worry if you have no background in automation, testing, programming, or coding. I am going to start from scratch and we are going to go up step by step.

In this session we will start with understanding what Playwright is and we will look at the features of Playwright. I will show you all the features and we will discuss what Playwright is, what applications are supported, what browsers are supported, what operating systems are supported, and everything about Playwright. So this is going to be a very theoretical introduction session, and from the next session onwards we will do hands-on — we will see the prerequisites and then we will install and use Playwright.

## How to ask questions and follow along

If you have any questions during this session, you can always let me know in the comment section or the Q&A section below this video. If you have any general question that is not related to Playwright or this video, you can still ask me — I read all my messages and I reply to everyone, so you can ask me your general questions as well. If it is a general question, you can add the hashtag **#AskRaghav**.

If you want, you can also go to my website **automationstepbystep.com**, where you will find all these tutorials as well, and you can see the **Ask Raghav** playlist there too — you can ask your general questions there.

If you find the pace of this video slow, you can go to the player settings, the video player settings, and increase the speed from there. With that, let's get started.

## What is Playwright

**Playwright** is a free and open-source framework. It is created by **Microsoft** and it can be used for doing test automation on web browser applications. When I say web browser, it can be desktop browsers or mobile browsers.

If I talk about the **applications supported** by Playwright: all web browser apps, all mobile web apps, and we can also do **API testing** with Playwright.

## Languages supported

Playwright is, as of now, implemented in four languages or four libraries:

- **Node.js library** — if you use the Node.js implementation of Playwright, then the options for programming language are **JavaScript** or **TypeScript**.
- **Java API** — if we use the Java library of Playwright, we can create our test cases and our framework in **Java**.
- **Python implementation** — we can use **Python** there.
- **.NET implementation** — we can use .NET languages like **C#**.

You can create your framework and write your test cases in any of these languages.

## Browsers supported

All the modern browsers are supported by Playwright, and we talk about the **browser engines** here. We have support for all **Chromium-based** browsers, all **WebKit** browsers, and all **Firefox** browsers.

- **Chromium** is a web browser engine, and under Chromium we have **Google Chrome**, **Microsoft Edge**, **Opera**, **Brave**, and many others.
- Under **WebKit** we have all the macOS and iOS browsers like **Safari** and all the iOS browsers.
- Under **Firefox**, all versions and all flavors of Firefox — whether it is desktop Firefox browsers or mobile Firefox browsers — everything is supported by Playwright.

You can also use these browsers in a **headless** mode or a **headed** mode. Headless means no GUI, so when you run your tests in headless mode, you will not see anything coming up on the screen — you will not see the physical browsers, everything will be running at the back end, and it will save time and memory. But if you want to run in a physical (headed) mode where you can see the physical browsers on your screen, that is also possible.

If you just search for "chromium browser list", you can find all these browsers like Opera, Microsoft Edge, Brave, Google Chrome — you can see the full list. Similarly, under WebKit you can see all the WebKit browsers like Safari, and then Firefox browsers — all of these are supported.

## Operating systems and CI support

If I talk about the **operating systems** supported by Playwright, then you can create your Playwright framework on a **Windows**, **macOS**, or **Linux** operating system. It also supports **CI runs**, so if you want to use any CI/CD tool or **Docker**, all that is supported.

## The official website and GitHub

This is the official website of Playwright. If you go and search for "playwright", you can see the official website **playwright.dev**, and here you can see the details about Playwright — the documentation, all the features: cross-browser, cross-platform, cross-language, mobile web, auto-wait, assertions, and all of these.

Here you can see the implementations: if you go to the dropdown, you can see all of these — Node.js, Python, Java, and .NET. When you select any of these implementations or libraries and click on the GitHub link, it will take you to the GitHub page for that particular API of Playwright. For example, I selected Node.js and clicked on the GitHub link, and it took me to the GitHub page for the Playwright Node.js implementation. Similarly, if I select Java and click the GitHub link, it takes me to the GitHub page for the Playwright Java implementation.

This is the link for the Playwright GitHub. This is also very important — you will see all the comments and everything here. That is why it is open source: we can contribute to this Playwright project. These two links (the official site and GitHub) are very important — I have shown you these so that in future, if there are any changes, you can always refer from here.

So this is what Playwright is. If you want, you can take a screenshot of this screen and keep it handy — keep it on your mobile or desktop screen and look at it multiple times so that it becomes very clear for you what Playwright is.

## Features of Playwright

With that, let us now go to the features of Playwright.

- **Free and open source.** Free means you can use it freely, and open source means we can contribute to the Playwright project.
- **Multi-browser, multi-language, multi-OS support.** This we have already seen.
- **Easy setup and installation.** In the coming session we will see how easy it is to set up, install, and configure Playwright.
- **Functional, API, and accessibility testing.** We can do functional testing and API testing with Playwright. There is a third-party plugin we can add into our Playwright framework to do **accessibility testing** as well.
- **Built-in reporters.** You will not have to add separate reporters in your framework, but if you want, you can also use **custom reporters** — for example, **Allure** reporting and others are supported.
- **CI/CD and Docker support.** If you want to use CI/CD tools like **Jenkins** or container platforms like **Docker**, that is possible with Playwright.
- **Recording and debugging.** If you want to record your test and have your test scripts generated, that is possible. If you want to debug your test and do step-by-step debugging, that is also possible — I will show you in the later sessions how we do recording and debugging.
- **Object locator capture.** You can capture the object locators from the screen, so you do not have to manually create the locators for your web objects — Playwright has options to explore and create locators for you.
- **Parallel testing.** With parallel testing we can make our testing very fast. Playwright in itself is very fast, but with parallel testing we can run Playwright on multiple browsers at the same time.
- **Auto-wait and auto-timeouts.** There are some auto-waits built into Playwright. When we are loading a page, finding an object, or doing any action on the object, there is a timeout available — by default it is **five seconds**, and we can change it as well.
- **Built-in assertions.** For example, if you want to click a button — say we are on the login screen and we want to click the login button — we will just add the step to click on the login button, but at the back end Playwright will run some built-in assertions like: is the page already loaded, is the object already loaded, is the object present, is the object clickable. All of this happens at the back end.
- **Less flaky tests.** With auto-wait, timeouts, and built-in assertions, our test cases are very less flaky. **Flaky tests** are tests that sometimes pass and sometimes fail when you run them. With Playwright there will be very few or no flaky tests.
- **Retry logic, logs, screenshots, and videos.** We have options for retry logic if you want to retry failed tests, options to see and generate logs, and options for screenshots and videos of our test execution.
- **Multi-tab and multi-window execution.** This is a very important feature. A lot of times in our applications, clicking a link or a button opens a page in a new window or new tab. In a lot of automation tools this is not supported, but in Playwright it is — you can do multi-window, multi-tab testing.
- **iframe and shadow DOM handling.** Playwright can handle iframes and shadow DOM objects. This is also very, very important and very useful in automation.
- **Device emulation, viewport, and geolocation.** If you want to emulate devices and run your test by emulating a mobile device, you can do that. If you want to set a viewport, screen size, or resolution and then do the testing, that is possible. If you want to change geolocations, that is also possible. For example, if I go to my Chrome browser and press **F12** on my keyboard to open Chrome DevTools, I have an option to select devices like Galaxy, iPhone, Pixel, Samsung, and I can set the resolution from there. With Playwright we can also do this — we can set the screen size, resolution, and geolocations.
- **Parameterization and data-driven testing.** We can do parameterization, add variables, do data-driven testing, or use external files like a CSV file to get our data and do testing.
- **Speed.** Playwright is very fast. When we run our test cases you will see how fast it is, and of course parallel testing makes it even faster.

These are all the features of Playwright. If you want, you can take a screenshot of this screen and keep it handy — look at it several times and you will never forget all the features of Playwright.

## Wrap-up and what's next

With that, we have completed this session. From the next session we will do hands-on — we will install Playwright, see the prerequisites, and then create and run our test cases. I hope this was very useful for you. Thank you for watching, and as I always say — **never stop learning**.
