
import string


def word_count(text):
    return len(text.split())


def longest_word(text):
    words = text.split()
    if not words:
        return ""
    return max(words, key=len)


def is_palindrome(text):
    cleaned = ''.join(
        char.lower() for char in text
        if char.isalnum()
    )
    return cleaned == cleaned[::-1]
