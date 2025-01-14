"""CSC148 Prep 5: Linked Lists

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: David Liu and Diane Horton

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 David Liu and Diane Horton

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

NOTE: There is an additional task in the prep5_starter_tests.py file.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


@check_contracts
class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    Attributes:
    - item:
        The data stored in this node.
    - next:
        The next node in the list, or None if there are no more nodes.
    """
    item: Any
    next: _Node | None

    def __init__(self, item: Any) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


@check_contracts
class LinkedList:
    """A linked list implementation of the List ADT.

    Private Attributes:
    - _first:
        The first node in the linked list, or None if the list is empty.
    """
    _first: _Node | None

    def __init__(self) -> None:
        """Initialize an empty linked list.
        """
        self._first = None

    def print_items(self) -> None:
        """Print out each item in this linked list."""
        curr = self._first
        while curr is not None:
            print(curr.item)
            curr = curr.next

    ##########################################################################
    # Part 1
    #
    # For each of the following linked list methods, read its docstring
    # and the complete its implementation.
    # You should use the provided *linked list traversal* code template
    # as your starting point, but of course you should modify it as necessary!
    #
    # NOTE: the first two methods are new special methods (you can tell by the
    # double underscores), and enable some special Python behaviour that we've
    # illustrated in the doctests.
    #
    # At the bottom of this file, we've included some helpers
    # to create some basic linked lists for our doctests.
    ##########################################################################

    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList()
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = three_items(1, 2, 3)
        >>> len(lst)
        3
        """
        curr = self._first

        count = 0

        while curr is not None:
            count += 1
            curr = curr.next

        return count

    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this list.

        Use == to compare items.

        >>> lst = three_items(1, 2, 3)
        >>> 2 in lst                     # Equivalent to lst.__contains__(2)
        True
        >>> 4 in lst
        False
        """
        curr = self._first
        while curr is not None:
            if item == curr.item:
                return True
            curr = curr.next
        return False

    # HINTS: for this one, you'll be adding a new item to a linked list.
    #   1. Create a new _Node object first.
    #   2. Consider the cases where the list is empty and non-empty separately.
    #   3. For the non-empty case, you'll first need to iterate to the
    #      *last node* in the linked list. (Review this prep's Quercus quiz!)
    def append(self, item: Any) -> None:
        """Append <item> to the end of this list.

        >>> lst = LinkedList()
        >>> lst.append(1)
        >>> lst._first.item
        1
        >>> lst.append(2)
        >>> lst._first.next.item
        2
        """
        curr = self._first
        while curr and curr.next is not None:
            curr = curr.next

        if curr is None:
            self._first = _Node(item)
        else:
            curr.next = _Node(item)


# ------------------------------------------------------------------------
# Helpers for creating linked lists (testing purposes only)
# You may use these to help you construct a LinkedList
# Do NOT change these helper functions.
# ------------------------------------------------------------------------
def one_item(x: Any) -> LinkedList:
    """Return a linked list containing the given item."""
    lst = LinkedList()
    node = _Node(x)
    lst._first = node
    return lst


def three_items(x1: Any, x2: Any, x3: Any) -> LinkedList:
    """Return a linked list containing the given three items."""
    lst = LinkedList()
    node1 = _Node(x1)
    node2 = _Node(x2)
    node3 = _Node(x3)
    node1.next = node2
    node2.next = node3
    lst._first = node1
    return lst


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run prep5" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['LinkedList.print_items'],
        'disable': ['W0212'],
        'max-line-length': 100,
        "output-format": "python_ta.reporters.PlainReporter"
    })
