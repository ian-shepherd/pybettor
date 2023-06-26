from typing import Union
from fractions import Fraction
from scipy import optimize
import numpy as np


def _convert_dec_odds(odds, cat_out, prob):
    if cat_out == "us":
        new_odds = _convert_dec_to_us_odds(odds)
    elif cat_out == "frac":
        new_odds = _convert_dec_to_frac(odds)
    elif cat_out == "dec":
        new_odds = odds
    elif cat_out == "all":
        new_odds = {
            "American": _convert_dec_to_us_odds(odds),
            "Decimal": odds,
            "Fraction": _convert_dec_to_frac(odds),
            "Implied Probability": prob,
        }

    return new_odds


def _convert_dec_to_us_odds(odds):
    new_odds = [(x - 1) * 100 if x >= 2 else -100 / (x - 1) for x in odds]
    new_odds = [round(x) for x in new_odds]
    return new_odds


def _convert_dec_to_frac(odds):
    new_odds = [Fraction(x - 1).limit_denominator(100) for x in odds]
    new_odds = [str(x.numerator) + "/" + str(x.denominator) for x in new_odds]
    return new_odds


def _implied_naive_odds(prob, category):
    if category == "all":
        us = [x / (1 - x) * -100 if x > 0.5 else (1 - x) / x * 100 for x in prob]
        dec = [round(1 / x, 2) for x in prob]
        frac = [Fraction(x - 1).limit_denominator(100) for x in dec]
        frac = [str(x.numerator) + "/" + str(x.denominator) for x in frac]
        prob = prob
        imp_odds = {
            "American": us,
            "Decimal": dec,
            "Fraction": frac,
            "Implied Probability": prob,
        }

    elif category == "us":
        imp_odds = [x / (1 - x) * -100 if x > 0.5 else (1 - x) / x * 100 for x in prob]
        imp_odds = [round(x) for x in imp_odds]

    elif category == "dec":
        imp_odds = [round(1 / x, 2) for x in prob]

    elif category == "frac":
        imp_odds = [Fraction((1.0 / x) - 1.0).limit_denominator(100) for x in prob]
        imp_odds = [str(x.numerator) + "/" + str(x.denominator) for x in imp_odds]

    return imp_odds


def _implied_basic_odds(prob, margin):
    return [1 / (x * (1 + margin)) for x in prob]


def _implied_wpo_odds(prob, margin):
    num_outcomes = len(prob)
    naive_odds = [1 / x for x in prob]
    specific_margins = [(margin * x) / num_outcomes for x in naive_odds]
    imp_odds = [x / (1 + y) for x, y in zip(naive_odds, specific_margins)]
    return imp_odds, specific_margins


def _implied_odds_ratio_odds(prob, margin):
    if margin != 0:
        res = optimize.root_scalar(
            f=or_solvefor,
            bracket=[0.05, 5],
            method="brentq",
            args=(np.array(prob), margin),
        )
        odds_ratio = res.root
    else:
        odds_ratio = 1

    imp_odds = [1 / or_func(cc=odds_ratio, probs=x) for x in prob]

    return imp_odds, odds_ratio


def or_func(cc, probs):
    or_probs = cc * probs
    return or_probs / (1 - probs + or_probs)


def or_solvefor(cc, probs, margin):
    tmp = or_func(cc, probs)
    return np.sum(tmp) - (1 + margin)


def _implied_power_odds(prob, margin):
    if margin != 0:
        res = optimize.root_scalar(
            f=pwr_solvefor,
            bracket=[0.0001, 1.1],
            method="brentq",
            args=(np.array(prob), margin),
        )
        exponent = res.root
    else:
        exponent = 1

    imp_odds = [1 / pwr_func(nn=exponent, probs=x) for x in prob]

    return imp_odds, exponent


def pwr_func(nn, probs):
    return np.power(probs, nn)


def pwr_solvefor(nn, probs, margin):
    tmp = pwr_func(nn, probs)
    return np.sum(tmp) - (1 + margin)


def _implied_additive_odds(probs, margin):
    imp_odds = [1 / (x + (margin / len(probs))) for x in probs]
    return imp_odds


def _implied_shin_odds(prob, margin, gross_margin):
    if margin != 0:
        res = optimize.root_scalar(
            f=shin_solvefor,
            bracket=[0, 0.4],
            method="brentq",
            args=(np.array(prob), margin, gross_margin),
        )
        zz = res.root
    else:
        zz = 0

    imp_odds = 1 / shin_func(zz, np.array(prob), gross_margin)

    return imp_odds, zz


def shin_func(zz, probs, gross_margin):
    yy = np.sqrt((zz * probs) + ((1 - zz) * probs**2))
    res = yy * np.sum(yy)

    if gross_margin is not None:
        res = res / (1 - gross_margin)

    return res


def shin_solvefor(zz, probs, margin, gross_margin):
    tmp = shin_func(zz, probs, gross_margin)
    return np.sum(tmp) - (1 + margin)


