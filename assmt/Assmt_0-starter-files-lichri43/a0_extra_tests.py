"""CSC148 Assignment 0 - Object-Oriented Modelling, Additional Tests

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

This file contains a small number of additional test cases for Parts 2, 3, and 4
for this assignment. Unlike a0_part1_test.py, you will *not* be submitting this file
for grading, so it's completely up to you how you decide to use it.
"""
from datetime import time

import pytest

from a0_part2 import load_section_data, Section
from a0_part3 import Course
from a0_part4 import Timetable, load_courses_data


################################################################################
# Sample test cases for Part 2 (uncomment them as you go)
################################################################################
def test_section_init() -> None:
    """Test that the __init__ creates and sets the required attributes
    correctly.
    """
    section_148_lec0101 = load_section_data('data/sections/csc148-lec0101.json')

    assert section_148_lec0101.section_code == 'LEC0101'
    assert section_148_lec0101.semester_code == '20239'

    expected_timeslots = [(1, time(10), time(11)), (3, time(9), time(11))]
    timeslot1 = section_148_lec0101.timeslots[0]
    timeslot2 = section_148_lec0101.timeslots[1]

    actual_timeslots = [
        (timeslot1.day, timeslot1.start, timeslot1.end),
        (timeslot2.day, timeslot2.start, timeslot2.end)
    ]
    assert expected_timeslots == actual_timeslots


def test_section_duration_multiple_timeslots() -> None:
    """Test that duration returns the correct duration when there are
    multiple timeslots"""
    section_148_lec0101 = load_section_data('data/sections/csc148-lec0101.json')
    assert section_148_lec0101.duration() == 3.0


def test_section_conflicts_one_conflict() -> None:
    """Test that conflicts returns True when one of the timeslots
    conflicts with other
    """
    section_148_lec0101 = load_section_data('data/sections/csc148-lec0101.json')

    other = Section({
        "name": "LEC0201",
        "deliveryModes": [
            {
                "session": "20239",
                "mode": "INPER"
            }
        ],
        "meetingTimes": [
            {
                "start": {
                    "day": 1,
                    "millisofday": 37800000
                },
                "end": {
                    "day": 1,
                    "millisofday": 41400000
                }
            },
        ]
    }
    )

    assert section_148_lec0101.has_conflict(other)


def test_rep_inv_invalid_semester() -> None:
    """Test creating a Section with an invalid semester code.

    Note that we're making use of a custom "bad" JSON file.
    You can create copies of the files we've provided and modify them for your
    own tests for the other representation invariants.
    """
    with pytest.raises(AssertionError):  # Check that the inner code raises an AssertionError
        load_section_data('data/sections/csc148-invalid-semester.json')


################################################################################
# Sample test cases for Part 3 (uncomment them as you go)
################################################################################
def test_course_get_code() -> None:
    """Test that Course.get_code returns the correct course code"""
    course_single_section = create_course_single_section()
    assert course_single_section.get_code() == 'CSC999H1'


def test_course_get_title() -> None:
    """Test that Course.get_title returns the correct course title"""
    course_single_section = create_course_single_section()
    assert course_single_section.get_title() == 'Non-existent Computer Science'


def test_course_lookup_section_wrong_semester() -> None:
    """Test that Course.lookup_section returns None when the wrong semester_code
    is provided
    """
    course_single_section = create_course_single_section()
    assert course_single_section.lookup_section('LEC0101', '20241') is None


def test_course_get_compatible_sections_one_section_no_conflicts() -> None:
    """Test that Course.get_compatible_sections returns the correct section
    when given a section that has no conflicts and a course with only a single section
    """
    course_single_section = create_course_single_section()
    section_148_lec0101 = load_section_data('data/sections/csc148-lec0101.json')

    actual = course_single_section.get_compatible_sections(section_148_lec0101)
    expected = [course_single_section.lookup_section('LEC0101', '20239')]

    assert actual == expected


################################################################################
# Sample test cases for Part 4 (uncomment them as you go)
################################################################################
def test_timetable_add_section_by_code() -> None:
    """Test that Timetable.add_section_by_code correctly adds a section to
    an empty timetable.
    """
    empty_timetable = Timetable('20239')
    course_single_section = create_course_single_section()
    assert empty_timetable.add_section_by_code(course_single_section, 'LEC0101')

    actual = empty_timetable.courses[course_single_section]
    expected = [course_single_section.lookup_section('LEC0101', '20239')]
    assert actual == expected


