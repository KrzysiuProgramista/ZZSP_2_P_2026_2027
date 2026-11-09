import unittest
from text_tools import word_count, longest_word, is_palindrome, remove_punctuation

class TestTextTools(unittest.TestCase):
    def test_word_count(self):
        self.assertEqual(word_count("Hello world"), {'hello': 1, 'world': 1})
    
    def test_word_count_empty(self):
        self.assertEqual(word_count(""), {})
    
    def test_word_count_one(self):
        self.assertEqual(word_count("Hello"), {'hello': 1})
    
    def test_longest_word(self):
        self.assertEqual(longest_word("I love the python language"), "language")

    def test_longest_word_one(self):
        self.assertEqual(longest_word("love"), "love")

    def test_longest_word_empty(self):
        self.assertEqual(longest_word(""), "")

    def test_is_palindrome(self):
        self.assertEqual(is_palindrome("racecar"), True)
    
    def test_is_palindrome_wrong(self):
        self.assertEqual(is_palindrome("world"), False)
    
    def test_is_palindrome_empty(self):
        self.assertEqual(is_palindrome(""), True)
    
    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation("hello, world."), "hello world")

    def test_remove_punctuation_one(self):
        self.assertEqual(remove_punctuation("hello,"), "hello")
    
    def test_remove_punctuation_empty(self):
        self.assertEqual(remove_punctuation(""), "")