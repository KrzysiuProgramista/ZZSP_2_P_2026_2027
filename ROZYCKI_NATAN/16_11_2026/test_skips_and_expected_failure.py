import sys
import unittest


class TestDecorators(unittest.TestCase):
    @unittest.skip("not implemented yet")
    def test_future_feature(self) -> None:
        self.fail("This should not run yet")

    @unittest.skipIf(sys.platform == "win32", "posix only")
    def test_posix_behaviour(self) -> None:
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_known_bug(self) -> None:
        self.assertEqual(1 + 1, 3)


if __name__ == "__main__":
    unittest.main()