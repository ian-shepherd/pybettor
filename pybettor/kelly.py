from fractions import Fraction
from convert_odds import convert_odds


def kelly(win_prob, odds, category: str = "us", kelly_factor: int = 1):
    """Kelly Criterion Calculation
    This function calculates the Kelly Criterion percentage of your
    bankroll to bet in order to maximize returns.

    Reference: i[Kelly Criterion wikipedia](https://en.wikipedia.org/wiki/Kelly_criterion) page

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

    if type(win_prob) is not list:
        win_prob = [win_prob]

    if type(odds) is not list:
        odds = [odds]

    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert all(1.0 >= x >= 0.0 for x in win_prob), "Win Prob must be between 0 and 1"
    assert category in [
        "us",
        "frac",
        "dec",
        "prob",
    ], "input category must be either: ('us', 'dec', 'frac', 'prob')"

    odds = convert_odds(odds, cat_in=category, cat_out="frac")

    odds = [float(Fraction(x)) for x in odds]
    bets = {"odds": odds, "win_prob": win_prob}
    kelly_perc = []
    for i in range(len(bets["odds"])):
        kelly_perc_temp = round(
            ((bets["odds"][i] * bets["win_prob"][i]) - (1 - bets["win_prob"][i]))
            / bets["odds"][i],
            4,
        )
        kelly_perc_temp = round(kelly_perc_temp / kelly_factor, 4)
        print(f"Kelly Percentage: {kelly_perc_temp}")
        kelly_perc.append(kelly_perc_temp)

    return kelly_perc
