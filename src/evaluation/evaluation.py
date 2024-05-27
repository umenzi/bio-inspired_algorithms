import time

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


def evaluate(obstacle_percentages, n_envs, trials, verbose=0):
    """
    Evaluates the algorithms for the given obstacle percentages

    :param obstacle_percentages: The obstacle percentages
    :param n_envs: The number of environments per obstacle percentage
    :param trials: The number of trials per environment
    :param verbose: The verbosity level

    :return: The results dataframe.
    The columns are the algorithms and the rows are the obstacle percentages.
    """

    # Initialize the results' dictionary
    results = {}

    # Loop over the algorithms
    for algo_id in CONFIG.ALGORITHMS:
        # Initialize the list of path lengths for the current algorithm
        path_lengths = []

        if verbose >= 1:
            print(f"Evaluating {algo_id}...")

        # Loop over the obstacle percentages
        for obstacle_percentage in obstacle_percentages:
            # Initialize the list of metric values for the current obstacle percentage
            metric_values = {"path_length": [], "time": [], "reachability": []}

            if verbose >= 1:
                print(f"For the obstacle percentage: {obstacle_percentage}")

            # We generate n_envs environments
            for i in range(n_envs):
                # Create the environment
                environment = Environment.create_environment(CONFIG.env.width, CONFIG.env.height,
                                                             obstacle_percentage, start_pos=CONFIG.env.start_pos,
                                                             end_pos=CONFIG.env.end_pos)
                if algo_id == "aco":
                    environment = ACOEnvironment.create_from_environment(environment)

                path_specification = PathSpecification(CONFIG.env.start_pos, CONFIG.env.end_pos)

                algo: Algorithm = obtain_algo(algo_id, environment)

                # Run the algorithm trials times for the current obstacle percentage
                for _ in range(trials):
                    # Start timer
                    start_time = time.time()

                    # Run the algorithm
                    path, checkpoints = algo.run(path_specification, print_progress=False)

                    # Stop the timer and calculate the elapsed time
                    runtime = time.time() - start_time

                    reached = path.get_path()[-1] == path_specification.end

                    if reached:
                        metric_values["path_length"].append(path.size())

                    metric_values["reachability"].append(reached)
                    metric_values["time"].append(runtime)

                if verbose >= 1:
                    print(f"Environment {i + 1} done...")

            for metric, values in metric_values.items():
                # Calculate the mean and standard deviation of the metric values
                mean = np.mean(values)
                std = np.std(values)

                key = (str(obstacle_percentage), metric)

                if key not in results:
                    results[key] = {}

                # Add the mean and standard deviation to the results' dictionary
                results[key][algo_id] = (mean, std)

    # Convert the results' dictionary to a pandas DataFrame and print it
    df = pd.DataFrame(results)

    return df


if '__main__' == __name__:
    # Set the obstacle percentages
    obstacle_percentages = [[(2.5, 0.15), (1.5, 0.018)],
                            [(2.5, 0.175), (1.5, 0.05)],
                            [(2.5, 0.2), (1.5, 0.08)]]

    n_envs = 4  # We generate 4 environments per obstacle percentage
    trials = 20  # We run each algorithm 20 times per environment
    verbose = 1

    # Evaluate the algorithms
    results = evaluate(obstacle_percentages, n_envs, trials, verbose=verbose)

    if verbose >= 1:
        # Print the results
        print(results)

    results.to_csv("results.csv", index=False)
