import random
import unittest

from flappy import FlappyGame


class AdaptiveModeTests(unittest.TestCase):
    def make_game(self):
        return FlappyGame(random.Random(1), gap=110, speed=2.5, adaptive=True)

    def test_difficulty_increases_after_five_pipes(self):
        game = self.make_game()
        game.score = 5
        game._apply_adaptive_difficulty()
        self.assertEqual(game.adaptive_level, 1)
        self.assertEqual(game.gap, 108)
        self.assertAlmostEqual(game.speed, 2.65)

    def test_minimum_gap_is_enforced(self):
        game = self.make_game()
        game.gap = game.MIN_GAP
        game.score = 5
        game._apply_adaptive_difficulty()
        self.assertEqual(game.gap, game.MIN_GAP)

    def test_maximum_speed_is_enforced(self):
        game = self.make_game()
        game.speed = game.MAX_SPEED - 0.05
        game.score = 5
        game._apply_adaptive_difficulty()
        self.assertEqual(game.speed, game.MAX_SPEED)

    def test_restart_resets_adaptive_progress_and_preset(self):
        game = self.make_game()
        game.score = 10
        game._apply_adaptive_difficulty()
        game.reset()
        self.assertEqual(game.score, 0)
        self.assertEqual(game.gap, 110)
        self.assertEqual(game.speed, 2.5)
        self.assertEqual(game.adaptive_level, 0)


if __name__ == "__main__":
    unittest.main()
