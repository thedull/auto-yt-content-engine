#!/usr/bin/env python3
"""Fetch metadata for a list of YouTube URLs and output videos.json.

Supports two input methods:
1. Command-line URLs: python fetch_metadata.py <url1> <url2> ... --out videos.json
2. JSON file: python fetch_metadata.py --file urls.json --out videos.json

JSON file format:
{
  "subject": "My Research Topic",  // optional
  "urls": ["https://youtube.com/watch?v=abc123", ...]
}
or simply:
["https://youtube.com/watch?v=abc123", ...]

The subject is optional and can be overridden via --subject flag.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Prefer the yt-dlp binary sitting next to the running Python (venv's bin/).
_PY_BIN_DIR = Path(sys.executable).parent
os.environ["PATH"] = f"{_PY_BIN_DIR}{os.pathsep}{os.environ.get('PATH', '')}"


def fetch_metadata(url: str) -> dict | None:
    """Fetch metadata for a single YouTube URL using yt-dlp."""
    cmd = [
        "yt-dlp",
        url,
        "--dump-json",
        "--skip-download",
        "--no-warnings",
        "--ignore-errors",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(f"Error fetching {url}: {proc.stderr}\n")
        return None

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        sys.stderr.write(f"Error parsing JSON for {url}\n")
        return None


def score(v: dict) -> int:
    """Engagement score; likes weighted 10x because they're rarer."""
    return (v.get("view_count") or 0) + 10 * (v.get("like_count") or 0)


def project(v: dict) -> dict:
    """Pick only the fields downstream stages need."""
    return {
        "id": v.get("id"),
        "url": v.get("webpage_url") or f"https://www.youtube.com/watch?v={v.get('id')}",
        "title": v.get("title"),
        "channel": v.get("channel") or v.get("uploader"),
        "uploader": v.get("uploader"),
        "duration": v.get("duration"),
        "view_count": v.get("view_count"),
        "like_count": v.get("like_count"),
        "upload_date": v.get("upload_date"),  # YYYYMMDD
        "score": score(v),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", help="JSON file containing URLs (and optional subject)")
    ap.add_argument("--subject", help="Research subject (overrides subject in JSON file)")
    ap.add_argument("--out", required=True, help="Output JSON path")
    ap.add_argument("urls", nargs="*", help="YouTube URLs (if not using --file)")
    args = ap.parse_args()

    # Determine URLs and subject
    urls: list[str] = []
    subject: str | None = None

    if args.file:
        # Read from JSON file
        file_path = Path(args.file)
        if not file_path.exists():
            sys.exit(f"error: file not found: {args.file}")

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            sys.exit(f"error: invalid JSON in {args.file}: {e}")

        # Handle both array and object formats
        if isinstance(data, list):
            urls = data
        elif isinstance(data, dict):
            urls = data.get("urls", [])
            subject = data.get("subject")
        else:
            sys.exit(f"error: JSON must be an array or object, got {type(data).__name__}")

        if not urls:
            sys.exit(f"error: no URLs found in {args.file}")
    else:
        # Use command-line URLs
        if not args.urls:
            sys.exit("error: must provide URLs either via --file or as positional arguments")
        urls = args.urls

    # Override subject from command-line if provided
    if args.subject:
        subject = args.subject

    # Fetch metadata for each URL
    print(f"Fetching metadata for {len(urls)} video(s)...", file=sys.stderr)
    videos: list[dict] = []
    failed: list[str] = []

    for url in urls:
        print(f"  {url}", file=sys.stderr)
        metadata = fetch_metadata(url)
        if metadata is None:
            failed.append(url)
            continue
        videos.append(project(metadata))

    if not videos:
        sys.exit("error: failed to fetch metadata for all URLs")

    # Write output
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(videos, indent=2) + "\n", encoding="utf-8")

    # Print summary to stderr
    print(f"Wrote {len(videos)} video(s) to {out_path}", file=sys.stderr)
    if failed:
        print(f"Failed to fetch {len(failed)} video(s):", file=sys.stderr)
        for url in failed:
            print(f"  - {url}", file=sys.stderr)

    # Print subject to stdout if provided (for the skill to use)
    if subject:
        print(f"SUBJECT:{subject}")

    # Print output path to stdout
    print(str(out_path))


if __name__ == "__main__":
    main()
