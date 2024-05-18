from algorithms.Algorithm import Algorithm
from environments.Environment import Environment
from agents.Firefly import Firefly
from helpers.PathSpecification import PathSpecification
from helpers.Path import Path


class FireflyAlgorithm(Algorithm):
    """
    Firefly Algorithm is a population-based optimisation technique inspired by the social behaviour of fireflies.

    In this algorithm, fireflies (agents) move through the search space and update their positions based on the
    attractiveness of other fireflies. The attractiveness is determined by the brightness of the firefly, which is
    determined by the fitness value of the firefly. This way, the fireflies converge to the best solution found by the
    swarm.

    We implement Lévy flights to get fireflies out of poor areas. Lévy flight is a random walk where the step lengths
    are drawn from a Lévy distribution. This allows the fireflies to explore the search space more effectively.
    """

    def __init__(self, environment: Environment, population_size,
                 alpha_init: float = 1.0, alpha_end: float = 0.1, gamma_init: float = 0.1, gamma_end: float = 5,
                 beta=1, max_iter=100, step_size: int = 1, obstacle_distance: int = 0):
        assert gamma_init < gamma_end, "Gamma init must be smaller than gamma end"
        assert alpha_init > alpha_end, "Alpha init must be greater than alpha end"

        super().__init__(environment, step_size, obstacle_distance)
        self.max_iter = max_iter
        self.population_size = population_size
        self.alpha_init = alpha_init
        self.alpha_end = alpha_end
        self.gamma_init = gamma_init
        self.gamma_end = gamma_end
        self.beta = beta

    def run(self, path_specification: PathSpecification, print_progress: bool = True) -> (Path, list):
        """
        The Firefly Algorithm to find the shortest path across generations.

        :param path_specification: The start and end coordinates of the path
        :param print_progress: Whether we print the result of each generation

        :return: The best path found and a list of checkpoints
        """
        # Initialize variables
        path_specification = path_specification
        path = Path(path_specification.start)

        best = None
        fireflies = [
            Firefly(self.environment, path_specification, self.alpha_init, self.alpha_end, self.beta, self.gamma_init,
                    self.gamma_end, self.step_size, self.obstacle_distance) for _ in range(self.population_size)]

        checkpoints = []

        if not best or (fireflies[0].intensity > best):
            best = fireflies[0].intensity

        for generation in range(self.max_iter):
            for i in range(len(fireflies)):
                const_count = 0
                for j in range(len(fireflies)):
                    # We want to maximize the brightness (i.e. minimize distance to goal)
                    if fireflies[i].intensity < fireflies[j].intensity:
                        adaptive = generation / self.max_iter
                        fireflies[i].move_towards(fireflies[j].position, adaptive)

                        # We double-check because of uncertainty in the fireflies' movement
                        if fireflies[i].intensity < fireflies[j].intensity:
                            fireflies[i].move_towards(fireflies[j].position, adaptive)
                    # If we don't move for 10 fireflies, make a Lévy flight
                    elif const_count >= 10:
                        const_count = 0
                        fireflies[i].random_move(0.1)
                    else:
                        const_count += 1

                    fireflies[i].update_intensity()

                    if (generation + 1) == 1 or (generation + 1) == 3 or (generation + 1) == 5 \
                            or (generation + 1) == 9 or (generation + 1) % 10 == 0:
                        checkpoints.append(path.size())

                    if fireflies[i].reach_end():
                        return fireflies[i].path, checkpoints

                    if fireflies[i].intensity > best:
                        best = fireflies[i].intensity
                        path = fireflies[i].path
                        print(fireflies[i].intensity)

        return path, checkpoints
