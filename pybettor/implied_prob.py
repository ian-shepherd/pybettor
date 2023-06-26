from typing import Union  # noqa: F401
from scipy import optimize
import numpy as np
import warnings


def _implied_basic_prob(naive_prob):
    return [x / sum(naive_prob) for x in naive_prob]


def _implied_wpo_prob(odds, margin):
    num_outcomes = len(odds)
    imp_prob = [(num_outcomes - margin * x) / (num_outcomes * x) for x in odds]
    specific_margins = [margin * (1 / x) / num_outcomes for x in imp_prob]

    return imp_prob, specific_margins


def _implied_odds_ratio_prob(naive_prob):
    res = optimize.root_scalar(
        f=or_solvefor, bracket=[0.05, 5], method="brentq", args=(np.array(naive_prob),)
    )
    odds_ratio = res.root
    imp_prob = [or_func(odds_ratio, x) for x in naive_prob]

    return imp_prob, odds_ratio


def or_func(cc, io):
    return io / (cc + io - cc * io)


def or_solvefor(cc, io):
    tmp = or_func(cc, io)
    return np.sum(tmp) - 1


def _implied_power_prob(naive_prob):
    res = optimize.root_scalar(
        pwr_solvefor, bracket=[0.0001, 1], method="brentq", args=(naive_prob,)
    )
    exponent = res.root
    imp_prob = [pwr_func(exponent, x) for x in naive_prob]

    return imp_prob, exponent


def pwr_func(nn, io):
    return np.power(io, 1 / nn)


def pwr_solvefor(nn, io):
    tmp = pwr_func(nn, io)
    return np.sum(tmp) - 1


def _implied_additive_prob(naive_prob):
    imp_prob = [x - ((sum(naive_prob) - 1) / len(naive_prob)) for x in naive_prob]

    return imp_prob


def _implied_shin_prob(naive_prob, shin_method, gross_margin):
    num_outcomes = len(naive_prob)
    naive_prob = np.array(naive_prob)
    naive_prob_sum = np.sum(naive_prob)
    if shin_method == "uniroot" and gross_margin != 0:
        shin_method = "js"
        warnings.warn(
            "gross_margin is not used when shin_method is 'uniroot'. shin_method is set to 'js'."
        )

    if shin_method == "js":
        zz_tmp = 0

        imp_prob, zz_tmp = _calculate_shin_z_value_js(
            naive_prob, gross_margin, num_outcomes, naive_prob_sum
        )

    elif shin_method == "uniroot":
        imp_prob, zz_tmp = _calculate_shin_z_value_uniroot(naive_prob)

    z_value = zz_tmp

    return imp_prob, z_value


def _calculate_shin_z_value_js(naive_prob, gross_margin, num_outcomes, naive_prob_sum):
    zz_tmp = 0

    for jj in range(1000):
        zz_prev = zz_tmp
        zz_tmp = (
            np.sum(
                np.sqrt(
                    zz_prev**2
                    + 4
                    * (1 - zz_prev)
                    * (((naive_prob**2 * (1 - gross_margin))) / naive_prob_sum)
                )
            )
            - 2
        ) / (num_outcomes - 2)

        if np.abs(zz_tmp - zz_prev) <= np.finfo(float).eps ** 0.25:
            break
        elif jj == 999:
            warnings.warn("shin did not converge")

        imp_prob = shin_func(zz_tmp, naive_prob)

    return imp_prob, zz_tmp


def _calculate_shin_z_value_uniroot(naive_prob):
    res = optimize.root_scalar(
        f=shin_solvefor, bracket=[0, 0.4], method="brentq", args=(naive_prob,)
    )
    zz_tmp = res.root
    imp_prob = shin_func(zz_tmp, naive_prob)

    return imp_prob, zz_tmp


def shin_func(zz, io):
    bb = np.sum(io)
    return (np.sqrt(zz**2 + 4 * (1 - zz) * ((io**2) / bb)) - zz) / (2 * (1 - zz))


def shin_solvefor(zz, io):
    tmp = shin_func(zz, io)
    return 1 - np.sum(tmp)


def _implied_balanced_book_prob(naive_prob, gross_margin):
    num_outcomes = len(naive_prob)

    zz = ((1 - gross_margin) * sum(naive_prob) - 1) / (num_outcomes - 1)
    imp_probs = [(((1 - gross_margin) * x) - zz) / (1 - zz) for x in naive_prob]

    return imp_probs, zz


def _implied_jsd_prob(naive_prob):
    res = optimize.root_scalar(
        f=jsd_solvefor,
        bracket=[0.0000001, 0.1],
        method="brentq",
        args=(naive_prob,),
        xtol=0.0000001,
    )
    distance = res.root
    imp_prob = jsd_func(distance, naive_prob)

    return imp_prob, distance


def kld(x, y):
    return np.sum(x * np.log(x / y))


def binom_jsd(p, io):
    pvec = np.array([p, 1 - p])
    iovec = np.array([io, 1 - io])

    mm = (pvec + iovec) / 2
    return np.sqrt((kld(pvec, mm) / 2) + (kld(iovec, mm) / 2))


