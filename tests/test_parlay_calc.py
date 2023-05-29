import unittest
import numpy.testing as npt
from pybettor.parlay_calc import parlay_calc


class TestParlayCalc(unittest.TestCase):
    def test_parlay_calc(self):
        risk = 75
        odds = [-110, -110, -110]
        category = "us"
        npt.assert_almost_equal(parlay_calc(risk, odds, category), 446.85)


if __name__ == "__main__":
    unittest.main()
