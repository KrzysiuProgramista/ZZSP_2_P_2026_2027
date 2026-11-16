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


def square_number(x):
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise TypeError("Input must be a number")
    return x * x