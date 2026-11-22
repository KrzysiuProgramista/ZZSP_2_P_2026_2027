import unittest
import tempfile
import os
import json

from file_store import FileStore

class TestFileStore(unittest.TestCase):

    def setUp(self):
        self.store = FileStore()

        temp = tempfile.NamedTemporaryFile(delete=False)
        self.filename = temp.name
        temp.close()

        os.remove(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_then_load(self):
        data = {"name": "Alice", "age": 25}

        self.store.save(data, self.filename)
        result = self.store.load(self.filename)

        self.assertEqual(result, data)

    def test_load_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.store.load(self.filename)

    def test_save_empty_dictionary(self):
        data = {}

        self.store.save(data, self.filename)
        result = self.store.load(self.filename)

        self.assertEqual(result, {})

    def test_overwrite_existing_file(self):
        self.store.save({"name": "Alice"}, self.filename)
        self.store.save({"name": "Bob"}, self.filename)

        result = self.store.load(self.filename)

        self.assertEqual(result, {"name": "Bob"})

    def test_load_corrupted_file(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write("{invalid json")

        with self.assertRaises(json.JSONDecodeError):
            self.store.load(self.filename)


if __name__ == "__main__":
    unittest.main()