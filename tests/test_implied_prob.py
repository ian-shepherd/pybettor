import unittest
import numpy.testing as npt
from pybettor.implied_prob import implied_prob


class TestImpliedProb(unittest.TestCase):
    def test_implied_us_odds(self):
        odds = -350
        category = "us"
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.77777778)

        odds = 180
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.35714286)

    def test_implied_frac_odds(self):
        odds = 6 / 1
        category = "frac"
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.14285714)

        odds = 2 / 7
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.77777778)

    def test_implied_dec_odds(self):
        odds = 2.5
        category = "dec"
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.4)

        odds = 4.9
        npt.assert_almost_equal(implied_prob(odds, category)[0], 0.20408163)


if __name__ == "__main__":
    unittest.main()
