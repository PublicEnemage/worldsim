#!/usr/bin/env python3
"""
Intent block spec-to-test gap check — Issue #286.

Parses PRECONDITIONS and ERROR CASES from intent blocks in app/ and checks
for corresponding tests in tests/. A 'corresponding test' is a test function
whose name or docstring references the function being claimed about.

Usage (from backend/ directory):
    python scripts/intent_gap_check.py [--json-out PATH] [--strict]

Exits 0 in warning-only mode (M8/M11 default).
Use --strict to promote gaps to a failure gate (M9 threshold enforcement).

Output:
  stdout — human-readable summary + per-module breakdown
  JSON sidecar — machine-readable artifact for dashboard integration (#259)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative to backend/ working directory)
# ---------------------------------------------------------------------------

APP_DIR = Path("app")
TESTS_DIR = Path("tests")
DEFAULT_JSON_OUT = Path("scripts") / "intent_gap_check_results.json"

# ---------------------------------------------------------------------------
# Stop words excluded from keyword extraction
# ---------------------------------------------------------------------------

_STOP = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "ought", "used", "to", "of", "in", "on", "at", "by", "for", "with",
    "from", "into", "through", "during", "before", "after", "above",
    "below", "between", "out", "off", "over", "under", "again", "further",
    "then", "once", "and", "but", "or", "nor", "so", "yet", "both",
    "either", "neither", "not", "no", "only", "same", "than", "too",
    "very", "just", "because", "as", "if", "when", "where", "how",
    "all", "each", "every", "few", "more", "most", "other", "some",
    "such", "what", "which", "who", "this", "that", "these", "those",
    "it", "its", "itself", "one", "two", "any", "also",
})

# Minimum number of shared keywords for a test to count as covering a claim.
_MIN_KEYWORD_OVERLAP = 2


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Claim:
    module: str       # relative path from app/ — e.g. "simulation/engine/propagation.py"
    function: str     # function name that the intent block belongs to
    field: str        # "PRECONDITIONS" or "ERROR CASES"
    text: str         # full claim text (multi-line joined)
    covered: bool = False
    matched_by: str = ""  # test function name that covers it, if any


@dataclass
class ModuleResult:
    module: str
    claims: list[Claim] = field(default_factory=list)

    @property
    def gap_count(self) -> int:
        return sum(1 for c in self.claims if not c.covered)

    @property
    def covered_count(self) -> int:
        return sum(1 for c in self.claims if c.covered)

    @property
    def total(self) -> int:
        return len(self.claims)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

_FIELD_START_RE = re.compile(r"^# (PRECONDITIONS|ERROR CASES): (.*)$")
_CONTINUATION_RE = re.compile(r"^#\s{2,}(.+)$")
_DEF_RE = re.compile(r"^(?:async\s+)?def\s+(\w+)\s*\(")
_INTENT_FIELD_ANY = re.compile(
    r"^# (?:INTENT|PRECONDITIONS|POSTCONDITIONS|ERROR CASES|KNOWN LIMITATIONS):"
)


def _extract_keywords(text: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text)
    return {t.lower() for t in tokens if t.lower() not in _STOP and len(t) > 2}


def parse_intent_claims(path: Path) -> list[tuple[str, str, str]]:
    """Return list of (function_name, field_type, claim_text) from a source file.

    Parses intent blocks in the format defined in CODING_STANDARDS.md §Intent Blocks.
    Only PRECONDITIONS and ERROR CASES claims are returned (INTENT, POSTCONDITIONS,
    and KNOWN LIMITATIONS are informational and not matched to tests).
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    results: list[tuple[str, str, str]] = []

    # Buffer for the current intent block being parsed
    current_field: str | None = None
    current_text_parts: list[str] = []
    pending_claims: list[tuple[str, str]] = []  # (field, text) awaiting function name
    in_intent_block = False

    for line in lines:
        # --- Check for intent block field start ---
        m = _FIELD_START_RE.match(line)
        if m:
            # Flush previous field
            if current_field and current_text_parts:
                pending_claims.append((current_field, " ".join(current_text_parts)))
            current_field = m.group(1)
            current_text_parts = [m.group(2).strip()] if m.group(2).strip() else []
            in_intent_block = True
            continue

        # --- Continuation line ---
        if in_intent_block and current_field:
            cont = _CONTINUATION_RE.match(line)
            if cont:
                current_text_parts.append(cont.group(1).strip())
                continue
            # Any other intent field ends the current one
            if _INTENT_FIELD_ANY.match(line):
                if current_field and current_text_parts:
                    pending_claims.append((current_field, " ".join(current_text_parts)))
                current_field = None
                current_text_parts = []
                continue

        # --- def statement closes the intent block ---
        def_match = _DEF_RE.match(line)
        if def_match and in_intent_block:
            # Flush final field
            if current_field and current_text_parts:
                pending_claims.append((current_field, " ".join(current_text_parts)))
            func_name = def_match.group(1)
            for fld, txt in pending_claims:
                if fld in ("PRECONDITIONS", "ERROR CASES"):
                    results.append((func_name, fld, txt))
            # Reset
            current_field = None
            current_text_parts = []
            pending_claims = []
            in_intent_block = False
            continue

        # --- Non-comment, non-def line resets block if we left it ---
        if in_intent_block and not line.startswith("#") and line.strip():
            # Flush and discard (no def found — malformed block)
            current_field = None
            current_text_parts = []
            pending_claims = []
            in_intent_block = False

    return results


