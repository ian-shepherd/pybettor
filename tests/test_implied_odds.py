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

    def test_implied_basic_odds(self):
        odds = [4.2, 3.7, 1.95]
        probs = [1 / x for x in odds]
        margin = 0.02118602
        odds = implied_odds(probs, category="dec", margin=margin, method="basic")
        npt.assert_almost_equal(odds, odds)

    def test_implied_wpo_odds(self):
        probs = [0.2310332, 0.2632083, 0.5057585]
        margin = 0.02118602
        odds = implied_odds(probs, category="dec", margin=margin, method="wpo")
        npt.assert_almost_equal(
            odds.get("implied_odds"),
            [4.200000554400074, 3.6999995017334, 1.9500000234000003],
        )
        npt.assert_almost_equal(
            odds.get("specific_margins"), [0.03056706, 0.02683049, 0.01396319]
        )

    def test_implied_odds_ratio_odds(self):
        probs = [0.2320048, 0.2636415, 0.5043537]
        margin = 0.02118602
        odds = implied_odds(probs, category="dec", margin=margin, method="odds_ratio")
        npt.assert_almost_equal(
            odds.get("implied_odds"),
            [4.19999514, 3.69999720, 1.95000182],
        )
        npt.assert_almost_equal(odds.get("odds_ratio"), 1.03445647)

    def test_implied_power_odds(self):
        probs = [0.2311414, 0.2630644, 0.5057941]
        margin = 0.02118602
        odds = implied_odds(probs, category="dec", margin=margin, method="power")
        npt.assert_almost_equal(
            odds.get("implied_odds"),
            [4.19999218, 3.69999545, 1.95000295],
        )
        npt.assert_almost_equal(odds.get("exponent"), 0.97976215)

    def test_implied_power_odds_no_margin(self):
        probs = [0.2311414, 0.2630644, 0.5057942]
        margin = 0
        odds = implied_odds(probs, category="dec", margin=margin, method="power")
        npt.assert_almost_equal(
            odds.get("implied_odds"),
            [4.32635607, 3.80135054, 1.97708870],
        )
        npt.assert_almost_equal(odds.get("exponent"), 1)

    def test_implied_additive_odds(self):
        probs = [0.2310332, 0.2632083, 0.5057585]
        margin = 0.02118602
        odds = implied_odds(probs, category="dec", margin=margin, method="additive")
        npt.assert_almost_equal(
            odds,
            [4.200000554400074, 3.6999995017334, 1.9500000234000003],
        )

    def test_implied_shin_odds(self):
        probs = [0.2315811, 0.2635808, 0.5048382]
        margin = 0.02118602
        odds = implied_odds(probs, category="dec", margin=margin, method="shin")
        npt.assert_almost_equal(
            odds.get("implied_odds"),
            [4.19983832, 3.69991362, 1.95005885],
        )
        npt.assert_almost_equal(odds.get("z_value"), 0.01060805)

    def test_implied_shin_odds_gross_margin(self):
        probs = [0.2315811, 0.2635808, 0.5048382]
        margin = 0.02118602
        gross_margin = 0.01
        odds = implied_odds(
            probs,
            category="dec",
            margin=margin,
            method="shin",
            gross_margin=gross_margin,
        )
        npt.assert_almost_equal(
            odds.get("implied_odds"),
            [4.21348251, 3.70719402, 1.94512092],
        )
        npt.assert_almost_equal(odds.get("z_value"), 0.00549115)

    def test_implied_balanced_book_odds(self):
        probs = [0.2299380, 0.2624575, 0.5076046]
        margin = 0.02118602
        odds = implied_odds(
            probs, category="dec", margin=margin, method="balanced_book"
        )
        npt.assert_almost_equal(
            odds.get("implied_odds"),
            [4.19999975, 3.70000001, 1.95000005],
        )
        npt.assert_almost_equal(odds.get("z_value"), 0.01059301)


if __name__ == "__main__":
    unittest.main()
