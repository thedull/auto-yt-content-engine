#!/usr/bin/env python3
"""Bulk-add local markdown files as sources to an existing NotebookLM notebook.

Two phases:
  1. Add every `.md` in `--dir` via `notebooklm source add <file> -n <id> --json`.
     Parses the returned JSON to collect source IDs.
  2. Serially wait for each source to finish processing via
     `notebooklm source wait <source_id> -n <id>`. Serial is intentional —
     parallel waits don't speed up Google's side and can trigger rate limits.

A final JSON summary is printed to stdout so the orchestrating agent can see
added vs. failed sources at a glance.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


# Allow the caller to override the notebooklm CLI location (useful when a
# project-local venv is preferred over the system PATH).
NB = os.environ.get("NOTEBOOKLM_BIN", "notebooklm")


def run(cmd: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(cmd, text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def add_source(md_path: Path, notebook_id: str) -> dict | None:
    """Return parsed JSON from `notebooklm source add` or None on failure."""
    rc, out, err = run([
        NB, "source", "add", str(md_path),
        "-n", notebook_id, "--json",
    ])
    if rc != 0:
        print(f"  [FAIL] {md_path.name}: {err.strip() or out.strip()}",
              file=sys.stderr)
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        print(f"  [FAIL] {md_path.name}: could not parse CLI JSON output",
              file=sys.stderr)
        return None


def wait_source(source_id: str, notebook_id: str, timeout: int) -> bool:
    """Return True on successful processing, False on timeout/error."""
    rc, _, err = run([
        NB, "source", "wait", source_id,
        "-n", notebook_id, "--timeout", str(timeout),
    ])
    if rc == 0:
        return True
    # notebooklm uses exit code 2 for timeout specifically.
    kind = "timeout" if rc == 2 else f"error (exit {rc})"
    print(f"  [{kind}] source {source_id}: {err.strip()}", file=sys.stderr)
    return False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--notebook", required=True, help="NotebookLM notebook ID")
    ap.add_argument("--dir", required=True, help="Directory of .md files to upload")
    ap.add_argument("--wait-timeout", type=int, default=600,
                    help="Per-source wait timeout in seconds (default 600)")
    args = ap.parse_args()

    md_dir = Path(args.dir)
    if not md_dir.is_dir():
        sys.exit(f"error: {md_dir} is not a directory")

    md_files = sorted(md_dir.glob("*.md"))
    if not md_files:
        sys.exit(f"error: no .md files in {md_dir}")

    print(f"Adding {len(md_files)} markdown file(s) to notebook "
          f"{args.notebook}...", file=sys.stderr)

    added: list[dict] = []
    failed: list[dict] = []

    for md in md_files:
        print(f"  + {md.name}", file=sys.stderr)
        result = add_source(md, args.notebook)
        if result is None:
            failed.append({"file": str(md), "stage": "add"})
            continue
        source_id = result.get("source_id") or result.get("id")
        if not source_id:
            failed.append({"file": str(md), "stage": "add",
                           "reason": "no source_id in CLI output"})
            continue
        added.append({"file": str(md), "source_id": source_id,
                      "title": result.get("title")})

    print(f"Waiting for {len(added)} source(s) to finish processing...",
          file=sys.stderr)

    for entry in added:
        if not wait_source(entry["source_id"], args.notebook, args.wait_timeout):
            failed.append({"file": entry["file"],
                           "source_id": entry["source_id"],
                           "stage": "wait"})

    summary = {"notebook": args.notebook, "added": added, "failed": failed}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
