import { describe, expect, it } from "vitest";

const releaseToken = process.env.SOVEREIGN_GITHUB_RELEASE_TOKEN;

const describeWithReleaseToken = releaseToken ? describe : describe.skip;

describeWithReleaseToken("SOVEREIGN_GITHUB_RELEASE_TOKEN", () => {
  it("can read the configured dashboard repository through the GitHub API", async () => {
    const response = await fetch("https://api.github.com/repos/LastFirst0/sovereign-engine-dashboard", {
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${releaseToken}`,
        "X-GitHub-Api-Version": "2022-11-28",
      },
    });

    expect(response.status).toBe(200);
    const repository = await response.json() as { full_name?: string };
    expect(repository.full_name).toBe("LastFirst0/sovereign-engine-dashboard");
  }, 15_000);
});
