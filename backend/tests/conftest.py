"""Root conftest — session-wide guards applied before any test is collected.

Python version guard (Issue #131):
  The project requires Python 3.11+ because datetime.UTC was introduced in
  3.11 and ruff's UP017 rule (enabled via target-version = "py312") rewrites
  timezone.utc to datetime.UTC. Running pytest under Python 3.10 or earlier
  produces ImportError at collection time. This guard surfaces a clear error
  immediately rather than a confusing import traceback.
"""
from __future__ import annotations

import sys


def pytest_configure(config: object) -> None:  # noqa: ARG001
    if sys.version_info < (3, 11):  # noqa: UP036 — intentional guard for misconfigured envs
        import pytest
        pytest.exit(
            f"\n\nPython 3.11+ is required — current interpreter is {sys.version}.\n"
            "The project uses datetime.UTC (3.11+) and targets Python 3.12.\n"
            "See docs/CONTRIBUTING.md §'Step 2: Python Environment' for setup instructions.\n"
            "Quick fix: cd backend && python3.12 -m venv .venv && source .venv/bin/activate\n",
            returncode=3,
        )
