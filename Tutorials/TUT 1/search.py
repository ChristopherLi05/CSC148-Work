"""CSC148 Lab 1: Introduction to CSC148!

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains a function that searches for an item in a list,
and illustrates how to use doctest.
"""
from python_ta.contracts import check_contracts
from typing import Any
import math


@check_contracts
def binary_search(lst: list, t: Any) -> int:
    """Return the index of <t> in <lst>, or -1 if it does not occur.

    Preconditions:
    - lst is sorted.
      Specifically, lst[0] <= lst[1] ... <= lst[n-1], where n is len(lst).
    - t can be compared to the elements of lst

    >>> binary_search([2, 4, 7, 8, 11], 11)  # 11 is at index 4 in the list
    4
    >>> binary_search([2, 4, 7, 8, 11], 5)   # 5 is not in the list
    -1
    """
    first = 0
    last = len(lst)-1
    while first<last:
        mid = (last + first)//2
        if t < lst[mid]:
            last = mid - 1
        else:
            first = mid + 1
    if lst[first] == t:
        return first
    else:
        return -1

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Task 6: Try uncommenting the following lines, which will cause
    # PythonTA to check this file. PyCharm Tip: you can comment/uncomment
    # many lines at a time by selecting them and pressing Ctrl + / (Windows)
    # or ⌘ + / (Mac).

    # import python_ta
    # python_ta.check_all()
