import re

def word_count(text: str) -> int:
    if not text:
        return 0
    words = text.split()
    return len(words)


def longest_word(text: str) -> str:
    if not text:
        return ""
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return ""
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    cleaned = [ch.lower() for ch in text if ch.isalnum()]
    return cleaned == cleaned[::-1]