from .implied_prob import implied_prob


def clv_calc(
    bet_odds: int or float, close_odds: int or float, category: str = "us"
) -> float:
    """Calculate Closing Line Value
    This function calculates the closing line value (CLV) for a given bet.

    Args:
        bet_odds (int, float): Odds or Implied Win Probability for the bet
        close_odds (int, float): Closing Odds or Implied Win Probability for the bet
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds

    Returns:
        float: Closing Line Value (CLV) of a bet
    """

    assert isinstance(bet_odds, (int, float)), "bet_odds must be numeric"
    assert isinstance(close_odds, (int, float)), "close_odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "input category must be either: ('us', 'dec', 'frac')"

    bet_prob = implied_prob(bet_odds, category=category)[0]
    close_prob = implied_prob(close_odds, category=category)[0]

    clv = (close_prob - bet_prob) / bet_prob

    return clv
