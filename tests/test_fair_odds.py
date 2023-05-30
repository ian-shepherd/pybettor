import unittest
import numpy.testing as npt
from pybettor.fair_odds import fair_odds


class TestFairOdds(unittest.TestCase):
    def test_fair_odds(self):
        line = 1.8
        odds = [1.8, 2.1]
        category = "dec"
        npt.assert_almost_equal(fair_odds(line, odds, category), 1.86)

        line = -115
        odds = [-115, 105]
        category = "us"
        npt.assert_almost_equal(fair_odds(line, odds, category), -110)

        line = 258
        odds = [258, -122, 258]
        npt.assert_almost_equal(fair_odds(line, odds), 297)

        line = -100
        odds = [-100, -120]
        npt.assert_almost_equal(fair_odds(line, odds), 109)


if __name__ == "__main__":
    unittest.main()
