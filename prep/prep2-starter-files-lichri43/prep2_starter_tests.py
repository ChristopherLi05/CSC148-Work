"""CSC148 Prep 2: Object Oriented Programming

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu, Diane Horton, and Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 David Liu, Diane Horton, and Sophia Huynh

=== Module Description ===
This module contains sample tests for Prep 2.
Complete the TODO in this file.
There is also a task inside prep2.py.
Make sure to look at that file and complete the TODO there as well.

We suggest you also add your own tests to practice writing tests and
to be confident your code is correct.

When writing a test case, make sure you create a new function, with its
name starting with "test_". For example:

def test_my_test_case():
    # Your test here

All test cases must have different names (i.e. you cannot have two tests
named test_my_test_case).

NOTE: We will not be checking this file with PythonTA. So even though you
will submit both this file and prep2.py, only prep2.py will be checked
with PythonTA for grading purposes.
"""
from prep2 import Spinner, Tweet
from datetime import date


################################################################################
# Part 3
# In this part, you will be fixing a bug within a provided test.
################################################################################
def test_buggy_consecutive_spins() -> None:
    """Test consecutive spins of your Spinner class.
    This test case has a bug in it."""

    s = Spinner(6)                          # Do not change this line
    s.spin(2)                               # Do not change this line
    expected_value1 = 2
    assert s.position == expected_value1    # Do not change this line

    s.spin(2)                               # Do not change this line
    expected_value2 = 4
    assert s.position == expected_value2    # Do not change this line


################################################################################
# Sample test cases below
#
# Use the below test cases as an example for writing your own test cases,
# and as a start to testing your prep2.py code.
#
# The self-test on MarkUs runs the tests below, along with a few others.
# Make sure you run the self-test after submitting your code!
#
# WARNING: THIS IS CURRENTLY AN EXTREMELY INCOMPLETE SET OF TESTS!
# We will test your code on a much more thorough set of tests!
# We encourage you to add your own test cases to this file.
################################################################################
def test_doctest() -> None:
    """Test the given doctest in the Spinner class docstring."""
    spinner = Spinner(8)

    spinner.spin(4)
    assert spinner.position == 4

    spinner.spin(2)
    assert spinner.position == 6

    spinner.spin(2)
    assert spinner.position == 0


def test_unlike_doctest() -> None:
    """Test the given doctest in the Tweet.unlike method."""
    tweet = Tweet('Sophia', date(2021, 1, 1), 'Happy new year!')
    tweet.like(5)
    assert tweet.likes == 5
    tweet.unlike()
    assert tweet.likes == 4


if __name__ == '__main__':
    import pytest
    pytest.main(['prep2_starter_tests.py'])
