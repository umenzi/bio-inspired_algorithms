import random

import numpy as np


class Firefly:
    """
    Firefly is a class that represents a firefly in the Firefly Algorithm.
    """
    def __init__(self, alpha_init, alpha_end, beta, gamma_init, gamma_end, upper_boundary, lower_boundary, function_dimension):
        self.alpha_init = alpha_init
        self.alpha_end = alpha_end
        self.beta = beta
        self.gamma_init = gamma_init
        self.gamma_end = gamma_end
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

    def move_towards(self, better_position, adaptive):
        # TODO: Currently meant for 1D, needs to be updated for 2D
        # Adaptive parameters
        alpha = self.alpha_init + adaptive * (self.alpha_end - self.alpha_init)
        gamma = self.gamma_init + adaptive * (self.gamma_end - self.gamma_init)

        # We compute the Euclidean distance between the particles
        distance = np.linalg.norm(self.__position - better_position)
        attractiveness = self.beta * np.exp(-gamma * (distance ** 2))
        random_number = random.uniform(0, 1) - 0.5

        self.__position += (attractiveness * (better_position - self.__position) +
                            alpha * random_number)
        # Try also (from http://dx.doi.org/10.1155/2015/561394):
        # self.__position += (attractiveness * (better_position - self.__position) +
        #                     alpha * distance * random_number)
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