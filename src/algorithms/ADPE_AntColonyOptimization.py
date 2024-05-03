import random

from environments import ACOEnvironment
from agents.Ant import Ant
from multiprocessing import Pool

from helpers.Route import Route


class ADPE_AntColonyOptimization:
    """
    Ant Colony Optimization is an algorithm based on the exploratory behaviour of ants to find food.

    This is Adaptive Dynamic Probabilistic Elitism (ADPE) Ant Colony Optimization, an extension of the original ACO
    algorithm.
    It introduces Probabilistic Elitism, where the pheromones of the best path are added with a certain
    probability.
    This reduces the chance of the algorithm getting stuck in a local minimum with respect to the original
    algorithm.
    """

    def __init__(self, environment: ACOEnvironment, ants_per_gen: int, generations: int, q: int,
                 evaporation: float, convergence_iter: int, no_change_iter: int, trail: float, sigma_elite: int,
                 default_elitist_probability: float = 0.5, step_size: int = 1, num_processes: int = 6):
        self.environment: ACOEnvironment = environment
        self.ants_per_gen: int = ants_per_gen
        self.generations: int = generations
        self.q: int = q
        self.evaporation: float = evaporation
        self.convergence_iter: int = convergence_iter
        self.no_change_iter: int = no_change_iter
        self.trail: float = trail
        self.step_size: int = step_size
        self.num_processes: int = num_processes
        self.sigma_elite: int = sigma_elite
        self.default_elitist_probability: float = default_elitist_probability
        self.maximum_global_tour_length = None

    def find_shortest_route(self, path_specification, print_progress=True):
        """
        The ACO algorithm to find the shortest route across generations.

        We first reset the pheromones (i.e. initialize them), then we create a specified
        number of ants for each generation and keep track of the shortest path found amongst all of them.
        After each generation, we evaporate the existing pheromones by the chosen evaporation parameter
        ρ, and we add the pheromones of each route found by the ants.
        This process is shown in the following pseudocode block.

        :param path_specification: The start and end coordinates of the path
        :param print_progress: Whether we print the result of each generation
        :return: The best route found
        """

        self.environment.reset()

        best_route: Route = None
        count = 0
        checkpoints = []

        for generation in range(self.generations):
            if print_progress:
                print("Generation", generation)

            # We introduce multi-threading
            # Basically, each ant compute their shortest path on a separate thread
            # This way, more ants are deployed to find routes (hence, the better our algorithm will be)
            with Pool(self.num_processes) as p:
                routes = p.map(self.find_route_parallel, [path_specification] * self.ants_per_gen)

            routes = [r for r in routes if r is not None]

            prev = best_route

            for route in routes:
                if best_route is None:
                    best_route = route
                if route.shorter_than(best_route):
                    best_route = route

            # We get the longest route for the probabilistic Elitism
            if self.maximum_global_tour_length is None:
                self.maximum_global_tour_length = best_route.size()

            if best_route is not None and prev is not None and prev == best_route:
                count += 1
            else:
                count = 0

            if print_progress:
                print("Routes found so far:", len(routes))
                if best_route is not None:
                    print("Best route's length:", best_route.size())
                print("\n")

            if count >= self.no_change_iter:
                if print_progress:
                    print("No change for many generations")
                return best_route, checkpoints

            if len(routes) == 0:
                continue

            self.environment.evaporate(self.evaporation)

            self.environment.add_pheromone_routes(routes, self.q)

            # Performance Improvement: Adding the pheromones of the best path using elitism
            # We use Probabilistic Elitism, where we add the pheromones of the best path with a certain probability
            # This reduces the chance of the algorithm getting stuck in a
            # local minimum with respect to the original elitist algorithm
            p: float = 1 - best_route.size() / self.maximum_global_tour_length
            if p < 0:
                p = self.default_elitist_probability

            if random.random() < p:
                for i in range(self.sigma_elite):
                    self.environment.add_pheromone_route(best_route, self.q)

            if (generation + 1) == 1 or (generation + 1) == 3 or (generation + 1) == 5 \
                    or (generation + 1) == 9 or (generation + 1) % 10 == 0:
                checkpoints.append(best_route.size())

        return best_route, checkpoints

    def find_route_parallel(self, path_specification):
        ant = Ant(self.environment, path_specification, self.convergence_iter, self.trail, self.step_size)
        return ant.find_route()
