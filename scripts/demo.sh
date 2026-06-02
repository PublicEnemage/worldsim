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
echo "$(bold '  PRESENTER GUIDE — WorldSim Stakeholder Demonstration (M10)')"
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo ""
echo "$(bold 'Stack status:')"
echo "  API:       $(green 'http://localhost:8000')  $(dim '(FastAPI + PostGIS)')"
echo "  Frontend:  $(green 'http://localhost:5173')  $(dim '(React + MapLibre GL)')"
echo ""
echo "$(bold 'Open the application in a browser now:')"
echo "  $(green "$FRONTEND_URL")"
echo ""
echo "$(bold 'Demo 3 — Argentina 2001–2004 Crisis Arc')"
echo "  Four steps: Zero Deficit Plan (2001) → Sovereign default (2002)"
echo "  → Kirchner recovery (2003) → Growth consolidation (2004)"
echo "  All four Zone 1 axes live: trajectory view, MDA alerts, PMM, four-framework."
echo "  Governance: live composite (WGI + V-Dem). Ecological: live (CO2 boundary proximity)."
echo "  Platform Principle: same engine as Greece, different crisis arc."
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
echo "          '$(dim "This is the baseline view. Each country on the map shows")"
echo "          $(dim "a simulation attribute as geographic context.")"
echo "          $(dim "The analytical instrument is the panel on the left.")''"
echo "          $(bold 'Note:') Do NOT narrate 'watch Argentina shift in the choropleth.'"
echo "          The choropleth is geographic context. The trajectory view is the instrument."
echo ""
echo "  Step 2  Scenarios panel → select '$(bold 'Argentina 2001-2002 Demo 3')'"
echo "          → Select as primary. The Zone 1 instrument cluster loads."
echo "          '$(dim "We are modeling Argentina's 2001-2002 sovereign default — four")"
echo "          $(dim "steps, annual, from the Zero Deficit Plan through the Kirchner")"
echo "          $(dim "recovery. Conditionality terms are the inputs.")"
echo "          $(dim "The simulation produces the consequences.")''"
echo ""
echo "  Step 3  Next Step × 4 (step counter: 1/4 → 2/4 → 3/4 → 4/4)"
echo "          '$(dim "Each step is one year: 2001 through 2004.")"
echo "          $(dim "Watch the trajectory view — four curves, one per framework.")"
echo "          $(dim "The step labels come from the historical event record.")''"
echo "          $(bold 'PAUSE at Step 3.') This is the thesis frame."
echo ""
echo "  Step 4  At Step 3: point to $(bold 'Zone 1A — Trajectory View')"
echo "          '$(dim "Step 3 is 2003 — the Kirchner recovery begins.")"
echo "          $(dim "Watch the financial curve: it is rising from the step 2 trough.")"
echo "          $(dim "Watch the governance curve: it is still flat in the breach zone.")"
echo "          $(dim "Financial recovery and institutional recovery are not the same event.")"
echo "          $(dim "No single-axis tool shows both simultaneously. This one does.")''"
echo "          $(bold 'PAUSE — let them read Zone 1B.')"
echo ""
echo "  Step 5  Point to $(bold 'Zone 1B — MDA Alert Panel') (governance WARNING)"
echo "          '$(dim "This is a Minimum Descent Altitude alert.")"
echo "          $(dim "MDA-GOV-DEMOCRACY-FLOOR: democratic quality score has dropped")"
echo "          $(dim "below 0.70 — the threshold below which institutions lose")"
echo "          $(dim "their protective function. Step 3. Governance framework.")"
echo "          $(dim "Read that as evidence you can cite in a negotiation.")''"
echo ""
echo "  Step 6  Point to $(bold 'Zone 1D — Four-Framework') current position"
echo "          '$(dim "Four axes: financial, human development, ecological, governance.")"
echo "          $(dim "Ecological and governance are live composite scores.")"
echo "          $(dim "The ecological score — 1.07 — means Argentina is 7 percent")"
echo "          $(dim "beyond the CO2 planetary boundary. The reference is 1.0.")"
echo "          $(dim "Governance: 0.665 — below the MDA floor. Financial and human")"
echo "          $(dim "development composites are deferred to a multi-country comparison")"
echo "          $(dim "framework — the indicators are live, the composite is not yet")"
echo "          $(dim "meaningful for a single entity. That is disclosed, not hidden.")''"
echo ""
echo "  Step 7  Advance to Step 4 → show Zone 1A full arc (all four steps visible)"
echo "          '$(dim "Step 4 is 2004 — GDP growing at plus 9 percent.")"
echo "          $(dim "Look at the trajectory: the financial arc has recovered.")"
echo "          $(dim "The governance arc is healing slowly.")"
echo "          $(dim "Same engine as Greece. Different crisis arc. Same analytical")"
echo "          $(dim "discipline. That is the Platform Principle.")''"
echo ""
echo "  $(yellow '[ 8:00 – 13:00 ]')  $(bold 'BACKTESTING CREDIBILITY')"
echo "  Lead with the IMF multiplier error (Blanchard-Leigh 2013):"
echo "  assumed 0.5, empirical 1.5. Three times what programmes used."
echo "  Five cases: Greece, Argentina, Lebanon, Thailand, Ecuador."
echo "  DIRECTION_ONLY = 'did GDP go up or down?' Pass on all five."
echo "  '$(dim "A model that gets the sign right across five distinct crisis")"
echo "   $(dim "mechanisms is capturing real causal dynamics.")''"
echo ""
echo "  $(bold 'Name the MAGNITUDE milestone — Argentina is the proof point:')"
echo "  '$(dim "The Argentina 2002 step is also the first case where the model is")"
echo "   $(dim "validated not just on direction but on magnitude: simulated GDP")"
echo "   $(dim "contraction of negative 10.55 percent against the historical")"
echo "   $(dim "negative 10.9 percent. Deviation: 3.2 percent. That is a material")"
echo "   $(dim "result — we are not claiming it before we have evidence for it.")''"
echo ""
echo "  $(yellow '[ 13:00 – 18:00 ]')  $(bold 'ROADMAP')"
echo "  M9: Standards Foundation — GovernanceModule promoted, WGI certified. Delivered."
echo "  M10: Engine Integrity and Instrument Delivery — all four Zone 1 axes live."
echo "       Argentina 2001-2002 second country fixture. PMM live. Delivered."
echo "  M11: Engine Investigation and Political Economy — ADR-009 (sparse matrix proof),"
echo "       political economy module (conditionality, elite capture). Next milestone."
echo "  Frame as expanding capability, not missing features."
echo "  Frame M11 as: 'The backtesting evidence tells us where to look next.'"
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
echo "  for scripted responses to the five most likely questions."
echo ""
echo "$(bold '─── HONEST DISCLOSURES (available if asked) ────────────────────')"
echo ""
echo "  • Distributions are pre-calibration. Bands show reasonable range,"
echo "    not empirically calibrated confidence intervals. Disclosed in UI."
echo "  • Ecological composite score is CO2-only. Other planetary boundary"
echo "    indicators (biodiversity, nitrogen, water) are future milestone scope."
echo "  • Financial and human development composites are null for single-entity"
echo "    scenarios — percentile rank requires ≥2 entities (Issue #193)."
echo "    Indicators (gdp_growth, unemployment_rate) are live."
echo "  • Financial dashed curves in Zone 1A: Path A scoring strategy (normalized"
echo "    absolute; requires ≥2 entities for percentile comparison). Disclosed"
echo "    in the methodology note, not hidden."
echo "  • GDP magnitude at step 2: model produced −10.55% vs historical −10.9%."
echo "    This IS the first MAGNITUDE-validated result. Not all steps are"
echo "    magnitude-validated — step 1 structural gap documented (#222, M11 scope)."
echo "  • GovernanceModule mean-reversion dynamics are simplified at M10."
echo "    Full political economy module (M11) adds conditionality modeling."
echo "  • This tool is not for financial advantage or surveillance."
echo ""
echo "$(bold '─── AUTOMATED WALKTHROUGH ───────────────────────────────────────')"
echo ""

if $RUN_PLAYWRIGHT; then
  echo "$(bold 'Launching Playwright demo walkthrough...')"
  echo "$(dim 'Browser will open. Press Resume in the inspector at each pause.')"
  echo ""
  cd "$REPO_ROOT/frontend"
  npx playwright test tests/e2e/demo-narrated-m10.spec.ts \
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
