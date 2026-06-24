"""VC-2 validation script — simulation timing gate.

Run on target hardware (ProBook) after docker compose stack is up:
    python tmp/vc2_test.py

Pass criterion: both 8-step and 100-step elapsed times <= 60s.
Authority: M16-G6 sprint entry §VC-2.
"""
import json
import time
import urllib.request

BASE = "http://localhost:8000/api/v1"


def create_and_run(label, config):
    body = json.dumps(
        {
            "name": label,
            "description": None,
            "configuration": config,
            "scheduled_inputs": [],
        }
    ).encode()
    req = urllib.request.Request(
        BASE + "/scenarios",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    sid = resp["scenario_id"]
    print("  scenario_id:", sid)
    run_req = urllib.request.Request(
        BASE + "/scenarios/" + sid + "/run",
        data=b"",
        method="POST",
    )
    t0 = time.time()
    urllib.request.urlopen(run_req)
    elapsed = time.time() - t0
    status = "PASS" if elapsed <= 60 else "FAIL"
    print(f"  elapsed: {elapsed:.1f}s  [{status}]")
    return elapsed


print("=== VC-2: 8-step ZMB ===")
t8 = create_and_run(
    "vc2-8step",
    {
        "entities": ["ZMB"],
        "n_steps": 8,
        "timestep_label": "annual",
        "start_date": "2022-01-01",
        "initial_attributes": {},
    },
)

print()
print("=== VC-2: 100-step ZMB ===")
t100 = create_and_run(
    "vc2-100step",
    {
        "entities": ["ZMB"],
        "n_steps": 8,
        "timestep_label": "quarterly",
        "start_date": "2000-01-01",
        "initial_attributes": {},
        "projection_steps": 100,
    },
)

print()
print("=== VC-2 Summary ===")
print(f"  8-step:   {t8:.1f}s  {'PASS' if t8 <= 60 else 'FAIL'} (limit: 60s)")
print(f"  100-step: {t100:.1f}s  {'PASS' if t100 <= 60 else 'FAIL'} (limit: 60s)")
