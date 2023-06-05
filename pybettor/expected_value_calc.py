from .convert_odds import convert_odds


def expected_value_calc(
    prob: float, odds: float, category: str = "us", risk: float = 100
) -> float:
    """Expected value calculator
    Given probability and odds, return the expected value.

    Args:
        prob (float): Win Probability of bet
        odds (float): Odds or Implied Win Probability for the bet
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds
        risk (float, optional): Size of the bet. Defaults to 100.

    Returns:
        The expected value of the odds vs the prodability.
    """

    assert isinstance(prob, (int, float)), "probability must be numeric"
    assert 0 <= prob <= 1, "probability must be in the range of 0 to 1 inclusive"
    assert isinstance(odds, (int, float)), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "type must be either: ('us', 'dec', 'frac')"
    assert isinstance(risk, (int, float)), "bet_size must be numeric"
    assert risk > 0, "bet_size must be greater than 0"

    loss_prob = 1 - prob
    amount_returned = (
        risk * odds
        if category == "dec"
        else risk * convert_odds(odds, category, "dec")[0]
    )
    amount_won = amount_returned - risk

    return prob * amount_won - loss_prob * risk
