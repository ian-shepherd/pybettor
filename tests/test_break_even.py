import unittest
import numpy.testing as npt
from pybettor.break_even import break_even


class TestBreakEven(unittest.TestCase):
    def test_break_even(self):
        risk = 110
        rtrn = 210
        legs = 1
        npt.assert_almost_equal(break_even(risk, rtrn, legs), 0.52380952)

        risk = 50
        rtrn = 750
        legs = 4
        npt.assert_almost_equal(break_even(risk, rtrn, legs), 0.50813274)


if __name__ == "__main__":
    unittest.main()
