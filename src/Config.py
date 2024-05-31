from dataclasses import dataclass, field, asdict
from typing import Union, Dict

from helpers.Coordinate import Coordinate


@dataclass
class EnvConfig:
    """
    Environment parameters
    """
    width = 40
    height = 40
    start_pos = Coordinate(2, 2)
    end_pos = Coordinate(38, 38)
    obstacle_distance = 5


@dataclass
class TrainConfig:
    """
    General config for training the algorithms
    """

    step_size = 1
    trail = 1.0
    convergence_iter = 4000


@dataclass
class AlgoConfig:
    """
    Abstract class to hold the specific hyperparameters for each algorithm
    """

    pass


@dataclass
class ACOConfig(AlgoConfig):
    aco_agents_per_generation = 30
    aco_no_generations = 20
    aco_q = 400
    aco_evaporation = 0.55
    aco_no_change_iter = 30
    aco_sigma_elite = 60


@dataclass
class PSOConfig(AlgoConfig):
    pso_num_iterations = 500  # To let Lévy flights get out of local optima eventually
    pso_inertia_weight = 0.87  # Currently irrelevant as adapted from acceleration coefficients, but given for completeness
    pso_num_particles = 100  # The number of particles generated initially to run pso on


@dataclass
class FireflyConfig(AlgoConfig):
    fa_population_size = 100
    fa_alpha_init = 0.87  # Є [0,1]
    fa_alpha_final = 0.36  # Є [0,1]
    fa_beta = 0.37  # Є [0,1]
    fa_gamma_init = 1.6  # it is suggested Є [0,10]
    fa_gamma_final = 7.8  # it is suggested Є [0,10]
    fa_max_iter = 100


@dataclass
class Config:
    ALGORITHMS = ["aco", "adpe_aco", "pso", "firefly"]

    env: EnvConfig = field(default_factory=EnvConfig)
    train_config: TrainConfig = field(default_factory=TrainConfig)
    algos: Dict[str, Union[ACOConfig, ACOConfig, PSOConfig, FireflyConfig]] = field(
        default_factory=lambda: {'aco': ACOConfig(), 'adpe_aco': ACOConfig(),
                                 'pso': PSOConfig(), 'firefly': FireflyConfig})

    num_experiments = 3

    def as_dict(self):
        return asdict(self)


CONFIG: Config = Config()
