import { index, int, mysqlEnum, mysqlTable, text, timestamp, uniqueIndex, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Durable catalogue metadata for generated evidence artifacts. The database
 * stores provenance and display metadata only; evidence bytes stay in versioned
 * artifact storage and are never duplicated into database columns.
 */
export const researchArtifacts = mysqlTable("researchArtifacts", {
  id: int("id").autoincrement().primaryKey(),
  artifactKey: varchar("artifactKey", { length: 128 }).notNull().unique(),
  title: varchar("title", { length: 255 }).notNull(),
  category: mysqlEnum("category", ["research_register", "falsification", "experiment", "release", "governance"]).notNull(),
  status: mysqlEnum("status", ["verified", "fail", "unverifiable", "unavailable"]).notNull(),
  sourceUrl: varchar("sourceUrl", { length: 1024 }).notNull(),
  contentDigest: varchar("contentDigest", { length: 128 }),
  summary: text("summary").notNull(),
  limitation: text("limitation").notNull(),
  publicationState: mysqlEnum("publicationState", ["staged", "published"]).notNull().default("published"),
  revision: int("revision").notNull().default(1),
  metadataDigest: varchar("metadataDigest", { length: 64 }),
  updatedBy: varchar("updatedBy", { length: 128 }).notNull().default("system-backfill"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, (table) => [index("researchArtifacts_category_status_idx").on(table.category, table.status)]);

export type ResearchArtifact = typeof researchArtifacts.$inferSelect;
export type InsertResearchArtifact = typeof researchArtifacts.$inferInsert;

/** Append-only metadata ledger; it records create, update, and migration backfill events. */
export const researchArtifactAudits = mysqlTable("researchArtifactAudits", {
  id: int("id").autoincrement().primaryKey(),
  artifactKey: varchar("artifactKey", { length: 128 }).notNull(),
  revision: int("revision").notNull(),
  action: mysqlEnum("action", ["create", "update", "backfill"]).notNull(),
  actorType: mysqlEnum("actorType", ["owner_token", "system_backfill"]).notNull(),
  actorLabel: varchar("actorLabel", { length: 128 }).notNull(),
  priorMetadataDigest: varchar("priorMetadataDigest", { length: 64 }),
  metadataDigest: varchar("metadataDigest", { length: 64 }).notNull(),
  recordSnapshot: text("recordSnapshot").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (table) => [index("researchArtifactAudits_artifact_created_idx").on(table.artifactKey, table.createdAt)]);

export type ResearchArtifactAudit = typeof researchArtifactAudits.$inferSelect;

/** A staged evidence record must collect independent decisions before publication. */
export const artifactPublicationRequests = mysqlTable("artifactPublicationRequests", {
  id: int("id").autoincrement().primaryKey(),
  requestKey: varchar("requestKey", { length: 160 }).notNull().unique(),
  artifactKey: varchar("artifactKey", { length: 128 }).notNull(),
  proposedRevision: int("proposedRevision").notNull(),
  recordSnapshot: text("recordSnapshot").notNull(),
  metadataDigest: varchar("metadataDigest", { length: 64 }).notNull(),
  requestedBy: varchar("requestedBy", { length: 128 }).notNull(),
  status: mysqlEnum("status", ["pending_review", "approved", "rejected", "published"]).notNull().default("pending_review"),
  requiredApprovals: int("requiredApprovals").notNull().default(2),
  approvedCount: int("approvedCount").notNull().default(0),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  publishedAt: timestamp("publishedAt"),
}, (table) => [index("publicationRequests_artifact_status_idx").on(table.artifactKey, table.status)]);

/** Append-only independent reviewer decisions; one decision per reviewer and request. */
export const artifactPublicationReviews = mysqlTable("artifactPublicationReviews", {
  id: int("id").autoincrement().primaryKey(),
  requestKey: varchar("requestKey", { length: 160 }).notNull(),
  reviewerId: varchar("reviewerId", { length: 128 }).notNull(),
  decision: mysqlEnum("decision", ["approve", "reject"]).notNull(),
  rationaleTemplateKey: varchar("rationaleTemplateKey", { length: 64 }),
  rationale: text("rationale").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (table) => [uniqueIndex("publicationReviews_request_reviewer_unique").on(table.requestKey, table.reviewerId), index("publicationReviews_request_idx").on(table.requestKey)]);

export type ArtifactPublicationRequest = typeof artifactPublicationRequests.$inferSelect;
export type ArtifactPublicationReview = typeof artifactPublicationReviews.$inferSelect;

/** Managed reviewer permissions. Tokens identify reviewers; this ledger governs whether and how they may decide. */
export const reviewerMemberships = mysqlTable("reviewerMemberships", {
  id: int("id").autoincrement().primaryKey(),
  reviewerId: varchar("reviewerId", { length: 128 }).notNull().unique(),
  displayName: varchar("displayName", { length: 128 }).notNull(),
  role: mysqlEnum("role", ["reviewer", "lead_reviewer", "observer"]).notNull().default("reviewer"),
  status: mysqlEnum("status", ["active", "suspended"]).notNull().default("active"),
  managedBy: varchar("managedBy", { length: 128 }).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, (table) => [index("reviewerMemberships_status_role_idx").on(table.status, table.role)]);

export type ReviewerMembership = typeof reviewerMemberships.$inferSelect;

/** Invitations guide prospective reviewers through onboarding. They are not credentials and cannot activate a reviewer without a configured reviewer identity accepting them. */
export const reviewerInvitations = mysqlTable("reviewerInvitations", {
  id: int("id").autoincrement().primaryKey(),
  invitationId: varchar("invitationId", { length: 96 }).notNull().unique(),
  proposedReviewerId: varchar("proposedReviewerId", { length: 128 }).notNull(),
  displayName: varchar("displayName", { length: 128 }).notNull(),
  role: mysqlEnum("role", ["reviewer", "lead_reviewer", "observer"]).notNull().default("reviewer"),
  requestedScope: mysqlEnum("requestedScope", ["general", "semantics", "implementation"]).notNull().default("general"),
  status: mysqlEnum("status", ["pending", "accepted", "revoked", "expired"]).notNull().default("pending"),
  invitationNote: text("invitationNote").notNull(),
  createdBy: varchar("createdBy", { length: 128 }).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  expiresAt: timestamp("expiresAt").notNull(),
  acceptedAt: timestamp("acceptedAt"),
  revokedAt: timestamp("revokedAt"),
}, (table) => [
  index("reviewerInvitations_status_expiry_idx").on(table.status, table.expiresAt),
  index("reviewerInvitations_reviewer_status_idx").on(table.proposedReviewerId, table.status),
]);

export type ReviewerInvitation = typeof reviewerInvitations.$inferSelect;

/** Immutable audit metadata for owner-triggered CSV exports of invitations nearing the declared reminder window. */
export const reviewerInvitationExportReceipts = mysqlTable("reviewerInvitationExportReceipts", {
  id: int("id").autoincrement().primaryKey(),
  receiptId: varchar("receiptId", { length: 96 }).notNull().unique(),
  accountOpenId: varchar("accountOpenId", { length: 96 }).notNull(),
  format: mysqlEnum("format", ["csv"]).notNull().default("csv"),
  reminderWindowHours: int("reminderWindowHours").notNull(),
  recordCount: int("recordCount").notNull(),
  resultDigest: varchar("resultDigest", { length: 64 }).notNull(),
  resultManifest: text("resultManifest").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (table) => [index("reviewerInvitationExportReceipts_account_created_idx").on(table.accountOpenId, table.createdAt)]);

export type ReviewerInvitationExportReceipt = typeof reviewerInvitationExportReceipts.$inferSelect;

/** External candidate review assignments are scope-specific. Assignment does not itself prove independence; each reviewer must attest and submit a scoped decision. */
export const externalAdapterReviewAssignments = mysqlTable("externalAdapterReviewAssignments", {
  id: int("id").autoincrement().primaryKey(),
  assignmentId: varchar("assignmentId", { length: 96 }).notNull().unique(),
  candidateId: varchar("candidateId", { length: 160 }).notNull(),
  candidateVersion: varchar("candidateVersion", { length: 64 }).notNull(),
  scope: mysqlEnum("scope", ["semantics", "implementation"]).notNull(),
  reviewerId: varchar("reviewerId", { length: 128 }).notNull(),
  status: mysqlEnum("status", ["pending", "approved", "blocked", "withdrawn"]).notNull().default("pending"),
  sourceCommit: varchar("sourceCommit", { length: 64 }).notNull(),
  evidenceUrl: varchar("evidenceUrl", { length: 1024 }),
  independenceAttestation: text("independenceAttestation"),
  rationale: text("rationale"),
  assignedBy: varchar("assignedBy", { length: 128 }).notNull(),
  assignedAt: timestamp("assignedAt").defaultNow().notNull(),
  decidedAt: timestamp("decidedAt"),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, (table) => [
  uniqueIndex("externalAdapterReview_candidate_scope_unique").on(table.candidateId, table.candidateVersion, table.scope),
  uniqueIndex("externalAdapterReview_candidate_reviewer_unique").on(table.candidateId, table.candidateVersion, table.reviewerId),
  index("externalAdapterReview_reviewer_status_idx").on(table.reviewerId, table.status),
]);

export type ExternalAdapterReviewAssignment = typeof externalAdapterReviewAssignments.$inferSelect;

/** Immutable action history for candidate-review assignment and decision events. */
export const externalAdapterReviewEvents = mysqlTable("externalAdapterReviewEvents", {
  id: int("id").autoincrement().primaryKey(),
  eventId: varchar("eventId", { length: 96 }).notNull().unique(),
  assignmentId: varchar("assignmentId", { length: 96 }).notNull(),
  action: mysqlEnum("action", ["assigned", "reassigned", "decision", "withdrawn"]).notNull(),
  actorId: varchar("actorId", { length: 128 }).notNull(),
  snapshot: text("snapshot").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (table) => [index("externalAdapterReviewEvents_assignment_created_idx").on(table.assignmentId, table.createdAt)]);

export type ExternalAdapterReviewEvent = typeof externalAdapterReviewEvents.$inferSelect;

/** Immutable receipt metadata for an authenticated account's filtered metadata export. */
export const archiveExportReceipts = mysqlTable("archiveExportReceipts", {
  id: int("id").autoincrement().primaryKey(),
  receiptId: varchar("receiptId", { length: 96 }).notNull().unique(),
  accountOpenId: varchar("accountOpenId", { length: 96 }).notNull(),
  format: mysqlEnum("format", ["csv", "json"]).notNull(),
  recordCount: int("recordCount").notNull(),
  filtersSnapshot: text("filtersSnapshot").notNull(),
  resultDigest: varchar("resultDigest", { length: 64 }).notNull(),
  resultManifest: text("resultManifest"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (table) => [index("archiveExportReceipts_account_created_idx").on(table.accountOpenId, table.createdAt)]);

export type ArchiveExportReceipt = typeof archiveExportReceipts.$inferSelect;

/** Public verification keys observed when signing receipt bundles. Private signing material stays only in the managed secret store. */
export const receiptSigningKeys = mysqlTable("receiptSigningKeys", {
  id: int("id").autoincrement().primaryKey(),
  keyFingerprint: varchar("keyFingerprint", { length: 64 }).notNull().unique(),
  algorithm: varchar("algorithm", { length: 32 }).notNull(),
  publicKeyJwk: text("publicKeyJwk").notNull(),
  status: mysqlEnum("status", ["active", "retired", "expired"]).notNull().default("active"),
  firstSeenAt: timestamp("firstSeenAt").defaultNow().notNull(),
  lastSeenAt: timestamp("lastSeenAt").defaultNow().onUpdateNow().notNull(),
  expiresAt: timestamp("expiresAt"),
  retiredAt: timestamp("retiredAt"),
}, (table) => [index("receiptSigningKeys_status_seen_idx").on(table.status, table.lastSeenAt)]);

export type ReceiptSigningKeyRecord = typeof receiptSigningKeys.$inferSelect;

/** An owner must explicitly approve a candidate public key before its matching managed private key may be activated. */
export const receiptKeyRotationRequests = mysqlTable("receiptKeyRotationRequests", {
  id: int("id").autoincrement().primaryKey(),
  requestId: varchar("requestId", { length: 96 }).notNull().unique(),
  keyFingerprint: varchar("keyFingerprint", { length: 64 }).notNull(),
  algorithm: varchar("algorithm", { length: 32 }).notNull(),
  publicKeyJwk: text("publicKeyJwk").notNull(),
  requestedExpiryAt: timestamp("requestedExpiryAt").notNull(),
  rationale: text("rationale").notNull(),
  status: mysqlEnum("status", ["pending", "approved", "activated", "cancelled", "expired"]).notNull().default("pending"),
  requestedBy: varchar("requestedBy", { length: 128 }).notNull(),
  approvedBy: varchar("approvedBy", { length: 128 }),
  approvedAt: timestamp("approvedAt"),
  activatedAt: timestamp("activatedAt"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, (table) => [index("receiptKeyRotation_status_expiry_idx").on(table.status, table.requestedExpiryAt)]);

export type ReceiptKeyRotationRequest = typeof receiptKeyRotationRequests.$inferSelect;

/** Immutable signature events bind an export receipt snapshot to a concrete retained public signing key. */
export const receiptBundleSignatures = mysqlTable("receiptBundleSignatures", {
  id: int("id").autoincrement().primaryKey(),
  signatureId: varchar("signatureId", { length: 96 }).notNull().unique(),
  receiptId: varchar("receiptId", { length: 96 }).notNull(),
  keyFingerprint: varchar("keyFingerprint", { length: 64 }).notNull(),
  payloadDigest: varchar("payloadDigest", { length: 64 }).notNull(),
  bundleStorageKey: varchar("bundleStorageKey", { length: 512 }),
  bundleStorageUrl: varchar("bundleStorageUrl", { length: 1024 }),
  bundleDigest: varchar("bundleDigest", { length: 64 }),
  signedAt: timestamp("signedAt").defaultNow().notNull(),
}, (table) => [index("receiptBundleSignatures_receipt_signed_idx").on(table.receiptId, table.signedAt)]);

export type ReceiptBundleSignature = typeof receiptBundleSignatures.$inferSelect;

/** Owner-scoped operational notifications. Delivery is manually refreshed; no background schedule is implied. */
export const ownerNotifications = mysqlTable("ownerNotifications", {
  id: int("id").autoincrement().primaryKey(),
  notificationKey: varchar("notificationKey", { length: 192 }).notNull().unique(),
  category: mysqlEnum("category", ["quorum_risk", "key_expiry"]).notNull(),
  severity: mysqlEnum("severity", ["warning", "critical"]).notNull(),
  title: varchar("title", { length: 255 }).notNull(),
  message: text("message").notNull(),
  targetRef: varchar("targetRef", { length: 192 }).notNull(),
  status: mysqlEnum("status", ["unread", "read", "dismissed"]).notNull().default("unread"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  readAt: timestamp("readAt"),
}, (table) => [index("ownerNotifications_status_created_idx").on(table.status, table.createdAt)]);

export type OwnerNotification = typeof ownerNotifications.$inferSelect;

/** Signed-session-owned archive presets; preferences are separate from evidence records. */
export const savedArchiveViews = mysqlTable("savedArchiveViews", {
  id: int("id").autoincrement().primaryKey(),
  ownerSubject: varchar("ownerSubject", { length: 96 }).notNull(),
  name: varchar("name", { length: 64 }).notNull(),
  term: text("term").notNull(),
  category: varchar("category", { length: 32 }).notNull(),
  status: varchar("status", { length: 32 }).notNull(),
  sort: varchar("sort", { length: 32 }).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, (table) => [index("savedArchiveViews_owner_updated_idx").on(table.ownerSubject, table.updatedAt)]);

export type SavedArchiveViewRecord = typeof savedArchiveViews.$inferSelect;

/** Governed source-byte intake. Raw corpus bytes remain in managed object storage. */
export const corpusSourceIntakes = mysqlTable("corpusSourceIntakes", {
  id: int("id").autoincrement().primaryKey(),
  intakeId: varchar("intakeId", { length: 96 }).notNull().unique(),
  sourceRole: mysqlEnum("sourceRole", ["genesis_oshb", "john_sblgnt"]).notNull(),
  originalFilename: varchar("originalFilename", { length: 255 }).notNull(),
  storageKey: varchar("storageKey", { length: 512 }).notNull().unique(),
  storageUrl: varchar("storageUrl", { length: 1024 }).notNull(),
  sha256: varchar("sha256", { length: 64 }).notNull(),
  byteLength: int("byteLength").notNull(),
  validationStatus: mysqlEnum("validationStatus", ["accepted"]).notNull().default("accepted"),
  validationReport: text("validationReport").notNull(),
  uploadedBy: varchar("uploadedBy", { length: 128 }).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (table) => [index("corpusSourceIntakes_role_created_idx").on(table.sourceRole, table.createdAt), index("corpusSourceIntakes_sha256_idx").on(table.sha256)]);

export type CorpusSourceIntake = typeof corpusSourceIntakes.$inferSelect;
