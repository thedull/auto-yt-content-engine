---
name: youtube-research-pipeline
description: End-to-end YouTube research pipeline. Accepts (a) a research subject — finds and ranks the top videos by view + like count, (b) a list of YouTube URLs from the command line, or (c) a JSON file with URLs (and optional subject). Extracts transcripts, structures them as Markdown, synthesizes a master summary, then asks the user which deliverables to produce — any combination of an MD course (reveal.js deck) and NotebookLM artifacts (slide deck, video, audio podcast, quiz, mind map, flashcards, infographic, report). Trigger when the user wants to research a topic from YouTube videos — whether they name a subject, paste URLs, or hand over a JSON file of URLs. Also triggers on "learn everything about X from YouTube," "build a knowledge base from these videos," or any request that combines YouTube + NotebookLM.
---

# YouTube Research Pipeline

Given a subject, produce a self-contained research folder. The exact contents of `deliverables/` depend on what the user picks from the artifact menu (asked after Stage 2):

```
<output-root>/
├── videos.json              # ranked video list from yt-dlp
├── transcripts/<id>.txt     # one per video (with YAML metadata header)
├── markdown/<id>.md         # structured markdown per video
├── master-summary.md        # Claude-synthesized cross-cutting summary  (always)
├── course.md                # reveal.js MD course                       (if selected)
├── assets/                  # diagrams referenced by course.md           (if selected)
├── deliverables/            # any selected NotebookLM artifacts
│   ├── slides.pdf           #   slide deck
│   ├── video.mp4            #   video
│   ├── audio.mp3            #   podcast
│   ├── quiz.md              #   quiz
│   ├── flashcards.md        #   flashcards
│   ├── mind-map.json        #   mind map (sync, instant)
│   ├── infographic.png      #   infographic
│   └── report.md            #   report
├── .notebook-id             # only if any NotebookLM artifact was picked
├── .artifacts.json          # the user's menu selection (cached for resume)
└── errors.log               # anything that was skipped and why
```

This skill chains four existing skills (`youtube-transcript`, `transcript-to-markdown`, `notebooklm`, `research-to-course`) plus two bundled scripts. Your job as the invoking agent is orchestration + synthesis. The scripts do the mechanical parts.

## Detect input mode

The skill accepts three input shapes. Pick the Stage 1 branch from the user's invocation:

| Input shape | Detection | Stage 1 branch | `.input-mode` value |
|---|---|---|---|
| Bare subject ("React performance") | No `youtube.com`/`youtu.be` URL anywhere in the args, no `.json` file path | **1a — search** | `subject` |
| One or more YouTube URLs | At least one arg matches `https?://(www\.)?(youtube\.com|youtu\.be)/` | **1b — metadata fetch** | `urls` |
| JSON file with URLs | Arg ends with `.json` (or `--file foo.json`) and the file exists | **1b — metadata fetch** | `urls` |
| Mixed (URLs + a subject string) | URLs present alongside non-URL prose | **1b**, treat the prose as the subject | `urls` |

Drop a one-line marker file at `<output-root>/.input-mode` (literally the string `subject` or `urls`) so Stage 4 can pick the right wording.

## Ask the user up-front

Confirm what you need (skip questions the user already answered in their prompt or in the JSON file):

1. **Subject** — the research topic. Resolution priority:
   1. Explicit `--subject "..."` flag
   2. `subject` key in the JSON file (URL mode)
   3. The bare-string portion of the invocation (mixed mode)
   4. Ask the user
   The subject titles the NotebookLM notebook + the master-summary header + the default output slug.
