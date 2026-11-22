import json
import os
import tempfile
import unittest

from file_store import FileStore

TEMP_PREFIX = "filestore_test_"


class TestFileStore(unittest.TestCase):

    def setUp(self):
        self.store = FileStore()

        handle, self.path = tempfile.mkstemp(prefix=TEMP_PREFIX, suffix=".json")
        os.close(handle)

        os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_save_then_load(self):
        data = {"city": "Łódź", "visits": 3, "tags": ["a", "b"]}

        self.store.save(data, self.path)

        self.assertEqual(self.store.load(self.path), data)

    def test_load_missing_file(self):
        self.assertFalse(os.path.exists(self.path))

        with self.assertRaises(FileNotFoundError):
            self.store.load(self.path)

    def test_save_empty_dict(self):
        self.store.save({}, self.path)

        self.assertEqual(self.store.load(self.path), {})

    def test_overwrite_existing_file(self):
        self.store.save({"version": 1, "note": "a longer first version"}, self.path)
        self.store.save({"version": 2}, self.path)

        self.assertEqual(self.store.load(self.path), {"version": 2})

    def test_load_corrupted_file(self):
        with open(self.path, "w", encoding="utf-8") as handle:
            handle.write('{"broken": ')

        with self.assertRaises(json.JSONDecodeError):
            self.store.load(self.path)


if __name__ == "__main__":
    unittest.main()
