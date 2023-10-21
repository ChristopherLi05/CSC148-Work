"""CSC148 Assignment 0 - Object-Oriented Modelling, Part 2

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

This file contains the code for a class representing a section.
For Part 2 of this assignment, you'll complete the implementation of this class.
"""
from __future__ import annotations
from datetime import time
import json

from python_ta.contracts import check_contracts

from a0_part1 import Timeslot


def load_section_data(file: str) -> Section:
    """Return a Section corresponding to the data found in <file>.

    Preconditions:
        - file is a valid JSON file in the format described in Part 2
          of the assignment handout, and represents a valid section

    NOTE: This function is provided for you, and you should not change it.
    It relies on you completing the Section initializer below to work properly.

    >>> my_section = load_section_data('data/sections/csc148-lec0101.json')
    >>> my_section.section_code
    'LEC0101'
    >>> my_section.semester_code
    '20239'
    >>> my_section.timeslots[0]  # Same order as the original JSON data
    Timeslot(1, datetime.time(10, 0), datetime.time(11, 0))
    >>> my_section.timeslots[1]
    Timeslot(3, datetime.time(9, 0), datetime.time(11, 0))
    """
    # This code reads data from a JSON file into Python, converting the
    # data into a combination of nested lists and dictionaries.
    with open(file) as f:
        raw_section_data = json.load(f)

    return Section(raw_section_data)


@check_contracts
class Section:
    """A representation of a section of a course.

    Instance Attributes:
        - section_code: section name
        - semester_code: semester code
        - timeslots: list of all meeting timeslots

    Representation Invariants: (Part 2c: fill these in)
        - self.semester_code in ['20239', '20241']
        - len(self.section_code) == 7
        - self.section_code[:3] in ['LEC', 'TUT', 'PRA']
        - self.timeslots
    """
    section_code: str
    semester_code: str
    timeslots: list[Timeslot]

    def __init__(self, raw_section_data: dict) -> None:
        """Initialize a section from the given JSON data.

        Preconditions:
            - The data is in the format described on the assignment handout.

        Hints:
            - This method is good review of Python dictionaries and lists.
            - You may find it helpful to copy-and-paste the example section data
              into the Python console (storing it in a variable) and then experiment
              with accessing the different parts.
            - Test the initialization of each attribute separately; section_code is easiest,
              followed by semester_code, and then timeslots.
            - You'll need to convert from milliseconds to datetime.time values.
              There are 1000 milliseconds in 1 second.
              We recommend creating a helper function to accomplish this task.
        """
        self.section_code = raw_section_data["name"]
        self.semester_code = raw_section_data["deliveryModes"][0]["session"]
        self.timeslots = [Timeslot(
            i["start"]["day"],
            time(i["start"]["millisofday"] // 3600000, i["start"]["millisofday"] // 60000 % 60),
            time(i["end"]["millisofday"] // 3600000, i["end"]["millisofday"] // 60000 % 60)
        )
            for i in raw_section_data["meetingTimes"]]

    def duration(self) -> float:
        """Return the total duration of timeslots of this section, in minutes.

        Preconditions:
        - none of this section's timeslots conflict with each other

        >>> my_section = load_section_data('data/sections/csc148-lec0101.json')
        >>> my_section.duration()
        3.0
        """
        return sum(map(Timeslot.duration, self.timeslots))

    def has_conflict(self, other: Section) -> bool:
        """Return whether this section and <other> conflict.

        >>> csc148_lec0201 = load_section_data('data/sections/csc148-lec0201.json')
        >>> csc236_lec0101 = load_section_data('data/sections/csc236-lec0301.json')
        >>> csc148_lec0201.has_conflict(csc236_lec0101)
        True
        """
        return any(any(x.has_conflict(y) for y in other.timeslots) for x in self.timeslots)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a0_part2" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['datetime', 'json', 'a0_part1'],
        'allowed-io': ['load_section_data'],
        "output-format": "python_ta.reporters.PlainReporter"
    })
