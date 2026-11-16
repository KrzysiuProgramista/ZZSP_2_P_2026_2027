import unittest
import os
import tempfile
from file_store import FileStore


class TestFileStore(unittest.TestCase):

    def setUp(self):
        self.store = FileStore()
        self.temp_file = tempfile.mktemp(suffix=".json")

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_then_load(self):
        data = {"name": "Alice", "balance": 100}
        self.store.save(data, self.temp_file)
        result = self.store.load(self.temp_file)
        self.assertEqual(result, data)

    def test_load_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.store.load(self.temp_file)

    def test_save_empty_dict(self):
        self.store.save({}, self.temp_file)
        result = self.store.load(self.temp_file)
        self.assertEqual(result, {})

    def test_overwrite_existing_file(self):
        self.store.save({"name": "Alice"}, self.temp_file)
        self.store.save({"name": "Bob"}, self.temp_file)
        result = self.store.load(self.temp_file)
        self.assertEqual(result, {"name": "Bob"})

    def test_load_corrupted_file(self):
        with open(self.temp_file, "w") as file:
            file.write("this is not valid JSON")

        with self.assertRaises(ValueError):
            self.store.load(self.temp_file)


if __name__ == "__main__":
    unittest.main()
