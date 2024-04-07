from helpers.Coordinate import Coordinate


class Obstacle:
    def __init__(self, center: Coordinate, radius: float):
        self.center = center
        self.radius = radius

    def get_center(self):
        return self.center

    def get_radius(self):
        return self.radius