from typing import Any

import optuna
import pandas as pd
from numpy.random import PCG64

from Config import CONFIG
from algorithms.AdpeAntColonyOptimization import AdpeAntColonyOptimization
from algorithms.AntColonyOptimization import AntColonyOptimization
from algorithms.FireflyAlgorithm import FireflyAlgorithm
from algorithms.ParticleSwarmOptimization import ParticleSwarmOptimization
from environments.ACOEnvironment import ACOEnvironment
from environments.Environment import Environment
from helpers.PathSpecification import PathSpecification


def objective(trial: optuna.Trial, obstacle_percentages, n_envs, algo):
    """
    Objective function for the hyperparameter tuning

    :param trial: The optuna trial
    :param obstacle_percentages: percentage of obstacles in the environment
    :param n_envs: number of environments to run
    :param algo: algorithm to tune

    :return: The size of the shortest path (i.e. the objective function to minimize)
    """

    # random seed
    seed = PCG64()

    new_size = 0

    for i in range(n_envs):
        # Create a new environment and path specification
        environment = (
            Environment.create_environment(CONFIG.env.width, CONFIG.env.height,
                                           obstacle_values=obstacle_percentages, start_pos=CONFIG.env.start_pos,
                                           end_pos=CONFIG.env.end_pos, seed=seed))
        spec = PathSpecification(CONFIG.env.start_pos, CONFIG.env.end_pos)

        # Select the correct algorithm
        if algo == "aco":
            aco_environment = ACOEnvironment.create_from_environment(environment)
            algo = AntColonyOptimization(aco_environment,
                                         CONFIG.algos["aco"].aco_agents_per_generation,
                                         CONFIG.algos["aco"].aco_no_generations,
                                         q=trial.suggest_int("q", 100, 1000),
                                         evaporation=trial.suggest_float("evaporation", 0.1, 0.9),
                                         convergence_iter=CONFIG.train_config.convergence_iter,
                                         no_change_iter=CONFIG.algos["aco"].aco_no_change_iter,
                                         trail=trial.suggest_float("trail", 0.1, 1.0),
                                         step_size=CONFIG.train_config.step_size,
                                         num_processes=6)
        elif algo == "adpe_aco":
            aco_environment = ACOEnvironment.create_from_environment(environment)
            algo = AdpeAntColonyOptimization(aco_environment,
                                             CONFIG.algos["aco"].aco_agents_per_generation,
                                             CONFIG.algos["aco"].aco_no_generations,
                                             q=trial.suggest_int("q", 100, 1000),
                                             evaporation=trial.suggest_float("evaporation", 0.1, 0.9),
                                             convergence_iter=CONFIG.train_config.convergence_iter,
                                             sigma_elite=trial.suggest_int("sigma_elite", 10, 100),
                                             no_change_iter=CONFIG.algos["aco"].aco_no_change_iter,
                                             trail=trial.suggest_float("trail", 0.1, 1.0),
                                             step_size=CONFIG.train_config.step_size,
                                             num_processes=6)
        elif algo == "pso":
            algo = ParticleSwarmOptimization(environment,
                                             num_particles=CONFIG.algos["pso"].pso_num_particles,
                                             convergence_iter=trial.suggest_int("convergence_iter", 100, 5000),
                                             trail=trial.suggest_float("trail", 0.1, 1.0),
                                             step_size=CONFIG.train_config.step_size,
                                             inertia_weight=trial.suggest_float("inertia_weight", 0.1, 1.0),
                                             max_iter=CONFIG.train_config.convergence_iter)
        elif algo == "firefly":
            algo = FireflyAlgorithm(environment,
                                    population_size=CONFIG.algos["firefly"].fa_population_size,
                                    alpha_init=trial.suggest_float("alpha_init", 0.0, 1.0),
                                    alpha_end=trial.suggest_float("alpha_final", 0.0, 1.0),
                                    gamma_init=trial.suggest_float("gamma_init", 0.0, 10.0),
                                    gamma_end=trial.suggest_float("gamma_end", 0.0, 10.0),
                                    beta=trial.suggest_float("beta", 0.0, 1.0),
                                    max_iter=CONFIG.train_config.convergence_iter,
                                    step_size=CONFIG.train_config.step_size)
        else:
            raise ValueError("Invalid algorithm")

        # Obtain the shortest path length
        shortest_path, checkpoints = algo.run(spec, print_progress=False)
        new_size = shortest_path.size()

        trial.report(shortest_path.size(), i)

        # Handle pruning based on the intermediate value.
        if trial.should_prune():
            raise optuna.exceptions.TrialPruned()

    return new_size


def tune(obstacle_percentages, n_envs, algo, n_trials=100, verbose: int = 0) -> dict[str, Any]:
    study = optuna.create_study(direction="minimize")

    study.optimize(lambda trial: objective(trial, obstacle_percentages, n_envs, algo), n_trials=n_trials)

    pruned_trials = [t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED]
    complete_trials = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]

    if verbose >= 1:
        print("Study statistics: ")
        print("  Number of finished trials: ", len(study.trials))
        print("  Number of pruned trials: ", len(pruned_trials))
        print("  Number of complete trials: ", len(complete_trials))

        print("Best trial:")
        trial = study.best_trial

        print("  Value: ", trial.value)

        print("  Params: ")
        for key, value in trial.params.items():
            print("    {}: {}".format(key, value))
    return study.best_params


if '__main__' == __name__:
    obstacle_percentages = [(2.5, 0.2), (1.5, 0.08)]
    n_envs = 5
    best_params = {}

    for algo in CONFIG.ALGORITHMS:
        best_params.update(tune(obstacle_percentages, n_envs, algo, n_trials=100, verbose=0))

    print(best_params)
