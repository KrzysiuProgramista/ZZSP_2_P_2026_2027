def remove_punctuation(text):
    changedText = text.lower().replace(",", "").replace(".", "")
    return changedText

def word_count(text):
    sum = {}
    for word in remove_punctuation(text).split():
        if word in sum:
            sum[word] += 1
        else:
            sum[word] = 1
    return sum

def longest_word(text):
    words = word_count(text)

    longestWord = ""

    for word in words:
        if len(word) > len(longestWord):
            longestWord = word

    return longestWord

def is_palindrome(text):
    word = remove_punctuation(text).replace(" ", "")
    return word == word[::-1]
