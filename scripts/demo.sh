#!/usr/bin/env bash
# WorldSim stakeholder demo launcher.
#
# Requirements: Docker (with Compose v2 plugin). Nothing else.
# Hardware target: 2-core, 8 GB RAM (Equitable Build Process standard).
#
# Usage:
#   ./scripts/demo.sh            — start stack, seed data, print presenter guide
#   ./scripts/demo.sh --run      — same, then launch the Playwright walkthrough
#   ./scripts/demo.sh --reset    — tear down and remove volumes (clean slate)
#
# The --run flag requires Node.js and npx to be available on the host for
# Playwright. The stack itself needs only Docker.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_HEALTH_URL="http://localhost:8000/health"
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

for arg in "$@"; do
  case "$arg" in
    --run)   RUN_PLAYWRIGHT=true ;;
    --reset) RESET=true ;;
    *)
      echo "Unknown flag: $arg"
      echo "Usage: $0 [--run] [--reset]"
      exit 1
      ;;
  esac
done

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
  echo "$(yellow 'Warning: seed command returned non-zero. GRC entity may already exist — proceeding.')"
fi

# ── Presenter guide ───────────────────────────────────────────────────────────

echo ""
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo "$(bold '  PRESENTER GUIDE — WorldSim Stakeholder Demonstration')"
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo ""
echo "$(bold 'Stack status:')"
echo "  API:       $(green 'http://localhost:8000')  $(dim '(FastAPI + PostGIS)')"
echo "  Frontend:  $(green 'http://localhost:5173')  $(dim '(React + MapLibre GL)')"
echo ""
echo "$(bold 'Open the application in a browser now:')"
echo "  $(green "$FRONTEND_URL")"
echo ""
echo "$(bold '─── TIMING GUIDE (20 minutes total) ────────────────────────────')"
echo ""
echo "  $(yellow '[ 0:00 – 3:00 ]')  $(bold 'PROBLEM FRAMING')"
echo "  The IMF walks in with institutional infrastructure."
echo "  The finance ministry walks in with economic judgment."
echo "  This tool closes that gap — open source, runs on a laptop."
echo "  Do NOT use warning language. The human cost ledger is"
echo "  analytical capability, not an alarm system."
echo ""
echo "  $(yellow '[ 3:00 – 8:00 ]')  $(bold 'LIVE APPLICATION (5 minutes)')"
echo ""
echo "  Step 1  Map loads — orient the audience. Do not linger."
echo "          '$(dim "This is the baseline view. Each country shows a simulation")"
echo "          $(dim "attribute. Click any country to open its analysis panel.")"
echo "          $(dim "What makes this different will become clear in a moment.")''"
echo ""
echo "  Step 2  Scenarios panel → enter '$(bold 'Greece 2010-2012 Demo')'"
echo "          → Create → Select as primary"
echo "          '$(dim "We are modeling the 2010-2012 IMF programme. Conditionality")"
echo "          $(dim "terms are the inputs. The simulation produces the consequences.")''"
echo ""
echo "  Step 3  Next Step × 3 (watch step counter: 1/3 → 2/3 → 3/3)"
echo "          '$(dim "Each step is one year. Watch Greece shift in the choropleth")"
echo "          $(dim "as the fiscal contraction accumulates across steps.")''"
echo ""
echo "  Step 4  Click Greece on the map → drawer opens"
echo "          '$(dim "This panel is the primary analytical surface.")''"
echo "          $(bold 'PAUSE — let them read the MDA alert panel first.')"
echo ""
echo "  Step 5  Point to $(bold 'MDA Threshold Breaches') heading"
echo "          '$(dim "These are Minimum Descent Altitude alerts — levels below")"
echo "          $(dim "which consequences become irreversible. This is not a warning")"
echo "          $(dim "about the model. It is a finding about where this path goes.")''"
echo "          Read the alert as evidence: indicator / step / severity / cohort."
echo ""
echo "  Step 6  Scroll to $(bold 'Multi-Framework Overview') radar chart"
echo "          '$(dim "Four axes: financial, human development, ecological, governance.")"
echo "          $(dim "The radar shows which dimensions are under stress.")''"
echo "          Be honest: ecological null at this milestone (M8)."
echo ""
echo "  Step 7  Scenarios panel → create second scenario → '+ Compare'"
echo "          → tick '$(bold 'Compare scenarios')' checkbox in header"
echo "          '$(dim "The DeltaChoropleth shows where the two paths diverge.")"
echo "          $(dim "The argument: this path crosses the threshold; this alternative")"
echo "          $(dim "achieves the same fiscal objective without crossing it.")''"
echo ""
echo "  $(yellow '[ 8:00 – 13:00 ]')  $(bold 'BACKTESTING CREDIBILITY')"
echo "  Lead with the IMF multiplier error (Blanchard-Leigh 2013):"
echo "  assumed 0.5, empirical 1.5. Three times what programmes used."
echo "  Five cases: Greece, Argentina, Lebanon, Thailand, Ecuador."
echo "  DIRECTION_ONLY = 'did GDP go up or down?' Pass on all five."
echo "  '$(dim "A model that gets the sign right across five distinct crisis")"
echo "   $(dim "mechanisms is capturing real causal dynamics.")''"
echo ""
echo "  $(yellow '[ 13:00 – 18:00 ]')  $(bold 'ROADMAP')"
echo "  M7: Uncertainty visualization — bands proportional to horizon."
echo "  M8: Ecological + Governance composite scores; causal meta-map."
echo "  M9: Methodology publication + Technical Steering Committee."
echo "  Frame as expanding capability, not missing features."
echo ""
echo "  $(yellow '[ 18:00 – 19:00 ]')  $(bold 'NORTH STAR CLOSING — 1 minute exactly')"
echo "  '$(dim "There is a quinoa farmer in Bolivia who will never know this")"
echo "   $(dim "tool exists. His government might. If his government has a finance")"
echo "   $(dim "minister with better analytical tools, that minister can negotiate")"
echo "   $(dim "better terms. The quinoa farmer lives at the end of that chain.")"
echo "   $(dim "Build it as if he does.")''"
echo ""
echo "  $(yellow '[ 19:00 – 30:00 ]')  $(bold 'Q&A')"
echo "  See docs/demo/stakeholder-walkthrough.md §Q&A Preparation"
echo "  for scripted responses to the four most likely questions."
echo ""
echo "$(bold '─── HONEST DISCLOSURES (available if asked) ────────────────────')"
echo ""
echo "  • Distributions are pre-calibration. Bands show reasonable range,"
echo "    not empirically calibrated confidence intervals. Disclosed in UI."
echo "  • Ecological + Governance composite scores null until M8."
echo "  • Fidelity thresholds are DIRECTION_ONLY (sign). Magnitude"
echo "    calibration (DISTRIBUTION_COMBINED) is the next validation layer."
echo "  • This tool is not for financial advantage or surveillance."
echo ""
echo "$(bold '─── AUTOMATED WALKTHROUGH ───────────────────────────────────────')"
echo ""

if $RUN_PLAYWRIGHT; then
  echo "$(bold 'Launching Playwright demo walkthrough...')"
  echo "$(dim 'Browser will open. Press Resume in the inspector at each pause.')"
  echo ""
  cd "$REPO_ROOT/frontend"
  npx playwright test tests/e2e/demo.spec.ts \
    --config playwright.demo.config.ts \
    --headed \
    --project=chromium
else
  echo "  To launch the automated Playwright walkthrough:"
  echo "  $(green '  ./scripts/demo.sh --run')"
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
