"""CSC148 Lab 3: Inheritance

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the implementation of a simple number game.
The key class design feature here is *inheritance*, which is used to enable
different types of players, both human and computer, for the game.
"""
from __future__ import annotations
import random

from python_ta.contracts import check_contracts


################################################################################
# Below is the implementation of NumberGame.
#
# You do not have to modify this class, but you should read through it and
# understand how it uses the Player class (and its subclasses) that you'll
# be implementing.
#
# As you read through, make note of any methods or attributes a Player will
# need.
################################################################################
@check_contracts
class NumberGame:
    """A number game for two players.

    A count starts at 0. On a player's turn, they add to the count an amount
    between a set minimum and a set maximum. The player who brings the count
    to a set goal amount is the winner.

    The game can have multiple rounds.

    Attributes:
    - goal:
        The amount to reach in order to win the game.
    - min_step:
        The minimum legal move.
    - max_step:
        The maximum legal move.
    - current:
        The current value of the game count.
    - players:
        The two players.
    - turn:
        The turn the game is on, beginning with turn 0.
        If turn is even number, it is players[0]'s turn.
        If turn is any odd number, it is player[1]'s turn.

    Representation Invariants:
    - self.turn >= 0
    - 0 <= self.current <= self.goal
    - 0 < self.min_step <= self.max_step <= self.goal
    """
    goal: int
    min_step: int
    max_step: int
    current: int
    players: tuple[Player, Player]
    turn: int

    def __init__(self, goal: int, min_step: int, max_step: int,
                 players: tuple[Player, Player]) -> None:
        """Initialize this NumberGame.

        Preconditions:
        - 0 < min_step <= max_step <= goal
        """
        self.goal = goal
        self.min_step = min_step
        self.max_step = max_step
        self.current = 0
        self.players = players
        self.turn = 0

    def play(self) -> str:
        """Play one round of this NumberGame. Return the name of the winner.

        A "round" is one full run of the game, from when the count starts
        at 0 until the goal is reached.
        """
        while self.current < self.goal:
            self.play_one_turn()
        # The player whose turn would be next (if the game weren't over) is
        # the loser. The one who went one turn before that is the winner.
        loser = self.whose_turn(self.turn)
        winner = self.whose_turn(self.turn - 1)
        winner.record_win()
        loser.record_loss()
        return winner.name

    def whose_turn(self, turn: int) -> Player:
        """Return the Player whose turn it is on the given turn number.
        """
        if turn % 2 == 0:
            return self.players[0]
        else:
            return self.players[1]

    def play_one_turn(self) -> None:
        """Play a single turn in this NumberGame.

        Determine whose move it is, get their move, and update the current
        total as well as the number of the turn we are on.
        Print the move and the new total.
        """
        next_player = self.whose_turn(self.turn)
        amount = next_player.move(
            self.current,
            self.min_step,
            self.max_step,
            self.goal
        )
        self.current += amount

        # We set a hard limit on self.current
        # (This is a strange corner case: don't worry about it!)
        if self.current > self.goal:
            self.current = self.goal

        self.turn += 1

        print(f'{next_player.name} moves {amount}.')
        print(f'Total is now {self.current}.')


