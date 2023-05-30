import unittest
import numpy.testing as npt
from pybettor.kelly import kelly


class TestKelly(unittest.TestCase):
    def test_kelly(self):
        win_prob = 0.6
        odds = 100
        npt.assert_almost_equal(kelly(win_prob, odds), 20)

        win_prob = 0.6
        odds = 2.0
        category = "dec"
        npt.assert_almost_equal(kelly(win_prob, odds, category), 20)


if __name__ == "__main__":
    unittest.main()
