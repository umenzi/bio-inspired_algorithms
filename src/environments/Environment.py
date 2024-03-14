import math
import random

import matplotlib.pyplot as plt
import numpy as np

from helpers.Coordinate import Coordinate
from helpers.Route import Route


def compute_inner_space(width, height):
    """
    Obstacles can only be generated in the central 80% of the grid
    :param width:
    :param height:
    :return:
    """
    width_margin = width * 0.1
    height_margin = height * 0.1

    left_boundary = width_margin
    right_boundary = width - width_margin
    bottom_boundary = height_margin
    top_boundary = height - height_margin

    return int(left_boundary), int(right_boundary), int(top_boundary), int(bottom_boundary)


def get_amount_of_obstacles(height, width, obstacle_percentage, obstacle_radius):
    # Area occupied by one obstacle
    obstacle_area = (obstacle_radius * 2 + 1) ** 2

    # Calculate how many cells we can place obstacles in (80% of the real total amount)
    total_cells = width * height * 0.8

    # Hence, the max amount of possible obstacles is:
    max_amount = total_cells / obstacle_area

    # Apply the percentage
    amount_of_obstacles = int(max_amount * obstacle_percentage)

    return amount_of_obstacles


def distance(pair1, pair2):
    return math.sqrt((pair1[0] - pair2[0]) ** 2 + (pair1[1] - pair2[1]) ** 2)


class Environment:
    """
    environments Class, used by all the Bio-Inspired AI algorithms.

    Note that we may want to use specific implementations of
    the environments class for each algorithm, as some use pheromones, etc.
    """

    def __init__(self, width: int, height: int, grid, start=None, end=None):
        self.width: int = width
        self.height: int = height
        self.grid = grid

        self.start: Coordinate = start
        self.end: Coordinate = end

    def get_width(self):
        """
        Width getter
        :return: width of the environment
        """
        return self.width

    def get_height(self):
        """
        Height getter
        :return: height of the environment
        """
        return self.height

    def reset(self):
        """
        Reset the environment for a new shortest path problem.
        """
        pass

    def in_bounds(self, position):
        """
        Check whether a coordinate lies in the current environment.

        :param position: The position to be checked
        :return: Whether the position is in the current environment
        """
        return position.x_between(0, self.width) and position.y_between(0, self.height) and self.grid[position.x][
            position.y] == 1

    def __str__(self):
        """
        Representation of an environments as defined by the input file format.

        :return: String representation
        """
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.height)
        string += " \n"
        for y in range(self.height):
            for x in range(self.width):
                string += str(self.grid[x][y])
                string += " "
            string += "\n"
        return string

    def visualize_environment(self, route: Route = None):
        # Create a copy of the grid to avoid modifying the original
        grid_copy = self.grid.copy()

        # Set start and end positions to special values
        grid_copy[self.start.x][self.start.y] = 2
        grid_copy[self.end.x][self.end.y] = 3

        # If a route is provided, draw the route on the grid
        if route is not None:
            current_point: Coordinate = route.start
            grid_copy[current_point.x][current_point.y] = 4

            for direction in route.get_route():
                current_point = current_point.add_direction(direction)
                grid_copy[current_point.x][current_point.y] = 4

        # Create a color map for the grid
        cmap = plt.cm.colors.ListedColormap(['darkgrey', 'white', 'red', 'green', 'blue'])

        # Create a bounds for the color map
        bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]

        # Create a norm for the color map
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

        # Plot the grid
        plt.imshow(grid_copy, cmap=cmap, norm=norm, origin='lower')

        # Hide the grid lines
        plt.grid(False)

        # Hide the x and y ticks
        plt.xticks([])
        plt.yticks([])

        # Show the plot
        plt.show()

    @staticmethod
    def create_environment(width: int, height: int, start_pos: (int, int), end_pos: (int, int),
                           obstacle_radius: int, obstacle_percentage: float):
        """
        Method that creates an environment with obstacles.

        :param width: of the environment
        :param height: of the environment
        :param start_pos: of the agents (we assume all agents start at the same position)
        :param end_pos: of the agents (we assume all agents aim to arrive to the same position)
        :param obstacle_radius: radius of the obstacles, which have a circular shape
        :param obstacle_percentage: how many obstacles (in percentage, from 0 to 1) to generate
        :return: an environment object with the specified parameters
        """

        # First, we check that creating the environment is possible
        if width < 0 or height < 0 or obstacle_radius < 0 or obstacle_percentage < 0.0 \
                or not (0 <= start_pos[0] <= width) or not (0 <= start_pos[1] <= height) or not \
                (0 <= end_pos[0] <= width) or not (0 <= end_pos[1] <= height) or \
                (start_pos[0] == end_pos[0] and start_pos[1] == end_pos[1]):
            raise ValueError("Width and height must be positive integers")

        # Initialize an empty grid
        # 1 means it's legal space
        # 0 means it's an obstacle
        grid = np.ones((width, height))

        # We now set the legal area for the obstacles
        left, right, top, bottom = compute_inner_space(width, height)

        amount_of_obstacles = get_amount_of_obstacles(height, width, obstacle_percentage, obstacle_radius)

        obstacles = []

        minimum_obstacle_distance = obstacle_radius * 2

        # Generate obstacles
        while len(obstacles) < amount_of_obstacles:
            obstacle_pos = (random.randint(left, right), random.randint(bottom, top))

            if all(distance(obstacle_pos, obstacle) >= minimum_obstacle_distance for obstacle in obstacles):
                obstacles.append(obstacle_pos)

                # We complete the grid
                for x in range(obstacle_pos[0] - obstacle_radius, obstacle_pos[0] + obstacle_radius):
                    for y in range(obstacle_pos[1] - obstacle_radius, obstacle_pos[1] + obstacle_radius):
                        grid[x, y] = 0

        print("Finished preparing the environment")

        return Environment(width, height, grid, Coordinate(start_pos[0], start_pos[1]),
                           Coordinate(end_pos[0], end_pos[1]))
