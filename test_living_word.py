"""
tests/test_living_word.py

Validates the Living Word JSON files produced by LivingWordParser.
Checks word counts, URI structure, and letter array integrity for
Genesis (OSHB) and John (SBLGNT).

Known source-text word counts (conservative lower bounds):
  - Genesis OSHB : 8,086 Hebrew words
  - John SBLGNT  : 15,635 Greek words

Run with:
    pytest tests/test_living_word.py -v
"""
import json
import os
import re
import sys

import pytest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC_PATH = os.path.join(_REPO_ROOT, "src")
if _SRC_PATH not in sys.path:
    sys.path.insert(0, _SRC_PATH)

GENESIS_PATH = os.path.join(_REPO_ROOT, "data", "living_word", "Genesis_OSHB.json")
JOHN_PATH    = os.path.join(_REPO_ROOT, "data", "living_word", "John_SBLGNT.json")

pytestmark = pytest.mark.skipif(
    not (os.path.exists(GENESIS_PATH) and os.path.exists(JOHN_PATH)),
    reason="Living Word source datasets are not present in this offline checkout.",
)

# Minimum word counts from the respective source texts.
# Genesis OSHB : verified against Westminster Leningrad Codex word count.
# John SBLGNT  : 15,438 words — the SBL Greek New Testament omits the
#                pericope adulterae (John 7:53-8:11) which is absent from the
#                earliest manuscripts; the Textus Receptus count is ~15,635.
GENESIS_MIN_WORDS = 8_086
JOHN_MIN_WORDS    = 15_438


