# Sovereign Protocol URI Specification

**Version:** 1.0  
**Status:** Normative  
**Implementation:** [`src/sovereign/legacy/sovereign_protocol.py`](../../src/sovereign/legacy/sovereign_protocol.py)

---

## 1. Overview

The Sovereign Protocol defines a URI scheme (`sov://`) for addressing every
element in the Sovereign Engine's multi-dimensional semantic space. A `sov://`
URI provides an absolute, human-readable, and cryptographically fingerprintable
address for any of the following:

| Domain | Addresses |
|---|---|
| `text` | Books, chapters, verses, words, individual letters in a sacred text corpus |
| `math` | Points in the 8-dimensional E₈ lattice |
| `space` | Points in the 3-dimensional Merkaba / quasicrystal projection space |

All URIs are:
- **Stable** — identical input data always produces the same URI.
- **Resolvable** — `SovereignProtocol.parse_uri()` maps any URI back to its structured components.
- **Fingerprintable** — `SovereignProtocol.generate_cryptographic_fingerprint()` produces a 64-character SHA-256 hex digest that can be committed to a blockchain or witness chain.

---

## 2. BNF Grammar

```
sov-uri          ::= "sov://" domain "/" domain-path

domain           ::= "text" | "math" | "space"

domain-path      ::= text-path | math-path | space-path

; ── Text domain ──────────────────────────────────────────────────
text-path        ::= language "/" corpus "/" book "/" chapter "/" verse
                     [ "/" word-segment [ "/" letter-segment ] ]

language         ::= "hebrew" | "greek" | "latin" | "aramaic"

corpus           ::= "oshb"     ; Open Scriptures Hebrew Bible
                   | "sblgnt"   ; SBL Greek New Testament (MorphGNT)
                   | "wlc"      ; Westminster Leningrad Codex
                   | "lxx"      ; Septuagint
                   | "kjv"      ; King James Version (English)
                   | corpus-id  ; Any future registered corpus

corpus-id        ::= 1*( ALPHA / DIGIT / "_" )

book             ::= 1*( ALPHA )    ; Lowercase book name, e.g. "genesis", "john"

chapter          ::= 1*DIGIT        ; 1-indexed

verse            ::= 1*DIGIT        ; 1-indexed

word-segment     ::= "w" 1*DIGIT    ; e.g. "w1", "w42"

letter-segment   ::= "l" 1*DIGIT    ; e.g. "l1", "l3"

; ── Math domain ──────────────────────────────────────────────────
math-path        ::= "e8" "/" e8-vector

e8-vector        ::= float8 *( "_" float8 )  ; exactly 8 floats separated by "_"

float8           ::= [ "-" ] 1*DIGIT [ "." 1*DIGIT ]
                   ; formatted to 1 decimal place: "1.0", "-0.5", "0.0"

; ── Space domain ─────────────────────────────────────────────────
space-path       ::= "merkaba" "/" coord3

coord3           ::= float3 "_" float3 "_" float3

float3           ::= [ "-" ] 1*DIGIT [ "." 1*DIGIT ]
                   ; formatted to 1 decimal place

ALPHA            ::= %x41-5A / %x61-7A   ; A-Z / a-z
DIGIT            ::= %x30-39             ; 0-9
```

---

## 3. Text Domain (`sov://text/`)

Addresses a linguistic element in a specific source text corpus.

### 3.1 URI Levels

| Level | Example | Identifies |
|---|---|---|
| Book-Chapter-Verse | `sov://text/hebrew/oshb/genesis/1/1` | Genesis 1:1 (all words) |
| Word | `sov://text/hebrew/oshb/genesis/1/1/w1` | First word of Genesis 1:1 |
| Letter | `sov://text/hebrew/oshb/genesis/1/1/w1/l1` | First letter of first word of Genesis 1:1 |
| Book-Chapter-Verse (Greek) | `sov://text/greek/sblgnt/john/1/1` | John 1:1 |
| Word (Greek) | `sov://text/greek/sblgnt/john/1/1/w1` | First word of John 1:1 ("ἐν") |
| Letter (Greek) | `sov://text/greek/sblgnt/john/1/1/w1/l1` | First letter of "ἐν" ("ἐ") |

