from implied_prob import implied_prob


def true_probability(line: float, odds, category: str = "us"):
    """_summary_

    Args:
        line (float): _description_
        odds (_type_): _description_
        category (str, optional): _description_. Defaults to "us".

    Returns:
        _type_: _description_
    """

    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "category must be either: ('us', 'dec', 'frac')"

    true_prob = implied_prob(odds=line, category=category)[0] / sum(
        implied_prob(odds=odds, category=category)
    )

    return true_prob
