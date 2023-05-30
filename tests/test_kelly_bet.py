import unittest
import numpy.testing as npt
from pybettor.kelly_bet import kelly_bet


class TestKellyBet(unittest.TestCase):
    def test_kelly_bet(self):
        unit_size = 100
        win_prob = 0.43
        odds = 2.6
        category = "dec"
        kelly_factor = 1.5
        npt.assert_almost_equal(
            kelly_bet(unit_size, win_prob, odds, category, kelly_factor), 492
        )

        unit_size = 50
        win_prob = 0.53
        odds = -105
        category = "us"
        kelly_factor = 2
        npt.assert_almost_equal(
            kelly_bet(unit_size, win_prob, odds, category, kelly_factor), 91
        )


if __name__ == "__main__":
    unittest.main()
