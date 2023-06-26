from .implied_prob import implied_prob


def edge_calc(
    win_prob: int or float, odds: int or float, category: str = "us"
) -> float:
    """Calculate the edge of a bet given the win probability and odds.

    Args:
        win_prob (intorfloat): _description_
        odds (intorfloat): _description_
        category (str, optional): _description_. Defaults to "us".

    Returns:
        float: edge of the bet
    """

    assert isinstance(win_prob, (int, float)), "win_prob must be numeric"
    assert 0 <= win_prob <= 1, "win_prob must be in the range of 0 to 1 inclusive"
    assert isinstance(odds, (int, float)), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
        "prob",
    ], "input category must be either: ('us', 'dec', 'frac', 'prob')"

    edge = win_prob - implied_prob(odds, category=category)[0]

    return edge
