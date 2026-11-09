def average(scores):
    try:
        return sum(scores) / len(scores)
    except ZeroDivisionError:
        return None
 
print(average([70, 80]))
print(average([]))

# Symptom: Program crashes with ZeroDivisionError
# Cause: Program tries to divide by len(scores) which is 0
# Fix: Put code into a try except block and return None when there is a ZeroDivisonError
# Tests: average([70,80]) returns 75.0 and average([]) returns None