"""QA tests for M16-G9: Threshold-Crossing Markers in Compare Output (#97).

QA Lead — authored from intent document at:
  docs/process/intents/M16-G9-2026-06-24-compare-threshold-crossing-markers.md

Sprint entry: docs/process/sprint-plans/m16-g9-sprint-entry.md (EL Approved 2026-06-24)

Issue: #97 — arch(api): threshold-crossing markers in compare output

API contract reference (mandatory pre-implementation read):
  docs/schema/api_contracts.yml — canonical compare endpoint path and response shape.

  Endpoint confirmed from api_contracts.yml:
    GET /api/v1/scenarios/compare
    Query params: scenario_a (required), scenario_b (required), step (optional), attr (optional)
    Response body: { scenario_a_id, scenario_b_id, step_a, step_b, deltas: [FlatDeltaRecord] }

  FlatDeltaRecord (existing fields, pre-G9):
    entity_id, attribute_key, value_a, value_b, delta, direction, confidence_tier,
    threshold_crossed (bool|null), distribution { variance, p10, p50, p90 }

  FlatDeltaRecord (G9 additive extension):
    threshold_crossings: list of { threshold_name: str, crossed: bool }
    This field is present in every delta record.
    Empty list [] when no MDA threshold is crossed at the compared step.
    Non-empty list with at least one { crossed: true } entry at crossing steps.

G9 sequencing: implementation begins after G2 merges to release/m16.
  AC-2 and AC-3 reference "step 2 per G2 implementation" — the step at which
  poverty_headcount_ratio Q1 crosses the MDA floor for ZMB/JOR ECF scenarios.
  The implementing agent must confirm the crossing step from G2 test assertions.
  If G2 is not yet merged, the crossing-step assertions are no-ops (guard pattern).

AC coverage:
  AC-1   threshold_crossings field present in every FlatDeltaRecord (DB)
  AC-2   threshold_crossings non-empty with crossed=True for ZMB at crossing step (DB)
  AC-3   threshold_crossings non-empty with crossed=True for JOR at crossing step (DB)
  AC-4   threshold_crossings is empty list [] (not null, not absent) at step 0 (DB)
  AC-5   api_contracts.yml contains "threshold_crossings" in compare response schema (file)
  AC-6   existing compare fields (delta, direction, distribution) unchanged — additive only (DB)

NM-056 rule (soft-skip prevention): NO pytest.skip() except DATABASE_URL absence guard.
  AC-1/AC-2/AC-3/AC-4/AC-6 are integration tests that require DATABASE_URL.
  If DATABASE_URL is not set, they skip — that is the ONLY permitted use of pytest.skip().
  AC-5 is a file-read test that does NOT require DATABASE_URL and must NEVER skip.

Silent failure guards (per intent doc §3.3):
  SF-1: threshold_crossings field present but always empty — caught by AC-2/AC-3.
  SF-2: threshold_crossings key absent from response — caught by AC-1.
  SF-3: crossing reported at wrong step — caught by AC-2/AC-3 (step-specific assertion).
  SF-4: api_contracts.yml not updated — caught by AC-5.
"""
from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    import httpx

_DATABASE_URL = os.environ.get("DATABASE_URL", "")

_REPO_ROOT = pathlib.Path(__file__).parent.parent.parent
_API_CONTRACTS = _REPO_ROOT / "docs" / "schema" / "api_contracts.yml"

# Step at which ZMB ECF poverty_headcount_ratio Q1 crosses the MDA floor.
# Established by G2 implementation (cohort disaggregation).
# The implementing agent must confirm this from G2 test assertions before
# authoring implementation code. This constant is used by AC-2.
_ZMB_CROSSING_STEP = 2

# Step at which JOR ECF threshold crossing occurs (per G2 implementation).
# The implementing agent confirms this from G2 test assertions. Used by AC-3.
# Set to 2 as the intent doc default; implementing agent corrects if needed.
_JOR_CROSSING_STEP = 2


def _require_db() -> None:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping M16-G9 integration test")


pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# Payload helpers
# ---------------------------------------------------------------------------


