import numpy as np


def hfa_calc(win_p_neutral: int or float, win_p_leag_hm: int or float) -> float:
    """Calculate Home Field Advantage
    This function calculates the home field advantage (HFA) for a given bet.

    Args:
        win_p_neutral (int, float): Win Probability Neutral Site
        win_p_leag_hm (int, float): Win Probability League Home

    Returns:
        float: Home Field Advantage (HFA) of a bet
    """

    assert isinstance(win_p_neutral, (int, float)), "win_p_neutral must be numeric"
    assert (
        0 <= win_p_neutral <= 1
    ), "win_p_neutral must be in the range of 0 to 1 inclusive"
    assert isinstance(win_p_leag_hm, (int, float)), "win_p_leag_hm must be numeric"
    assert (
        0 <= win_p_leag_hm <= 1
    ), "win_p_leag_hm must be in the range of 0 to 1 inclusive"

    log_odds_tm = np.log(win_p_neutral) - np.log(1 - win_p_neutral)
    log_odds_lg = np.log(win_p_leag_hm) - np.log(1 - win_p_leag_hm)

    hfa = np.exp(log_odds_tm + log_odds_lg) / (1 + np.exp(log_odds_tm + log_odds_lg))

    return hfa
