from fractions import Fraction
from .convert_odds import convert_odds


def bet_calc(risk: int or float, odds: int or float, category: str = "us") -> float:
    """Calculate Bet Payout
    This function calculates the payout for a given bet.

    Args:
        risk (int, float): Unit size of your bankroll, typically 1% of bankroll (100)
        odds (int, float): Odds or Implied Win Probability for the bet
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds \n
            'prob', Implied Probability

    Returns:
        float: Payout of a bet
    """

    assert isinstance(risk, (int, float)), "risk must be numeric"
    assert isinstance(odds, (int, float)), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
        "prob",
    ], "input category must be either: ('us', 'dec', 'frac', 'prob')"

    if category == "dec":
        pass
    else:
        odds = convert_odds(odds, cat_in=category, cat_out="dec")[0]

    bets = {"odds": odds, "risk": risk}
    payout = round(bets["risk"] * bets["odds"], 2)

    return payout
