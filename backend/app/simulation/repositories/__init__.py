"""Simulation repositories — database I/O boundary for ADR-004 Decision 2.

SimulationStateRepository: loads initial SimulationState from PostGIS.
ScenarioSnapshotRepository: writes/reads step snapshots to scenario_state_snapshots.

quantity_serde: Quantity ↔ JSONB envelope serialization (SA-09 format).
"""
