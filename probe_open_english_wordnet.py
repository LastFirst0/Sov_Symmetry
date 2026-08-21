"""Inspect a public Open English WordNet hierarchy without modifying kernel behavior."""

from __future__ import annotations

import json

import wn


def main() -> None:
    lexicon_id = "oewn:2025"
    try:
        lexicon = wn.Wordnet(lexicon_id)
    except wn.Error:
        wn.download(lexicon_id)
        lexicon = wn.Wordnet(lexicon_id)

    candidates = lexicon.synsets("animal", pos="n")
    result = []
    for synset in candidates[:5]:
        result.append(
            {
                "id": synset.id,
                "lemmas": [word.lemma() for word in synset.words()],
                "definition": synset.definition(),
                "hypernyms": [parent.id for parent in synset.hypernyms()],
                "hyponyms": [child.id for child in synset.hyponyms()],
            }
        )
    print(json.dumps({"lexicon": lexicon_id, "animal_candidates": result}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
