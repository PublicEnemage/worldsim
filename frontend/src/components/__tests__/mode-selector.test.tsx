/**
 * Vitest/RTL: ModeSelector — unit tests.
 *
 * Authored BEFORE implementation from intent document at:
 * docs/process/intents/G8b-2026-06-13-mode-transition-step-preservation.md
 *
 * Covers:
 *   - getModeLabel regression: still returns correct values for all three modes
 *     after ModeIndicator → ModeSelector refactor (UX-RULING-3 / US-026)
 *   - ModeSelector at current_step=0: tapping inactive label calls setMode directly (no modal)
 *   - ModeSelector at current_step=3: tapping inactive label shows ModeTransitionModal
 *     before mode changes (SF-2 guard)
 *   - setMode store action: sets mode-only; does not reset current_step (SF-1 guard)
 *
 * Design authority: §7 of intent document.
 * Store action setMode spec: §7.1 — setMode must not call setScenario (which resets step).
 *
 * AC references from intent document:
 *   AC-1  — step preserved after transition (E2E primary; store-level unit here)
 *   AC-5  — SF-1: setMode does not reset current_step
 *   AC-6  — SF-2: modal shown before mode changes (RTL render-cycle assertion)
 *   AC-7  — current-step-display testid present (component-level presence)
 *
 * Imports from future component paths. Tests will fail to compile until
 * ModeSelector.tsx and ModeTransitionModal.tsx exist. This is expected —
 * these tests define the implementation contract, not describe existing code.
 */
import { render, screen, act, cleanup, fireEvent } from "@testing-library/react";
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { useScenarioStepStore } from "../../store/scenarioStepStore";
// getModeLabel regression — imported from existing location (still lives in ModeIndicator after refactor)
import { getModeLabel, MODE_LABELS } from "../ModeIndicator";
// New components authored as part of G8b implementation
import { ModeSelector } from "../ModeSelector";

afterEach(cleanup);

// ---------------------------------------------------------------------------
// getModeLabel regression
// These tests confirm the function is unchanged after the ModeIndicator →
// ModeSelector refactor. UX-RULING-3: no raw field names in displayed text.
// ---------------------------------------------------------------------------

describe("getModeLabel regression — UX-RULING-3 / US-026 unchanged after refactor", () => {
  it("MODE_1 → 'Replay'", () => {
    expect(getModeLabel("MODE_1")).toBe("Replay");
  });

  it("MODE_2 → 'Simulation'", () => {
    expect(getModeLabel("MODE_2")).toBe("Simulation");
  });

  it("MODE_3 → 'Active Control'", () => {
    expect(getModeLabel("MODE_3")).toBe("Active Control");
  });

  it("all three labels are distinct", () => {
    const labels = new Set([
      getModeLabel("MODE_1"),
      getModeLabel("MODE_2"),
      getModeLabel("MODE_3"),
    ]);
    expect(labels.size).toBe(3);
  });

  it("MODE_LABELS constant matches getModeLabel for all modes", () => {
    expect(MODE_LABELS.MODE_1).toBe(getModeLabel("MODE_1"));
    expect(MODE_LABELS.MODE_2).toBe(getModeLabel("MODE_2"));
    expect(MODE_LABELS.MODE_3).toBe(getModeLabel("MODE_3"));
  });

  it("no label contains raw field name substrings (MODE_1, MODE_2, MODE_3, underscore)", () => {
    for (const mode of ["MODE_1", "MODE_2", "MODE_3"] as const) {
      const label = getModeLabel(mode);
      expect(label).not.toContain("MODE_1");
      expect(label).not.toContain("MODE_2");
      expect(label).not.toContain("MODE_3");
      expect(label).not.toContain("_");
    }
  });
});

// ---------------------------------------------------------------------------
// setMode store action — SF-1 guard
//
// Intent §7.1: setMode sets mode only; does not reset current_step,
// trajectory, scenario_id, or any other state.
//
// This is the unit test for the new store action. The store action is authored
// as part of G8b implementation. These tests verify the contract.
// ---------------------------------------------------------------------------

