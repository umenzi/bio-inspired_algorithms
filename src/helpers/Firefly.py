import random

import numpy as np


class Firefly:
    """
    Firefly is a class that represents a firefly in the Firefly Algorithm.
    """
    def __init__(self, alpha, beta, gamma, upper_boundary, lower_boundary, function_dimension):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.__intensity = None
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary
        self.__position = np.array(
            [random.uniform(self.lower_boundary, self.upper_boundary) for _ in range(function_dimension)])

    @property
    def intensity(self):
        return self.__intensity

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    def move_towards(self, better_position):
        # We compute the Euclidean distance between the particles
        distance = np.linalg.norm(self.__position - better_position)
        attractiveness = self.beta * np.exp(-self.gamma * (distance ** 2))
        random_number = random.uniform(0, 1)

        self.__position += (attractiveness * (better_position - self.__position) +
                            self.alpha * (random_number - 0.5))
        self.check_boundaries()

    def random_walk(self, area):
        self.__position = np.array(
            [random.uniform(cord - area, cord + area) for x, cord in np.ndenumerate(self.__position)])

    def update_intensity(self, func):
        self.__intensity = -1 * func(self.__position)

    def check_boundaries(self):
        for i, cord in np.ndenumerate(self.__position):
            if cord < self.lower_boundary:
                self.__position[i] = self.lower_boundary
            elif cord > self.upper_boundary:
                self.__position[i] = self.upper_boundary
            else:
                self.__position[i] = cord
