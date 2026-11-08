# text_tools.py


def word_count(text):
    if text == "":
        return 0
    words = text.split()
    return len(words)


def longest_word(text):
    if text == "":
        return ""
    words = text.split()
    if len(words) == 0:
        return ""

    longest = words[0]
    for word in words:
        if len(word) > len(longest):
            longest = word
    return longest


def is_palindrome(text):
    if text == "":
        return True
    
    cleaned = text.lower()
    reversed_text = cleaned[::-1]
    return cleaned == reversed_text