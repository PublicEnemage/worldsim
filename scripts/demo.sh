#!/usr/bin/env bash
# WorldSim stakeholder demo launcher.
#
# Requirements: Docker (with Compose v2 plugin). Nothing else.
# Hardware target: 2-core, 8 GB RAM (Equitable Build Process standard).
#
# Usage:
#   ./scripts/demo.sh                 — start stack, seed data, print presenter guide (current milestone)
#   ./scripts/demo.sh --milestone 16  — start stack with presenter guide for milestone 16
#   ./scripts/demo.sh --run           — same, then launch the Playwright walkthrough
#   ./scripts/demo.sh --reset         — tear down and remove volumes (clean slate)
#
# The --milestone flag selects the demo cycle. Guide content is derived from
# docs/demo/m{N}/stakeholder-walkthrough.md and docs/demo/m{N}/screenshot-brief.md.
# The --run flag requires Node.js and npx to be available on the host for
# Playwright. The stack itself needs only Docker.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_HEALTH_URL="http://localhost:8000/api/v1/health/"
FRONTEND_URL="http://localhost:5173"
MAX_WAIT_SECONDS=120

# ── Colour helpers ────────────────────────────────────────────────────────────

bold()   { printf '\033[1m%s\033[0m' "$*"; }
green()  { printf '\033[32m%s\033[0m' "$*"; }
yellow() { printf '\033[33m%s\033[0m' "$*"; }
red()    { printf '\033[31m%s\033[0m' "$*"; }
dim()    { printf '\033[2m%s\033[0m' "$*"; }

# ── Parse flags ───────────────────────────────────────────────────────────────

RUN_PLAYWRIGHT=false
RESET=false
MILESTONE="16"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run)           RUN_PLAYWRIGHT=true; shift ;;
    --reset)         RESET=true; shift ;;
    --milestone)     MILESTONE="$2"; shift 2 ;;
    --milestone=*)   MILESTONE="${1#--milestone=}"; shift ;;
    *)
      echo "Unknown flag: $1"
      echo "Usage: $0 [--run] [--reset] [--milestone N]"
      exit 1
      ;;
  esac
done

# ── Resolve milestone demo documents ─────────────────────────────────────────

WALKTHROUGH="$REPO_ROOT/docs/demo/m${MILESTONE}/stakeholder-walkthrough.md"
SCREENSHOT_BRIEF="$REPO_ROOT/docs/demo/m${MILESTONE}/screenshot-brief.md"

# ── Reset ─────────────────────────────────────────────────────────────────────

if $RESET; then
  echo ""
  echo "$(bold 'Resetting WorldSim stack...')"
  cd "$REPO_ROOT"
  docker compose down -v --remove-orphans
  echo "$(green 'Stack removed. Run ./scripts/demo.sh to rebuild.')"
  exit 0
fi

# ── Pre-flight: Docker available ──────────────────────────────────────────────

if ! docker info >/dev/null 2>&1; then
  echo "$(red 'ERROR: Docker is not running.')"
  echo "Start Docker Desktop and retry."
  exit 1
fi

# ── Start the stack ───────────────────────────────────────────────────────────

echo ""
echo "$(bold '╔══════════════════════════════════════════════════════════════╗')"
echo "$(bold '║               WorldSim Stakeholder Demo                     ║')"
echo "$(bold '╚══════════════════════════════════════════════════════════════╝')"
echo ""
echo "Starting Docker Compose stack..."
cd "$REPO_ROOT"
docker compose up -d --build 2>&1 | grep -E "^(#|✓|=>|Creating|Starting|Pulling|Building|ERROR)" || true
echo ""

# ── Wait for API health ───────────────────────────────────────────────────────

printf "Waiting for API health (%s)..." "$API_HEALTH_URL"
ELAPSED=0
until curl -sf "$API_HEALTH_URL" >/dev/null 2>&1; do
  sleep 2
  ELAPSED=$((ELAPSED + 2))
  if [ "$ELAPSED" -ge "$MAX_WAIT_SECONDS" ]; then
    echo ""
    echo "$(red "ERROR: API did not become healthy within ${MAX_WAIT_SECONDS}s.")"
    echo "Check: docker compose logs api"
    exit 1
  fi
  printf '.'
done
echo " $(green 'OK')"

# ── Wait for frontend ─────────────────────────────────────────────────────────

