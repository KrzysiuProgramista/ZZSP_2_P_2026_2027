import unittest

from text_tools import word_count, longest_word, is_palindrome


class TestWordCount(unittest.TestCase):
    def test_normal_case(self):
        self.assertEqual(word_count("the quick brown fox"), 4)

    def test_empty_input(self):
        self.assertEqual(word_count(""), 0)

    def test_extra_spaces(self):
        self.assertEqual(word_count("  hello   world  "), 2)


class TestLongestWord(unittest.TestCase):
    def test_normal_case(self):
        self.assertEqual(longest_word("I love programming"), "programming")

    def test_empty_input(self):
        self.assertEqual(longest_word(""), "")

    def test_one_word(self):
        self.assertEqual(longest_word("hello"), "hello")

    def test_tie_returns_first_longest(self):
        self.assertEqual(longest_word("cat dog bat"), "cat")


class TestIsPalindrome(unittest.TestCase):
    def test_normal_case(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertFalse(is_palindrome("hello"))

    def test_empty_input(self):
        self.assertTrue(is_palindrome(""))

    def test_mixed_case_spaces_and_punctuation(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))


if __name__ == "__main__":
    unittest.main()
