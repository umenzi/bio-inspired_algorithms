from helpers.Direction import Direction


class SurroundingPheromone:
    """
    Class containing the pheromone information around a certain point in the environment.
    """

    def __init__(self, up: int, right: int, down: int, left: int):
        """
        Creates a surrounding pheromone object.

        :param up: the amount of pheromone upwards.
        :param right: the amount of pheromone to the right.
        :param down: the amount of pheromone downwards.
        :param left: the amount of pheromone to the left.
        """

        self.up: int = up
        self.down: int = down
        self.left: int = left
        self.right: int = right
        self.total_surrounding_pheromone: int = right + up + down + left

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

        if direction == Direction.up:
            return self.up
        elif direction == Direction.right:
            return self.right
        elif direction == Direction.left:
            return self.left
        elif direction == Direction.down:
            return self.down
        else:
            return None
