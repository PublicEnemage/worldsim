#!/usr/bin/env python3
"""
M11.5 Pillar 2 — Computer Use Usability Session Runner

Drives a live browser via Playwright and the Anthropic computer-use API.
The agent sees the actual rendered UI and navigates by clicking — no API
access, no screenshots handed in advance. Produces a genuine think-aloud
transcript conforming to pillar-2-methodology.md.

Usage:
    python3 scripts/run_usability_session.py <session_id> <persona_id>

Example:
    python3 scripts/run_usability_session.py 2026-06-04-persona-2-003 persona-2

Prerequisites:
    pip3 install anthropic playwright
    playwright install chromium
    ANTHROPIC_API_KEY environment variable set
    Frontend running at http://localhost:5173
    Backend running at http://localhost:8000
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import anthropic
from playwright.sync_api import Page, sync_playwright

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
BETA = "computer-use-2025-11-24"
TOOL_TYPE = "computer_20251124"
VIEWPORT_W = 1440
VIEWPORT_H = 900
MAX_TURNS = 60          # hard stop — session ends after this many turns
SCREENSHOT_PAUSE_MS = 1500  # wait after each action before next screenshot

FRONTEND_URL = "http://localhost:5173"
DOCS_DIR = Path(__file__).parents[1] / "docs" / "ux" / "usability-sessions"
TRANSCRIPT_DIR = DOCS_DIR / "transcripts"

# ---------------------------------------------------------------------------
# Persona task prompts (verbatim from pillar-2-methodology.md Appendix A)
# ---------------------------------------------------------------------------

PERSONA_PROMPTS: dict[str, dict[str, str]] = {
    "persona-2": {
        "use_case": "IMF+loan+evaluation",
        "prompt": """You are Eleni Papadopoulos, Deputy Finance Minister of Greece. The year is 2012.
The Troika — IMF, ECB, and European Commission — has just circulated a draft
conditionality package for Greece's second bailout. The package includes minimum wage
cuts of 22%, further pension reductions, and an accelerated privatisation schedule.
Your negotiating session begins in the morning. You have tonight to identify which
specific terms cross human cost thresholds — and to build a counter-proposal that
achieves the same fiscal consolidation target while protecting the cohorts most
vulnerable to the proposed measures.

You have been given access to an analytical tool. Use it to answer this question:
**Which specific terms in the conditionality package drive critical threshold crossings,
at which step, and for which cohorts — and what is the minimum modification that avoids
those crossings?**""",
    },
    "persona-1": {
        "use_case": "fiscal+multiplier+analysis",
        "prompt": """You are Lucas Ferreira, Country Economist at the IMF Fiscal Affairs Department. You are
building the Article IV consultation for a mid-size European economy facing early-stage
fiscal stress. The programme design your team is developing assumes a fiscal multiplier
of 0.5 — the IMF consensus estimate. You have seen internal literature suggesting the
true multiplier may be closer to 1.5. Before the design meeting tomorrow, you want to
understand what the difference means for human development threshold crossings.

You have been given access to an analytical tool. Use it to answer this question:
**What happens to poverty headcount and health system capacity threshold crossings if
the fiscal multiplier is 1.5 instead of 0.5 — at which step, and in which income
cohort does the difference become critical?**""",
    },
    "persona-5": {
        "use_case": "executive+board+briefing",
        "prompt": """You are an Executive Director at the IMF, representing a developing-country
constituency. The Executive Board session on the Greek programme resumes in 5 minutes.
You have read the 80-page staff report. You are not an economist. Your question going
into the room is whether the financial recovery the programme is producing is being
purchased at proportionate or disproportionate human cost — and whether there were
alternative paths.

