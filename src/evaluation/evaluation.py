import pandas as pd
import numpy as np

from Config import CONFIG
from algorithms.AdpeAntColonyOptimization import AdpeAntColonyOptimization
from algorithms.Algorithm import Algorithm
from algorithms.AntColonyOptimization import AntColonyOptimization
from algorithms.FireflyAlgorithm import FireflyAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimization
from environments.ACOEnvironment import ACOEnvironment
from environments.Environment import Environment
from helpers.PathSpecification import PathSpecification


def obtain_algo(algo_id, environment) -> Algorithm:
    """
    Returns the algorithm object based on the algo_id

    :param algo_id: The algorithm id
    :param environment: The environment object

    :return: The algorithm object
    """

    if algo_id == "aco":
        return AntColonyOptimization(environment, CONFIG.algos["aco"].aco_agents_per_generation,
                                     CONFIG.algos["aco"].aco_no_generations, CONFIG.algos["aco"].aco_q,
                                     CONFIG.algos["aco"].aco_evaporation, CONFIG.train_config.convergence_iter,
                                     CONFIG.algos["aco"].aco_no_change_iter,
                                     CONFIG.train_config.trail,
                                     CONFIG.train_config.step_size,
                                     obstacle_distance=CONFIG.env.obstacle_distance)
    elif algo_id == "adpe_aco":
        return AdpeAntColonyOptimization(environment, CONFIG.algos["aco"].aco_agents_per_generation,
                                         CONFIG.algos["aco"].aco_no_generations, CONFIG.algos["aco"].aco_q,
                                         CONFIG.algos["aco"].aco_evaporation, CONFIG.train_config.convergence_iter,
                                         CONFIG.algos["aco"].aco_no_change_iter,
                                         CONFIG.train_config.trail,
                                         CONFIG.train_config.step_size,
                                         obstacle_distance=CONFIG.env.obstacle_distance,
                                         default_elitist_probability=CONFIG.algos["aco"].aco_sigma_elite)
    elif algo_id == "pso":
        return ParticleSwarmOptimization(environment, CONFIG.algos["pso"].pso_num_particles,
                                         CONFIG.train_config.convergence_iter, CONFIG.train_config.trail,
                                         CONFIG.train_config.step_size, CONFIG.algos["pso"].pso_inertia_weight,
                                         CONFIG.algos["pso"].pso_num_iterations,
                                         obstacle_distance=CONFIG.env.obstacle_distance)
    elif algo_id == "firefly":
        return FireflyAlgorithm(environment, CONFIG.algos["firefly"].fa_population_size,
                                CONFIG.algos["firefly"].fa_alpha_init, CONFIG.algos["firefly"].fa_alpha_final,
                                CONFIG.algos["firefly"].fa_gamma_init, CONFIG.algos["firefly"].fa_gamma_final,
                                CONFIG.algos["firefly"].fa_beta, CONFIG.algos["firefly"].fa_max_iter,
                                CONFIG.train_config.step_size,
                                obstacle_distance=CONFIG.env.obstacle_distance)
    else:
        raise ValueError("Invalid algo_id")


def evaluate(obstacle_percentages):
    """
    Evaluates the algorithms for the given obstacle percentages

    :param obstacle_percentages: The obstacle percentages

    :return: The results dataframe.
    The columns are the algorithms and the rows are the obstacle percentages.
    """

    # Initialize the results' dictionary
    results = {}

    # Loop over the algorithms
    for algo_id in CONFIG.ALGORITHMS:
        # Initialize the list of path lengths for the current algorithm
        path_lengths = []

        # Loop over the obstacle percentages
        for obstacle_percentage in obstacle_percentages:
            # Initialize the list of path lengths for the current obstacle percentage
            obstacle_path_lengths = []

            # Run the algorithm 20 times for the current obstacle percentage
            for _ in range(20):
                # Create the environment
                environment = Environment(
                    CONFIG.env.width, CONFIG.env.height, obstacles=obstacle_percentage,
                    start=CONFIG.env.start_pos, end=CONFIG.env.end_pos)
                if algo_id == "aco":
                    environment = ACOEnvironment.create_from_environment(environment)

                path_specification = PathSpecification(CONFIG.env.start_pos, CONFIG.env.end_pos)

                algo: Algorithm = obtain_algo(algo_id, environment)

                # Run the algorithm
                path, checkpoints = algo.run(path_specification, print_progress=False)

                # Append the path length to the list of path lengths for the current obstacle percentage
                obstacle_path_lengths.append(len(path))

            # Calculate the average path length for the current obstacle percentage
            average_path_length = np.mean(obstacle_path_lengths)

            # Append the average path length to the list of path lengths for the current algorithm
            path_lengths.append(average_path_length)

        # Add the list of path lengths for the current algorithm to the results' dictionary
        results[algo_id] = path_lengths

        # Convert the results' dictionary to a pandas DataFrame and print it
        df = pd.DataFrame(results, index=[str(op) for op in obstacle_percentages])

        return df


if '__main__' == __name__:
    # Set the obstacle percentages
    obstacle_percentages = [[(2.5, 0.15), (1.5, 0.018)],
                            [(2.5, 0.175), (1.5, 0.05)],
                            [(2.5, 0.2), (1.5, 0.08)]]

    # Evaluate the algorithms
    results = evaluate(obstacle_percentages)

    # Print the results
    print(results)
