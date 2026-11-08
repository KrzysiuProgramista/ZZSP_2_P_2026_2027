import unittest
from text_tools import word_count, longest_word, is_palindrome


class TestWordCount(unittest.TestCase):

    def test_normal_case(self):
        self.assertEqual(word_count("The quick brown fox"), 4)

    def test_empty_input(self):
        self.assertEqual(word_count(""), 0)

    def test_awkward_case_extra_spaces(self):
        self.assertEqual(word_count("   hello    world   "), 2)


class TestLongestWord(unittest.TestCase):

    def test_normal_case(self):
        self.assertEqual(longest_word("The quick brown fox jumps"), "jumps")

    def test_empty_input(self):
        self.assertEqual(longest_word(""), "")

    def test_awkward_case_punctuation_and_one_word(self):
        self.assertEqual(longest_word("   ...supercalifragilistic...!   "), "supercalifragilistic")


class TestIsPalindrome(unittest.TestCase):

    def test_normal_case(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertFalse(is_palindrome("python"))

    def test_empty_input(self):
        self.assertTrue(is_palindrome(""))

    def test_awkward_case_mixed_case_spaces_and_punctuation(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama!"))
        self.assertTrue(is_palindrome("Was it a car or a cat I saw?"))
        self.assertTrue(is_palindrome("No 'x' in Nixon"))


if __name__ == "__main__":
    unittest.main()