---
name: youtube-transcript
description: Download a plain-text transcript for any YouTube video, even when the video has no captions. Uses yt-dlp to fetch existing subtitles when available, otherwise downloads the audio and transcribes it locally with faster-whisper. Use this skill whenever the user wants to get the transcript, subtitles, captions, or written text of a YouTube video, convert a YouTube video to text, extract what's said in a video, or pull quotes/content from a YouTube link — even if they don't use the word "transcript" and even if the video has no captions.
---

# YouTube Transcript

Given a YouTube URL, produce a clean `.txt` transcript in the video's original language.

## How it works

The bundled script `scripts/get_transcript.py` handles the whole flow:

1. **Subtitles first (fast path).** It asks yt-dlp for the video's metadata, picks the best available subtitle track in the video's original language (manual > auto-generated), downloads the VTT, and converts it to clean prose. VTT-to-text deduplicates the rolling-window repetitions that YouTube auto-captions produce, so the output reads naturally.
2. **Audio transcription fallback.** If the video has no subtitles in any language, the script downloads `bestaudio` with yt-dlp, converts it to 16 kHz mono WAV via ffmpeg, and transcribes it locally with `faster-whisper` using the `tiny` model (the fastest variant, runs on CPU with int8 quantization). Language is set to the video's original language when yt-dlp reports one; otherwise whisper auto-detects.

Output is written as a `.txt` file. The path is printed on stdout so you can capture it; status messages go to stderr.

## Usage

The skill ships with a dedicated virtualenv at `.venv/` that has `yt-dlp` and `faster-whisper` preinstalled. **Always invoke the script with that venv's Python** so dependencies resolve:

```bash
${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv/bin/python \
  ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/scripts/get_transcript.py <youtube-url>

# optional flags:
#   -o /path/to/out.txt         custom output path
#   --force-transcribe          skip subs, always transcribe audio
```

By default the transcript is saved to `<video_title>.txt` in the current working directory, and the path is printed on stdout.

### Output format

Each transcript file starts with a YAML-fenced metadata header, then a blank line, then the transcript body:

```
---
URL: https://www.youtube.com/watch?v=abc123
Title: Example Video
Channel: Example Channel
ChannelURL: https://www.youtube.com/@example
Uploaded: 2024-10-15
Duration: 12:34
Language: en
VideoID: abc123
Source: youtube-captions (en-orig)   # or: faster-whisper-tiny
---

If Claude Code plus NotebookLM is amazing...
```

Downstream skills (e.g. `transcript-to-markdown`) can parse this header to preserve attribution. `Source` records the path taken (captions vs. local Whisper) — useful when deciding how much to trust punctuation/spelling.

## Dependencies

Checked at runtime. If any are missing, install and retry — don't abandon the task:

- **`yt-dlp`** — installed in the skill's `.venv`. Upgrade periodically (YouTube breaks yt-dlp often): `uv pip install --python <venv>/bin/python -U yt-dlp`.
- **`ffmpeg`** — system binary on PATH. `brew install ffmpeg` on macOS, `apt install ffmpeg` on Debian/Ubuntu.
- **`faster-whisper`** — installed in the skill's `.venv`. Only imported when the audio fallback runs.

If the `.venv` is missing (e.g., fresh clone), run the project's setup script:

```bash
${CLAUDE_PROJECT_DIR}/.claude/setup.sh
```

Or recreate this skill's venv directly:

```bash
uv venv ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv --python 3.11
VIRTUAL_ENV=${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/.venv \
  uv pip install -r ${CLAUDE_PROJECT_DIR}/.claude/skills/youtube-transcript/requirements.txt
```

## Notes on quality and edge cases

- **Auto-captions are noisy.** YouTube's auto-generated captions lack punctuation and occasionally misrecognize words. The output reflects that. For important transcripts, `--force-transcribe` with whisper may actually produce a cleaner result despite being slower, because whisper adds punctuation.
- **`tiny` model tradeoff.** The user asked for "faster," so this skill uses `tiny`. It's good enough for most speech but struggles with heavy accents, low-quality audio, or technical jargon. If the user reports quality issues, suggest editing the script to use `base` or `small` — the only change is the model name passed to `WhisperModel(...)`.
- **Private / age-gated / region-locked videos** will fail at the yt-dlp step. Surface the yt-dlp error to the user rather than retrying blindly.
- **Long videos** with no captions mean a long whisper run. A 1-hour video on CPU with the `tiny` model typically takes several minutes. Warn the user before starting if the video is long and captions aren't available.
