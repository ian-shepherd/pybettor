from .implied_prob import implied_prob
from .true_probability import true_probability
import pandas as pd


def true_implied_prob(line: float, odds, category: str = "us"):
    """Bet Implied Probability
    This function calculates the implied probability of a bet given the odds.

    Args:
        odds (float): _description_
        category (str, optional): type of odds. Defaults to "us".

    Returns:
        float: probability
    """

    assert isinstance(line, (int, float)), "line much be numeric"
    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "category must be either: ('us', 'dec', 'frac')"

    true_prob = true_probability(line=line, odds=odds, category=category)
    imp_prob = implied_prob(odds=line, category=category)

    df = pd.DataFrame(
        list(zip([true_prob], imp_prob)), columns=["true_prob", "imp_prob"]
    )

    return df