################################################################################
# Implement your Player class and it subclasses below!
################################################################################
class Player:
    """
    Generic Player Class

    Attributes:
        - name: player name

    Private Attributes:
        - win_loss: win, loss of the player
    """
    name: str
    _win_loss: list[int, int]

    def __init__(self, name: str) -> None:
        """
        Initializes the object
        """
        self.name = name
        self._win_loss = [0, 0]

    def move(self, current_num: int, min_step: int, max_step: int, goal: int) -> int:
        """
        Returns the move the player would like to do
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', wins={self._win_loss[0]}, losses={self._win_loss[1]})"

    def record_win(self) -> None:
        """
        Adds a counter for the win
        """
        self._win_loss[0] += 1

    def record_loss(self) -> None:
        """
        Adds a counter for the loss
        """
        self._win_loss[1] += 1


class RandomPlayer(Player):
    """
    Player that makes a move randomly
    """

    def __init__(self, name: str) -> None:
        """
        Initializes a RandomPlayer
        """
        Player.__init__(self, name)

    def move(self, current_num: int, min_step: int, max_step: int, goal: int) -> int:
        """
        Returns a random number between min_step and max_step (inclusive)
        """
        return random.randint(min_step, max_step)


class UserPlayer(Player):
    """
    Player that asks the user for the move
    """
    def __init__(self, name: str) -> None:
        """
        Initializes a UserPlayer
        """
        Player.__init__(self, name)

    def move(self, current_num: int, min_step: int, max_step: int, goal: int) -> int:
        """
        Asks the user for a number between min_step and max_step (inclusive), keeps on asking
        until user inputs get a valid number
        """
        while True:
            try:
                if min_step <= int(a := input(
                        f"Player {self.name}, enter a number between {min_step} and {max_step}: ")) <= max_step:
                    return int(a)
            except ValueError:
                print("Try again")


class StrategicPlayer(Player):
    """
    Player that strategically does moves
    """
    # hash: [number, who_wins]
    memoize: dict[str, tuple[int, int]] = {}

    def __init__(self, name: str) -> None:
        Player.__init__(self, name)

    def move(self, current_num: int, min_step: int, max_step: int, goal: int) -> int:
        temp = StrategicPlayer.move_internal(0, current_num, min_step, max_step, goal, 0)

        if temp[1] == 0:
            return temp[0]
        return random.randint(min_step, max_step)

    @staticmethod
    def move_internal(
            player_num: int, current_num: int, min_step: int, max_step: int, goal: int, depth: int
    ) -> tuple[int, int]:
        """
        Recursive function that tries to find the best move for player 0
        Maxdepth = 20
        """

        hash_ = f"{player_num},{current_num}"

        if hash_ in StrategicPlayer.memoize:
            return StrategicPlayer.memoize[hash_]

        if depth >= 20:
            return -1, -1

        player = (-1, -1)

        for i in range(max_step, min_step - 1, -1):
            if current_num + i >= goal:
                StrategicPlayer.memoize[hash_] = (i, player_num)
                return i, player_num
            else:
                player = StrategicPlayer.move_internal(1 - player_num, current_num + i, min_step,
                                                       max_step, goal, depth + 1)
                player = (i, player[1])

                if player != (-1, -1):
                    StrategicPlayer.memoize[hash_] = player

                    if player[1] == player_num:
                        return player

        return player


@check_contracts
def make_player(generic_name: str) -> Player:
    """Return a new Player based on user input.

    Allow the user to choose a player name and player type.
    <generic_name> is a placeholder used to identify which player is being made.
    """
    # name = input(f'Enter a name for {generic_name}: ')
    name = generic_name
    player_type = input("What type of player (Random, Strategic, User (default)): ")

    if player_type == "Random":
        return RandomPlayer(name)
    elif player_type == "Strategic":
        return StrategicPlayer(name)
    else:
        return UserPlayer(name)


################################################################################
# The main game program
################################################################################
def main() -> None:
    """Play multiple rounds of a NumberGame based on user input settings.
    """

    goal = 21
    minimum = 1
    maximum = 3
    # goal = int(input('Enter goal amount: '))
    # minimum = int(input('Enter minimum move: '))
    # maximum = int(input('Enter maximum move: '))
    p1 = make_player('p1')
    p2 = make_player('p2')
    while True:
        g = NumberGame(goal, minimum, maximum, (p1, p2))
        winner = g.play()
        print(f'And {winner} is the winner!!!')
        print(p1)
        print(p2)
        again = input('Again? (y/n) ')
        if again != 'y':
            return


if __name__ == '__main__':
    # main()

    # Uncomment to check your work with python_ta!
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['random', 'functools'],
        'allowed-io': [
            'main',
            'make_player',
            'UserPlayer.move',
            'NumberGame.play_one_turn'
        ],
        'max-line-length': 100,
        "output-format": "python_ta.reporters.PlainReporter"
    })
