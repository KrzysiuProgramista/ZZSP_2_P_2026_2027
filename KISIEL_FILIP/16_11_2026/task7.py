#zad 7
import sys
import unittest


class TestSkipAndExpectedFailure(unittest.TestCase):
    @unittest.skip("not implemented yet")
    def test_feature_not_implemented(self):
        self.fail("This test is skipped, so this line is not executed.")

    @unittest.skipIf(sys.platform == "win32", "posix only")
    def test_posix_only_feature(self):
        self.assertNotEqual(sys.platform, "win32")

    @unittest.expectedFailure
    def test_known_unfixed_problem(self):
        self.assertEqual(2 + 2, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