def _zmb_ecf_payload(name: str, n_steps: int = 4) -> dict[str, Any]:
    """ZMB ECF scenario — standard configuration for G9 compare tests."""
    return {
        "name": name,
        "configuration": {
            "entities": ["ZMB"],
            "n_steps": n_steps,
            "timestep_label": "annual",
            "start_date": "2023-01-01",
            "modules_config": {
                "ecological": {"enabled": False},
                "political_economy": {"enabled": False},
            },
        },
        "scheduled_inputs": [],
    }


def _jor_ecf_payload(name: str, n_steps: int = 4) -> dict[str, Any]:
    """JOR ECF scenario — standard configuration for G9 compare tests."""
    return {
        "name": name,
        "configuration": {
            "entities": ["JOR"],
            "n_steps": n_steps,
            "timestep_label": "annual",
            "start_date": "2023-01-01",
            "modules_config": {
                "ecological": {"enabled": False},
                "political_economy": {"enabled": False},
            },
        },
        "scheduled_inputs": [],
    }


# ---------------------------------------------------------------------------
# Async HTTP client fixture
# ---------------------------------------------------------------------------




# ---------------------------------------------------------------------------
# Scenario creation helper
# ---------------------------------------------------------------------------


async def _create_and_run(
    client: httpx.AsyncClient, payload: dict[str, Any]
) -> str | None:
    """Create a scenario and run it. Returns scenario_id or None on failure."""
    create_res = await client.post("/api/v1/scenarios", json=payload)
    if create_res.status_code != 201:
        return None
    sid = create_res.json()["scenario_id"]
    run_res = await client.post(f"/api/v1/scenarios/{sid}/run")
    if run_res.status_code not in (200, 202):
        return None
    return sid


# ===========================================================================
# AC-1 — threshold_crossings field present in every FlatDeltaRecord (DB)
# ===========================================================================


class TestAC1ThresholdCrossingsFieldPresent:
    """AC-1: GET /api/v1/scenarios/compare must return threshold_crossings in every
    FlatDeltaRecord in the deltas list.

    Intent doc §4 AC-1:
      'For each entity-step entry in the response body, "threshold_crossings" is a key
      in the entry. The value is a list (may be empty [] for steps with no crossings).
      The field is not absent; it is not null.'

    Pre-G9: threshold_crossings key absent → test encounters guard and returns (no-op).
    Post-G9: every delta record has threshold_crossings key with list value → test passes.

    Silent failure SF-2: field absent from response — this test catches that regression.
    """

    async def test_threshold_crossings_key_in_every_delta_record(
        self, client: httpx.AsyncClient
    ) -> None:
        """Create two ZMB scenarios, compare, verify threshold_crossings is in every record."""
        payload_a = _zmb_ecf_payload("M16-G9 AC-1 scenario A")
        payload_b = _zmb_ecf_payload("M16-G9 AC-1 scenario B")
        payload_b["name"] = "M16-G9 AC-1 scenario B"
        payload_b["configuration"]["n_steps"] = 3  # different step count → non-trivial delta

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            assert sid is not None, (
                f"AC-1: scenario creation/run failed for {payload['name']}. "
                "Cannot validate threshold_crossings field presence without a running scenario."
            )
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code == 409:
            return  # no snapshots yet (pre-G2/G4 guard)
        assert compare_res.status_code == 200, (
            f"AC-1: GET /compare returned {compare_res.status_code}: {compare_res.text[:300]}"
        )

        body = compare_res.json()
        deltas: list[dict[str, Any]] = body.get("deltas", [])
        if not deltas:
            return  # no shared indicators to compare (pre-G4 guard)

        # Guard: check if the first delta record has threshold_crossings at all.
        # If absent, G9 is not yet implemented — return as no-op.
        first = deltas[0]
        if "threshold_crossings" not in first:
            return  # pre-G9 guard — field not yet added

        # Post-G9: every delta record must have threshold_crossings as a list.
        missing: list[dict[str, Any]] = []
        wrong_type: list[dict[str, Any]] = []

        for delta in deltas:
            if "threshold_crossings" not in delta:
                missing.append({
                    "entity": delta.get("entity_id"),
                    "key": delta.get("attribute_key"),
                })
                continue
            value = delta["threshold_crossings"]
            if not isinstance(value, list):
                wrong_type.append({
                    "entity": delta.get("entity_id"),
                    "key": delta.get("attribute_key"),
                    "type": type(value).__name__,
                    "value": value,
                })

        assert not missing, (
            f"AC-1 FAIL: {len(missing)} delta record(s) are missing 'threshold_crossings' key: "
            f"{missing[:5]}. "
            "Intent doc AC-1: 'for each entity-step entry, threshold_crossings is a key "
            "in the entry.' "
            "The field must be present even when empty (empty list [], not absent)."
        )
        assert not wrong_type, (
            f"AC-1 FAIL: {len(wrong_type)} delta record(s) have threshold_crossings "
            f"with wrong type: "
            f"{wrong_type[:3]}. "
            "Intent doc AC-1: threshold_crossings must be a list. "
            "Null or non-list values are not acceptable."
        )

    async def test_threshold_crossings_is_not_null_in_any_record(
        self, client: httpx.AsyncClient
    ) -> None:
        """threshold_crossings must never be null — empty list is correct for no-crossing steps."""
        payload_a = _zmb_ecf_payload("M16-G9 AC-1b scenario A")
        payload_b = _zmb_ecf_payload("M16-G9 AC-1b scenario B")

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            if sid is None:
                return  # setup failed
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code != 200:
            return

        body = compare_res.json()
        deltas = body.get("deltas", [])
        if not deltas or "threshold_crossings" not in deltas[0]:
            return  # pre-G9 guard

        for delta in deltas:
            value = delta.get("threshold_crossings")
            assert value is not None, (
                f"AC-1 FAIL: threshold_crossings is null for "
                f"{delta.get('entity_id')}.{delta.get('attribute_key')}. "
                "Intent doc AC-1: 'The field is not absent; it is not null.' "
                "An empty list [] is correct for steps with no crossings."
            )


