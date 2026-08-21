export const reviewerRationaleTemplates = [
  { key: "evidence_trace_complete", decision: "approve" as const, title: "Evidence trace complete", text: "I verified that the cited artifact, declared metadata digest, and stated limitation are present and consistent. This decision approves the publication workflow only; it does not assert any external theory, physical interpretation, or applied outcome." },
  { key: "criteria_not_met", decision: "reject" as const, title: "Criteria not yet met", text: "I could not verify one or more declared provenance, integrity, or limitation requirements. The record should remain staged until the missing evidence is supplied and independently re-reviewed." },
  { key: "negative_result_preserved", decision: "approve" as const, title: "Negative result preserved", text: "I verified that the contrary or negative outcome is represented without reframing it as support. The stated limitations and next obligation remain visible in the publication record." },
  { key: "scope_mismatch", decision: "reject" as const, title: "Scope mismatch", text: "The proposed statement exceeds the declared finite predicate, dataset, protocol, or limitation boundary. The request should be revised to state only what the attached evidence can verify." },
] as const;

type PlanningRecord = { artifactKey: string; title: string; category: string; status: string; sourceUrl: string; contentDigest: string | null; limitation: string };
export function buildEvidenceTestPlan(record: PlanningRecord) {
  const categoryChecks: Record<string, string[]> = {
    experiment: ["Freeze the protocol, dataset manifest, split identifiers, and random-seed policy before any comparison.", "Predeclare the baseline, paired comparison, uncertainty method, and decision threshold.", "Run a negative or shuffled-label control where the protocol declares one."],
    release: ["Verify the artifact manifest and each declared digest before interpreting release status.", "Validate the attestation and public-key policy; return unverifiable when a trust prerequisite is absent.", "Record the exact verifier version and failure code in the receipt."],
    governance: ["Check that each action stays within its declared authorization and does not trigger a prohibited automatic promotion.", "Validate the controlling policy, source register, and any required reviewer quorum.", "Preserve a durable audit event for each authorized change."],
    research_register: ["Confirm the work package question, claim class, non-claims, owner role, and decision gate are declared.", "Verify that source manifests cover each factual input required by the planned test."],
    falsification: ["Confirm the contrary result, evidence pointer, and next obligation are present.", "Test only the stated structural or empirical predicate; do not convert a failed result into support."],
  };
  const statusChecks: Record<string, string[]> = {
    fail: ["Keep the failure verdict visible in all summaries and exports.", "Do not claim a positive advantage unless a new preregistered result clears its stated criterion."],
    unverifiable: ["Identify the missing trust input or evidence field before retrying verification.", "Return unverifiable rather than inferring a pass from incomplete provenance."],
    unavailable: ["Restore the declared source or mark the test blocked; do not substitute an unverified source."],
    verified: ["Recompute the declared finite predicate or metadata digest from the cited source before relying on this record."],
  };
  return {
    artifactKey: record.artifactKey,
    title: record.title,
    scope: `Bounded verification plan for ${record.category.replace(/_/g, " ")} evidence.`,
    requiredInputs: ["Versioned source URL", "Declared limitation", "Metadata digest or documented absence", "Named decision criterion"],
    checks: [...(categoryChecks[record.category] ?? []), ...(statusChecks[record.status] ?? [])],
    stopRules: ["Stop and mark the work blocked when provenance, protocol, or authorization is missing.", "Do not publish a new claim from this plan; a completed evidence packet and governed review are required."],
    nonClaims: [record.limitation, "This planner creates a checklist, not a result, diagnosis, prediction, or theory endorsement."],
  };
}
