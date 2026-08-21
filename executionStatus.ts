export const EXECUTION_STATUS_URL = "/manus-storage/kernel_execution_status_v0.1_final_c74beb85.json";
export type ExecutionRun = { id: string; command: string; passed?: number; python_passed?: number; rust_passed?: number; skipped: number; failed: number; status: string; scope: string; adapters?: string[] };
export type ExecutionStatus = { schema: "sov.kernel_execution_status"; schema_version: "0.1.0"; generated_at: string; runs: ExecutionRun[]; operational_boundary: string };
export type ExecutionStatusLoad = { state: "loading" | "ready" | "unavailable"; status: ExecutionStatus | null; message?: string };
export async function loadExecutionStatus(fetcher: typeof fetch = fetch): Promise<ExecutionStatusLoad> {
  try { const response = await fetcher(EXECUTION_STATUS_URL); if (!response.ok) throw new Error(`Execution status returned ${response.status}`); const value: unknown = await response.json(); if (!value || typeof value !== "object") throw new Error("Execution status is invalid"); const status = value as Partial<ExecutionStatus>; if (status.schema !== "sov.kernel_execution_status" || status.schema_version !== "0.1.0" || !Array.isArray(status.runs)) throw new Error("Execution status schema is unsupported"); return { state: "ready", status: status as ExecutionStatus }; }
  catch (error) { return { state: "unavailable", status: null, message: error instanceof Error ? error.message : "Execution status unavailable" }; }
}