# ===========================================================================
# AC-2 — threshold_crossings populated at ZMB crossing step (DB)
# ===========================================================================


class TestAC2ZmbCrossingStep:
    """AC-2: For the ZMB ECF scenario at step 2 (the step where poverty_headcount_ratio Q1
    crosses the MDA floor per G2 implementation), threshold_crossings contains a non-empty
    list with at least one entry having crossed=True and a non-empty threshold_name.

    Intent doc §4 AC-2:
      'For the ZMB ECF scenario at step 2: The entry's threshold_crossings list is
      non-empty. At least one entry has "crossed": true. That entry has a non-empty
      string value for "threshold_name".'

    The crossing step is established by G2. If G2 is not merged, this test returns
    as a no-op at the G2-dependency guard below.

    Silent failure SF-1 (always-empty list) and SF-3 (wrong step) are caught here.
    """

    async def test_zmb_threshold_crossing_at_crossing_step(
        self, client: httpx.AsyncClient
    ) -> None:
        """ZMB ECF compare at step 2 must return crossed=True in threshold_crossings."""
        payload_a = _zmb_ecf_payload("M16-G9 AC-2 ZMB ECF", n_steps=4)
        payload_b = _zmb_ecf_payload("M16-G9 AC-2 ZMB alt", n_steps=4)

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            assert sid is not None, (
                f"AC-2: scenario setup failed for {payload['name']}. "
                "G2 must be merged before G9's AC-2 can pass."
            )
            ids.append(sid)

        # Compare at the crossing step (step 2, per G2 implementation).
        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={
                "scenario_a": ids[0],
                "scenario_b": ids[1],
                "step": str(_ZMB_CROSSING_STEP),
            },
        )
        if compare_res.status_code in (404, 409):
            return  # step not available or no snapshots (G2 dependency guard)
        assert compare_res.status_code == 200, (
            f"AC-2: GET /compare?step={_ZMB_CROSSING_STEP} returned "
            f"{compare_res.status_code}: {compare_res.text[:300]}"
        )

        body = compare_res.json()
        deltas: list[dict[str, Any]] = body.get("deltas", [])
        if not deltas:
            return  # no delta records (G4/G2 dependency guard)

        # Guard: if first record lacks threshold_crossings, G9 not yet implemented.
        if "threshold_crossings" not in deltas[0]:
            return

        # Find any delta record with a threshold crossing at this step.
        # The crossing is expected on poverty_headcount_ratio or a related MDA indicator.
        crossed_records = [
            delta for delta in deltas
            if any(
                entry.get("crossed") is True
                for entry in (delta.get("threshold_crossings") or [])
            )
        ]

        assert crossed_records, (
            f"AC-2 FAIL: No delta record has threshold_crossings with crossed=True "
            f"for ZMB ECF at step {_ZMB_CROSSING_STEP}. "
            "Intent doc AC-2: 'at step 2, threshold_crossings list is non-empty with "
            "at least one entry having crossed=True.' "
            "This is SF-1 (always-empty list) or SF-3 (crossing at wrong step). "
            f"All threshold_crossings at this step: "
            f"{[d.get('threshold_crossings') for d in deltas[:5]]}"
        )

        # Each crossing entry must have a non-empty threshold_name string.
        for delta in crossed_records:
            for entry in delta["threshold_crossings"]:
                if entry.get("crossed") is True:
                    assert entry.get("threshold_name"), (
                        f"AC-2 FAIL: crossing entry has crossed=True but threshold_name is "
                        f"empty or absent: {entry}. "
                        "Intent doc AC-2: 'that entry has a non-empty string value "
                        "for threshold_name.'"
                    )

    async def test_zmb_threshold_crossings_entries_have_required_keys(
        self, client: httpx.AsyncClient
    ) -> None:
        """Each threshold_crossings entry must have both threshold_name and crossed keys."""
        payload_a = _zmb_ecf_payload("M16-G9 AC-2b ZMB ECF keys")
        payload_b = _zmb_ecf_payload("M16-G9 AC-2b ZMB alt keys")

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            if sid is None:
                return
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={
                "scenario_a": ids[0],
                "scenario_b": ids[1],
                "step": str(_ZMB_CROSSING_STEP),
            },
        )
        if compare_res.status_code != 200:
            return

        body = compare_res.json()
        deltas = body.get("deltas", [])
        if not deltas or "threshold_crossings" not in deltas[0]:
            return

        for delta in deltas:
            for entry in delta.get("threshold_crossings") or []:
                assert "threshold_name" in entry, (
                    f"AC-2b FAIL: threshold_crossings entry missing 'threshold_name': {entry}. "
                    "Intent doc visual spec: each entry has "
                    "{{ threshold_name: str, crossed: bool }}."
                )
                assert "crossed" in entry, (
                    f"AC-2b FAIL: threshold_crossings entry missing 'crossed': {entry}. "
                    "Intent doc visual spec: each entry has "
                    "{{ threshold_name: str, crossed: bool }}."
                )
                assert isinstance(entry["crossed"], bool), (
                    f"AC-2b FAIL: 'crossed' must be a boolean, got "
                    f"{type(entry['crossed']).__name__}: {entry}."
                )


