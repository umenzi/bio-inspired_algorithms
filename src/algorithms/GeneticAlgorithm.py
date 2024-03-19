import random

import numpy as np


class GeneticAlgorithm:
    """
    TSP problem solver using genetic algorithms.
    """

    def __init__(self, generations, pop_size, mutation_prob=0.005, crossover_prob=0.7):
        """
        Constructs a new 'genetic algorithm' object.
        :param generations: the amount of generations.
        :param pop_size: the population size.
        :param mutation_prob: the probability of mutation.
        """

        self.generations = generations
        self.pop_size = pop_size
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob

    def solve_tsp(self, tsp_data):
        """
        This method should solve the TSP.
        :param tsp_data: the TSP data.
        :return: the optimized product sequence.
        """

        # STEP 1: Creating the initial population.

        population_set = self.generate(tsp_data.product_locations, self.pop_size)

        # This contains the population (index 0) with the best fitness (index 1) so far
        best_solution = [np.array([]), -1]

        for i in range(self.generations):

            # STEP 2: Evaluating fitness for each solution (= chromosome).

            fitness_list = []
            pop_fit_list = []

            for population in population_set:
                fitness_list.append(self.assess_fitness(population, tsp_data))
                pop_fit_list.append((population, fitness_list[-1]))

            # Obtain fitness ratio
            fitness_ratio_list = self.fitness_ratio(population_set, fitness_list)

            # Update if necessary the best solution found so far
            cur_max = max(pop_fit_list, key=lambda x: x[1])

            if best_solution[1] < cur_max[1]:
                best_solution = cur_max

            # STEP 3: Generate the new population after selecting, doing crossover and mutation.
            population_set = self.select(population_set, fitness_ratio_list)

        # print("Path length is:", 1 / best_solution[1])

        return best_solution[0]

    def generate(self, products, pop_size):
        """
        This method generates an initial population.
        Each gene will represent the product number.
        Chromosomes describe the order of products which the robot will visit.

        :param products: the items in the store.
        :param pop_size: the size of the population.
        :return: the generated set of sequences to get all items.
        """

        population = []

        for i in range(pop_size):
            chromosome = list(range(len(products)))
            random.shuffle(chromosome)
            population.append(chromosome)
            # population.append(random.sample(products, len(products)))

        return population

    def assess_fitness(self, product_order, tsp_data):
        """
        Calculates the fitness function, which is 1 / d_path, where d_path is the total length
        of the path travelled by the robot to get all the products in the specified order of
        the permuted chromosome.

        :param product_order:
        :param tsp_data:
        :return:
        """

        distance_matrix = tsp_data.get_distances()
        start_distances = tsp_data.get_start_distances()
        end_distances = tsp_data.get_end_distances()

        fitness = start_distances[product_order[0]]

        for i in range(len(product_order) - 1):
            fitness += distance_matrix[product_order[i]][product_order[i + 1]]

        fitness += end_distances[product_order[len(product_order) - 1]] + len(product_order)

        return 1 / fitness

    def fitness_ratio(self, population_set, fitness_list):
        """
        Computes the fitness ratio, so we turn the fitness into a probability.

        :param population_set: The population on which we compute the fitness ratio.
        :param fitness_list: Fitness functions to be turned into probabilities.
        :return: Set of fitness ratios of the given population.
        """

        fitness_ratio_list = []

        sum_of_fitness = np.sum(fitness_list)

        for i in range(len(fitness_list)):
            fitness_ratio_list.append((population_set[i], 100 * (fitness_list[i] / sum_of_fitness)))

        return fitness_ratio_list

    def select(self, population, fitness_ratio_list):
        """
        To create the next generation, we use elitism, to ensure that the fittest solutions are not lost due
        to randomness. This means that we take the top 33.3% of the current population as our elite set, we take
        2 elements of the elite set to go to the next generation without change, and then to fill the rest with
        the next generation, we take one parent from the elite set and one parent from the whole population set.

        Elitism can also harm the genetic algorithm, as it lowers the possibility of finding new
        individuals that provide more optimal solutions. This is why we only pass 2 elements of the elite set.

        Implementation based on https://www.baeldung.com/cs/elitism-in-evolutionary-algorithms
        :param population: the population from which we obtain the next generation.
        :param fitness_ratio_list:
        :return:
        """

        # Pick the elite set
        fitness_ratio_list.sort(reverse=True, key=lambda x: x[1])
        elite_list = [path for path, fitness_ratio in fitness_ratio_list[:len(population) // 3]]

        # Pick 2 elements from the elite set to go to the new population without any changes
        new_pop = elite_list[:2].copy()

        # For the remaining, we use genetic operations with one of the parents being from the elite set,
        # which is roughly a third of the population, and the other parent being any chromosome in the
        # current generation (including the ones from the elite set)
        while len(new_pop) < len(population):
            parent1 = random.sample(elite_list, 1)[0]
            parent2 = random.sample(population, 1)[0]

            # Perform crossover to create child
            if random.random() <= self.crossover_prob:
                child = self.crossover(parent1, parent2)
            else:
                child = random.choice([parent1, parent2])

            # Perform mutation on child with probability mutation_prob
            if random.random() <= self.mutation_prob:
                self.mutate(child)

            # Add child to next generation
            new_pop.append(child)

        return new_pop

    def crossover(self, parent1, parent2):
        """
        We create a child chromosome by picking a random splitting point for the parent chromosomes, and taking
        the left part of the first parent and the right part of the second parent.
        We also perform “Order Crossover”: we make sure that the child chromosome has all the product locations,
        and does not contain any duplicate location.
        The child inherits from both parents, which may form a better solution than the parents alone.
        :param parent1: One of the parent chromosomes.
        :param parent2: The other parent chromosome.
        :return: A child chromosome.
        """

        # Order crossover:

        gene_a = int(len(parent1) * random.random())
        gene_b = int(len(parent2) * random.random())

        start_gene = min(gene_a, gene_b)
        final_gene = max(gene_a, gene_b)

        child = []

        child_p1 = []

        for i in range(start_gene, final_gene):
            child_p1.append(parent1[i])

        child_p2 = [item for item in parent2 if item not in child_p1]

        for i in range(start_gene):
            child.append(child_p2[i])

        child.extend(child_p1)

        for i in range(start_gene, len(child_p2)):
            child.append(child_p2[i])

        return child

        # One point crossover

        # crossover_point = random.randint(0, len(parent1) - 1)
        # child = parent1[:crossover_point] + parent2[crossover_point:]
        #
        # child = list(set(child))
        #
        # for loc1 in parent2:
        #     if loc1 not in child:
        #         child.append(loc1)
        #
        # return child

    def mutate(self, child):
        """
        Since our problem is an ordering problem, we use Swap Mutation. We select two positions of
        the chromosome at random, and we swap them.

        Mutation is very important, because it prevents the algorithm to get stuck in a local optimum.
        We only apply mutation with a low probability (we chose 0.01), because we want to avoid the
        chromosomes being inconsistent.

        :param child: The chromosome we will mutate.
        :return: The mutated chromosome.
        """

        pos1, pos2 = random.sample(range(len(child)), 2)

        child[pos1], child[pos2] = child[pos2], child[pos1]

        return child
