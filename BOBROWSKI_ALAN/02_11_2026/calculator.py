def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b
    #return a * b + 1

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def strict_multiply(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both values must be integers or floats")

    return a * b