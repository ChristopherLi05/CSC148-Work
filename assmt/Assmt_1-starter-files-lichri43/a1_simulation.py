"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function run_example_simulation
here at the bottom of the `fil`e, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
modify/remove any of the existing attributes.
"""
# You MAY import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Any

from python_ta.contracts import check_contracts

import a1_algorithms
from a1_entities import Person, Elevator
from a1_visualizer import Direction, Visualizer


# TODO - check if I can do this in OH

def sign(num: int | float) -> int:
    """
    Returns the sign of the number: -1 if num < 0, 0 if num = 0, 1 if num > 0
    """
    if num < 0:
        return -1
    elif num > 0:
        return 1
    else:
        return 0


@check_contracts
class Simulation:
    """The main simulation class.

    Instance Attributes:
    - arrival_generator: the algorithm used to generate new arrivals.
    - elevators: a list of the elevators in the simulation
    - moving_algorithm: the algorithm used to decide how to move elevators
    - num_floors: the number of floors
    - visualizer: the Pygame visualizer used to visualize this simulation
    - waiting: a dictionary of people waiting for an elevator, where:
        - The keys are floor numbers from 1 to num_floors, inclusive
        - Each corresponding value is the list of people waiting at that floor
          (could be an empty list)
    - num_rounds: Number of rounds the simulation has gone through
    - total_people: Total number of people the simulation has gone through
    - waiting_times: List of waiting times of successful people

    Representation Invariants:
    - len(self.elevators) >= 1
    - self.num_floors >= 2
    - list(self.waiting.keys()) == list(range(1, self.num_floors + 1))
    - self.num_rounds >= 0
    - self.total_people >= 0
    """
    arrival_generator: a1_algorithms.ArrivalGenerator
    elevators: list[Elevator]
    moving_algorithm: a1_algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: dict[int, list[Person]]

    num_rounds: int
    total_people: int
    waiting_times: list[int]

    def __init__(self,
                 config: dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration.

        Preconditions:
        - config is a dictionary in the format found on the assignment handout
        - config['num_floors'] >= 2
        - config['elevator_capacity'] >= 1
        - config['num_elevators'] >= 1

        A partial implementation has been provided to you; you'll need to finish it!
        """

        # Initialize the algorithm attributes (this is done for you)
        self.arrival_generator = config['arrival_generator']
        self.moving_algorithm = config['moving_algorithm']

        self.num_floors = config["num_floors"]
        self.elevators = [
            Elevator(config["elevator_capacity"]) for _ in range(config["num_elevators"])
        ]
        self.waiting = {i + 1: [] for i in range(self.num_floors)}

        self.num_rounds = 0
        self.total_people = 0
        self.waiting_times = []

        # Initialize the visualizer (this is done for you).
        # Note that this should be executed *after* the other attributes
        # have been initialized, particularly self.elevators and self.num_floors.
        self.visualizer = Visualizer(self.elevators, self.num_floors,
                                     config['visualize'])

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> dict[str, int]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Preconditions:
        - num_rounds >= 1
        - This method is only called once for each Simulation instance
            (since we have not asked you to "reset" back to the initial simulation state
            for this assignment)
        """
        self.num_rounds += num_rounds

        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: elevator disembarking
            self.handle_disembarking()

            # Stage 2: new arrivals
            self.generate_arrivals(i)

            # Stage 3: elevator boarding
            self.handle_boarding()

            # Stage 4: move the elevators
            self.move_elevators()

            # Stage 5: update wait times
            self.update_wait_times()

            # Pause for 1 second
            # TODO - uncomment this
            # self.visualizer.wait(1)

        # The following line waits until the user closes the Pygame window
        self.visualizer.wait_for_exit()

        return self._calculate_stats()

    def handle_disembarking(self) -> None:
        """Handle people leaving elevators.

        Hints:
        - You shouldn't loop over a list (e.g. elevator.passengers) and mutate it within the
          loop body. This will cause unexpected behaviour due to how Python implements looping!
        - It's fine to reassign elevator.passengers to a new list. If you do so,
          make sure to call elevator.update() so that the new "fullness" of the elevator
          gets visualized properly.
        """

        for e in self.elevators:
            for i in range(len(e.passengers) - 1, -1, -1):
                if e.passengers[i].target == e.current_floor:
                    p = e.passengers.pop(i)
                    self.visualizer.show_disembarking(p, e)
                    self.waiting_times.append(p.wait_time)

    def generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""
        arrivals = self.arrival_generator.generate(round_num)

        for i, j in arrivals.items():
            self.waiting[i].extend(j)
            self.total_people += len(j)

        self.visualizer.show_arrivals(arrivals)

    def handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""

        # Creates a dict {floor_num: [(direction, elevator)]}
        mappings = {
            i + 1: [
                (sign(j.target_floor - j.current_floor), j)
                for j in self.elevators
                if j.current_floor == i + 1 and j.fullness() != 1
            ]
            for i in range(self.num_floors)
        }

        for floor_num, psngr in self.waiting.items():
            if not (elevators := mappings[floor_num]):
                continue

            while psngr:
                for e in elevators:
                    if (e[1].fullness() != 1
                            and (e[0] == 0 or sign(psngr[0].target - psngr[0].start) == e[0])):
                        p = psngr.pop(0)

                        e[1].passengers.append(p)
                        # e[1].target_floor = e[1].target_floor \
                        #     if e[1].target_floor != e[1].current_floor \
                        #     else p.target

                        self.visualizer.show_boarding(p, e[1])
                        break
                else:
                    break

    def move_elevators(self) -> None:
        """Update elevator target floors and then move them."""

        self.moving_algorithm.update_target_floors(self.elevators, self.waiting, self.num_floors)

        directions = []
        for e in self.elevators:
            d = sign(e.target_floor - e.current_floor)

            e.current_floor += d
            directions.append([Direction.STAY, Direction.UP, Direction.DOWN][d])

        self.visualizer.show_elevator_moves(self.elevators, directions)

    def update_wait_times(self) -> None:
        """Update the waiting time for every person waiting in this simulation.

        Note that this includes both people waiting for an elevator AND people
        who are passengers on an elevator. It does not include people who have
        reached their target floor.
        """
        for i in self.waiting.values():
            for j in i:
                j.wait_time += 1

        for i in self.elevators:
            for j in i.passengers:
                j.wait_time += 1

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> dict[str, int]:
        """Report the statistics for the current run of this simulation.

        Preconditions:
        - This method is only called after the simulation rounds have finished

        You MAY change the interface for this method (e.g., by adding new parameters).
        We won't call it directly in our testing.
        """
        return {
            'num_rounds': self.num_rounds,
            'total_people': self.total_people,
            'people_completed': len(self.waiting_times),
            'max_time': max(self.waiting_times) if self.waiting_times else -1,
            'avg_time': int(sum(self.waiting_times) / len(self.waiting_times))
        }


###############################################################################
# Simulation runner
###############################################################################
def run_example_simulation() -> dict[str, int]:
    """Run a sample simulation, and return the simulation statistics.

    This function is provided to help you test your work. You MAY change it
    (e.g., by changing the configuration values) for further testing.
    """
    num_floors = 8
    num_elevators = 4
    elevator_capacity = 3

    config = {
        'num_floors': num_floors,
        'num_elevators': num_elevators,
        'elevator_capacity': elevator_capacity,
        'arrival_generator': a1_algorithms.SingleArrivals(num_floors),
        # 'arrival_generator': a1_algorithms.FileArrivals(num_floors, "data/sample_arrivals_ten.csv"),
        # 'moving_algorithm': a1_algorithms.EndToEndLoop(),
        'moving_algorithm': a1_algorithms.FurthestFloor(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(50)
    return stats


if __name__ == '__main__':
    print(run_example_simulation())

    # We haven't provided any doctests for you, but if you add your own the following
    # code will run them!
    # import doctest
    #
    # doctest.testmod()

    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    # sample_run_stats = run_example_simulation()
    # print(sample_run_stats)

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a1_simulation" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['a1_entities', 'a1_visualizer', 'a1_algorithms'],
        'max-nested-blocks': 4,
        'max-attributes': 10,
        'max-line-length': 100,
        "output-format": "python_ta.reporters.PlainReporter"
    })
