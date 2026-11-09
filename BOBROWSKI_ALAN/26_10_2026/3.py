def last_reading(readings):
    return readings[-1]
 
print(last_reading([12, 13, 17]))
print(last_reading([42]))
# Symptom: Program crashes with IndexError
# Cause: Program tries to index the length of the list which is out of range
# Fix: Use readings[-1] to index the last element of the list
# Tests: last_reading([12,13,17]) returns 17
# last_reading[42] returns 42