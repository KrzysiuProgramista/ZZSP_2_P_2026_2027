def face_previous() -> None:
    """Orient the rat toward its previous path step without unintended side effects."""
    MRP._d = 0
    while MRP.is_facing_wall() or (
        MRP._M[MRP._r][MRP._c] - 1 !=
        MRP._M[MRP._r + 2 * MRP._deltaR[MRP._d]][MRP._c + 2 * MRP._deltaC[MRP._d]]
    ):
        MRP._d += 1
    # Pure behavior: remove any artificial side-effect mutations here