describe("setMode store action — SF-1: mode-only state update", () => {
  beforeEach(() => {
    useScenarioStepStore.getState().reset();
    useScenarioStepStore.getState().setScenario("test-scenario-g8b", 8, "MODE_1");
    // Simulate being at step 3 (as in the Sri Lanka marquee case)
    useScenarioStepStore.setState({ current_step: 3 });
  });

  it("setMode('MODE_2') changes mode to MODE_2", () => {
    const store = useScenarioStepStore.getState();
    // setMode action added by G8b implementation (§7.1)
    store.setMode("MODE_2");
    expect(useScenarioStepStore.getState().mode).toBe("MODE_2");
  });

  it("setMode('MODE_2') does NOT reset current_step to 0 (SF-1 guard)", () => {
    const store = useScenarioStepStore.getState();
    store.setMode("MODE_2");
    // current_step must remain 3 — SF-1 silent failure is step resetting to 0
    expect(useScenarioStepStore.getState().current_step).toBe(3);
  });

  it("setMode('MODE_2') does NOT clear scenario_id", () => {
    const store = useScenarioStepStore.getState();
    store.setMode("MODE_2");
    expect(useScenarioStepStore.getState().scenario_id).toBe("test-scenario-g8b");
  });

  it("setMode('MODE_2') does NOT clear step_count", () => {
    const store = useScenarioStepStore.getState();
    store.setMode("MODE_2");
    expect(useScenarioStepStore.getState().step_count).toBe(8);
  });

  it("setMode('MODE_1') from MODE_2 reverts mode without side effects", () => {
    useScenarioStepStore.setState({ mode: "MODE_2" });
    useScenarioStepStore.getState().setMode("MODE_1");
    const state = useScenarioStepStore.getState();
    expect(state.mode).toBe("MODE_1");
    expect(state.current_step).toBe(3); // unchanged
    expect(state.scenario_id).toBe("test-scenario-g8b"); // unchanged
  });

  it("setMode('MODE_3') from MODE_1 transitions to MODE_3 without resetting step", () => {
    useScenarioStepStore.getState().setMode("MODE_3");
    expect(useScenarioStepStore.getState().mode).toBe("MODE_3");
    expect(useScenarioStepStore.getState().current_step).toBe(3);
  });
});

// ---------------------------------------------------------------------------
// ModeSelector component — AC-7: current-step-display testid present
//
// Intent §7.4: ScenarioControls.tsx adds data-testid="current-step-display"
// to the step counter span. This unit test confirms the testid is present
// in a rendered ModeSelector context (which embeds or co-renders with
// the step counter).
//
// Note: The step counter testid lives in ScenarioControls, not in ModeSelector.
// This test imports ModeSelector to validate the outer ModeSelector renders
// correctly. The ScenarioControls step-display testid is tested in E2E (AC-7).
// ---------------------------------------------------------------------------

describe("ModeSelector component — data-testid presence and structure", () => {
  beforeEach(() => {
    useScenarioStepStore.getState().reset();
    useScenarioStepStore.getState().setScenario("test-g8b", 8, "MODE_1");
  });

  it("renders mode-indicator container with data-testid and data-mode attributes", () => {
    render(<ModeSelector />);
    const indicator = screen.getByTestId("mode-indicator");
    expect(indicator).toBeTruthy();
    expect(indicator.getAttribute("data-mode")).toBe("MODE_1");
  });

  it("renders all three mode selector labels with named testids", () => {
    render(<ModeSelector />);
    expect(screen.getByTestId("mode-selector-label-MODE_1")).toBeTruthy();
    expect(screen.getByTestId("mode-selector-label-MODE_2")).toBeTruthy();
    expect(screen.getByTestId("mode-selector-label-MODE_3")).toBeTruthy();
  });

  it("active mode label shows correct text ('Replay' for MODE_1)", () => {
    render(<ModeSelector />);
    // The active label for MODE_1 must render "Replay" (UX-RULING-3)
    const replayLabel = screen.getByTestId("mode-selector-label-MODE_1");
    expect(replayLabel.textContent).toContain("Replay");
  });

  it("mode label text does not contain raw field names", () => {
    render(<ModeSelector />);
    const allText = screen.getByTestId("mode-indicator").textContent ?? "";
    expect(allText).not.toContain("MODE_1");
    expect(allText).not.toContain("MODE_2");
    expect(allText).not.toContain("MODE_3");
  });
});

