import re


def word_count(text):
    if not text or not text.strip():
        return 0
    return len(text.strip().split())


def longest_word(text):
    if not text or not text.strip():
        return ""
    words = re.findall(r"[A-Za-z0-9']+", text)
    if not words:
        return ""
    return max(words, key=len)


def is_palindrome(text):
    cleaned = re.sub(r"[^A-Za-z0-9]", "", text).lower()
    return cleaned == cleaned[::-1]