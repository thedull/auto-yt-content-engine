#!/usr/bin/env python3
"""Search YouTube for a subject and return the top-N videos ranked by engagement.

Uses yt-dlp's `ytsearch<N>:<query>` with `--dump-json` (NDJSON, one video per
line). We intentionally avoid `--flat-playlist` — it strips view_count and
like_count, which we need for ranking.

Scoring: score = view_count + 10 * like_count. Likes are rarer than views, so
weighting them higher surfaces videos with strong positive signal over viral
but mediocre ones. Easy to tweak here if the mix feels off.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Prefer the yt-dlp binary sitting next to the running Python (venv's bin/).
_PY_BIN_DIR = Path(sys.executable).parent
os.environ["PATH"] = f"{_PY_BIN_DIR}{os.pathsep}{os.environ.get('PATH', '')}"


def search(query: str, pool: int) -> list[dict]:
    """Run yt-dlp search and parse NDJSON results."""
    cmd = [
        "yt-dlp",
        f"ytsearch{pool}:{query}",
        "--dump-json",
        "--skip-download",
        "--no-warnings",
        "--ignore-errors",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0 and not proc.stdout.strip():
        sys.stderr.write(proc.stderr)
        sys.exit(f"error: yt-dlp search failed (exit {proc.returncode})")

    results: list[dict] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            results.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return results


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
    ap.add_argument("subject", help="Search query")
    ap.add_argument("--top", type=int, default=10, help="Number of videos to return")
    ap.add_argument("--search-pool", type=int, default=30,
                    help="How many results to ask yt-dlp for before ranking "
                         "(default 30; overfetch lets us drop junk)")
    ap.add_argument("--out", required=True, help="Output JSON path")
    args = ap.parse_args()

    if args.search_pool < args.top:
        args.search_pool = args.top

    print(f"Searching YouTube for `{args.subject}` (pool={args.search_pool})...",
          file=sys.stderr)
    videos = search(args.subject, args.search_pool)
    if not videos:
        sys.exit("error: yt-dlp returned zero results (YouTube may have broken "
                 "yt-dlp — try `uv pip install --python <venv>/bin/python -U yt-dlp`)")

    ranked = sorted(videos, key=score, reverse=True)[:args.top]
    out = [project(v) for v in ranked]

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")

    # Short human-readable summary to stderr so the invoking agent sees progress.
    for i, v in enumerate(out, 1):
        views = f"{v['view_count']:,}" if v['view_count'] else "?"
        likes = f"{v['like_count']:,}" if v['like_count'] else "?"
        print(f"  {i:>2}. [{views} views, {likes} likes] {v['title']}",
              file=sys.stderr)

    print(f"Wrote {len(out)} ranked videos to {out_path}", file=sys.stderr)
    print(str(out_path))


if __name__ == "__main__":
    main()
