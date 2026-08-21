import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { PersistedArchiveContent } from "./PersistedArchive";

describe("PersistedArchive route", () => {
  it("renders the durable-metadata boundary and loading-safe state", () => {
    const html = renderToStaticMarkup(<PersistedArchiveContent archive={{ state: "loading", records: [] }} audits={[]} onRetry={() => undefined} />);
    expect(html).toContain("Persisted evidence index");
    expect(html).toContain("Versioned evidence files remain the authoritative payload");
    expect(html).toContain("Loading persisted research metadata");
  });
  it("renders persisted evidence received through the typed contract", () => {
    const html = renderToStaticMarkup(<PersistedArchiveContent archive={{ state: "ready", records: [{ id: 1, artifactKey: "m0.dna_geometry.v0", title: "M0 DNA geometry", category: "experiment", status: "fail", sourceUrl: "/artifact", contentDigest: null, summary: "No advantage", limitation: "No clinical claim", publicationState: "published", revision: 1, metadataDigest: "abc", updatedBy: "system-backfill", updatedAt: new Date() }] }} audits={[]} onRetry={() => undefined} />);
    expect(html).toContain("M0 DNA geometry");
    expect(html).toContain("No advantage");
  });
  it("links directly to the latest retained full-platform replay without overstating its scope", () => {
    const html = renderToStaticMarkup(<PersistedArchiveContent archive={{ state: "ready", records: [] }} audits={[]} onRetry={() => undefined} />);
    expect(html).toContain("Latest retained replay");
    expect(html).toContain("32232417722");
    expect(html).toContain("Open hosted run");
    expect(html).toContain("they do not establish a theory");
  });
});
