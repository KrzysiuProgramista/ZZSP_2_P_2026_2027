import unittest
from text_tools import word_count, longest_word, is_palindrome


class TestTextTools(unittest.TestCase):
    # word_count tests
    def test_word_count_normal(self):
        self.assertEqual(word_count("python unit tests are useful"), 5)

    def test_word_count_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_word_count_extra_spaces(self):
        self.assertEqual(word_count("   one   two   "), 2)

    # longest_word tests
    def test_longest_word_normal(self):
        self.assertEqual(longest_word("cat elephant dog"), "elephant")

    def test_longest_word_empty(self):
        self.assertEqual(longest_word(""), "")

    def test_longest_word_single_word(self):
        self.assertEqual(longest_word("   Algorithm!   "), "Algorithm")

    # is_palindrome tests
    def test_is_palindrome_normal(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_is_palindrome_empty(self):
        self.assertTrue(is_palindrome(""))

    def test_is_palindrome_mixed_case_and_punctuation(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama!"))


if __name__ == "__main__":
    unittest.main()