import enum


class Direction(enum.Enum):
    """
    Enum representing the directions an ant can take.
    """
    east = 0
    north = 1
    west = 2
    south = 3

    @classmethod
    def dir_to_int(cls, direction):
        """
        Direction to an int.
        :param direction: the direction.
        :return: an integer from 0-3.
        """
        return direction.value
