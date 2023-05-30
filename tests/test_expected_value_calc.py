from numpy.testing import assert_almost_equal, assert_raises

from pybettor.expected_value_calc import expected_value_calc


def test_expected_value_calc_valid_us_category():
    implied_probability = 0.6
    odds = 200
    expected_result = 80.0
    result = expected_value_calc(implied_probability, odds)
    assert_almost_equal(result, expected_result)


def test_expected_value_calc_valid_dec_category():
    implied_probability = 0.4
    odds = 1.5
    expected_result = -40.0
    result = expected_value_calc(implied_probability, odds, category="dec")
    assert_almost_equal(result, expected_result)


def test_expected_value_calc_valid_frac_category():
    implied_probability = 0.75
    odds = 3/2
    expected_result = 87.5
    result = expected_value_calc(implied_probability, odds, category="frac")
    assert_almost_equal(result, expected_result)


def test_expected_value_calc_invalid_implied_probability_below_zero():
    implied_probability = -0.1
    odds = 2.0
    with assert_raises(AssertionError):
        expected_value_calc(implied_probability, odds)


def test_expected_value_calc_invalid_implied_probability_above_one():
    implied_probability = 1.2
    odds = 3.0
    with assert_raises(AssertionError):
        expected_value_calc(implied_probability, odds)


def test_expected_value_calc_invalid_category():
    implied_probability = 0.5
    odds = 2.5
    invalid_category = "invalid"
    with assert_raises(AssertionError):
        expected_value_calc(implied_probability, odds,
                            category=invalid_category)


def test_expected_value_calc_negative_odds():
    implied_probability = 0.8
    odds = -150
    expected_result = 33.336
    result = expected_value_calc(implied_probability, odds)
    assert_almost_equal(result, expected_result)


def test_expected_value_calc_negative_odds_positive_result():
    implied_probability = 0.3
    odds = -250
    expected_result = -58.0
    result = expected_value_calc(implied_probability, odds)
    assert_almost_equal(result, expected_result)
