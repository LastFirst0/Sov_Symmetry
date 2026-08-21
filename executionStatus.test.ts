import { describe, expect, it } from "vitest";
import { loadExecutionStatus } from "./executionStatus";

const ready = { schema: "sov.kernel_execution_status", schema_version: "0.1.0", generated_at: "2026-08-19T05:42:00Z", runs: [{ id: "bounded", command: "pytest", passed: 3, skipped: 0, failed: 0, status: "pass", scope: "finite" }], operational_boundary: "record only" };
describe("recorded execution-status feed", () => {
  it("accepts a versioned execution-status artifact", async () => expect(await loadExecutionStatus(async () => new Response(JSON.stringify(ready), { status: 200 }))).toMatchObject({ state: "ready", status: { runs: [{ id: "bounded" }] } }));
  it("fails closed for unavailable or malformed artifacts", async () => { expect((await loadExecutionStatus(async () => new Response("missing", { status: 404 }))).state).toBe("unavailable"); expect((await loadExecutionStatus(async () => new Response(JSON.stringify({ schema: "wrong" }), { status: 200 }))).state).toBe("unavailable"); });
});
