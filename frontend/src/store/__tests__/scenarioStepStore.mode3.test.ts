/**
 * Vitest: scenarioStepStore — Mode 3 branch action tests (G6b, Issue #753).
 *
 * Covers:
 *   - initBranch: sets baselineScenarioId, branchScenarioId, branchFromStep,
 *     branchStepsComputed=0, recomputeStatus="computing"
 *   - updateBranchProgress: advances branchStepsComputed
 *   - setBranchComplete: sets recomputeStatus="complete"
 *   - setBranchFailed: sets recomputeStatus="failed", nulls trajectory
 *   - resetBranch: restores all branch fields to defaults
 *   - reset(): Mode 3 fields included in full reset
 */
import { describe, it, expect, beforeEach } from "vitest";
import { useScenarioStepStore } from "../scenarioStepStore";

function getState() {
  return useScenarioStepStore.getState();
}

beforeEach(() => {
  useScenarioStepStore.getState().reset();
});

// ---------------------------------------------------------------------------
// initBranch
// ---------------------------------------------------------------------------

describe("initBranch", () => {
  it("sets baselineScenarioId, branchScenarioId, branchFromStep", () => {
    getState().initBranch("base-001", "branch-002", 3);
    const s = getState();
    expect(s.baselineScenarioId).toBe("base-001");
    expect(s.branchScenarioId).toBe("branch-002");
    expect(s.branchFromStep).toBe(3);
  });

  it("resets branchStepsComputed to 0", () => {
    // First, simulate some in-progress progress.
    getState().initBranch("base-001", "branch-002", 2);
    getState().updateBranchProgress(4);
    // Re-init should zero it out.
    getState().initBranch("base-001", "branch-003", 2);
    expect(getState().branchStepsComputed).toBe(0);
  });

  it("sets recomputeStatus to 'computing'", () => {
    getState().initBranch("base-001", "branch-002", 0);
    expect(getState().recomputeStatus).toBe("computing");
  });
});

// ---------------------------------------------------------------------------
// updateBranchProgress
// ---------------------------------------------------------------------------

describe("updateBranchProgress", () => {
  it("updates branchStepsComputed", () => {
    getState().initBranch("b", "c", 0);
    getState().updateBranchProgress(5);
    expect(getState().branchStepsComputed).toBe(5);
  });

  it("successive calls overwrite (not accumulate)", () => {
    getState().initBranch("b", "c", 0);
    getState().updateBranchProgress(2);
    getState().updateBranchProgress(4);
    expect(getState().branchStepsComputed).toBe(4);
  });
});

// ---------------------------------------------------------------------------
// setBranchComplete
// ---------------------------------------------------------------------------

describe("setBranchComplete", () => {
  it("sets recomputeStatus to 'complete'", () => {
    getState().initBranch("b", "c", 0);
    getState().setBranchComplete();
    expect(getState().recomputeStatus).toBe("complete");
  });

  it("does not change branchScenarioId", () => {
    getState().initBranch("b", "branch-007", 0);
    getState().setBranchComplete();
    expect(getState().branchScenarioId).toBe("branch-007");
  });
});

// ---------------------------------------------------------------------------
// setBranchFailed
// ---------------------------------------------------------------------------

describe("setBranchFailed", () => {
  it("sets recomputeStatus to 'failed'", () => {
    getState().initBranch("b", "c", 0);
    getState().setBranchFailed();
    expect(getState().recomputeStatus).toBe("failed");
  });

  it("nulls trajectory so baseline renders at full opacity", () => {
    getState().initBranch("b", "c", 0);
    getState().setBranchFailed();
    expect(getState().trajectory).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// resetBranch
// ---------------------------------------------------------------------------

describe("resetBranch", () => {
  it("clears all Mode 3 branch fields to defaults", () => {
    getState().initBranch("base-001", "branch-002", 5);
    getState().updateBranchProgress(3);
    getState().resetBranch();

    const s = getState();
    expect(s.baselineScenarioId).toBeNull();
    expect(s.branchScenarioId).toBeNull();
    expect(s.branchFromStep).toBeNull();
    expect(s.branchStepsComputed).toBe(0);
    expect(s.recomputeStatus).toBe("idle");
  });
});

// ---------------------------------------------------------------------------
// reset() — full store reset includes Mode 3 fields
// ---------------------------------------------------------------------------

describe("reset()", () => {
  it("includes Mode 3 branch fields in full reset", () => {
    getState().initBranch("base-001", "branch-002", 5);
    getState().reset();

    const s = getState();
    expect(s.baselineScenarioId).toBeNull();
    expect(s.branchScenarioId).toBeNull();
    expect(s.branchFromStep).toBeNull();
    expect(s.branchStepsComputed).toBe(0);
    expect(s.recomputeStatus).toBe("idle");
  });
});

// ---------------------------------------------------------------------------
// State machine: idle → computing → complete → reset → idle
// ---------------------------------------------------------------------------

describe("Mode 3 state machine lifecycle", () => {
  it("full lifecycle: idle → computing → complete → reset", () => {
    const s = useScenarioStepStore;

    // Initial idle.
    expect(s.getState().recomputeStatus).toBe("idle");

    // init → computing.
    s.getState().initBranch("base", "branch", 2);
    expect(s.getState().recomputeStatus).toBe("computing");

    // progress updates don't change status.
    s.getState().updateBranchProgress(1);
    expect(s.getState().recomputeStatus).toBe("computing");

    // complete.
    s.getState().setBranchComplete();
    expect(s.getState().recomputeStatus).toBe("complete");

    // reset → idle.
    s.getState().resetBranch();
    expect(s.getState().recomputeStatus).toBe("idle");
  });

  it("full lifecycle: idle → computing → failed → idle", () => {
    const s = useScenarioStepStore;

    s.getState().initBranch("base", "branch", 0);
    expect(s.getState().recomputeStatus).toBe("computing");

    s.getState().setBranchFailed();
    expect(s.getState().recomputeStatus).toBe("failed");

    s.getState().resetBranch();
    expect(s.getState().recomputeStatus).toBe("idle");
  });
});
