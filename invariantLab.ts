import type { KernelJourney, KernelStatus } from "@/lib/ecosystem";

export type LabStatus = KernelStatus;
export type LabReceipt = { id: string; status: LabStatus; predicate: string; value: string; explanation: string; scope: string };
export type LabState = { mode: "baseline" | "mutation" | "unverifiable"; label: string; receipt: LabReceipt; input: unknown };

function stateFrom(journey: KernelJourney, mode: "baseline" | "mutation" | "unverifiable"): LabState {
  const sample = journey[mode]; const receipt = sample.receipt;
  return { mode, label: mode === "baseline" ? "fixture-backed baseline" : mode === "mutation" ? "one fixture-backed mutation" : "malformed input boundary", input: sample.declared_input, receipt: { id: receipt.receipt_id, status: receipt.status, predicate: journey.adapter_id, value: JSON.stringify(sample.declared_input), explanation: receipt.why ?? receipt.plain_status ?? "Generated receipt explanation unavailable.", scope: journey.non_claim || receipt.scope || "Scope unavailable." } };
}

export function evaluateJourney(journey: KernelJourney, mode: "baseline" | "mutation" | "unverifiable"): LabState { return stateFrom(journey, mode); }
export function unavailableLabState(message: string): LabState { return { mode: "unverifiable", label: "artifact unavailable", input: null, receipt: { id: "no-generated-receipt", status: "unverifiable", predicate: "No predicate selected", value: "—", explanation: message, scope: "No status is inferred when the generated release feed is unavailable." } }; }
