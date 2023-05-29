from .implied_prob import implied_prob
from .implied_odds import implied_odds


def fair_odds(
    line: int or float = -110, odds: list = [-110, -110], category: str = "us"
) -> float:
    """Calculates the fair offs for a bet.

    Args:
        line (int or loat, optional): line of bet. Defaults to -110.
        odds (list, optional): odds of all sides. Defaults to [-110, -110].
        category (str): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds

    Returns:
        float: fair odds
    """

    assert isinstance(line, (int, float)), "line must be numeric"
    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "type must be either: ('us', 'dec', 'frac')"

    true_prob = implied_prob(odds=line, category=category)[0] / sum(
        implied_prob(odds=odds, category=category)
    )

    fair_odds = implied_odds(true_prob, category=category)[0]

    return fair_odds
