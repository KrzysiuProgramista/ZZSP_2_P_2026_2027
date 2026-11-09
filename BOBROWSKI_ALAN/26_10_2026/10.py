tickets = {
    "standard": {"price": 20, "stock": 8},
    "vip": {"price": 50, "stock": 6},
}
 
def purchase(ticket_type, quantity, balance):
    if ticket_type in tickets:
        ticket = tickets[ticket_type]
    else:
        return {"ok": False, "message": "Unknown ticket type"}

    if quantity <= 0:
        return {"ok": False, "message": "Invalid quantity"}

    if quantity > ticket["stock"]:
        return {"ok": False, "message": "Not enough tickets"}

    total = ticket["price"] * quantity

    if quantity >= 5:
        total = total * 0.9

    if balance < total:
        return {"ok": False, "message": "Insufficient funds"}

    ticket["stock"] -= quantity
    new_balance = balance - total

    return {"ok": True, "total": total,
            "balance": new_balance,
            "remaining_stock": ticket["stock"]}

print(purchase("standard", 3, 100))
print(purchase("standard", 5, 200))
print(purchase("vip", 2, 50))
print(purchase("gold", 1, 100))
print(purchase("standard", 0, 100))

# Symptom:
# Stock was overwritten instead of reduced.
# Balance was calculated incorrectly.
# Unknown ticket types caused the program to crash.
# Updates could happen before all checks were completed.

# Causes:
# Incorrect stock assignment.
# Reversed balance subtraction.
# Missing ticket type validation.
# Incorrect order of operations and return statement.

# Fix:
# Added a check for unknown ticket types.
# Used ticket["stock"] -= quantity.
# Used balance - total.
# Moved stock and balance updates before return.
# Ensured all validation checks happen before updates.

# Tests:
# 1. Standard, 3 tickets, balance 100:
# Expected: total 60, balance 40, stock 5.

# 2. Standard, 5 tickets, balance 200:
# Expected: total 90, balance 110, stock 0 (after test 1).

# 3. VIP, 2 tickets, balance 50:
# Expected: Insufficient funds, stock unchanged.

# 4. Gold, 1 ticket, balance 100:
# Expected: Unknown ticket type, no crash.

# 5. Standard, 0 tickets, balance 100:
# Expected: Invalid quantity, no state change.