### 3.2 Field Definitions

**`language`**  
Lowercase ISO-style language tag identifying the script tradition:

| Value | Script | Tradition |
|---|---|---|
| `hebrew` | Hebrew (right-to-left) | Masoretic, OSHB |
| `greek` | Greek | SBL GNT, LXX |
| `latin` | Latin | Vulgate, classical |
| `aramaic` | Aramaic (right-to-left) | Daniel 2:4–7:28, Ezra 4:8–6:18 |

**`corpus`**  
Identifies the specific text edition:

| Value | Full Name | Notes |
|---|---|---|
| `oshb` | Open Scriptures Hebrew Bible | WLC no-cantillation text, morphologically analyzed |
| `sblgnt` | SBL Greek New Testament | Via MorphGNT morphological database |
| `wlc` | Westminster Leningrad Codex | Full Masoretic text with accents |
| `lxx` | Septuagint | Greek OT |

**`book`**  
Lowercase English book name. No spaces or hyphens. Examples:

| Book | URI value |
|---|---|
| Genesis | `genesis` |
| 1 Kings | `1kings` |
| Song of Solomon | `songofsolomon` |
| John | `john` |
| 1 Corinthians | `1corinthians` |
| Revelation | `revelation` |

**`chapter`** / **`verse`**  
1-indexed integers. No leading zeros.

**`word-segment`**  
`w` followed by a 1-indexed integer. Word ordering follows the source text left-to-right
reading order (even for right-to-left Hebrew — the index is positional within the verse as
stored in the source file, not display order).

**`letter-segment`**  
`l` followed by a 1-indexed integer. Ordering follows the character order in the UTF-8
`surface` string after any corpus-specific normalization (e.g., OSHB strips cantillation
marks; MorphGNT strips punctuation). Accents are retained as part of the letter character
for Greek (e.g., `ἐ` is a single codepoint including the rough breathing mark).

### 3.3 Construction Rules (normative)

1. All path segments are lowercase.
2. `chapter` and `verse` are serialized as bare integers with no leading zeros (`1`, not `01`).
3. `word-segment` format: `w` + integer (no leading zeros). First word = `w1`.
4. `letter-segment` format: `l` + integer (no leading zeros). First letter = `l1`.
5. A verse-level URI (without `word-segment`) refers to the verse as a whole, not to any specific word.
6. A word-level URI (without `letter-segment`) refers to the whole word.

### 3.4 Canonical Examples

```
# Genesis 1:1 — entire verse
sov://text/hebrew/oshb/genesis/1/1

# Genesis 1:1 — first word (בְּרֵאשִׁית)
sov://text/hebrew/oshb/genesis/1/1/w1

# Genesis 1:1 — third letter of first word (ר)
sov://text/hebrew/oshb/genesis/1/1/w1/l3

# John 1:1 — entire verse
sov://text/greek/sblgnt/john/1/1

# John 1:1 — fifth word (λόγος)
sov://text/greek/sblgnt/john/1/1/w5

# John 1:1 — second letter of fifth word (ό)
sov://text/greek/sblgnt/john/1/1/w5/l2

# Revelation 1:8 — ninth word
sov://text/greek/sblgnt/revelation/1/8/w9

# Daniel 2:4 (Aramaic portion begins)
sov://text/aramaic/wlc/daniel/2/4/w1
```

---

## 4. Math Domain (`sov://math/`)

Addresses a point in the 8-dimensional E₈ lattice.

### 4.1 Format

```
sov://math/e8/<v0>_<v1>_<v2>_<v3>_<v4>_<v5>_<v6>_<v7>
```

Each component is a float formatted to **exactly 1 decimal place**, using `-` for
negatives. The underscore `_` is the separator (no spaces).

### 4.2 Valid E₈ Root Points

The E₈ lattice has exactly 240 roots. They fall into two families:

