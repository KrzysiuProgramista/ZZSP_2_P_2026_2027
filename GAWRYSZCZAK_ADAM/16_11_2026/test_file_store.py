import os
import json
import unittest
from file_store import FileStore


class TestFileStore(unittest.TestCase):

    def setUp(self):
        self.store = FileStore()
        self.temp_file = "temp_test_data.json"

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_and_load(self):
        data = {"name": "Anna", "score": 100}
        self.store.save(self.temp_file, data)
        loaded = self.store.load(self.temp_file)
        self.assertEqual(loaded, data)

    def test_load_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            self.store.load("nieistniejacy_plik.json")

    def test_save_empty_dict(self):
        self.store.save(self.temp_file, {})
        loaded = self.store.load(self.temp_file)
        self.assertEqual(loaded, {})

    def test_overwrite_existing_file(self):
        self.store.save(self.temp_file, {"a": 1})
        self.store.save(self.temp_file, {"b": 2})
        loaded = self.store.load(self.temp_file)
        self.assertEqual(loaded, {"b": 2})

    def test_load_corrupted_file(self):
        with open(self.temp_file, "w", encoding="utf-8") as file:
            file.write("{ uszkodzony json...")

        with self.assertRaises(json.JSONDecodeError):
            self.store.load(self.temp_file)


if __name__ == "__main__":
    unittest.main()