# Community Report Export Architecture Spec — US-043

**Authors:** Community Resilience, Customer Agent, UX Designer
**Date:** 2026-06-03
**Authority:** ARCH-REVIEW-006 AR-006-B-008, AR-006-B-009, AR-006-B-010
**EL sign-off:** Accepted 2026-06-03
**Closes:** Issue #608

---

## Context

US-043 specifies a community-oriented export format: an A4 two-column, screen-readable
PDF output with plain-language epistemic disclosure (see
`docs/standards/epistemic-disclosure-vocabulary.md`). The architectural path for
generating this output was undecided. This document records the EL decision and the
format adapter architecture requirement.

---

## 1. EL Decision — PDF Rendering Path (AR-006-B-008)

**Decision: Path B — Structured export (HTML → user conversion).** Accepted 2026-06-03.

WorldSim generates a structured HTML document. The user renders it using local tooling
(browser print-to-PDF, WeasyPrint installed locally, or equivalent). WorldSim does not
generate the PDF file directly.

**Rationale:**

Path A (in-app PDF generation via WeasyPrint or Puppeteer) was rejected on two grounds:

1. **Equitable Build Process (CLAUDE.md §Equitable Build Process, absolute):** Adding
   a PDF rendering runtime dependency (WeasyPrint, Puppeteer, wkhtmltopdf) to the
   application stack would require contributors on modest hardware to install and
   configure that dependency to run the full test suite. The CI pipeline targets the
   GitHub Actions free-tier runner (2-core, 7GB RAM, Ubuntu). PDF rendering libraries
   with headless browser dependencies (Puppeteer) are expensive in both RAM and CI
   minutes. The test suite must not require proprietary software or heavy dependencies
   to pass.

2. **Infrastructure burden:** In-app PDF generation introduces a new test surface,
   runtime failure modes (memory exhaustion on large reports, font rendering differences
   across environments), and a new CI dependency. These costs are disproportionate to
   the benefit when the user can render the HTML locally with standard tooling.

**Path B limitation acknowledged:** For community advocacy organizations with limited
technical capacity, HTML-to-PDF conversion may not be trivial. To mitigate:

- The exported HTML must be self-contained (all CSS inlined, no external dependencies)
- The HTML must render correctly in print mode (browser print dialog → Save as PDF)
- The export screen must display one-sentence instructions: "Open in a browser and
  use Print → Save as PDF to produce an A4 document."

This mitigation makes browser print-to-PDF the primary conversion path — available
on any device with a modern browser, requiring no additional software installation.

**Community Resilience and Customer Agent consultation:** Recorded in ARCH-REVIEW-006
§Story 3 §Challenge from Community Resilience and §Challenge from Customer Agent.

---

## 2. Format Adapter Architecture (AR-006-B-009)

The export pipeline must be designed with **pluggable format adapters** from the initial
implementation. The A4 two-column HTML format ships in M11. Additional formats (print
PDF, screen-optimized single-column, plain Markdown) are anticipated for M12+ based on
Persona 7 (investigative journalists) and Persona 4V (ministry officials) requirements.

### 2.1 Adapter Interface

```python
from abc import ABC, abstractmethod
from typing import Any

class ReportFormatAdapter(ABC):
    """
    # INTENT: Abstract base for community report format adapters.
    # PRECONDITIONS: report_data must be a validated ReportPayload dict.
    # POSTCONDITIONS: Returns rendered output as bytes or str.
    # ERROR CASES: Raises FormatRenderError if rendering fails.
    """

    @abstractmethod
    def render(self, report_data: dict[str, Any]) -> bytes | str:
        ...

    @property
    @abstractmethod
    def content_type(self) -> str:
        ...

    @property
    @abstractmethod
    def file_extension(self) -> str:
        ...
```

### 2.2 M11 Adapter: A4 Two-Column HTML

The M11 implementation ships one adapter: `A4TwoColumnHTMLAdapter`. It renders the
community report as a self-contained HTML file with:
- Inline CSS (print stylesheet included for A4 page breaks)
- No external fonts, scripts, or images
- Inline epistemic disclosure per `docs/standards/epistemic-disclosure-vocabulary.md`
- `@media print` rules targeting A4 page size

### 2.3 Export API Endpoint

`GET /api/v1/scenarios/{scenario_id}/report?format=a4-html`

The `format` query parameter maps to an adapter key. The pipeline selects the adapter
and calls `adapter.render(report_data)`. Unsupported format values return HTTP 400.

---

## 3. Epistemic Disclosure Layout (AR-006-B-010)

The CM placement rule (inline qualifier — see
`docs/standards/epistemic-disclosure-vocabulary.md §Placement Rule`) determines the
HTML template structure:

Each indicator value is rendered as:

```html
<span class="indicator-value">68%</span>
<span class="epistemic-qualifier">
  (This is an estimated figure — independent verification recommended)
</span>
```

The `.epistemic-qualifier` class renders as an inline parenthetical in the default
stylesheet. The template does not require a separate footnote section or sidebar.

---

## 4. Cross-References

- `docs/standards/epistemic-disclosure-vocabulary.md` — canonical disclosure vocabulary
- `docs/architecture/reviews/ARCH-REVIEW-006-milestone10.md §Story 3` — originating review
- `docs/CONTRIBUTING.md §Equitable Build Process` — equitable build requirements
