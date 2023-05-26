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

    assert type(odds) is list or isinstance(
        odds, (int, float)), 'odds must be numeric'
    assert cat_in in categories, "input category must be one of ('us', 'dec', 'frac', 'prob')"
    assert cat_out in categories + \
        ['all'], "output category must be one of ('all', 'us', 'dec', 'frac', 'prob')"
    assert cat_in != cat_out, "input and output categories must be different"

    if not isinstance(odds, list):
        odds = [odds]

    new_odds = {}

    if cat_in == 'us':
        assert all(isinstance(x, int)
                   for x in odds), 'us odds must be whole numbers'
        assert not any(x in range(-99, 100)
                       for x in odds), 'us odds cannot be between -99 and 99'

        if cat_out in ('all', 'dec'):
            new_odds['Decimal'] = _convert_us_odds(odds)
        if cat_out in ('all', 'frac'):
            new_odds['Fraction'] = _convert_us_to_frac(odds)
        if cat_out in ('all', 'prob'):
            new_odds['Implied Probability'] = implied_prob(odds, category='us')

    elif cat_in == 'dec':
        assert all(
            x >= 1 for x in odds), 'dec odds must be greater than or equal to 1'

        if cat_out in ('all', 'us'):
            new_odds['American'] = _convert_dec_odds(odds)
        if cat_out in ('all', 'frac'):
            new_odds['Fraction'] = _convert_dec_to_frac(odds)
        if cat_out in ('all', 'prob'):
            new_odds['Implied Probability'] = implied_prob(
                odds, category='dec')

    elif cat_in == 'frac':
        assert all(x > 0 for x in odds), 'frac odds must be greater than 0'

        if cat_out in ('all', 'us'):
            new_odds['American'] = _convert_frac_odds(odds)
        if cat_out in ('all', 'dec'):
            new_odds['Decimal'] = _convert_frac_to_dec(odds)
        if cat_out in ('all', 'prob'):
            new_odds['Implied Probability'] = implied_prob(
                odds, category='frac')

    elif cat_in == 'prob':
        if cat_out in ('all', 'us'):
            new_odds['American'] = implied_odds(odds, category='us')
        if cat_out in ('all', 'dec'):
            new_odds['Decimal'] = implied_odds(odds, category='dec')
        if cat_out in ('all', 'frac'):
            new_odds['Fraction'] = implied_odds(odds, category='frac')

    return new_odds
