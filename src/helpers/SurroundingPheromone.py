from helpers.Direction import Direction


class SurroundingPheromone:
    """
    Class containing the pheromone information around a certain point in the environment.
    """

    def __init__(self, up: int, up_right: int, right: int, down_right: int, down: int,
                 down_left: int, left: int, up_left: int):
        """
        Creates a surrounding pheromone object.

        :param up: The pheromone level in the up direction
        :param up_right: The pheromone level in the up-right direction
        :param right: The pheromone level in the right direction
        :param down_right: The pheromone level in the down-right direction
        :param down: The pheromone level in the down direction
        :param down_left: The pheromone level in the down-left direction
        :param left: The pheromone level in the left direction
        """

        self.up: int = up
        self.up_right: int = up_right
        self.right: int = right
        self.down_right: int = down_right
        self.down: int = down
        self.down_left: int = down_left
        self.left: int = left
        self.up_left: int = up_left
        self.total_surrounding_pheromone: int = right + up + down + left + up_right + down_right + down_left + up_left

    def get_total_surrounding_pheromone(self):
        """
        Get the total amount of surrounding pheromone.

        :return: Total surrounding pheromone
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
        elif direction == Direction.up_right:
            return self.up_right
        elif direction == Direction.down_right:
            return self.down_right
        elif direction == Direction.down_left:
            return self.down_left
        elif direction == Direction.up_left:
            return self.up_left
        else:
            return None
