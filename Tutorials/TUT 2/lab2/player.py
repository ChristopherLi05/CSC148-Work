class Player:
    """
    A player for the game

    Attributes:
        - name: name of the player
        - game_history: history of the last 100 scores they've achieved

    Representation Invariants:
        - len(self.game_history) <= 100

    """

    name: str
    game_history: list

    def __init__(self, name):
        """
        Initializes a new player

        >>> p = Player("A")
        >>> p.name
        'A'
        >>> p.game_history
        []
        """

        self.name = name
        self.game_history = []

    def add_score(self, score: int) -> None:
        """
        Adds a new score to the player's history

        >>> p = Player("A")
        >>> p.add_score(3)
        >>> p.game_history
        [3]
        >>> p.add_score(5)
        >>> p.add_score(6)
        >>> p.add_score(7)
        >>> p.add_score(8)
        >>> p.game_history
        [8, 7, 6, 5, 3]
        """
        self.game_history = ([score] + self.game_history)[:100]

    def average_score(self, num_games: int = 100) -> float:
        """
        Gets average of the recent games, defaults to all

        >>> p = Player("A")
        >>> p.add_score(3)
        >>> p.add_score(5)
        >>> p.add_score(6)
        >>> p.add_score(7)
        >>> p.add_score(8)
        >>> p.average_score(1)
        8.0
        >>> p.average_score(3)
        7.0
        """
        return sum(self.game_history[0:num_games]) / max(len(self.game_history[0:num_games]), 1)

    def top_score(self):
        """
        Gets the top score the player

        >>> p = Player("A")
        >>> p.add_score(3)
        >>> p.add_score(5)
        >>> p.add_score(6)
        >>> p.add_score(7)
        >>> p.add_score(8)
        >>> p.add_score(7)
        >>> p.top_score()
        8
        """
        return max(self.game_history, default=0)
