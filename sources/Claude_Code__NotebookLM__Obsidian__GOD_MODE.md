# Claude Code + NotebookLM + Obsidian = GOD MODE

> **Source:** [Claude Code + NotebookLM + Obsidian = GOD MODE](https://www.youtube.com/watch?v=kU3qYQ7ACMA) — [Chase AI](https://www.youtube.com/@Chase-H-AI) · 2026-03-05 · 14:34
> *Transcript generated via `youtube-captions (en-orig)`.*

## TL;DR

- A practical, sub-30-minute workflow that combines **Claude Code**, **NotebookLM**, **Obsidian**, and the **Skill Creator** into a single research pipeline.
- Claude Code searches YouTube (via a `yt-dlp` skill), sends results to NotebookLM for analysis, and pulls back a deliverable — podcast, infographic, slide deck, etc. — all orchestrated through skills.
- The **Skill Creator** is used to bundle the individual skills (YouTube search, NotebookLM integration) into a single "super skill" that runs the whole pipeline on one command.
- **Obsidian** acts as the persistence layer: every analysis lands in a vault of linked Markdown files, giving the user a visual second brain and giving Claude Code a transparent, easily-queryable knowledge base.
- **`CLAUDE.md`** is the "brain within a brain" — updated over time so Claude Code learns the user's conventions, work style, and output preferences, making the whole system a self-improving loop.
- The workflow is a **template**, not a fixed recipe — swap YouTube for PDFs, articles, or any other source and the structure still holds.

## Why this workflow matters

If Claude Code plus NotebookLM is amazing, and Claude Code plus Obsidian is free value, and Claude Code plus the brand new Skill Creator is legitimately game-changing, then what happens when we combine all these tools together in a practical yet simple-to-set-up workflow that you can start using today in under 30 minutes?

That's exactly what we're going to find out. This workflow turns Claude Code into an absolute research monster. It's also a capstone of everything covered in the last few videos — Claude Code with NotebookLM, Claude Code with Obsidian, Claude Code with the new Skill Creator — synthesized into something with practical value.

What's important isn't my exact use case. This is a personal Chase AI use case for how I do research for my content. But you're not a content creator. You probably have a real job. So throughout this entire lesson, don't focus on the intricacies of how I'm doing my YouTube search. Focus on this: **how do I swap the YouTube search for whatever use case I have** and whatever source of information I need — PDFs, articles, text, whatever? How can we fit this template into your life? That's where the value lies, and that's what I want you to focus on. This is a very flexible workflow that adapts to your needs.

## What the workflow does

Research on steroids. Inside Claude Code, we're going to do research via YouTube — in this case, YouTube videos are the data source. A specific skill handles that search. From there, we send the YouTube data to **NotebookLM** via Claude Code. NotebookLM runs analysis on those videos and produces any deliverable we want — a podcast, a video, an infographic, a slide deck — and passes all of that back to us inside Claude Code.

All of this is executed through **skills**. Furthermore, we combine all those sub-skills into essentially one super skill. We do that using the **Skill Creator**. The Skill Creator is where the super skill comes from, and the NotebookLM integration lands inside it.

## Where Obsidian fits in

The workflow above is great in a vacuum, but to really supercharge it we need persistence. I'm not just going to run this workflow one time — I'll run it dozens or hundreds of times. Enter **Obsidian**.

All the data we analyze — and more importantly, the *way* we attack the data, how we like our analysis done, what we want the deliverables to look like, how we think — all of that gets recorded by Claude Code as a series of Markdown and text files inside the vault.

The Obsidian vault is great for two reasons:

- **For me as the human**, I get great insight into what's going on in my text files. I can click through the files, see how they link together, and get neat graphs.
- **For Claude Code**, all those Markdown files are transparent. It's easier, when things are set up in this Obsidian-style format, for Claude Code to find what it needs.

Over time, we also refine how Claude Code speaks to us and thinks — via the `CLAUDE.md` file. So Obsidian helps Claude Code do this workflow in the manner *we* want. With Obsidian added, Claude Code becomes a well-trained personal assistant that executes this workflow on our behalf.

## The self-improving loop

This almost becomes a self-improving loop. The more I run the workflow, the more its analysis gets shaped the way I like it. The more I talk to Claude Code, the more that data is recorded. Claude Code continues to build and build and build over time — a corpus of knowledge and evidence for *how I like to work*.

That's how we get this symbiotic relationship: Claude Code + Skill Creator + NotebookLM + Obsidian, all helping one another. And look how flexible it is — swap YouTube for PDFs, drop NotebookLM if you don't need it. As long as you keep the template of **flow + Obsidian + skills improved via the Skill Creator**, you have something extremely powerful that most people aren't doing.

## Sponsor break

Before we get into how to set this up exactly — a word from our sponsor: yours truly. If you want to learn more about Claude Code, I just released a **Claude Code Masterclass** inside of **Chase AI Plus**. It takes you from zero to essentially AI dev, regardless of your technical background or lack thereof. Chase AI Plus is great if you're serious about AI and trying to make a career out of it. There's also a free Chase AI community — link in the description — where all the skills we talk about today, along with a number of other free resources, are available. So there's something for everybody.

## Setting up the Skill Creator

First thing we need to do is create our skills. You'll notice I'm **inside my vault** — you have to be in your Obsidian vault folder for Obsidian to pick up on this stuff.

For the Skill Creator itself, I've covered installation in depth in another video. The 5-second version:

1. Run `/plugin` inside Claude Code.
2. Search for the **Skill Creator** tool.
3. Install it.
4. Exit Claude Code, spin it back up.

You're ready to go.

## Building the YouTube search skill

To build a skill, I run `/skill-creator` — using the slash command (rather than natural language) ensures it actually invokes the skill. Then I describe what I want.

In this case, I said I wanted to create a skill that searches YouTube and returns structured video results. It should use **`yt-dlp`** to search for videos by query and return the results. (Adjust this for whatever source you want to use — these prompts are available inside my community.)

Once you run that, it creates the skill automatically inside your `.claude` folder and gives you descriptions of what the Skill Creator did. You have the ability to run tests on the skill as well, but we'll skip that for now. That gives me the YouTube skill — I can now search YouTube from Claude Code.

## Building the NotebookLM skill

What about the NotebookLM side? I've got a full video deep dive on this, but here's the 30-second rundown.

NotebookLM **does not have a public-facing API**. So to connect Claude Code to NotebookLM, we use a GitHub repo called **`notebooklm-api`** (link in the description). Installation is easy — you run a couple of commands in your terminal:

1. Open a new terminal (**not** inside Claude Code — just a regular terminal).
2. Paste and run the install commands from the repo.
3. Authenticate with `notebooklm login`. A browser window pops up; log in and you're done.

You now have NotebookLM installed. But we still need to teach Claude Code how to use it — that's where a skill comes in.

The repo gives us a command (`notebooklm skill install`) to do this. But now that we have the **Skill Creator**, a better approach is to copy the entire GitHub repo (or pass a link to it) and tell Claude Code:

> "Skill Creator — create a skill so we can best use the NotebookLM skill."

This is one of the best things about Claude Code: **it will do things that affect its own use**. It understands how skills work within its own ecosystem, so when I do this, it self-improves in a way — which is great. Once you run it, you'll get the same kind of message as when we created the YouTube skill.

Specifically for NotebookLM, these commands allow us to do anything — and more — from the Claude Code terminal that you could do inside NotebookLM normally. We can:

- Create our own notebook
- Add as many sources as we like (up to 50 — from Drive, copy/text, files, YouTube, etc.)
- Generate any deliverable NotebookLM supports: audio overview, mind map, flashcards, infographic, and so on.

## Combining sub-skills into a super skill

Now I have the YouTube skill and the NotebookLM skill. But I don't want to tell Claude Code one-by-one, "okay, do the YouTube skill, thumbs up, now do that skill, thumbs up." I want to do it all at once. I want to turn it into **one skill**.

That's what we do next: **turning a workflow into a skill**. Same process as before — run the Skill Creator and describe what I want. For the YouTube pipeline super skill, I did a stream-of-consciousness prompt:

> "I want this YouTube pipeline skill. I want it to use the YouTube search. I want it to send results to NotebookLM. And if I ask for a deliverable, I want it brought back."

That's the idea, in way too many words. The Skill Creator builds the skill, tells you what it did, and asks if you want to run any evals — your call. At that point, our workflow is essentially set up. Skills are ready. It's inside Obsidian. All that's left is to execute.

## Running the workflow: Claude Code + MCP example

Let's run it. For this example, I'll ask Claude Code to search for videos about **Claude Code and MCP**. I want to find the top five MCP servers — but not just the list. I want analysis on:

- How are those videos doing? What's driving views?
- What are the outliers?
- What are the gaps? What can we do to capitalize on them?

And I want Claude Code to take that analysis and create an **infographic** for me.

That's the exact prompt. I have my YouTube pipeline skill loaded — I could have used natural language, but **anytime you use the slash command, you know it's going to work 100%**.

You can see it start the pipeline: calling the sub-skills, hitting YouTube search and NotebookLM. One great thing about the NotebookLM side is that **all the AI processing is done by NotebookLM** — those are tokens you're not paying for and Claude Code doesn't have to use. It's all offloaded to Google. Thanks, Google.

After about 6 minutes, the analysis is complete. Text-only analysis from NotebookLM is pretty quick. The deliverables can take time — a full slide deck can take up to 15 minutes because there are several images to generate. An infographic is a handful of minutes.

Here's our infographic on MCP. We didn't give it a lot of guidance on the visuals, but it's solid: **Supabase, Context7, Playwright** — it breaks the landscape down into autonomous coding and the essential vibe coding stack. The full list it surfaced: Supabase, Figma, Sentry, PostHog, Context7, Playwright. Can't argue with that.

At the top, you can see it also gave us the full Markdown file for the research.

## Obsidian integration + the `CLAUDE.md` brain within a brain

Remember, this is all happening inside Obsidian. What might look like a normal Markdown file — with things randomly in double brackets — is much more obvious and easier to read in context via Obsidian. Inside Obsidian, the same document shows:

- Key takeaways, with headings
- **Backlinks** to the other articles it's related to
- Its place in the **graph view**

But that's not where Obsidian's value ends. The real value is that I have — see the left panel — all these Markdown files which, **in aggregate**, show Claude Code how I work.

And that's where `CLAUDE.md` comes in. `CLAUDE.md` is the **brain within a brain**. If this vault is the second brain of mine where I have all these ideas, then `CLAUDE.md` is the brain within the brain that tells Claude what this all means — in terms of conventions for how to talk to me, how to give me deliverables, how I want things done.

Over time the vault grows and grows. But `CLAUDE.md` can grow along with it — trained and learning alongside this corpus of knowledge. It's as simple as telling Claude Code:

> "Can we update `CLAUDE.md` so it better reflects my work style, analysis, and output preferences based on our latest conversations?"

Something as broad as that is enough for Claude to go nuts with it. If you want to be more specific, you can be. It's flexible — up to you.

Over time, that relationship between Claude Code and Obsidian is what improves performance. Doing this over a week won't have much effect. Over a month, definitely. Over a year and hundreds of documents and conversations, it will have a **huge lasting effect**.

## Closing thoughts

That's where I'll leave you today. I hope you got more out of this than just this particular workflow — and a little inside view of how I do my content research. The big sell here is that we can take the specifics away: all you need is *some* workflow that helps *you*, in whatever it is you do. If we can take that workflow, turn it into skills, and even turn a mass of skills into a single skill plugged into this pipeline — then everything ends up helping everything else. On the long term, tons of value there.

Let me know in the comments what you thought. As always, if you want to learn more about Claude Code, check out the Claude Code Masterclass inside Chase AI Plus — link in the comments.