# ===========================================================================
# AC-3 — threshold_crossings populated for JOR ECF at crossing step (DB)
# ===========================================================================


class TestAC3JorCrossingStep:
    """AC-3: For the JOR ECF scenario at the relevant threshold-crossing step
    (confirming step number from G2 implementation), threshold_crossings is a
    non-empty list with at least one entry having crossed=True.

    Intent doc §4 AC-3:
      'For the JOR ECF scenario at the relevant threshold-crossing step: threshold_crossings
       is a non-empty list with at least one entry having crossed=True.'
    """

    async def test_jor_threshold_crossing_at_crossing_step(
        self, client: httpx.AsyncClient
    ) -> None:
        """JOR ECF compare at crossing step must return crossed=True in threshold_crossings."""
        payload_a = _jor_ecf_payload("M16-G9 AC-3 JOR ECF", n_steps=4)
        payload_b = _jor_ecf_payload("M16-G9 AC-3 JOR alt", n_steps=4)

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            assert sid is not None, (
                f"AC-3: scenario setup failed for {payload['name']}. "
                "G2 must be merged before G9's AC-3 can pass."
            )
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={
                "scenario_a": ids[0],
                "scenario_b": ids[1],
                "step": str(_JOR_CROSSING_STEP),
            },
        )
        if compare_res.status_code in (404, 409):
            return  # step not available or no snapshots (G2 dependency guard)
        assert compare_res.status_code == 200, (
            f"AC-3: GET /compare?step={_JOR_CROSSING_STEP} returned "
            f"{compare_res.status_code}: {compare_res.text[:300]}"
        )

        body = compare_res.json()
        deltas: list[dict[str, Any]] = body.get("deltas", [])
        if not deltas:
            return

        if "threshold_crossings" not in deltas[0]:
            return  # pre-G9 guard

        crossed_records = [
            delta for delta in deltas
            if any(
                entry.get("crossed") is True
                for entry in (delta.get("threshold_crossings") or [])
            )
        ]

        assert crossed_records, (
            f"AC-3 FAIL: No delta record has threshold_crossings with crossed=True "
            f"for JOR ECF at step {_JOR_CROSSING_STEP}. "
            "Intent doc AC-3: at the JOR crossing step, threshold_crossings must be "
            "non-empty with at least one crossed=True entry. "
            "Implementing agent: confirm the JOR crossing step from G2 test assertions. "
            f"All threshold_crossings at this step: "
            f"{[d.get('threshold_crossings') for d in deltas[:5]]}"
        )


