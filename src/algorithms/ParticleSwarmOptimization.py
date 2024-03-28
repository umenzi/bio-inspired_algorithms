import math
import random
import numpy as np

from helpers.Route import Route
from helpers.Coordinate import Coordinate
from helpers.PathSpecification import PathSpecification
from environments.Environment import Environment
from agents.Particle import Particle


class ParticleSwarmOptimization:
    def __init__(self, environment: Environment, path_specification: PathSpecification, num_particles: int,
                 convergence_iter: int, trail: float, step_size: int, inertia_weight: float, max_iter: int = 100):
        self.environment = environment
        self.path_specification = path_specification
        self.num_particles = num_particles
        self.particles = []
        self.global_best_pos = path_specification.start
        self.levy_best = path_specification.start
        self.route = Route(path_specification.start)
        self.max_iter = max_iter

        # Initialize particles with random velocities
        for _ in range(num_particles):
            velocity_x = random.uniform(-1, 1)
            velocity_y = random.uniform(-1, 1)
            particle = Particle(environment, path_specification, convergence_iter, trail, velocity_x, velocity_y,
                                step_size, inertia_weight)
            self.particles.append(particle)

    def run(self):
        const_count: int = 0
        for _ in range(self.max_iter):
            # get the coefficients c1 and c2 based on iteration
            c1: float = math.cos((math.pi / 2) * (_ / self.max_iter)) * math.cos(math.pi * (_ / self.max_iter)) + 1.5
            c2: float = (math.sin((math.pi / 2) * (_ / self.max_iter)) * math.sin(math.pi * ((_ / self.max_iter) + 1.5))
                         + 1.5)
            # update the speeds and positions of particles
            for particle in self.particles:
                particle.update_particle(self.global_best_pos, particle.personal_best_pos, c1, c2, _, self.max_iter)

            # check if the particles have fallen into poor areas and get them out with Levy flight
            # TODO: implement Levy flight
            # the particles are judged to have fallen into a poor area if they do not change in more than 10 iters
            if self.levy_best == self.global_best_pos:
                const_count += 1
                if const_count > 10:
                    # do Lévy flight
                    for particle in self.particles:
                        levy_steps = self.levy_flight(beta=1.5, size=2)
                        levy_vel_x = levy_steps[0]
                        levy_vel_y = levy_steps[1]
                        levy_pos = Coordinate(particle.current_position.x + levy_vel_x,
                                              particle.current_position.y + levy_vel_y)
                        # take the direction that is allowed
                        if self.environment.distance_to_closest_obstacle(levy_pos) > 0:
                            if 0 <= levy_pos.x <= self.environment.width - 1:
                                particle.current_position.x = levy_pos.x
                                particle.velocity_x = levy_vel_x
                            if 0 <= levy_pos.y <= self.environment.height - 1:
                                particle.current_position.y = levy_pos.y
                                particle.velocity_y = levy_vel_y
            else:
                # reset count and levy best
                const_count = 0
                self.levy_best = self.global_best_pos

            # calculate particle fitness values, update personal bests and global best
            for particle in self.particles:
                fitness: float = self.evaluate_fitness(particle.current_position)
                fitness_pb: float = self.evaluate_fitness(particle.personal_best_pos)
                fitness_gb: float = self.evaluate_fitness(self.global_best_pos)
                if fitness < fitness_pb:
                    particle.personal_best_pos = particle.current_position
                if fitness < fitness_gb:
                    self.global_best_pos = particle.current_position

            # Add global best to route
            self.route.add(self.global_best_pos)
            print(self.global_best_pos)

            # check termination conditions (global best at end position)
            # we want to see if the global best is within 0.5 (safe margin) of the end position set the global best to
            # end, append end to route and stop
            if self.global_best_pos.x_between(self.environment.end.x - 0.5, self.environment.end.x + 0.5) and \
                    self.global_best_pos.y_between(self.environment.end.y - 0.5, self.environment.end.y + 0.5):
                self.route.add(self.environment.end)
                return self.route

        return self.route

    def evaluate_fitness(self, pos: Coordinate):
        # minimize the distance to the goal but maximize the distance to the nearest obstacle
        distance_to_goal = math.sqrt((pos.x - self.environment.end.x) ** 2 + (pos.y - self.environment.end.y) ** 2)
        distance_to_obstacle = self.environment.distance_to_closest_obstacle(pos)

        # for now, we assign weight 1 to the goal distance and 0 to the obstacle distance
        # effectively only the goal distance is considered
        weight_goal: float = 1.0
        weight_obstacle: float = 0.0

        # since we need to maximize one and minimize the other, we invert distance to obstacle, so we can minimize it

        return weight_goal * distance_to_goal + weight_obstacle * (1 / distance_to_obstacle)

    def levy_flight(self, beta: float, size: int):
        # Draw samples from a uniform distribution
        u = np.random.uniform(0.01, 1, size=size)

        # Calculate the corresponding step lengths
        steps = u ** (-1 / beta)

        # make sure the steps are between -2 and 2 (obstacle radius)
        steps = np.clip(steps, -2, 2)

        return steps
