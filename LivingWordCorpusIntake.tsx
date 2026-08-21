import { useState } from "react";
import { FileCheck2, ShieldCheck, Upload } from "lucide-react";
import { clearIngestionToken, setIngestionToken } from "@/lib/ingestionToken";

type Role = "genesis_oshb" | "john_sblgnt";
const filenames: Record<Role, string> = { genesis_oshb: "Genesis_OSHB.json", john_sblgnt: "John_SBLGNT.json" };

export function LivingWordCorpusIntake({ onAccepted }: { onAccepted?: () => void }) {
  const [open, setOpen] = useState(false); const [role, setRole] = useState<Role>("genesis_oshb"); const [token, setToken] = useState(""); const [file, setFile] = useState<File | null>(null); const [notice, setNotice] = useState<string | null>(null); const [busy, setBusy] = useState(false);
  const submit = async (event: React.FormEvent) => {
    event.preventDefault(); setNotice(null);
    if (!file) { setNotice("Select the declared source JSON file before upload."); return; }
    if (file.name !== filenames[role]) { setNotice(`The declared ${role.replace(/_/g, " ")} role requires ${filenames[role]}.`); return; }
    setBusy(true); setIngestionToken(token);
    try {
      const response = await fetch("/api/corpus-sources/intake", { method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json", "X-Sovereign-Source-Role": role, "X-Sovereign-Original-Filename": file.name }, body: file });
      const payload = await response.json() as { code?: string; statement?: string; intake?: { sha256: string; byteLength: number; validationReport: string } };
      if (!response.ok) throw new Error(payload.code ?? "CORPUS_INTAKE_FAILED");
      setNotice(`Source accepted structurally: ${payload.intake?.byteLength.toLocaleString() ?? ""} bytes, SHA-256 ${payload.intake?.sha256.slice(0, 12) ?? ""}…. ${payload.statement ?? ""}`); setFile(null); onAccepted?.();
    } catch (error) { setNotice(`Source intake did not complete: ${error instanceof Error ? error.message : "unknown error"}. No publication or verification verdict was created.`); }
    finally { setBusy(false); setToken(""); clearIngestionToken(); }
  };
  return <section className="owner-ingestion"><button type="button" className="ingestion-toggle" onClick={() => setOpen((value) => !value)}><Upload size={14} /> Governed Living Word source upload</button>{open && <form onSubmit={submit}><div className="ingestion-intro"><ShieldCheck size={17} /><p>Upload retains one declared corpus source under owner authorization. The server validates structural format, computes a SHA-256 digest, stores the bytes under a server-issued key, and records provenance. Acceptance is not publication, evidence verification, or content interpretation.</p></div><div className="ingestion-grid"><label>Owner token<input type="password" required value={token} onChange={(event) => setToken(event.target.value)} autoComplete="off" /></label><label>Declared source role<select value={role} onChange={(event) => { setRole(event.target.value as Role); setFile(null); }}><option value="genesis_oshb">Genesis OSHB</option><option value="john_sblgnt">John SBLGNT</option></select></label><label className="wide">Required filename<input disabled value={filenames[role]} /></label><label className="wide">JSON source file<input type="file" accept="application/json,.json" required onChange={(event) => setFile(event.target.files?.[0] ?? null)} /><small>Maximum 25 MB. The server rejects an incorrect role/file-name pairing, invalid JSON, insufficient words, malformed identifiers, and source-schema inconsistencies.</small></label></div><div className="ingestion-submit"><button type="submit" disabled={busy}>{busy ? "Validating & storing…" : <><FileCheck2 size={13} /> Validate and retain source</>}</button>{notice && <p>{notice}</p>}</div></form>}</section>;
}
