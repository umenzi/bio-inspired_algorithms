from environments.Environment import Environment
from helpers.Firefly import Firefly
from helpers.PathSpecification import PathSpecification
from helpers.Route import Route


class FireflyAlgorithm:
    """
    Firefly Algorithm is a population-based optimisation technique inspired by the social behaviour of fireflies.

    In this algorithm, fireflies (agents) move through the search space and update their positions based on the
    attractiveness of other fireflies. The attractiveness is determined by the brightness of the firefly, which is
    determined by the fitness value of the firefly. This way, the fireflies converge to the best solution found by the
    swarm.

    We implement Lévy flights to get fireflies out of poor areas. Lévy flight is a random walk where the step lengths
    are drawn from a Lévy distribution. This allows the fireflies to explore the search space more effectively.
    """

    def __init__(self, environment: Environment, path_specification: PathSpecification, population_size: int,
                 randomness_strength: int = 1.0, attractiveness: int = 1.0, absorption: int = 0.01, max_iter: int = 100,
                 lower_bound: int = -5, upper_bound: int = 5, dimension: int = 2):
        self.environment = environment
        self.path_specification = path_specification
        self.route = Route(path_specification.start)

        self.max_iter = max_iter
        self.best = None
        self.fireflies = [Firefly(randomness_strength, attractiveness, absorption,
                                  upper_bound, lower_bound, dimension)
                          for _ in range(population_size)]

    def run(self, function):
        # TODO: Function needs to be removed
        if not self.best or (self.fireflies[0].intensity > self.best):
            self.best = self.fireflies[0].intensity

        for _ in range(self.max_iter):
            for i in range(len(self.fireflies)):
                for j in range(len(self.fireflies)):
                    # If i is brighter than j, move j towards i
                    if self.fireflies[i].intensity >= self.fireflies[j].intensity:
                        self.fireflies[j].move_towards(self.fireflies[i].position)
                        self.fireflies[j].update_intensity(function)

                        self.best = min(self.fireflies[i].intensity, self.best)

        return self.best
