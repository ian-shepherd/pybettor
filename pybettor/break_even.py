def break_even(risk: float or int, rtrn: float or int, legs: int = 1) -> float:
    """Calculate the break even win percentage needed based on the amount risked and the amount returned.

    Args:
        risk (float or int): amount risked on the bet
        rtrn (float or int): amount returned on the bet
        legs (int, optional): number of legs in the bet. Defaults to 1.

    Returns:
        float: break even win percentage needed
    """
    assert isinstance(risk, (int, float)), "risk must be numeric"
    assert isinstance(rtrn, (int, float)), "rtrn must be numeric"
    assert isinstance(legs, int), "legs must be an integer"

    prob = (risk / rtrn) ** (1 / legs)

    return prob
