import unittest
import numpy.testing as npt
from pybettor.implied_odds import implied_odds


class TestImpliedOdds(unittest.TestCase):
    def test_implied_us_odds(self):
        prob = 0.75
        category = "us"
        npt.assert_almost_equal(implied_odds(prob, category)[0], -300)

    def test_implied_frac_odds(self):
        prob = 0.75
        category = "frac"

        odds = implied_odds(prob, category)[0]
        odds = odds.split("/")
        odds = float(odds[0]) / float(odds[1])
        npt.assert_almost_equal(odds, 1 / 3)

    def test_implied_dec_odds(self):
        prob = 0.75
        category = "dec"
        npt.assert_almost_equal(implied_odds(prob, category)[0], 1.33)

    def test_implied_all_odds(self):
        prob = 0.75
        category = "all"
        odds = implied_odds(prob, category)
        american = odds.get("American")[0]
        decimal = odds.get("Decimal")[0]
        fractional = odds.get("Fraction")[0]
        fractional = fractional.split("/")
        fractional = float(fractional[0]) / float(fractional[1])
        implied_prob = odds.get("Implied Probability")[0]

        npt.assert_almost_equal(
            [american, fractional, decimal, implied_prob], [-300, 33 / 100, 1.33, 0.75]
        )


if __name__ == "__main__":
    unittest.main()
