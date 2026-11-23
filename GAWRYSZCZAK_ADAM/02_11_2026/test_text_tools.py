import unittest
from text_tools import word_count, longest_word, is_palindrome


class TestTextTools(unittest.TestCase):


    def test_word_count_normal(self):
        self.assertEqual(word_count("Ala ma kota"), 3)

    def test_word_count_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_word_count_extra_spaces(self):
        self.assertEqual(word_count("   duzo    spacji   w tekscie  "), 4)


    def test_longest_word_normal(self):
        self.assertEqual(longest_word("Python jest super jezykiem"), "jezykiem")

    def test_longest_word_empty(self):
        self.assertEqual(longest_word(""), "")

    def test_longest_word_single_word_and_spaces(self):
        self.assertEqual(longest_word("   programowanie   "), "programowanie")


    def test_is_palindrome_normal(self):
        self.assertTrue(is_palindrome("kajak"))
        self.assertFalse(is_palindrome("komputer"))

    def test_is_palindrome_empty(self):
        self.assertTrue(is_palindrome(""))

    def test_is_palindrome_awkward_punctuation_and_case(self):
        self.assertTrue(is_palindrome("Kobyła ma mały bok!"))
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))


if __name__ == "__main__":
    unittest.main()