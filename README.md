[![PyPI version fury.io](https://badge.fury.io/py/pybettor.svg)](https://pypi.python.org/pypi/pybettor/) [![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://www.tidyverse.org/lifecycle/#experimental) [![Twitter
Follow](https://img.shields.io/twitter/follow/theFirmAISports?style=social)](https://twitter.com/theFirmAISports)


## Tools for Sports Betting

This package contains tools and functions to help sports bettors make more money\!

## Installation

You can install pybettor from [PyPi](https://pypi.org/project/pybettor/) with:

``` python
pip install "pybettor"
```

## Running Tests
```python
pip install pytest
pytest
```

## Running Linting
```python
pip install flake8
flake8 . --count --max-complexity=15 --max-line-length=128 --statistics
```

## Examples

#### Implied Probability

Implied probabilities, or break-even win percentage, can easily be found with this function. Here is an example with given odds of -300 (US Odds), 2.5 (Decimal Odds), 4.9 (Decimal Odds), 7/1 (Fractional Odds).

``` python
implied_prob(-300, category="us")
```

    [0.75]

``` python
implied_prob(2.5, category="dec")
```

    [0.4]

```python
implied_prob(7/1, category="frac")
```

    [0.125]

#### Odds from Probabilities

Let’s say you believe a bet has a 75% chance to cover, what would the price be? Using the implied odds function can give you the price based on your probability.

``` python
implied_odds(0.75, category="us")
```

    [-300]

``` python
implied_odds(0.75, category="dec")
```

    [1.33]

``` python
implied_odds(0.75, category="frac")
```

    ['1/3']

``` python
implied_odds(0.75, category="all")
```

        American  Decimal Fraction  Implied Probability
    0    -300.0     1.33   33/100                 0.75

#### Converting Odds

Let’s say you want to convert the American Odds you see on the screen (-175) to another type.

``` python
convert_odds(-175)
```

       American  Decimal Fraction  Implied Probability
    0      -175     1.57      4/7             0.636364

## Special Thanks

  - To the entire [A.I. Sports](https://aisportsfirm.com/home/our-team/) team\!