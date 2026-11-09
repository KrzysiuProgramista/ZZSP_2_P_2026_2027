def remove_expired(sessions):
    i = 0
    while i < len(sessions):
        if sessions[i]["expired"]:
            sessions.pop(i)
        else:
            i += 1
    return sessions
 
sessions1 = [
    {"id": 1, "expired": True},
    {"id": 2, "expired": True},
    {"id": 3, "expired": False},
]

sessions2 = [
    {"id": 1, "expired": False},
    {"id": 2, "expired": False},
    {"id": 3, "expired": False},
]

sessions3 = [
    {"id": 1, "expired": True},
    {"id": 2, "expired": True},
    {"id": 3, "expired": True},
]

print(remove_expired(sessions1))
print(remove_expired(sessions2))
print(remove_expired(sessions3))

# Symptom: Program only removes session 1
# Cause: Removing `session[0]` shifts `session[1]` to index 0, but the loop moves forward, skipping it.
# Fix: Use a while loop with an index variable.
# Tests: Two expired sessions next to each other return [{'id': 3, 'expired': False}]
# No expired sessions return [{'id': 1, 'expired': False}, {'id': 2, 'expired': False}, {'id': 3, 'expired': False}]
# All expired sessions return []