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
  echo "$(yellow 'Warning: seed command returned non-zero. ZMB entity may already exist — proceeding.')"
fi

# ── Presenter guide ───────────────────────────────────────────────────────────

echo ""
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo "$(bold '  PRESENTER GUIDE — WorldSim Stakeholder Demonstration (M14)')"
echo "$(bold '══════════════════════════════════════════════════════════════════')"
echo ""
echo "$(bold 'Stack status:')"
echo "  API:       $(green 'http://localhost:8000')  $(dim '(FastAPI + PostGIS)')"
echo "  Frontend:  $(green 'http://localhost:5173')  $(dim '(React + MapLibre GL)')"
echo ""
echo "$(bold 'Open the application in a browser now:')"
echo "  $(green "$FRONTEND_URL")"
echo ""
echo "$(bold 'Demo 5 — Zambia 2024, IMF Extended Credit Facility Review')"
echo "  Single entity. Six annual steps. Trust architecture (ADR-016 + ADR-015)."
echo "  The challenge moment: creditor challenges reserve coverage figure."
echo "  The ministry response: Grounding strip citation on screen at zero interaction."
echo "  Political economy module live: programme_survival_probability in Zone 1D."
echo "  No Mode 3 in Demo 5 scope (EL decision 2026-06-19)."
echo "  Full script: docs/demo/m14/stakeholder-walkthrough.md"
echo ""
echo "$(bold '─── TIMING GUIDE (20 minutes + Q&A) ────────────────────────────')"
echo ""
echo "  $(yellow '[ 0:00 – 3:00 ]')  $(bold 'SECTION 1 — THE ROOM')"
echo "  Open: 'There is a room where this happens.'"
echo "  On one side: creditor team. Institutional memory. Proprietary models."
echo "  On the other: finance ministry, three economists, public data."
echo "  The question is never 'do you have a model?' The question is:"
echo "  'Can you defend your number?' Today the ministry team can."
echo "  Do NOT use warning language. The trust architecture is capability, not alarm."
echo ""
echo "  $(yellow '[ 3:00 – 11:00 ]')  $(bold 'SECTION 2 — LIVE APPLICATION')"
echo ""
echo "  Presentation order: C → A → B → D → E (thesis frame first)"
echo ""
echo "  Step 1  Scenarios panel → select '$(bold "Zambia 2024 IMF ECF Review Demo 5")'"
echo "          → Select as primary. Advance to step 1 (2024, IMF program accepted)."
echo "          '$(bold "FRAME A:") The Grounding strip. Before the analysis runs, every'"
echo "          'initial number has a named source, a confidence tier, and a date.'"
echo "          'Reserve coverage: 3.8 months. Source: IMF WEO Apr 2024. Tier two.'"
echo "          'The trust architecture is visible from moment one.'"
echo "          '$(bold "Zone 1A:") Reserve trajectory with T2 badge on the curve.'"
echo "          Do NOT say 'watch Zambia shift on the map' — the instrument carries the argument."
echo ""
echo "  Step 2  Advance to step 2 (2025, fiscal conditionality begins)."
echo "          '$(bold "FRAME C — THESIS:") The creditor challenges the 3.8-month figure.'"
echo "          'The analyst reads the answer off the screen.'"
echo "          '$(bold "Zone 1B:") Reserve coverage with tier label visible — T2 · IMF WEO Apr 2024.'"
echo "          'The self-interpreting sentence names the threshold and the direction.'"
echo "          'Source is the IMF's own publication. Creditor is challenging their own dataset.'"
echo "          '$(bold "PAUSE. Let them read Zone 1B and the Grounding strip simultaneously.")'"
echo ""
echo "  Step 3  '$(bold "FRAME B:") The alert in detail. Layer 3 output — what the number means.'"
echo "          'Not just 3.2 months. At current draw rate, CRITICAL in 2 steps.'"
echo "          'Indicator name: Reserve Coverage (months). Not a database field name.'"
echo "          'Tier label: human-readable. Direction of risk: on screen.'"
echo ""
echo "  Step 4  Advance to step 3 (2026, CRITICAL threshold crossed)."
echo "          '$(bold "FRAME D:") Zone 1D. Four composites plus programme survival probability.'"
echo "          'This is a new capability. The model asks: can this programme'"
echo "          'actually be implemented given the fiscal pressure? That is a'"
echo "          'different question from whether IMF approved it.'"
echo "          'Reserve CRITICAL and PSP are on the same instrument.'"
echo "          'Related signals. Not the same constraint.'"
echo ""
echo "  Step 5  Advance to step 5 (2028). Advance step 4 silently."
echo "          '$(bold "FRAME E:") The full evidence thread. Five steps of the arc.'"
echo "          'Every number: named source. Every input: visible in assumption surface.'"
echo "          'The ministry team can defend every finding at the table.'"
echo "          'Without specialist mediation. The kryptonite constraint met.'"
echo ""
echo "  $(yellow '[ 11:00 – 16:00 ]')  $(bold 'SECTION 3 — BACKTESTING CREDIBILITY')"
echo "  Blanchard-Leigh 2013: assumed multiplier 0.5, empirical 1.5."
echo "  Same epistemic problem this tool addresses: assumptions in consequential"
echo "  decisions not visible to affected parties."
echo "  Five validated cases: Greece, Argentina, Lebanon, Thailand, Ecuador."
echo "  DIRECTION_ONLY on all five. Argentina year 1: MAGNITUDE calibrated (3.2% deviation)."
echo "  Zambia is not yet a backtested case — honest disclosure. The reserve coverage"
echo "  trajectory is scenario output, not calibrated prediction."
echo ""
echo "  $(yellow '[ 16:00 – 19:00 ]')  $(bold 'SECTION 4 — WHAT IS BEING BUILT')"
echo "  M14 delivers two capabilities demonstrated today:"
echo "  $(bold '  Trust architecture:') ADR-016 Grounding strip + ADR-015 Evidence thread."
echo "  $(bold '  Political economy module:') Programme survival probability."
echo "  Answers the challenge moment. Does not require specialist mediation."
echo "  What comes next (M15/M16): counter-proposal branch (Mode 3 + trust arc),"
echo "  cross-examination of composite decomposition (ADR-015 Component 4)."
echo "  Technical Steering Committee: first governance actor independent of EL."
echo ""
echo "  $(yellow '[ 19:00 – 20:00 ]')  $(bold 'NORTH STAR CLOSING — 1 minute exactly')"
echo "  '$(dim "There is a quinoa farmer in Bolivia who will never know this")"
echo "   $(dim "tool exists. His government might. If his government has a finance")"
echo "   $(dim "minister with better analytical tools, that minister can negotiate")"
echo "   $(dim "better terms. The quinoa farmer lives at the end of that chain.")"
echo "   $(dim "Build it as if he does.")''"
echo ""
echo "  $(yellow '[ 20:00 – 30:00 ]')  $(bold 'Q&A')"
echo "  See docs/demo/m14/stakeholder-walkthrough.md §Q&A Preparation"
echo "  for scripted responses to the five most likely questions."
echo ""
echo "$(bold '─── HONEST DISCLOSURES (available if asked) ────────────────────')"
echo ""
echo "  • Zambia is not yet a backtested case. The reserve coverage trajectory"
echo "    is scenario output under the configured initial attributes and scheduled"
echo "    inputs. It is not a calibrated prediction of Zambia's actual trajectory."
echo "  • Ecological and governance data for Zambia: T4 (synthetic extrapolation"
echo "    from SADC comparable economies). The tool labels this visibly in Zone 1B."
echo "    This is the No False Precision principle in action — the tool says what"
echo "    it knows and what it inferred."
echo "  • Political economy module (PSP): the model's assessment of programme"
echo "    implementation capacity under the current fiscal trajectory. Not an IMF view."
echo "    Not a political prediction. A quantified constraint estimate."
echo "  • No Mode 3 in Demo 5. The counter-proposal capability (Mode 3 + trust arc)"
echo "    is M15 scope. If asked: 'Today we show the trust architecture — the ability"
echo "    to source and defend every number. The next demo cycle combines both.'"
echo "  • Uncertainty bands are pre-calibration. Bands show reasonable range,"
echo "    not empirically calibrated confidence intervals. Disclosed in UI."
echo "  • This tool is not for financial advantage or surveillance."
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
