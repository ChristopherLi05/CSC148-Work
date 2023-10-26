"""CSC148 Lab 7: Recursion

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few nested list functions for you to practice recursion.
"""
from python_ta.contracts import check_contracts


@check_contracts
def greater_than_all(obj: int | list, n: int) -> bool:
    """Return True iff there is no int in <obj> that is larger than or
    equal to <n> (or, equivalently, <n> is greater than all ints in <obj>).

    >>> greater_than_all(10, 3)
    False
    >>> greater_than_all([1, 2, [1, 2], 4], 10)
    True
    >>> greater_than_all([], 0)
    True
    """
    if isinstance(obj, int):
        return obj < n
    else:
        # for i in obj:
        #     if not greater_than_all(i, n):
        #         return False
        # return True

        return all(greater_than_all(i, n) for i in obj)


@check_contracts
def add_n(obj: int | list, n: int) -> int | list:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    if isinstance(obj, int):
        return obj + n
    else:
        return [add_n(i, n) for i in obj]


@check_contracts
def nested_list_equal(obj1: int | list, obj2: int | list) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.
    You should only use == in the base case. Do NOT use it to compare
    otherwise (as that defeats the purpose of this exercise)!

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    if (isinstance(obj1, int) and isinstance(obj2, list)) or (
            isinstance(obj1, list) and isinstance(obj2, int)):
        return False
    # implies obj2 is also int
    elif isinstance(obj1, int):
        return obj1 == obj2
    # implies obj1, obj2 is list
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        return all(map(lambda x: nested_list_equal(*x), zip(obj1, obj2)))


@check_contracts
def duplicate(obj: int | list) -> list:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    Note: this function is always guaranteed to return a list (so the return type
    annotation is just "list" instead of "int | list").

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    if isinstance(obj, int):
        return [obj, obj]
    else:
        to_return = []
        for i in obj:
            if isinstance(i, int):
                to_return += [i, i]
            else:
                to_return += [duplicate(i)]
        return to_return


if __name__ == '__main__':
    # import doctest

    # doctest.testmod()

    import python_ta

    python_ta.check_all(
        config={'max-line-length': 100, "output-format": "python_ta.reporters.PlainReporter"
                })
