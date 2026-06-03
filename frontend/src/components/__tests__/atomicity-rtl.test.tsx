/**
 * RTL: Atomicity and mode indicator render-cycle tests.
 *
 * AC-006 — All four Zone 1 instruments update in a single React render cycle
 *   on step advance. Tested by wrapping advanceStep() in act() and asserting
 *   all four instrument DOM nodes reflect the new current_step value before
 *   act() resolves — no additional act() call required.
 *
 * US-026 — Mode indicator text updates within the same render cycle as the
 *   mode state change. Tested by setting store mode and asserting the
 *   ModeIndicator text reflects the new value within the same act() call.
 *
 * Why RTL and not Vitest subscribe?
 *   The Vitest subscribe test (TrajectoryView.test.ts §AC-006) verifies that
 *   the Zustand store emits exactly one state change per set() call. That is
 *   a store-level invariant test. This RTL test verifies the React rendering
 *   contract: that all subscribed components reflect the new state within the
 *   SAME React render cycle (act() boundary), not across multiple cycles.
 *   The two tests are complementary — one tests Zustand, one tests React.
 *
 * Approach for AC-006:
 *   Rather than rendering the full TrajectoryView (which requires Recharts/jsdom
 *   and is complex), we render four lightweight Zustand-subscriber components —
 *   one per Zone 1 instrument slot — that each display current_step from the
 *   store. This is functionally equivalent to the four real instruments and
 *   cleanly isolates the atomicity invariant from component rendering complexity.
 *
 * Source: docs/frontend/fa-brief-m9-instrument-cluster.md §Named Acceptance Criteria
 *         Issue #459 — QA Lead acceptance tests
 */
import { render, screen, act, cleanup } from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { useScenarioStepStore } from "../../store/scenarioStepStore";
import { ModeIndicator } from "../ModeIndicator";

// Explicit cleanup — @testing-library/react auto-cleanup requires a global
// afterEach, which Vitest exposes only as an import, not a global.
afterEach(cleanup);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Minimal Zone 1 subscriber — displays current_step from the Zustand atom. */
function StepSubscriber({ testId }: { testId: string }) {
  const { current_step } = useScenarioStepStore();
  return <div data-testid={testId}>{current_step}</div>;
}

// ---------------------------------------------------------------------------
// AC-006 — All four Zone 1 instruments update in one render cycle (act())
// ---------------------------------------------------------------------------

describe("AC-006 — atomicity: all Zone 1 subscribers reflect new step in one act()", () => {
  beforeEach(() => {
    useScenarioStepStore.getState().reset();
    useScenarioStepStore.getState().setScenario("test-scenario", 5, "MODE_1");
    useScenarioStepStore.setState({ current_step: 0 });
  });

  it("all four instrument subscribers show updated current_step after one act()", () => {
    render(
      <>
        <StepSubscriber testId="zone-1a" />
        <StepSubscriber testId="zone-1b" />
        <StepSubscriber testId="zone-1c" />
        <StepSubscriber testId="zone-1d" />
      </>,
    );

    // Baseline: all show step 0
    expect(screen.getByTestId("zone-1a").textContent).toBe("0");
    expect(screen.getByTestId("zone-1b").textContent).toBe("0");
    expect(screen.getByTestId("zone-1c").textContent).toBe("0");
    expect(screen.getByTestId("zone-1d").textContent).toBe("0");

    // Advance step inside a single act() boundary
    act(() => {
      useScenarioStepStore.getState().advanceStep();
    });

    // After act() resolves: all four subscribers must reflect step 1
    // No additional act() call should be required (atomicity contract).
    expect(screen.getByTestId("zone-1a").textContent).toBe("1");
    expect(screen.getByTestId("zone-1b").textContent).toBe("1");
    expect(screen.getByTestId("zone-1c").textContent).toBe("1");
    expect(screen.getByTestId("zone-1d").textContent).toBe("1");
  });

  it("second step advance: all four subscribers update atomically again", () => {
    render(
      <>
        <StepSubscriber testId="z1a" />
        <StepSubscriber testId="z1b" />
        <StepSubscriber testId="z1c" />
        <StepSubscriber testId="z1d" />
      </>,
    );

    act(() => { useScenarioStepStore.getState().advanceStep(); });
    act(() => { useScenarioStepStore.getState().advanceStep(); });

    expect(screen.getByTestId("z1a").textContent).toBe("2");
    expect(screen.getByTestId("z1b").textContent).toBe("2");
    expect(screen.getByTestId("z1c").textContent).toBe("2");
    expect(screen.getByTestId("z1d").textContent).toBe("2");
  });

  it("advanceStep at step_count: all four subscribers remain at step_count (no overshoot)", () => {
    useScenarioStepStore.setState({ current_step: 5 }); // at step_count

    render(
      <>
        <StepSubscriber testId="a1a" />
        <StepSubscriber testId="a1b" />
        <StepSubscriber testId="a1c" />
        <StepSubscriber testId="a1d" />
      </>,
    );

    act(() => { useScenarioStepStore.getState().advanceStep(); });

    // Should stay at 5 — not increment past step_count
    expect(screen.getByTestId("a1a").textContent).toBe("5");
    expect(screen.getByTestId("a1b").textContent).toBe("5");
    expect(screen.getByTestId("a1c").textContent).toBe("5");
    expect(screen.getByTestId("a1d").textContent).toBe("5");
  });
});

// ---------------------------------------------------------------------------
// US-026 — ModeIndicator text updates in same render cycle as mode state change
// ---------------------------------------------------------------------------

describe("US-026 — ModeIndicator: text updates within same act() as mode change", () => {
  beforeEach(() => {
    useScenarioStepStore.getState().reset();
  });

  it("MODE_1 → renders 'Replay'", () => {
    render(<ModeIndicator />);
    expect(screen.getByTestId("mode-indicator").textContent).toBe("Replay");
  });

  it("MODE_1 → MODE_2: indicator shows 'Simulation' within same act()", () => {
    render(<ModeIndicator />);

    act(() => {
      useScenarioStepStore.setState({ mode: "MODE_2" });
    });

    expect(screen.getByTestId("mode-indicator").textContent).toBe("Simulation");
  });

  it("MODE_1 → MODE_3: indicator shows 'Active Control' within same act()", () => {
    render(<ModeIndicator />);

    act(() => {
      useScenarioStepStore.setState({ mode: "MODE_3" });
    });

    expect(screen.getByTestId("mode-indicator").textContent).toBe("Active Control");
  });

  it("MODE_3 → MODE_1: indicator reverts to 'Replay'", () => {
    useScenarioStepStore.setState({ mode: "MODE_3" });

    render(<ModeIndicator />);
    expect(screen.getByTestId("mode-indicator").textContent).toBe("Active Control");

    act(() => {
      useScenarioStepStore.setState({ mode: "MODE_1" });
    });

    expect(screen.getByTestId("mode-indicator").textContent).toBe("Replay");
  });

  it("indicator never shows raw field names ('MODE_1', 'MODE_2', 'MODE_3')", () => {
    render(<ModeIndicator />);

    for (const mode of ["MODE_1", "MODE_2", "MODE_3"] as const) {
      act(() => { useScenarioStepStore.setState({ mode }); });
      const text = screen.getByTestId("mode-indicator").textContent ?? "";
      expect(text).not.toContain("MODE_1");
      expect(text).not.toContain("MODE_2");
      expect(text).not.toContain("MODE_3");
    }
  });
});
