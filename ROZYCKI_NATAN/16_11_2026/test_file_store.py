import json
import os
import tempfile
import unittest
import uuid
from file_store import FileStore


class TestFileStore(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_filename = os.path.join(
            tempfile.gettempdir(), f"filestore_{uuid.uuid4().hex}.json"
        )
        self.store = FileStore(self.temp_filename)

    def tearDown(self) -> None:
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_save_then_load(self) -> None:
        data = {"name": "Alice", "scores": [10, 20, 30]}
        self.store.save(data)
        self.assertEqual(self.store.load(), data)

    def test_load_missing_file_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.store.load()

    def test_save_empty_dict(self) -> None:
        self.store.save({})
        self.assertEqual(self.store.load(), {})

    def test_overwrite_existing_file(self) -> None:
        self.store.save({"version": 1, "extra": "old"})
        self.store.save({"version": 2})
        self.assertEqual(self.store.load(), {"version": 2})

    def test_load_corrupted_file_raises(self) -> None:
        with open(self.temp_filename, "w", encoding="utf-8") as f:
            f.write("{not valid json")
        with self.assertRaises(json.JSONDecodeError):
            self.store.load()


if __name__ == "__main__":
    unittest.main()