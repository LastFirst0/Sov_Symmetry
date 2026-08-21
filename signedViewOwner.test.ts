import { describe, expect, it } from "vitest";
import { createContext } from "../../server/trpc";

function makeResponse() { const headers = new Map<string, string>(); return { headers, response: { setHeader: (name: string, value: string) => headers.set(name, value) } as never }; }

describe("signed saved-view owner identity", () => {
  it("restores the same verified owner from its HttpOnly cookie and isolates a fresh session", async () => {
    const first = makeResponse();
    const initial = await createContext({ req: { headers: {} } as never, res: first.response });
    const cookie = first.headers.get("Set-Cookie");
    expect(cookie).toContain("sov_archive_view_owner=");
    expect(cookie).toContain("HttpOnly");
    const returning = await createContext({ req: { headers: { cookie } } as never, res: makeResponse().response });
    const fresh = await createContext({ req: { headers: {} } as never, res: makeResponse().response });
    expect(returning.viewOwnerId).toBe(initial.viewOwnerId);
    expect(fresh.viewOwnerId).not.toBe(initial.viewOwnerId);
  });
});
