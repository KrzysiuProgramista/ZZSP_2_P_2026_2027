# test_text_tools.py
import unittest
from text_tool import is_palindrome, longest_word, word_count


class TestTextTools(unittest.TestCase):

    def test_word_count_normal(self):
        self.assertEqual(word_count("hello world"), 2)

    def test_word_count_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_word_count_awkward(self):
        self.assertEqual(word_count("one   two"), 2)

    def test_longest_word_normal(self):
        self.assertEqual(longest_word("cat dog elephant"), "elephant")

    def test_longest_word_empty(self):
        self.assertEqual(longest_word(""), "")

    def test_longest_word_awkward(self):
        self.assertEqual(longest_word("a bb ccc"), "ccc")

    def test_is_palindrome_normal(self):
        self.assertTrue(is_palindrome("madam"))

    def test_is_palindrome_empty(self):
        self.assertTrue(is_palindrome(""))

    def test_is_palindrome_awkward(self):
        self.assertTrue(is_palindrome("Racecar"))


if __name__ == "__main__":
    unittest.main()