#!/usr/bin/env bash
# speak.sh — macOS TTS wrapper for the WorldSim screen-recorded demo.
#
# Usage:
#   scripts/speak.sh "Text to speak"
#   scripts/speak.sh --list-voices
#
# On non-macOS systems, prints the text instead of speaking so the narrated
# Playwright spec can run (silently) on Linux CI runners without erroring.

set -euo pipefail

VOICE="Zoe (Enhanced)"
RATE=175

if [[ "${1:-}" == "--list-voices" ]]; then
  say --voice "?" 2>/dev/null | awk '{print $1}' || echo "say not available on this platform"
  exit 0
fi

TEXT="${1:-}"
if [[ -z "$TEXT" ]]; then
  echo "Usage: speak.sh \"Text to speak\"" >&2
  exit 1
fi

if command -v say &>/dev/null; then
  say -v "$VOICE" -r "$RATE" "$TEXT"
else
  # Non-macOS fallback: print so the recording operator can read along.
  echo "[NARRATION] $TEXT"
fi