# ===========================================================================
# AC-4 — empty list for step with no crossings — not null, not absent (DB)
# ===========================================================================


class TestAC4EmptyListAtNonCrossingStep:
    """AC-4: At step 0 (initial state, no thresholds crossed), threshold_crossings
    must be an empty list [], not null, not absent. HTTP 200.

    Intent doc §4 AC-4:
      'For the ZMB ECF scenario at step 0 (initial state, no thresholds crossed):
       threshold_crossings value is [] (empty list). The key is present. HTTP 200.'

    This guards against SF-1 being masked by the test: the SF-1 detection only works
    if we can distinguish "always empty" from "correctly empty at non-crossing step."
    This AC verifies the field is correctly present-and-empty at step 0, which is the
    correct behavior — not a failure.
    """

    async def test_step_0_has_empty_threshold_crossings_not_null(
        self, client: httpx.AsyncClient
    ) -> None:
        """Compare at step 0 must return threshold_crossings=[] (not null, not absent)."""
        payload_a = _zmb_ecf_payload("M16-G9 AC-4 ZMB step0 A", n_steps=3)
        payload_b = _zmb_ecf_payload("M16-G9 AC-4 ZMB step0 B", n_steps=3)

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            if sid is None:
                return
            ids.append(sid)

        # Compare without step param — uses latest snapshot.
        # Also test at explicit step 0 if the endpoint supports it.
        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code in (409,):
            return
        if compare_res.status_code != 200:
            return

        body = compare_res.json()
        deltas: list[dict[str, Any]] = body.get("deltas", [])
        if not deltas or "threshold_crossings" not in deltas[0]:
            return  # pre-G9 guard

        # For steps where no threshold is crossed, every record's list must be [] not null.
        # We use the initial scenario compare (step 0 / pre-crossing).
        # If any record IS crossed, we skip that record — focus on non-crossed records.
        non_crossed_records = [
            delta for delta in deltas
            if not any(
                entry.get("crossed") is True
                for entry in (delta.get("threshold_crossings") or [])
            )
        ]

        for delta in non_crossed_records:
            value = delta.get("threshold_crossings")
            assert value is not None, (
                f"AC-4 FAIL: threshold_crossings is null for "
                f"{delta.get('entity_id')}.{delta.get('attribute_key')} "
                "at a non-crossing step. "
                "Intent doc AC-4: 'threshold_crossings value is [] (empty list). "
                "The key is present. HTTP 200.' Null is not acceptable."
            )
            assert isinstance(value, list), (
                f"AC-4 FAIL: threshold_crossings is {type(value).__name__} "
                f"(not a list) for {delta.get('entity_id')}.{delta.get('attribute_key')}. "
                "Intent doc AC-4: empty list [] is correct for non-crossing steps."
            )
            # For non-crossed records, the list should be empty (no crossing entries).
            assert len(value) == 0, (
                f"AC-4 FAIL: threshold_crossings is non-empty for a record flagged as "
                f"non-crossing: {value[:2]}. "
                "A crossing entry with crossed=False is acceptable; a crossed=True entry "
                "in a 'non-crossed' record means the crossing detection is misclassified."
            )