// ---------------------------------------------------------------------------
// ModeSelector at current_step=0 — no modal on label tap
//
// Intent §6 (out of scope): "If current_step === 0 (scenario not yet advanced),
// the Mode 1→2 transition may omit the modal (no unsaved state) and transition
// directly."
//
// This test verifies that clicking an inactive label at step 0 calls setMode
// directly without showing a confirmation modal.
// ---------------------------------------------------------------------------

describe("ModeSelector at current_step=0 — direct transition, no modal", () => {
  beforeEach(() => {
    useScenarioStepStore.getState().reset();
    useScenarioStepStore.getState().setScenario("test-g8b-step0", 8, "MODE_1");
    // Explicitly confirm current_step is 0
    useScenarioStepStore.setState({ current_step: 0 });
  });

  it("tapping 'Simulation' label at step 0 does NOT show mode-transition-modal", () => {
    render(<ModeSelector />);

    // No modal in the initial render
    const modalBefore = screen.queryByTestId("mode-transition-modal");
    expect(modalBefore).toBeNull();

    // Click the "Simulation" label
    const simulationLabel = screen.getByTestId("mode-selector-label-MODE_2");
    act(() => {
      fireEvent.click(simulationLabel);
    });

    // Modal must still not be present — step 0 uses direct setMode path
    const modalAfter = screen.queryByTestId("mode-transition-modal");
    expect(modalAfter).toBeNull();
  });

  it("tapping 'Simulation' label at step 0 changes data-mode to MODE_2 immediately", () => {
    render(<ModeSelector />);

    const simulationLabel = screen.getByTestId("mode-selector-label-MODE_2");
    act(() => {
      fireEvent.click(simulationLabel);
    });

    // Mode must have changed directly (no modal gate at step 0)
    const indicator = screen.getByTestId("mode-indicator");
    expect(indicator.getAttribute("data-mode")).toBe("MODE_2");
  });

  it("tapping 'Simulation' at step 0 does not reset current_step (still 0 → not a regression)", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    expect(useScenarioStepStore.getState().current_step).toBe(0);
  });

  it("tapping the active MODE_1 label at step 0 is a no-op (no modal, no mode change)", () => {
    render(<ModeSelector />);

    const replayLabel = screen.getByTestId("mode-selector-label-MODE_1");
    act(() => {
      fireEvent.click(replayLabel);
    });

    // No modal
    expect(screen.queryByTestId("mode-transition-modal")).toBeNull();
    // Mode unchanged
    expect(screen.getByTestId("mode-indicator").getAttribute("data-mode")).toBe("MODE_1");
  });
});

// ---------------------------------------------------------------------------
// ModeSelector at current_step=3 — modal appears, blocks mode change (AC-6 unit level)
//
// Intent §4 AC-6 (SF-2): "assert mode-transition-modal is visible BEFORE
// mode-indicator attribute changes from data-mode='MODE_1'."
//
// These tests confirm the modal gate at the RTL level (no browser required).
// The Playwright AC-6 test confirms the same at the full app level.
// ---------------------------------------------------------------------------

