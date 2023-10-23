"""CSC148 Lab 1: Introduction to CSC148!
=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto
=== Module description ===
This module illustrates a simple unit test for our binary_search function.
"""
from search import binary_search


def test_search() -> None:
    """Simple test for binary_search."""
    assert binary_search(..., ...) == ...


if __name__ == '__main__':
    import pytest

pytest.main(['test_search.py'])

# def bin_search(lst: list[object], val: object):
#     """
#     Binary searches a list <lst> for a val <val>
#
#     Preconditions
#      - lst = sorted(list)
#      -
#
#     >>> bin_search([1, 2, 3], 2)
#     1
#     >>> bin_search([1, 2, 3], -1)
#     -1
#     """
#     p1, p2 = 0, len(lst) - 1
#
#     if lst[p1] > val or lst[p2] < val:
#         return -1
#     if lst[p1] == val:
#         return p1
#     elif lst[p2] == val:
#         return p2
#
#     while p1 < p2 - 1:
#         midpt = int((p1 + p2) / 2)
#
#         if lst[midpt] == val:
#             return midpt
#         elif lst[midpt] < val:
#             p1 = midpt
#         else:
#             p2 = midpt
#
#     return -1
#
#
# if __name__ == "__main__":
#     with open("names.txt") as f:
#         vals = sorted([i.strip() for i in f])
#
#     print(bin_search(vals, "blah2"))
#     print(bin_search(vals, "blah3"))
#     print(bin_search(vals, "hello"))
#     print(bin_search(vals, "world"))
#     print(bin_search(vals, "blah"))
#     print(bin_search(vals, "afdaf"))
#
#