def jsd_func(jsd, io):
    def tosolve(p, io, jsd):
        return binom_jsd(p, io) - jsd

    pp = np.zeros(len(io))
    for ii in range(len(io)):
        res = optimize.root_scalar(
            f=tosolve,
            bracket=[0.00001, io[ii]],
            method="brentq",
            args=(io[ii], jsd),
        )
        pp[ii] = res.root

    return pp


def jsd_solvefor(jsd, io):
    return np.sum(jsd_func(jsd, io)) - 1


def implied_prob(
    odds: Union[int, float, list],
    category: str = "us",
    method: str = "naive",
    shin_method: str = "js",
    gross_margin: float = 0,
    normalize: bool = True,
) -> list or dict:
    """Bet Implied Probability
    This function calculates the implied probability for an event given the odds.

    Methodology are based on the R package 'implied' by Joshua Ulrich
    (https://cran.r-project.org/web/packages/implied/vignettes/introduction.html)
    (https://cran.r-project.org/web/packages/implied/implied.pdf)


    Args:
        odds (int, float, list): odds of an event
        category (str, optional): type of odds. Defaults to "us". \n
            'us', American Odds \n
            'dec', Decimal Odds \n
            'frac', Fractional Odds
        method (str, optional): method to calculate implied probability. Defaults to "naive". \n
            'naive', naive implied probability \n
            'basic', basic implied probability \n
            'wpo', weighted probability odds \n
            'odds_ratio', odds ratio \n
            'power', power \n
            'additive', additive \n
            'shin', shin \n
            'balanced_book', balanced book \n
            'jsd', jensen-shannon divergence
        shin_method (str, optional): method to calculate shin implied probability. Defaults to "js". \n
            'js', jensen-shannon divergence \n
            'uniroot', uniroot
        gross_margin (float, optional): gross margin of sportsbook. Defaults to 0.
        normalize (bool, optional): normalize implied probability to sum to 1 if method is not naive. Defaults to True.


    Returns:
        list or dictionary: implied probability
            Only returns a list if method='naive'
    """

    odds = [odds] if not isinstance(odds, list) else odds

    assert all(isinstance(x, (int, float)) for x in odds), "odds must be numeric"
    assert category in [
        "us",
        "frac",
        "dec",
    ], "category must be either: ('us', 'dec', 'frac')"
    assert method in [
        "naive",
        "basic",
        "wpo",
        "odds_ratio",
        "power",
        "additive",
        "shin",
        "balanced_book",
        "jsd",
    ], "method must be either: ('naive', 'basic', 'wpo', 'odds_ratio', 'power', 'additive', 'shin', 'balanced_book', 'jsd')"  # noqa: E501

    # category assertions
    if category == "us":
        assert all(isinstance(x, int) for x in odds), "us odds must be a whole number"
        assert not any(
            x in range(-99, 100) for x in odds
        ), "us odds cannot be between -99 and 99"
    elif category == "dec":
        assert all(x >= 1 for x in odds), "dec odds must be greater than 1"
    elif category == "frac":
        assert all(x > 0 for x in odds), "frac odds must be greater than 0"

    # calculate naive probability
    category_formulas = {
        "us": lambda x: 1 / (1 - 100 / x) if x <= -100 else 1 / (1 + x / 100),
        "dec": lambda x: 1 / x,
        "frac": lambda x: 1 / (1 + x),
    }
    naive_prob = [category_formulas[category](x) for x in odds]

    # build dictionary
    margin = np.sum(naive_prob) - 1
    mydict = {"naive_prob": naive_prob, "margin": margin}

    if method == "naive":
        return naive_prob
    elif method == "basic":
        imp_prob = _implied_basic_prob(naive_prob)
    elif method == "wpo":
        assert (
            category == "dec"
        ), "wpo method only works with decimal odds, use convert_odds() to convert odds to decimal"
        imp_prob, specific_margins = _implied_wpo_prob(odds, margin)
        mydict["specific_margins"] = specific_margins
    elif method == "odds_ratio":
        imp_prob, odds_ratio = _implied_odds_ratio_prob(naive_prob)
        mydict["odds_ratio"] = odds_ratio
    elif method == "power":
        imp_prob, exponent = _implied_power_prob(naive_prob)
        mydict["exponent"] = exponent
    elif method == "additive":
        imp_prob = _implied_additive_prob(naive_prob)
    elif method == "shin":
        imp_prob, z_value = _implied_shin_prob(naive_prob, shin_method, gross_margin)
        mydict["z_value"] = z_value
    elif method == "balanced_book":
        imp_prob, z_value = _implied_balanced_book_prob(naive_prob, gross_margin)
        mydict["z_value"] = z_value
    elif method == "jsd":
        imp_prob, distance = _implied_jsd_prob(naive_prob)
        mydict["distance"] = distance

    # Normalize
    if normalize:
        imp_prob = [x / sum(imp_prob) for x in imp_prob]

    # warn if probabilities outside of [0,1]
    if any(x < 0 for x in imp_prob) or any(x > 1 for x in imp_prob):
        warnings.warn("implied probabilities outside of [0,1]")

    mydict["implied_prob"] = imp_prob

    # sort dictionary
    sort_order = [
        "naive_prob",
        "implied_prob",
        "margin",
        "specific_margins",
        "odds_ratio",
        "exponent",
        "z_value",
        "distance",
    ]
    mydict = {k: mydict[k] for k in sort_order if k in mydict}

    return mydict
