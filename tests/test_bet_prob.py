import unittest
import numpy.testing as npt
from pybettor.bet_prob import bet_prob


class TestBetProb(unittest.TestCase):
    def test_nfl_win_bet_prob(self):
        pred_spread = -9
        spread = -3.5
        sport = "NFL"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("win_prob"), 0.65425188
        )

    def test_nfl_lose_bet_prob(self):
        pred_spread = -9
        spread = -3.5
        sport = "NFL"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("lose_prob"), 0.34574811
        )

    def test_nfl_push_bet_prob(self):
        pred_spread = -9
        spread = -3.5
        sport = "NFL"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("push_prob"), 0.0
        )

    def test_ncaaf_win_bet_prob(self):
        pred_spread = 21
        spread = 10.5
        sport = "NCAAF"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("win_prob"), 0.25583164
        )

    def test_ncaaf_lose_bet_prob(self):
        pred_spread = 21
        spread = 10.5
        sport = "NCAAF"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("lose_prob"), 0.74416835
        )

    def test_ncaaf_push_bet_prob(self):
        pred_spread = 21
        spread = 10.5
        sport = "NCAAF"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("push_prob"), 0.0
        )

    def test_nba_bet_win_prob(self):
        pred_spread = -7
        spread = -3
        sport = "NBA"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("win_prob"), 0.61472925
        )

    def test_nba_bet_lose_prob(self):
        pred_spread = -7
        spread = -3
        sport = "NBA"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("lose_prob"), 0.35383023
        )

    def test_nba_bet_push_prob(self):
        pred_spread = -7
        spread = -3
        sport = "NBA"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("push_prob"), 0.03144051
        )

    def test_ncaab_win_bet_prob(self):
        pred_spread = -3
        spread = 5
        sport = "NCAAB"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("win_prob"), 0.77337264
        )

    def test_ncaab_lose_bet_prob(self):
        pred_spread = -3
        spread = 5
        sport = "NCAAB"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("lose_prob"), 0.19766254
        )

    def test_ncaab_push_bet_prob(self):
        pred_spread = -3
        spread = 5
        sport = "NCAAB"
        npt.assert_almost_equal(
            bet_prob(pred_spread, spread, sport).get("push_prob"), 0.02896480
        )


if __name__ == "__main__":
    unittest.main()
