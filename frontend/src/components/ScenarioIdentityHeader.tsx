/**
 * ScenarioIdentityHeader — Zone 0 persistent scenario identity strip.
 *
 * Always visible in the main viewport above the instrument cluster.
 * Addresses GAP-02 (M11.5): every Priority A cold-start session failed to
 * confirm which scenario was loaded. A Board member citing a finding from
 * this tool is asserting "this is data for Greece" — this element makes
 * that assertion verifiable without coordinator guidance.
 *
 * Implements: Issue #744, M11.5 Priority A synthesis GAP-02 (universal).
 */

interface Props {
  scenarioName: string;
  entityId: string | null;
  currentStep: number | null;
  totalSteps: number;
  /** Mode 2 fiscal multiplier override (Issue #746). Shown when present and ≠ 1.0. */
  fiscalMultiplier?: number | null;
}

/** Status segment displayed at the right of the identity strip. */
export function formatStatus(currentStep: number | null, totalSteps: number): string {
  if (currentStep === null || currentStep === 0) return "Ready";
  if (currentStep >= totalSteps) return `Complete (${totalSteps} steps)`;
  return `Step ${currentStep} of ${totalSteps}`;
}

/** Returns the multiplier label string for the header strip, or null when no override is active. */
export function formatMultiplierLabel(fiscalMultiplier: number | null | undefined): string | null {
  if (fiscalMultiplier == null || fiscalMultiplier === 1.0) return null;
  return `Fiscal ×${fiscalMultiplier.toFixed(1)}`;
}

export function ScenarioIdentityHeader({ scenarioName, entityId, currentStep, totalSteps, fiscalMultiplier }: Props) {
  const multiplierLabel = formatMultiplierLabel(fiscalMultiplier);
  const parts: string[] = [
    `Scenario: ${scenarioName}`,
    entityId ? `Entity: ${entityId}` : "",
    multiplierLabel ? `Mode: 2 (${multiplierLabel})` : "",
    `Status: ${formatStatus(currentStep, totalSteps)}`,
  ].filter(Boolean);

  return (
    <div
      data-testid="scenario-identity-header"
      style={{
        background: "#1a1a2e",
        color: "#c8cce0",
        fontFamily: "monospace",
        fontSize: 12,
        padding: "5px 16px",
        whiteSpace: "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
        letterSpacing: "0.02em",
        borderBottom: "2px solid #2d3561",
        flexShrink: 0,
      }}
    >
      {parts.join("  /  ")}
    </div>
  );
}
