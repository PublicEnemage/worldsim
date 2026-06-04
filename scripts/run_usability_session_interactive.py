#!/usr/bin/env python3
"""
M11.5 Pillar 2 — Interactive Playwright Session Server

Keeps a Playwright browser open and accepts actions via file-based IPC.
The coordinator (Claude Code) drives the session: it reads screenshots,
passes them to a cold-start subagent, parses the subagent's action request,
and writes the action here for execution.

Usage:
    python3 scripts/run_usability_session_interactive.py <session_id> <persona_id> [--scenario <uuid>]

IPC protocol (all files live in /tmp/worldsim_session_<id>/):
    screenshot.png   — current viewport screenshot (overwritten each turn)
    action.txt       — coordinator writes this; runner reads, executes, deletes
    status.txt       — runner writes "READY" when screenshot is fresh
    transcript.txt   — runner appends coordinator-provided think-aloud lines

Action format (written to action.txt):
    click:<text>           click the first visible element containing <text>
    click_testid:<id>      click element with data-testid=<id>
    scroll_down:<n>        scroll down n * 120px
    scroll_up:<n>          scroll up n * 120px
    scroll_to_top          scroll to top of page
    type:<text>            type <text> into the focused element
    press:<key>            press a key (Enter, Escape, Tab, etc.)
    wait:<seconds>         pause for N seconds
    done                   end the session (clicks End Session button)
    abort                  end without clicking End Session (session invalid)

Coordinator writes transcript lines to transcript_input.txt; runner appends
them to transcript.txt.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

FRONTEND_URL = "http://localhost:5173"
PERSONA_USE_CASES = {
    "persona-2": "IMF+loan+evaluation",
    "persona-1": "fiscal+multiplier+analysis",
    "persona-5": "executive+board+briefing",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("session_id")
    parser.add_argument("persona_id")
    parser.add_argument("--scenario", default=None)
    args = parser.parse_args()

    session_dir = Path(f"/tmp/worldsim_session_{args.session_id}")
    session_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = session_dir / "screenshot.png"
    action_path = session_dir / "action.txt"
    status_path = session_dir / "status.txt"
    transcript_path = session_dir / "transcript.txt"
    transcript_input_path = session_dir / "transcript_input.txt"

    # Clear any stale files from a previous run
    for f in [action_path, status_path, transcript_input_path]:
        f.unlink(missing_ok=True)

    use_case = PERSONA_USE_CASES.get(args.persona_id, "scenario+analysis")
    session_url = (
        f"{FRONTEND_URL}/?usability_session={args.session_id}"
        f"&persona={args.persona_id}&use_case={use_case}"
        + (f"&scenario={args.scenario}" if args.scenario else "")
    )

    print(f"[server] session_dir  : {session_dir}", flush=True)
    print(f"[server] session_url  : {session_url}", flush=True)
    print(f"[server] screenshot   : {screenshot_path}", flush=True)
    print(f"[server] action file  : {action_path}", flush=True)
    print(f"[server] status file  : {status_path}", flush=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, channel="chrome")
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print(f"[server] navigating to {session_url} ...", flush=True)
        page.goto(session_url, wait_until="networkidle", timeout=20000)
        if args.scenario:
            page.wait_for_timeout(3000)

        def take_screenshot() -> None:
            page.screenshot(path=str(screenshot_path), type="png")

        def set_ready(turn: int) -> None:
            status_path.write_text(f"READY:{turn}")

        def flush_transcript() -> None:
            if transcript_input_path.exists():
                text = transcript_input_path.read_text()
                transcript_input_path.unlink()
                with open(transcript_path, "a") as f:
                    f.write(text + "\n")

        def execute_action(raw: str) -> bool:
            """Execute one action. Returns False if session should end."""
            raw = raw.strip()
            print(f"[server] action: {raw!r}", flush=True)

            if raw == "done":
                # Click End Session button
                try:
                    end_btn = page.locator('[data-testid="end-session-btn"]')
                    end_btn.wait_for(state="visible", timeout=5000)
                    end_btn.click(force=True)
                    page.wait_for_timeout(3000)
                    banner = page.locator('[data-testid="session-recording-banner"]')
                    txt = banner.text_content(timeout=3000) or ""
                    print(f"[server] session saved: {txt.strip()[:80]}", flush=True)
                except Exception as e:
                    print(f"[server] end-session click failed: {e}", flush=True)
                return False

            if raw == "abort":
                print("[server] session aborted by coordinator", flush=True)
                return False

            # Parse and execute
            try:
                if raw.startswith("click:"):
                    text = raw[len("click:"):].strip()
                    page.get_by_text(text).first.click(timeout=5000)

                elif raw.startswith("click_testid:"):
                    tid = raw[len("click_testid:"):].strip()
                    page.locator(f'[data-testid="{tid}"]').first.click(
                        force=True, timeout=5000
                    )

                elif raw.startswith("scroll_down:"):
                    n = int(raw[len("scroll_down:"):].strip())
                    page.mouse.wheel(0, n * 120)

                elif raw.startswith("scroll_up:"):
                    n = int(raw[len("scroll_up:"):].strip())
                    page.mouse.wheel(0, -n * 120)

                elif raw == "scroll_to_top":
                    page.evaluate("window.scrollTo(0, 0)")

                elif raw.startswith("type:"):
                    text = raw[len("type:"):].strip()
                    page.keyboard.type(text)

                elif raw.startswith("press:"):
                    key = raw[len("press:"):].strip()
                    page.keyboard.press(key)

                elif raw.startswith("wait:"):
                    secs = float(raw[len("wait:"):].strip())
                    time.sleep(min(secs, 10))

                else:
                    print(f"[server] unrecognised action: {raw!r}", flush=True)

            except Exception as e:
                print(f"[server] action error: {e}", flush=True)

            return True

        # Initial screenshot
        take_screenshot()
        set_ready(0)
        print("[server] initial screenshot ready — waiting for coordinator", flush=True)

        turn = 0
        running = True

        while running:
            flush_transcript()

            if action_path.exists():
                raw_action = action_path.read_text().strip()
                action_path.unlink()
                status_path.unlink(missing_ok=True)

                running = execute_action(raw_action)

                if running:
                    page.wait_for_timeout(1500)  # let page settle
                    take_screenshot()
                    turn += 1
                    set_ready(turn)
                    print(f"[server] turn {turn} ready", flush=True)
            else:
                time.sleep(0.2)

        browser.close()
        print("[server] browser closed — session complete", flush=True)


if __name__ == "__main__":
    main()
