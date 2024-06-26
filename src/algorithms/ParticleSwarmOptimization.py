import math
import random

from agents.Particle import Particle
from algorithms.Algorithm import Algorithm
from environments.Environment import Environment
from helpers.Coordinate import Coordinate
from helpers.Levy import levy_flight
from helpers.Path import Path
from helpers.PathSpecification import PathSpecification


class ParticleSwarmOptimization(Algorithm):
    """
    Particle Swarm Optimization is a population-based optimization technique inspired by the social behavior of birds
    flocking or fish schooling.

    In this algorithm, particles (agents) move through the search space and update their
    positions based on their own best position and the best position found by the swarm.
    This way, the particles converge to the best solution found by the swarm.

    We implement Lévy flights to get particles out of poor areas.
    Lévy flight is a random walk where the step lengths are drawn from a Lévy distribution.
    This allows the particles to explore the search space more effectively.
    """

    def __init__(self, environment: Environment, num_particles: int,
                 convergence_iter: int, trail: float, step_size: int, inertia_weight: float, max_iter: int = 100,
                 obstacle_distance: int = 0):
        super().__init__(environment, step_size, obstacle_distance)

        self.num_particles = num_particles
        self.max_iter = max_iter
        self.convergence_iter = convergence_iter
        self.trail = trail
        self.inertia_weight = inertia_weight

    def run(self, path_specification: PathSpecification, print_progress: bool = True) -> (Path, list):
        """
        The Particle Swarm Optimization algorithm to find the shortest path across generations.

        :param path_specification: The start and end coordinates of the path
        :param print_progress: Whether we print the result of each generation

        :return: The best path found and a list of checkpoints
        """

        # Initialize variables
        particles = []
        global_best_pos = path_specification.start
        levy_best = path_specification.start
        path = Path(path_specification.start)

        # Initialize particles with random velocities
        for _ in range(self.num_particles):
            velocity_x = random.uniform(-1, 1)
            velocity_y = random.uniform(-1, 1)
            particle = Particle(self.environment, path_specification, self.convergence_iter, self.trail, velocity_x,
                                velocity_y,
                                self.step_size, self.inertia_weight)
            particles.append(particle)

        checkpoints = []

        const_count: int = 0

        for generation in range(self.max_iter):
            # Get the coefficients c1 and c2 based on iteration
            c1: float = (math.cos((math.pi / 2) * (generation / self.max_iter)) *
                         math.cos(math.pi * (generation / self.max_iter)) + 1.5)
            c2: float = (math.sin((math.pi / 2) * (generation / self.max_iter)) *
                         math.sin(math.pi * ((generation / self.max_iter) + 1.5)) + 1.5)

            # Update the speeds and positions of particles
            for particle in particles:
                particle.update_particle(global_best_pos, particle.personal_best_pos,
                                         c1, c2, generation, self.max_iter)

            # Check if the particles have fallen into poor areas and get them out with Lévy flight
            # The particles are judged to have fallen into a poor area if they do not change in more than 10 iters
            if levy_best == global_best_pos:
                const_count += 1
                if const_count > 10:
                    # Do Lévy flight
                    for particle in particles:
                        levy_steps = levy_flight(beta=1.5, size=2)
                        levy_vel_x = levy_steps[0]
                        levy_vel_y = levy_steps[1]
                        levy_pos = Coordinate(particle.current_position.x + levy_vel_x,
                                              particle.current_position.y + levy_vel_y)

                        # Take the direction that is allowed
                        if self.environment.distance_to_closest_obstacle(levy_pos) > 0:
                            if 0 <= levy_pos.x <= self.environment.width - 1:
                                particle.current_position.x = levy_pos.x
                                particle.velocity_x = levy_vel_x
                            if 0 <= levy_pos.y <= self.environment.height - 1:
                                particle.current_position.y = levy_pos.y
                                particle.velocity_y = levy_vel_y
            else:
                # Reset count and levy best
                const_count = 0
                levy_best = global_best_pos

            # Calculate particle fitness values, update personal bests and global best
            for particle in particles:
                fitness: float = self.evaluate_fitness(particle.current_position)
                fitness_pb: float = self.evaluate_fitness(particle.personal_best_pos)
                fitness_gb: float = self.evaluate_fitness(global_best_pos)

                if fitness < fitness_pb:
                    particle.personal_best_pos = particle.current_position
                if fitness < fitness_gb:
                    global_best_pos = particle.current_position

            # Add global best to the path
            path.add(global_best_pos)
            if print_progress:
                print(global_best_pos)

            if (generation + 1) == 1 or (generation + 1) == 3 or (generation + 1) == 5 \
                    or (generation + 1) == 9 or (generation + 1) % 10 == 0:
                checkpoints.append(path.size())

            # Check termination conditions (global best at end position)
            # We want to see if the global best is within 0.5
            # (safe margin) of the end position set the global best to end, append end to path and stop
            if global_best_pos.x_between(self.environment.end.x - 0.5, self.environment.end.x + 0.5) and \
                    global_best_pos.y_between(self.environment.end.y - 0.5, self.environment.end.y + 0.5):
                path.add(self.environment.end)
                return path, checkpoints

        return path, checkpoints

    def evaluate_fitness(self, pos: Coordinate):
        # Minimize the distance to the goal but maximize the distance to the nearest obstacle
        distance_to_goal = math.sqrt((pos.x - self.environment.end.x) ** 2 + (pos.y - self.environment.end.y) ** 2)
        distance_to_obstacle = self.environment.distance_to_closest_obstacle(pos)

        # For now, we assign weight 1 to the goal distance and 0 to the obstacle distance
        # effectively only the goal distance is considered
        weight_goal: float = 1.0
        weight_obstacle: float = 0.0

        # Since we need to maximize one and minimize the other, we invert distance to an obstacle, so we can minimize it
        return weight_goal * distance_to_goal + weight_obstacle * (1 / distance_to_obstacle)
