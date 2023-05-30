import unittest
import numpy.testing as npt
from pybettor.true_probability import true_probability


class TestTrueProbability(unittest.TestCase):
    def test_true_probability(self):
        line = -110
        odds = [-110, -110]
        category = "us"
        npt.assert_almost_equal(true_probability(line, odds, category), 0.5)


if __name__ == "__main__":
    unittest.main()
