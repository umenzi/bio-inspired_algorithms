import numpy as np


def levy_flight(beta: float, size: int):
    """
    Generate a step length from a Levy distribution.

    :param beta: the beta parameter of the Levy distribution
    :param size: the number of samples to generate
    :return: the step lengths
    """

    # Draw samples from a uniform distribution
    u = np.random.uniform(0.01, 1, size=size)

    # Calculate the corresponding step lengths
    steps = u ** (-1 / beta)

    # Make sure the steps are between -2 and 2 (obstacle radius)
    steps = np.clip(steps, -2, 2)

    return steps