You have been given access to an analytical tool. Use it to answer this question:
**Has the Greek programme produced financial recovery and human development deterioration
simultaneously — and if so, was that tradeoff avoidable?**""",
    },
}

# ---------------------------------------------------------------------------
# System prompt sent to the agent (cold-start: no WorldSim knowledge)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are navigating an analytical tool to answer a question. You have never seen this \
tool before. As you work, narrate your thinking in real time using these markers:

[LOOKING FOR: ...]    — what you are trying to find right now
[TRIED: ...]          — what action you just took (click, scroll, read)
[FOUND: ...]          — what you actually found
[EXPECTED: ...]       — what you expected to find
[CONFUSED: ...]       — where the interface did not match your expectation
[GAVE UP ON: ...]     — something you stopped trying, and why
[CONCLUDED: ...]      — your final answer at the end

Emit these markers inline with your reasoning — before and after each action, not \
reconstructed afterward. When you have answered the question (or concluded you cannot), \
click the "End Session" button visible at the top of the screen.

Do not read source code, API documentation, or configuration files. Navigate only \
through the visual interface you see on screen.\
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def take_screenshot(page: Page) -> str:
    """Return a base64-encoded PNG of the current viewport."""
    png = page.screenshot(type="png")
    return base64.standard_b64encode(png).decode()


def build_screenshot_message(b64: str) -> dict:
    return {
        "type": "tool_result",
        "tool_use_id": "initial",
        "content": [
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": b64},
            }
        ],
    }


def execute_action(page: Page, action: str, inp: dict) -> None:
    """Translate a computer-use action into a Playwright call."""
    coord = inp.get("coordinate", [0, 0])
    x, y = coord[0], coord[1]

    if action == "screenshot":
        pass  # handled by the loop

    elif action == "left_click":
        page.mouse.click(x, y)

    elif action == "double_click":
        page.mouse.dblclick(x, y)

    elif action == "right_click":
        page.mouse.click(x, y, button="right")

    elif action == "middle_click":
        page.mouse.click(x, y, button="middle")

    elif action == "mouse_move":
        page.mouse.move(x, y)

    elif action == "type":
        page.keyboard.type(inp.get("text", ""))

    elif action == "key":
        # Map Anthropic key names to Playwright key names
        key = inp.get("key", "")
        key_map = {
            "Return": "Enter", "Escape": "Escape", "Tab": "Tab",
            "BackSpace": "Backspace", "Delete": "Delete", "space": "Space",
            "ctrl+c": "Control+c", "ctrl+v": "Control+v",
            "ctrl+a": "Control+a", "ctrl+z": "Control+z",
            "ctrl+s": "Control+s",
            "super": "Meta",
        }
        page.keyboard.press(key_map.get(key, key))

    elif action == "scroll":
        direction = inp.get("scroll_direction", "down")
        amount = inp.get("scroll_amount", 3)
        delta_y = amount * 100 if direction == "down" else -amount * 100
        delta_x = amount * 100 if direction == "right" else (-amount * 100 if direction == "left" else 0)
        page.mouse.wheel(delta_x, delta_y)

    elif action == "left_click_drag":
        start = inp.get("startCoordinate", [0, 0])
        end = inp.get("endCoordinate", [0, 0])
        page.mouse.move(start[0], start[1])
        page.mouse.down()
        page.mouse.move(end[0], end[1])
        page.mouse.up()

    elif action == "wait":
        duration = inp.get("duration", 1)
        time.sleep(duration)

    else:
        print(f"  [runner] unknown action: {action}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Session loop
# ---------------------------------------------------------------------------


def run_session(session_id: str, persona_id: str, scenario_id: str | None) -> list[str]:
    """
    Run one usability session. Returns the transcript lines.
    """
    persona = PERSONA_PROMPTS.get(persona_id)
    if not persona:
        raise ValueError(f"Unknown persona: {persona_id}. Available: {list(PERSONA_PROMPTS)}")

    use_case = persona["use_case"]
    task_prompt = persona["prompt"]

    session_url = (
        f"{FRONTEND_URL}/?usability_session={session_id}"
        f"&persona={persona_id}&use_case={use_case}"
        + (f"&scenario={scenario_id}" if scenario_id else "")
    )

    print(f"\n{'='*60}")
    print(f"Session ID  : {session_id}")
    print(f"Persona     : {persona_id}")
    print(f"URL         : {session_url}")
    print(f"Model       : {MODEL}")
    print(f"{'='*60}\n")

    client = anthropic.Anthropic()
    transcript_lines: list[str] = []
    messages: list[dict] = []

    def log(line: str) -> None:
        print(line)
        transcript_lines.append(line)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, channel="chrome")
        context = browser.new_context(viewport={"width": VIEWPORT_W, "height": VIEWPORT_H})
        page = context.new_page()

        # Navigate to session URL — activates rrweb recording banner
        page.goto(session_url, wait_until="networkidle", timeout=20000)
        if scenario_id:
            page.wait_for_timeout(3000)  # wait for scenario auto-load

        # Seed the conversation: task prompt + first screenshot
        initial_screenshot = take_screenshot(page)
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"{task_prompt}\n\nHere is the URL: {session_url}"},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": initial_screenshot,
                        },
                    },
                ],
            }
        ]

        log(f"# Session Transcript — {session_id}")
        log(f"Persona: {persona_id}")
        log(f"Use case: {use_case.replace('+', ' ')}")
        log(f"Session valid: YES — cold-start agent (no prior WorldSim context)")
        log(f"Model: {MODEL}")
        log(f"Session URL: {session_url}")
        log("")
        log("---")
        log("")

        turn = 0
        session_ended = False

        while turn < MAX_TURNS and not session_ended:
            turn += 1
            print(f"\n[turn {turn}] calling API...", file=sys.stderr)

            response = client.beta.messages.create(
                model=MODEL,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=[
                    {
                        "type": TOOL_TYPE,
                        "name": "computer",
                        "display_width_px": VIEWPORT_W,
                        "display_height_px": VIEWPORT_H,
                    }
                ],
                messages=messages,
                betas=[BETA],
            )

            # Collect text output and tool uses from this response
            text_parts: list[str] = []
            tool_uses: list[dict] = []

            for block in response.content:
                if hasattr(block, "text"):
                    text_parts.append(block.text)
                elif block.type == "tool_use":
                    tool_uses.append(block)

            # Log the agent's think-aloud text
            if text_parts:
                agent_text = "\n".join(text_parts)
                log(agent_text)
                if "[CONCLUDED:" in agent_text:
                    session_ended = True

            # Append assistant message
            messages.append({"role": "assistant", "content": response.content})

            if session_ended:
                print("[runner] Agent concluded — ending session.", file=sys.stderr)
                break

            if response.stop_reason == "end_turn" and not tool_uses:
                print("[runner] end_turn with no tool uses — session over.", file=sys.stderr)
                break

            if not tool_uses:
                break

            # Execute each tool use and collect results
            tool_results = []
            for tu in tool_uses:
                action = tu.input.get("action", "")
                print(f"  [action] {action} {tu.input}", file=sys.stderr)

                if action != "screenshot":
                    execute_action(page, action, tu.input)
                    page.wait_for_timeout(SCREENSHOT_PAUSE_MS)

                # Always return a fresh screenshot as the tool result
                new_screenshot = take_screenshot(page)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": new_screenshot,
                            },
                        }
                    ],
                })

            messages.append({"role": "user", "content": tool_results})

        # Attempt to click End Session button if not already done
        if not session_ended:
            log("\n[runner: 45-minute limit reached — coordinator ending session]")

        try:
            end_btn = page.locator('[data-testid="end-session-btn"]')
            if end_btn.is_visible(timeout=2000):
                end_btn.click(force=True)
                page.wait_for_timeout(3000)
                banner = page.locator('[data-testid="session-recording-banner"]').text_content(timeout=2000)
                log(f"\n[Session saved: {banner.strip()[:80]}]")
        except Exception as e:
            log(f"\n[End Session click failed: {e}]")

        browser.close()

    return transcript_lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an M11.5 computer-use usability session")
    parser.add_argument("session_id", help="Session ID, e.g. 2026-06-04-persona-2-003")
    parser.add_argument("persona_id", help="Persona ID, e.g. persona-2")
    parser.add_argument("--scenario", default=None, help="Scenario UUID to pre-load via ?scenario= URL param")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    transcript_path = TRANSCRIPT_DIR / f"{args.session_id}-transcript.md"

    lines = run_session(args.session_id, args.persona_id, args.scenario)

    with open(transcript_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\nTranscript written to: {transcript_path}")


if __name__ == "__main__":
    main()
