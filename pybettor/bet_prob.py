import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np


def _plot_results(probabilities, pred_spread, spread, sd):
    win_prob = probabilities['win_prob']
    push_prob = probabilities['push_prob']
    lose_prob = probabilities['lose_prob']

    fig, ax = plt.subplots()

    x = np.linspace(pred_spread - (sd * 3), pred_spread + (sd * 3), 501)
    ax.plot(x, stats.norm.pdf(x, loc=pred_spread, scale=sd),
            "b-", label="Normal Distribution")

    x_left = np.linspace(pred_spread - (sd * 3), spread, 501)
    ax.fill_between(x_left, stats.norm.pdf(
        x_left, loc=pred_spread, scale=sd), color="limegreen", alpha=0.75)

    x_right = np.linspace(spread, pred_spread + (sd * 3), 501)
    ax.fill_between(x_right, stats.norm.pdf(
        x_right, loc=pred_spread, scale=sd), color="salmon", alpha=0.75)

    ax.axvline(spread, color="black", linestyle="--", label="Spread")
    ax.axvline(pred_spread, color="black", linestyle="--", label="Prediction")

    annotation_text = (
        f"Point Edge: {spread - pred_spread}\n"
        f"Win Probability: {round(win_prob * 100, 2)}%\n"
        f"Lose Probability: {round(lose_prob * 100, 2)}%\n"
        f"Push Probability: {round(push_prob * 100, 2)}%"
    )
    ax.annotate(
        annotation_text,
        xy=(pred_spread - (sd * 3), ax.get_ylim()[1]),
        xytext=(-15, -2),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=10,
        fontweight="bold",
    )

    ax.set_xlabel("Final Margin")
    ax.set_ylabel("")
    ax.set_title(f"Predicted Line: {pred_spread} - Actual Line: {spread}")

    ax.set_ylim(0, None)
    ax.yaxis.set_ticks([])
    ax.set_facecolor("white")

    return fig


def bet_prob(pred_spread: float, spread: float, sport: str = "NBA", plot=False) -> dict or tuple:
    """
    Calculates the probability of winning, losing, and pushing a bet based on the predicted spread and actual spread.
    Plotting normal distribution curve and area under curve for spread sides if plot=True

    Args:
        pred_spread (float): predicted spread for the team you want to bet on
        spread (float): actual spread for the team you want to bet on
        sport (str, optional): sport. Defaults to "NBA". Possible values are: "NBA", "NCAAB", "NFL", "NCAAF"

    Returns:
        dict: dictionary of probabilities
        fig: matplotlib figure if plot=True
    """

    assert isinstance(pred_spread, (int, float)), "pred_spread must be numeric"
    assert isinstance(spread, (int, float)), "spread must be numeric"
    assert sport in ["NBA", "NCAAB", "NFL",
                     "NCAAF"], "sport must be either: ('NBA', 'NCAAB', 'NFL', 'NCAAF')"

    sd = {"NBA": 12, "NCAAB": 10, "NFL": 13.86, "NCAAF": 16}[sport]

    win_prob = 1 - stats.norm.cdf(pred_spread + 0.5, loc=spread, scale=sd)
    lose_prob = stats.norm.cdf(pred_spread - 0.5, loc=spread, scale=sd)
    push_prob = 1 - win_prob - lose_prob if spread % 1 == 0 else 0

    probabilities = {
        "win_prob": win_prob,
        "lose_prob": lose_prob,
        "push_prob": push_prob,
    }

    if plot:
        fig = _plot_results(probabilities, pred_spread, spread, sd)
        return probabilities, fig

    return probabilities
