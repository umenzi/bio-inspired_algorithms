import enum


class Direction(enum.Enum):
    """
    Enum representing the directions an agent can take, in clockwise order.

    Note that the Coordinate object can also move in any direction given an angle,
    but this includes the most common directions you could use.
    Recommended when you want to move in a grid or graph-like structure.
    """
    up = 0
    up_right = 1
    right = 2
    down_right = 3
    down = 4
    down_left = 5
    left = 6
    up_left = 7

    @classmethod
    def dir_to_int(cls, direction):
        """
        Direction to an int.

        :param direction: The direction.
        :return: An integer from 0-7.
        """
        return direction.value
