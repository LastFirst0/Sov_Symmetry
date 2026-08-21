import { describe, expect, it } from "vitest";
import { buildEvidenceTestPlan, reviewerRationaleTemplates } from "../../server/testPlanning";

describe("evidence-bounded test planner", () => {
  it("turns a failed experiment record into checks and stop rules without creating a positive claim", () => {
    const plan = buildEvidenceTestPlan({ artifactKey: "m0.dna_geometry.v0", title: "M0", category: "experiment", status: "fail", sourceUrl: "/artifact", contentDigest: "digest", limitation: "Benchmark-only; no clinical claim." });
    expect(plan.checks.join(" ")).toContain("Predeclare the baseline");
    expect(plan.checks.join(" ")).toContain("failure verdict visible");
    expect(plan.nonClaims.join(" ")).toContain("not a result");
    expect(plan.stopRules.join(" ")).toContain("provenance");
  });
  it("offers templates whose declared decision matches approval or rejection only", () => {
    expect(reviewerRationaleTemplates.filter((item) => item.decision === "approve").length).toBeGreaterThan(0);
    expect(reviewerRationaleTemplates.filter((item) => item.decision === "reject").length).toBeGreaterThan(0);
    expect(reviewerRationaleTemplates.find((item) => item.key === "scope_mismatch")?.decision).toBe("reject");
  });
});
