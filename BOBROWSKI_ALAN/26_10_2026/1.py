def greeting(name):
    return f"Hello, {name}!"

print(greeting("Richard"))

# Symptom: Running crashes with syntax error
# Cause: No : when defining function
# Fix: Add :
# Tests: input Maya, input John and input Richard work.