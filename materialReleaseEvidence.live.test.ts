import { describe, expect, it } from "vitest";
import { listPublicReleaseEvidence } from "../../server/materialReleaseGovernance";

const describeWithReleaseToken = process.env.SOVEREIGN_GITHUB_RELEASE_TOKEN ? describe : describe.skip;

describeWithReleaseToken("public material-release evidence integration", () => {
  it("returns bounded replay or gate records with source identity, scope, limitation, and inspectable URL", async () => {
    const records = await listPublicReleaseEvidence();
    expect(records.length).toBeGreaterThan(0);
    expect(records.some((record) => record.kind === "unified_replay" || record.kind === "material_gate")).toBe(true);
    for (const record of records) {
      expect(record.sourceUrl).toMatch(/^https:\/\/github\.com\//);
      expect(record.testScope.length).toBeGreaterThan(20);
      expect(record.limitation.length).toBeGreaterThan(20);
      expect(["verified", "fail", "unverifiable"]).toContain(record.result);
    }
  }, 30_000);
});
