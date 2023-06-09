import unittest
import numpy.testing as npt
from pybettor.clv_calc import clv_calc


class TestClvCalc(unittest.TestCase):
    def test_clv_calc(self):
        bet_odds = -110
        close_odds = -230
        npt.assert_almost_equal(clv_calc(bet_odds, close_odds), 0.3305785)

        bet_odds = 1.75
        close_odds = 1.5
        npt.assert_almost_equal(
            clv_calc(bet_odds, close_odds, category="dec"), 0.1666666
        )

        bet_odds = 5 / 2
        close_odds = 2
        npt.assert_almost_equal(
            clv_calc(bet_odds, close_odds, category="frac"), 0.1666666
        )


if __name__ == "__main__":
    unittest.main()
