from fractions import Fraction
from .implied_odds import implied_odds
from .implied_prob import implied_prob


def convert_odds(odds, cat_in: str = "us", cat_out: str = "all") -> list or dict:
    """
    Odds Converter
    This function converts any odds or probability.

    Args:
        odds (float): Odds, or lines, for a given bet(s) (-115, -105)
        cat_in (str, optional): type of odds. Defaults to "us".
        cat_out (str, optional): type of odds. Defaults to "all".

    Returns:
        list or dictionary: Converted Odds
    """
    categories = ["us", "dec", "frac", "prob"]

    assert type(odds) is list or isinstance(
        odds, (int, float)), "odds must be numeric"
    assert cat_in in categories, "input category must be one of ('us', 'dec', 'frac', 'prob')"
    assert cat_out in categories + \
        ["all"], "output category must be one of ('all', 'us', 'dec', 'frac', 'prob')"
    assert cat_in != cat_out, "input and output categories must be different"

    if not isinstance(odds, list):
        odds = [odds]

    if cat_in == "us":
        assert all(isinstance(x, int)
                   for x in odds), "us odds must be whole numbers"
        assert not any(x in range(-99, 100)
                       for x in odds), "us odds cannot be between -99 and 99"

        if cat_out == "all":
            us = odds
            dec = [round(-100 / x + 1 if x <= -100 else x / 100 + 1, 2)
                   for x in odds]
            frac = [str(Fraction(-100 / x if x <= -100 else x /
                        100).limit_denominator(100)) for x in odds]
            prob = implied_prob(odds, category="us")
            new_odds = {
                "American": us,
                "Decimal": dec,
                "Fraction": frac,
                "Implied Probability": prob,
            }

        elif cat_out == "dec":
            new_odds = [round(-100 / x + 1 if x <= -
                              100 else x / 100 + 1, 2) for x in odds]

        elif cat_out == "frac":
            new_odds = [str(Fraction(-100 / x if x <= -100 else x /
                            100).limit_denominator(100)) for x in odds]

        elif cat_out == "prob":
            new_odds = implied_prob(odds, category="us")

    elif cat_in == "dec":
        assert all(
            x >= 1 for x in odds), "dec odds must be greater than or equal to 1"

        if cat_out == "all":
            us = [round((x - 1) * 100 if x >= 2 else -100 / (x - 1))
                  for x in odds]
            dec = odds
            frac = [str(Fraction(x - 1).limit_denominator(100)) for x in odds]
            prob = implied_prob(odds, category="dec")
            new_odds = {
                "American": us,
                "Decimal": dec,
                "Fraction": frac,
                "Implied Probability": prob,
            }

        elif cat_out == "us":
            new_odds = [round((x - 1) * 100 if x >= 2 else -
                              100 / (x - 1)) for x in odds]

        elif cat_out == "frac":
            new_odds = [str(Fraction(x - 1).limit_denominator(100))
                        for x in odds]

        elif cat_out == "prob":
            new_odds = implied_prob(odds, category="dec")

    elif cat_in == "frac":
        assert all(x > 0 for x in odds), "frac odds must be greater than 0"

        if cat_out == "all":
            us = [round(x * 100 if x >= 1 else -100 / x) for x in odds]
            dec = [round(x + 1, 2) for x in odds]
            frac = [str(Fraction(x).limit_denominator(100)) for x in odds]
            prob = implied_prob(odds, category="frac")
            new_odds = {
                "American": us,
                "Decimal": dec,
                "Fraction": frac,
                "Implied Probability": prob,
            }

        elif cat_out == "us":
            new_odds = [round(x * 100 if x >= 1 else -100 / x) for x in odds]

        elif cat_out == "dec":
            new_odds = [round(x + 1, 2) for x in odds]

        elif cat_out == "prob":
            new_odds = implied_prob(odds, category="frac")

    elif cat_in == "prob":
        if cat_out == "all":
            us = implied_odds(odds, category="us")
            dec = implied_odds(odds, category="dec")
            frac = implied_odds(odds, category="frac")
            prob = odds
            new_odds = {
                "American": us,
                "Decimal": dec,
                "Fraction": frac,
                "Implied Probability": prob,
            }

        elif cat_out == "us":
            new_odds = implied_odds(odds, category="us")

        elif cat_out == "dec":
            new_odds = implied_odds(odds, category="dec")

        elif cat_out == "frac":
            new_odds = implied_odds(odds, category="frac")

    return new_odds
