from fractions import Fraction
from convert_odds import convert_odds


def bet_calc(risk, odds, category: str = "us"):
    """Calculate Bet Payout
    This function calculates the payout for a given bet.

    Args:
        risk (float): Unit size of your bankroll, typically 1% of bankroll (100)
        odds (float): Odds or Implied Win Probability for the bet
        category (str, optional): 'us', 'dec', 'frac', 'prob'
            Odds category.
            Defaults to "us".

    Returns:
        List[float]: Payout of a bet
    """

    if type(risk) is not list:
        risk = [risk]

    if type(odds) is not list:
        odds = [odds]

    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
        "prob",
    ], "input category must be either: ('us', 'dec', 'frac', 'prob')"

    if category == "dec":
        pass
    else:
        odds = convert_odds(odds, cat_in=category, cat_out="dec")

    bets = {"odds": odds, "risk": risk}
    payout = []
    for i in range(len(bets["odds"])):
        ## the magic
        payout_temp = round(bets["risk"][i] * bets["odds"][i], 2)
        payout.append(payout_temp)

    return payout
