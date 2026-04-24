---
name: research-to-course
description: Turn a research bundle (a folder of structured Markdown transcripts + a master summary) into a curated, presentable reveal.js course deck. Use when the user asks to "build a course from these markdowns", "turn this research into a deck", "create a presentation from the transcripts", "make a reveal.js deck", or any request that means "synthesize this corpus into a slide deck I can present." Typical follow-up to the `youtube-research-pipeline` skill; works on any folder containing `markdown/*.md` plus an optional `master-summary.md`.
---

# Research → Course (reveal.js deck)

Given a folder containing structured Markdown transcripts and an optional cross-cutting summary, produce a single curated reveal.js deck (`course.md`) plus any supporting SVG assets. You act as **expert curriculum designer** — synthesizing, not concatenating.

## When to use this skill

After the user has a research bundle on disk — typically the output of `youtube-research-pipeline`:

```
<bundle>/
├── markdown/<id>.md           # one structured transcript per source
└── master-summary.md          # optional but useful: themes/consensus/gaps
```

The deliverable goes alongside it:

```
<bundle>/
├── course.md                  # ⭐ the reveal.js deck
├── assets/                    # SVG diagrams referenced by the deck
└── README.md                  # how-to-render instructions (update existing)
```

---

## Ask the user up-front

Before drafting the curriculum, confirm four things via `AskUserQuestion` (or accept defaults if the user gave them in the prompt):

1. **Language/tech scope** — primary track + what goes in appendices.
2. **Target audience** — beginner / intermediate practitioner / experienced switcher.
3. **Depth** — quick intro (~30-50 slides) / core (~60-90) / comprehensive (~120-180).
4. **Adjacent topics in scope** — specific peripheral areas (CI/CD, cloud, AI tooling, etc.). Multi-select.

These four answers shape the curriculum. Don't skip them — a course built without knowing the audience drifts into either trivia or jargon.

---

## Curation rules (non-negotiable)

These come from real reveal.js gotchas — encode them in your output.

### Content

- **One concept per slide.** Walls of text don't work in reveal.js. Long explanations belong in `Note:` (speaker notes), not on the slide body.
- **Code is first-class.** Every "how" gets a code fence on its own slide, not buried in prose. Heavy code → vertical sub-slides (`----`).
- **Cite per slide in speaker notes.** Format: `Source: <Channel> — <video title>`. Lets the user trace any claim back to the original transcript without polluting the visible deck.
- **Where the corpus disagrees, pick a side and say why.** Use the `master-summary.md`'s "Disagreements" section as input. Don't present "well, it depends" — present a recommendation with a reason.
- **Where the corpus has gaps, name them.** Add a "Beyond this course" slide so the deck doesn't pretend completeness.
- **No lifted content.** Rephrase in your voice; quote the original verbatim only when the original phrasing is itself the lesson (a memorable soundbite).

### reveal.js format

Use this exact convention for compatibility with `reveal-md`'s defaults:

```markdown
---
title: <Course title>
theme: black
highlightTheme: monokai
revealOptions:
  transition: slide
  hash: true
  controls: true
  progress: true
  slideNumber: 'c/t'
---

<style>
.reveal pre { width: 100%; box-shadow: none; margin: 12px auto; }
.reveal pre code {
  font-size: 0.58em;
  line-height: 1.4;
  padding: 0.6em 0.9em;
  max-height: 620px;
  border-radius: 6px;
}
.reveal :not(pre) > code { font-size: 0.78em; padding: 2px 6px; }
.reveal table { font-size: 0.55em; margin: 10px auto; }
.reveal table th, .reveal table td { padding: 6px 12px; }
.reveal ul, .reveal ol { font-size: 0.82em; }
.reveal blockquote { font-size: 0.8em; }
.reveal img { max-height: 560px; background: transparent; border: none; box-shadow: none; }
.reveal h2 { margin-bottom: 0.4em; }
.reveal section > p { font-size: 0.85em; }
</style>

# Title slide
```

- **`---` (3 dashes)** on a blank line → new horizontal slide
- **`----` (4 dashes)** on a blank line → new vertical sub-slide
- **`Note:` block** at the end of a slide → speaker notes (visible with `S` key)

### CSS sizing — only relative units

**Never use `vw`/`vh`/`vmin`/`vmax`.** Reveal.js scales each slide via CSS `transform`; viewport-relative units bypass that scaling and break in fullscreen and slide-overview modes. Use `em`, `%`, or unitless multipliers (and fixed `px` is acceptable since reveal scales the whole transform).

