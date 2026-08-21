import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";

describe("persisted research-artifact API boundary", () => {
  it("exposes only the public read-only list procedure", () => {
    const procedures = appRouter._def.procedures;
    expect(Object.keys(procedures)).toEqual(["researchArtifacts.list"]);
    expect(procedures["researchArtifacts.list"]?._def.type).toBe("query");
    expect(Object.values(procedures).some((procedure) => procedure._def.type === "mutation")).toBe(false);
  });
});
