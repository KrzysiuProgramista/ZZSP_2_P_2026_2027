import json
import os
import tempfile
import unittest

from file_store import FileStore


class TestFileStore(unittest.TestCase):
    def setUp(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(path)  # start as if the file didn't exist yet
        self.path = path
        self.store = FileStore(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_save_then_load(self):
        data = {"a": 1, "b": [1, 2, 3]}
        self.store.save(data)
        self.assertEqual(self.store.load(), data)

    def test_load_missing_file(self):
        self.assertEqual(self.store.load(), {})

    def test_save_empty_dict(self):
        self.store.save({})
        self.assertEqual(self.store.load(), {})

    def test_overwrite_existing_file(self):
        self.store.save({"a": 1})
        self.store.save({"b": 2})
        self.assertEqual(self.store.load(), {"b": 2})

    def test_load_corrupted_file(self):
        with open(self.path, "w") as fh:
            fh.write("{not valid json")
        with self.assertRaises(json.JSONDecodeError):
            self.store.load()


if __name__ == "__main__":
    unittest.main()