def test_timetable_get_all_sections_single_section() -> None:
    """Test that Timetable.get_all_sections returns the correct section.
    """
    course_single_section = create_course_single_section()
    timetable = Timetable('20239')
    timetable.add_section_by_code(course_single_section, 'LEC0101')

    actual = timetable.get_all_sections()
    expected = [course_single_section.lookup_section('LEC0101', '20239')]

    assert actual == expected


def test_timetable_is_valid_single_section():
    """Test that Timetable.is_valid returns True for a timetable with a single section.
    """
    course_single_section = create_course_single_section()
    timetable = Timetable('20239')
    timetable.add_section_by_code(course_single_section, 'LEC0101')

    assert timetable.is_valid()


def test_timetable_empty():
    """Tests if empty timetables are valid
    """
    timetable = Timetable('20239')

    assert timetable.is_valid()


def test_timetable_same_semester():
    """Tests if courses with different semesters is not valid
    """
    timetable = Timetable('20241')

    all_courses = load_courses_data('data/courses/courses-100.json')
    timetable.add_section_by_code(all_courses["PHC301H1"], "LEC0101")

    # add_section_by_code ignores when semester code isn't right
    timetable.semester_code = '20239'

    assert not timetable.is_valid()


def test_timetable_conflicting():
    """Tests if timetable is valid with conflicting sessions
    """

    timetable = Timetable('20239')

    assert timetable.add_section_by_code(create_custom_course([["LEC0101", time(1, 0), time(2, 0)]]), "LEC0101")
    assert timetable.add_section_by_code(create_custom_course([["TUT0101", time(1, 0), time(2, 0)]]), "TUT0101")
    assert not timetable.is_valid()


def test_timetable_no_lec():
    """Tests if timetable has no lectures
    """

    timetable = Timetable('20239')

    assert timetable.add_section_by_code(create_custom_course([["TUT0101", time(1, 0), time(2, 0)]]), "TUT0101")
    assert not timetable.is_valid()


def test_timetable_mult_lec():
    """Tests if timetable has multiple lectures
    """

    timetable = Timetable('20239')

    c = create_custom_course([["LEC0101", time(1, 0), time(2, 0)], ["LEC0102", time(2, 0), time(3, 0)]])

    assert timetable.add_section_by_code(c, "LEC0101")
    assert timetable.add_section_by_code(c, "LEC0102")
    assert not timetable.is_valid()


def test_timetable_courses_after():
    """Tests if courses one after another is valid
    """

    timetable = Timetable('20239')

    c = create_custom_course([["LEC0101", time(1, 0), time(2, 0)], ["TUT0101", time(2, 0), time(3, 0)]])

    assert timetable.add_section_by_code(c, "LEC0101")
    assert timetable.add_section_by_code(c, "TUT0101")
    assert timetable.is_valid()


################################################################################
# Helper functions that create objects we can use in our test cases
################################################################################
def create_course_single_section() -> Course:
    """Return a Course with a single section.

    This is a convenience helper function to avoid copying a lot of code.
    """
    return Course({
        "name": "Non-existent Computer Science",
        "code": "CSC999H1",
        "sections": [
            {
                "name": "LEC0101",
                "deliveryModes": [
                    {
                        "session": "20239",
                        "mode": "INPER"
                    }
                ],
                "meetingTimes": [
                    {
                        "start": {
                            "day": 2,
                            "millisofday": 36000000
                        },
                        "end": {
                            "day": 2,
                            "millisofday": 39600000
                        }
                    }
                ]
            }
        ]
    })


def create_custom_course(sections: list[list[str, time, time]]) -> Course:
    """Return a Course with a single section.

    This is a convenience helper function to avoid copying a lot of code.
    """

    return Course({
        "name": "Random CS Course",
        "code": "CSC998H1",
        "sections": [
            {
                "name": i[0],
                "deliveryModes": [
                    {
                        "session": "20239",
                        "mode": "INPER"
                    }
                ],
                "meetingTimes": [
                    {
                        "start": {
                            "day": 1,
                            "millisofday": (i[1].hour * 60 + i[1].minute) * 60000
                        },
                        "end": {
                            "day": 1,
                            "millisofday": (i[2].hour * 60 + i[2].minute) * 60000
                        }
                    }
                ]
            }
            for i in sections
        ]
    })


if __name__ == '__main__':
    pytest.main(['a0_extra_tests.py'])