# ---------------------------------------------------------------------------
# Test coverage matching
# ---------------------------------------------------------------------------


def _gather_test_corpus(tests_dir: Path) -> dict[str, str]:
    """Return mapping of test_function_name → (name + docstring) text.

    Handles both `def test_*` and `async def test_*` function definitions.
    Extracts the first string literal after the `:` as the docstring.
    """
    corpus: dict[str, str] = {}
    # Matches: optional "async ", "def ", function name starting with "test_"
    def_re = re.compile(r"^(?:async\s+)?def\s+(test_\w+)")
    # Matches a docstring as the first non-empty line after def
    doc_re = re.compile(r'^\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\')', re.DOTALL)

    for test_file in tests_dir.rglob("test_*.py"):
        try:
            lines = test_file.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue

        i = 0
        while i < len(lines):
            m = def_re.match(lines[i])
            if m:
                name = m.group(1)
                # Scan ahead for docstring (within next 5 lines)
                doc = ""
                rest = "\n".join(lines[i + 1 : i + 6])
                dm = doc_re.search(rest)
                if dm:
                    doc = (dm.group(1) or dm.group(2) or "").strip()
                corpus[name] = f"{name} {doc}".lower()
            i += 1

    return corpus


def check_coverage(
    func_name: str,
    claim_text: str,
    corpus: dict[str, str],
) -> tuple[bool, str]:
    """Return (covered, matched_test_name).

    A claim is covered when a test function's name or docstring contains
    at least MIN_KEYWORD_OVERLAP keywords drawn from the claim text and/or
    the function name. Function name does not need to appear verbatim
    (private helpers like _accumulate are rarely named in test function names).

    Matching is per the Issue #286 spec: "a test function whose name or
    docstring references the specific precondition or error case described."
    """
    # Build combined keyword set from both the claim text and function name
    claim_keywords = _extract_keywords(claim_text)
    func_keywords = _extract_keywords(func_name)
    combined_keywords = claim_keywords | func_keywords

    if not combined_keywords:
        return False, ""

    best_name = ""
    best_overlap = 0
    for name, text in corpus.items():
        test_keywords = _extract_keywords(text)
        overlap = len(combined_keywords & test_keywords)
        if overlap > best_overlap:
            best_overlap = overlap
            best_name = name

    if best_overlap >= _MIN_KEYWORD_OVERLAP:
        return True, best_name

    return False, best_name if best_name else ""


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------


