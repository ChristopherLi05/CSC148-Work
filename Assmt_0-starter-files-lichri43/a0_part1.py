"""CSC148 Assignment 0 - Object-Oriented Modelling, Part 1

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Joonho Kim

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 David Liu, Joonho Kim

=== Module Description ===

This file contains the code for a class representing a section timeslot.
For Part 1a of this assignment, you'll complete the implementation of this class.
"""
from __future__ import annotations
from datetime import time

from python_ta.contracts import check_contracts


@check_contracts
class Timeslot:
    """A single meeting time for a course section.

    Instance Attributes:
        - day: the day of the week when this timeslot meets.
            This is stored as an integer between 1 and 5, where
            1 represents Monday, 2 represents Tuesday, etc.
        - start: the starting time of this timeslot.
        - end: the ending time of this timeslot.

    Start and end times are represented as datetime.time objects. You may find the
    Python documentation useful: https://docs.python.org/3/library/datetime.html#time-objects

    Start and end times can have non-zero hours and minutes, but their "seconds" and "microseconds"
    attributes are 0. (These are encoded in representation invariants, and will help simplify
    the Timeslot.duration method.)

    We do NOT enforce that classes can only occur during certain hours of the day
    (e.g., between 9am and 9pm).

    Representation Invariants:
        - 1 <= self.day <= 5
        - self.start < self.end
        - self.start.seconds == 0 and self.start.microseconds == 0
        - self.end.seconds == 0 and self.end.microseconds == 0
    """
    day: int
    start: time
    end: time

    def __init__(self, day: int, start: time, end: time) -> None:
        """Initialize a new timeslot with the given attributes.

        >>> my_timeslot = Timeslot(2, time(10), time(12, 30))  # Tuesdays 10--12:30
        >>> my_timeslot.day
        2
        >>> my_timeslot.start
        datetime.time(10, 0)
        >>> my_timeslot.end
        datetime.time(12, 30)
        """
        self.day = day
        self.start = start
        self.end = end

    def duration(self) -> float:
        """Return the duration of this timeslot, in hours.

        >>> my_timeslot = Timeslot(2, time(10), time(12, 30))
        >>> my_timeslot.duration()
        2.5

        Hints:
            - Read the representation invariants carefully!
            - Don't forget about minutes.
            - Don't perform any rounding (since this is not part of the function specification!)
        """
        temp = self.end.hour * 60 + self.end.minute - self.start.hour * 60 - self.start.minute
        return temp / 60

    def has_conflict(self, other: Timeslot) -> bool:
        """Return whether this timeslot conflicts with the other timeslot.

        See assignment handout for the definition of timeslot conflicts.

        >>> timeslot1 = Timeslot(1, time(1), time(4))
        >>> timeslot2 = Timeslot(1, time(3), time(6))
        >>> timeslot1.has_conflict(timeslot2)
        True
        """
        return self.day == other.day and \
            (self.start <= other.start < self. end or other.start <= self.start < other.end)

    def __repr__(self) -> str:
        """Returns a string representation of the timeslot.

        This function is a special method that displays a custom string when
        an object of this type is evaluated in the Python console. It is provided
        for you for testing purposes; please don't change it!

        >>> my_timeslot = Timeslot(2, time(10), time(12, 30))
        >>> my_timeslot
        Timeslot(2, datetime.time(10, 0), datetime.time(12, 30))
        """
        return f'Timeslot({self.day}, {repr(self.start)}, {repr(self.end)})'


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a0_part1" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['datetime'],
        "output-format": "python_ta.reporters.PlainReporter"
    })
