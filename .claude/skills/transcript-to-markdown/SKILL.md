---
name: transcript-to-markdown
description: Convert a raw .txt transcript (typically from the youtube-transcript skill, but any prose transcript works) into a well-structured Markdown document with headings, paragraphs, bullet lists, bolded key terms, and an optional TL;DR — without summarizing or dropping content. Use this skill whenever the user wants to turn a transcript, caption dump, interview, lecture, or podcast text file into readable Markdown, clean up an auto-generated transcript, add structure/headings to a wall of text, or chain transcript → notes. Trigger even if the user says "format this transcript", "make this readable", or "organize this text" without using the word "markdown".
---

# Transcript → Markdown

Transform a raw, unstructured transcript (no punctuation, no paragraph breaks, or auto-caption-style prose) into a readable Markdown document that a human would want to read or skim. **Preserve all substantive content** — this is a formatting and structuring pass, not a summary.

## Inputs and outputs

- **Input**: path to a `.txt` file (most often produced by the `youtube-transcript` skill).
- **Output**: a `.md` file written alongside the input, with the same base name (e.g. `foo.txt` → `foo.md`). If a file by that name exists, overwrite only if the user confirmed; otherwise append a `-structured` suffix.
- Announce the output path at the end so downstream skills (e.g. a master skill chaining transcript → markdown → notes) can pick it up.

### Parse the metadata header first

If the input begins with a `---`-fenced YAML block (as produced by `youtube-transcript`), parse it before reading the body. Use those fields to:

- Fill the H1 title from `Title:` (better than inferring from the filename).
- Render a **Source** line at the top of the document using `URL`, `Channel`, `ChannelURL`, `Uploaded`, and `Duration`. The exact template is below.
- Treat `Source: faster-whisper-tiny` as a signal that punctuation/spelling in the body is model-generated — be slightly more willing to fix obvious transcription errors. `Source: youtube-captions ...` means YouTube's own captions, which have their own error profile (missing punctuation, rolling-window artifacts already deduped).

If the header is missing (e.g. the `.txt` didn't come from the YouTube skill), fall back to inferring the title from the filename or the opening sentence, and omit the Source line — **don't fabricate a URL or channel**.

### Source line template

When a header is present, render this block immediately under the H1 (before the TL;DR):

```markdown
> **Source:** [{Title}]({URL}) — [{Channel}]({ChannelURL}) · {Uploaded} · {Duration}
> *Transcript generated via `{Source}`.*
```

Omit any field that's empty. If there's no `ChannelURL`, use plain text for the channel name. If `Title` and `URL` are both missing, drop the blockquote entirely.

## How to structure the Markdown

Read the full transcript before writing anything. You need the whole arc to pick sensible section boundaries and identify what the key terms actually are. Then produce a document in this shape:

```markdown
# {Video / transcript title}

> Source: {filename or original URL if evident from the text}

## TL;DR

- {3-6 bullets capturing the main takeaways in the speaker's own framing}

## {Section heading 1}

{Paragraphs. Merge run-on caption fragments into real sentences with punctuation.
Bold **key terms** and **named tools/concepts** the first time they appear in
a meaningful way. Use bullet lists when the speaker is enumerating steps or items.}

## {Section heading 2}

...
```

### Rules that matter

1. **Don't summarize the body.** The TL;DR block is the only place where you condense. Below it, every idea, example, caveat, and aside from the transcript should still be present — just in proper prose. If you find yourself dropping a sentence because it feels redundant, stop: the speaker probably said it intentionally (for emphasis, humor, or to introduce a transition).
2. **Fix punctuation and sentence boundaries.** Auto-captions often arrive as one endless stream. Add periods, commas, quotation marks, question marks. Capitalize proper nouns. Fix obvious transcription errors when you're highly confident (e.g. "cloud code" → "Claude Code" when context makes it unambiguous); otherwise leave the original wording alone.
3. **Remove filler sparingly.** You can clean up "um", "uh", "you know", and repeated false starts ("I was — I was going to say...") because they add no information and make the text harder to read. Don't remove hedges or qualifiers that carry meaning ("I think", "probably", "in most cases").
4. **Section headings should reflect the content**, not be generic like "Introduction" or "Part 1". If the speaker walks through five tools, use the tool names. If they tell a story with a turning point, name the turning point. Aim for ~4–10 sections for a typical 10–30 minute video; more if the transcript is long.
5. **Bolding is for signposting, not decoration.** Bold terms that a reader skimming the doc should notice — product names, named concepts, numbered steps. If everything is bold, nothing is.
6. **Preserve quotes and specific numbers verbatim.** If the speaker quotes someone or cites a figure, put it in the Markdown exactly as they said it.
7. **No hallucinated content.** Do not add links, references, or facts that aren't in the transcript. If the speaker mentions a URL or tool name without details, that's fine — don't fabricate detail to fill the gap.

### Inferring the title

If the filename is descriptive (e.g. `Claude_Code__NotebookLM__Obsidian__GOD_MODE.txt`), convert it to a human title for the H1. Otherwise pick a title from the transcript's opening statement of topic. If neither works, ask the user.

## Workflow

1. Read the input `.txt` end-to-end.
2. Draft the TL;DR bullets (this also forces you to identify the document's arc).
3. Pick section boundaries based on topic shifts, not time or paragraph count.
4. Write the full structured Markdown in one pass. Don't leave `[...]` placeholders — if a section is thin, it's thin; don't pad it.
5. Write the output file. Print the output path on its own line at the end so a caller parsing stdout can grab it.

## Example (condensed)

**Input (excerpt):**

```
so today we're going to talk about claude code and how you can combine it
with notebook lm to build a research workflow the first thing you need to
do is install claude code which you can get from anthropic's website then
you'll want to also get notebook lm which is a google product...
```

**Output (excerpt):**

```markdown
# Claude Code + NotebookLM: A Research Workflow

## TL;DR

- Combines **Claude Code** and **NotebookLM** into a single research loop
- Start by installing Claude Code from Anthropic's website
- NotebookLM is the Google side of the workflow
- ...

## Setting up the tools

Today we're going to talk about **Claude Code** and how you can combine it with **NotebookLM** to build a research workflow. The first thing you need to do is install Claude Code, which you can get from Anthropic's website. Then you'll want to also get NotebookLM, which is a Google product...
```

Notice: punctuation added, tool names bolded on first substantive mention, paragraphs formed, content fully preserved.
