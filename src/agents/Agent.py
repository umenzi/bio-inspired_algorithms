class Agent:
    """
    Simple agent class, from where all the specific agents are implemented.
    """

    def __init__(self, environment, path_specification):
        """
        Constructor for the agent taking an environments and PathSpecification.

        :param environment: environments the ant will be running in.
        :param path_specification: The path specification consisting of a start coordinate and an end coordinate.
        """
        self.environment = environment
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
