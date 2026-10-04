def is_facing_unvisited() -> bool:
    """Check if the cell 2 units ahead in direction _d has not been visited."""
    target_row = MRP._r + 2 * MRP._deltaR[MRP._d]
    target_col = MRP._c + 2 * MRP._deltaC[MRP._d]
    return MRP._M[target_row][target_col] == MRP._UNVISITED