def _implied_balanced_book_odds(prob, margin, gross_margin):
    num_outcomes = len(prob)

    if gross_margin is None:
        gross_margin = 0

    zz = (((1 - gross_margin) * (1 + margin)) - 1) / (num_outcomes - 1)
    imp_odds = [
        1 / ((1 + margin) * (((x * (1 - zz)) + zz) / ((num_outcomes - 1) * zz + 1)))
        for x in prob
    ]

    return imp_odds, zz


def implied_odds(
    prob: Union[int, float, list],
    category: str = "us",
    method: str = "naive",
    margin: float = 0,
    gross_margin: float = None,
    normalize: bool = True,
) -> list or dict:
    """Bet Implied Odds
    Provides the fair odds for an event given the probability.

    Methodology are based on the R package 'implied' by Joshua Ulrich
    (https://cran.r-project.org/web/packages/implied/vignettes/introduction.html)
    (https://cran.r-project.org/web/packages/implied/implied.pdf)

    Args:
        prob (int, float, list): probability of an event
        category (str, optional): type of odds. Defaults to "us". \n
            'all', returns all odds \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds
        method (str, optional): method to calculate implied odds. Defaults to "naive". \n
            'naive', naive implied odds \n
            'basic', basic implied odds \n
            'wpo', weighted probability odds \n
            'odds_ratio', odds ratio \n
            'power', power \n
            'additive', additive \n
            'shin', shin \n
            'balanced_book', balanced book
        margin (float, optional): margin to apply to odds. Defaults to 0.
        gross_margin (float, optional): gross margin to apply to odds. Defaults to None.
        normalize (bool, optional): normalize implied odds to sum to 1 if method is not naive. Defaults to True.

    Returns:
        list or dictionary: fair odds of a given event.
            Only returns list when category != 'all' or method in ('naive', 'basic', 'additive')
    """

    if type(prob) is not list:
        prob = [prob]

    assert all(isinstance(x, float) for x in prob), "probability must be numeric"
    assert all(x > 0 and x < 1 for x in prob), "probability must be between 0 and 1"
    assert category in [
        "us",
        "frac",
        "dec",
        "all",
    ], "category must be either: ('us', 'dec', 'frac', 'all')"
    assert method in [
        "naive",
        "basic",
        "wpo",
        "odds_ratio",
        "power",
        "additive",
        "shin",
        "balanced_book",
    ], "method must be either: ('naive', 'basic', 'wpo', 'odds_ratio', 'power', 'additive', 'shin', 'balanced_book')"
    assert isinstance(margin, (int, float)), "margin must be numeric"
    assert margin >= 0, "margin must be greater than or equal to 0"
    assert (
        isinstance(gross_margin, (int, float)) or gross_margin is None
    ), "gross_margin must be numeric or None"
    assert gross_margin is None or (
        gross_margin >= 0 and gross_margin < 1
    ), "gross_margin must be None or between 0 and 1"
    if len(prob) > 1 and method != "naive":
        assert (
            np.sum(prob) >= 1 - margin
        ), "sum of probabilities must be greater than or equal to 1 - margin"

    if normalize:
        balanced_prob = [x / np.sum(prob) for x in prob]
    else:
        balanced_prob = prob

    mydict = {}

    if method == "naive":
        imp_odds = _implied_naive_odds(prob, category)
        return imp_odds
    elif method == "basic":
        imp_odds = _implied_basic_odds(balanced_prob, margin)
        imp_odds = _convert_dec_odds(imp_odds, category, prob)
        return imp_odds
    elif method == "wpo":
        imp_odds, specific_margins = _implied_wpo_odds(balanced_prob, margin)
        mydict["specific_margins"] = specific_margins
    elif method == "odds_ratio":
        imp_odds, odds_ratio = _implied_odds_ratio_odds(balanced_prob, margin)
        mydict["odds_ratio"] = odds_ratio
    elif method == "power":
        imp_odds, exponent = _implied_power_odds(balanced_prob, margin)
        mydict["exponent"] = exponent
    elif method == "additive":
        imp_odds = _implied_additive_odds(balanced_prob, margin)
        imp_odds = _convert_dec_odds(imp_odds, category, prob)
        return imp_odds
    elif method == "shin":
        imp_odds, z_value = _implied_shin_odds(balanced_prob, margin, gross_margin)
        mydict["z_value"] = z_value
    elif method == "balanced_book":
        imp_odds, z_value = _implied_balanced_book_odds(
            balanced_prob, margin, gross_margin
        )
        mydict["z_value"] = z_value

    imp_odds = _convert_dec_odds(imp_odds, category, prob)
    mydict["implied_odds"] = imp_odds

    # sort dictionary
    sort_order = [
        "implied_odds",
        "specific_margins",
        "odds_ratio",
        "exponent",
        "z_value",
    ]
    mydict = {key: mydict[key] for key in sort_order if key in mydict}

    return mydict
