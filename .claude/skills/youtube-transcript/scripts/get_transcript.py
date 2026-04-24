#!/usr/bin/env python3
"""Download a transcript for a YouTube video.

Strategy:
  1. Try to grab existing subtitles (manual or auto-generated) via yt-dlp
     in the video's original language. This is fast and lossless.
  2. If no subtitles are available, download the audio and transcribe it
     locally with faster-whisper using the `tiny` model (fastest).

Output: plain .txt file. Language follows the video's original language.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Prefer the binary sitting next to the currently running Python (i.e. the
# venv's bin/) so we pick up yt-dlp installed via `uv pip install` into the
# skill's .venv even if that venv isn't activated on the caller's PATH.
_PY_BIN_DIR = Path(sys.executable).parent
os.environ["PATH"] = f"{_PY_BIN_DIR}{os.pathsep}{os.environ.get('PATH', '')}"


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


def ensure_tool(name: str, install_hint: str) -> None:
    if shutil.which(name) is None:
        sys.exit(f"error: `{name}` not found on PATH. Install with: {install_hint}")


def get_metadata(url: str) -> dict:
    """Fetch video metadata (title, language, available subs) via yt-dlp."""
    proc = run(["yt-dlp", "-J", "--skip-download", url])
    return json.loads(proc.stdout)


def pick_subtitle_lang(meta: dict) -> str | None:
    """Pick the best subtitle language code matching the video's language.

    Prefers manual subs in the original language, then auto-captions in the
    original language, then any manual sub, then any auto-caption.
    """
    orig = (meta.get("language") or "").split("-")[0].lower() or None
    subs = meta.get("subtitles") or {}
    autos = meta.get("automatic_captions") or {}

    def match(pool: dict) -> str | None:
        if not pool:
            return None
        if orig:
            for code in pool:
                if code.split("-")[0].lower() == orig:
                    return code
        return None

    # Prefer manual in original language, then auto in original language.
    return match(subs) or match(autos) or (next(iter(subs), None) if subs else None) or (next(iter(autos), None) if autos else None)


def download_subtitles(url: str, lang: str, workdir: Path) -> Path | None:
    """Download subtitles in the given language as VTT. Returns path or None."""
    # --write-subs covers manual; --write-auto-subs covers auto-generated.
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", lang,
        "--sub-format", "vtt",
        "-o", str(workdir / "%(id)s.%(ext)s"),
        url,
    ]
    subprocess.run(cmd, check=True, text=True, capture_output=True)
    vtts = list(workdir.glob("*.vtt"))
    return vtts[0] if vtts else None


def vtt_to_text(vtt_path: Path) -> str:
    """Strip WEBVTT headers, timestamps, and tags; dedupe consecutive lines.

    YouTube auto-caption VTTs repeat each line across overlapping cues (rolling
    window). Deduping consecutive identical lines produces clean prose.
    """
    raw = vtt_path.read_text(encoding="utf-8", errors="replace")
    lines: list[str] = []
    for block in raw.split("\n\n"):
        for line in block.splitlines():
            if not line.strip():
                continue
            if line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
                continue
            if "-->" in line:
                continue
            if re.fullmatch(r"\d+", line.strip()):  # cue index
                continue
            # Strip inline tags like <00:00:01.234><c> word </c>
            clean = re.sub(r"<[^>]+>", "", line).strip()
            if not clean:
                continue
            if lines and lines[-1] == clean:
                continue
            lines.append(clean)
    return "\n".join(lines)


def download_audio(url: str, workdir: Path) -> Path:
    """Download bestaudio and convert to 16kHz mono wav (whisper-friendly)."""
    out = workdir / "audio.%(ext)s"
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "wav",
        "--postprocessor-args", "-ar 16000 -ac 1",
        "-o", str(out),
        url,
    ]
    subprocess.run(cmd, check=True, text=True, capture_output=True)
    wavs = list(workdir.glob("audio.*"))
    if not wavs:
        sys.exit("error: audio download failed")
    return wavs[0]


def transcribe(audio_path: Path, language: str | None) -> str:
    """Transcribe audio with faster-whisper using the tiny model (fastest)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit(
            "error: faster-whisper not installed. Install with:\n"
            "  pip install faster-whisper"
        )

    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(audio_path),
        language=language,  # None = auto-detect
        vad_filter=True,
    )
    return "\n".join(seg.text.strip() for seg in segments if seg.text.strip())


def format_duration(seconds: int | float | None) -> str:
    if not seconds:
        return ""
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def build_header(meta: dict, url: str, source: str) -> str:
    """YAML-fenced metadata block prepended to the transcript.

    Format is frontmatter-style so downstream tools (e.g. transcript-to-markdown)
    can parse a stable set of fields. `source` records whether the body came
    from captions or local whisper transcription.
    """
    fields = {
        "URL": url,
        "Title": meta.get("title", "") or "",
        "Channel": meta.get("uploader", "") or meta.get("channel", "") or "",
        "ChannelURL": meta.get("uploader_url", "") or meta.get("channel_url", "") or "",
        "Uploaded": meta.get("upload_date", "") or "",  # YYYYMMDD
        "Duration": format_duration(meta.get("duration")),
        "Language": (meta.get("language") or "") or "",
        "VideoID": meta.get("id", "") or "",
        "Source": source,
    }
    if fields["Uploaded"] and len(fields["Uploaded"]) == 8:
        d = fields["Uploaded"]
        fields["Uploaded"] = f"{d[:4]}-{d[4:6]}-{d[6:]}"
    lines = ["---"]
    for k, v in fields.items():
        if v:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Download or generate a YouTube transcript.")
    ap.add_argument("url", help="YouTube video URL")
    ap.add_argument("-o", "--output", help="Output .txt path (default: <title>.txt in cwd)")
    ap.add_argument("--force-transcribe", action="store_true",
                    help="Skip subtitle fetch and always transcribe audio")
    args = ap.parse_args()

    ensure_tool("yt-dlp", "pip install yt-dlp")
    ensure_tool("ffmpeg", "brew install ffmpeg (macOS) or apt install ffmpeg (Linux)")

    print("Fetching video metadata...", file=sys.stderr)
    meta = get_metadata(args.url)
    title = meta.get("title", "transcript")
    safe_title = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_") or "transcript"
    out_path = Path(args.output) if args.output else Path.cwd() / f"{safe_title}.txt"
    orig_lang = (meta.get("language") or "").split("-")[0].lower() or None

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        text: str | None = None
        source = ""

        if not args.force_transcribe:
            lang = pick_subtitle_lang(meta)
            if lang:
                print(f"Subtitles available in `{lang}` — downloading...", file=sys.stderr)
                vtt = download_subtitles(args.url, lang, workdir)
                if vtt:
                    text = vtt_to_text(vtt)
                    source = f"youtube-captions ({lang})"

        if not text:
            print("No usable subtitles. Downloading audio and transcribing locally "
                  "(faster-whisper, tiny model)...", file=sys.stderr)
            audio = download_audio(args.url, workdir)
            text = transcribe(audio, orig_lang)
            source = "faster-whisper-tiny"

        header = build_header(meta, args.url, source)
        out_path.write_text(f"{header}\n\n{text}\n", encoding="utf-8")
        print(f"Wrote transcript: {out_path}", file=sys.stderr)
        print(str(out_path))


if __name__ == "__main__":
    main()
