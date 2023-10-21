"""CSC148 Assignment 0 - Object-Oriented Modelling, Part 3

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

This file contains the code for a class representing a course.
For Part 3 of this assignment, you'll complete the implementation of this class.
"""
from __future__ import annotations
import json

from python_ta.contracts import check_contracts

from a0_part2 import Section


def load_course_data(file: str) -> Course:
    """Return a Course corresponding to the data found in <file>.

    Preconditions:
        - file is a valid JSON file in the format described in Part 3
          of the assignment handout, and represents a valid course

    >>> csc148 = load_course_data('data/courses/course-csc148.json')
    >>> csc148.name
    'Introduction to Computer Science'
    >>> csc148.code
    'CSC148H1'
    >>> len(csc148.sections)
    12

    NOTE: This function is provided for you, and you should not change it.
    It relies on you completing the Course initializer below to work properly.
    """
    with open(file) as f:
        raw_course_data = json.load(f)

    return Course(raw_course_data)


@check_contracts
class Course:
    """A course.

    Instance Attributes (you need to fill this in!):
        - name: Course Name
        - code: Course Code
        - sections: List of course sections

    Representation Invariants:
        - self does not have duplicate section codes in the same semester
        - self.name
        - self.code
        - self.sections
    """

    name: str
    code: str
    sections: list[Section]

    def __init__(self, raw_course_data: dict) -> None:
        """Initialize a course from the given JSON data.

        Preconditions:
            - The data is in the format described on the assignment handout.

        Hints:
            - This might seem daunting at first because this JSON data is larger than the
              section data in Part 2. However, keep in mind that the "section data" portions
              of raw_course_data can be used to create new Section objects!
        """
        self.name = raw_course_data["name"]
        self.code = raw_course_data["code"]
        self.sections = [Section(i) for i in raw_course_data["sections"]]

    def get_code(self) -> str:
        """Return the course code for this course.

        >>> csc148 = load_course_data('data/courses/course-csc148.json')
        >>> csc148.get_code()
        'CSC148H1'
        """
        return self.code

    def get_title(self) -> str:
        """Return the course title for this course.

        >>> csc148 = load_course_data('data/courses/course-csc148.json')
        >>> csc148.get_title()
        'Introduction to Computer Science'
        """
        return self.name

    def lookup_section(self, section_code: str, semester_code: str) -> Section | None:
        """Return the section of this course that has the given section_code and semester_code.

        Return None if this course does not have a matching section.

        Preconditions:
            - this course has *at most one* section that matches the given section_code
              and semester_code

        >>> csc148 = load_course_data('data/courses/course-csc148.json')
        >>> lec0101 = csc148.lookup_section('LEC0101', '20239')
        >>> lec0101.section_code
        'LEC0101'
        >>> lec0101.semester_code
        '20239'
        >>> lec0101.timeslots[0]
        Timeslot(1, datetime.time(10, 0), datetime.time(11, 0))
        >>> lec0101.timeslots[1]
        Timeslot(3, datetime.time(9, 0), datetime.time(11, 0))
        """
        return temp[0] if (temp := [i for i in self.sections if i.section_code == section_code
                                    and i.semester_code == semester_code]) else None

    def get_compatible_sections(self, other_section: Section) -> list[Section]:
        """Return a list of the sections of this course that are compatible with <other_section>.

        A section is compatible with <other_section> when BOTH:

        - The section has the same semester as <other_section>
        - The section does not conflict with <other_section>

        Note that an empty list is a valid return value (when there are no compatible sections).
        """
        return [i for i in self.sections if i.semester_code == other_section.semester_code
                and not i.has_conflict(other_section)]


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a0_part3" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'extra-imports': ['json', 'a0_part2'],
        'allowed-io': ['load_course_data'],
        'disable': ['R1710'],
        "output-format": "python_ta.reporters.PlainReporter"
    })
