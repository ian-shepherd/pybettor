import numpy as np
import numpy.testing as npt
from pybettor import convert_odds

odds = [-115, 2.5, 1/3, 0.6]
cat_in = 'us'
cat_out = 'all'

expected_results = {
    'American': [-115, 145, -300, -167],
    'Decimal': [1.87, 3.5, 1.33, 1.67],
    'Fraction': ['20/23', '5/2', '1/3', '3/5'],
    'Implied Probability': [0.535, 0.286, 0.75, 0.625]
}


def test_convert_odds():
    result = convert_odds(odds, cat_in, cat_out)
    for key, expected in expected_results.items():
        npt.assert_almost_equal(result[key], expected)


test_convert_odds()
