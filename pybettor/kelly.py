from fractions import Fraction
from .convert_odds import convert_odds


def kelly(win_prob, odds, category: str = "us", kelly_factor: int = 1) -> float:
    """Kelly Criterion Calculation
    This function calculates the Kelly Criterion percentage of your
    bankroll to bet in order to maximize returns.

    Reference: Kelly Criterion wikipedia(https://en.wikipedia.org/wiki/Kelly_criterion) page

    Args:
        win_prob (float): Win Probability of bet
        odds (float): Odds or Implied Win Probability for the bet
        category (str, optional): 'us', 'dec', 'frac', 'prob'
            Odds category.
            Defaults to "us".
        kelly_factor (int, optional): Kelly Factor is used to shrink the kelly bet size.
            Half kelly (2), Quarter Kelly (4) are common in the sports betting world.
            Defaults to 1.

    Returns:
        float: Optimal percentage of bankroll to risk on bet based on the kelly criterion
    """

    assert isinstance(odds, (int, float)), "odds must be numeric"
    assert win_prob < 1 and win_prob > 0, "Win Prob must be between 0 and 1"
    assert category in [
        "us",
        "frac",
        "dec",
        "prob",
    ], "input category must be either: ('us', 'dec', 'frac', 'prob')"

    odds = convert_odds(odds, cat_in=category, cat_out="frac")[0]
    odds = float(Fraction(odds))

    bets = {"odds": odds, "win_prob": win_prob}
    kelly_perc = round(
        (
            ((bets["odds"] * bets["win_prob"]) - (1 - bets["win_prob"]))
            / bets["odds"]
            / kelly_factor
        )
        * 100,
        2,
    )

    return kelly_perc
