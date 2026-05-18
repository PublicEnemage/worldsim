import { useState, useEffect } from "react";

// Reads the browser's prefers-reduced-motion media query and reacts to changes.
// Returns true when the user has opted out of motion — consumers must disable
// animations when this is true (ADR-005 Amendment 3 Area 5 requirement).
export function usePrefersReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = useState(
    () => window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  );

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  return prefersReduced;
}
