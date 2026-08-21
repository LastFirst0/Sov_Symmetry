import json

import pytest

from sov_evidence_geometry_core.living_word_validation import LivingWordValidationError, validate_living_word_bytes, validate_living_word_sequence, validate_upload_metadata


def word(*, language="hebrew", corpus="oshb", book="genesis", chapter=1, verse=1, index=1, surface="אב"):
    return {"word_uri": f"sov://text/{language}/{corpus}/{book}/{chapter}/{verse}/w{index}", "surface": surface, "chapter": chapter, "verse": verse, "word_index": index, "letters": [{"letter_uri": f"sov://text/{language}/{corpus}/{book}/{chapter}/{verse}/w{index}/l1", "char": surface[0]}, {"letter_uri": f"sov://text/{language}/{corpus}/{book}/{chapter}/{verse}/w{index}/l2", "char": surface[1]}]}


def corpus():
    return [word(index=index) for index in range(1, 8_087)]


def expect(code, sequence):
    with pytest.raises(LivingWordValidationError, match=code): validate_living_word_sequence("genesis_oshb", sequence)


def test_rejects_unknown_role():
    with pytest.raises(LivingWordValidationError, match="E_CORPUS_ROLE_UNSUPPORTED"): validate_living_word_sequence("unknown", [])  # type: ignore[arg-type]


@pytest.mark.parametrize(("filename", "byte_length", "code"), [("Genesis_OSHB.json", 0, "E_CORPUS_SIZE_INVALID"), ("../Genesis_OSHB.json", 4, "E_CORPUS_FILENAME_INVALID"), ("John_SBLGNT.json", 4, "E_CORPUS_ROLE_FILENAME_MISMATCH"), ("Genesis_OSHB.txt", 4, "E_CORPUS_FILENAME_INVALID")])
def test_rejects_bad_upload_metadata(filename, byte_length, code):
    with pytest.raises(LivingWordValidationError, match=code): validate_upload_metadata(source_role="genesis_oshb", filename=filename, byte_length=byte_length)


def test_rejects_invalid_json_bytes():
    with pytest.raises(LivingWordValidationError, match="E_CORPUS_JSON_INVALID"): validate_living_word_bytes("genesis_oshb", b"not-json")


def test_rejects_non_array_top_level(): expect("E_CORPUS_TOP_LEVEL_INVALID", {"word": "not-array"})
def test_rejects_below_word_floor(): expect("E_CORPUS_WORD_COUNT", corpus()[:-1])
def test_rejects_missing_required_word_field():
    data = corpus(); del data[0]["verse"]; expect("E_CORPUS_WORD_SCHEMA", data)
def test_rejects_wrong_language_uri():
    data = corpus(); data[0]["word_uri"] = data[0]["word_uri"].replace("/hebrew/", "/greek/"); expect("E_CORPUS_WORD_URI_INVALID", data)
def test_rejects_malformed_word_uri():
    data = corpus(); data[0]["word_uri"] = "invalid"; expect("E_CORPUS_WORD_URI_INVALID", data)
def test_rejects_empty_surface():
    data = corpus(); data[0]["surface"] = ""; expect("E_CORPUS_SURFACE_INVALID", data)
@pytest.mark.parametrize("field", ["chapter", "verse", "word_index"])
def test_rejects_nonpositive_or_boolean_coordinates(field):
    data = corpus(); data[0][field] = False; expect("E_CORPUS_COORDINATE_INVALID", data)
def test_rejects_uri_coordinate_mismatch():
    data = corpus(); data[0]["chapter"] = 2; expect("E_CORPUS_URI_COORDINATE_MISMATCH", data)
def test_rejects_empty_letters():
    data = corpus(); data[0]["letters"] = []; expect("E_CORPUS_LETTERS_INVALID", data)
def test_rejects_incomplete_letter_object():
    data = corpus(); data[0]["letters"][0] = {"char": "א"}; expect("E_CORPUS_LETTER_SCHEMA", data)
def test_rejects_malformed_letter_uri():
    data = corpus(); data[0]["letters"][0]["letter_uri"] = "invalid"; expect("E_CORPUS_LETTER_URI_INVALID", data)
def test_rejects_multi_character_letter():
    data = corpus(); data[0]["letters"][0]["char"] = "AB"; expect("E_CORPUS_LETTER_CHAR_INVALID", data)
def test_rejects_surface_letter_mismatch():
    data = corpus(); data[0]["letters"] = data[0]["letters"][:1]; expect("E_CORPUS_SURFACE_LETTER_MISMATCH", data)
def test_accepts_realistic_valid_bytes():
    raw = json.dumps(corpus(), ensure_ascii=False).encode("utf-8"); assert validate_living_word_bytes("genesis_oshb", raw).word_count == 8_086
