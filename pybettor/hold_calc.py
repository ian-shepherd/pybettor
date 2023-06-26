from typing import Union  # noqa: F401
from .implied_prob import implied_prob


def hold_calc(odds, category: str = "us", **kwargs) -> float:
    """Sportsbook Hold Calculator
    This function calculates the hold perrcentage that the sportsbook has for the given bet.

    Args:
        odds int, float, list): odds of an event
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds
        **kwargs: keyword arguments to pass to implied_prob

    Returns:
        float: hold percentage of odds
    """

    # Error handling
    if not all(isinstance(line, (int, float)) for line in odds):
        raise ValueError("Lines must be numeric")

    imp_probs = implied_prob(odds, category=category, **kwargs)
    if isinstance(imp_probs, dict):
        hold = imp_probs.get("margin")
    else:
        hold = 1 - (1 / sum(imp_probs))

    return hold
