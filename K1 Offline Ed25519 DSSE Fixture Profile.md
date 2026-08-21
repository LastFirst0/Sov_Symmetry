# K1 Offline Ed25519 DSSE Fixture Profile

**Status:** Contract draft; no production key custody or network key discovery.  
**Purpose:** Replace the Q0 HMAC-only fixture binding with deterministic offline public-key test vectors after K1 fixture inputs are frozen.

| Field | Rule |
|---|---|
| Payload type | `application/vnd.sovereign.quorum.response.v1+json` only |
| DSSE PAE | Exact DSSE PAE over payload type and canonical UTF-8 payload bytes |
| Algorithm | `ed25519` only; no algorithm negotiation |
| Key policy | Policy names a stable `key_id`, node ID, public key bytes, `active`/`revoked` state, and profile version |
| Accepted signature count | Exactly one policy-listed active key per response |
| Offline fixtures | Deterministic published test keys only; never operational or user keys |
| Rejections | Unknown key, revoked key, wrong algorithm, malformed base64, invalid signature, payload-type mutation, or request/policy-binding mutation must be preserved as rejection evidence |

This profile establishes only exact offline verification behavior. It does not establish HSM custody, rotation service availability, remote discovery, transparency replication, consensus, or key-compromise response operations.
