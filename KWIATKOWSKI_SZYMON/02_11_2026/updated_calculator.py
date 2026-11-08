def _check_numeric(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numbers")


def add(a, b):
    _check_numeric(a, b)
    return a + b


def subtract(a, b):
    _check_numeric(a, b)
    return a - b


def multiply(a, b):
    _check_numeric(a, b)
    return a * b


def divide(a, b):
    _check_numeric(a, b)
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b