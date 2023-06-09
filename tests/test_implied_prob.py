import unittest
import numpy.testing as npt
from pybettor.implied_prob import implied_prob


class TestImpliedProb(unittest.TestCase):
    def test_naive_implied_us_odds(self):
        odds = -350
        category = "us"
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.77777778)

        odds = 180
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.35714286)

    def test_naive_implied_frac_odds(self):
        odds = 6 / 1
        category = "frac"
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.14285714)

        odds = 2 / 7
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.77777778)

    def test_naive_implied_dec_odds(self):
        odds = 2.5
        category = "dec"
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.4)

        odds = 4.9
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.20408163)

    def test_basic_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="basic")
        npt.assert_almost_equal(
            probs.get("naive_prob"), [0.23809524, 0.27027027, 0.51282051]
        )
        npt.assert_almost_equal(
            probs.get("implied_prob"), [0.23315559, 0.26466311, 0.50218128]
        )
        npt.assert_almost_equal(probs.get("margin"), 0.02118602)

    def test_wpo_assertion_error(self):
        odds = [-110, -110]
        category = "us"
        with self.assertRaises(AssertionError):
            implied_prob(odds, category, method="wpo")

    def test_wpo_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="wpo")
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.23103323, 0.26320826, 0.50575850],
        )
        npt.assert_almost_equal(
            probs.get("specific_margins"), [0.03056706, 0.02683049, 0.01396319]
        )

    def test_odds_ratio_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="odds_ratio")
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.23200452, 0.26364129, 0.50435417],
        )
        npt.assert_almost_equal(probs.get("odds_ratio"), 1.03445647)

    def test_power_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="power")
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.23114097, 0.26306409, 0.50579492],
        )
        npt.assert_almost_equal(probs.get("exponent"), 0.97976215)

    def test_additive_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="additive")
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.23103323, 0.26320826, 0.50575850],
        )

    def test_shin_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="shin")
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.23158105, 0.26358076, 0.50483817],
        )
        npt.assert_almost_equal(probs.get("z_value"), 0.01066652)

    def test_shin_implied_odds_gross_margin(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        gross_margin = 0.01
        probs = implied_prob(odds, category, method="shin", gross_margin=gross_margin)
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.2323284, 0.2640952, 0.5035764],
        )
        npt.assert_almost_equal(probs.get("z_value"), 0.00543179)

    def test_shin_implied_odds_shin_method(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        shin_method = "uniroot"
        probs = implied_prob(odds, category, method="shin", shin_method=shin_method)
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.231572, 0.2635745, 0.5048535],
        )
        npt.assert_almost_equal(probs.get("z_value"), 0.01060805)

    def test_balanced_book_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="balanced_book")
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.22993796, 0.26245747, 0.50760456],
        )
        npt.assert_almost_equal(probs.get("z_value"), 0.01059301)

    def test_jsd_implied_odds(self):
        odds = [4.2, 3.7, 1.95]
        category = "dec"
        probs = implied_prob(odds, category, method="jsd")
        npt.assert_almost_equal(
            probs.get("implied_prob"),
            [0.23152161, 0.26341082, 0.50506756],
        )
        npt.assert_almost_equal(probs.get("distance"), 0.00548306)


if __name__ == "__main__":
    unittest.main()