printf "Waiting for frontend (%s)..." "$FRONTEND_URL"
ELAPSED=0
until curl -sf "$FRONTEND_URL" >/dev/null 2>&1; do
  sleep 2
  ELAPSED=$((ELAPSED + 2))
  if [ "$ELAPSED" -ge "$MAX_WAIT_SECONDS" ]; then
    echo ""
    echo "$(red "ERROR: Frontend did not become available within ${MAX_WAIT_SECONDS}s.")"
    echo "Check: docker compose logs frontend"
    exit 1
  fi
  printf '.'
done
echo " $(green 'OK')"

# ── Run migrations ────────────────────────────────────────────────────────────

echo ""
echo "Running Alembic migrations..."
if docker compose exec -T api alembic upgrade head 2>&1 | tail -3; then
  echo "$(green 'Migrations complete.')"
else
  echo "$(yellow 'Warning: migration command returned non-zero. Proceeding — may already be at head.')"
fi

# ── Seed Natural Earth data ───────────────────────────────────────────────────

echo ""
echo "Seeding Natural Earth data..."
if docker compose exec -T api python -m app.db.seed.natural_earth_loader 2>&1 | tail -5; then
  echo "$(green 'Seed complete.')"
else
  echo "$(yellow 'Warning: seed command returned non-zero. ZMB entity may already exist — proceeding.')"
fi

# ── Presenter guide ───────────────────────────────────────────────────────────

echo ""
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo "$(bold "  PRESENTER GUIDE — WorldSim Stakeholder Demo (Milestone ${MILESTONE})")"
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo ""
echo "$(bold 'Stack status:')"
echo "  API:       $(green 'http://localhost:8000')  $(dim '(FastAPI + PostGIS)')"
echo "  Frontend:  $(green 'http://localhost:5173')  $(dim '(React + MapLibre GL)')"
echo ""
echo "$(bold 'Open the application in a browser now:')"
echo "  $(green "$FRONTEND_URL")"
echo ""
echo "$(bold "Demo documents for Milestone ${MILESTONE}:")"
echo "  Walkthrough:       $WALKTHROUGH"
echo "  Screenshot brief:  $SCREENSHOT_BRIEF"
echo ""

if [ -f "$WALKTHROUGH" ]; then
  echo "$(bold '─── WALKTHROUGH SUMMARY ─────────────────────────────────────────')"
  echo ""
  head -80 "$WALKTHROUGH"
  echo ""
  echo "  $(dim "Full guide: $WALKTHROUGH")"
else
  echo "$(yellow "  WARNING: $WALKTHROUGH not found.")"
  echo "  Demo documents for milestone ${MILESTONE} have not been authored yet."
  echo "  See docs/process/sprint-plans/m16-sprint-plan.md §G8."
fi

echo ""
echo "$(bold '─── NORTH STAR CLOSING (do not change) ─────────────────────────')"
echo ""
echo "  '$(dim "There is a quinoa farmer in Bolivia who will never know this")"
echo "   $(dim "tool exists. His government might. If his government has a finance")"
echo "   $(dim "minister with better analytical tools, that minister can negotiate")"
echo "   $(dim "better terms. The quinoa farmer lives at the end of that chain.")"
echo "   $(dim "Build it as if he does.")''"
echo ""
echo "$(bold '─── AUTOMATED WALKTHROUGH ───────────────────────────────────────')"
echo ""

if $RUN_PLAYWRIGHT; then
  echo "$(bold 'Launching Playwright demo walkthrough...')"
  echo "$(dim 'Browser will open. TTS narration plays per step.')"
  echo ""
  cd "$REPO_ROOT/frontend"
  npx playwright test tests/e2e/demo-narrated.spec.ts \
    --config playwright.demo.config.ts \
    --headed \
    --project=chromium
else
  echo "  To launch the automated Playwright walkthrough:"
  echo "  $(green "  ./scripts/demo.sh --milestone ${MILESTONE} --run")"
  echo ""
  echo "  Requirements for --run: Node.js + npx on host (Playwright uses"
  echo "  the local ./frontend/node_modules installation)."
  echo ""
  echo "  Without --run: open $(green "$FRONTEND_URL") and follow the guide above."
fi

echo ""
echo "$(bold '─── SHUTDOWN ────────────────────────────────────────────────────')"
echo ""
echo "  To stop the stack:  $(green 'docker compose down')"
echo "  Clean slate reset:  $(green './scripts/demo.sh --reset')"
echo ""