def run_check(app_dir: Path, tests_dir: Path) -> tuple[list[ModuleResult], dict]:
    """Scan app_dir for intent blocks and return (per-module results, summary dict)."""
    corpus = _gather_test_corpus(tests_dir)

    module_results: dict[str, ModuleResult] = {}

    for py_file in sorted(app_dir.rglob("*.py")):
        if py_file.name.startswith("_") and py_file.name != "__init__.py":
            continue
        rel = str(py_file.relative_to(app_dir))
        raw_claims = parse_intent_claims(py_file)
        if not raw_claims:
            continue

        mr = ModuleResult(module=rel)
        for func_name, fld, text in raw_claims:
            covered, matched = check_coverage(func_name, text, corpus)
            mr.claims.append(Claim(
                module=rel,
                function=func_name,
                field=fld,
                text=text,
                covered=covered,
                matched_by=matched,
            ))
        module_results[rel] = mr

    results = list(module_results.values())

    total_claims = sum(m.total for m in results)
    total_covered = sum(m.covered_count for m in results)
    total_gaps = sum(m.gap_count for m in results)
    coverage_rate = total_covered / total_claims if total_claims else 1.0

    summary = {
        "total_claims": total_claims,
        "covered": total_covered,
        "gaps": total_gaps,
        "coverage_rate": round(coverage_rate, 4),
        "modules": [
            {
                "module": m.module,
                "total": m.total,
                "covered": m.covered_count,
                "gaps": m.gap_count,
                "uncovered_claims": [
                    {
                        "function": c.function,
                        "field": c.field,
                        "text": c.text[:120],
                        "closest_test": c.matched_by,
                    }
                    for c in m.claims
                    if not c.covered
                ],
            }
            for m in results
        ],
    }

    return results, summary


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


def print_report(results: list[ModuleResult], summary: dict) -> None:
    total = summary["total_claims"]
    covered = summary["covered"]
    gaps = summary["gaps"]
    rate = summary["coverage_rate"]

    print("=" * 72)
    print("Intent Block Spec-to-Test Gap Check (Issue #286)")
    print("=" * 72)
    print(f"  Total claims parsed (PRECONDITIONS + ERROR CASES): {total}")
    print(f"  Claims with corresponding tests:                    {covered}")
    print(f"  Claims without corresponding tests (gaps):          {gaps}")
    print(f"  Coverage rate:                                      {rate:.1%}")
    print()

    if gaps == 0:
        print("  No gaps found.")
        return

    print("  Per-module breakdown:")
    print()
    for m in results:
        if m.gap_count == 0:
            continue
        print(f"  [{m.module}]  {m.gap_count}/{m.total} gaps")
        for c in m.claims:
            if not c.covered:
                short = c.text[:80] + ("…" if len(c.text) > 80 else "")
                print(f"    {c.function}() — {c.field}")
                print(f"      claim: {short}")
                if c.matched_by:
                    print(f"      closest: {c.matched_by} (below overlap threshold)")
        print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json-out",
        type=Path,
        default=DEFAULT_JSON_OUT,
        help="Path for JSON sidecar output (default: scripts/intent_gap_check_results.json)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any gaps exist (failure gate mode — not active in M8/M11)",
    )
    args = parser.parse_args()

    if not APP_DIR.is_dir():
        print(f"ERROR: app/ directory not found at {APP_DIR.resolve()}", file=sys.stderr)
        print("Run from the backend/ directory: python scripts/intent_gap_check.py",
              file=sys.stderr)
        return 2

    results, summary = run_check(APP_DIR, TESTS_DIR)
    print_report(results, summary)

    # Write JSON sidecar
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"  JSON sidecar written to: {args.json_out}")

    if args.strict and summary["gaps"] > 0:
        print(f"\nFAILURE: {summary['gaps']} gap(s) detected (--strict mode).",
              file=sys.stderr)
        return 1

    if summary["gaps"] > 0:
        print(f"\nWARNING: {summary['gaps']} spec-to-test gap(s) detected.")
        print("  This is a warning in M8/M11. Promote to --strict in M9.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
