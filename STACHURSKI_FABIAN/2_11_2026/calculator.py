def _check_numeric(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("Arguments must be numeric")


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
    _check_numeric(a)
    _check_numeric(b)
    return a + b