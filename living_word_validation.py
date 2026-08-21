"""Pure source-schema validation for governed Living Word corpus intake.

This module validates declared text-source structure only.  It does not make
semantic, historical, theological, clinical, or empirical claims about a corpus.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from typing import Any, Literal, Mapping, Sequence

CorpusRole = Literal["genesis_oshb", "john_sblgnt"]

_RULES: dict[CorpusRole, dict[str, Any]] = {
    "genesis_oshb": {"language": "hebrew", "book": "genesis", "min_words": 8_086},
    "john_sblgnt": {"language": "greek", "book": "john", "min_words": 15_438},
}
_WORD_URI = re.compile(r"^sov://text/(hebrew|greek)/[a-z]+/[a-z]+/\d+/\d+/w\d+$")
_LETTER_URI = re.compile(r"^sov://text/(hebrew|greek)/[a-z]+/[a-z]+/\d+/\d+/w\d+/l\d+$")


class LivingWordValidationError(ValueError):
    """A fail-closed machine-readable rejection of a supplied corpus source."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        super().__init__(f"{code}: {detail}")


@dataclass(frozen=True)
class LivingWordValidationReport:
    source_role: CorpusRole
    sha256: str
    word_count: int
    validator: str = "living-word-source.v1"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_upload_metadata(*, source_role: object, filename: object, byte_length: object, max_bytes: int = 25 * 1024 * 1024) -> CorpusRole:
    """Validate pre-storage intake metadata before parsing a source payload."""
    if source_role not in _RULES:
        raise LivingWordValidationError("E_CORPUS_ROLE_UNSUPPORTED", "source_role must be genesis_oshb or john_sblgnt")
    if not isinstance(filename, str) or not filename or "/" in filename or "\\" in filename or not filename.endswith(".json"):
        raise LivingWordValidationError("E_CORPUS_FILENAME_INVALID", "filename must be a plain non-empty .json basename")
    if not isinstance(byte_length, int) or isinstance(byte_length, bool) or byte_length <= 0 or byte_length > max_bytes:
        raise LivingWordValidationError("E_CORPUS_SIZE_INVALID", "payload byte length is empty, invalid, or exceeds intake limit")
    required_stem = "Genesis_OSHB" if source_role == "genesis_oshb" else "John_SBLGNT"
    if filename != f"{required_stem}.json":
        raise LivingWordValidationError("E_CORPUS_ROLE_FILENAME_MISMATCH", "filename does not match declared source role")
    return source_role


def validate_living_word_bytes(source_role: CorpusRole, raw_bytes: bytes) -> LivingWordValidationReport:
    """Validate JSON bytes with the same structural boundary as the legacy suite."""
    if source_role not in _RULES:
        raise LivingWordValidationError("E_CORPUS_ROLE_UNSUPPORTED", "unknown source role")
    try:
        parsed = json.loads(raw_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LivingWordValidationError("E_CORPUS_JSON_INVALID", "payload is not UTF-8 JSON") from exc
    return validate_living_word_sequence(source_role, parsed, sha256=hashlib.sha256(raw_bytes).hexdigest())


def validate_living_word_sequence(source_role: CorpusRole, sequence: object, *, sha256: str = "0" * 64) -> LivingWordValidationReport:
    """Validate a decoded corpus sequence; intended for both upload and unit tests."""
    if source_role not in _RULES:
        raise LivingWordValidationError("E_CORPUS_ROLE_UNSUPPORTED", "unknown source role")
    rule = _RULES[source_role]
    if not isinstance(sequence, list):
        raise LivingWordValidationError("E_CORPUS_TOP_LEVEL_INVALID", "top-level JSON value must be an array")
    if len(sequence) < rule["min_words"]:
        raise LivingWordValidationError("E_CORPUS_WORD_COUNT", f"expected at least {rule['min_words']} words")

    for index, word in enumerate(sequence):
        _validate_word(word, index, rule["language"])
    return LivingWordValidationReport(source_role=source_role, sha256=sha256, word_count=len(sequence))


def _validate_word(word: object, index: int, language: str) -> None:
    if not isinstance(word, Mapping):
        raise LivingWordValidationError("E_CORPUS_WORD_SCHEMA", f"record {index} is not an object")
    required = ("word_uri", "surface", "chapter", "verse", "word_index", "letters")
    if any(field not in word for field in required):
        raise LivingWordValidationError("E_CORPUS_WORD_SCHEMA", f"record {index} misses a required field")
    uri, surface, letters = word["word_uri"], word["surface"], word["letters"]
    if not isinstance(uri, str) or not _WORD_URI.fullmatch(uri) or f"/{language}/" not in uri:
        raise LivingWordValidationError("E_CORPUS_WORD_URI_INVALID", f"record {index} has invalid word_uri")
    if not isinstance(surface, str) or not surface:
        raise LivingWordValidationError("E_CORPUS_SURFACE_INVALID", f"record {index} has an empty or non-string surface")
    if any(not isinstance(word[field], int) or isinstance(word[field], bool) or word[field] < 1 for field in ("chapter", "verse", "word_index")):
        raise LivingWordValidationError("E_CORPUS_COORDINATE_INVALID", f"record {index} has invalid chapter, verse, or word_index")
    uri_parts = uri.split("/")
    if int(uri_parts[6]) != word["chapter"] or int(uri_parts[7]) != word["verse"]:
        raise LivingWordValidationError("E_CORPUS_URI_COORDINATE_MISMATCH", f"record {index} URI and declared coordinates differ")
    if not isinstance(letters, list) or not letters:
        raise LivingWordValidationError("E_CORPUS_LETTERS_INVALID", f"record {index} must declare one or more letters")
    for letter_index, letter in enumerate(letters):
        if not isinstance(letter, Mapping) or "letter_uri" not in letter or "char" not in letter:
            raise LivingWordValidationError("E_CORPUS_LETTER_SCHEMA", f"record {index} letter {letter_index} is incomplete")
        letter_uri, character = letter["letter_uri"], letter["char"]
        if not isinstance(letter_uri, str) or not _LETTER_URI.fullmatch(letter_uri):
            raise LivingWordValidationError("E_CORPUS_LETTER_URI_INVALID", f"record {index} letter {letter_index} has invalid URI")
        if not isinstance(character, str) or len(character) != 1:
            raise LivingWordValidationError("E_CORPUS_LETTER_CHAR_INVALID", f"record {index} letter {letter_index} must be one character")
    if len(surface) != len(letters):
        raise LivingWordValidationError("E_CORPUS_SURFACE_LETTER_MISMATCH", f"record {index} surface and letter count differ")