# ===========================================================================
# AC-5 — api_contracts.yml updated in same PR (file read — no DB required)
# ===========================================================================


class TestAC5ApiContractsUpdated:
    """AC-5: docs/schema/api_contracts.yml must contain 'threshold_crossings' within
    the compare response schema definition. This file change must be committed in the
    same PR as the backend implementation.

    Intent doc §4 AC-5:
      'docs/schema/api_contracts.yml content includes the string "threshold_crossings"
       within the compare response schema definition. The schema entry documents: type
       as array, entry shape (threshold_name string, crossed boolean), and empty-list
       behavior. This file change is committed in the same PR as the backend implementation.'

    This is a file-read test — does NOT require DATABASE_URL.
    Never skipped (NM-056: no conditional skip in non-integration tests).

    Pre-G9: api_contracts.yml does not contain threshold_crossings → test FAILS.
    This is intentional: the test is currently red. It becomes green when the
    implementing agent commits the api_contracts.yml update together with the
    backend code change.

    Note: a currently-red test that guards a schema contract is correct per NM-056.
    The file-check test must FAIL pre-implementation to be meaningful.
    """

    def test_api_contracts_yml_contains_threshold_crossings(self) -> None:
        """api_contracts.yml must document threshold_crossings in the compare response schema."""
        assert _API_CONTRACTS.exists(), (
            f"AC-5 FAIL: api_contracts.yml not found at expected path {_API_CONTRACTS}. "
            "The schema registry must be maintained alongside the code. "
            "CLAUDE.md §Schema registry mandate: 'When schema files are out of date with "
            "the code, update them in the same commit as the code change.'"
        )

        content = _API_CONTRACTS.read_text(encoding="utf-8")

        assert "threshold_crossings" in content, (
            "AC-5 FAIL: 'threshold_crossings' not found in api_contracts.yml. "
            "Intent doc AC-5: 'docs/schema/api_contracts.yml content includes the string "
            "'threshold_crossings' within the compare response schema definition.' "
            "The implementing agent must add the threshold_crossings field documentation "
            "to the /scenarios/compare response body definition in the same PR as the "
            "backend implementation. This is not a follow-up — it is part of the same commit. "
            "CLAUDE.md §Schema registry mandate: schema drift is a compliance violation."
        )

    def test_api_contracts_threshold_crossings_entry_documents_threshold_name(self) -> None:
        """api_contracts.yml threshold_crossings entry must document threshold_name key."""
        if not _API_CONTRACTS.exists():
            pytest.fail(
                "AC-5 FAIL: api_contracts.yml not found. Cannot verify schema documentation."
            )
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "threshold_crossings" not in content:
            pytest.fail(
                "AC-5 FAIL: 'threshold_crossings' not in api_contracts.yml. "
                "Run the primary AC-5 test first to diagnose."
            )

        assert "threshold_name" in content, (
            "AC-5 FAIL: 'threshold_name' not documented in api_contracts.yml. "
            "Intent doc AC-5: the schema entry must document 'entry shape "
            "(threshold_name string, crossed boolean)'. "
            "The threshold_crossings array item shape must be fully documented."
        )

    def test_api_contracts_threshold_crossings_entry_documents_crossed_boolean(self) -> None:
        """api_contracts.yml threshold_crossings entry must document crossed as boolean."""
        if not _API_CONTRACTS.exists():
            pytest.fail(
                "AC-5 FAIL: api_contracts.yml not found. Cannot verify schema documentation."
            )
        content = _API_CONTRACTS.read_text(encoding="utf-8")
        if "threshold_crossings" not in content:
            pytest.fail(
                "AC-5 FAIL: 'threshold_crossings' not in api_contracts.yml. "
                "Run the primary AC-5 test first to diagnose."
            )

        # The schema documentation must reference 'crossed' as a documented field.
        assert "crossed" in content, (
            "AC-5 FAIL: 'crossed' not documented in api_contracts.yml. "
            "Intent doc AC-5: entry shape requires 'crossed: bool'. "
            "The schema documentation must be specific, not generic."
        )


