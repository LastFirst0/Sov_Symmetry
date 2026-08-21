# File: adapters/python/register_artifact.py
# Purpose: Full adapter flow: canonicalize payload, hash, sign (via KMS), insert Postgres, upsert embedding, create Neo4j provenance, optionally anchor on-chain.
# Requires: psycopg2-binary, neo4j, requests, cryptography (or KMS SDK), pgvector client, embedding model client

import os
import json
import hashlib
import base64
import requests
import psycopg2
from neo4j import GraphDatabase
from typing import Dict, Any
from datetime import datetime
from pgvector.psycopg2 import register_vector

# Config from env
PG_DSN = os.getenv("PG_DSN", "postgresql://postgres:postgres@localhost:5432/postgres")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "test")
EMBEDDING_SERVICE = os.getenv("EMBEDDING_SERVICE", "http://localhost:8000/embed")
KMS_SIGN_ENDPOINT = os.getenv("KMS_SIGN_ENDPOINT", "http://localhost:9000/sign")  # signs hex hash

def canonical_serialize(payload: Dict[str, Any], format_hint: str) -> bytes:
    """
    Deterministic canonical serialization.
    - For protobuf: caller should pass pre-serialized bytes.
    - For JSON: apply canonical JSON (sorted keys, normalized numbers).
    """
    if format_hint.startswith("protobuf"):
        # payload is expected to be bytes
        if isinstance(payload, bytes):
            return payload
        raise ValueError("Protobuf payload must be bytes for canonicalization")
    # JSON canonicalization
    def normalize(obj):
        if isinstance(obj, dict):
            return {k: normalize(obj[k]) for k in sorted(obj.keys())}
        if isinstance(obj, list):
            return [normalize(x) for x in obj]
        if isinstance(obj, float):
            # minimal decimal representation
            return float("{:.12g}".format(obj))
        return obj
    normalized = normalize(payload)
    return json.dumps(normalized, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def compute_hash(canonical_bytes: bytes, algo: str = "sha3_256") -> str:
    if algo.lower() in ("sha3-256", "sha3_256", "sha3"):
        h = hashlib.sha3_256(canonical_bytes).hexdigest()
    else:
        # fallback to sha256
        h = hashlib.sha256(canonical_bytes).hexdigest()
    return h

def sign_hash_with_kms(hex_hash: str, signer_key_id: str) -> bytes:
    # Example: call KMS to sign; KMS returns base64 signature
    resp = requests.post(KMS_SIGN_ENDPOINT, json={"hash": hex_hash, "key_id": signer_key_id})
    resp.raise_for_status()
    sig_b64 = resp.json().get("signature")
    return base64.b64decode(sig_b64)

def generate_embedding(payload: Dict[str, Any]) -> list:
    resp = requests.post(EMBEDDING_SERVICE, json={"payload": payload})
    resp.raise_for_status()
    return resp.json()["vector"]

def upsert_artifact(conn, artifact: Dict[str, Any], signature: bytes, signer_key_id: str):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO artifact (id, artifact_type, name, version, origin_module, payload_uri, payload_hash, payload_hash_algo, canonical_format, signature, signer_key_id, zone, tags, metadata, created_by)
            VALUES (gen_random_uuid(), %(artifact_type)s, %(name)s, %(version)s, %(origin_module)s, %(payload_uri)s, %(payload_hash)s, %(payload_hash_algo)s, %(canonical_format)s, %(signature)s, %(signer_key_id)s, %(zone)s, %(tags)s, %(metadata)s, %(created_by)s)
            RETURNING id
        """, {
            "artifact_type": artifact["artifact_type"],
            "name": artifact["name"],
            "version": artifact.get("version", "0.0.0"),
            "origin_module": artifact.get("origin_module", "unknown"),
            "payload_uri": artifact.get("payload_uri"),
            "payload_hash": artifact["payload_hash"],
            "payload_hash_algo": artifact.get("payload_hash_algo", "SHA3-256"),
            "canonical_format": artifact["canonical_format"],
            "signature": signature,
            "signer_key_id": signer_key_id,
            "zone": artifact.get("zone", "experimental"),
            "tags": artifact.get("tags", []),
            "metadata": json.dumps(artifact.get("metadata", {})),
            "created_by": artifact.get("created_by", "system")
        })
        row = cur.fetchone()
        return row[0]

def create_provenance_neo4j(driver, artifact_id: str, actor: str, action: str, module: str, details: Dict[str, Any]):
    with driver.session() as session:
        session.run("""
            MERGE (a:Artifact {id: $artifact_id})
            MERGE (p:Person {id: $actor})
            CREATE (p)-[:PERFORMED {action:$action, module:$module, details:$details, at:datetime()}]->(a)
        """, artifact_id=artifact_id, actor=actor, action=action, module=module, details=details)

def register_artifact_flow(payload: Dict[str, Any], format_hint: str, signer_key_id: str):
    canonical = canonical_serialize(payload, format_hint)
    payload_hash = compute_hash(canonical, algo="sha3_256")
    signature = sign_hash_with_kms(payload_hash, signer_key_id)
    # Insert artifact and embedding
    conn = psycopg2.connect(PG_DSN)
    register_vector(conn)  # pgvector adapter
    try:
        artifact_meta = {
            "artifact_type": payload.get("artifact_type", "unknown"),
            "name": payload.get("name", "unnamed"),
            "version": payload.get("version", "0.0.0"),
            "origin_module": payload.get("origin_module", "unknown"),
            "payload_uri": payload.get("payload_uri"),
            "payload_hash": payload_hash,
            "payload_hash_algo": "SHA3-256",
            "canonical_format": format_hint,
            "zone": payload.get("zone", "experimental"),
            "tags": payload.get("tags", []),
            "metadata": payload.get("metadata", {}),
            "created_by": payload.get("created_by", "system")
        }
        with conn:
            artifact_id = upsert_artifact(conn, artifact_meta, signature, signer_key_id)
            # embedding
            vector = generate_embedding(payload)
            with conn.cursor() as cur:
                cur.execute("INSERT INTO embedding (artifact_id, vector, model_name, metadata) VALUES (%s, %s, %s, %s) ON CONFLICT (artifact_id) DO UPDATE SET vector = EXCLUDED.vector", (artifact_id, vector, "open-embed-1536", json.dumps({})))
    finally:
        conn.close()
    # Neo4j provenance
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    create_provenance_neo4j(driver, artifact_id, actor=payload.get("created_by", "system"), action="create", module=payload.get("origin_module", "unknown"), details={"payload_hash": payload_hash})
    driver.close()
    return {"artifact_id": artifact_id, "payload_hash": payload_hash}
