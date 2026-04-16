"""
WorldSim Compliance Scan Script

Manual equivalent of the CI compliance-scan job. Used for milestone-exit reviews,
quarterly governance audits, and ad hoc scans triggered by significant architecture
changes.

Performs the same machine-detectable checks as the CI job plus additional pattern
analysis suitable for milestone-level review. Produces structured output showing
files scanned, checks run, violations found by category, warnings emitted, and a
summary line.

Usage:
    python scripts/compliance_scan.py --scope full
    python scripts/compliance_scan.py --scope simulation-engine
    python scripts/compliance_scan.py --scope tests

Exit codes:
    0 — Clean or warnings only (COMPLIANCE-WARN entries emitted but no violations)
    1 — Violations found (hard failures that CI would block on)

Scope definitions:
    full             — All Python files under backend/app/ and backend/tests/
    simulation-engine — Files under backend/app/simulation/ only
    tests            — Files under backend/tests/ only
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Scope configuration
# ---------------------------------------------------------------------------

BACKEND_ROOT = Path(__file__).parent.parent
APP_ROOT = BACKEND_ROOT / "app"
SIMULATION_ROOT = APP_ROOT / "simulation"
TESTS_ROOT = BACKEND_ROOT / "tests"

SCOPE_PATHS: dict[str, list[Path]] = {
    "full": [APP_ROOT, TESTS_ROOT],
    "simulation-engine": [SIMULATION_ROOT],
    "tests": [TESTS_ROOT],
}

# ---------------------------------------------------------------------------
# Monetary terminology — keywords that indicate a variable may carry a
# monetary or financial quantity. Float literals adjacent to these terms
# warrant review for Decimal compliance.
# ---------------------------------------------------------------------------

MONETARY_KEYWORDS = re.compile(
    r"\b(debt|gdp|revenue|expenditure|reserve|currency|price|cost|rate|"
    r"payment|balance|deficit|surplus|export|import|inflation|interest|"
    r"principal|loan|bond|yield|spread|budget|fiscal|monetary|tariff)\b",
    re.IGNORECASE,
)

FLOAT_LITERAL = re.compile(r"\b\d+\.\d+\b")

# Legacy typing imports that should be replaced with Python 3.10+ builtins
LEGACY_TYPING_PATTERN = re.compile(
    r"from\s+typing\s+import\s+[^\n]*(Dict|List|Optional|Tuple|Set)"
)

# ---------------------------------------------------------------------------
# Result collection
# ---------------------------------------------------------------------------

class ScanResult:
    """Accumulates findings across all checks."""

    def __init__(self) -> None:
        self.files_scanned: list[str] = []
        self.checks_run: list[str] = []
        self.violations: list[str] = []
        self.warnings: list[str] = []

    def add_violation(self, check: str, location: str, message: str) -> None:
        self.violations.append(f"  VIOLATION [{check}] {location}: {message}")

    def add_warning(self, check: str, location: str, message: str) -> None:
        self.warnings.append(f"  COMPLIANCE-WARN [{check}] {location}: {message}")

    def record_check(self, check_name: str) -> None:
        self.checks_run.append(check_name)

    def record_files(self, paths: list[Path]) -> None:
        for path in paths:
            self.files_scanned.append(str(path.relative_to(BACKEND_ROOT)))

    def print_report(self) -> None:
        print("\n" + "=" * 70)
        print("WORLDSIM COMPLIANCE SCAN REPORT")
        print("=" * 70)

        print(f"\nFiles scanned: {len(self.files_scanned)}")
        for f in sorted(self.files_scanned):
            print(f"  {f}")

        print(f"\nChecks run ({len(self.checks_run)}):")
        for c in self.checks_run:
            print(f"  {c}")

        if self.violations:
            print(f"\nViolations ({len(self.violations)}):")
            for v in self.violations:
                print(v)
        else:
            print("\nViolations: none")

        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}) — require human review:")
            for w in self.warnings:
                print(w)
        else:
            print("\nWarnings: none")

        print("\n" + "=" * 70)
        if self.violations:
            print(f"SUMMARY: VIOLATIONS-FOUND — {len(self.violations)} violation(s), "
                  f"{len(self.warnings)} warning(s)")
        else:
            print(f"SUMMARY: CLEAN — 0 violations, {len(self.warnings)} warning(s)")
        print("=" * 70 + "\n")

    @property
    def has_violations(self) -> bool:
        return len(self.violations) > 0


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_bare_except(scope_paths: list[Path], result: ScanResult) -> None:
    """Check for bare except clauses (E722) using ruff."""
    result.record_check("bare-except (E722)")
    cmd = ["ruff", "check", "--select", "E722", "--output-format", "text"]
    cmd += [str(p) for p in scope_paths]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=BACKEND_ROOT)  # noqa: S603
    if proc.returncode != 0:
        for line in proc.stdout.strip().splitlines():
            if line.strip():
                result.add_violation("E722", line, "bare except clause")


def check_ambiguous_variable_names(scope_paths: list[Path], result: ScanResult) -> None:
    """Check for ambiguous variable names (E741) using ruff."""
    result.record_check("ambiguous-variable-names (E741)")
    cmd = ["ruff", "check", "--select", "E741", "--output-format", "text"]
    cmd += [str(p) for p in scope_paths]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=BACKEND_ROOT)  # noqa: S603
    if proc.returncode != 0:
        for line in proc.stdout.strip().splitlines():
            if line.strip():
                result.add_violation("E741", line, "ambiguous variable name (l, O, or I)")


def check_legacy_typing_imports(scope_paths: list[Path], result: ScanResult) -> None:
    """Check for legacy typing imports (Dict, List, Optional, Tuple, Set)."""
    result.record_check("legacy-typing-imports")
    python_files = _collect_python_files(scope_paths)
    result.record_files(python_files)
    for path in python_files:
        content = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(content.splitlines(), start=1):
            if LEGACY_TYPING_PATTERN.search(line):
                result.add_violation(
                    "legacy-typing",
                    f"{path.relative_to(BACKEND_ROOT)}:{lineno}",
                    f"legacy typing import — use Python 3.10+ built-ins: {line.strip()}",
                )


def check_monetary_float_literals(scope_paths: list[Path], result: ScanResult) -> None:
    """Warn on float literals adjacent to monetary terminology.

    Emits COMPLIANCE-WARN (not a violation) because determining whether a
    float literal is performing monetary arithmetic requires human judgment.
    A float used as a propagation weight or dimensionless ratio is correct;
    a float used as a GDP or debt value is a Decimal compliance issue.
    """
    result.record_check("monetary-float-literals (warn-only)")
    python_files = _collect_python_files(scope_paths)
    for path in python_files:
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        for lineno, line in enumerate(lines, start=1):
            if not FLOAT_LITERAL.search(line):
                continue
            # Check this line and the two surrounding lines for monetary keywords
            context_start = max(0, lineno - 2)
            context_end = min(len(lines), lineno + 1)
            context = " ".join(lines[context_start:context_end])
            if MONETARY_KEYWORDS.search(context):
                result.add_warning(
                    "monetary-float",
                    f"{path.relative_to(BACKEND_ROOT)}:{lineno}",
                    f"float literal near monetary keyword — verify Decimal compliance: "
                    f"{line.strip()[:80]}",
                )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _collect_python_files(scope_paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in scope_paths:
        if path.is_file() and path.suffix == ".py":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.py")))
    return files


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="WorldSim compliance scan — run before milestone exit or quarterly audit.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--scope",
        choices=["full", "simulation-engine", "tests"],
        default="full",
        help="Scope of files to scan (default: full)",
    )
    args = parser.parse_args()

    scope_paths = SCOPE_PATHS[args.scope]
    existing_paths = [p for p in scope_paths if p.exists()]

    if not existing_paths:
        print(f"No paths found for scope '{args.scope}'. Paths checked:")
        for p in scope_paths:
            print(f"  {p}")
        sys.exit(0)

    print(f"WorldSim compliance scan — scope: {args.scope}")
    print(f"Backend root: {BACKEND_ROOT}")
    print(f"Scanning: {[str(p.relative_to(BACKEND_ROOT)) for p in existing_paths]}")

    result = ScanResult()

    check_bare_except(existing_paths, result)
    check_ambiguous_variable_names(existing_paths, result)
    check_legacy_typing_imports(existing_paths, result)

    # Monetary float check only applies to app/simulation — not tests
    if args.scope in ("full", "simulation-engine"):
        simulation_paths = [p for p in existing_paths if "simulation" in str(p)]
        if simulation_paths:
            check_monetary_float_literals(simulation_paths, result)

    result.print_report()
    sys.exit(1 if result.has_violations else 0)


if __name__ == "__main__":
    main()
