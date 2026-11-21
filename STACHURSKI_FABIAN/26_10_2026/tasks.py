# Task 01
def greeting(name):
    return f"Hello, {name}!"

print(greeting("Maya"))


# Task 02
tickets = int(input("How many tickets? "))
if tickets > 0:
    print("Reservation accepted")
else:
    print("Enter a positive number")


# Task 03
def last_reading(readings):
    return readings[len(readings) - 1]

print(last_reading([12, 13, 17]))


# Task 04
def average(scores):
    if not scores:
        return None
    return sum(scores) / len(scores)

print(average([70, 80]))
print(average([]))


# Task 05
def emergency_contact(person):
    contact = person.get("contact", {})
    return contact.get("name") or "Not provided"

print(emergency_contact({"name": "Sam"}))
print(emergency_contact({"contact": {"name": "Alex"}}))


# Task 06
def shipping_cost(weight):
    if weight > 5:
        cost = 12
    elif weight > 1:
        cost = 8
    else:
        cost = 5
    return cost

print(shipping_cost(6))


# Task 07
def remove_expired(sessions):
    for session in list(sessions):
        if session["expired"]:
            sessions.remove(session)
    return sessions

sessions = [
    {"id": 1, "expired": True},
    {"id": 2, "expired": True},
    {"id": 3, "expired": False},
]
print(remove_expired(sessions))


# Task 08
def count_words(text):
    counts = {}
    for raw_word in text.lower().split():
        word = raw_word.strip(".,!?")
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts

print(count_words("Go, go. STOP go!"))


# Task 09
def can_book(age, seats, student):
    if not (1 <= seats <= 4):
        return False
    if student:
        return age >= 16
    return age >= 18


# Task 10
tickets = {
    "standard": {"price": 20, "stock": 8},
    "vip": {"price": 50, "stock": 6},
}


def purchase(ticket_type, quantity, balance):
    if ticket_type not in tickets:
        return {"ok": False, "message": "Unknown ticket type"}
    if quantity <= 0:
        return {"ok": False, "message": "Invalid quantity"}

    ticket = tickets[ticket_type]
    if quantity > ticket["stock"]:
        return {"ok": False, "message": "Not enough tickets"}

    total = ticket["price"] * quantity
    if quantity >= 5:
        total = total * 0.9

    if balance < total:
        return {"ok": False, "message": "Insufficient funds"}

    ticket["stock"] -= quantity
    new_balance = balance - total
    return {
        "ok": True,
        "total": total,
        "balance": new_balance,
        "remaining_stock": ticket["stock"],
    }