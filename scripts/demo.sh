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
echo "$(bold '  PRESENTER GUIDE — WorldSim Stakeholder Demonstration (M12)')"
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo ""
echo "$(bold 'Stack status:')"
echo "  API:       $(green 'http://localhost:8000')  $(dim '(FastAPI + PostGIS)')"
echo "  Frontend:  $(green 'http://localhost:5173')  $(dim '(React + MapLibre GL)')"
echo ""
echo "$(bold 'Open the application in a browser now:')"
echo "  $(green "$FRONTEND_URL")"
echo ""
echo "$(bold 'Demo 4 — Jordan + Egypt, Strait of Hormuz 2024–2031')"
echo "  Eight steps. Two entities. ExternalSectorModule live (ADR-012)."
echo "  Same fuel+food commodity shock, different import profiles → divergent crises."
echo "  All four composite scores live simultaneously for the first time."
echo "  Mode 3 Active Control: branch from step 3 at 1.30× fiscal multiplier."
echo "  Full script: docs/demo/m12/stakeholder-walkthrough.md"
echo ""
echo "$(bold '─── TIMING GUIDE (22 minutes + Q&A) ────────────────────────────')"
echo ""
echo "  $(yellow '[ 0:00 – 3:00 ]')  $(bold 'SECTION 1 — THE PROBLEM')"
echo "  Open: 'There is a room where this happens.'"
echo "  On one side: IMF team with proprietary models, institutional memory."
echo "  On the other: finance ministry, two economists, spreadsheets, public data."
echo "  The factory worker in Amman. The hospital losing 15% of its operating budget."
echo "  None of those people are in the room. The minister is the only one between"
echo "  them and what gets decided in the next three hours."
echo "  Do NOT use warning language. The human cost ledger is analytical capability."
echo ""
echo "  $(yellow '[ 3:00 – 11:00 ]')  $(bold 'SECTION 2 — LIVE APPLICATION (Act 1 + Act 2)')"
echo ""
echo "  $(bold 'ACT 1 — The baseline reveals the consequence')"
echo ""
echo "  Step 1  Map loads. Do not linger on the choropleth."
echo "          'This is a platform — one analytical framework, different ingredients.'"
echo "          'The instrument is the panel on the left, not the map.'"
echo ""
echo "  Step 2  Scenarios panel → select '$(bold 'Jordan/Egypt 2024 Hormuz Demo 4')'"
echo "          → Select as primary."
echo "          'Jordan fuel import dependency 0.42. Egypt food import dependency 0.35.'"
echo "          'The same external shock lands differently on two import structures.'"
echo "          '$(bold 'Zone 1D:') All four composite scores live — first time in Demo history.'"
echo ""
echo "  Step 3  Advance to step 3 (2026) — $(bold 'PAUSE. This is the thesis frame.')"
echo "          'Jordan reserves: 5.0 months, burning at ~1.2 months per step.'"
echo "          'Egypt governance: 0.07 on V-Dem LDI — already at one-tenth of the floor.'"
echo "          '$(bold 'Zone 1B:') Egypt governance alert is CRITICAL from step 1.'"
echo "          'That is not a step 3 finding. It is a pre-existing structural condition.'"
echo "          $(bold 'PAUSE. Let them read Zone 1B.')"
echo "          'Two alert states. Two entirely different policy problems.'"
echo ""
echo "  Step 4  Advance to step 5 (2028) without stopping at step 4."
echo "          At step 5: '$(bold 'Zone 1B:') Jordan reserve CRITICAL.'"
echo "          'Reserve_coverage_months: 2.5. The IMF minimum adequate reserve benchmark.'"
echo "          'Zone 1A unemployment: GCC support drove 17.73%→16.59% at step 4.'"
echo "          'Conditionality reversed it: 16.59%→17.25% at step 5. One step. Clawed back.'"
echo "          $(bold 'PAUSE. Continue advancing silently to step 7.')"
echo "          At step 7: 'Three TERMINAL alerts. Reserves at zero. Three simultaneous breaches.'"
echo "          'The baseline produces this over eight years. That is what the minister sees.'"
echo "          'The ministry team does not accept this as inevitable.'"
echo ""
echo "  $(bold 'ACT 2 — Mode 3 tests a counter-proposal')"
echo ""
echo "  Step 5  $(bold 'Mode 3 Active Control') — branch from step 3, 1.30× multiplier."
echo "          'GCC partners have provided emergency support to Jordan three times"
echo "          in recent history: 2012-13 (Arab Spring), 2018 (fiscal crisis),"
echo "          2023 (IMF co-financing). This is not an imaginary intervention.'"
echo "          Enable Mode 3 toggle. Set fiscal multiplier to 1.30. Apply Change."
echo "          'The branch: IMF liquidity at step 3 stays. Austerity at step 4 does not.'"
echo "          '\"We accept the programme. We negotiate away the spending cut.\"'"
echo "          $(bold 'PAUSE. Read Zone 1A — step 5 is where the divergence peaks.')"
echo "          '$(bold 'Primary divergence at step 5:') +1.70pp GDP. Unemployment does not reverse.'"
echo "          'The reserve curve: identical in baseline and branch. Both reach zero by step 7.'"
echo "          '$(bold 'The reserve crisis is survived under better conditions, not avoided.')'"
echo "          'The minister should know this before she uses this finding.'"
echo "          'That is a different conversation than the one that happened in Athens in 2010.'"
echo ""
echo "  Step 6  $(bold 'Zone 1D — All Four Axes (step 5, 2028)')"
echo "          'Financial: reserve-linked divergence between JOR and EGY.'"
echo "          'Human Development: bottom-quintile consumption capacity eroded.'"
echo "          'Ecological: CO2 accumulation independent of the Hormuz crisis.'"
echo "          'Governance: Egypt far below floor from step 1. Jordan stable.'"
echo "          'No axis is null. No axis is dashed. This is the M12 measurement claim.'"
echo "          'Greece 2014 looked like recovery on GDP. It was not recovery on unemployment,"
echo "          child poverty, or life expectancy. The four-axis view shows that in the room,"
echo "          in the moment when it can still be argued at the table.'"
echo ""
echo "  $(yellow '[ 11:00 – 16:00 ]')  $(bold 'SECTION 3 — BACKTESTING CREDIBILITY')"
echo "  IMF multiplier error: Blanchard-Leigh 2013. Assumed 0.5, empirical 1.5."
echo "  Five validated cases: Greece, Argentina, Lebanon, Thailand, Ecuador."
echo "  DIRECTION_ONLY on all five. Argentina year 1: MAGNITUDE calibrated."
echo "  '$(dim "Simulated contraction: −10.55%. Historical: −10.9%. Deviation: 3.2%.")"
echo "   $(dim "That is a material result. We are not claiming it before we have evidence.")''"
echo "  Ecuador is the recovery case: distinguishes stabilization from continued decline."
echo "  Same engine that runs Jordan and Egypt ran all five validated cases."
echo ""
echo "  $(yellow '[ 16:00 – 20:00 ]')  $(bold 'SECTION 4 — WHAT IS BEING BUILT (M13)')"
echo "  'What you saw is the platform at the limit of what it can honestly claim.'"
echo "  'Three questions a sophisticated negotiator would ask remain unanswerable today.'"
echo "  $(bold 'Political feasibility gap:') M13 Political Economy Module — programme survival"
echo "  probability. Shifts from 'what does this produce?' to 'can this government deliver it?'"
echo "  $(bold 'Conditionality design gap:') M13 models alternative programme structures"
echo "  comparable on the same instrument — not binary accept/reject."
echo "  $(bold 'Medium-term horizon gap:') M13 makes years 9–15 debt sustainability examinable."
echo "  '$(dim "Honest note: demo cadence is every two milestones.")"
echo "   $(dim "The next demo reflects M14 capability. M13 is the foundation.")''"
echo ""
echo "  $(yellow '[ 20:00 – 21:00 ]')  $(bold 'NORTH STAR CLOSING — 1 minute exactly')"
echo "  '$(dim "There is a quinoa farmer in Bolivia who will never know this")"
echo "   $(dim "tool exists. His government might. If his government has a finance")"
echo "   $(dim "minister with better analytical tools, that minister can negotiate")"
echo "   $(dim "better terms. The quinoa farmer lives at the end of that chain.")"
echo "   $(dim "Build it as if he does.")''"
echo ""
echo "  $(yellow '[ 21:00 – 30:00 ]')  $(bold 'Q&A')"
echo "  See docs/demo/m12/stakeholder-walkthrough.md §Q&A Preparation"
echo "  for scripted responses to the five most likely questions."
echo ""
echo "$(bold '─── HONEST DISCLOSURES (available if asked) ────────────────────')"
echo ""
echo "  • Distributions are pre-calibration. Bands show reasonable range,"
echo "    not empirically calibrated confidence intervals. Disclosed in UI."
echo "  • Ecological composite score is CO2-only in M12. Land use pressure"
echo "    is in measurement output but does not drive the composite."
echo "    Full multi-boundary ecological composite is M13 scope."
echo "  • Commodity shock transmission is directional, not magnitude-calibrated."
echo "    Reserve level projections are scenario outputs, not predictions."
echo "  • Mode 3 does not recommend — it shows consequences. Political feasibility"
echo "    is M13. Mode 3 is the counter-proposal function, not a prescriber."
echo "  • Reserve depletion is identical in baseline and Mode 3 branch."
echo "    Better conditionality terms improve GDP and unemployment trajectories."
echo "    They do not change Jordan's structural import dependency. State this"
echo "    explicitly when presenting the Mode 3 comparison."
echo "  • Egypt's governance CRITICAL alert fires from step 1. This is correct —"
echo "    democratic quality score 0.07 (V-Dem 2023). Not a model artifact."
echo "  • Argentina MAGNITUDE calibration: −10.55% vs historical −10.9% (deviation 3.2%)."
echo "    This is the first MAGNITUDE result. Remaining four cases are DIRECTION_ONLY."
echo "  • This tool is not for financial advantage or surveillance."
echo ""
echo "$(bold '─── AUTOMATED WALKTHROUGH ───────────────────────────────────────')"
echo ""

if $RUN_PLAYWRIGHT; then
  echo "$(bold 'Launching Playwright demo walkthrough...')"
  echo "$(dim 'Browser will open. Press Resume in the inspector at each pause.')"
  echo ""
  cd "$REPO_ROOT/frontend"
  npx playwright test tests/e2e/demo-narrated.spec.ts \
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
