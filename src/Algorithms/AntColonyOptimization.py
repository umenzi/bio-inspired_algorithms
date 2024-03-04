from Board.ACOBoard import ACOBoard
from Agent.Ant import Ant
from multiprocessing import Pool


class AntColonyOptimization:

    def __init__(self, maze: ACOBoard, ants_per_gen, generations, q, evaporation, convergence_iter, no_change_iter,
                 trail, sigma_elite, num_processes=6):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation
        self.convergence_iter = convergence_iter
        self.no_change_iter = no_change_iter
        self.trail = trail
        self.num_processes = num_processes
        self.sigma_elite = sigma_elite

    def find_shortest_route(self, path_specification):
        self.maze.reset()

        best_route = None
        count = 0
        checkpoints = []
        start = path_specification.get_start()
        end = path_specification.get_end()

        for generation in range(self.generations):
            print("Generation", generation)

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

            print("Routes found so far:", len(routes))
            if best_route is not None:
                print("Best route's length:", best_route.size())
            print("\n")

            if count >= self.no_change_iter:
                print("No change for many generations")
                return best_route

            if len(routes) == 0:
                continue

            self.maze.evaporate(self.evaporation)

            self.maze.add_pheromone_routes(routes, self.q)

            # Adding the pheromones of the best path using elitism
            for i in range(self.sigma_elite):
                self.maze.add_pheromone_route(best_route, self.q)

            if (generation + 1) == 1 or (generation + 1) == 3 or (generation + 1) == 5 \
                    or (generation + 1) == 9 or (generation + 1) % 10 == 0:
                checkpoints.append(best_route.size())

        return best_route, checkpoints

    def find_route_parallel(self, path_specification):
        ant = Ant(self.maze, path_specification, self.convergence_iter, self.trail)
        return ant.find_route()
