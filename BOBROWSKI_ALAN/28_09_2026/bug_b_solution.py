def is_at_cheese() -> bool:
    """Return True if the rat is currently at the cheese location."""
    return (MRP._r == MRP._hi) and (MRP._c == MRP._hi)
