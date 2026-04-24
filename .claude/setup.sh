#!/usr/bin/env bash
# Bootstrap the project-local Python venvs used by the skills.
#
# Requires:
#   - uv          (https://docs.astral.sh/uv/) — for venv + pip install
#   - ffmpeg      (brew install ffmpeg / apt install ffmpeg) — for whisper audio decode
#
# Safe to re-run: existing venvs are upgraded in place.

set -euo pipefail

# Resolve project root (directory containing this script's .. )
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILLS_DIR="${SCRIPT_DIR}/skills"

echo "→ Project root: ${PROJECT_DIR}"

# ── Prereq checks ────────────────────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
  echo "✗ 'uv' is required. Install: https://docs.astral.sh/uv/"
  exit 1
fi
if ! command -v ffmpeg &>/dev/null; then
  echo "⚠ ffmpeg not on PATH. The whisper fallback in youtube-transcript will"
  echo "  fail until you install it (brew install ffmpeg / apt install ffmpeg)."
fi

setup_skill_venv() {
  local skill="$1"
  local req_file="${SKILLS_DIR}/${skill}/requirements.txt"
  local venv_dir="${SKILLS_DIR}/${skill}/.venv"

  if [[ ! -f "${req_file}" ]]; then
    echo "  (skip ${skill}: no requirements.txt)"
    return 0
  fi

  echo "→ ${skill}"
  uv venv "${venv_dir}" --python 3.11 --quiet
  VIRTUAL_ENV="${venv_dir}" uv pip install --quiet -r "${req_file}"
  echo "  ✓ ${venv_dir}"
}

# ── Set up each skill that declares requirements ─────────────────────────────
for skill in youtube-transcript notebooklm; do
  setup_skill_venv "${skill}"
done

echo
echo "✓ Setup complete."
echo
echo "The pipeline skill expects CLAUDE_PROJECT_DIR to be set by the Claude Code"
echo "harness. If running skills manually from a shell, export it:"
echo
echo "  export CLAUDE_PROJECT_DIR=\"${PROJECT_DIR}\""
