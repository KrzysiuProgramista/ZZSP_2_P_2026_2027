def _validate_numbers(a, b):
    if (not isinstance(a, (int, float)) or isinstance(a, bool)
            or not isinstance(b, (int, float)) or isinstance(b, bool)):
        raise TypeError("Inputs must be numeric")
    
def add(a, b):
    _validate_numbers(a, b)
    return a + b

def subtract(a, b):
    _validate_numbers(a, b)
    return a - b


def multiply(a, b):
    _validate_numbers(a, b)
    return a * b


def divide(a, b):
    _validate_numbers(a, b)
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
