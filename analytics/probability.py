import numpy as np

def monte_carlo(data, simulations=1000):
    mean = data.mean()
    std = data.std()
    return np.random.normal(mean, std, simulations).tolist()
