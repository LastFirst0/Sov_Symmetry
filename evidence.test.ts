import { afterEach, describe, expect, it, vi } from "vitest";
import { emptyEvidenceSummary, loadQ1Evidence, q1Blockers } from "./evidence";

describe("Q1 evidence loader", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("derives counts only from the two verified JSON artifacts", async () => {
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce({ ok: true, json: async () => ({ counts: { cases: 10, passed: 10, failed: 0 } }) })
      .mockResolvedValueOnce({ ok: true, json: async () => ({ total_cases: 5750, failures: [] }) }));
    await expect(loadQ1Evidence()).resolves.toMatchObject({ q1Cases: 10, q1Passed: 10, q1Failed: 0, q0FuzzCases: 5750, q0FuzzFailures: 0, state: "verified" });
  });

  it("fails closed when an artifact cannot be retrieved", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false }));
    await expect(loadQ1Evidence()).resolves.toMatchObject({ ...emptyEvidenceSummary, state: "unavailable" });
  });
});

describe("Q1 blocker tracker", () => {
  it("keeps unresolved promotion work visible rather than implying completion", () => {
    expect(q1Blockers).toHaveLength(6);
    expect(q1Blockers.filter((item) => item.state === "complete")).toHaveLength(1);
    expect(q1Blockers.filter((item) => item.state === "pending").map((item) => item.label)).toContain("Ed25519 fixture profile");
  });
});