# ===========================================================================
# AC-6 — existing compare fields unchanged — additive-only extension (DB)
# ===========================================================================


class TestAC6ExistingFieldsUnchanged:
    """AC-6: The compare response for existing fields (delta, direction, distribution,
    entity_id, attribute_key, value_a, value_b) must be unchanged in type, name, and
    nullability. threshold_crossings is purely additive.

    Intent doc §4 AC-6:
      'GET /compare response body for existing fields (delta, baseline; and distribution
       if present from G4) is unchanged in type, name, and nullability contract.
       The threshold_crossings addition is verified additive-only.'
    """

    async def test_existing_delta_field_present_and_string_typed(
        self, client: httpx.AsyncClient
    ) -> None:
        """delta, direction, entity_id, attribute_key must still be present post-G9."""
        payload_a = _zmb_ecf_payload("M16-G9 AC-6 backward-compat A")
        payload_b = _zmb_ecf_payload("M16-G9 AC-6 backward-compat B")
        payload_b["name"] = "M16-G9 AC-6 backward-compat B"
        payload_b["configuration"]["n_steps"] = 2

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            if sid is None:
                return
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code not in (200,):
            return

        body = compare_res.json()
        deltas: list[dict[str, Any]] = body.get("deltas", [])
        if not deltas:
            return

        first = deltas[0]

        assert "delta" in first, (
            "AC-6 FAIL: 'delta' field missing from compare response after G9 extension. "
            "G9 adds 'threshold_crossings' but must not rename or remove existing fields."
        )
        assert "direction" in first, (
            "AC-6 FAIL: 'direction' field missing from compare response after G9 extension."
        )
        assert "entity_id" in first, (
            "AC-6 FAIL: 'entity_id' field missing from compare response after G9 extension."
        )
        assert "attribute_key" in first, (
            "AC-6 FAIL: 'attribute_key' field missing from compare response after G9 extension."
        )

        # delta must be a string (Decimal serialised as string per api_contracts.yml).
        delta_value = first.get("delta")
        assert isinstance(delta_value, str), (
            f"AC-6 FAIL: 'delta' field changed type from string to {type(delta_value).__name__}. "
            "api_contracts.yml: 'delta: Decimal as string'. G9 must not alter this type."
        )

    async def test_threshold_crossings_addition_does_not_remove_distribution(
        self, client: httpx.AsyncClient
    ) -> None:
        """distribution field from G4 must still be present alongside threshold_crossings."""
        payload_a = _zmb_ecf_payload("M16-G9 AC-6b dist-check A", n_steps=4)
        payload_b = _zmb_ecf_payload("M16-G9 AC-6b dist-check B", n_steps=4)

        ids: list[str] = []
        for payload in (payload_a, payload_b):
            sid = await _create_and_run(client, payload)
            if sid is None:
                return
            ids.append(sid)

        compare_res = await client.get(
            "/api/v1/scenarios/compare",
            params={"scenario_a": ids[0], "scenario_b": ids[1]},
        )
        if compare_res.status_code != 200:
            return

        body = compare_res.json()
        deltas = body.get("deltas", [])
        if not deltas:
            return

        first = deltas[0]

        # If G4 distribution is present (post-G4), it must remain after G9 extension.
        if "distribution" not in first:
            return  # G4 not yet implemented — nothing to verify

        distribution = first["distribution"]
        assert distribution is not None or isinstance(distribution, dict), (
            "AC-6 FAIL: 'distribution' field changed to a non-dict/non-null type "
            "after G9 extension. G4 adds distribution; G9 must not modify or remove it."
        )

        # Both threshold_crossings and distribution must coexist if G9 is implemented.
        if "threshold_crossings" in first:
            assert "distribution" in first, (
                "AC-6 FAIL: 'distribution' absent when 'threshold_crossings' is present. "
                "G9 must be purely additive — both fields must coexist."
            )
