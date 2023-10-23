from __future__ import annotations


class Runner:
    """
    Basic Runner Class

    Attributes:
        - name: Name of the runner
        - email: Email of the runner
        - speed_category: Which speed category runner is in (0-3)
        - races: List of races runner is in
    """

    name: str
    email: str
    speed_category: int
    races: list[Registry]

    def __init__(self, name: str, email: str, speed_category: int) -> None:
        """
        Initializer

        >>> r = Runner("A", "B", 0)
        >>> r.name
        'A'
        >>> r.email
        'B'
        >>> r.speed_category
        0
        """
        self.name = name

        self.email = email
        self.speed_category = speed_category

        self.races = []

    def register_race(self, race: Registry) -> None:
        """
        Registers runner for a race

        >>> r = Runner("A", "B", 0)
        >>> rg = Registry("C")
        >>> r.register_race(rg)
        >>> r.races
        [Registry(name='C')]
        """
        self.races.append(race)
        race.register_user(self)

    def change_email(self, new_email: str) -> None:
        """
        Changes runner email

        >>> r = Runner("A", "B", 0)
        >>> r.email
        'B'
        >>> r.change_email("C")
        >>> r.email
        'C'
        """
        self.email = new_email

    def change_speed_category(self, new_category: int) -> None:
        """
        Changes runner speed category

        >>> r = Runner("A", "B", 0)
        >>> rg = Registry("C")
        >>> r.register_race(rg)
        >>> r.speed_category
        0
        >>> len(rg.categories[0])
        1
        >>> len(rg.categories[1])
        0
        >>> r.change_speed_category(1)
        >>> r.speed_category
        1
        >>> len(rg.categories[0])
        0
        >>> len(rg.categories[1])
        1
        """
        for i in self.races:
            i.change_speed_category(self, new_category)

        self.speed_category = new_category


class Registry:
    """
    Basic Registry Class

    Attributes:
        - name: Name of the Race
        - categories: List of the categories (0: under 20, 1: under 30, 2: under 40, 3: over 40)
    """

    name: str
    categories: list[list[Runner]]

    def __init__(self, name: str) -> None:
        """
        Basic Initializer

        >>> rg = Registry("A")
        >>> rg.name
        'A'
        >>> rg.categories
        [[], [], [], []]
        """
        self.name = name
        # 0: under 20
        # 1: under 30
        # 2: under 40
        # 3: over 40
        self.categories = [[] for _ in range(4)]

    def __repr__(self) -> str:
        """
        Basic repr
        """
        return f"Registry(name='{self.name}')"

    def register_user(self, runner: Runner) -> None:
        """
        Registers a user to this race, just modifies the categories

        >>> r = Runner("A", "B", 0)
        >>> rg = Registry("C")
        >>> rg.register_user(r)
        >>> len(rg.categories[0])
        1
        """
        self.categories[runner.speed_category].append(runner)

    def change_speed_category(self, runner: Runner, new_category: int) -> None:
        """
        Changes speed category

        >>> r = Runner("A", "B", 0)
        >>> rg = Registry("C")
        >>> r.register_race(rg)
        >>> len(rg.categories[0])
        1
        >>> len(rg.categories[1])
        0
        >>> rg.change_speed_category(r, 1)
        >>> len(rg.categories[0])
        0
        >>> len(rg.categories[1])
        1
        """
        try:
            self.categories[runner.speed_category].remove(runner)
        except ValueError:
            pass

        self.categories[new_category].append(runner)
