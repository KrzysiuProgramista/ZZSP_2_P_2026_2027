import re

WORD_PATTERN = re.compile(r"\w+(?:['’-]\w+)*")


def _words(text):
    return WORD_PATTERN.findall(text)


def word_count(text):
    return len(_words(text))


def longest_word(text):
    words = _words(text)
    if not words:
        return ""
    return max(words, key=len)


def is_palindrome(text):
    cleaned = [char.lower() for char in text if char.isalnum()]
    return cleaned == cleaned[::-1]
