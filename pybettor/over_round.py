from .implied_prob import implied_prob


def over_round(lines, category: str = "us") -> float:
    """Sportsbook's Over Round Percentage
    This function calculates the extra implied probability
    from each line of the bet, known as the House Edge or Over Round.

    Args:
        lines List[float]: Win Probability of bet [-115, -105]
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds \n
            'prob', Implied Probability


    Returns:
        float: Bet's Over Round percent
    """

    if type(lines) is not list:
        lines = [lines]

    assert all(isinstance(x, (int, float))
               for x in lines), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
        "prob",
    ], "input category must be either: ('us', 'dec', 'frac', 'prob')"

    if category == "prob":
        probs = lines
    else:
        probs = implied_prob(lines, category)

    house_edge = sum(probs) - 1

    return house_edge
