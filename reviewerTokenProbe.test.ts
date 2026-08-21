import { describe, expect, it } from "vitest";
import { appRouter } from "../../server/routers";
import { createContext, reviewerTokens } from "../../server/trpc";

describe("reviewer token configuration", () => {
  it("accepts a configured reviewer credential through the protected typed endpoint", async () => {
    const entries = Object.entries(reviewerTokens());
    expect(entries.length).toBeGreaterThanOrEqual(2);
    const [reviewerId, token] = entries[0]!;
    const context = await createContext({ req: { headers: { authorization: `Bearer ${token}` } } as never, res: {} as never });
    await expect(appRouter.createCaller(context).reviewerProbe()).resolves.toEqual({ reviewerId });
  });
});
