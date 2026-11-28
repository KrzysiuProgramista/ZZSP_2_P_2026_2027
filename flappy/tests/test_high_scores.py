import json
import tempfile
import unittest
from pathlib import Path

from flappy import (
    default_high_scores, load_high_scores, save_high_scores, update_high_score,
)


class HighScoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.path = Path(self.temp_dir.name) / "scores.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_missing_file_returns_defaults(self):
        self.assertEqual(load_high_scores(self.path), default_high_scores())

    def test_valid_json_loads_records(self):
        self.path.write_text(json.dumps({"easy": 12, "normal": 7, "hard": 3}))
        self.assertEqual(load_high_scores(self.path),
                         {"easy": 12, "normal": 7, "hard": 3})

    def test_malformed_json_is_safe(self):
        self.path.write_text("{not valid json")
        self.assertEqual(load_high_scores(self.path), default_high_scores())

    def test_unexpected_structure_and_invalid_values_are_safe(self):
        self.path.write_text(json.dumps([1, 2, 3]))
        self.assertEqual(load_high_scores(self.path), default_high_scores())
        self.path.write_text(json.dumps({
            "easy": -4, "normal": "high", "hard": True, "extra": 99
        }))
        self.assertEqual(load_high_scores(self.path), default_high_scores())

    def test_higher_score_is_saved(self):
        scores = default_high_scores()
        self.assertTrue(update_high_score(scores, "easy", 10, self.path))
        self.assertEqual(load_high_scores(self.path)["easy"], 10)

    def test_lower_score_does_not_overwrite_record(self):
        scores = {"easy": 10, "normal": 0, "hard": 0}
        save_high_scores(scores, self.path)
        self.assertFalse(update_high_score(scores, "easy", 5, self.path))
        self.assertEqual(load_high_scores(self.path)["easy"], 10)

    def test_difficulties_have_separate_records(self):
        scores = default_high_scores()
        update_high_score(scores, "easy", 8, self.path)
        update_high_score(scores, "hard", 3, self.path)
        loaded = load_high_scores(self.path)
        self.assertEqual(loaded, {"easy": 8, "normal": 0, "hard": 3})

    def test_restart_keeps_saved_records(self):
        scores = default_high_scores()
        update_high_score(scores, "normal", 14, self.path)
        # Simulate a fresh game process by loading the file into a new structure.
        restarted_scores = load_high_scores(self.path)
        self.assertEqual(restarted_scores["normal"], 14)


if __name__ == "__main__":
    unittest.main()
