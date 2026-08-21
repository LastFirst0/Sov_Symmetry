import { acceptReviewerInvitation, activateReceiptKeyRotation, approveReceiptKeyRotation, assertCurrentReceiptSigningKeyUsable, assignExternalAdapterReviewer, cancelReceiptKeyRotation, createReviewerInvitation, decideExternalAdapterReview, decidePublicationRequest, externalAdapterCandidateStatus, getArchiveExportReceipt, getReceiptSigningKey, listAllArchiveExportReceipts, listArchiveExportReceipts, listCorpusSourceIntakes, listExternalAdapterReviewAssignments, listExternalAdapterReviewEvents, listOwnerNotifications, listPublicationRequests, listPublicationReviews, listReceiptBundleTimeline, listReceiptKeyRotationRequests, listReceiptSigningKeys, listResearchArtifactAudits, listResearchArtifacts, listReviewerInvitations, listReviewerMemberships, listSavedArchiveViews, publishApprovedArtifact, recordArchiveExport, recordReceiptBundleSignature, recordReceiptSigningKey, refreshOwnerNotifications, requestReceiptKeyRotation, removeArchiveView, reviewerOperationsStatus, revokeReviewerInvitation, saveArchiveView, stageArtifactPublication, syncReviewerMemberships, updateOwnerNotification, updateReviewerMembership } from "./db";
import { createHash } from "node:crypto";
import { ownerProcedure, protectedProcedure, publicProcedure, reviewerProcedure, reviewerTokens, router } from "./trpc";
import { z } from "zod";
import { buildEvidenceTestPlan, reviewerRationaleTemplates } from "./testPlanning";
import { receiptSigningDescriptor, signReceiptBundlePayload } from "./receiptBundles";
import { artifactSubmissionProfile, artifactSubmissionProfiles } from "./artifactSubmission";
import { storagePutSignedReceiptBundle } from "./storage";
import { dispatchMaterialReleaseApproval, listOwnerMaterialReleaseTags, listPublicReleaseEvidence, previewMaterialReleaseTag } from "./materialReleaseGovernance";
import { compareReviewerInvitationExportReceipts, listReviewerInvitationExportReceipts, recordNearExpiryReviewerInvitationExport, reviewerInvitationExpiryPrintSummary, reviewerInvitationExportReceiptDetail } from "./db";

