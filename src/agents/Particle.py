import math
import random

from agents.Agent import Agent
from environments.Environment import Environment
from helpers.Direction import Direction
from helpers.Coordinate import Coordinate
from helpers.PathSpecification import PathSpecification
from helpers.Route import Route
import numpy as np


class Particle(Agent):
    """
    agents representing the particle functionality
    """

    def __init__(self, environment: Environment, path_specification: PathSpecification,
                 convergence_iter: int, trail: float, velocity_x: float, velocity_y: float, step_size: int = 1,
                 inertia_weight: float = 1.0):
        super().__init__(environment, path_specification, step_size)

        self.personal_best_pos = self.current_position  # initially personal best is start
        self.current_position = self.current_position  # get rid of stupid warnings
        self.rand = random
        self.convergence_iter = convergence_iter
        self.trail = trail
        # a particle is defined by its position and velocity
        # the current position is already inherent of the Agent class, so we add a velocity
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.w = inertia_weight

    def update_particle(self, global_best_pos: Coordinate, personal_best_pos: Coordinate, c1: float, c2: float,
                        curr_iter: int, iter_max: int):
        # random coefficients r1, r2
        r1: float = self.rand.uniform(0, 1)
        r2: float = self.rand.uniform(0, 1)
        # evaluate the inertia weight
        if c1 >= c2:
            self.w = math.exp(((c1 - c2) / (c1 + c2)) * (curr_iter / iter_max)) - 0.2
        else:
            self.w = (1 / 3) * (c1 / c2) * (iter_max / curr_iter)
        # update the velocities according to pso strategy(c1-c2)/(c1+c2)
        new_vel_x: float = (self.w * self.velocity_x + c1 * r1 * (personal_best_pos.x - self.current_position.x)
                            + c2 * r2 * (global_best_pos.x - self.current_position.x))
        new_vel_y: float = (self.w * self.velocity_y + c1 * r1 * (personal_best_pos.y - self.current_position.y)
                            + c2 * r2 * (global_best_pos.y - self.current_position.y))
        # clamp new velocity to [-2, 2]
        new_vel_x = np.clip(new_vel_x, -2, 2)
        new_vel_y = np.clip(new_vel_y, -2, 2)
        # record the new position
        new_pos: Coordinate = Coordinate(self.current_position.x + new_vel_x, self.current_position.y + new_vel_y)
        # update the velocities and current position if it is not out of bounds
        # meaning if not obstacle or out of search space
        if not self.position_out_of_bounds(new_pos):
            self.velocity_x = new_vel_x
            self.velocity_y = new_vel_y
            self.current_position = new_pos

        return self.current_position  # return the current position

    def position_out_of_bounds(self, pos: Coordinate):
        # check if within bounds OR colliding with an obstacle
        xout: bool = not (0 <= pos.x <= self.environment.width - 1)
        yout: bool = not (0 <= pos.y <= self.environment.height - 1)
        obs: bool = self.environment.distance_to_closest_obstacle(pos) < 0

        return xout or yout or obs
