import unittest
import numpy.testing as npt
from pybettor.hold_calc import hold_calc


class TestHoldCalc(unittest.TestCase):
    def test_hold_calc(self):
        odds = [-110, -110]
        npt.assert_almost_equal(hold_calc(odds), 0.0454545)

        odds = [-125, -125]
        npt.assert_almost_equal(hold_calc(odds), 0.1)

        odds = [285, -122, 258]
        npt.assert_almost_equal(hold_calc(odds), 0.08140533)

        odds = [1.75, 1.75]
        npt.assert_almost_equal(hold_calc(odds, category="dec"), 0.125)


if __name__ == "__main__":
    unittest.main()