| Family | Coordinates | Count |
|---|---|---|
| Integer | All permutations of `(±1, ±1, 0, 0, 0, 0, 0, 0)` | 112 |
| Half-integer | `(±½, ±½, ±½, ±½, ±½, ±½, ±½, ±½)` with an **even** number of minus signs | 128 |

A `sov://math/e8/` URI **may** address any point in ℝ⁸, not only lattice roots.
Non-root points represent intermediate geometric states (e.g., a vector being
snapped toward a root, or a word-level seed vector).

### 4.3 Canonical Examples

```
# E₈ origin (not a root — represents the Singularity / zero state)
sov://math/e8/0.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0

# Integer root: (1, -1, 0, 0, 0, 0, 0, 0)
sov://math/e8/1.0_-1.0_0.0_0.0_0.0_0.0_0.0_0.0

# Half-integer root: (½, ½, ½, ½, ½, ½, ½, ½)  — all positive, 0 minus signs (even)
sov://math/e8/0.5_0.5_0.5_0.5_0.5_0.5_0.5_0.5

# Half-integer root with two minus signs (even count)
sov://math/e8/-0.5_-0.5_0.5_0.5_0.5_0.5_0.5_0.5

# Seed vector for a Hebrew word (pre-snap, not a lattice root)
sov://math/e8/0.7_-0.7_0.0_0.0_0.0_0.0_0.0_0.0
```

### 4.4 Relationship to Text URIs

Every `sov://text/...` word URI maps deterministically to a `sov://math/e8/` URI
through the following pipeline:

1. Sum the `get_letter_vec()` vectors of each letter in the word's `surface` string.
2. L2-normalize the resulting 8D vector.
3. Snap to the nearest E₈ root using Conway–Sloane CVP.
4. Serialize the snapped root as a `sov://math/e8/` URI.

This mapping is many-to-one: multiple words may share the same `sov://math/e8/` address
(they are in the same E₈ coset class).

---

## 5. Space Domain (`sov://space/`)

Addresses a point in the 3-dimensional Merkaba projection of the E₈ lattice.

### 5.1 Format

```
sov://space/merkaba/<x>_<y>_<z>
```

Each coordinate is a float formatted to **exactly 1 decimal place**.

### 5.2 Projection Basis

The Merkaba projection maps 8D E₈ vectors to 3D via the cogitation bridge's
quasicrystal geometry. The specific projection matrix is defined in
`sovereign.septivium.cognition_bridge/quasicrystal_builder.py` (`PolyglotEngine.project_to_merkaba()`).

Key properties:
- The 3D coordinates are real-valued; they are not quantized to integer positions.
- Multiple 8D vectors can project to the same 3D point (the projection is lossy).
- The origin `sov://space/merkaba/0.0_0.0_0.0` corresponds to the E₈ zero vector (Singularity).

### 5.3 Canonical Examples

```
# Singularity / origin / Throne
sov://space/merkaba/0.0_0.0_0.0

# A projected Hebrew root coordinate
sov://space/merkaba/1.4_-0.7_2.1

# A projected Greek root coordinate (half-integer E₈ family)
sov://space/merkaba/0.8_0.8_-1.2
```

---

## 6. Cryptographic Fingerprinting

Every `sov://` URI can be converted to a **64-character SHA-256 hex digest**:

```python
from sovereign.legacy.sovereign_protocol import SovereignProtocol

uri  = "sov://text/hebrew/oshb/genesis/1/1/w1"
hash = SovereignProtocol.generate_cryptographic_fingerprint(uri)
# → "a3f9...d12e"  (64-char hex, deterministic)
```

The fingerprint is:
- **Deterministic:** The same URI always produces the same digest.
- **Unique up to collision probability:** SHA-256 provides 2⁻²⁵⁶ collision probability.
- **Chain-anchored:** The `GeometricKnowledgeChain` commits these hashes as block content,
  linking every linguistic element to an immutable ledger record.

### 6.1 Fingerprint Use Cases

