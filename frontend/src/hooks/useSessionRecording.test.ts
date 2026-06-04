/**
 * Tests for useSessionRecording hook — Pillar 1, M11.5.
 *
 * Mocks rrweb's record() function and fetch to avoid real DOM recording or
 * network calls in the test environment.
 */
import { renderHook } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { useSessionRecording } from "./useSessionRecording";

vi.mock("rrweb", () => ({
  record: vi.fn(() => vi.fn()),
}));

const ORIGINAL_SEARCH = window.location.search;

function setSearchParams(params: string) {
  Object.defineProperty(window, "location", {
    writable: true,
    value: { ...window.location, search: params },
  });
}

function restoreLocation() {
  Object.defineProperty(window, "location", {
    writable: true,
    value: { ...window.location, search: ORIGINAL_SEARCH },
  });
}

let fetchMock: ReturnType<typeof vi.fn>;

beforeEach(() => {
  vi.clearAllMocks();
  fetchMock = vi.fn();
  vi.stubGlobal("fetch", fetchMock);
});

afterEach(() => {
  restoreLocation();
  vi.unstubAllGlobals();
});

describe("useSessionRecording", () => {
  describe("when usability_session param is absent", () => {
    it("isRecording is false", () => {
      setSearchParams("?");
      const { result } = renderHook(() => useSessionRecording());
      expect(result.current.isRecording).toBe(false);
    });

    it("sessionId is null", () => {
      setSearchParams("");
      const { result } = renderHook(() => useSessionRecording());
      expect(result.current.sessionId).toBeNull();
    });

    it("endSession returns error without calling fetch", async () => {
      setSearchParams("");
      const { result } = renderHook(() => useSessionRecording());
      const outcome = await result.current.endSession();
      expect(outcome.ok).toBe(false);
      expect(fetchMock).not.toHaveBeenCalled();
    });
  });

  describe("when usability_session param is present", () => {
    it("isRecording is true", () => {
      setSearchParams("?usability_session=test-session-001");
      const { result } = renderHook(() => useSessionRecording());
      expect(result.current.isRecording).toBe(true);
    });

    it("sessionId matches the URL param", () => {
      setSearchParams("?usability_session=2026-06-04-persona-1-001");
      const { result } = renderHook(() => useSessionRecording());
      expect(result.current.sessionId).toBe("2026-06-04-persona-1-001");
    });

    it("endSession posts to the sessions API", async () => {
      setSearchParams("?usability_session=test-session-save&persona=persona-1");
      fetchMock.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ session_id: "test-session-save" }),
      });

      const { result } = renderHook(() => useSessionRecording());
      const outcome = await result.current.endSession();

      expect(outcome.ok).toBe(true);
      expect(fetchMock).toHaveBeenCalledWith(
        "http://localhost:8000/api/v1/sessions/recording",
        expect.objectContaining({ method: "POST" })
      );
    });

    it("endSession returns error detail when fetch responds not-ok", async () => {
      setSearchParams("?usability_session=test-session-fail");
      fetchMock.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: "Session already exists." }),
      });

      const { result } = renderHook(() => useSessionRecording());
      const outcome = await result.current.endSession();

      expect(outcome.ok).toBe(false);
      expect(outcome.error).toBe("Session already exists.");
    });

    it("endSession can only be called once — second call skips fetch", async () => {
      setSearchParams("?usability_session=test-session-once");
      fetchMock.mockResolvedValue({
        ok: true,
        json: async () => ({}),
      });

      const { result } = renderHook(() => useSessionRecording());
      await result.current.endSession();
      const second = await result.current.endSession();

      expect(second.ok).toBe(false);
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });
  });
});
