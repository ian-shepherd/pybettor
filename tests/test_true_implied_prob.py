import unittest
import numpy.testing as npt
from pybettor.true_implied_prob import true_implied_prob


class TestTrueImpliedProb(unittest.TestCase):
    def test_true_implied_prob(self):
        line = -110
        odds = [-110, -110]
        category = "us"
        probs = true_implied_prob(line, odds, category)
        npt.assert_almost_equal(probs.get("true_prob"), 0.5)
        npt.assert_almost_equal(probs.get("imp_prob"), 0.52380952)


if __name__ == "__main__":
    unittest.main()
