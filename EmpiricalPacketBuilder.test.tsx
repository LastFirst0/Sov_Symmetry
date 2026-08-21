/** @vitest-environment jsdom */
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import EmpiricalPacketBuilder from "./EmpiricalPacketBuilder";

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe("EmpiricalPacketBuilder", () => {
  it("refuses to export when required evidence fields are absent", async () => {
    const user = userEvent.setup(); render(<EmpiricalPacketBuilder />);
    await user.click(screen.getByRole("button", { name: /export local json draft/i }));
    expect(screen.getByText(/complete every named field/i)).toBeTruthy();
  });

  it("exports only after all declared evidence identifiers are supplied", async () => {
    const user = userEvent.setup(); const create = vi.fn(() => "blob:packet"); const revoke = vi.fn(); Object.defineProperty(URL, "createObjectURL", { value: create, configurable: true }); Object.defineProperty(URL, "revokeObjectURL", { value: revoke, configurable: true }); render(<EmpiricalPacketBuilder />);
    const fields: Array<[string, string]> = [["Target quantity", "length"], ["Unit", "m"], ["Scope", "bounded sample"], ["Dataset ID", "data:test"], ["Dataset version", "1"], ["Dataset SHA-256", "a".repeat(64)], ["License", "CC-BY-4.0"], ["Access conditions", "reviewed"], ["Custodian ID", "org:test"], ["Uncertainty basis", "declared basis"], ["External method ID", "method:test"], ["Protocol version", "1"], ["Output schema", "output.v1"]];
    for (const [label, value] of fields) await user.type(screen.getByLabelText(label), value);
    await user.click(screen.getByRole("button", { name: /export local json draft/i }));
    expect(create).toHaveBeenCalledOnce(); expect(screen.getByText(/local draft exported/i)).toBeTruthy();
  });
});
