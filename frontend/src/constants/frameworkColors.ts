/**
 * Framework color constants — confirmed by UX Designer Agent, 2026-05-23.
 *
 * MV-001 (CVD validation) closed this session:
 *   - Ecological provisional green (#3A7A4B) / Human Development orange (#C67C2E) both shift
 *     toward yellow-olive under deuteranopia — indistinguishable.
 *   - Fix: replace green with teal (#1A8FA0), which shifts toward blue under CVD (opposite
 *     direction from amber #D4841A), preserving distinction.
 *   - Financial blue strengthened to #2271B3 to survive 60% opacity ghost curves.
 *   - Governance purple saturated to #7B50A8 to separate from Financial blue under CVD shift.
 *
 * Authority: UX Designer (ADR-010 Decision 3). Do not modify without UX Designer ruling.
 * Reference: fa-brief-m9-instrument-cluster.md §Framework Colors §CVD Validation Result
 */
export const FRAMEWORK_COLORS = {
  financial: "#2271B3",
  human_development: "#D4841A",
  ecological: "#1A8FA0",
  governance: "#7B50A8",
} as const;

export type FrameworkKey = keyof typeof FRAMEWORK_COLORS;
