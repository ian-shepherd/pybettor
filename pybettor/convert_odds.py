from fractions import Fraction
from .implied_odds import implied_odds
from .implied_prob import implied_prob


def _convert_dec_to_us_odds(odds):
    new_odds = [(x - 1) * 100 if x >= 2 else -100 / (x - 1) for x in odds]
    new_odds = [round(x) for x in new_odds]
    return new_odds


def _convert_frac_to_us_odds(odds):
    new_odds = [x * 100 if x >= 1 else -100 / x for x in odds]
    new_odds = [round(x) for x in new_odds]
    return new_odds


def _convert_us_to_dec(odds):
    new_odds = [-100 / x + 1 if x <= -100 else x / 100 + 1 for x in odds]
    new_odds = [round(x, 4) for x in new_odds]
    return new_odds


def _convert_us_to_frac(odds):
    new_odds = [-100 / x if x <= -100 else x / 100 for x in odds]
    new_odds = [Fraction(x).limit_denominator(100) for x in new_odds]
    new_odds = [str(x.numerator) + "/" + str(x.denominator) for x in new_odds]
    return new_odds


def _convert_dec_to_frac(odds):
    new_odds = [Fraction(x - 1).limit_denominator(100) for x in odds]
    new_odds = [str(x.numerator) + "/" + str(x.denominator) for x in new_odds]
    return new_odds


def _convert_frac_to_dec(odds):
    return [round(x + 1, 4) for x in odds]


def _convert_frac_to_frac(odds):
    frac = [Fraction(x).limit_denominator(100) for x in odds]
    frac = [str(x.numerator) + "/" + str(x.denominator) for x in frac]
    return frac


def convert_odds(odds, cat_in="us", cat_out="all") -> list or dict:
    """Odds Converter
    This function converts any odds or probability.

    Args:
        odds (float): Odds, or lines, for a given bet(s) (-115, -105)
        cat_in (str, optional):  \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds \n
            'prob', Implied Probability
        cat_out (str, optional): type of odds. Defaults to "all". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds \n
            'prob', Implied Probability

    Returns:
        list or dictionary: Converted Odds
    """
    categories = ["us", "dec", "frac", "prob"]

    assert isinstance(odds, (int, float, list)), "odds must be numeric"
    assert (
        cat_in in categories
    ), "input category must be one of ('us', 'dec', 'frac', 'prob')"
    assert cat_out in categories + [
        "all"
    ], "output category must be one of ('all', 'us', 'dec', 'frac', 'prob')"
    assert cat_in != cat_out, "input and output categories must be different"

    if not isinstance(odds, list):
        odds = [odds]

    conversions = {
        ("us", "us"): lambda x: odds,
        ("us", "dec"): _convert_us_to_dec,
        ("us", "frac"): _convert_us_to_frac,
        ("us", "prob"): lambda odds: implied_prob(odds, category="us"),
        ("dec", "dec"): lambda x: odds,
        ("dec", "us"): _convert_dec_to_us_odds,
        ("dec", "frac"): _convert_dec_to_frac,
        ("dec", "prob"): lambda odds: implied_prob(odds, category="dec"),
        ("frac", "frac"): _convert_frac_to_frac,
        ("frac", "us"): _convert_frac_to_us_odds,
        ("frac", "dec"): _convert_frac_to_dec,
        ("frac", "prob"): lambda odds: implied_prob(odds, category="frac"),
        ("prob", "prob"): lambda x: odds,
        ("prob", "us"): lambda odds: implied_odds(odds, category="us"),
        ("prob", "dec"): lambda odds: implied_odds(odds, category="dec"),
        ("prob", "frac"): lambda odds: implied_odds(odds, category="frac"),
    }

    display_odds_key = {
        "us": "American",
        "dec": "Decimal",
        "frac": "Fraction",
        "prob": "Implied Probability",
    }

    new_odds = {}

    if cat_out == "all":
        cat_out = categories
        for category_out in cat_out:
            key = (cat_in, category_out)
            new_odds[display_odds_key[category_out]] = conversions[key](odds)
    else:
        key = (cat_in, cat_out)
        new_odds = conversions[key](odds)

    return new_odds