2. **Top N** — *subject mode only*, default **10**, cap at 50 (NotebookLM's per-notebook source limit). Skip in URL mode (the URL list is already the input).
3. **Output root** — *optional user-defined directory* (e.g. an Obsidian vault path). If the user doesn't specify one, default to `./research/<subject-slug>/` under the current working directory.

Slugify the subject for the default path: lowercase → replace non-alphanumerics with `-` → collapse repeated dashes → trim leading/trailing dashes → cap at 60 chars.

If the user provided an output root, use it **as-is** (no `<subject-slug>` subfolder appended — they chose the path deliberately, likely inside a vault structure they've already organized).

## Pipeline overview

```
[Stage 1a/1b] subject → search & rank   OR   URLs/JSON → fetch metadata
[Stage 2]  per-video: transcript .txt → structured .md   (parallel, batch of 5)
─── ASK ARTIFACT MENU ───  (cached to .artifacts.json)
[Stage 3]  create NotebookLM notebook → upload all .md   (skipped if no NotebookLM artifacts picked)
[Stage 4]  Claude reads all .md → master-summary.md      (always runs)
[Stage 4b] research-to-course → course.md                (only if "MD course" picked)
[Stage 5]  NotebookLM: generate selected artifacts       (parallel)
[Stage 6]  download selected artifacts
```

Every stage is **idempotent** — rerunning the skill on the same subject/output skips already-completed work. If a stage was interrupted, the skill can resume. The user's artifact selection is cached to `<output-root>/.artifacts.json` on first run so resumes don't re-prompt.

---

## Stage 1a — Search and rank (subject mode)

Run the bundled script using the `youtube-transcript` skill's venv (it already has `yt-dlp` installed):

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv/bin/python \
  ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-research-pipeline/scripts/search_and_rank.py \
  "<subject>" --top <N> --out <output-root>/videos.json
```

The script overfetches (30 results by default) then ranks by `view_count + 10 × like_count` and writes the top N. Stderr shows the ranked list so you can glance at what was picked.

**Skip this stage if `videos.json` already exists** and contains ≥ N entries.

If yt-dlp fails with zero results, it's usually because YouTube broke the extractor. Suggest to the user:

```bash
VIRTUAL_ENV=${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv uv pip install -U yt-dlp
```

Then retry Stage 1a.

---

## Stage 1b — Fetch metadata from URLs (URL mode)

Use this branch when the user provided URLs (CLI args) or a JSON file. The script writes a `videos.json` in the **same shape** as Stage 1a, so Stages 2–6 don't need to know which branch ran.

### CLI URLs

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv/bin/python \
  ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-research-pipeline/scripts/fetch_metadata.py \
  <url1> <url2> ... --out <output-root>/videos.json
```

### JSON file

The JSON file may be either a `{ "subject": "...", "urls": [...] }` object or a bare URL array:

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv/bin/python \
  ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-research-pipeline/scripts/fetch_metadata.py \
  --file <path-to-urls.json> --out <output-root>/videos.json
```

If the JSON file has a `subject` key and no `--subject` flag was provided on the command line, use that as the subject for the run.

### Idempotency

**Skip this stage if `videos.json` already exists** and contains entries for every requested URL. (Compare the URL list against `videos.json[].url`.)

### Failure modes

If a URL is private, age-restricted, or unavailable, yt-dlp will skip it — the script logs the failure to stderr and continues with the rest. Append any skipped URLs to `<output-root>/errors.log` with the reason. If yt-dlp itself crashes (extractor broken), suggest the same `uv pip install -U yt-dlp` upgrade as Stage 1a.

---

## Stage 2 — Per-video transcript + markdown

Read `videos.json`. For each video, you need two output files:

- `<output-root>/transcripts/<video_id>.txt`
- `<output-root>/markdown/<video_id>.md`

**Skip any video** where the `.md` already exists (idempotency).

### Run in parallel batches of 5

Don't serialize — it's too slow if several videos hit the whisper fallback. Don't go above 5 concurrent either — YouTube will start rate-limiting yt-dlp and multiple whisper runs on CPU compete badly.

For each batch of up to 5 videos, spawn `Agent` tool calls **in a single message** (multiple tool_use blocks) with `subagent_type: general-purpose`. Each subagent does one video end-to-end. Prompt template:

```
You are processing one YouTube video in a larger research pipeline. Do these steps exactly:

1. Run this command to produce the transcript file:
   ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv/bin/python \
     ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/scripts/get_transcript.py \
     "<url>" -o "<output-root>/transcripts/<video_id>.txt"
   If it exits non-zero, report the error and stop — do not proceed to step 2.

2. Read the resulting .txt file (it starts with a YAML metadata header between
   --- fences, followed by the transcript body).

3. Apply the `transcript-to-markdown` skill to convert it. Write the output to:
   <output-root>/markdown/<video_id>.md
   Follow the SKILL.md at ${CLAUDE_PROJECT_DIR}/.claude/skills/transcript-to-markdown/SKILL.md —
   parse the metadata header, use Title for the H1, render a Source blockquote
   with the real YouTube URL and channel, preserve all content, and produce
   TL;DR + sectioned body.

4. Report back a one-line JSON: {"video_id": "...", "ok": true}
   or {"video_id": "...", "ok": false, "stage": "transcript|markdown", "error": "..."}

Do not ask clarifying questions. Do not report progress. Only the final JSON line.
```

After the batch completes, append any failures (subagent reported `ok: false`, or crashed) to `<output-root>/errors.log` with the video_id, URL, stage, and error message. **Drop failed videos from the list passed to Stage 3** — don't try to upload a nonexistent markdown.

If the `videos.json` flags several videos with no captions (look at the transcript header's `Source:` field after Stage 2 — `faster-whisper-tiny` means whisper ran), warn the user at the start of this stage: "N of M videos lack captions; expect ~3 extra minutes per whisper video on CPU."

---

## Artifact menu — ask the user

Once Stage 2 finishes (per-video markdown is on disk), pause and ask the user which deliverables they want. `master-summary.md` is **always** generated — don't ask about it.

**Skip the prompt if `<output-root>/.artifacts.json` already exists** (resume case) and use the cached selection instead.

Use `AskUserQuestion`. Because it caps at 4 options per question, fan out across two questions:

**Q1 — primary deliverables** (`multiSelect: true`):

| Label | Description |
|---|---|
| MD course (reveal.js) | Curated `course.md` deck via the `research-to-course` skill |
| NotebookLM slide deck | Auto-generated presentation PDF (~5–15 min) |
| NotebookLM video | AI-narrated video walkthrough (~15–45 min) |
| More NotebookLM artifacts… | Show extra options (audio, quiz, mind map, flashcards, infographic, report) |

If the user selects "More NotebookLM artifacts…", ask **Q2** (`multiSelect: true`):

| Label | Description |
|---|---|
| Audio podcast (.mp3) | NotebookLM podcast |
| Quiz (.md) | NotebookLM quiz |
| Mind map (.json) | NotebookLM mind map (instant, sync) |
| Flashcards (.md) | NotebookLM flashcards |
| Infographic (.png) | NotebookLM infographic |
| Report (.md) | NotebookLM report (briefing-doc by default) |

Q2 has 6 options, but `AskUserQuestion` caps at 4. Split into two passes if needed (`Audio / Quiz / Mind map / more…` then `Flashcards / Infographic / Report`), or ask in plain prompt text if the user prefers brevity.

After collecting selections, write the resolved set to `<output-root>/.artifacts.json`:

```json
{
  "md_course": true,
  "notebooklm": ["slide-deck", "video", "audio", "quiz", "mind-map", "flashcards", "infographic", "report"]
}
```

Use only the keys the user picked. The `notebooklm` array drives Stages 3, 5, and 6:

- **If `notebooklm` is empty**, skip Stage 3 entirely (no notebook is created, no upload).
- **If `md_course` is false**, skip Stage 4b.
- **If both are empty/false**, the run ends after Stage 4 with just `master-summary.md` + per-video markdown.

State the implications back to the user before proceeding (e.g. "Generating: MD course + NotebookLM slide deck. Skipping NotebookLM video, audio, quiz… Estimated time: ~20 min.").

---

## Stage 3 — Create notebook and upload markdowns

**Skip this stage entirely if `.artifacts.json`'s `notebooklm` array is empty.** No NotebookLM artifacts means there's no reason to create a notebook or upload sources.

Create the notebook (one command, capture the ID):

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm create "<subject>" --json
```

Parse `id` from the JSON. Save it — every subsequent NotebookLM command needs `-n <id>`.

**Idempotency**: if you already created a notebook for this run, its ID should be cached. Write it to `<output-root>/.notebook-id` the first time and read from there on retry.

Then upload everything:

```bash
NOTEBOOKLM_BIN=${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm \
  python ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-research-pipeline/scripts/upload_to_notebook.py \
  --notebook <id> \
  --dir <output-root>/markdown/
```

The script adds each `.md` then serially waits for each source to finish processing. Its final stdout is a JSON `{added: [...], failed: [...]}` — surface any failures to the user and append them to `errors.log`.

### Command paths

The `notebooklm` CLI lives at `${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm` (populated by `.claude/setup.sh`). All commands below use that full path directly so the pipeline works on a fresh clone without PATH fiddling. The helper script `upload_to_notebook.py` respects the `NOTEBOOKLM_BIN` env var (defaults to `notebooklm` on PATH); the pipeline sets it explicitly.

---

## Stage 4 — Master summary

Read **every** `.md` file in `<output-root>/markdown/`. Don't summarize them one-by-one — read the whole corpus into your context, then synthesize. Opus 4.7's 1M context window comfortably handles 10 transcripts.

Write `<output-root>/master-summary.md` with this structure:

```markdown
# <Subject> — Research Summary

> **Scope:** N YouTube videos on "<subject>", {scope-clause}.
> Generated <YYYY-MM-DD>.

## Sources

- [{Video 1 Title}]({URL}) — {Channel} · {Uploaded} · {Duration}
- [{Video 2 Title}]({URL}) — {Channel} · {Uploaded} · {Duration}
- ...

## Themes

{Cross-cutting topics that surface across multiple videos. Each theme gets a
paragraph explaining the idea and citing which videos discuss it. Don't just
list video-by-video takeaways — find the patterns.}

## Consensus

{Points where most or all videos agree. State the claim plainly, then note how
many sources back it. This is the most load-bearing section — it's the signal
in the noise.}

## Disagreements / Open questions

{Where videos conflict, recommend different tools for the same job, or leave
something unresolved. Name the disagreement concretely, cite the sources, and
if one side has a stronger argument, say so.}

## Gaps

{What's missing from the corpus as a whole. Questions a curious viewer would
ask that no video addresses. This tells the reader where they still need to
dig on their own.}
```

Pull the source metadata (titles, URLs, channel, upload date, duration) from each `.md`'s Source blockquote — it was written by `transcript-to-markdown` from the YAML header. No need to re-parse `videos.json`.

For `{scope-clause}`, read `<output-root>/.input-mode`: if it's `subject`, write `ranked by views + likes`; if it's `urls`, write `provided by user`.

**Skip this stage if `master-summary.md` already exists.**

---

## Stage 4b — MD course (only if selected)

If `.artifacts.json`'s `md_course` is true, invoke the **`research-to-course`** skill on `<output-root>/`. Follow that skill's SKILL.md — it reads `markdown/*.md` + `master-summary.md`, asks the user 4 questions about audience/depth/scope, and writes `course.md` (+ optional `assets/`) into the output root.

Skip this stage if `<output-root>/course.md` already exists. This stage can run in parallel with Stage 5 polling — kick off `research-to-course` after Stage 5 has launched its `generate` calls but while waiting on artifact completion.

---

## Stage 5 — Generate selected NotebookLM artifacts (parallel)

**Skip this stage if `.artifacts.json`'s `notebooklm` array is empty.**

For each selected artifact, fire one `notebooklm generate <type>` command. Run them all **in parallel** (one `Bash` tool_use block per artifact, sent in a single message):

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm generate <type> -n <id> --json
```

The `<type>` token matches the artifact name in `.artifacts.json` exactly: `slide-deck`, `video`, `audio`, `quiz`, `mind-map`, `flashcards`, `infographic`, `report`.

Each returns a `task_id` (or for `mind-map`, the artifact synchronously). Save the map of `{artifact: task_id}` to `<output-root>/.tasks.json`.

### Synchronous artifacts

`mind-map` completes immediately — no polling needed. The `generate` call returns the artifact ID and it's already done.

### Asynchronous artifacts

For everything else, poll via `notebooklm artifact get <task_id>`.

**Do not use `notebooklm artifact wait` or `notebooklm artifact poll`.** They sit on a task-status endpoint that gets stuck reporting `in_progress` even after the artifact has actually completed — the wait will hang until its timeout and never resolve, especially for `video` tasks. Confirmed bug as of 2026-04.

Poll loop (one per async artifact, run in parallel as background `Bash` calls with `run_in_background: true`):

```bash
while :; do
  s=$(${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm artifact get <task_id> -n <id> 2>/dev/null | awk '/^Status:/ {print $2}')
  case "$s" in completed) echo ok; exit 0 ;; failed) echo failed; exit 1 ;; esac
  sleep 30
done
```

Rely on the runtime's task-completion notification — do not sleep/poll the background tasks yourself.

Approximate completion times (set safety caps accordingly):

| Artifact | Typical time | Poll interval | Safety cap |
|---|---|---|---|
| slide-deck | 5–15 min | 30s | 30 min |
| video | 15–45 min | 60s | 60 min |
| audio | 5–15 min | 30s | 30 min |
| quiz | 1–5 min | 15s | 15 min |
| flashcards | 1–5 min | 15s | 15 min |
| infographic | 2–10 min | 30s | 20 min |
| report | 2–10 min | 30s | 20 min |
| mind-map | sync | — | — |

Handle the **failed** case per-artifact: if any one artifact fails, report it but let the others continue. Don't abort the whole stage on a single failure.

### Rate limits

If a `generate` command fails with a rate-limit / HTTP 429 / "quota" error, wait 5 minutes and retry once. If it fails again, drop that artifact, log it, and continue with the others — the user can manually re-run `notebooklm generate <type>` later without re-doing Stages 1–4.

---

## Stage 6 — Download

**Skip this stage if `.artifacts.json`'s `notebooklm` array is empty.**

Make sure `<output-root>/deliverables/` exists first. Then, for each artifact whose Stage 5 task reported `completed`, run the matching download command:

| Artifact | Download command | Output file |
|---|---|---|
| slide-deck | `notebooklm download slide-deck <out>/deliverables/slides.pdf -n <id> -a <task_id>` | `slides.pdf` |
| video | `notebooklm download video <out>/deliverables/video.mp4 -n <id> -a <task_id>` | `video.mp4` |
| audio | `notebooklm download audio <out>/deliverables/audio.mp3 -n <id> -a <task_id>` | `audio.mp3` |
| quiz | `notebooklm download quiz <out>/deliverables/quiz.md -n <id> -a <task_id>` | `quiz.md` |
| mind-map | `notebooklm download mind-map <out>/deliverables/mind-map.json -n <id> -a <task_id>` | `mind-map.json` |
| flashcards | `notebooklm download flashcards <out>/deliverables/flashcards.md -n <id> -a <task_id>` | `flashcards.md` |
| infographic | `notebooklm download infographic <out>/deliverables/infographic.png -n <id> -a <task_id>` | `infographic.png` |
| report | `notebooklm download report <out>/deliverables/report.md -n <id> -a <task_id>` | `report.md` |

Run downloads in parallel — they're fast. Skip any artifact that didn't complete in Stage 5.

Use the full path to the `notebooklm` binary as elsewhere: `${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm`.

---

## Final report

Print a clean summary to the user. **List only the artifacts the user selected** (and indicate which succeeded vs failed):

```
✓ Pipeline complete.

Output root:   <output-root>
Videos:        <n_ok>/<n_requested> processed successfully (<n_failed> skipped — see errors.log)
Summary:       <output-root>/master-summary.md
{if md_course}        MD course:     <output-root>/course.md
{if notebook created} Notebook:      https://notebooklm.google.com/notebook/<notebook_id>
{per selected NotebookLM artifact, on its own line:}
  Slide deck:  <output-root>/deliverables/slides.pdf
  Video:       <output-root>/deliverables/video.mp4
  Audio:       <output-root>/deliverables/audio.mp3
  Quiz:        <output-root>/deliverables/quiz.md
  Mind map:    <output-root>/deliverables/mind-map.json
  Flashcards:  <output-root>/deliverables/flashcards.md
  Infographic: <output-root>/deliverables/infographic.png
  Report:      <output-root>/deliverables/report.md
```

If any stage fell short (e.g. video generation timed out but slide deck succeeded), state that explicitly. Don't silently omit failures.

---

## If the user stops you mid-pipeline

Every stage writes to disk before advancing, and every stage checks for its outputs before running. Re-invoking the skill with the same subject + output root resumes from the first incomplete stage. Tell the user this if they seem nervous about a long-running Stage 5.
