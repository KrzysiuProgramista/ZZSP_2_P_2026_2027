def _validate_number(val):
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise TypeError(f"Expected a numeric input, got {type(val).__name__}")


def add(a, b):
    _validate_number(a)
    _validate_number(b)
    return a + b


def subtract(a, b):
    _validate_number(a)
    _validate_number(b)
    return a - b


def multiply(a, b):
    _validate_number(a)
    _validate_number(b)
    return a * b


def divide(a, b):
    _validate_number(a)
    _validate_number(b)
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b