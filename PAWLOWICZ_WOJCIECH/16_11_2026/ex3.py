import json
import os
import tempfile
import unittest

class FileStore:
    def __init__(self, path):
        self.path = path

    def save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)


class TestFileStore(unittest.TestCase):
    def setUp(self):
        # reserve a unique temp path for this test
        fd, self.path = tempfile.mkstemp()
        os.close(fd)

    def tearDown(self):
        # delete it if it still exists, so no test file is left behind
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_save_then_load_round_trips_data(self):
        store = FileStore(self.path)
        store.save({"theme": "dark", "volume": 7})
        self.assertEqual(store.load(), {"theme": "dark", "volume": 7})

    def test_load_missing_file_raises(self):
        store = FileStore(self.path)
        os.remove(self.path)
        with self.assertRaises(FileNotFoundError):
            store.load()

    def test_save_empty_dict(self):
        store = FileStore(self.path)
        store.save({})
        self.assertEqual(store.load(), {})

    def test_save_overwrites_existing_data(self):
        store = FileStore(self.path)
        store.save({"version": 1})
        store.save({"version": 2})
        self.assertEqual(store.load(), {"version": 2})

    def test_load_corrupted_file_raises(self):
        store = FileStore(self.path)
        with open(self.path, "w") as f:
            f.write("{not valid json")
        with self.assertRaises(json.JSONDecodeError):
            store.load()


if __name__ == "__main__":
    unittest.main()