The CSS block above is the canonical baseline. Tweak font sizes within these constraints, but never reach for `vw`/`vh`.

### Code-block font size

`0.58em` (the value above) renders code at roughly 60-65% slide width — the sweet spot. Going lower makes code unreadable; going higher pushes wide lines off the slide.

### Tables for command listings

Inline shell comments after `#` may render poorly inside fenced ```bash blocks (the highlighter strips formatting). For multi-command reference slides, use a Markdown table (Command | Does) instead of a fenced bash block with comments.

---

## SVG diagrams (when ASCII falls short)

For any concept where ASCII art would be ambiguous or ugly (architecture, lifecycles, flows), emit an SVG into `<bundle>/assets/<name>.svg` and reference it via `![alt](assets/<name>.svg)`.

### SVG style guide

- **Design for dark theme** (theme: black). Use dark fills (`#1e2a3a`, `#0f2922`) with light text (`#ffffff`, `#c0c8d0`) and bright accent strokes.
- **Use `viewBox`** for scalability; avoid hardcoded `width`/`height`.
- **Cap height in the deck CSS** (the `max-height: 560px` rule above) so SVGs don't dominate slides.

### Arrow markers — the trap

Use this exact marker spec for rightward/auto-rotated arrows:

```xml
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#e8e8e8"/>
  </marker>
</defs>
```

`orient="auto"` rotates the marker so its **+X axis** aligns with the line direction. The triangle's tip must therefore be at `(10, 5)` (the +X edge) — *not* at `(5, 10)`. Get this wrong and arrows on vertical lines come out pointing sideways.

`refX="9" refY="5"` aligns the tip with the line's endpoint.

---

## Structure of `course.md`

A typical comprehensive deck:

| Section | Slides | Purpose |
|---|---|---|
| Welcome / how to use | 2 | Set expectations, format guide |
| Module 1 — What is X? | 5-7 | Definition, value prop |
| Module 2 — Architecture | 5-7 | How it works under the hood |
| Module 3 — Setup | 8-12 | Get the audience running |
| Modules 4-N — Curriculum | varies | One concept per module, ~10 slides each |
| Beyond this course | 1-2 | Honest scope statement |
| Appendix A, B, C | 4-6 each | Secondary tracks (other languages, edge cases) |
| Source attribution | 2 | Tabular list of all sources cited |
| Closing | 1-2 | Q&A logistics, where to learn more |

Total: 120-180 slides for a comprehensive course. Adjust to match the user's depth choice.

Pull source metadata (titles, URLs, channel) from each `.md`'s Source blockquote — `transcript-to-markdown` writes that header from the YAML metadata. The source-attribution appendix should list every video with its YouTube link.

---

## Verification checklist

After writing the file, confirm:

```bash
# Sanity-check size
wc -l <bundle>/course.md   # expect 2500-4500 lines for 120-180 slides

# Confirm separator counts
grep -c "^---$"   <bundle>/course.md   # horizontal slide count + 2 (front-matter fences)
grep -c "^----$" <bundle>/course.md   # vertical sub-slide count

# No viewport-relative units in CSS
grep -n "vw\|vh\|vmin\|vmax" <bundle>/course.md   # should be empty

# All SVG assets exist
grep -oE "assets/[^)]+\.svg" <bundle>/course.md | sort -u | while read p; do
  test -f "<bundle>/$p" && echo "✓ $p" || echo "✗ MISSING: $p"
done
```

Then suggest the render command in your final report:

```bash
npx reveal-md <bundle>/course.md --watch
```

---

## Updating the bundle's README

If `<bundle>/README.md` exists (typical when this follows `youtube-research-pipeline`), append a "How to run the slides" section pointing at `course.md` and the keyboard shortcuts. Don't rewrite the whole README — just add the deck section.

If it doesn't exist, create one with: folder layout, deck render commands, and source attribution table.

---

## What this skill does NOT do

- It does **not** re-fetch transcripts. The corpus must already exist on disk (output of `youtube-research-pipeline` or any compatible bundle).
- It does **not** generate slides via NotebookLM. That's a different artifact (covered by the pipeline). The output here is a hand-curated reveal.js deck — fundamentally different (deeper curation, presentable by a human, editable).
- It does **not** manage rendering / hosting. The output is a portable Markdown file; rendering is up to the user (`reveal-md`, vanilla reveal.js, GitHub Pages, etc.).
