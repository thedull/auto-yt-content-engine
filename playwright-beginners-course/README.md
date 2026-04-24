# Playwright Course for Beginners

A self-contained research bundle and trainer-ready course distilled from the 15 most-watched Playwright tutorials on YouTube (~50 hours of source material).

The pipeline that built this folder lives at `~/.claude/skills/youtube-research-pipeline/` (see [Regenerating from scratch](#regenerating-from-scratch) below).

---

## Folder layout

```
playwright-beginners-course/
├── README.md                # this file
├── course.md                # ⭐ the reveal.js deck (~190 slides)
├── master-summary.md        # cross-cutting research synthesis
├── videos.json              # ranked video list from yt-dlp
├── transcripts/             # 15 raw .txt transcripts (with YAML metadata headers)
├── markdown/                # 15 structured .md transcripts (the corpus the deck was built from)
├── assets/                  # SVG diagrams referenced by course.md
├── deliverables/            # NotebookLM-generated artifacts
└── .notebook-id, .tasks.json  # internal state from the pipeline run
```

### `course.md` — the main deliverable

A reveal.js Markdown deck. ~190 slides across 18 modules + 4 appendices. JS/TS is the primary track; Python, Java, .NET in appendices. Speaker notes cite the source video for every claim. See [How to run the slides](#how-to-run-the-slides).

Built via the `research-to-course` skill (see [Regenerating the deck](#regenerating-the-deck) below) — not part of the auto-pipeline because course curation is heavy (~1 hour of model time) and not every research bundle needs a presentation.

### `master-summary.md`

A research synthesis (themes, consensus, disagreements, gaps) across all 15 sources. Useful as a quick-reference companion to the deck — read this if you want the *what* without the *how*.

### `markdown/`

15 structured Markdown transcripts (one per video), each with YAML metadata header, TL;DR, and section breakdown. This is the curated corpus the deck and master summary were built from.

### `transcripts/`

The raw plain-text transcripts (15 files). Sourced from YouTube captions where available, with `faster-whisper-tiny` as fallback for videos without captions. Each file starts with a YAML metadata block (title, channel, URL, duration, transcript source).

### `assets/`

SVG diagrams embedded in the deck:

- `architecture.svg` — Playwright client → server → browser flow
- `fixture-lifecycle.svg` — `beforeEach` / test body / `afterEach` lifecycle

Both are designed for the deck's black theme (dark fills, light text). Edit directly in any text editor or vector tool.

### `deliverables/`

NotebookLM-generated artifacts from the same corpus:

- `slides.pdf` (19 MB) — *Playwright Automation Architecture* slide deck
- `video.mp4` (23 MB) — *A Deep Dive into Playwright* video overview

These are an alternative presentation of the same material — useful for sharing with stakeholders who don't want to sit through a full course.

### `videos.json`

The ranked list of source videos with view/like counts, durations, and YouTube IDs. Used by the pipeline; useful for citation.

---

## How to run the slides

### Quickest path: `reveal-md`

```bash
npx reveal-md ./course.md --watch
```

Opens the deck in your browser at `http://localhost:1948`. `--watch` hot-reloads on save.

### Export to a static site

```bash
npx reveal-md ./course.md --static _site
```

Writes a fully self-contained `_site/` directory you can host anywhere (GitHub Pages, S3, Netlify).

### Export to PDF

```bash
npx reveal-md ./course.md --print course.pdf
```

Uses headless Chromium to print every slide to a single PDF.

### Keyboard shortcuts (during presentation)

| Key | Action |
|---|---|
| `→` / `↓` | Next slide / sub-slide |
| `←` / `↑` | Previous |
| `S` | Open speaker notes window |
| `F` | Fullscreen |
| `Esc` | Slide overview grid |
| `B` | Black out screen |
| `?` | Show all shortcuts |

### Slide separator convention

- `---` (3 dashes) on a blank line → new horizontal slide
- `----` (4 dashes) on a blank line → new vertical sub-slide

This is `reveal-md`'s default. If you use vanilla reveal.js (Markdown plugin), pass:

```
data-separator="^\r?\n---\r?\n$"
data-separator-vertical="^\r?\n----\r?\n$"
```

### Customizing the look

The deck embeds a `<style>` block (right after the YAML front-matter) that tunes code-block size, table density, and image max-height. Edit there for global tweaks.

**Important**: stick to `em`, `%`, or unitless multipliers — never `vw`/`vh`. Reveal.js scales each slide via CSS `transform`, and viewport-relative units bypass that scaling, breaking fullscreen and slide-overview modes.

---

## Resources

### Source videos (full list)

Sorted by view count (descending).

| Channel | Video | Length | Views |
|---|---|---|---:|
| Automation Step by Step (Raghav Pal) | [Playwright Beginner Tutorial 1](https://www.youtube.com/watch?v=4_m3HsaNwOE) | 13 min | 694,006 |
| TestMu / LambdaTest (Kaushik) | [Playwright with TypeScript](https://www.youtube.com/watch?v=wawbt1cATsk) | 5h 41m | 305,441 |
| Mukesh Otwani | [Playwright Automation for Beginners (JS)](https://www.youtube.com/watch?v=pq20Gd4LXeI) | 8h 17m | 223,973 |
| Testopic (Victor) | [What is Playwright?](https://www.youtube.com/watch?v=wGr5rz8WGCE) | 12 min | 196,254 |
| Testing Funda (Zeeshan) | [Playwright with JavaScript Full Course](https://www.youtube.com/watch?v=qhb1_JqJZyM) | 9h 55m | 157,438 |
| Testers Talk (Bakkappa) | [Playwright TS Full Course 2026](https://www.youtube.com/watch?v=788GvvcfwTY) | 8h 55m | 157,088 |
| Testers Talk (Bakkappa) | [Playwright Tutorial Full Course 2026 (JS)](https://www.youtube.com/watch?v=2poXBtifpzA) | 6h 55m | 153,576 |
| SDET-QA (Pavan) | [Setup & Writing Tests Session 1](https://www.youtube.com/watch?v=ziuIDwX18h4) | 1h 38m | 145,070 |
| Automation Step by Step (Raghav Pal) | [Playwright Python 1](https://www.youtube.com/watch?v=VZ5LU8vHT0s) | 44 min | 113,813 |
| Execute Automation | [Playwright vs Selenium](https://www.youtube.com/watch?v=X08AwI35xdo) | 11 min | 77,406 |
| Playwright (official) | [Get Started with VS Code (2025)](https://www.youtube.com/watch?v=WvsLGZnHmzw) | 20 min | 72,271 |
| Python Simplified | [Web Scraping + CAPTCHA Bypass](https://www.youtube.com/watch?v=RGR5Xj0Qqfs) | 21 min | 71,997 |
| Cosden Solutions (Darius) | [React Testing with Playwright](https://www.youtube.com/watch?v=3NW0Mz943_E) | 33 min | 65,234 |
| freeCodeCamp.org (Bo KS) | [Software Testing — Playwright + AI](https://www.youtube.com/watch?v=jydYq7oAtD8) | 1h 03m | 58,973 |
| TestMu / LambdaTest (Kaushik) | [Playwright Java Tutorial](https://www.youtube.com/watch?v=MOuzZJJ6cLI) | 5h 02m | 48,719 |

Full metadata in `videos.json`.

### Official references

- **Docs**: [playwright.dev](https://playwright.dev)
- **GitHub**: [microsoft/playwright](https://github.com/microsoft/playwright)
- **Discord**: linked from the docs homepage
- **VS Code extension**: search "Playwright Test for VSCode" by Microsoft

---

## Regenerating from scratch

The research bundle (transcripts, master summary, NotebookLM artifacts) was produced by the `youtube-research-pipeline` skill. To rebuild from scratch (or run the pipeline on a different topic):

```
/youtube-research-pipeline <subject>, top <N>, save to <path>
```

Example:

```
/youtube-research-pipeline Playwright course for beginners, top 15, save to ./playwright-beginners-course
```

The pipeline is idempotent — re-running it skips work already on disk.

### Regenerating the deck

`course.md` and the SVG assets are *not* produced by the pipeline. They come from a separate skill, `research-to-course`, which curates an existing research bundle into a presentable reveal.js deck. To rebuild just the deck:

> "Turn the markdowns in `./playwright-beginners-course/` into a reveal.js course deck."

The skill will ask four questions up-front (audience, depth, language scope, adjacent topics in scope) and then write a fresh `course.md` plus any SVG assets. The synthesis is heavy — expect a long session and ~3000-5000 lines of output for a comprehensive course.

---

## License & attribution

Source material is YouTube-hosted public content. Transcripts are derivative works of the original creators — credit them when reusing. The `course.md` deck is original synthesis (curation + structure + commentary); transcripts and metadata are the property of the respective channels.
