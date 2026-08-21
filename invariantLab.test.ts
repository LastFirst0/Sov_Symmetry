import { describe, expect, it } from "vitest";
import { evaluateJourney, unavailableLabState } from "./invariantLab";
import type { KernelJourney } from "./ecosystem";
describe("guided invariant lab", () => {
  const journey: KernelJourney = { id: "symmetric", title: "Matrix symmetry", adapter_id: "matrix.symmetric.v1", non_claim: "Finite predicate only.", baseline: { declared_input: [[1]], receipt: { receipt_id: "base", status: "verified" } }, mutation: { declared_input: [[2]], receipt: { receipt_id: "mut", status: "fail" } }, unverifiable: { declared_input: [], receipt: { receipt_id: "bad", status: "unverifiable" } } };
  it("returns the generated baseline receipt", () => expect(evaluateJourney(journey, "baseline").receipt.status).toBe("verified"));
  it("returns the generated mutation receipt", () => expect(evaluateJourney(journey, "mutation").receipt.status).toBe("fail"));
  it("fails closed when generated release data is unavailable", () => expect(unavailableLabState("feed missing").receipt.status).toBe("unverifiable"));
});
