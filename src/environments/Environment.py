import math
import random

import matplotlib.pyplot as plt

from helpers.Coordinate import Coordinate
from helpers.Obstacle import Obstacle
from helpers.Route import Route


class Environment:
    """
    environments Class, used by all the Bio-Inspired AI algorithms.

    Note that we may want to use specific implementations of
    the environments class for each algorithm, as some use pheromones, etc.
    """

    def __init__(self, width: int, height: int, obstacles=None, start=None, end=None):
        """
        Constructor for the environments class.
        :param width: of the environment
        :param height: of the environment
        :param obstacles: of the environment (each of type Obstacle)
        :param start: of the agents (we assume all agents start at the same position).
        Default: (0, 0)
        :param end: of the agents (we assume all agents aim to arrive to the same position).
        Default: (width - 1, height - 1)
        """

        self.width: int = width
        self.height: int = height

        # Set obstacles of the environment
        if obstacles is None:
            self.obstacles = []
        else:
            self.obstacles = obstacles

        # We set the initial and final position of our environment (by default, the opposite corners)
        if start is None:
            self.start = Coordinate(0, 0)
        else:
            self.start: Coordinate = start

        if end is None:
            self.end = Coordinate(width - 1, height - 1)
        else:
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

    def distance_to_closest_obstacle(self, position) -> float:
        """
        Returns the smallest distance to an obstacle, or -1 if it is the position is not valid (out of bounds or
        colliding with an obstacle)

        :param position: The position to be checked
        :return: Whether the position is in the current environment
        """

        # Check whether the given position is within the bounds of the environment
        if not position.x_between(0, self.width) or not position.y_between(0, self.height):
            return -1.0

        # We initially set the minimum distance to the maximum possible distance
        minimum_distance = distance(self.start, self.end)

        # Check whether the given position is not colliding with an obstacle
        for obstacle in self.obstacles:
            minimum_distance = distance(obstacle.center, position)
            if minimum_distance <= obstacle.radius:
                return -1.0

        return minimum_distance

    def __str__(self):
        """
        Representation of an environments as defined by the input file format.

        :return: String representation
        """
        string = f"Environment of size {self.width}x{self.height}\n"
        string += f"Start: {self.start.x}, {self.start.y}\n"
        string += f"End: {self.end.x}, {self.end.y}\n"
        string += "Obstacles:\n"
        for obstacle in self.obstacles:
            string += f"  Center: {obstacle.center}, Radius: {obstacle.radius}\n"
        return string

    def visualize_environment(self, route: Route = None):
        fig, ax = plt.subplots()

        # Draw obstacles as circles
        for obstacle in self.obstacles:
            # We need to convert the obstacle to a (int, int) because matplotlib requires it is subscriptable
            circle = plt.Circle((obstacle.center.x, obstacle.center.y), obstacle.radius, color='darkgrey')
            ax.add_artist(circle)

        # Draw start and end points as squares
        ax.add_patch(plt.Rectangle((self.start.x, self.start.y), 1, 1, color='green'))  # Start in green
        ax.add_patch(plt.Rectangle((self.end.x, self.end.y), 1, 1, color='red'))  # End in red

        # If a route is provided, draw the route on the grid
        if route is not None:
            x_values = [point.x for point in route.get_route()]
            y_values = [point.y for point in route.get_route()]
            ax.plot(x_values, y_values, 'b-', linewidth=2)  # Route in blue, with a bigger width to make it more visible

        # Adjust axes limits
        ax.set_xlim(-1, self.width)
        ax.set_ylim(-1, self.height)

        plt.show()

    @staticmethod
    def create_environment(width: int, height: int, obstacle_values,
                           start_pos: Coordinate = None, end_pos: Coordinate = None):
        """
        Method that creates an environment with obstacles.

        :param width: of the environment
        :param height: of the environment
        :param obstacle_values: a list of obstacle types we want, as a pair of ints (x, y)
        where x is the radius and y is the frequency (in %)
        :param start_pos: of the agents (we assume all agents start at the same position).
        Default: (0, 0)
        :param end_pos: of the agents (we assume all agents aim to arrive to the same position).
        Default: (width - 1, height - 1)
        :return: an environment object with the specified parameters
        """

        # First, we check that creating the environment is possible

        # Whether the variables given are not negative, and that the start and end positions are both given or not given
        if width < 0 or height < 0:
            raise ValueError("The given variables are not valid: make sure that width, "
                             "height, obstacle_radius, and obstacle_percentage are all non-negative")
        if (start_pos is None) != (end_pos is None):
            raise ValueError("The given start_pos and end_pos are not valid: make sure that both "
                             "start_pos and end_pos are given or not given")

        # If given start_pos and end_pos, check that they are within the bounds of the environment
        if ((start_pos is not None and end_pos is not None) and
                (start_pos.x < 0 or start_pos.y < 0 or end_pos.x < 0 or end_pos.y < 0 or start_pos.x >= width
                 or start_pos.y >= height or end_pos.x >= width or end_pos.y >= height or
                 (start_pos.x == end_pos.x and start_pos.y == end_pos.y))):
            raise ValueError("The given start_pos and end_pos are not valid: make sure that both start_pos and end_pos")

        # We now set the legal area for the obstacles
        left, right, top, bottom = compute_inner_space(width, height)

        obstacles = []

        for obstacle in obstacle_values:
            amount_of_obstacles = get_amount_of_obstacles(height, width, obstacle[1], obstacle[0])

            current_amount = 0

            # Generate obstacles
            while current_amount < amount_of_obstacles:
                obstacle_pos = Coordinate(random.randint(left, right), random.randint(bottom, top))

                if all(distance(obstacle_pos, obstacle2.center) >= (obstacle[0] + obstacle2.radius) for obstacle2 in obstacles):
                    obstacles.append(Obstacle(obstacle_pos, obstacle[0]))
                    current_amount += 1

        print("Finished preparing the environment")

        return Environment(width, height, obstacles, start_pos, end_pos)


