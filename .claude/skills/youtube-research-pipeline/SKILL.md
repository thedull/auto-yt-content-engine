---
name: youtube-research-pipeline
description: End-to-end research pipeline that, given a subject, finds the most popular YouTube videos on it, extracts transcripts, converts them to structured Markdown, uploads everything to a fresh NotebookLM notebook, synthesizes a master summary, and generates a presentation (slide deck) and a video. Use this skill whenever the user wants to "learn everything about X from YouTube," research a topic in depth from video sources, build a knowledge base from YouTube, create a presentation or video overview from YouTube content, or batch-process YouTube videos into a notebook — even when they don't say the word "pipeline." If the user mentions combining YouTube + NotebookLM, trigger this.
---

# YouTube Research Pipeline

Given a subject, produce a self-contained research folder:

```
<output-root>/
├── videos.json              # ranked video list from yt-dlp
├── transcripts/<id>.txt     # one per video (with YAML metadata header)
├── markdown/<id>.md         # structured markdown per video
├── master-summary.md        # Claude-synthesized cross-cutting summary
├── deliverables/
│   ├── slides.pdf           # from NotebookLM
│   └── video.mp4            # from NotebookLM
└── errors.log               # anything that was skipped and why
```

This skill chains three existing skills (`youtube-transcript`, `transcript-to-markdown`, `notebooklm`) plus two bundled scripts. Your job as the invoking agent is orchestration + synthesis. The scripts do the mechanical parts.

## Ask the user up-front

Before starting, confirm three things (or proceed with defaults if the user gave them in the prompt):

1. **Subject** — the search query.
2. **Top N** — default **10** videos. Cap at 50 (NotebookLM's per-notebook source limit).
3. **Output root** — *optional user-defined directory* (e.g. an Obsidian vault path). If the user doesn't specify one, default to `./research/<subject-slug>/` under the current working directory.

Slugify the subject for the default path: lowercase → replace non-alphanumerics with `-` → collapse repeated dashes → trim leading/trailing dashes → cap at 60 chars.

If the user provided an output root, use it **as-is** (no `<subject-slug>` subfolder appended — they chose the path deliberately, likely inside a vault structure they've already organized).

## Pipeline overview

```
[Stage 1] yt-dlp search → ranked video list
[Stage 2] per-video: transcript .txt → structured .md   (parallel, batch of 5)
[Stage 3] create NotebookLM notebook → upload all .md
[Stage 4] Claude reads all .md → master-summary.md
[Stage 5] NotebookLM: generate slide-deck + video       (parallel)
[Stage 6] download slides.pdf + video.mp4
```

Every stage is **idempotent** — rerunning the skill on the same subject/output skips already-completed work. If a stage was interrupted, the skill can resume.

---

## Stage 1 — Search and rank

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

Then retry Stage 1.

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

## Stage 3 — Create notebook and upload markdowns

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

> **Scope:** N YouTube videos on "<subject>", ranked by views + likes.
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

**Skip this stage if `master-summary.md` already exists.**

---

## Stage 5 — Generate slide deck + video (parallel)

Fire both generation commands **in parallel** (two `Bash` tool calls in one message):

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm generate slide-deck -n <id> --json
${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm generate video -n <id> --json
```

Each returns a `task_id` in the JSON. Save them (e.g. to `<output-root>/.tasks.json`).

Then poll for completion in parallel.

**Do not use `notebooklm artifact wait` or `notebooklm artifact poll`.** They sit on a task-status endpoint that gets stuck reporting `in_progress` even after the artifact has actually completed — the wait will hang until its timeout and never resolve, especially for `video` tasks. Confirmed bug as of 2026-04.

Instead, poll via `notebooklm artifact get <task_id>` in a shell loop. The `task_id` returned by `generate` is the same UUID as the eventual artifact ID, so `get` works on it directly. The artifact's `Status:` field is authoritative — it will be `pending` → `in_progress` → `completed` (or `failed`).

Run both polls in parallel as background `Bash` calls:

```bash
# slide-deck poll: check every 30s, give up after 30 min
until ${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm artifact get <slide_task_id> -n <id> 2>/dev/null | grep -q "Status: completed"; do
  sleep 30
  # safety: bail if it's been >30 min (60 iterations)
done && echo "slides ready"
```

```bash
# video poll: check every 60s, give up after 60 min
until ${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm artifact get <video_task_id> -n <id> 2>/dev/null | grep -q "Status: completed"; do
  sleep 60
done && echo "video ready"
```

Use `Bash` with `run_in_background: true` for both, then rely on the runtime's task-completion notification — do not sleep/poll yourself.

Also handle the **failed** case: if `Status: failed` appears, exit the loop and report partial success.

A more defensive single-line form that handles both completed and failed:

```bash
while :; do
  s=$(${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm artifact get <task_id> -n <id> 2>/dev/null | awk '/^Status:/ {print $2}')
  case "$s" in completed) echo ok; exit 0 ;; failed) echo failed; exit 1 ;; esac
  sleep 30
done
```

- Slide deck usually completes in 5–15 min.
- Video usually completes in 15–45 min. Set the loop's safety cap accordingly.

### Rate limits

If either `generate` command fails with a rate-limit / HTTP 429 / "quota" error, wait 5 minutes and retry once. If it fails again, stop and report the partial success — the user can manually re-run `notebooklm generate ...` later without re-doing Stages 1-4.

---

## Stage 6 — Download

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm download slide-deck <output-root>/deliverables/slides.pdf -n <id> -a <slide_task_id>
${CLAUDE_PROJECT_DIR}/.claude/skills/notebooklm/.venv/bin/notebooklm download video <output-root>/deliverables/video.mp4 -n <id> -a <video_task_id>
```

Make sure `<output-root>/deliverables/` exists first.

---

## Final report

Print a clean summary to the user:

```
✓ Pipeline complete.

Output root:   <output-root>
Videos:        <n_ok>/<n_requested> processed successfully (<n_failed> skipped — see errors.log)
Notebook:      https://notebooklm.google.com/notebook/<notebook_id>
Summary:       <output-root>/master-summary.md
Slide deck:    <output-root>/deliverables/slides.pdf
Video:         <output-root>/deliverables/video.mp4
```

If any stage fell short (e.g. video generation timed out but slide deck succeeded), state that explicitly. Don't silently omit failures.

---

## If the user stops you mid-pipeline

Every stage writes to disk before advancing, and every stage checks for its outputs before running. Re-invoking the skill with the same subject + output root resumes from the first incomplete stage. Tell the user this if they seem nervous about a long-running Stage 5.
