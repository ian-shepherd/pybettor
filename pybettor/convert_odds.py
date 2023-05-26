from fractions import Fraction
from .implied_odds import implied_odds
from .implied_prob import implied_prob


def _convert_us_odds(odds):
    return [-100 / x + 1 if x <= -100 else x / 100 + 1 for x in odds]


def _convert_us_to_frac(odds):
    return [str(Fraction(-100 / x if x <= -100 else x / 100).limit_denominator(100)) for x in odds]


def _convert_dec_odds(odds):
    return [(x - 1) * 100 if x >= 2 else -100 / (x - 1) for x in odds]


def _convert_dec_to_frac(odds):
    return [str(Fraction(x - 1).limit_denominator(100)) for x in odds]


def _convert_frac_odds(odds):
    return [x * 100 if x >= 1 else -100 / x for x in odds]


def _convert_frac_to_dec(odds):
    return [x + 1 for x in odds]


def convert_odds(odds, cat_in='us', cat_out='all'):
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
    categories = ['us', 'dec', 'frac', 'prob']

    assert isinstance(odds, (int, float, list)), 'odds must be numeric'
    assert cat_in in categories, "input category must be one of ('us', 'dec', 'frac', 'prob')"
    assert cat_out in categories + \
        ['all'], "output category must be one of ('all', 'us', 'dec', 'frac', 'prob')"
    assert cat_in != cat_out, "input and output categories must be different"

    if not isinstance(odds, list):
        odds = [odds]

    conversions = {
        ('us', 'dec'): _convert_us_odds,
        ('us', 'frac'): _convert_us_to_frac,
        ('us', 'prob'): lambda odds: implied_prob(odds, category='us'),
        ('dec', 'us'): _convert_dec_odds,
        ('dec', 'frac'): _convert_dec_to_frac,
        ('dec', 'prob'): lambda odds: implied_prob(odds, category='dec'),
        ('frac', 'us'): _convert_frac_odds,
        ('frac', 'dec'): _convert_frac_to_dec,
        ('frac', 'prob'): lambda odds: implied_prob(odds, category='frac'),
        ('prob', 'us'): lambda odds: implied_odds(odds, category='us'),
        ('prob', 'dec'): lambda odds: implied_odds(odds, category='dec'),
        ('prob', 'frac'): lambda odds: implied_odds(odds, category='frac')
    }

    new_odds = {}

    if cat_out == 'all':
        cat_out = categories

    for category_in in cat_in:
        for category_out in cat_out:
            key = (category_in, category_out)
            if key in conversions:
                new_odds[category_out.capitalize()] = conversions[key](odds)

    return new_odds
