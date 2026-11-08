import string

def word_count(text):
    if not text or not text.strip():
        return 0
    return len(text.split())

def longest_word(text):
    if not text or not text.strip():
        return ""
    words = text.split()
    cleaned_words = [w.strip(string.punctuation) for w in words]
    cleaned_words = [w for w in cleaned_words if w]
    if not cleaned_words:
        return ""
    return max(cleaned_words, key=len)

def is_palindrome(text):
    if not text:
        return True
    cleaned = ''.join(ch.lower() for ch in text if ch.isalnum())
    if not cleaned:
        return True
    return cleaned == cleaned[::-1]