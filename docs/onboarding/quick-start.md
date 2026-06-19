# WorldSim Quick Start

> **Time to first insight: 10 minutes.** By the end of this guide you will have
> loaded a scenario, navigated to the instrument cluster, and identified the top
> threshold breach with its severity classification — without any assistance.

---

## What You Will Do

1. Access WorldSim and open the interface
2. Load a scenario using the scenario creation form
3. Navigate to the instrument cluster and read Zone 1B (threshold alerts)
4. Interpret your first MDA alert and its severity classification

You do not need to understand the simulation engine, the underlying model, or
any technical details to complete these steps. The goal of this guide is
working proficiency — the ability to load a scenario and read what it tells you.

---

## Step 1: Access WorldSim

**Local development environment:**

```bash
docker compose up
# In a second terminal, once the API container is healthy:
docker compose exec api alembic upgrade head
docker compose exec api python -m app.db.seed.natural_earth_loader
```

Open `http://localhost:5173` in your browser.

You should see a world map with country entities. The scenario creation panel
is on the right side of the screen.

**If you are accessing a hosted instance:**
Use the URL provided to you by the WorldSim team or your ministry's technical
coordinator.

---

## Step 2: Load a Scenario

The scenario creation form lets you configure which country to analyze, what
time period to examine, and which analytical modules to activate.

**Basic steps:**

1. In the scenario panel on the right, click **"Create Scenario"** (or the
   equivalent "New Scenario" button).
2. Select an entity from the dropdown. For your first scenario, select
   **Jordan** (`JOR`) — a well-documented case with available data.
3. Set the **start date** to `2023-01-01` and leave the step count at the
   default (8 steps).
4. Click **"Create"** or **"Run"** to initialize the scenario.

The choropleth map will highlight the selected country. The instrument cluster
will appear in the main panel area.

**Advance the scenario:** Use the step controls ("Next Step" or the step
counter) to advance the simulation forward. Each step represents a discrete
time period (typically a quarter or year, depending on the scenario).

---

## Step 3: Read the Instrument Cluster

The instrument cluster is divided into zones, each showing a different
analytical perspective. The zones are always visible — you do not need to open
any drawer or navigate away from the main view.

**Zone 1B — Threshold Alerts (MDA Alerts):**

Zone 1B is the most important zone for immediate situational awareness. It
shows active threshold breaches — indicators that have crossed their Minimum
Descent Altitude (MDA) floor. An MDA alert is the simulation's signal that a
monitored indicator has reached a level that, if sustained or worsened, leads
to an irreversible deterioration.

The top row in Zone 1B shows the highest-severity active breach. This is the
first thing to read when you open a scenario. If Zone 1B shows "No active
threshold breaches," the scenario has not reached any critical floors yet —
advance the scenario to observe how indicators evolve.

**Zone 1A — Trajectory View:**
Shows how the composite score for each measurement framework (financial, human
development, ecological, governance) has evolved step by step.

**Zone 1C — PMM Widget:**
Shows the Policy Mix Monitor — how current parameter settings compare to the
modeled baseline.

**Zone 1D — Four-Framework Display:**
Shows the current position of the simulation across all four measurement
frameworks simultaneously, with confidence tier annotations.

---

## Step 4: Interpret Your First MDA Alert

When Zone 1B shows an active breach, you will see:

- **Severity classification** (top label): one of `TERMINAL`, `CRITICAL`, or
  `WARNING`
- **Indicator name**: the specific variable that has crossed its floor
  (e.g., "Reserve Coverage")
- **Current value vs. floor**: what the indicator shows now versus the MDA
  threshold it has crossed
- **Steps to depletion**: how many simulation steps remain before the
  situation reaches its worst-case point, based on the current trajectory

**MDA alert severity classifications:**

| Severity | Meaning |
|---|---|
| `TERMINAL` | The indicator has crossed the irreversible threshold. At the current trajectory, full depletion or systemic collapse occurs within 4 steps or fewer. Immediate intervention is required. |
| `CRITICAL` | The indicator has crossed the warning floor and is approaching the TERMINAL threshold. The situation is serious but not yet irreversible. Policy intervention can still change the trajectory. |
| `WARNING` | The indicator has crossed an early-warning floor. The trajectory is concerning but there is time to respond. Use this as a preparation signal. |

**Reading the detail row in Zone 1B:**

The top slot in Zone 1B shows the full alert detail without any interaction
required. Example:

> "Reserve Coverage — TERMINAL — 2.1 months below the CRITICAL threshold.
> At current draw rate, full depletion occurs in 4 steps."

This is the claim you can take into a meeting. The severity, the indicator, the
distance from the floor, and the time-to-depletion are all present in the
first row.

---

## Next Steps

Now that you can load a scenario and read the instrument cluster, the following
guides will help you interpret what you see more deeply:

- **[Scenario Creation Guide](scenario-creation.md)** — understanding the
  Grounding Strip, scenario parameters, and data provenance flags before
  you run a scenario
- **[Data Provenance Guide](data-provenance.md)** — understanding confidence
  tiers (T1–T5), what they mean for your negotiating position, and how to
  read a Structural Absence Declaration
- **[Methodology Overview](methodology-overview.md)** — what the simulation
  claims, what it does not claim, and the documented model blindspots

---

*For technical setup, contributing, and the simulation architecture, see
[`docs/CONTRIBUTING.md`](../CONTRIBUTING.md).*
