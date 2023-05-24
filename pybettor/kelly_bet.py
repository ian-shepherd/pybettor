from fractions import Fraction
from .convert_odds import convert_odds


def kelly_bet(
    unit_size, win_prob, odds, category: str = "us", kelly_factor: int = 1
) -> int:
    """Kelly Criterion Bet Size
    This function calculates the Kelly Criterion and returns the dollar amount
    to bet in order to maximize returns.

    Reference: Kelly Criterion wikipedia(https://en.wikipedia.org/wiki/Kelly_criterion) page

    Args:
        unit_size (float): Unit size of your bankroll, typically 1% of bankroll (100)
        win_prob (float): Win Probability of bet
        odds (float): Odds or Implied Win Probability for the bet
        category (str, optional): : type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds \n
            'prob', Implied Probability
        kelly_factor (int, optional): Kelly Factor is used to shrink the kelly bet size.
            Half kelly (2), Quarter Kelly (4) are common in the sports betting world.
            Defaults to 1.

    Returns:
        int: Optimal bet size to risk on bet based on the kelly criterion and bankroll
    """

    assert isinstance(unit_size, (int, float)), "unit size must be numeric"
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
    bet_size = round(
        (
            ((bets["odds"] * bets["win_prob"]) - (1 - bets["win_prob"]))
            / bets["odds"]
            / kelly_factor
        )
        * unit_size
        * 100,
    )

    return bet_size
