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
                 convergence_iter: int, trail: float, velocity_x: int, velocity_y: int, step_size: int = 1,
                 inertia_weight: int = 1):
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

    def update_particle(self, global_best_pos: Coordinate, personal_best_pos: Coordinate):
        # need to do the update with integers
        # random variables, need to be ints
        r1: int = self.rand.randint(0, 2)
        r2: int = self.rand.randint(0, 2)
        new_vel_x: int = (self.w * self.velocity_x + r1 * (personal_best_pos.x - self.current_position.x)
                          + r2 * (global_best_pos.x - self.current_position.x))
        new_vel_y: int = (self.w * self.velocity_y + r1 * (personal_best_pos.y - self.current_position.y)
                          + r2 * (global_best_pos.y - self.current_position.y))
        # clamp the velocities into the range [-1, 1]
        new_vel_x = max(-1, min(1, new_vel_x))
        new_vel_y = max(-1, min(1, new_vel_y))
        # update the position, and the personal best position and return the position to update global best
        new_pos: Coordinate = Coordinate(self.current_position.x + new_vel_x, self.current_position.y + new_vel_y)
        # update the velocities and personal best and return the new position if it is not out of bounds
        if not self.position_out_of_bounds(new_pos):
            self.velocity_x = new_vel_x
            self.velocity_y = new_vel_y
            self.current_position = new_pos
            if self.evaluate_fitness(new_pos) < self.evaluate_fitness(personal_best_pos):
                self.personal_best_pos = new_pos

        return self.personal_best_pos  # return the personal best to compete for global best

    def evaluate_fitness(self, pos: Coordinate):
        # minimize the distance to the goal but maximize the distance to the nearest obstacle
        distance_to_goal = math.sqrt((pos.x - self.end.x) ** 2 + (pos.y - self.end.y) ** 2)
        distance_to_obstacle = self.environment.distance_to_closest_obstacle(pos)

        # for now, we assign weight 1 to the goal distance and 0 to the obstacle distance
        # effectively only the goal distance is considered
        weight_goal: float = 1.0
        weight_obstacle: float = 300.0

        # since we need to maximize one and minimize the other, we invert distance to obstacle, so we can minimize it

        return weight_goal * distance_to_goal + weight_obstacle * (1 / distance_to_obstacle)

    def position_out_of_bounds(self, pos: Coordinate):
        # check if within bounds OR colliding with an obstacle
        xout: bool = not pos.x_between(0, self.environment.width)
        yout: bool = not pos.y_between(0, self.environment.height)
        obs: bool = self.environment.distance_to_closest_obstacle(pos) < 0

        return xout or yout or obs
