import { useMemo, useState } from "react";
import { ExternalLink, RefreshCw, ShieldAlert, UserRoundCheck } from "lucide-react";
import { clearIngestionToken, setIngestionToken } from "@/lib/ingestionToken";
import { trpc } from "@/lib/trpc";

type ReviewScope = "semantics" | "implementation";
const scopeLabels: Record<ReviewScope, string> = { semantics: "Semantics review", implementation: "Implementation review" };

export function ExternalAdapterCandidateReview() {
  const status = trpc.externalAdapterReview.status.useQuery();
  const utils = trpc.useUtils();
  const [ownerToken, setOwnerToken] = useState("");
  const [reviewerIds, setReviewerIds] = useState<Record<ReviewScope, string>>({ semantics: "", implementation: "" });
  const [ownerNotice, setOwnerNotice] = useState<string | null>(null);
  const [inviteReviewerId, setInviteReviewerId] = useState("");
  const [inviteDisplayName, setInviteDisplayName] = useState("");
  const [inviteRole, setInviteRole] = useState<"reviewer" | "lead_reviewer" | "observer">("reviewer");
  const [inviteScope, setInviteScope] = useState<"general" | ReviewScope>("general");
  const [inviteNote, setInviteNote] = useState("Please review the declared scope independently. This invitation does not provide a token or automatically activate reviewer authority.");
  const [inviteExpiry, setInviteExpiry] = useState(14);
  const [acceptInvitationId, setAcceptInvitationId] = useState("");
  const [reviewerToken, setReviewerToken] = useState("");
  const [assignmentId, setAssignmentId] = useState("");
  const [decision, setDecision] = useState<"approved" | "blocked">("approved");
  const [rationale, setRationale] = useState("");
  const [attestation, setAttestation] = useState("");
  const [evidenceUrl, setEvidenceUrl] = useState("");
  const [reviewerNotice, setReviewerNotice] = useState<string | null>(null);
  const assignments = trpc.externalAdapterReview.assignments.useQuery(undefined, { enabled: false });
  const events = trpc.externalAdapterReview.events.useQuery(undefined, { enabled: false });
  const roster = trpc.reviewerMemberships.list.useQuery(undefined, { enabled: false });
  const invitations = trpc.reviewerInvitations.list.useQuery(undefined, { enabled: false });
  const assign = trpc.externalAdapterReview.assign.useMutation({
    onSuccess: async () => { setOwnerNotice("Reviewer scope assignment recorded. The reviewer must now submit their own attested decision."); await utils.externalAdapterReview.status.invalidate(); await assignments.refetch(); await events.refetch(); },
    onError: () => setOwnerNotice("Assignment was rejected. Use an active configured reviewer, keep the two reviewer IDs distinct, and do not reassign a completed scope."),
    onSettled: clearIngestionToken,
  });
  const decide = trpc.externalAdapterReview.decide.useMutation({
    onSuccess: async () => { setReviewerNotice("Scoped decision and independence attestation recorded. The candidate remains quarantined until a separate core admission and activation decision."); setReviewerToken(""); setRationale(""); setAttestation(""); setEvidenceUrl(""); await utils.externalAdapterReview.status.invalidate(); },
    onError: () => setReviewerNotice("Decision was rejected. Only the assigned active reviewer can decide once, with an evidence URL, rationale, and independence attestation."),
    onSettled: clearIngestionToken,
  });
  const createInvitation = trpc.reviewerInvitations.create.useMutation({
    onSuccess: async () => { setOwnerNotice("Invitation recorded. Share its ID and onboarding instructions privately; it does not create a reviewer token or membership."); setInviteReviewerId(""); setInviteDisplayName(""); await invitations.refetch(); },
    onError: () => setOwnerNotice("Invitation was rejected. Resolve any existing pending invitation for that reviewer ID and provide a substantive onboarding note."),
    onSettled: clearIngestionToken,
  });
  const revokeInvitation = trpc.reviewerInvitations.revoke.useMutation({
    onSuccess: async () => { setOwnerNotice("Invitation revoked."); await invitations.refetch(); },
    onError: () => setOwnerNotice("Invitation could not be revoked; it may already be accepted, expired, or revoked."),
    onSettled: clearIngestionToken,
  });
  const acceptInvitation = trpc.reviewerInvitations.accept.useMutation({
    onSuccess: () => { setReviewerNotice("Invitation accepted. A configured active reviewer membership is still required before you can receive a candidate-review scope."); setAcceptInvitationId(""); },
    onError: () => setReviewerNotice("Invitation acceptance was rejected. The reviewer token must match the invited reviewer ID and an active non-observer membership must already exist."),
    onSettled: clearIngestionToken,
  });
  const activeReviewers = useMemo(() => (roster.data ?? []).filter((member) => member.status === "active" && member.role !== "observer"), [roster.data]);
  const assignmentRows = assignments.data ?? [];
  const loadOwnerData = async () => { setOwnerNotice(null); setIngestionToken(ownerToken); await Promise.all([roster.refetch(), assignments.refetch(), events.refetch(), invitations.refetch()]); clearIngestionToken(); };
  const submitAssignment = (scope: ReviewScope) => { setOwnerNotice(null); setIngestionToken(ownerToken); assign.mutate({ scope, reviewerId: reviewerIds[scope] }); };
  const submitDecision = () => { setReviewerNotice(null); setIngestionToken(reviewerToken); decide.mutate({ assignmentId, decision, rationale, independenceAttestation: attestation, evidenceUrl }); };
  const submitInvitation = () => { setOwnerNotice(null); setIngestionToken(ownerToken); createInvitation.mutate({ proposedReviewerId: inviteReviewerId, displayName: inviteDisplayName, role: inviteRole, requestedScope: inviteScope, invitationNote: inviteNote, expiresInDays: inviteExpiry }); };
  const submitInvitationAcceptance = () => { setReviewerNotice(null); setIngestionToken(reviewerToken); acceptInvitation.mutate({ invitationId: acceptInvitationId }); };
  const data = status.data;
  return <section className="archive-visuals" aria-label="External adapter candidate quarantine and review tracking">
    <div className="filter-title"><ShieldAlert size={16} /><div><p className="eyebrow">EXTERNAL ADAPTER ADMISSION</p><h2>Candidate quarantine is active.</h2></div><span>{status.isLoading ? "loading" : "quarantined"}</span></div>
    {status.isLoading ? <p className="ledger-empty">Loading recorded candidate status…</p> : status.error || !data ? <div className="archive-state unavailable"><strong>Candidate status unavailable.</strong><p>The review state could not be retrieved; no admission is inferred.</p><button type="button" onClick={() => void status.refetch()}><RefreshCw size={14} /> Retry</button></div> : <>
      <div className="signal-stat"><span>{data.candidateId}@{data.candidateVersion}</span><strong>Quarantined · Gate 6 blocked</strong><small>{data.reason}</small></div>
      <div className="review-grid">{data.assignments.map((entry) => <article key={entry.scope}><div className="request-status"><span className={`archive-status ${entry.state}`}>{entry.state}</span><strong>{scopeLabels[entry.scope]}</strong></div><p>{entry.isAssigned ? (entry.reviewerAvailable ? "Assigned reviewer is active; awaiting their attested scoped decision." : "The assigned reviewer is not currently eligible. Owner action is required.") : "No reviewer is assigned to this required scope."}</p></article>)}</div>
      <div className="record-actions"><a href={data.packageUrl} target="_blank" rel="noreferrer"><ExternalLink size={13} /> Candidate package</a><a href={data.admissionReportUrl} target="_blank" rel="noreferrer"><ExternalLink size={13} /> Gate report</a><a href={data.firstRunUrl} target="_blank" rel="noreferrer"><ExternalLink size={13} /> First-run record</a></div>
      <small>Completing both reviews does not activate this package. A new core admission run and a separate explicit dispatch decision would still be required.</small>
      <div className="audit-list"><strong>Assignment event timeline</strong>{data.timeline.length === 0 ? <p className="ledger-empty">No assignment events yet. The candidate remains quarantined until distinct reviewers are invited, activated, assigned, and independently attest their scoped decisions.</p> : data.timeline.map((event, index) => <article key={`${event.occurredAt}-${index}`}><span className="audit-action">{event.action}</span><div><strong>{scopeLabels[event.scope as ReviewScope] ?? "Candidate review"}</strong><p>{event.actor} · {new Date(event.occurredAt).toLocaleString()}</p></div></article>)}</div>
    </>}
    <details className="saved-views"><summary><UserRoundCheck size={14} /> Owner invitation, assignment, and reviewer decision controls</summary><div className="saved-view-entry"><label>Owner token<input type="password" value={ownerToken} onChange={(event) => setOwnerToken(event.target.value)} autoComplete="off" /></label><button type="button" disabled={!ownerToken || roster.isFetching || assignments.isFetching} onClick={() => void loadOwnerData()}>{roster.isFetching ? "Loading…" : "Load reviewer onboarding"}</button></div>{ownerNotice && <p>{ownerNotice}</p>}<div className="owner-ingestion"><h3>Invite a prospective reviewer</h3><p>An invitation is a tracked onboarding record, not a credential. The person must already be configured as an active reviewer before accepting it with their own reviewer token.</p><div className="ingestion-grid"><label>Proposed reviewer ID<input value={inviteReviewerId} onChange={(event) => setInviteReviewerId(event.target.value)} placeholder="reviewer-name" /></label><label>Display name<input value={inviteDisplayName} onChange={(event) => setInviteDisplayName(event.target.value)} /></label><label>Role<select value={inviteRole} onChange={(event) => setInviteRole(event.target.value as typeof inviteRole)}><option value="reviewer">Reviewer</option><option value="lead_reviewer">Lead reviewer</option><option value="observer">Observer</option></select></label><label>Requested scope<select value={inviteScope} onChange={(event) => setInviteScope(event.target.value as typeof inviteScope)}><option value="general">General onboarding</option><option value="semantics">Semantics review</option><option value="implementation">Implementation review</option></select></label><label>Expiry days<input type="number" min="1" max="30" value={inviteExpiry} onChange={(event) => setInviteExpiry(Number(event.target.value))} /></label><label className="wide">Onboarding note<textarea value={inviteNote} onChange={(event) => setInviteNote(event.target.value)} minLength={24} /></label></div><button type="button" disabled={!inviteReviewerId || !inviteDisplayName || inviteNote.trim().length < 24 || createInvitation.isPending} onClick={submitInvitation}>{createInvitation.isPending ? "Creating…" : "Create tracked invitation"}</button></div>{(invitations.data ?? []).length > 0 && <div className="audit-list"><strong>Invitation lifecycle</strong>{(invitations.data ?? []).map((item) => <article key={item.invitationId}><span className={`audit-action ${item.status}`}>{item.status}</span><div><strong>{item.displayName} · {item.requestedScope}</strong><p>Invitation ID: <code>{item.invitationId}</code> · expires {new Date(item.expiresAt).toLocaleString()}</p></div>{item.status === "pending" && <button type="button" onClick={() => { setIngestionToken(ownerToken); revokeInvitation.mutate({ invitationId: item.invitationId }); }}>Revoke</button>}</article>)}</div>}{activeReviewers.length > 0 && <div className="review-grid">{(["semantics", "implementation"] as ReviewScope[]).map((scope) => <article key={scope}><h3>{scopeLabels[scope]}</h3><select value={reviewerIds[scope]} onChange={(event) => setReviewerIds({ ...reviewerIds, [scope]: event.target.value })}><option value="">Choose a distinct active reviewer</option>{activeReviewers.map((member) => <option key={member.reviewerId} value={member.reviewerId}>{member.displayName} · {member.reviewerId}</option>)}</select><button type="button" disabled={!reviewerIds[scope] || assign.isPending} onClick={() => submitAssignment(scope)}>Assign scope</button></article>)}</div>}{assignmentRows.length > 0 && <div className="audit-list">{assignmentRows.map((item) => <article key={item.assignmentId}><span className={`audit-action ${item.status}`}>{item.status}</span><div><strong>{scopeLabels[item.scope as ReviewScope]} · {item.reviewerId}</strong><p>Assignment ID: <code>{item.assignmentId}</code></p><small>Use this ID with the assigned reviewer token below.</small></div></article>)}</div>}
      <div className="owner-ingestion"><h3>Reviewer acceptance and assigned decision</h3><p>Only the invited, assigned reviewer’s configured token can accept an invitation or submit a decision. Neither action creates a token.</p><div className="ingestion-grid"><label>Reviewer token<input type="password" value={reviewerToken} onChange={(event) => setReviewerToken(event.target.value)} autoComplete="off" /></label><label>Invitation ID to accept<input value={acceptInvitationId} onChange={(event) => setAcceptInvitationId(event.target.value)} /></label></div><button type="button" disabled={!reviewerToken || !acceptInvitationId || acceptInvitation.isPending} onClick={submitInvitationAcceptance}>{acceptInvitation.isPending ? "Accepting…" : "Accept invitation"}</button><div className="ingestion-grid"><label>Assignment ID<input value={assignmentId} onChange={(event) => setAssignmentId(event.target.value)} /></label><label>Decision<select value={decision} onChange={(event) => setDecision(event.target.value as "approved" | "blocked")}><option value="approved">Approve scoped review</option><option value="blocked">Block candidate review</option></select></label><label>Evidence URL<input type="url" value={evidenceUrl} onChange={(event) => setEvidenceUrl(event.target.value)} placeholder="https://…" /></label><label className="wide">Scoped rationale<textarea value={rationale} onChange={(event) => setRationale(event.target.value)} minLength={24} /></label><label className="wide">Independence attestation<textarea value={attestation} onChange={(event) => setAttestation(event.target.value)} minLength={32} placeholder="I am not the candidate author or controlling organization, and I reviewed only the assigned scope…" /></label></div><button type="button" disabled={!reviewerToken || !assignmentId || rationale.trim().length < 24 || attestation.trim().length < 32 || !evidenceUrl || decide.isPending} onClick={submitDecision}>{decide.isPending ? "Recording…" : "Record attested decision"}</button>{reviewerNotice && <p>{reviewerNotice}</p>}</div>
    </details>
  </section>;
}
