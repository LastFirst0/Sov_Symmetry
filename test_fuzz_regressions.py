import json
import tempfile
import unittest
from pathlib import Path

from sov_evidence_geometry_core import derive_id
from sov_evidence_geometry_core.errors import CoreContractError
from sov_evidence_geometry_core.persistence import FileObjectStore


class FuzzRegressionTests(unittest.TestCase):
    def _record(self):
        fixture_path = Path(__file__).parent / "data" / "cross_language_invariant_vectors.json"
        document = json.loads(fixture_path.read_text(encoding="utf-8"))
        return document["records"][0]

    def test_non_hex_digest_cannot_escape_objects_root(self):
        with tempfile.TemporaryDirectory() as directory:
            store = FileObjectStore(directory)
            with self.assertRaises(CoreContractError) as context:
                store._path("sov:sha256:../" + "a" * 61)
            self.assertEqual(context.exception.code, "E_SCHEMA_INVALID")
            self.assertTrue(Path(store.objects).exists())

    def test_noncanonical_stored_bytes_are_tamper(self):
        with tempfile.TemporaryDirectory() as directory:
            store = FileObjectStore(directory)
            object_id = store.put(self._record())
            path = store._path(object_id)
            path.write_bytes(path.read_bytes() + b" ")
            with self.assertRaises(CoreContractError) as context:
                store.verify_manifest()
            self.assertEqual(context.exception.code, "E_AUDIT_TAMPER")


if __name__ == "__main__":
    unittest.main()