const artifactInput = z.object({
  artifactKey: z.string().min(3).max(128).regex(/^[a-z0-9._-]+$/),
  title: z.string().min(3).max(255),
  category: z.enum(["research_register", "falsification", "experiment", "release", "governance"]),
  status: z.enum(["verified", "fail", "unverifiable", "unavailable"]),
  sourceUrl: z.string().min(1).max(1024).refine((value) => value.startsWith("/") || /^https:\/\//.test(value), "Source must be a site-relative or HTTPS URL."),
  contentDigest: z.string().max(128).nullable().optional(),
  summary: z.string().min(12).max(8000),
  limitation: z.string().min(12).max(8000),
});
const filtersInput = z.object({ term: z.string().max(500), category: z.enum(["all", "research_register", "falsification", "experiment", "release", "governance"]), status: z.enum(["all", "verified", "fail", "unverifiable", "unavailable"]), sort: z.enum(["updated_desc", "updated_asc", "title_asc", "category_asc", "status_asc"]) });
const invitationExpiryWindowInput = z.union([z.literal(24), z.literal(48), z.literal(72)]);

export const appRouter = router({
  auth: router({
    me: publicProcedure.query(({ ctx }) => ctx.user),
  }),
  ownerProbe: ownerProcedure.query(() => ({ authorized: true as const })),
  reviewerProbe: reviewerProcedure.query(({ ctx }) => ({ reviewerId: ctx.reviewerId })),
  researchArtifacts: router({
    /** Public, read-only metadata catalogue. Evidence bytes remain in artifact storage. */
    list: publicProcedure.query(async () => listResearchArtifacts()),
    history: publicProcedure.input(z.object({ artifactKey: z.string().min(3).max(128).optional() })).query(async ({ input }) => listResearchArtifactAudits(input.artifactKey)),
  }),
  corpusSources: router({
    list: ownerProcedure.query(() => listCorpusSourceIntakes()),
  }),
  publication: router({
    list: publicProcedure.query(async () => listPublicationRequests()),
    reviews: publicProcedure.input(z.object({ requestKey: z.string().min(3).max(160).optional() })).query(async ({ input }) => listPublicationReviews(input.requestKey)),
    stage: ownerProcedure.input(artifactInput).mutation(async ({ input }) => stageArtifactPublication(input)),
    rationaleTemplates: publicProcedure.query(() => reviewerRationaleTemplates),
    decide: reviewerProcedure.input(z.object({ requestKey: z.string().min(3).max(160), decision: z.enum(["approve", "reject"]), rationale: z.string().min(8).max(4000), rationaleTemplateKey: z.string().max(64).nullable().optional() })).mutation(async ({ input, ctx }) => {
      const template = input.rationaleTemplateKey ? reviewerRationaleTemplates.find((item) => item.key === input.rationaleTemplateKey) : null;
      if (template && template.decision !== input.decision) throw new Error("RATIONALE_TEMPLATE_DECISION_MISMATCH");
      return decidePublicationRequest(input.requestKey, ctx.reviewerId, input.decision, input.rationale, input.rationaleTemplateKey ?? null);
    }),
    publish: ownerProcedure.input(z.object({ requestKey: z.string().min(3).max(160) })).mutation(async ({ input }) => publishApprovedArtifact(input.requestKey)),
  }),
  submissionGuidance: router({
    profiles: publicProcedure.query(() => artifactSubmissionProfiles),
    profile: publicProcedure.input(z.object({ category: z.enum(["research_register", "falsification", "experiment", "release", "governance"]) })).query(({ input }) => artifactSubmissionProfile(input.category)),
  }),
  reviewerMemberships: router({
    list: ownerProcedure.query(() => listReviewerMemberships()),
    syncConfigured: ownerProcedure.mutation(() => syncReviewerMemberships(Object.keys(reviewerTokens()), "owner-token")),
    update: ownerProcedure.input(z.object({ reviewerId: z.string().regex(/^[A-Za-z0-9._-]{3,128}$/), displayName: z.string().trim().min(3).max(128), role: z.enum(["reviewer", "lead_reviewer", "observer"]), status: z.enum(["active", "suspended"]) })).mutation(({ input }) => updateReviewerMembership({ ...input, managedBy: "owner-token" })),
  }),
  reviewerOperations: router({
    status: ownerProcedure.query(() => reviewerOperationsStatus()),
  }),
  externalAdapterReview: router({
    /** Public status is deliberately limited: it exposes the quarantine and progress, not reviewer credentials or owner governance metadata. */
    status: publicProcedure.query(async () => {
      const status = await externalAdapterCandidateStatus();
      return { candidateId: status.candidateId, candidateVersion: status.candidateVersion, sourceCommit: status.sourceCommit, packageUrl: status.packageUrl, admissionReportUrl: status.admissionReportUrl, firstRunUrl: status.firstRunUrl, status: status.status, reason: status.reason, independentlyReviewed: status.independentlyReviewed, admissionDecision: status.admissionDecision, activationAllowed: status.activationAllowed, assignments: status.assignments.map((entry) => ({ scope: entry.scope, state: entry.assignment?.status ?? "unassigned", isAssigned: entry.isAssigned, reviewerAvailable: entry.isActiveReviewer })), timeline: status.timeline };
    }),
    assignments: ownerProcedure.query(() => listExternalAdapterReviewAssignments()),
    events: ownerProcedure.query(() => listExternalAdapterReviewEvents()),
    assign: ownerProcedure.input(z.object({ scope: z.enum(["semantics", "implementation"]), reviewerId: z.string().regex(/^[A-Za-z0-9._-]{3,128}$/) })).mutation(({ input }) => assignExternalAdapterReviewer({ ...input, assignedBy: "owner-token" })),
    decide: reviewerProcedure.input(z.object({ assignmentId: z.string().min(8).max(96), decision: z.enum(["approved", "blocked"]), rationale: z.string().trim().min(24).max(6000), independenceAttestation: z.string().trim().min(32).max(2000), evidenceUrl: z.string().url().max(1024) })).mutation(({ input, ctx }) => decideExternalAdapterReview({ ...input, reviewerId: ctx.reviewerId })),
  }),
  reviewerInvitations: router({
    list: ownerProcedure.query(() => listReviewerInvitations()),
    create: ownerProcedure.input(z.object({ proposedReviewerId: z.string().regex(/^[A-Za-z0-9._-]{3,128}$/), displayName: z.string().trim().min(3).max(128), role: z.enum(["reviewer", "lead_reviewer", "observer"]), requestedScope: z.enum(["general", "semantics", "implementation"]), invitationNote: z.string().trim().min(24).max(2000), expiresInDays: z.number().int().min(1).max(30) })).mutation(({ input }) => createReviewerInvitation({ ...input, createdBy: "owner-token" })),
    revoke: ownerProcedure.input(z.object({ invitationId: z.string().min(8).max(96) })).mutation(({ input }) => revokeReviewerInvitation(input.invitationId)),
    accept: reviewerProcedure.input(z.object({ invitationId: z.string().min(8).max(96) })).mutation(({ input, ctx }) => acceptReviewerInvitation(input.invitationId, ctx.reviewerId)),
    exportExpiring: ownerProcedure.input(z.object({ windowHours: invitationExpiryWindowInput })).mutation(({ input, ctx }) => recordNearExpiryReviewerInvitationExport(ctx.user?.openId ?? "owner-token", input.windowHours)),
    exportHistory: ownerProcedure.query(({ ctx }) => listReviewerInvitationExportReceipts(ctx.user?.openId ?? "owner-token")),
    exportReceiptDetail: ownerProcedure.input(z.object({ receiptId: z.string().min(8).max(96) })).query(({ input, ctx }) => reviewerInvitationExportReceiptDetail(ctx.user?.openId ?? "owner-token", input.receiptId)),
    compareExportReceipts: ownerProcedure.input(z.object({ leftReceiptId: z.string().min(8).max(96), rightReceiptId: z.string().min(8).max(96) }).refine((input) => input.leftReceiptId !== input.rightReceiptId, "Select two different export receipts.")).query(({ input, ctx }) => compareReviewerInvitationExportReceipts(ctx.user?.openId ?? "owner-token", input.leftReceiptId, input.rightReceiptId)),
    printSummary: ownerProcedure.input(z.object({ windowHours: invitationExpiryWindowInput })).query(({ input }) => reviewerInvitationExpiryPrintSummary(input.windowHours)),
  }),
  materialReleaseEvidence: router({
    /** Public metadata only: no credentials, write controls, or inferred release eligibility are exposed. */
    list: publicProcedure.query(() => listPublicReleaseEvidence()),
  }),
  materialReleaseApprovals: router({
    list: ownerProcedure.query(() => listOwnerMaterialReleaseTags()),
    preview: ownerProcedure.input(z.object({ tag: z.string().trim().min(1).max(160) })).query(({ input }) => previewMaterialReleaseTag(input.tag)),
    /** Dispatches the canonical GitHub workflow; that workflow independently revalidates tag, commit, and successful gate evidence. */
    approve: ownerProcedure.input(z.object({ tag: z.string().trim().min(1).max(160) })).mutation(({ input }) => dispatchMaterialReleaseApproval(input.tag)),
  }),
  exports: router({
    signingKey: publicProcedure.query(() => receiptSigningDescriptor()),
    record: protectedProcedure.input(z.object({ format: z.enum(["csv", "json"]), filters: filtersInput })).mutation(({ input, ctx }) => recordArchiveExport(ctx.user.openId, input.format, input.filters)),
    mine: protectedProcedure.query(({ ctx }) => listArchiveExportReceipts(ctx.user.openId)),
    bundle: protectedProcedure.input(z.object({ receiptId: z.string().min(3).max(96) })).mutation(async ({ input, ctx }) => {
      const receipt = await getArchiveExportReceipt(ctx.user.openId, input.receiptId);
      if (!receipt) throw new Error("EXPORT_RECEIPT_NOT_FOUND");
      if (!receipt.resultManifest) throw new Error("EXPORT_RECEIPT_MANIFEST_UNAVAILABLE");
      let resultManifest: { artifactKey: string; revision: number; metadataDigest: string | null }[];
      try { resultManifest = JSON.parse(receipt.resultManifest); } catch { throw new Error("EXPORT_RECEIPT_MANIFEST_INVALID"); }
      if (!Array.isArray(resultManifest) || resultManifest.some((item) => typeof item?.artifactKey !== "string" || !Number.isInteger(item?.revision))) throw new Error("EXPORT_RECEIPT_MANIFEST_INVALID");
      const signing = receiptSigningDescriptor(); await assertCurrentReceiptSigningKeyUsable(signing);
      const bundle = signReceiptBundlePayload({ schema: "sov.archive_receipt_bundle.payload", schemaVersion: "0.1.0", receipt: { receiptId: receipt.receiptId, accountOpenId: receipt.accountOpenId, format: receipt.format, recordCount: receipt.recordCount, filtersSnapshot: receipt.filtersSnapshot, resultDigest: receipt.resultDigest, createdAt: receipt.createdAt.toISOString() }, resultManifest });
      const serializedBundle = JSON.stringify(bundle); const bundleDigest = createHash("sha256").update(serializedBundle).digest("hex");
      const bundleStorageKey = `signed-receipts/${receipt.receiptId}/${bundle.signing.keyFingerprint}/${bundleDigest}.json`;
      const storedBundle = await storagePutSignedReceiptBundle(bundleStorageKey, Buffer.from(serializedBundle, "utf8"));
      await recordReceiptSigningKey(bundle.signing);
      await recordReceiptBundleSignature({ receiptId: receipt.receiptId, keyFingerprint: bundle.signing.keyFingerprint, canonicalPayload: bundle.canonicalPayload, bundleStorageKey: storedBundle.key, bundleStorageUrl: storedBundle.url, bundleDigest });
      return bundle;
    }),
    timeline: protectedProcedure.query(({ ctx }) => listReceiptBundleTimeline(ctx.user.openId)),
    all: ownerProcedure.query(() => listAllArchiveExportReceipts()),
  }),
  signingKeyHistory: router({
    list: publicProcedure.query(() => listReceiptSigningKeys()),
    lookup: publicProcedure.input(z.object({ keyFingerprint: z.string().regex(/^[a-f0-9]{64}$/) })).query(async ({ input }) => {
      const current = receiptSigningDescriptor();
      if (current.keyFingerprint === input.keyFingerprint) return { ...current, status: "active" as const, source: "current" as const };
      const record = await getReceiptSigningKey(input.keyFingerprint);
      if (!record) throw new Error("SIGNING_KEY_NOT_FOUND");
      return { algorithm: record.algorithm, keyFingerprint: record.keyFingerprint, publicKeyJwk: JSON.parse(record.publicKeyJwk) as JsonWebKey, status: record.status, firstSeenAt: record.firstSeenAt, lastSeenAt: record.lastSeenAt, retiredAt: record.retiredAt, source: "historical" as const };
    }),
  }),
  keyLifecycle: router({
    list: ownerProcedure.query(() => listReceiptKeyRotationRequests()),
    request: ownerProcedure.input(z.object({ publicKeyJwk: z.object({ kty: z.literal("OKP"), crv: z.literal("Ed25519"), x: z.string().min(1) }).passthrough(), expiresAt: z.coerce.date(), rationale: z.string().trim().min(12).max(2000) })).mutation(({ input }) => requestReceiptKeyRotation({ algorithm: "Ed25519", publicKeyJwk: input.publicKeyJwk, requestedExpiryAt: input.expiresAt, rationale: input.rationale, requestedBy: "owner-token" })),
    approve: ownerProcedure.input(z.object({ requestId: z.string().min(3).max(96) })).mutation(({ input }) => approveReceiptKeyRotation(input.requestId)),
    cancel: ownerProcedure.input(z.object({ requestId: z.string().min(3).max(96) })).mutation(({ input }) => cancelReceiptKeyRotation(input.requestId)),
    activate: ownerProcedure.input(z.object({ requestId: z.string().min(3).max(96) })).mutation(({ input }) => activateReceiptKeyRotation(input.requestId, receiptSigningDescriptor())),
  }),
  ownerNotifications: router({
    refresh: ownerProcedure.mutation(() => refreshOwnerNotifications()),
    list: ownerProcedure.query(() => listOwnerNotifications()),
    update: ownerProcedure.input(z.object({ notificationKey: z.string().min(3).max(192), status: z.enum(["read", "dismissed"]) })).mutation(({ input }) => updateOwnerNotification(input.notificationKey, input.status)),
  }),
  testPlanner: router({
    templates: publicProcedure.query(() => reviewerRationaleTemplates),
    plan: publicProcedure.input(z.object({ artifactKey: z.string().min(3).max(128) })).query(async ({ input }) => {
      const record = (await listResearchArtifacts()).find((item) => item.artifactKey === input.artifactKey);
      if (!record) throw new Error("ARTIFACT_NOT_FOUND");
      return buildEvidenceTestPlan(record);
    }),
  }),
  savedViews: router({
    list: protectedProcedure.query(async ({ ctx }) => listSavedArchiveViews(ctx.user.openId)),
    save: protectedProcedure.input(z.object({ name: z.string().trim().min(1).max(64), term: z.string().max(500), category: z.enum(["all", "research_register", "falsification", "experiment", "release", "governance"]), status: z.enum(["all", "verified", "fail", "unverifiable", "unavailable"]), sort: z.enum(["updated_desc", "updated_asc", "title_asc", "category_asc", "status_asc"]) })).mutation(async ({ input, ctx }) => saveArchiveView(ctx.user.openId, input)),
    remove: protectedProcedure.input(z.object({ id: z.number().int().positive() })).mutation(async ({ input, ctx }) => removeArchiveView(ctx.user.openId, input.id)),
  }),
});

export type AppRouter = typeof appRouter;