############################################################################################################
# Helper functions


def compute_inner_space(width, height):
    """
    Obstacles can only be generated in the central 80% of the grid
    :param width: of the environment
    :param height: of the environment
    :return: the four boundaries of the inner space (where obstacles can be placed)
    """

    width_margin = width * 0.1
    height_margin = height * 0.1

    left_boundary = width_margin
    right_boundary = width - width_margin
    bottom_boundary = height_margin
    top_boundary = height - height_margin

    return int(left_boundary), int(right_boundary), int(top_boundary), int(bottom_boundary)


def get_amount_of_obstacles(height, width, obstacle_percentage, obstacle_radius):
    """
    Calculate the amount of obstacles to be placed in the environment
    :param height: of the environment
    :param width: of the environment
    :param obstacle_percentage: how many obstacles (in percentage, from 0 to 1) to generate
    :param obstacle_radius: the radius of the obstacles
    :return: how many obstacles to place in the environment
    """

    # Area occupied by one obstacle
    obstacle_area = (obstacle_radius * 2 + 1) ** 2

    # Calculate how many cells we can place obstacles in (80% of the real total amount)
    total_cells = width * height * 0.8

    # Hence, the max amount of possible obstacles is:
    max_amount = total_cells / obstacle_area

    # Apply the percentage
    amount_of_obstacles = int(max_amount * obstacle_percentage)

    return amount_of_obstacles


def distance(pair1: Coordinate, pair2: Coordinate):
    """
    Euclidean distance between two pairs of coordinates
    :param pair1: a pair of coordinates
    :param pair2: a pair of coordinates
    :return: the distance between the two pairs
    """

    return math.sqrt((pair1.x - pair2.x) ** 2 + (pair1.y - pair2.y) ** 2)
