import random

from algorithms.Algorithm import Algorithm
from environments.ACOEnvironment import ACOEnvironment
from agents.Ant import Ant
from multiprocessing import Pool

from environments.Environment import Environment
from helpers.Path import Path
from helpers.PathSpecification import PathSpecification


class AdpeAntColonyOptimization(Algorithm):
    """
    Ant Colony Optimization is an algorithm based on the exploratory behaviour of ants to find food.

    This is Adaptive Dynamic Probabilistic Elitism (ADPE) Ant Colony Optimization, an extension of the original ACO
    algorithm.
    It introduces Probabilistic Elitism, where the pheromones of the best path are added with a certain
    probability.
    This reduces the chance of the algorithm getting stuck in a local minimum with respect to the original
    algorithm.
    """

    def __init__(self, environment: Environment, ants_per_gen: int, generations: int, q: int, evaporation: float,
                 convergence_iter: int, no_change_iter: int, trail: float, sigma_elite: int,
                 default_elitist_probability: float = 0.5, step_size: int = 1, num_processes: int = 6,
                 obstacle_distance: int = 0):
        super().__init__(environment, step_size, obstacle_distance)
        self.environment: ACOEnvironment = ACOEnvironment.create_from_environment(self.environment)
        self.ants_per_gen: int = ants_per_gen
        self.generations: int = generations
        self.q: int = q
        self.evaporation: float = evaporation
        self.convergence_iter: int = convergence_iter
        self.no_change_iter: int = no_change_iter
        self.trail: float = trail
        self.num_processes: int = num_processes
        self.sigma_elite: int = sigma_elite
        self.default_elitist_probability: float = default_elitist_probability
        self.maximum_global_tour_length = None

    def run(self, path_specification: PathSpecification, print_progress: bool = True) -> (Path, list):
        """
        The ACO algorithm to find the shortest path across generations.

        We first reset the pheromones (i.e. initialize them), then we create a specified
        number of ants for each generation and keep track of the shortest path found amongst all of them.
        After each generation, we evaporate the existing pheromones by the chosen evaporation parameter
        ρ, and we add the pheromones of each path found by the ants.
        This process is shown in the following pseudocode block.

        :param path_specification: The start and end coordinates of the path
        :param print_progress: Whether we print the result of each generation
        :return: The best path found
        """

        self.environment.reset()

        best_path: Path = None
        count = 0
        checkpoints = []

        for generation in range(self.generations):
            if print_progress:
                print("Generation", generation)

            # We introduce multi-threading
            # Basically, each ant compute their shortest path on a separate thread
            # This way, more ants are deployed to find paths (hence, the better our algorithm will be)
            with Pool(self.num_processes) as p:
                paths = p.map(self.run_parallel, [path_specification] * self.ants_per_gen)

            paths = [r for r in paths if r is not None]

            prev = best_path

            for path in paths:
                if best_path is None:
                    best_path = path
                if path.shorter_than(best_path):
                    best_path = path

            # We get the longest path for the probabilistic Elitism
            if self.maximum_global_tour_length is None:
                self.maximum_global_tour_length = best_path.size()

            if best_path is not None and prev is not None and prev == best_path:
                count += 1
            else:
                count = 0

            if print_progress:
                print("Paths found so far:", len(paths))
                if best_path is not None:
                    print("Best path's length:", best_path.size())
                print("\n")

            if count >= self.no_change_iter:
                if print_progress:
                    print("No change for many generations")
                return best_path, checkpoints

            if len(paths) == 0:
                continue

            self.environment.evaporate(self.evaporation)

            self.environment.add_pheromone_paths(paths, self.q)

            # Performance Improvement: Adding the pheromones of the best path using elitism
            # We use Probabilistic Elitism, where we add the pheromones of the best path with a certain probability
            # This reduces the chance of the algorithm getting stuck in a
            # local minimum with respect to the original elitist algorithm
            p: float = 1 - best_path.size() / self.maximum_global_tour_length
            if p < 0:
                p = self.default_elitist_probability

            if random.random() < p:
                for i in range(self.sigma_elite):
                    self.environment.add_pheromone_path(best_path, self.q)

            if (generation + 1) == 1 or (generation + 1) == 3 or (generation + 1) == 5 \
                    or (generation + 1) == 9 or (generation + 1) % 10 == 0:
                checkpoints.append(best_path.size())

        return best_path, checkpoints

    def run_parallel(self, path_specification):
        ant = Ant(self.environment, path_specification, self.convergence_iter, self.trail, self.step_size)
        return ant.find_path()
