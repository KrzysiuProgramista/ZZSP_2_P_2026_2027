"""text_tools.py -- small string-processing helpers."""

import string


def word_count(text: str) -> int:
    return len(text.split())


def longest_word(text: str) -> str:
    words = text.split()
    if not words:
        return ""
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    cleaned = [ch.lower() for ch in text if ch not in string.whitespace and ch not in string.punctuation]
    return cleaned == cleaned[::-1]
