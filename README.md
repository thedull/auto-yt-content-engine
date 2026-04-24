# Content — research + course pipeline

A self-contained repo that bundles:

- **Claude Code skills** for end-to-end YouTube research (search → transcribe → structure → NotebookLM → synthesize).
- A **worked example**: a full Playwright course (slides + video + narrated deck) distilled from 15 community tutorials.
- **Seed sources** used to bootstrap the pipeline design.

Everything needed to reproduce the example — or run the pipeline on a new topic — is tracked here.

---

## Repo layout

```
Content/
├── .claude/
│   ├── skills/                      # Claude Code skills (project-scoped)
│   │   ├── youtube-research-pipeline/   # orchestrator (/youtube-research-pipeline)
│   │   ├── youtube-transcript/          # captions + whisper fallback
│   │   ├── transcript-to-markdown/      # structure raw transcripts
│   │   ├── notebooklm/                  # NotebookLM CLI wrapper
│   │   └── research-to-course/          # bundle → curated reveal.js deck
│   ├── setup.sh                     # recreates Python venvs from requirements
│   └── settings.local.json          # per-clone settings (gitignored)
├── playwright-beginners-course/     # the example output (reveal.js deck + assets)
│   └── README.md                    # how to render and present the deck
├── sources/                         # seed material (design notes, reference docs)
├── .gitignore
└── README.md                        # (this file)
```

---

## Prerequisites

The skills shell out to two binaries and pull Python deps via `uv`:

- **[uv](https://docs.astral.sh/uv/)** — for fast venv + pip installs
  `brew install uv` (macOS) or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **ffmpeg** — required only when transcribing videos without captions (whisper path)
  `brew install ffmpeg` (macOS) or `apt install ffmpeg`
- **[Claude Code](https://claude.com/claude-code)** — to invoke the skills

---

## First-time setup

```bash
git clone <this-repo>
cd Content
./.claude/setup.sh
```

`setup.sh` creates two project-local venvs:

- `.claude/skills/youtube-transcript/.venv/` — `yt-dlp`, `faster-whisper` (~190 MB)
- `.claude/skills/notebooklm/.venv/` — `notebooklm-py` (~140 MB)

Both are gitignored. Re-running the script is safe and upgrades in place.

---

## Running the pipeline

Open the repo in Claude Code. From any conversation:

```
/youtube-research-pipeline <subject>, top <N>, save to <output-path>
```

Example:

```
/youtube-research-pipeline Kubernetes operators, top 15, save to ./k8s-operators
```

The pipeline will:

1. **Search & rank** — yt-dlp pulls ~30 candidates, ranks by `views + 10 × likes`, keeps top N
2. **Transcribe** — captions when available, `faster-whisper` (tiny) otherwise
3. **Structure** — each transcript becomes a well-sectioned Markdown doc
4. **Upload to NotebookLM** — all docs become sources in a fresh notebook
5. **Synthesize** — Claude reads the whole corpus and writes a cross-cutting summary
6. **Generate deliverables** — NotebookLM produces a slide deck + video overview

Every stage is idempotent; re-invoking with the same output path resumes from the first incomplete stage.

See [`playwright-beginners-course/README.md`](./playwright-beginners-course/README.md) for a complete worked example — the 15-video Playwright research bundle that shipped with this repo.

### Optional follow-up: build a presentable course deck

The pipeline output is a research bundle (transcripts, master summary, NotebookLM artifacts) — useful for reference but not a polished presentation. To turn the same corpus into a hand-curated reveal.js slide deck (~120-180 slides), invoke the `research-to-course` skill:

> "Turn the markdown files in `./playwright-beginners-course/` into a reveal.js course deck."

You'll be asked four questions up-front (audience, depth, language scope, adjacent topics), then Claude synthesizes the corpus into a single `course.md` plus any SVG diagrams. Render with `npx reveal-md <bundle>/course.md --watch`.

Kept separate from the pipeline because the synthesis is heavy (~1 hour of model time) and not every research project warrants a full deck.

---

## Skill overview

| Skill | Invoked as | What it does |
|---|---|---|
| `youtube-research-pipeline` | `/youtube-research-pipeline` | Top-level orchestrator; chains the others |
| `youtube-transcript` | *(internal)* | Fetches YouTube captions; whisper-transcribes if none |
| `transcript-to-markdown` | *(internal)* | Structures raw transcripts into readable Markdown |
| `notebooklm` | *(internal + CLI)* | Wraps the `notebooklm-py` CLI for notebook management |
| `research-to-course` | *(intent-based)* | Curates a research bundle into a reveal.js course deck |

The internal skills are directly invokable too — check each skill's `SKILL.md` for standalone usage.

---

## Design notes

- **Portable paths.** All skills reference `${CLAUDE_PROJECT_DIR}` (set by the Claude Code harness) instead of `$HOME`. Clone this repo anywhere and it works without editing.
- **Python deps via uv.** venvs are recreated from `requirements.txt` rather than committed. `setup.sh` is the single entry point.
- **Claude Code discovery.** Skills in `.claude/skills/` are auto-discovered by Claude Code when working in this directory. Project copies take precedence over anything in `~/.claude/skills/`.
- **Gitignored state.** Pipeline artifacts (`.notebook-id`, `.tasks.json`, `errors.log`) and Claude Code local state (`settings.local.json`, `statsig/`) are excluded from the repo. The **output folders** themselves (e.g. `playwright-beginners-course/`) are intentionally **committed** — they are the research deliverables.

---

## License & attribution

Source transcripts are derivative works of the original YouTube creators — credit them when reusing content. The skill code, pipeline design, and synthesized write-ups in this repo are original work.
