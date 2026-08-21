import { describe, expect, it, vi } from "vitest";
import { loadEcosystemFeed } from "./ecosystem";

describe("ecosystem release feed", () => {
  it("fails closed when the fetched artifact is missing or malformed", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ schema: "wrong" }) }));
    const result = await loadEcosystemFeed();
    expect(result.state).toBe("unavailable");
    expect(result.feed).toBeNull();
    vi.unstubAllGlobals();
  });
});
