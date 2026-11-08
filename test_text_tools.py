import unittest
from text_tools import word_count, longest_word, is_palindrome

class TestTextTools(unittest.TestCase):

    # --- Testy dla word_count ---
    def test_word_count_normal(self):
        self.assertEqual(word_count("Python programming is awesome"), 4)

    def test_word_count_empty(self):
        self.assertEqual(word_count(""), 0)
        self.assertEqual(word_count("   "), 0)

    def test_word_count_awkward(self):
        self.assertEqual(word_count("  Extra   spaces   tutaj! "), 3)
        self.assertEqual(word_count("JednoSłowo"), 1)

    # --- Testy dla longest_word ---
    def test_longest_word_normal(self):
        self.assertEqual(longest_word("Python programowanie to super sprawa"), "programowanie")

    def test_longest_word_empty(self):
        self.assertEqual(longest_word(""), "")
        self.assertEqual(longest_word("   "), "")

    def test_longest_word_awkward(self):
        # Sprawdza czy poprawnie ignoruje interpunkcję przy wyznaczaniu długości
        self.assertEqual(longest_word("  kot  przepiękny...   "), "przepiękny")
        self.assertEqual(longest_word("Słowo"), "Słowo")

    # --- Testy dla is_palindrome ---
    def test_is_palindrome_normal(self):
        self.assertTrue(is_palindrome("kajak"))
        self.assertFalse(is_palindrome("python"))

    def test_is_palindrome_empty(self):
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome("   "))

    def test_is_palindrome_awkward(self):
        # Ignoruje spacje, interpunkcję oraz wielkość liter
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertTrue(is_palindrome("Kobyła ma mały bok."))
        self.assertFalse(is_palindrome("To nie jest palindrom!"))

if __name__ == "__main__":
    unittest.main()