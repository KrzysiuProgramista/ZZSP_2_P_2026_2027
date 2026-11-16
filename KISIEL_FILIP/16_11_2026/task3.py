#zad 3
import json
import os
import tempfile
import unittest


class FileStore:
    def __init__(self, path):
        self.path = path

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)


class TestFileStore(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        self.store = FileStore(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_save_then_load(self):
        data = {"theme": "dark"}
        self.store.save(data)
        self.assertEqual(self.store.load(), data)

    def test_load_missing_file(self):
        os.remove(self.path)
        with self.assertRaises(FileNotFoundError):
            self.store.load()

    def test_save_empty_dict(self):
        self.store.save({})
        self.assertEqual(self.store.load(), {})

    def test_overwrite(self):
        self.store.save({"theme": "light"})
        self.store.save({"theme": "dark"})
        self.assertEqual(self.store.load(), {"theme": "dark"})

    def test_load_corrupted_file(self):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write("{invalid json}")
        with self.assertRaises(json.JSONDecodeError):
            self.store.load()


if __name__ == "__main__":
    unittest.main(verbosity=2)
