# Bio-Inspired Navigation for MultiAgent Systems in Extreme Environments

This repository presents a modular,
easy-to-use framework for the simulation and analysis of Bio-Inspired algorithms for
the navigation of multi-agent systems in extreme environments.

## Getting started

There are multiple components in this project, each with its own default implementation:

- The default environment, `Environment.py`, is a 2D grid with obstacles and a starting and final position.
  - Special relevance for the  `visualize_environment` method, which plots the environment and the route found by the
    algorithm, if any.
    - The user can generate as many types of obstacles as desired
      by providing an array of the obstacles' radius and their frequencies. 
      The obstacles are then generated randomly in the inner 80% of the environment.
- The agents, `Agent.py`, are able to move in the four cardinal directions.
- The algorithms are stored in the `algorithms` folder.
- Additional helper classes, such as `Coordinate.py` or `Direction.py`, are also provided in the `helpers` folder.


### Swarm algorithms

The following are the algorithms currently implemented:
- Particle Swarm Optimization (PSO).
- Ant Colony Optimization (ACO).
- Adaptive dynamic probabilistic elitist ACO (ADPE ACO) [2].
- Adaptive Firefly Algorithm (AFFA) [1].
- Gaussian Firefly Algorithm.

When adding new algorithms, make sure to extend each of these classes with your own implementation.
You may also need to extend the default environment, as in the case of the ACO algorithm.
PSO, for example, does not require any changes.

A detailed example of several Bio-Inspired algorithms is given in `Main.ipynb`.

# References

[1] Chang Liu, Yuxin Zhao, Feng Gao, Liqiang Liu, "Three-Dimensional Path Planning Method for Autonomous Underwater
Vehicle Based on Modified Firefly Algorithm", Mathematical Problems in Engineering, vol. 2015, Article ID 561394, 
10 pages, 2015. https://doi.org/10.1155/2015/561394

[2] Chatterjee, A., Kim, E. & Reza, H. Adaptive Dynamic Probabilistic Elitist Ant Colony Optimization in Traveling 
Salesman Problem. SN COMPUT. SCI. 1, 95 (2020). https://doi.org/10.1007/s42979-020-0083-z