describe("ModeSelector at current_step=3 — confirmation modal before mode change", () => {
  beforeEach(() => {
    useScenarioStepStore.getState().reset();
    useScenarioStepStore.getState().setScenario("test-g8b-step3", 8, "MODE_1");
    useScenarioStepStore.setState({ current_step: 3 });
  });

  it("tapping 'Simulation' label at step 3 shows mode-transition-modal", () => {
    render(<ModeSelector />);

    expect(screen.queryByTestId("mode-transition-modal")).toBeNull();

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    expect(screen.getByTestId("mode-transition-modal")).toBeTruthy();
  });

  it("modal is visible while mode-indicator still shows MODE_1 (SF-2: modal precedes mode change)", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    // Modal is present
    const modal = screen.getByTestId("mode-transition-modal");
    expect(modal).toBeTruthy();

    // Mode indicator still MODE_1 — modal has blocked the transition
    const indicator = screen.getByTestId("mode-indicator");
    expect(indicator.getAttribute("data-mode")).toBe("MODE_1");
  });

  it("modal contains confirm and cancel buttons", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    expect(screen.getByTestId("mode-transition-modal-confirm")).toBeTruthy();
    expect(screen.getByTestId("mode-transition-modal-cancel")).toBeTruthy();
  });

  it("modal text contains 'step position' and 'entity configuration' (AC-3 unit level)", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    const modal = screen.getByTestId("mode-transition-modal");
    const modalText = modal.textContent ?? "";
    expect(modalText).toContain("step position");
    expect(modalText).toContain("entity configuration");
  });

  it("clicking confirm changes data-mode to MODE_2 (AC-1 unit level)", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    act(() => {
      fireEvent.click(screen.getByTestId("mode-transition-modal-confirm"));
    });

    expect(screen.getByTestId("mode-indicator").getAttribute("data-mode")).toBe("MODE_2");
  });

  it("clicking confirm does NOT reset current_step (SF-1 unit level — AC-5)", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    act(() => {
      fireEvent.click(screen.getByTestId("mode-transition-modal-confirm"));
    });

    // current_step must remain 3 — setMode was used, not setScenario
    expect(useScenarioStepStore.getState().current_step).toBe(3);
  });

  it("clicking cancel leaves mode at MODE_1 and step at 3 (AC-4 unit level)", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    act(() => {
      fireEvent.click(screen.getByTestId("mode-transition-modal-cancel"));
    });

    expect(screen.getByTestId("mode-indicator").getAttribute("data-mode")).toBe("MODE_1");
    expect(useScenarioStepStore.getState().current_step).toBe(3);
    // Modal must be dismissed
    expect(screen.queryByTestId("mode-transition-modal")).toBeNull();
  });

  it("clicking cancel dismisses the modal", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    expect(screen.getByTestId("mode-transition-modal")).toBeTruthy();

    act(() => {
      fireEvent.click(screen.getByTestId("mode-transition-modal-cancel"));
    });

    expect(screen.queryByTestId("mode-transition-modal")).toBeNull();
  });

  it("tapping the active MODE_1 label at step 3 is a no-op (no modal, no mode change)", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_1"));
    });

    expect(screen.queryByTestId("mode-transition-modal")).toBeNull();
    expect(screen.getByTestId("mode-indicator").getAttribute("data-mode")).toBe("MODE_1");
  });
});

// ---------------------------------------------------------------------------
// ModeSelector mode store update atomicity
//
// Confirms ModeSelector uses setMode (mode-only path) and not setScenario
// (which resets current_step). This is the RTL equivalent of the SF-1 E2E guard.
// ---------------------------------------------------------------------------

describe("ModeSelector — mode state update atomicity (setMode path, not setScenario)", () => {
  beforeEach(() => {
    useScenarioStepStore.getState().reset();
    useScenarioStepStore.getState().setScenario("atomicity-test", 5, "MODE_1");
    useScenarioStepStore.setState({ current_step: 3 });
  });

  it("after confirming modal at step 3: store.current_step is 3, store.mode is MODE_2", () => {
    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    act(() => {
      fireEvent.click(screen.getByTestId("mode-transition-modal-confirm"));
    });

    const state = useScenarioStepStore.getState();
    expect(state.mode).toBe("MODE_2");
    expect(state.current_step).toBe(3); // SF-1 guard: step preserved
    expect(state.scenario_id).toBe("atomicity-test"); // scenario_id preserved
    expect(state.step_count).toBe(5); // step_count preserved
  });

  it("after direct transition at step 0: store.current_step is 0, store.mode is MODE_2", () => {
    // Override step back to 0
    useScenarioStepStore.setState({ current_step: 0 });

    render(<ModeSelector />);

    act(() => {
      fireEvent.click(screen.getByTestId("mode-selector-label-MODE_2"));
    });

    const state = useScenarioStepStore.getState();
    expect(state.mode).toBe("MODE_2");
    expect(state.current_step).toBe(0); // was 0 before; still 0 after
    expect(state.scenario_id).toBe("atomicity-test");
  });
});
