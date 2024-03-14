from helpers.Direction import Direction


class SurroundingPheromone:
    """
    Class containing the pheromone information around a certain point in the environment.
    """

    def __init__(self, north: int, east: int, south: int, west: int):
        """
        Creates a surrounding pheromone object.

        :param north: the amount of pheromone in the north.
        :param east: the amount of pheromone in the east.
        :param south: the amount of pheromone in the south.
        :param west: the amount of pheromone in the west.
        """

        self.north: int = north
        self.south: int = south
        self.west: int = west
        self.east: int = east
        self.total_surrounding_pheromone: int = east + north + south + west

    def get_total_surrounding_pheromone(self):
        """
        Get the total amount of surrounding pheromone.

        :return: total surrounding pheromone
        """

        return self.total_surrounding_pheromone

    def get(self, direction: Direction):
        """
        Get a specific pheromone level.
        
        :param direction: Direction of pheromone.
        :return: Pheromone of dir.
        """

        if direction == Direction.north:
            return self.north
        elif direction == Direction.east:
            return self.east
        elif direction == Direction.west:
            return self.west
        elif direction == Direction.south:
            return self.south
        else:
            return None
