import unittest
import numpy.testing as npt
from pybettor.edge_calc import edge_calc


class TestEdgeCalc(unittest.TestCase):
    def test_edge_calc(self):
        win_prob = 0.75
        odds = -175
        npt.assert_almost_equal(edge_calc(win_prob, odds), 0.1136364)

        win_prob = 0.75
        odds = 1.2855
        npt.assert_almost_equal(edge_calc(win_prob, odds, category="dec"), -0.02790743)

        win_prob = 0.75
        odds = 3 / 7
        npt.assert_almost_equal(edge_calc(win_prob, odds, category="frac"), 0.05)


if __name__ == "__main__":
    unittest.main()
