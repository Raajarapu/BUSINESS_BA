import numpy as np


def monte_carlo(series, simulations=1000):
    """
    Monte Carlo simulation for risk analysis
    """
    series = series.dropna()

    if series.empty:
        return []

    mean = series.mean()
    std = series.std()

    if std == 0:
        return [mean] * simulations

    simulations_result = np.random.normal(mean, std, simulations)
    return simulations_result.tolist()
