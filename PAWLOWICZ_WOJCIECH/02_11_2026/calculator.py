"""calculator.py -- a tiny calculator module."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def safe_add(a, b):
    """Exercise 3: raises TypeError for non-numeric input."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("safe_add requires numeric arguments.")
    return a + b
