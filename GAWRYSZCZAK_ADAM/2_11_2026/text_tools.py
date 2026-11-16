def word_count(text):

    words = text.split()
    return len(words)


def longest_word(text):
    words = text.split()
    if not words:
        return ""
    return max(words, key=len)


def is_palindrome(text):

    cleaned = ""
    for char in text:
        if char.isalnum():
            cleaned += char.lower()
    return cleaned == cleaned[::-1]