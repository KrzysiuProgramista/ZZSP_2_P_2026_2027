def can_book(age, seats, student):
    if seats > 0 and age >= 18 and seats <= 4 or student and age >= 16 and seats <= 4:
        return True
    return False

case1 = (25, 5, False)
case2 = (15, 1, True)
case3 = (16, 1, True)
case4 = (20, 0, False)
case5 = (20, 4, False)

print(can_book(*case1))
print(can_book(*case2))
print(can_book(*case3))
print(can_book(*case4))
print(can_book(*case5))

# Symptom: 
    # • (25, 5, False) → True
    # • (15, 1, True) → False
    # • (16, 1, True) → True.
    # • (20, 0, False) → False.
    # • (20, 4, False) → True.

# Cause: Original condition allows anyone aged 18 or over to book five or more seats because there is no upper seat limit in the first condition.
# Fix: Add seats <= 4 to both conditions and seats > 0
# Tests:
    # • (25, 5, False) → False
    # • (15, 1, True) → False
    # • (16, 1, True) → True.
    # • (20, 0, False) → False.
    # • (20, 4, False) → True.
