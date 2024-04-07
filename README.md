# Bio-Inspired Navigation for MultiAgent Systems in Extreme Environments

This repository contains several implementations of Bio-Inspired algorithms, such as PCO or ACO, 
for the navigation of multi-agent systems in extreme environments. 

The main goal of this project is to provide a set of tools to simulate and analyze the behavior of a group of agents in 
a given environment. 

Hence, the design of the system is highly modular, allowing for easy extension and modification of the algorithms and environments.

## Getting started

There are multiple components in this project, each with its own default implementation:

- The default environment, `Environment.py`, is a 2D grid with obstacles and a starting and final position.
  - Special relevance for the  `visualize_environment` method, which plots the environment and the route found by the
    algorithm, if any.
- The agents, `Agent.py`, are able to move in the four cardinal directions.
- The algorithms, are stored in the `algorithms` folder.
- Additional helper classes, such as `Coordinate.py` or `Direction.py`, are also provided in the `helpers` folder.


### Swarm algorithms

The following are the algorithms currently implemented:
- Particle Swarm Optimization (PSO).
- Ant Colony Optimization (ACO). Specifically, an adaptive dynamic probabilistic elitist ACO (ADPE ACO) has been implemented [1].


When adding new algorithms, make sure to extend each of these classes with your own implementation.

A detailed example of the usage of several Bio-Inspired algorithms, such as ACO or the Genetic algorithm, are given in
`Main.ipynb`.


## The environment

The environment framework allows both for discrete and continuous spaces.
For example, ACO uses a discrete space, while PSO uses a continuous space.

The user can generate as many types of obstacles as desired, by providing an array of the obstacles radius and their frequencies.
The obstacles are then generated randomly in the inner 80% of the environment.

# References

[1] Chatterjee, A., Kim, E. & Reza, H. Adaptive Dynamic Probabilistic Elitist Ant Colony Optimization in Traveling 
Salesman Problem. SN COMPUT. SCI. 1, 95 (2020). https://doi.org/10.1007/s42979-020-0083-z
