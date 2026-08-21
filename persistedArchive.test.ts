import { describe, expect, it } from "vitest";
import { archiveLoadFromQuery } from "./persistedArchive";

const record = { id: 1, artifactKey: "m0.dna_geometry.v0", title: "M0", category: "experiment", status: "fail" as const, sourceUrl: "/artifact", contentDigest: "digest", summary: "No advantage", limitation: "No medical claim", updatedAt: new Date("2026-08-18T00:00:00.000Z") };

describe("archiveLoadFromQuery", () => {
  it("returns database-backed records only from the typed ready contract", () => {
    const result = archiveLoadFromQuery({ isLoading: false, error: null, data: [record] });
    expect(result.state).toBe("ready");
    expect(result.records[0]?.artifactKey).toBe("m0.dna_geometry.v0");
    expect(result.records[0]?.status).toBe("fail");
  });
  it("fails closed when the typed archive query fails", () => {
    const result = archiveLoadFromQuery({ isLoading: false, error: new Error("unavailable"), data: undefined });
    expect(result.state).toBe("unavailable");
    expect(result.records).toEqual([]);
  });
});
