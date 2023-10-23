import math, random


class Vehicle:
    """An abstract class for a vehicle in the Super Duper system.
    Attributes:
    - position: The location of this vehicle (coordinates on a 2-D grid).
    - fuel: The amount of fuel remaining for this vehicle.
    Representation Invariants:
    - self.fuel >= 0
    """

    travel_distance: float = 0
    position: tuple[int, int]
    fuel: int

    def __init__(self, initial_fuel: int, initial_position: tuple[int, int]) -> None:
        """Initialize a new Vehicle with the given fuel and position.
        Precondition: initial_fuel >= 0
        """
        self.fuel = initial_fuel
        self.position = initial_position

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """Return how much fuel this vehicle needs to move to the given position.
        Note: the amount returned may be larger than self.fuel,
        indicating that this vehicle cannot move to the given position.
        """
        raise NotImplementedError

    def get_distance(self, new_x, new_y):
        raise NotImplementedError

    def move(self, new_x: int, new_y: int) -> None:
        """Move this vehicle to the given position.
        Do nothing if this vehicle does not have enough fuel to move to the
        specified position.
        """
        needed = self.fuel_needed(new_x, new_y)
        if needed <= self.fuel:
            self.travel_distance += self.get_distance(new_x, new_y)
            self.position = (new_x, new_y)
            self.fuel -= needed


class Car(Vehicle):
    """A car in the Super Duper system.
    A car can only move vertically and horizontally, and uses
    one unit of fuel per unit distance travelled.
    """

    def __init__(self, initial_fuel: int) -> None:
        """Initialize a new Vehicle with the given fuel and position.
        A car always starts at (0, 0).
        Precondition: initial_fuel >= 0
        """
        Vehicle.__init__(self, initial_fuel, (0, 0))

    def get_distance(self, new_x, new_y):
        return abs(new_x - self.position[0]) + abs(new_y - self.position[1])

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """Return how much fuel this vehicle needs to move to the given position.
        Note: the amount returned may be larger than self.fuel,
        indicating that this vehicle cannot move to the given position.
        """
        return self.get_distance(new_x, new_y)

    # def move(self, new_x: int, new_y: int) -> None:
    #     old_x, old_y = self.position
    #     Vehicle.move(self, new_x, new_y)
    #     self.travel_distance += abs(old_x - new_x) + abs(old_y - new_y)


class Helicopter(Vehicle):
    """A Helicopter in the Super Duper system.
    """

    def __init__(self, initial_fuel: int) -> None:
        """Initialize a new Vehicle with the given fuel and position.
        """
        Vehicle.__init__(self, initial_fuel, (3, 5))

    def get_distance(self, new_x, new_y):
        dx = self.position[0] - new_x
        dy = self.position[1] - new_y
        return math.sqrt(dx ** 2 + dy ** 2)

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        return int(math.ceil(self.get_distance(new_x, new_y)))

    # def move(self, new_x: int, new_y: int) -> None:
    #     old_x, old_y = self.position
    #     Vehicle.move(self, new_x, new_y)
    #     self.travel_distance += ((old_x - new_x) ** 2 + (old_y - new_y) ** 2) ** 0.5


class UnreliableMagicCarpet(Vehicle):
    """A UnreliableMagicCarpet in the Super Duper system.
    """

    def __init__(self) -> None:
        """Initialize a new Vehicle with the given fuel and position.
        A car always starts at (0, 0).
        Precondition: initial_fuel >= 0
        """
        initial_x = random.randint(-10, 10)
        initial_y = random.randint(-10, 10)
        Vehicle.__init__(self, 0, (initial_x, initial_y))

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        return 0

    def get_distance(self, new_x, new_y):
        dx = self.position[0] - new_x
        dy = self.position[1] - new_y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move(self, new_x: int, new_y: int) -> None:
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)

        new_x = new_x + dx
        new_y = new_y + dy

        self.travel_distance += self.get_distance(new_x, new_y)
        self.position = (new_x, new_y)


class SuperDuperManager:
    """A class responsible for keeping track of all vehicles in the system.
    Private Attributes:
    - _vehicles:
    Maps a string that uniquely identifies a vehicle to the corresponding Vehicle object.
    For example, _vehicles['car1'] would be a Vehicle object with the id_ 'car1'.
    """
    _vehicles: dict[str, Vehicle]

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.
        There are no vehicles in the system when first created.
        """

    def add_vehicle(self, vehicle_type: str, id_: str, fuel: int) -> None:
        """Add a new vehicle with the given type, id_, and fuel to the system.
        Do nothing if there is already a vehicle with the given id.
        Preconditions:
        - vehicle_type in ['Car', 'Helicopter', 'UnreliableMagicCarpet']
        - fuel >= 0
        """
        if id_ not in self._vehicles:  # Check to make sure the id isn't already used.
            if vehicle_type == 'Car':
                self._vehicles[id_] = Car(fuel)
        elif vehicle_type == 'Helicopter':
            self._vehicles[id_] = Helicopter(fuel)
        else:  # vehicle_type == 'UnreliableMagicCarpet':
            self._vehicles[id_] = UnreliableMagicCarpet()

    def get_vehicle_position(self, id_: str) -> tuple[int, int]:
        """Return the position of the vehicle with the given id.
        Precondition: A vehicle corresponding to id_ has been added
        """
        vehicle = self._vehicles[id_]
        return vehicle.position

    def move_vehicle(self, id_: str, new_x: int, new_y: int) -> None:
        """Move the vehicle with the given id to the given position.
        Do nothing if the vehicle does not have enough fuel to move.

        Precondition: A vehicle corresponding to id_ has been added
        """

        self._vehicles[id_].move(new_x, new_y)

    def get_total_travel_distance(self) -> float:
        """Return the total distance travelled by all vehicles."""

        total_distance = 0.0
        for vehicle in self._vehicles.values():  # Iterates over the *values* in the dictionary
            total_distance += vehicle.travel_distance
        return total_distance
