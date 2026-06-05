# Cloud Compute Path

**Issue:** #750
**Author:** Chief Engineer Agent
**Reviewed by:** Chief Engineer Agent (performance accuracy)
**Date:** 2026-06-05
**Dependency:** ADR-009 (matrix engine in production, PR #769 merged 2026-06-05)

---

## Purpose

The matrix engine enables high-resolution multi-country scenarios that may exceed the performance envelope of a standard laptop. This document defines:

1. What triggers the need for cloud compute
2. The minimum viable laptop configuration for the canonical user (single-country, standard resolution)
3. Cloud provider options with indicative pricing at each resolution tier
4. Self-hosted alternatives for institutions with their own infrastructure

This document is grounded in Phase 1 baseline benchmarks (`docs/architecture/performance/phase1-iterative-baseline.md`, Issue #514, 2026-05-31) measured on the ProBook reference hardware (Intel i5-8265U, 8 GiB RAM) — the minimum viable configuration for the democratization mission.

---

## Equitable Build Process Confirmation

**The standard single-country scenario stays within the 8GB/4-core laptop envelope.**

The Phase 1 benchmarks establish the following on the ProBook (i5-8265U, 8 GiB RAM, the equity baseline):

| Scenario | ProBook cost | Headroom |
|---|---|---|
| Single step, 1 entity | 0.0074 ms | — |
| Single step, 100 entities | 0.089 ms | 11,000 steps/s |
| 15-year annual simulation, 100 entities | < 2 ms compute | Negligible |
| 1,000 MC runs, 1 entity, 10 steps | 174 ms total | Well within interactive budget |
| Peak memory, 100 entities / 1,000 relationships | 0.108 MiB | << 8 GiB |

The standard use case — single-country scenario, 10–30 annual steps, 1,000 Monte Carlo runs — completes in under 200 ms of compute time on a 2019-era Intel laptop with 8 GiB RAM. **Cloud compute is not required for the canonical user** (a finance ministry analyst running single-country scenario analysis). The Equitable Build Process constraint (CLAUDE.md §Equitable Build Process) is satisfied without qualification.

The matrix engine (ADR-009, production as of M12) does not change this assessment for standard scenarios. Matrix multiplication at low entity counts (< 200) carries overhead comparable to the iterative engine; the matrix engine's advantage materialises at high entity counts and dense relationship graphs, which is the institutional multi-country use case, not the standard use case.

---

## Minimum Viable Laptop Configuration

For a global south finance ministry analyst running the WorldSim standard use case:

| Component | Minimum | Notes |
|---|---|---|
| CPU | 4-core, any 2018+ x86-64 or ARM | Intel i5-8265U is the verified baseline |
| RAM | 8 GiB | 100-entity scenarios use < 1 MiB; 7 GiB headroom for OS and browser |
| Storage | 10 GiB free | Docker images ~4 GiB; database ~1 GiB for 5 years of scenario data |
| OS | Ubuntu 20.04+, macOS 12+, Windows 10+ | Python 3.13, Docker Desktop (or native Docker on Linux) |
| Network | Intermittent is acceptable | All computation is local; network only for initial setup |
| GPU | Not required | The simulation engine is CPU-bound at standard scale |

A contributor on a 2019 mid-range laptop with 8 GiB RAM can run the full test suite, the FastAPI backend, the Vite frontend, and a PostGIS database simultaneously within this envelope. This has been verified against the CI runner specification (2-core, 7 GiB RAM, Ubuntu).

---

## When Cloud Compute Becomes Necessary

Cloud compute is warranted when any of the following conditions are met:

### Condition 1 — Multi-country scenario at full regional scale (> 50 entities)

Phase 1 benchmarks show propagation cost is driven by edge density, not entity count. A moderately connected 50-country scenario (50 entities, ~500 relationships, ~10 edges/entity) is well within laptop range. The transition point is a dense multi-country graph:

| Configuration | ProBook cost/step | 100-step scenario | Verdict |
|---|---|---|---|
| 100 entities, 1,000 relationships (sparse) | 1.15 ms | 115 ms | Laptop |
| 50 entities, 200 relationships (dense, 4 edges/entity) | ~0.8 ms* | 80 ms | Laptop |
| 200 entities, 4,000 relationships (sparse) | ~4.5 ms* | 450 ms | Laptop |
| 500 entities, 50,000 relationships (dense) | ~250 ms* | 25 s | Cloud threshold |
| Full G20, dense trade graph (20 entities, 380 relationships) | ~3 ms* | 300 ms | Laptop |

*Projected from Phase 1 scaling characteristics; Phase 2 A/B report (`docs/architecture/performance/phase2-ab-comparison.md`) will confirm matrix engine numbers at these scales.

**Practical trigger:** When a single 100-step scenario run takes longer than 30 seconds on the analyst's laptop, cloud offload becomes worth the operational cost.

### Condition 2 — High-resolution Monte Carlo (> 10,000 runs)

The ProBook achieves ~5,750 single-entity runs per second. At 100 entities (more realistic), throughput drops to roughly 80–100 runs per second (extrapolated from per-step cost). At this rate:

| Ensemble size | ProBook estimate | Laptop viable? |
|---|---|---|
| 1,000 runs | ~10–12 s | Yes |
| 10,000 runs | ~100–120 s | Marginal (2 min) |
| 100,000 runs | ~1,000 s | No — cloud threshold |

The ADR-006 Monte Carlo minimum sample sizes for full distributional output require 10,000 runs for robust confidence intervals. This is at the marginal boundary for a constrained laptop. Institutional users conducting multi-country scenario analysis with full uncertainty quantification should plan for cloud or self-hosted compute.

### Condition 3 — Full backtesting suite with live database

The Greece 2010–2012 backtesting suite (`tests/backtesting/`) requires a live PostGIS database and runs the full simulation for each historical data point. This is not a laptop-scale workload for institutional fidelity studies covering multiple countries and decades. CI handles this on GitHub Actions runners for continuous validation.

---

## Cloud Provider Options

All pricing is indicative (June 2026). Actual cost depends on region, reserved vs. on-demand pricing, and data transfer.

### Tier 1 — Single-country analyst (occasionally needed)

**Use case:** Finance ministry analyst running occasional high-resolution scenario (10,000 MC runs, single country).

| Provider | Instance | vCPU | RAM | Indicative cost/hr | 2-hour session |
|---|---|---|---|---|---|
| AWS | t3.medium | 2 | 4 GiB | ~$0.047 | ~$0.09 |
| GCP | e2-medium | 2 | 4 GiB | ~$0.034 | ~$0.07 |
| Azure | B2s | 2 | 4 GiB | ~$0.050 | ~$0.10 |
| Hetzner (EU) | CPX21 | 3 | 4 GiB | ~$0.010 | ~$0.02 |

**Recommendation:** Hetzner for EU-based institutions or researchers; GCP e2-medium for elsewhere. A 2-hour session costs less than a cup of coffee. The WorldSim Docker Compose stack starts cold in under 5 minutes on any of these.

### Tier 2 — Multi-country institutional analysis (regular use)

**Use case:** Central bank or finance ministry running weekly multi-country simulations with full MC ensemble, using the WorldSim platform as a standing analytical tool.

| Provider | Instance | vCPU | RAM | Indicative cost/hr | Monthly (40 hrs/week) |
|---|---|---|---|---|---|
| AWS | c6i.2xlarge | 8 | 16 GiB | ~$0.340 | ~$547 |
| GCP | c2-standard-8 | 8 | 32 GiB | ~$0.381 | ~$610 |
| Azure | F8s v2 | 8 | 16 GiB | ~$0.339 | ~$544 |
| Hetzner | CCX33 | 8 | 32 GiB | ~$0.078 | ~$125 |

**Note:** Monthly costs assume 40 compute-hours per week — sessions are not 24/7. Actual usage for a finance ministry analytical team is likely 20–40 hours per month, not per week, which reduces cost by 4–5×.

**Recommendation for resource-constrained institutions:** A Hetzner CCX33 at ~$0.078/hr is 4–5× cheaper than equivalent AWS/GCP/Azure at comparable CPU and RAM. For a global south finance ministry, this is the recommended starting point.

### Tier 3 — Research institution / academic (full backtesting + MC)

**Use case:** Academic research group running full country panel backtesting, multi-decade historical validation, and large MC ensembles.

| Provider | Instance | vCPU | RAM | Indicative cost/hr |
|---|---|---|---|---|
| AWS | c6i.8xlarge | 32 | 64 GiB | ~$1.36 |
| GCP | c2-standard-30 | 30 | 120 GiB | ~$1.47 |
| Azure | F32s v2 | 32 | 64 GiB | ~$1.36 |
| Hetzner | CCX63 | 48 | 192 GiB | ~$0.46 |

**Note on GPU:** The simulation engine is CPU-bound; GPU instances provide no benefit and are not recommended. Matrix multiplication at the entity counts WorldSim operates at (tens to low hundreds) does not saturate a CPU and cannot use GPU parallelism efficiently.

---

## Self-Hosted Options

Institutions with their own server infrastructure can self-host without cloud costs. WorldSim's Docker Compose stack runs on any Linux host with Docker installed.

### Minimum self-hosted server specification (Tier 2 equivalent)

| Component | Minimum | Recommended |
|---|---|---|
| CPU | 4-core x86-64, 2.5 GHz+ | 8-core, any modern server CPU |
| RAM | 16 GiB | 32 GiB |
| Storage | 100 GiB SSD | 500 GiB SSD (historical data accumulates) |
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| Network | 100 Mbps | 1 Gbps (for multi-user access) |

### Deployment

```bash
# Clone the repository
git clone https://github.com/PublicEnemage/worldsim.git
cd worldsim

# Start the full stack (PostGIS, FastAPI, Vite)
docker compose up -d --build

# Run database migrations
docker compose exec api alembic upgrade head

# Seed Natural Earth data
docker compose exec api python -m app.db.seed.natural_earth_loader
```

The self-hosted stack is identical to the development stack. There is no separate "server edition" — the Docker Compose file is the deployment artifact.

### Multi-user considerations

The FastAPI backend is stateless between requests; the PostGIS database is the only shared state. Multiple analysts can run concurrent scenarios without interference. The primary bottleneck at multi-user scale is database write throughput for scenario state; this becomes relevant above ~10 concurrent active simulations. At that scale, a dedicated PostgreSQL instance (separate from the app server) with connection pooling (PgBouncer) is the next scaling step.

### Air-gapped deployment

For institutions with air-gapped networks (central banks with security-isolated analytical environments):

1. Build Docker images on an internet-connected machine: `docker compose build`
2. Export images: `docker save worldsim_api worldsim_db | gzip > worldsim-images.tar.gz`
3. Transfer the tarball and the repository to the air-gapped environment
4. Load on the target host: `docker load < worldsim-images.tar.gz`
5. Run `docker compose up -d` — no outbound network connections are made at runtime

No API keys, license checks, or telemetry are present in the WorldSim stack. Air-gapped deployment is fully supported.

---

## Cost Summary

| User type | Hardware | Monthly cost | Notes |
|---|---|---|---|
| Finance ministry analyst (standard use) | 8 GiB laptop | $0 | No cloud needed |
| Analyst needing occasional high-MC runs | Cloud Tier 1 (on-demand) | < $5/mo | Pay per session |
| Institutional analytical team (weekly use) | Cloud Tier 2 or self-hosted | $30–150/mo | Hetzner or own server |
| Research institution (full backtesting) | Cloud Tier 3 or self-hosted | $100–500/mo | Depends on run frequency |

---

## References

- Phase 1 baseline benchmarks: `docs/architecture/performance/phase1-iterative-baseline.md`
- Phase 2 A/B comparison (pending): `docs/architecture/performance/phase2-ab-comparison.md`
- ADR-009: `docs/adr/ADR-009-simulation-engine-computation-model.md`
- CLAUDE.md §Equitable Build Process
- Equitable build requirements: `docs/CONTRIBUTING.md §Equitable Build Process`
