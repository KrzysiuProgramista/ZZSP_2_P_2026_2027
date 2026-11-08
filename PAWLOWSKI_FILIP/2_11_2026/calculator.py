def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def strict_add(a, b):
    for value in (a, b):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Arguments must be numbers")
    return a + b
