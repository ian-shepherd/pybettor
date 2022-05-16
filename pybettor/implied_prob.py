def implied_prob(odds, category: str = "us"):
    """Provides the implied probability for an event given the odds

    Args:
        odds (str or list): odds of an event
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds

    Returns:
        list: implied probability of odds
    """

    if type(odds) is not list:
        odds = [odds]

    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "category must be either: ('us', 'dec', 'frac')"

    if category == "us":

        assert all(isinstance(x, int) for x in odds), "us odds must be a whole number"
        assert not any(
            x in range(-99, 100) for x in odds
        ), "us odds cannot be between -99 and 99"

        imp_prob = [1 / (1 - 100 / x) if x <= -100 else 1 / (1 + x / 100) for x in odds]

    elif category == "dec":

        assert all(x >= 1 for x in odds), "dec odds must be greater than 1"

        imp_prob = [1 / x for x in odds]

    elif category == "frac":

        assert all(x > 0 for x in odds), "frac odds must be greater than 0"

        imp_prob = [1 / (1 + x) for x in odds]

    return imp_prob
