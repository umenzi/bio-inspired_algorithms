import pickle
import re
import sys
import traceback

from helpers.Coordinate import Coordinate
from helpers.PathSpecification import PathSpecification


class TSPData:
    """
    Class containing the product distances. Can be either build from an environment, a product
    location list and a PathSpecification or be reloaded from a file.
    """

    def __init__(self, product_locations, spec):
        """
        Constructs a new TSP data object.
        :param product_locations: the product locations.
        :param spec: the path specification.
        """

        self.product_locations = product_locations
        self.spec = spec

        self.distances = None
        self.start_distances = None
        self.end_distances = None
        self.product_to_product = None
        self.start_to_product = None
        self.product_to_end = None

    def calculate_routes(self, aco):
        """
        Calculate the routes from the product locations to each other, the start, and the end.

        Additionally generate arrays that contain the length of all the routes.
        :param aco: The ACO environments
        """

        self.product_to_product = self.build_distance_matrix(aco)
        self.start_to_product = self.build_start_to_products(aco)
        self.product_to_end = self.build_products_to_end(aco)
        self.build_distance_lists()
        return

    # Build
    def build_distance_lists(self):
        """
        :return: a list of integer distances of all the product-product routes.
        """

        number_of_products = len(self.product_locations)
        self.distances = []
        self.start_distances = []
        self.end_distances = []

        for i in range(number_of_products):
            self.distances.append([])
            for j in range(number_of_products):
                self.distances[i].append(self.product_to_product[i][j].size())
            self.start_distances.append(self.start_to_product[i].size())
            self.end_distances.append(self.product_to_end[i].size())
        return

    def get_distances(self):
        """
        Distance product to product getter
        :return: the list
        """

        return self.distances

    def get_start_distances(self):
        """
        Distance start to product getter
        :return: the list
        """

        return self.start_distances

    def get_end_distances(self):
        """
        Distance product to end getter
        :return: the list
        """

        return self.end_distances

    def __eq__(self, other):
        """
        Equals method
        :param other: the other TSPData to check
        :return: boolean (whether equal)
        """

        return self.distances == other.distances \
            and self.product_to_product == other.product_to_product \
            and self.product_to_end == other.product_to_end \
            and self.start_to_product == other.start_to_product \
            and self.spec == other.spec \
            and self.product_locations == other.product_locations

    def write_to_file(self, file_path):
        """
        Persist object to file so that it can be reused later
        :param file_path:  Path to persist to
        """
        pickle.dump(self, open(file_path, "wb"))

    def write_action_file(self, product_order, file_path):
        """
        Write away an action file based on a solution from the TSP problem.
        :param product_order: Solution of the TSP problem
        :param file_path: Path to the solution file
        """

        total_length = self.start_distances[product_order[0]]
        for i in range(len(product_order) - 1):
            frm = product_order[i]
            to = product_order[i + 1]
            total_length += self.distances[frm][to]

        total_length += self.end_distances[product_order[len(product_order) - 1]] + len(product_order)

        string = ""
        string += str(total_length)
        string += ";\n"
        string += str(self.spec.get_start())
        string += ";\n"
        string += str(self.start_to_product[product_order[0]])
        string += "take product #"
        string += str(product_order[0] + 1)
        string += ";\n"

        for i in range(len(product_order) - 1):
            frm = product_order[i]
            to = product_order[i + 1]
            string += str(self.product_to_product[frm][to])
            string += "take product #"
            string += str(to + 1)
            string += ";\n"
        string += str(self.product_to_end[product_order[len(product_order) - 1]])

        f = open(file_path, "w")
        f.write(string)

    def build_distance_matrix(self, aco):
        """
        Calculate the optimal routes between all the individual routes
        :param aco: ACO environments to calculate optimal routes in
        :return: Optimal routes between all products in 2d array
        """

        number_of_product = len(self.product_locations)
        product_to_product = []
        for i in range(number_of_product):
            product_to_product.append([])
            for j in range(number_of_product):
                start = self.product_locations[i]
                end = self.product_locations[j]
                shortest_route, checkpoints = aco.find_shortest_route(PathSpecification(start, end))
                product_to_product[i].append(shortest_route)
                print("Route between product", i, "and", j)

        return product_to_product

    def build_start_to_products(self, aco):
        """
        Calculate optimal route between the start and all the products
        :param aco: ACO environments to calculate optimal routes in
        :return: Optimal route from start to products
        """

        start = self.spec.get_start()
        start_to_products = []
        for i in range(len(self.product_locations)):
            shortest_route, checkpoints = aco.find_shortest_route(PathSpecification(start, self.product_locations[i]))
            start_to_products.append(shortest_route)
        return start_to_products

    def build_products_to_end(self, aco):
        """
        Calculate optimal routes between the products and the end point
        :param aco: The ACO environments to calculate optimal routes in
        :return: Optimal route from products to end
        """

        end = self.spec.get_end()
        products_to_end = []
        for i in range(len(self.product_locations)):
            shortest_route, checkpoints = aco.find_shortest_route(PathSpecification(self.product_locations[i], end))
            products_to_end.append(shortest_route)
        return products_to_end

    @staticmethod
    def read_from_file(file_path):
        """
        Load TSP data from a file
        :param file_path: Persist file
        :return: TSPData object from the file
        """

        return pickle.load(open(file_path, "rb"))

    @staticmethod
    def read_specification(coordinates, product_file):
        """
        Read a TSP problem specification based on a coordinate file and a product file
        :param coordinates: Path to the coordinate file
        :param product_file: Path to the product file
        :return TSP object with uninitialized routes
        """

        try:
            f = open(product_file, "r")
            lines = f.read().splitlines()

            first_line = re.compile("[:,;]\\s*").split(lines[0])
            product_locations = []
            number_of_products = int(first_line[0])
            for i in range(number_of_products):
                line = re.compile("[:,;]\\s*").split(lines[i + 1])
                product = int(line[0])
                x = int(line[1])
                y = int(line[2])
                product_locations.append(Coordinate(x, y))
            spec = PathSpecification.read_coordinates(coordinates)
            return TSPData(product_locations, spec)
        except FileNotFoundError:
            print("Error reading file " + product_file)
            traceback.print_exc()
            sys.exit()
