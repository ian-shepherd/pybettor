from fractions import Fraction


def implied_odds(prob, category: str = "us") -> list or dict:
    """Bet Implied Odds
    Provides the fair odds for an event given the probability.

    Args:
        prob (float): probability of an event
        category (str, optional): type of odds. Defaults to "us". \n
            'all', returns all odds \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds

    Returns:
        list or dictionary: fair odds of a given event. Only returns a dictionary when category = 'all'
    """

    if type(prob) is not list:
        prob = [prob]

    assert all(isinstance(x, float) for x in prob), "probability must be numeric"
    assert all(x > 0 and x < 1 for x in prob), "probability must be between 0 and 1"
    assert category in [
        "us",
        "frac",
        "dec",
        "all",
    ], "category must be either: ('us', 'dec', 'frac', 'all')"

    if category == "all":
        us = [x / (1 - x) * -100 if x > 0.5 else (1 - x) / x * 100 for x in prob]
        dec = [round(1 / x, 2) for x in prob]
        frac = [Fraction(x - 1).limit_denominator(100) for x in dec]
        frac = [str(x.numerator) + "/" + str(x.denominator) for x in frac]
        prob = prob
        imp_odds = {
            "American": us,
            "Decimal": dec,
            "Fraction": frac,
            "Implied Probability": prob,
        }

    elif category == "us":
        imp_odds = [x / (1 - x) * -100 if x > 0.5 else (1 - x) / x * 100 for x in prob]
        imp_odds = [round(x) for x in imp_odds]

    elif category == "dec":
        imp_odds = [round(1 / x, 2) for x in prob]

    elif category == "frac":
        imp_odds = [Fraction((1.0 / x) - 1.0).limit_denominator(100) for x in prob]
        imp_odds = [str(x.numerator) + "/" + str(x.denominator) for x in imp_odds]

    return imp_odds