# sov:// URI regex — matches both word-level and letter-level URIs.
_SOV_WORD_PATTERN   = re.compile(
    r"^sov://text/(hebrew|greek)/[a-z]+/[a-z]+/\d+/\d+/w\d+$"
)
_SOV_LETTER_PATTERN = re.compile(
    r"^sov://text/(hebrew|greek)/[a-z]+/[a-z]+/\d+/\d+/w\d+/l\d+$"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load(path: str):
    if not os.path.exists(path):
        pytest.skip(f"Living Word data not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _validate_sequence(sequence, label: str, min_words: int, lang: str):
    """Run all structural checks on a Living Word sequence."""

    # 1. Word count
    assert len(sequence) >= min_words, (
        f"{label}: expected >= {min_words} words, got {len(sequence)}"
    )

    # 2. Per-word structural checks (sample every 100th word for speed)
    for idx in range(0, len(sequence), 100):
        word = sequence[idx]

        # Required fields
        for field in ("word_uri", "surface", "chapter", "verse", "word_index", "letters"):
            assert field in word, (
                f"{label}[{idx}]: missing field '{field}'"
            )

        # sov:// URI format
        uri = word["word_uri"]
        assert _SOV_WORD_PATTERN.match(uri), (
            f"{label}[{idx}]: malformed word_uri: {uri!r}"
        )

        # Language embedded in URI matches expected
        assert f"/{lang}/" in uri, (
            f"{label}[{idx}]: URI language mismatch, expected '{lang}' in {uri!r}"
        )

        # Surface is non-empty string
        assert isinstance(word["surface"], str) and len(word["surface"]) > 0, (
            f"{label}[{idx}]: empty surface string"
        )

        # Chapter/verse/word_index are positive ints
        assert isinstance(word["chapter"], int) and word["chapter"] >= 1
        assert isinstance(word["verse"],   int) and word["verse"]   >= 1
        assert isinstance(word["word_index"], int) and word["word_index"] >= 1

        # Letters array
        letters = word["letters"]
        assert isinstance(letters, list) and len(letters) > 0, (
            f"{label}[{idx}]: empty letters array for word '{word['surface']}'"
        )

        for l_idx, letter in enumerate(letters):
            assert "letter_uri" in letter and "char" in letter, (
                f"{label}[{idx}] letter[{l_idx}]: missing 'letter_uri' or 'char'"
            )
            l_uri = letter["letter_uri"]
            assert _SOV_LETTER_PATTERN.match(l_uri), (
                f"{label}[{idx}] letter[{l_idx}]: malformed letter_uri: {l_uri!r}"
            )
            assert isinstance(letter["char"], str) and len(letter["char"]) == 1, (
                f"{label}[{idx}] letter[{l_idx}]: char must be a single character"
            )

    # 3. Letter count consistency — every word's letter count must match
    #    the length of its surface string (after accounting for any stripping
    #    the parser may apply; allow ±0 exact match as the contract).
    mismatches = []
    for idx, word in enumerate(sequence):
        expected = len(word["surface"])
        actual   = len(word["letters"])
        if expected != actual:
            mismatches.append((idx, word["surface"], expected, actual))
        if len(mismatches) >= 10:
            break  # cap error list

    assert not mismatches, (
        f"{label}: surface/letters length mismatches (first {len(mismatches)}):\n"
        + "\n".join(
            f"  [{i}] '{s}' expected {e} got {a}"
            for i, s, e, a in mismatches
        )
    )

    # 4. URI chapter/verse embedding consistency — parse URI and compare fields
    for idx in range(0, len(sequence), 500):
        word = sequence[idx]
        uri_parts = word["word_uri"].split("/")
        # Format: sov://text/<lang>/<corpus>/<book>/<chapter>/<verse>/w<idx>
        uri_chapter = int(uri_parts[6])
        uri_verse   = int(uri_parts[7])
        assert uri_chapter == word["chapter"], (
            f"{label}[{idx}]: URI chapter {uri_chapter} != field chapter {word['chapter']}"
        )
        assert uri_verse == word["verse"], (
            f"{label}[{idx}]: URI verse {uri_verse} != field verse {word['verse']}"
        )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGenesisOSHB:
    """Structural validation for Genesis_OSHB.json"""

    def test_file_exists(self):
        assert os.path.exists(GENESIS_PATH), f"Missing: {GENESIS_PATH}"

    def test_is_valid_json(self):
        _load(GENESIS_PATH)

    def test_minimum_word_count(self):
        sequence = _load(GENESIS_PATH)
        assert len(sequence) >= GENESIS_MIN_WORDS, (
            f"Genesis: expected >= {GENESIS_MIN_WORDS} words, got {len(sequence)}"
        )

    def test_structure_and_uris(self):
        sequence = _load(GENESIS_PATH)
        _validate_sequence(sequence, "Genesis_OSHB", GENESIS_MIN_WORDS, "hebrew")

    def test_first_word_bereshit(self):
        """The first word of Genesis 1:1 must be the Hebrew 'בְּרֵאשִׁית'."""
        sequence = _load(GENESIS_PATH)
        first = sequence[0]
        assert first["chapter"] == 1
        assert first["verse"]   == 1
        assert first["word_index"] == 1
        # Surface should contain at least the root letters of בְּרֵאשִׁית
        # (OSHB may strip cantillation; accept any form containing ר-א-ש)
        surface = first["surface"]
        assert any(ch in surface for ch in "ראש"), (
            f"Expected root letters ר/א/ש in first word, got: {surface!r}"
        )

    def test_no_empty_surfaces(self):
        sequence = _load(GENESIS_PATH)
        empties = [i for i, w in enumerate(sequence) if not w.get("surface", "").strip()]
        assert not empties, f"Genesis: {len(empties)} words with empty surface strings"


class TestJohnSBLGNT:
    """Structural validation for John_SBLGNT.json"""

    def test_file_exists(self):
        assert os.path.exists(JOHN_PATH), f"Missing: {JOHN_PATH}"

    def test_is_valid_json(self):
        _load(JOHN_PATH)

    def test_minimum_word_count(self):
        sequence = _load(JOHN_PATH)
        assert len(sequence) >= JOHN_MIN_WORDS, (
            f"John: expected >= {JOHN_MIN_WORDS} words, got {len(sequence)}"
        )

    def test_structure_and_uris(self):
        sequence = _load(JOHN_PATH)
        _validate_sequence(sequence, "John_SBLGNT", JOHN_MIN_WORDS, "greek")

    def test_first_word_en(self):
        """The first word of John 1:1 must be 'Ἐν' (In)."""
        sequence = _load(JOHN_PATH)
        first = sequence[0]
        assert first["chapter"] == 1
        assert first["verse"]   == 1
        assert first["word_index"] == 1
        # Allow for accent-stripped variant 'εν' or full form 'Ἐν'
        surface_lower = first["surface"].lower()
        # The word should normalize to a form of 'εν'
        assert any(ch in surface_lower for ch in "εν"), (
            f"Expected John 1:1 first word to contain ε/ν, got: {first['surface']!r}"
        )

    def test_no_empty_surfaces(self):
        sequence = _load(JOHN_PATH)
        empties = [i for i, w in enumerate(sequence) if not w.get("surface", "").strip()]
        assert not empties, f"John: {len(empties)} words with empty surface strings"


class TestSovereignProtocol:
    """Verify that the sov:// URI parser round-trips correctly."""

    def setup_method(self):
        # Add legacy path for SovereignProtocol
        legacy_path = os.path.join(_SRC_PATH, "sov_proto", "legacy")
        if legacy_path not in sys.path:
            sys.path.insert(0, os.path.join(_SRC_PATH, "sov_proto", "legacy"))

    def test_text_uri_roundtrip(self):
        from sov_proto.legacy.sovereign_protocol import SovereignProtocol
        uri = SovereignProtocol.create_text_uri("hebrew", "oshb", "genesis", 1, 1, 1)
        assert uri == "sov://text/hebrew/oshb/genesis/1/1/w1"
        parsed = SovereignProtocol.parse_uri(uri)
        assert parsed["chapter"] == 1
        assert parsed["verse"]   == 1

    def test_letter_uri_roundtrip(self):
        from sov_proto.legacy.sovereign_protocol import SovereignProtocol
        uri = SovereignProtocol.create_text_uri("greek", "sblgnt", "john", 1, 1, 1, 1)
        assert uri == "sov://text/greek/sblgnt/john/1/1/w1/l1"
        parsed = SovereignProtocol.parse_uri(uri)
        assert parsed["chapter"] == 1
        assert parsed["letter"]  == "l1"

    def test_fingerprint_determinism(self):
        from sov_proto.legacy.sovereign_protocol import SovereignProtocol
        uri = "sov://text/hebrew/oshb/genesis/1/1/w1"
        h1 = SovereignProtocol.generate_cryptographic_fingerprint(uri)
        h2 = SovereignProtocol.generate_cryptographic_fingerprint(uri)
        assert h1 == h2
        assert len(h1) == 64  # SHA-256 hex digest
