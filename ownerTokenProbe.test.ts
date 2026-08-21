import { describe, expect, it } from "vitest";
import { appRouter } from "../../server/routers";
import { createContext } from "../../server/trpc";

function requestWithToken(token: string | undefined) {
  return { headers: token ? { authorization: `Bearer ${token}` } : {} } as never;
}

describe("owner ingestion token", () => {
  it("accepts the configured server-side secret through the typed owner probe", async () => {
    const configured = process.env.SOVEREIGN_INGESTION_TOKEN;
    expect(configured).toBeTruthy();
    const context = await createContext({ req: requestWithToken(configured), res: {} as never });
    const caller = appRouter.createCaller(context);
    await expect(caller.ownerProbe()).resolves.toEqual({ authorized: true });
  });
  it("rejects a missing token through the same typed API boundary", async () => {
    const context = await createContext({ req: requestWithToken(undefined), res: {} as never });
    const caller = appRouter.createCaller(context);
    await expect(caller.ownerProbe()).rejects.toMatchObject({ code: "FORBIDDEN" });
  });
  it("rejects publication staging before a database write when the token is missing", async () => {
    const context = await createContext({ req: requestWithToken(undefined), res: {} as never });
    const caller = appRouter.createCaller(context);
    await expect(caller.publication.stage({ artifactKey: "owner.test.v1", title: "Owner test record", category: "governance", status: "unverifiable", sourceUrl: "/artifact", contentDigest: null, summary: "A typed owner-staging boundary test record.", limitation: "This mutation must be denied without owner authorization." })).rejects.toMatchObject({ code: "FORBIDDEN" });
  });
});
