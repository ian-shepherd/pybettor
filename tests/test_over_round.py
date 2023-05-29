import unittest
import numpy.testing as npt
from pybettor.over_round import over_round


class TestOverRound(unittest.TestCase):
    def test_over_round(self):
        lines = [1.3, 1.9]
        category = "dec"
        npt.assert_almost_equal(over_round(lines, category), 0.29554655)

        lines = [-110, -110]
        category = "us"
        npt.assert_almost_equal(over_round(lines, category), 0.04761904)


if __name__ == "__main__":
    unittest.main()
