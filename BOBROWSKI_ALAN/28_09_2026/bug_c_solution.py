def turn_clockwise() -> None:
    """Turn the rat clockwise by cycling direction modulo 4."""
    MRP._d = (MRP._d + 1) % 4
