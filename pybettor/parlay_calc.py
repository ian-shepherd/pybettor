import numpy as np

from convert_odds import convert_odds


def parlay_calc(risk: float = 100.0, odds=[-110, -110], category: str = "us"):
    """Parlay Calculation
    This function calculates the payout of parlay bets.

    Args:
        risk (float): Risk of parlay bet
        odds (list): odds of an event
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds

    Returns:
        float: Parlay payout
    """

    if type(odds) is not list:
        odds = [odds]

    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "category must be either: ('us', 'dec', 'frac')"

    total_odds = np.prod(convert_odds(odds, cat_in=category, cat_out="dec"))
    payout = round(total_odds * risk, 2) - risk

    return payout
