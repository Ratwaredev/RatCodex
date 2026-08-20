from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).parents[1] / "templates" / "atomic_json.py"
spec = importlib.util.spec_from_file_location("atomic_json_template", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
write_json_atomic = module.write_json_atomic


class AtomicJsonTests(unittest.TestCase):
    def test_writes_valid_utf8_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nested" / "data.json"
            write_json_atomic(path, {"name": "café", "count": 2})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), {"name": "café", "count": 2})

    def test_serialization_failure_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            path.write_text('{"stable": true}\n', encoding="utf-8")
            with self.assertRaises(TypeError):
                write_json_atomic(path, {"bad": object()})
            self.assertEqual(path.read_text(encoding="utf-8"), '{"stable": true}\n')

    def test_leaves_no_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            write_json_atomic(path, [1, 2, 3])
            leftovers = [p.name for p in Path(tmp).iterdir() if p.name.endswith(".tmp")]
            self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
