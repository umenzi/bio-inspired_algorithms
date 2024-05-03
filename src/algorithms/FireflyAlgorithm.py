from environments.Environment import Environment
from agents.Firefly import Firefly
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

    def __init__(self, environment: Environment, path_specification: PathSpecification, population_size, alpha_init=1.0,
                 alpha_end=0.1, gamma_init=0.1, gamma_end: int = 5, beta=1, max_iter=100,
                 step_size: int = 1, obstacle_distance: int = 0):
        assert gamma_init < gamma_end, "Gamma init must be smaller than gamma end"
        assert alpha_init > alpha_end, "Alpha init must be greater than alpha end"

        self.environment = environment
        self.path_specification = path_specification
        self.route = Route(path_specification.start)

        self.max_iter = max_iter
        self.best = None
        self.fireflies = [
            Firefly(environment, path_specification, alpha_init, alpha_end, beta, gamma_init,
                    gamma_end, step_size, obstacle_distance) for _ in range(population_size)]

    def run(self):
        if not self.best or (self.fireflies[0].intensity > self.best):
            self.best = self.fireflies[0].intensity

        for w in range(self.max_iter):
            for i in range(len(self.fireflies)):
                const_count = 0
                for j in range(len(self.fireflies)):
                    # We want to maximize the brightness (i.e. minimize distance to goal)
                    if self.fireflies[i].intensity < self.fireflies[j].intensity:
                        adaptive = w / self.max_iter
                        self.fireflies[i].move_towards(self.fireflies[j].position, adaptive)

                        # We double-check because of uncertainty in the fireflies' movement
                        if self.fireflies[i].intensity < self.fireflies[j].intensity:
                            self.fireflies[i].move_towards(self.fireflies[j].position, adaptive)
                    # If we don't move for 10 fireflies, make a Lévy flight
                    elif const_count >= 10:
                        const_count = 0
                        self.fireflies[i].random_move()
                        # self.fireflies[i].levy_move(0.1)
                    else:
                        const_count += 1

                    self.fireflies[i].update_intensity()

                    if self.fireflies[i].reach_end():
                        return self.fireflies[i].route

                    if self.fireflies[i].intensity > self.best:
                        self.best = self.fireflies[i].intensity
                        self.route = self.fireflies[i].route
                        print(self.fireflies[i].intensity)

        return self.route
