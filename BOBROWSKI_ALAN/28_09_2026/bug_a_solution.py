def is_facing_wall() -> bool:
    """Check if the cell directly ahead in direction MRP._d contains a wall."""
    target_row = MRP._r + MRP._deltaR[MRP._d]
    target_col = MRP._c + MRP._deltaC[MRP._d]
    return MRP._M[target_row][target_col] == MRP._WALL
