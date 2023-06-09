import unittest
import numpy.testing as npt
from pybettor.hfa_calc import hfa_calc


class TestHfaCalc(unittest.TestCase):
    def test_hfa_calc(self):
        win_p_neutral = 0.142
        win_p_leag_hm = 0.61
        npt.assert_almost_equal(hfa_calc(win_p_neutral, win_p_leag_hm), 0.2056309)

        win_p_neutral = 0.5
        win_p_leag_hm = 0.6

        npt.assert_almost_equal(hfa_calc(win_p_neutral, win_p_leag_hm), 0.5999999)


if __name__ == "__main__":
    unittest.main()
