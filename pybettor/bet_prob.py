import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np


def bet_prob(
    pred_spread: float, spread: float, sport: str = "NBA", plot=False
) -> dict or tuple:
    """
    Calculates the probability of winning, losing, and pushing a bet based on the predicted spread and actual spread. 
    The function also plots the normal distribution curve and the area under the curve for the left and right sides of the spread if plot=True.
    Standard deviations are as follows:
        NBA: 12
        NCAAB: 10
        NFL: 13.86
        NCAAF: 16
    Standard deviations are based on the following references:
        Stern, Hal. "The Probability of Winning a Football Game as a function of the Pointspread."
          The American Statistician 45, no. 3 (1991): 179-83. Accessed July 18, 2020. doi:10.2307/2684286. 
          {https://statistics.stanford.edu/sites/g/files/sbiybj6031/f/COV%20NSF%2059.pdf}

        Stern, Hal. "On the Probability of Winning a Football Game." 
        The American Statistician 45, no. 3 (1991): 179-83. Accessed July 18, 2020. doi:10.2307/2684286. 
        {https://www-jstor-org.turing.library.northwestern.edu/stable/2684286}

        Winston, Wayne L. "From Point Ratings to Probabilities." 
        In Mathletics: How Gamblers, Managers, and Sports Enthusiasts Use Mathematics in Baseball, Basketball, and Football, 290-97. 
        PRINCETON; OXFORD: Princeton University Press, 2009. Accessed July 18, 2020. doi:10.2307/j.ctt7sj9q.48.

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
    assert sport in [
        "NBA",
        "NCAAB",
        "NFL",
        "NCAAF",
    ], "sport must be either: ('NBA', 'NCAAB', 'NFL', 'NCAAF')"

    if sport == "NBA":
        sd = 12
    elif sport == "NCAAB":
        sd = 10
    elif sport == "NFL":
        sd = 13.86
    elif sport == "NCAAF":
        sd = 16

    if spread % 1 == 0:
        win_prob = 1 - stats.norm.cdf(pred_spread + 0.5, loc=spread, scale=sd)
        lose_prob = stats.norm.cdf(pred_spread - 0.5, loc=spread, scale=sd)
        push_prob = 1 - win_prob - lose_prob
    else:
        win_prob = 1 - stats.norm.cdf(pred_spread, loc=spread, scale=sd)
        lose_prob = stats.norm.cdf(pred_spread, loc=spread, scale=sd)
        push_prob = 0

    mydict = {
        "win_prob": win_prob,
        "lose_prob": lose_prob,
        "push_prob": push_prob,
    }

    if plot:

        # Create the figure and axes
        fig, ax = plt.subplots()

        # Generate x values
        x = np.linspace(pred_spread - (sd * 3), pred_spread + (sd * 3), 501)

        # Plot the normal distribution curve
        ax.plot(
            x,
            stats.norm.pdf(x, loc=pred_spread, scale=sd),
            "b-",
            label="Normal Distribution",
        )

        # Plot the area under the curve for the left side
        x_left = np.linspace(pred_spread - (sd * 3), spread, 501)
        ax.fill_between(
            x_left,
            stats.norm.pdf(x_left, loc=pred_spread, scale=sd),
            color="limegreen",
            alpha=0.75,
        )

        # Plot the area under the curve for the right side
        x_right = np.linspace(spread, pred_spread + (sd * 3), 501)
        ax.fill_between(
            x_right,
            stats.norm.pdf(x_right, loc=pred_spread, scale=sd),
            color="salmon",
            alpha=0.75,
        )

        # Plot the vertical lines
        ax.axvline(spread, color="black", linestyle="--", label="Spread")
        ax.axvline(pred_spread, color="black",
                   linestyle="--", label="Prediction")

        # Add the annotation
        annotation_text = f"Point Edge: {spread - pred_spread}\nWin Probability: {round(win_prob * 100,2)}%\nLose Probability: {round(lose_prob * 100,2)}%\nPush Probability: {round(push_prob * 100,2)}%"
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

        # Set the axis labels and title
        ax.set_xlabel("Final Margin")
        ax.set_ylabel("")
        ax.set_title(f"Predicted Line: {pred_spread} - Actual Line: {spread}")

        # Set the y-axis limits and remove y-axis ticks
        ax.set_ylim(0, None)
        ax.yaxis.set_ticks([])

        # Set the plot background to white
        ax.set_facecolor("white")

        return mydict, fig

    else:
        return mydict