| Use | Mechanism |
|---|---|
| Witness proof | SHA-256 of word URI committed to block hash chain |
| Deduplication | Compare fingerprints to detect repeated concepts across corpora |
| Cross-corpus linking | Genesis "light" and John "logos" share no URI but can be linked by E₈ coordinate proximity |
| Blockchain timestamping | Submit fingerprint to Bitcoin OP_RETURN for external immutability |

---

## 7. URI Parsing

`SovereignProtocol.parse_uri(uri_string)` returns a structured dict:

### Text URI
```python
{
    "domain":   "text",
    "language": "hebrew",
    "corpus":   "oshb",
    "book":     "genesis",
    "chapter":  1,
    "verse":    1,
    "word":     "w1",      # None if no word segment
    "letter":   "l1"       # None if no letter segment
}
```

### Math URI
```python
{
    "domain":  "math",
    "lattice": "e8",
    "vector":  [1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}
```

### Space URI
```python
{
    "domain":   "space",
    "topology": "merkaba",
    "x": 1.4,
    "y": -0.7,
    "z": 2.1
}
```

---

## 8. Namespace Extensions (Reserved)

The following path structures are reserved for future domains:

| URI prefix | Planned use |
|---|---|
| `sov://chain/<height>` | Reference to a specific GeometricKnowledgeChain block |
| `sov://graph/<node_id>` | Neo4j graph node by UUID |
| `sov://tensor/<plenum_id>` | Reference to a 75D Triune Logos Plenum vector |
| `sov://audio/<e8_root_idx>` | MIDI / cymatic harmonic for a given E₈ root |
| `sov://cipher/<packet_hash>` | Lattice-encrypted packet reference |

---

## 9. Implementation Reference

| Function | Location | Description |
|---|---|---|
| `SovereignProtocol.create_text_uri()` | [`sovereign_protocol.py:11`](../../src/sovereign/legacy/sovereign_protocol.py#L11) | Constructs a text URI from language/corpus/book/chapter/verse[/word[/letter]] |
| `SovereignProtocol.create_geometric_uri()` | [`sovereign_protocol.py:23`](../../src/sovereign/legacy/sovereign_protocol.py#L23) | Constructs a `sov://math/e8/` URI from an 8D float vector |
| `SovereignProtocol.create_spatial_uri()` | [`sovereign_protocol.py:33`](../../src/sovereign/legacy/sovereign_protocol.py#L33) | Constructs a `sov://space/merkaba/` URI from x, y, z floats |
| `SovereignProtocol.parse_uri()` | [`sovereign_protocol.py:48`](../../src/sovereign/legacy/sovereign_protocol.py#L48) | Parses any `sov://` URI back to a structured dict |
| `SovereignProtocol.generate_cryptographic_fingerprint()` | [`sovereign_protocol.py:40`](../../src/sovereign/legacy/sovereign_protocol.py#L40) | SHA-256 hex digest of any URI string |
| `LivingWordParser.parse_morphgnt_book()` | [`living_word_parser.py:18`](../../src/sovereign/ingestor/living_word_parser.py#L18) | Emits word + letter URIs for Greek NT books |
| `LivingWordParser.parse_oshb_book()` | [`living_word_parser.py:85`](../../src/sovereign/ingestor/living_word_parser.py#L85) | Emits word + letter URIs for Hebrew OT books |

---

## 10. Validation Rules Summary

A conforming `sov://` URI implementation MUST:

1. Produce lowercase-only path components for all text domain segments.
2. Use `/` as the path separator and `_` as the coordinate separator within `e8-vector` and `coord3`.
3. Format all floats in `math` and `space` URIs to exactly 1 decimal place (e.g., `1.0` not `1`, `-0.5` not `-.5`).
4. Index `chapter`, `verse`, `word_index`, and `letter_index` starting at **1** (not 0).
5. Prefix word segments with `w` and letter segments with `l` (not `word_` or `letter_`).
6. Reject any URI that does not begin with `sov://`.
7. Reject any URI whose domain is not one of `text`, `math`, `space` (or a registered extension).
8. The `word-segment` MUST be present if `letter-segment` is present.
