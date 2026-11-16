import unittest
from text_tools import word_count, longest_word, is_palindrome


class TestTextTools(unittest.TestCase):

    # word_count
    def test_word_count_normal(self):
        self.assertEqual(word_count("Hello world Python"), 3)

    def test_word_count_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_word_count_extra_spaces(self):
        self.assertEqual(word_count("  Hello   world  "), 2)

    # longest_word
    def test_longest_word_normal(self):
        self.assertEqual(longest_word("Python is awesome"), "awesome")

    def test_longest_word_empty(self):
        self.assertEqual(longest_word(""), "")

    def test_longest_word_one_word(self):
        self.assertEqual(longest_word("Programming"), "Programming")

    # is_palindrome
    def test_palindrome_normal(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_palindrome_empty(self):
        self.assertTrue(is_palindrome(""))

    def test_palindrome_mixed_case(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama!"))


if __name__ == "__main__":
    unittest.main()
