"""CSC148 Assignment 0 - Object-Oriented Modelling, Part 1 (Tests)

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

This file contains the code for testing your Timeslot class.
For Part 1b of this assignment, you'll complete the test cases below
according to their given docstrings.

Notes:

1. You MAY add additional test cases beyond the ones we've started
   for you; just make sure that you use different names that don't conflict
   with the ones we've given you.
2. We are *not* grading this file with PythonTA.
"""
from datetime import time
import pytest

from a0_part1 import Timeslot


def test_duration_simple() -> None:
    """Test Timeslot.duration when the duration is exactly 1 hour.

    We have provided a template (fill in the ...) that you can use
    for other tests in this file.
    """
    timeslot = Timeslot(1, time(10), time(11))

    assert timeslot.duration() == 1


def test_duration_long() -> None:
    """Test Timeslot.duration when the duration is exactly 23.25 hours.
    """
    timeslot = Timeslot(1, time(0, 15), time(23, 30))

    assert timeslot.duration() == 23.25


def test_has_conflict_different_days() -> None:
    """Test Timeslot.has_conflict when given two timeslots that:

    1. have the same start and end times,
    2. but are on different days.
    """
    timeslot1 = Timeslot(1, time(0, 15), time(23, 30))
    timeslot2 = Timeslot(2, time(0, 15), time(23, 30))

    assert not timeslot1.has_conflict(timeslot2)
    assert not timeslot2.has_conflict(timeslot1)


def test_has_conflict_back_to_back() -> None:
    """Test Timeslot.has_conflict when given two timeslots that:

    1. are on the same day,
    2. and the start time for one timeslot equals the end time for the other
    """
    timeslot1 = Timeslot(1, time(10), time(11))
    timeslot2 = Timeslot(1, time(11), time(12))

    assert not timeslot1.has_conflict(timeslot2)
    assert not timeslot2.has_conflict(timeslot1)


def test_has_conflict_fully_contained() -> None:
    """Test Timeslot.has_conflict when given two timeslots that:

    1. are on the same day,
    2. and one timeslot is contained inside the other (i.e., starts after
       and ends before the other timeslot).
    """
    timeslot1 = Timeslot(1, time(11), time(13))
    timeslot2 = Timeslot(1, time(11), time(12))

    assert timeslot1.has_conflict(timeslot2)
    assert timeslot2.has_conflict(timeslot1)


def test_rep_inv_invalid_day() -> None:
    """Test creating a Timeslot with a day that's < 1 or > 5.

    This should cause PythonTA's check_contracts to raise an error,
    which is checked for using pytest.raises in the code we've provided.
    The only part you need to fill in is the ... to create the invalid Timeslot.

    Note: we're introducing this format of test here so that you can use it
    on other parts of this assignment!
    """
    with pytest.raises(AssertionError):  # Check that the inner code raises an AssertionError
        Timeslot(0, time(0), time(1))


def test_rep_inv_invalid_start_end() -> None:
    """Test creating a Timeslot with a valid day, but a start time that is >= the end time.

    This test follows the same structure as the previous one.
    """
    with pytest.raises(AssertionError):  # Check that the inner code raises an AssertionError
        Timeslot(1, time(1), time(0))


if __name__ == '__main__':
    pytest.main(['a0_part1_test.py', '-v'])
