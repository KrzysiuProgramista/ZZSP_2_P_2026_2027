def count_words(text):
    counts = {}
    for word in text.lower().replace(",", "").replace(".", "").replace("!", "").split():
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
 
print(count_words("Go, go. STOP go!"))
print(count_words("Stop and go!"))

# Symptom: Program counts go! as a seperate word and counts only 1 go
# Cause: Program doesn't delete ! before counting
# Fix: Check whether the word has already been counted. If it has, increment the count; otherwise, set it to 1