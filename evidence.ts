export type Q1EvidenceSummary = {
  q1Cases: number | null;
  q1Passed: number | null;
  q1Failed: number | null;
  q0FuzzCases: number | null;
  q0FuzzFailures: number | null;
  state: "loading" | "verified" | "unavailable";
  message?: string;
};

type Q1AuditPayload = { counts?: { cases?: number; passed?: number; failed?: number } };
type Q0FuzzPayload = { total_cases?: number; failures?: unknown[] };

export const Q1_AUDIT_URL = "/manus-storage/q1_security_audit_report_b1869aad.json";
export const Q0_FUZZ_URL = "/manus-storage/q0_adversarial_fuzz_report_rerun_19755623.json";

export const emptyEvidenceSummary: Q1EvidenceSummary = {
  q1Cases: null,
  q1Passed: null,
  q1Failed: null,
  q0FuzzCases: null,
  q0FuzzFailures: null,
  state: "loading",
};

export async function loadQ1Evidence(): Promise<Q1EvidenceSummary> {
  try {
    const [q1Response, q0Response] = await Promise.all([fetch(Q1_AUDIT_URL), fetch(Q0_FUZZ_URL)]);
    if (!q1Response.ok || !q0Response.ok) throw new Error("Verified evidence artifact could not be fetched");
    const [q1, q0] = await Promise.all([q1Response.json() as Promise<Q1AuditPayload>, q0Response.json() as Promise<Q0FuzzPayload>]);
    const q1Cases = q1.counts?.cases;
    const q1Passed = q1.counts?.passed;
    const q1Failed = q1.counts?.failed;
    const q0FuzzCases = q0.total_cases;
    const q0FuzzFailures = q0.failures?.length;
    if (![q1Cases, q1Passed, q1Failed, q0FuzzCases, q0FuzzFailures].every((value) => typeof value === "number")) {
      throw new Error("Verified evidence artifact has an unsupported schema");
    }
    return {
      q1Cases: q1Cases ?? null,
      q1Passed: q1Passed ?? null,
      q1Failed: q1Failed ?? null,
      q0FuzzCases: q0FuzzCases ?? null,
      q0FuzzFailures: q0FuzzFailures ?? null,
      state: "verified",
    };
  } catch (error) {
    return { ...emptyEvidenceSummary, state: "unavailable", message: error instanceof Error ? error.message : "Evidence unavailable" };
  }
}

export type BlockerState = "complete" | "pending";
export type Q1Blocker = { id: string; label: string; evidence: string; state: BlockerState; next: string };

export const q1Blockers: Q1Blocker[] = [
  { id: "baseline", label: "Deterministic audit baseline", evidence: "Q0 fuzz + Q1 oracle", state: "complete", next: "Maintain regression corpus" },
  { id: "parity", label: "Full Rust parity", evidence: "QG1 partial", state: "pending", next: "Map full fixture/error set and rationals" },
  { id: "ed25519", label: "Ed25519 fixture profile", evidence: "QG2 pending", state: "pending", next: "Replace HMAC-only fixture adapter" },
  { id: "persistence", label: "Durable quorum records", evidence: "QG3 pending", state: "pending", next: "Persist decisions, rejections, equivocation" },
  { id: "checkpoint", label: "Merkle checkpoint replay", evidence: "QG3 pending", state: "pending", next: "Bind checkpoints and proofs to decisions" },
  { id: "operations", label: "Operational security review", evidence: "QG5 pending", state: "pending", next: "Accept key lifecycle and incident policy" },
];
