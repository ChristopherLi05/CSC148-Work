"""CSC148 Prep 10: Recursive Sorting Algorithms

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
Copyright (c) 2021 David Liu and Diane Horton

=== Module Description ===
This file includes the recursive sorting algorithms from this week's prep
readings, and two short programming exercises to extend your learning about
these algorithms in different ways.
"""
from typing import Any
from python_ta.contracts import check_contracts


################################################################################
# Mergesort and Quicksort
################################################################################
@check_contracts
def mergesort(lst: list) -> list:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of mergesort; it does not mutate the
    input list.

    >>> mergesort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Divide the list into two parts, and sort them recursively.
        mid = len(lst) // 2
        left_sorted = mergesort(lst[:mid])
        right_sorted = mergesort(lst[mid:])

        # Merge the two sorted halves. Need a helper here!
        return _merge(left_sorted, right_sorted)


@check_contracts
def _merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Preconditions:
        - sorted(lst1) == lst1
        - sorted(lst2) == lst2
    """
    index1 = 0
    index2 = 0
    merged = []
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] <= lst2[index2]:
            merged.append(lst1[index1])
            index1 += 1
        else:
            merged.append(lst2[index2])
            index2 += 1

    # Now either index1 == len(lst1) or index2 == len(lst2).

    # The remaining elements of the other list
    # can all be added to the end of <merged>.
    # Note that at most ONE of lst1[index1:] and lst2[index2:]
    # is non-empty, but to keep the code simple, we include both.
    return merged + lst1[index1:] + lst2[index2:]


@check_contracts
def quicksort(lst: list) -> list:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of quicksort; it does not mutate the
    input list.

    >>> quicksort([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Pick pivot to be first element.
        # Could make lots of other choices here (e.g., last, random)
        pivot = lst[0]

        # Partition rest of list into two halves
        smaller, bigger = _partition(lst[1:], pivot)

        # Recurse on each partition
        smaller_sorted = quicksort(smaller)
        bigger_sorted = quicksort(bigger)

        # Return! Notice the simple combining step
        return smaller_sorted + [pivot] + bigger_sorted


@check_contracts
def _partition(lst: list, pivot: Any) -> tuple[list, list]:
    """Return a partition of <lst> with the chosen pivot.

    Return two lists, where the first contains the items in <lst>
    that are <= pivot, and the second is the items in <lst> that are > pivot.
    """
    smaller = []
    bigger = []

    for item in lst:
        if item <= pivot:
            smaller.append(item)
        else:
            bigger.append(item)

    return smaller, bigger


################################################################################
# Synthesize exercises
################################################################################
@check_contracts
def mergesort3(lst: list) -> list:
    """Return a sorted version of <lst> using three-way mergesort.

    Three-way mergesort is similar to mergesort, except:
        - it divides the input list into *three* lists of (almost) equal length
        - the main helper merge3 takes in *three* sorted lists, and returns
          a sorted list that contains elements from all of its inputs.

    HINT: depending on your implementation, you might need another base case
    when len(lst) == 2 to avoid an infinite recursion error.

    >>> mergesort3([10, 2, 5, -6, 17, 10])
    [-6, 2, 5, 10, 10, 17]
    >>> mergesort3([0])
    [0]
    >>> mergesort3([1, 0])
    [0, 1]
    >>> mergesort3([2, 1, 0])
    [0, 1, 2]
    >>> import random
    """
    # You must NOT use mergesort, sort, or sorted.
    if len(lst) < 2:  # We've provided the base case for you.
        return lst[:]
    else:
        center = max(len(lst) // 3, 1)
        left_sorted = mergesort3(lst[:center])
        mid_sorted = mergesort3(lst[center: 2 * center])
        right_sorted = mergesort3(lst[2 * center:])

        # Merge the three sorted thirds. Need a helper here!
        return merge3(left_sorted, mid_sorted, right_sorted)


@check_contracts
def merge3(lst1: list, lst2: list, lst3: list) -> list:
    """Return a sorted list with the elements in the given input lists.

    Preconditions:
        - sorted(lst1) == lst1
        - sorted(lst2) == lst2
        - sorted(lst3) == lst3

    This *must* be implemented using the same approach as _merge; in particular,
    it should use indexes to keep track of where you are in each list.
    This will keep your implementation efficient, which we will be checking for.

    You may call _merge in this function, but you should only call it ONCE at most.
    i.e. merge the three lists together and use _merge as needed when
    there's only two lists left to merge.

    Since this involves some detailed work with indexes, we recommend splitting
    up your code into one or more helpers to divide up (and test!) each part
    separately.

    Note that we've made this method public because we'll be testing it directly.
    """
    indexes = [0, 0, 0]
    lsts = [lst1, lst2, lst3]

    merged = []

    while min_lsts := [i for i in range(3) if indexes[i] < len(lsts[i])]:
        min_i = min(min_lsts, key=lambda x: lsts[x][indexes[x]])
        merged.append(lsts[min_i][indexes[min_i]])
        indexes[min_i] += 1

    return merged


@check_contracts
def kth_smallest(lst: list, k: int) -> Any:
    """Return the <k>-th smallest element in <lst>.

    Raise IndexError if k < 0 or k >= len(lst).
    Note: for convenience, k counts from 0, so kth_smallest(lst, 0) == min(lst).

    Preconditions:
        - len(lst) == len(set(lst)) # <lst> does not contain duplicates.

    >>> kth_smallest([10, 20, -4, 3], 0)
    -4
    >>> kth_smallest([10, 20, -4, 3], 2)
    10
    """
    if k >= len(lst) or k < 0:
        raise IndexError

    smaller, bigger = _partition(lst[1:], lst[0])
    if len(smaller) < k:
        return kth_smallest(bigger, k - len(smaller) - 1)
    elif len(smaller) == k:
        return lst[0]
    else:
        return kth_smallest(smaller, k)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run prep10" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(
        config={'max-line-length': 100, 'output-format': 'python_ta.reporters.PlainReporter'})
