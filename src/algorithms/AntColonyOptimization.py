from environments import ACOEnvironment
from agents.Ant import Ant
from multiprocessing import Pool


class AntColonyOptimization:
    """
    Ant Colony Optimization is an algorithm based on the exploratory behaviour of ants to find food.

    Agents in the algorithm act as ants and deposit pheromone on the paths they travel, which will be updated based
    on the quality of said path. In our case, this relates directly to the length of the route. Through this process,
    agents search for the optimal path through a graph or network.

    The ACO algorithm is put in use in optimization problems where the search space is large, and many solutions are
    possible, but not all are optimal. This includes the Travelling Salesman Problem. It has also been used to solve
    other problems such as resource allocation, machine learning, and data mining.
    """

    def __init__(self, environment: ACOEnvironment, ants_per_gen, generations, q, evaporation, convergence_iter,
                 no_change_iter, trail, sigma_elite, num_processes=6):
        self.environment = environment
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation
        self.convergence_iter = convergence_iter
        self.no_change_iter = no_change_iter
        self.trail = trail
        self.num_processes = num_processes
        self.sigma_elite = sigma_elite

    def find_shortest_route(self, path_specification, print_progress=True):
        """
        The ACO algorithm to find the shortest route across generations.

        We first reset the pheromones (i.e. initialize them), then we create a specified
        number of ants for each generation and keep track of the shortest path found amongst all of them.
        After each generation, we evaporate the existing pheromones by the chosen evaporation parameter
        ρ, and we add the pheromones of each of the routes found by the ants. This process is shown in
        the following pseudocode block.

        :param path_specification:
        :param print_progress: whether we print the result of each generation
        :return:
        """

        self.environment.reset()

        best_route = None
        count = 0
        checkpoints = []
        start = path_specification.get_start()
        end = path_specification.get_end()

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
                return best_route

            if len(routes) == 0:
                continue

            self.environment.evaporate(self.evaporation)

            self.environment.add_pheromone_routes(routes, self.q)

            # Performance Improvement: Adding the pheromones of the best path using elitism
            for i in range(self.sigma_elite):
                self.environment.add_pheromone_route(best_route, self.q)

            if (generation + 1) == 1 or (generation + 1) == 3 or (generation + 1) == 5 \
                    or (generation + 1) == 9 or (generation + 1) % 10 == 0:
                checkpoints.append(best_route.size())

        return best_route, checkpoints

    def find_route_parallel(self, path_specification):
        ant = Ant(self.environment, path_specification, self.convergence_iter, self.trail)
        return ant.find_route()
