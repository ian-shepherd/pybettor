from .convert_odds import convert_odds


def expected_value_calc(implied_probability: float, odds: float, category: str = "us") -> float:
    """Expected value calculator
    This function returns the expected value of given odds, based on the implied probability.

    Args:
        implied_probability (float): Win Probability of bet
        odds (float): Odds or Implied Win Probability for the bet
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds

    Returns:
        The expected value of the odds.
    """

    assert implied_probability >= 0, "implied probability must be in the range of 0 to 1 inclusive"
    assert implied_probability <= 1, "implied probability must be in the range of 0 to 1 inclusive"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "type must be either: ('us', 'dec', 'frac')"

    implied_loss_probability = 1 - implied_probability
    amount_returned = 100 * odds if category == 'dec' else 100 * convert_odds(
        odds, category, 'dec')[0]
    amount_won = amount_returned - 100
    return implied_probability * amount_won - implied_loss_probability * 100
