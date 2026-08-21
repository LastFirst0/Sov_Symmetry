import { describe, expect, it } from "vitest";

const enabled = process.env.RUN_LIVE_SAVED_VIEWS === "1";
const uniqueName = `live-view-${Date.now()}`;

async function list(cookie?: string) {
  const response = await fetch("http://localhost:3000/api/trpc/savedViews.list?batch=1", { headers: cookie ? { cookie } : {} });
  expect(response.status).toBe(200);
  const payload = await response.json() as [{ result?: { data?: { json?: { id: number; name: string }[] } } }];
  return { cookie: response.headers.get("set-cookie")?.split(";")[0] ?? cookie ?? "", views: payload[0]?.result?.data?.json ?? [] };
}

async function mutate(path: "save" | "remove", cookie: string, input: unknown) {
  const response = await fetch(`http://localhost:3000/api/trpc/savedViews.${path}?batch=1`, { method: "POST", headers: { cookie, "content-type": "application/json" }, body: JSON.stringify({ 0: { json: input } }) });
  expect(response.status).toBe(200);
  return response.json() as Promise<[{ result?: { data?: { json?: { id?: number; removed?: boolean } } } }]>;
}

describe("live signed-session saved views", () => {
  it.runIf(enabled)("persists a view for its signed session, isolates a fresh session, and removes the test view", async () => {
    const initial = await list();
    expect(initial.cookie).toContain("sov_archive_view_owner=");
    const created = await mutate("save", initial.cookie, { name: uniqueName, term: "M0", category: "experiment", status: "fail", sort: "updated_desc" });
    const id = created[0]?.result?.data?.json?.id;
    expect(id).toBeTypeOf("number");
    const restored = await list(initial.cookie);
    expect(restored.views.some((view) => view.name === uniqueName)).toBe(true);
    const fresh = await list();
    expect(fresh.views.some((view) => view.name === uniqueName)).toBe(false);
    const removed = await mutate("remove", initial.cookie, { id });
    expect(removed[0]?.result?.data?.json).toMatchObject({ removed: true });
    const afterRemoval = await list(initial.cookie);
    expect(afterRemoval.views.some((view) => view.name === uniqueName)).toBe(false);
  });
});
