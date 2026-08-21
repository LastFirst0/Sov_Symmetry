import { createHash, generateKeyPairSync } from "node:crypto";
import { writeFileSync } from "node:fs";
import { ENV } from "../server/_core/env.ts";
import { appRouter } from "../server/routers.ts";

if (!ENV.ownerOpenId) throw new Error("ROTATION_OWNER_UNAVAILABLE");

const now = new Date();
const owner = {
  id: 0,
  openId: ENV.ownerOpenId,
  name: process.env.OWNER_NAME || "project-owner",
  email: null,
  loginMethod: "rotation-maintenance",
  role: "admin",
  createdAt: now,
  updatedAt: now,
  lastSignedIn: now,
};
const { privateKey, publicKey } = generateKeyPairSync("ed25519");
const publicKeyJwk = publicKey.export({ format: "jwk" });
if (publicKeyJwk.kty !== "OKP" || publicKeyJwk.crv !== "Ed25519" || !publicKeyJwk.x) throw new Error("ROTATION_SUCCESSOR_PUBLIC_KEY_INVALID");
const keyFingerprint = createHash("sha256").update(JSON.stringify({ kty: publicKeyJwk.kty, crv: publicKeyJwk.crv, x: publicKeyJwk.x })).digest("hex");
const privateKeyPath = "/home/ubuntu/rotation_successor_2026-08-19.pem";
writeFileSync(privateKeyPath, privateKey.export({ format: "pem", type: "pkcs8" }), { encoding: "utf8", mode: 0o600 });

const caller = appRouter.createCaller({ user: owner, ingestionAuthorized: true, reviewerId: null });
const expiresAt = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000);
const request = await caller.keyLifecycle.request({ publicKeyJwk, expiresAt, rationale: "Controlled continuity replay: retain a pre-rotation bundle, activate an approved successor, retain a post-rotation bundle, and verify both signatures with retained public material." });
const approved = await caller.keyLifecycle.approve({ requestId: request.requestId });

console.log(JSON.stringify({ requestId: approved.requestId, keyFingerprint, publicKeyJwk, expiresAt: approved.requestedExpiryAt, status: approved.status, privateKeyPath }, null, 2));
setImmediate(() => process.exit(0));
