import unittest
import numpy.testing as npt
from pybettor.expected_value_calc import expected_value_calc


class TestBetCalc(unittest.TestCase):
    def test_expected_value_calc_valid_us_category(self):
        prob = 0.6
        odds = 200
        expected_result = 80.0
        result = expected_value_calc(prob, odds)
        npt.assert_almost_equal(result, expected_result)

    def test_expected_value_calc_valid_dec_category(self):
        prob = 0.4
        odds = 1.5
        expected_result = -40.0
        result = expected_value_calc(prob, odds, category="dec")
        npt.assert_almost_equal(result, expected_result)

    def test_expected_value_calc_valid_frac_category(self):
        prob = 0.75
        odds = 3 / 2
        expected_result = 87.5
        result = expected_value_calc(prob, odds, category="frac")
        npt.assert_almost_equal(result, expected_result)

    def test_expected_value_calc_invalid_implied_probability_below_zero(self):
        prob = -0.1
        odds = 2.0
        with npt.assert_raises(AssertionError):
            expected_value_calc(prob, odds)

    def test_expected_value_calc_invalid_implied_probability_above_one(self):
        prob = 1.2
        odds = 3.0
        with npt.assert_raises(AssertionError):
            expected_value_calc(prob, odds)

    def test_expected_value_calc_invalid_category(self):
        prob = 0.5
        odds = 2.5
        invalid_category = "invalid"
        with npt.assert_raises(AssertionError):
            expected_value_calc(prob, odds, category=invalid_category)

    def test_expected_value_calc_negative_odds(self):
        prob = 0.8
        odds = -150
        expected_result = 33.336
        result = expected_value_calc(prob, odds)
        npt.assert_almost_equal(result, expected_result)

    def test_expected_value_calc_negative_odds_positive_result(self):
        prob = 0.3
        odds = -250
        expected_result = -58.0
        result = expected_value_calc(prob, odds)
        npt.assert_almost_equal(result, expected_result)


if __name__ == "__main__":
    unittest.main()
