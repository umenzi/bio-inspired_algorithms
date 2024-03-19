import enum


class Direction(enum.Enum):
    """
    Enum representing the directions an agent can take.

    Note that the Coordinate object can also move in any direction given an angle,
    but this includes the most common directions you could use.
    """
    right = 0
    up = 1
    left = 2
    down = 3
    # diagonals
    up_right = 4
    up_left = 5
    down_right = 6
    down_left = 7

    @classmethod
    def dir_to_int(cls, direction):
        """
        Direction to an int.
        :param direction: the direction.
        :return: an integer from 0-7.
        """
        return direction.value
