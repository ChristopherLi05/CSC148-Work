"""CSC148 Assignment 0 - Object-Oriented Modelling, Part 4

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

This file contains the code for a class representing a timetable.
For Part 4 of this assignment, you'll complete the implementation of this class.
"""
from __future__ import annotations
import json

from python_ta.contracts import check_contracts

from a0_part2 import Section
from a0_part3 import Course


@check_contracts
class Timetable:
    """A timetable for a single semester.

    Instance Attributes:
        - semester_code: the semester code for this timetable, e.g. '20239'
        - courses: dictionary that maps courses to the section(s) of that course that
            have been selected for this timetable. Note that a course can have more than one
            section selected (e.g., CSC148H1 might have both a LEC and TUT section).

    Representation Invariants:
        - self.semester_code in ['20239', '20241']
    """
    semester_code: str
    courses: dict[Course, list[Section]]  # Maps course to a list of sections

    def __init__(self, semester_code: str) -> None:
        """Initialize an empty timetable for the given semester.

        Preconditions:
            - semester_code in ['20239', '20241']

        This function is provided for you, and you should not change it.

        >>> my_timetable = Timetable('20239')
        >>> my_timetable.semester_code
        '20239'
        >>> my_timetable.courses
        {}
        """
        self.semester_code = semester_code
        self.courses = {}

    def add_section_by_code(self, course: Course, section_code: str) -> bool:
        """Add a new section to this timetable from the given course and section_code.

        Return True if a section was successfully added to the course, and False otherwise.
        - A section is NOT successfully added when no Section corresponding to section_code
          can be found for the course (in the correct semester).
        - In all other cases a section is successfully added.

        A section can be added even if it would make the timetable invalid (according to the
        definition in Part 4b).

        Hints:
            - How do you know what semester to use when looking up the section?
        """
        if sec := course.lookup_section(section_code, self.semester_code):
            self.courses.setdefault(course, [])
            self.courses[course].append(sec)
            return True
        return False

    def get_all_sections(self) -> list[Section]:
        """Return a list of sections in this timetable.

        The sections may be returned in any order.
        """
        return [j for i in self.courses.values() for j in i]

    def is_valid(self) -> bool:
        """Return whether this timetable is valid or not.

        See the assignment handout for the definition of "valid" for a timetable.

        Hints:
            - Reuse functions you've already implemented!
            - There are three different conditions that need to be checked for timetable validity.
              We recommend implementing and testing each condition separately, and encourage you
              to use helper functions/methods here!
        """
        return (all(i.semester_code == self.semester_code for i in self.get_all_sections())
                and all(not k.has_conflict(j) for i, j in enumerate(self.get_all_sections(), 1)
                        for k in self.get_all_sections()[i:])
                and all(sum(map(lambda x: x.section_code.startswith("LEC"), i)) == 1
                        for i in self.courses.values()))


def load_courses_data(file: str) -> dict[str, Course]:
    """Return a dictionary of Courses corresponding to the data found in <file>.

    Preconditions:
        - file is a valid JSON file that contains a list of course data,
          where each element is JSON data in the format described in Part 3
          of the assignment handout

    NOTE: This function is provided for you, and you should not change it.
    It relies on you completing the Course initializer in Part 3.
    """
    all_courses = {}

    with open(file) as f:
        raw_courses_data = json.load(f)
        for raw_course_data in raw_courses_data:
            new_course = Course(raw_course_data)
            all_courses[new_course.code] = new_course

    return all_courses


def run_part4_example() -> Timetable:
    """Run an example for Part 4.

    You MAY change this function (we will not be testing it directly, though it still will
    be checked by PythonTA).

    Note that this function loads a JSON file courses-100.json which is a *list*
    of individual course JSON objects of the format described in Part 3.
    You can open courses-100.json to see the raw data!
    """
    all_courses = load_courses_data('data/courses/courses-100.json')
    my_timetable = Timetable('20239')
    my_timetable.add_section_by_code(all_courses['CSB454H1'], 'LEC0101')
    my_timetable.add_section_by_code(all_courses['ENG250H1'], 'LEC5101')
    my_timetable.add_section_by_code(all_courses['CHM222H1'], 'TUT0101')

    return my_timetable


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a0_part4" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['load_courses_data'],
        'max-line-length': 100,
        'extra-imports': ['json', 'a0_part2', 'a0_part3'],
        'max-nested-blocks': 4,
        "output-format": "python_ta.reporters.PlainReporter"
    })
