import random

from helpers.Route import Route
from agents.Particle import Particle


class ParticleSwarmOptimization:
    def __init__(self, environment, path_specification, num_particles, convergence_iter, trail, step_size,
                 inertia_weight):
        self.environment = environment
        self.path_specification = path_specification
        self.num_particles = num_particles
        self.particles = []
        self.global_best_pos = path_specification.start
        self.route = Route(path_specification.start)

        # Initialize particles
        for _ in range(num_particles):
            velocity_x = random.randint(-1, 1)
            velocity_y = random.randint(-1, 1)
            particle = Particle(environment, path_specification, convergence_iter, trail, velocity_x, velocity_y,
                                step_size, inertia_weight)
            self.particles.append(particle)

    def run(self):
        for _ in range(100):
            # two loops over particles, first find the global best then the particles
            for particle in self.particles:
                if ((particle.evaluate_fitness(particle.current_position) <
                     particle.evaluate_fitness(self.global_best_pos))
                        and not particle.position_out_of_bounds(particle.current_position)):
                    self.global_best_pos = particle.current_position

            for particle in self.particles:
                particle.update_particle(self.global_best_pos, particle.personal_best_pos)

            # Add global best to route
            self.route.add(self.global_best_pos)

        return self.route
