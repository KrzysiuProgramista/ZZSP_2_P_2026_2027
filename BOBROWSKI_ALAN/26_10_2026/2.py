tickets = int(input("How many tickets? "))
if tickets > 0:
    print("Reservation accepted")
else:
    print("Enter a positive number")

# Symptom: Program crashes with TypeError
# Cause: You can't use the > operator with a string and an integer
# Fix: Convert tickets to int first
# Tests: input 3 prints "Reservation accepted"
# input 0 prints "Enter a positive number"