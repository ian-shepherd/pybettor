import numpy.testing as npt

from pybettor.convert_odds import convert_odds

# Generate test cases
odds = [-115, 2.5, 1/3, 0.6]
cat_in = 'us'
cat_out = 'all'

# Define expected results
expected_results = {
    'us': [-115, 145, -300, -167],
    'dec': [1.87, 3.5, 1.33, 1.67],
    'frac': ['20/23', '5/2', '1/3', '3/5'],
    'prob': [0.535, 0.286, 0.75, 0.625]
}

# Test convert_odds function


def test_convert_odds():
    converted_odds = convert_odds(odds, cat_in, cat_out)
    for key, expected in expected_results.items():
        npt.assert_almost_equal(converted_odds[key], expected)


# Run the tests
test_convert_odds()
