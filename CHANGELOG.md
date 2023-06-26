# Change Log

### 1.1.3 2023-06-09 Added new functionality to implied_odds() and implied_prob()
* added functionality to pass various methods to account for margin of bookmaker

### 1.1.2 2023-06-07 Added expected value function
* added expected_value_calc() calculates the expected value of given odds based on implied probability

### 1.1.1 2023-05-29 Added unit tests and fixed bugs
* Added unit tests for all functions
* Reduced complexity of convert_odds()


### 1.1.0 2023-05-24 Added new functions and updated documentation and output of functions
* Functions added
    * bet_prob() calculates probability of bet
    * break_even() calculates win rate needed to break even
    * fair_odds() calculates fair odds of bet

* Functions changed
    * bet_calc() added type castings to ensure correct output and changed output from list to float
    * convert_odds() added type casting and changed output from float or dataframe to list or dictionary
    * implied_odds() added type casting and changed output from list or dataframe to list or dictionary
    * implied_prob() added type casting
    * kelly_bet() added type casting and changed output from list to int
    * kelly() added type casting and changed output from list to int
    * over_round() added type casting and correct documentation for return type
    * parlay_calc() added type casting
    * true_implied_prob() added type casting and changed output from dataframe to dictionary
    * true_probability() added type casting


### 1.0.0 2022-06-12 Added new functions
Functions added
* bet_calc() calculated bet payout
* kelly_bet() calculates dollar amount to bet via Kelly Criterion
* kelly() calculates % of bankroll to bet via Kelly Criterion
* over_round() calculates over round of bet
* parlay_calc() calculates payout of parlay bets
* true_implied_prob() calculates true implied probability
* true_probability() calculates true probability


### 0.0.1 2020-07-20 Initial release
Functions added
* convert_odds() converts odds to different types
* implied odds() calculates the fair odds from probability
* implied prob() calculates the implied probability from odds