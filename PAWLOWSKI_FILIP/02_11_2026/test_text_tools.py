import unittest

from text_tools import word_count, longest_word, is_palindrome


class TestWordCount(unittest.TestCase):
    def test_normal_sentence(self):
        self.assertEqual(word_count("The quick brown fox"), 4)

    def test_empty_input(self):
        self.assertEqual(word_count(""), 0)

    def test_extra_spaces(self):
        self.assertEqual(word_count("  hello    world  "), 2)

    def test_single_word(self):
        self.assertEqual(word_count("hello"), 1)

    def test_punctuation_is_not_counted_as_word(self):
        self.assertEqual(word_count("Hello , world !"), 2)


class TestLongestWord(unittest.TestCase):
    def test_normal_sentence(self):
        self.assertEqual(longest_word("I love programming in Python"), "programming")

    def test_empty_input(self):
        self.assertEqual(longest_word(""), "")

    def test_single_word(self):
        self.assertEqual(longest_word("hello"), "hello")

    def test_extra_spaces(self):
        self.assertEqual(longest_word("   a    abc   ab   "), "abc")

    def test_trailing_punctuation_is_ignored(self):
        self.assertEqual(longest_word("Hello, wonderful!"), "wonderful")

    def test_tie_returns_first_word(self):
        self.assertEqual(longest_word("cat dog"), "cat")


class TestIsPalindrome(unittest.TestCase):
    def test_normal_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_normal_non_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_empty_input(self):
        self.assertTrue(is_palindrome(""))

    def test_mixed_case(self):
        self.assertTrue(is_palindrome("RaceCar"))

    def test_spaces_and_punctuation(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama!"))

    def test_single_character(self):
        self.assertTrue(is_palindrome("x"))

    def test_only_punctuation_and_spaces(self):
        self.assertTrue(is_palindrome(" ,.! "))


if __name__ == "__main__":
    unittest.main()
