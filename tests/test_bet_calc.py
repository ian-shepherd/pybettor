import numpy.testing as npt
from pybettor import bet_calc


def test_bet_calc():
    risk = 100
    odds = -110
    npt.assert_almost_equal(bet_calc(risk, odds), -11000)

    risk = 50
    odds = 1.75
    npt.assert_almost_equal(bet_calc(risk, odds, category="dec"), 87.5)

    risk = 200
    odds = "5/2"
    npt.assert_almost_equal(bet_calc(risk, odds, category="frac"), 1000)

    risk = 300
    odds = 0.6
    npt.assert_almost_equal(bet_calc(risk, odds, category="prob"), 180)

    risk = 100
    odds = -200
    category = "invalid"
    try:
        bet_calc(risk, odds, category=category)
    except AssertionError as e:
        assert str(
            e) == "input category must be either: ('us', 'dec', 'frac', 'prob')"

    risk = "100"
    odds = -200
    try:
        bet_calc(risk, odds)
    except AssertionError as e:
        assert str(e) == "risk must be numeric"

    risk = 100
    odds = "invalid"
    try:
        bet_calc(risk, odds)
    except AssertionError as e:
        assert str(e) == "odds must be numeric"
