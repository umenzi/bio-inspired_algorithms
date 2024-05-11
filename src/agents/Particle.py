import math
import random

import numpy as np

from agents.Agent import Agent
from environments.Environment import Environment
from helpers.Coordinate import Coordinate
from helpers.PathSpecification import PathSpecification


class Particle(Agent):
    """
    An agent representing the particle functionality
    """

    def __init__(self, environment: Environment, path_specification: PathSpecification,
                 convergence_iter: int, trail: float, velocity_x: float, velocity_y: float, step_size: int = 1,
                 inertia_weight: float = 1.0):
        super().__init__(environment, path_specification, step_size)

        self.personal_best_pos = self.current_position  # Initially personal best is start
        self.current_position = self.current_position  # Get rid of warnings
        self.rand = random
        self.convergence_iter = convergence_iter
        self.trail = trail
        # A particle is defined by its position and velocity,
        # The current position is already inherent of the Agent class, so we add a velocity
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.w = inertia_weight

    def update_particle(self, global_best_pos: Coordinate, personal_best_pos: Coordinate, c1: float, c2: float,
                        curr_iter: int, iter_max: int):
        # Random coefficients r1, r2
        r1: float = self.rand.uniform(0, 1)
        r2: float = self.rand.uniform(0, 1)
        # Evaluate the inertia weight
        if c1 >= c2:
            self.w = math.exp(((c1 - c2) / (c1 + c2)) * (curr_iter / iter_max)) - 0.2
        else:
            self.w = (1 / 3) * (c1 / c2) * (iter_max / curr_iter)
        # Update the velocities according to pso strategy(c1-c2)/(c1+c2)
        new_vel_x: float = (self.w * self.velocity_x + c1 * r1 * (personal_best_pos.x - self.current_position.x)
                            + c2 * r2 * (global_best_pos.x - self.current_position.x))
        new_vel_y: float = (self.w * self.velocity_y + c1 * r1 * (personal_best_pos.y - self.current_position.y)
                            + c2 * r2 * (global_best_pos.y - self.current_position.y))
        # Clamp new velocity to [-2, 2]
        new_vel_x = np.clip(new_vel_x, -2, 2)
        new_vel_y = np.clip(new_vel_y, -2, 2)
        # Record the new position
        new_pos: Coordinate = Coordinate(self.current_position.x + new_vel_x, self.current_position.y + new_vel_y)
        # Update the velocities and current position if it is not out of bounds,
        # meaning if not obstacle or out of search space
        if not self.position_out_of_bounds(new_pos):
            self.velocity_x = new_vel_x
            self.velocity_y = new_vel_y
            self.current_position = new_pos

        return self.current_position  # Return the current position
