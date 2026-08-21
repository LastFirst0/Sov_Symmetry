/** @vitest-environment jsdom */
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const ecosystemMock = vi.hoisted(() => ({ loadEcosystemFeed: vi.fn() }));
vi.mock("@/lib/ecosystem", () => ({ emptyEcosystemLoad: { state: "loading", feed: null }, loadEcosystemFeed: ecosystemMock.loadEcosystemFeed }));
import InvariantLab from "./InvariantLab";

const journey = { id: "symmetric", title: "Matrix symmetry", adapter_id: "matrix.symmetric.v1", non_claim: "Finite predicate only.", baseline: { declared_input: [[1, 2], [2, 4]], receipt: { receipt_id: "base", status: "verified", why: "Matrix is symmetric." } }, mutation: { declared_input: [[1, 7], [2, 4]], receipt: { receipt_id: "mutation", status: "fail", why: "Matrix is not symmetric." } }, unverifiable: { declared_input: [], receipt: { receipt_id: "malformed", status: "unverifiable" } } };

describe("fixture-backed InvariantLab", () => {
  beforeEach(() => { ecosystemMock.loadEcosystemFeed.mockReset(); window.localStorage.clear(); });
  afterEach(() => cleanup());
  it("loads a generated journey and gates mutation behind a prediction", async () => {
    ecosystemMock.loadEcosystemFeed.mockResolvedValue({ state: "ready", feed: { journeys: [journey] } }); const user = userEvent.setup(); render(<InvariantLab />);
    await screen.findByRole("heading", { name: "Matrix symmetry" }); const action = screen.getByRole("button", { name: /apply fixture mutation/i }) as HTMLButtonElement; expect(action.disabled).toBe(true); await user.click(screen.getByLabelText(/the check fails/i)); expect(action.disabled).toBe(false); await user.click(action); expect((await screen.findAllByText("fail")).length).toBeGreaterThanOrEqual(2);
  });
  it("shows an unverifiable state when the release feed is unavailable", async () => {
    ecosystemMock.loadEcosystemFeed.mockResolvedValue({ state: "unavailable", feed: null, message: "feed unavailable" }); render(<InvariantLab />); expect(await screen.findByText("feed unavailable")).toBeTruthy(); expect(screen.getAllByText("unverifiable").length).toBeGreaterThanOrEqual(2);
  });
});
