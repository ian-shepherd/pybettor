import unittest
import numpy.testing as npt
from pybettor.convert_odds import convert_odds


class TestConvertOdds(unittest.TestCase):
    def test_convert_us_odds(self):
        odds = [-115, -105, 120]
        expected_result = [1.87, 1.95, 2.2]
        result = convert_odds(odds, "us", "dec")
        npt.assert_almost_equal(result, expected_result, 2)

    def test_convert_us_to_frac(self):
        odds = [-115, -105, 120]
        expected_result = ["20/23", "20/21", "6/5"]
        result = convert_odds(odds, "us", "frac")
        npt.assert_array_equal(result, expected_result)

    def test_convert_dec_odds(self):
        odds = [1.87, 3.5, 1.33, 1.67]
        expected_result = [-115, 250, -303, -149]
        result = convert_odds(odds, "dec", "us")
        npt.assert_almost_equal(result, expected_result)

    def test_convert_dec_to_frac(self):
        odds = [1.87, 3.5, 1.33, 1.67]
        expected_result = ["87/100", "5/2", "33/100", "67/100"]
        result = convert_odds(odds, "dec", "frac")
        npt.assert_array_equal(result, expected_result)

    def test_convert_frac_odds(self):
        odds = [20 / 23, 5 / 2, 1 / 3, 67 / 100]
        expected_result = [-115, 250, -300, -149]
        result = convert_odds(odds, "frac", "us")
        npt.assert_almost_equal(result, expected_result, 0)

    def test_convert_frac_to_dec(self):
        odds = [20 / 23, 5 / 2, 1 / 3, 3 / 5]
        expected_result = [1.87, 3.5, 1.33, 1.6]
        result = convert_odds(odds, "frac", "dec")
        npt.assert_almost_equal(result, expected_result, 2)

    def test_convert_us_to_all(self):
        odds = [-115, -105, 120]

        expected = {
            "American": [-115, -105, 120],
            "Decimal": [1.87, 1.95, 2.2],
            "Fraction": ["20/23", "20/21", "6/5"],
            "Implied Probability": [0.53, 0.51, 0.45],
        }

        result = convert_odds(odds, cat_in="us", cat_out="all")

        npt.assert_array_equal(result["American"], expected["American"])
        npt.assert_almost_equal(result["Decimal"], expected["Decimal"], 2)
        npt.assert_array_equal(result["Fraction"], expected["Fraction"])
        npt.assert_almost_equal(
            result["Implied Probability"], expected["Implied Probability"], 2
        )

    def test_convert_frac_to_all(self):
        odds = [3 / 4, 4 / 5, 5 / 6]

        expected = {
            "American": [-133, -125, -120],
            "Decimal": [1.75, 1.8, 1.83],
            "Fraction": ["3/4", "4/5", "5/6"],
            "Implied Probability": [0.571, 0.556, 0.545],
        }

        result = convert_odds(odds, cat_in="frac", cat_out="all")

        npt.assert_array_equal(result["American"], expected["American"])
        npt.assert_almost_equal(result["Decimal"], expected["Decimal"], 2)
        npt.assert_array_equal(result["Fraction"], expected["Fraction"])
        npt.assert_almost_equal(
            result["Implied Probability"], expected["Implied Probability"], 2
        )

    def test_convert_dec_to_all(self):
        odds = [2.5, 1.75, 1.91]

        expected = {
            "American": [150, -133, -110],
            "Decimal": [2.5, 1.75, 1.91],
            "Fraction": ["3/2", "3/4", "91/100"],
            "Implied Probability": [0.4, 0.571, 0.523],
        }

        result = convert_odds(odds, cat_in="dec", cat_out="all")

        npt.assert_array_equal(result["American"], expected["American"])
        npt.assert_almost_equal(result["Decimal"], expected["Decimal"], 2)
        npt.assert_array_equal(result["Fraction"], expected["Fraction"])
        npt.assert_almost_equal(
            result["Implied Probability"], expected["Implied Probability"], 2
        )

    def test_convert_prob_to_all(self):
        odds = [0.7, 0.5, 0.3]

        expected = {
            "American": [-233, 100, 233],
            "Decimal": [1.43, 2.0, 3.33],
            "Fraction": ["3/7", "1/1", "7/3"],
            "Implied Probability": [0.7, 0.5, 0.3],
        }

        result = convert_odds(odds, cat_in="prob", cat_out="all")

        npt.assert_array_equal(result["American"], expected["American"])
        npt.assert_almost_equal(result["Decimal"], expected["Decimal"], 2)
        npt.assert_array_equal(result["Fraction"], expected["Fraction"])
        npt.assert_almost_equal(
            result["Implied Probability"], expected["Implied Probability"], 2
        )


if __name__ == "__main__":
    unittest.main()
