"""CSC148 Lab 11: More on sorting

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains a mutating implementation of mergesort,
and a skeleton implementation of Timsort that you will work through
during this lab.
"""
from python_ta.contracts import check_contracts


###############################################################################
# Introduction: mutating version of mergesort
###############################################################################
@check_contracts
def mergesort2(lst: list,
               start: int = 0,
               end: int | None = None) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Note: this is a *mutating, in-place* version of mergesort,
    meaning it does not return a new list, but instead sorts the input list.

    When we divide the list into halves, we don't create new lists for each
    half; instead, we simulate this by passing additional parameters (start
    and end) to represent the part of the list we're currently recursing on.
    """
    if end is None:
        end = len(lst)

    if start < end - 1:
        mid = (start + end) // 2
        mergesort2(lst, start, mid)
        mergesort2(lst, mid, end)
        _merge(lst, start, mid, end)


@check_contracts
def _merge(lst: list, start: int, mid: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Precondition: lst[start:mid] and lst[mid:end] are sorted.
    """
    result = []
    left = start
    right = mid
    while left < mid and right < end:
        if lst[left] < lst[right]:
            result.append(lst[left])
            left += 1
        else:
            result.append(lst[right])
            right += 1

    # This replaces lst[start:end] with the correct sorted version.
    lst[start:end] = result + lst[left:mid] + lst[right:end]


###############################################################################
# Task 1: Finding runs
###############################################################################
@check_contracts
def find_runs(lst: list) -> list[tuple[int, int]]:
    """Return a list of tuples indexing the runs of lst.

    Preconditions:
    - lst != []

    >>> find_runs([1, 4, 7, 10, 2, 5, 3, -1])
    [(0, 4), (4, 6), (6, 7), (7, 8)]
    >>> find_runs([0, 1, 2, 3, 4, 5])
    [(0, 6)]
    >>> find_runs([10, 4, -2, 1])
    [(0, 1), (1, 2), (2, 4)]
    """
    runs = []

    # Keep track of the start and end points of a run.
    run_start = 0
    run_end = 1
    while run_end < len(lst):
        if lst[run_end] < lst[run_end - 1]:
            runs.append((run_start, run_end))
            run_start = run_end
        run_end += 1

    runs.append((run_start, run_end))

    return runs


###############################################################################
# Task 2: Merging runs
###############################################################################
@check_contracts
def timsort(lst: list) -> None:
    """Sort <lst> in place.

    # >>> lst = []
    # >>> timsort(lst)
    # >>> lst
    # []
    # >>> lst = [1]
    # >>> timsort(lst)
    # >>> lst
    # [1]
    >>> lst = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> timsort(lst)
    >>> lst
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    if not lst:
        return

    runs = find_runs(lst)

    while len(runs) > 1:
        (_, b), (c, d) = runs.pop(), runs.pop()

        _merge2(lst, c, d, b)
        runs.append((c, b))


def sign(n: int | float) -> int:
    """Returns sign of the number"""
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        return 0


def reverse(lst: list, start: int, end: int) -> None:
    """Reverses the list"""
    lst[start:end] = lst[start:end][::-1]


###############################################################################
# Task 3: Descending runs
###############################################################################
@check_contracts
def find_runs2(lst: list) -> list[tuple[int, int]]:
    """Return a list of tuples indexing the runs of lst.

    Now, a run can be either ascending or descending!

    Preconditions:
    - lst != []

    First set of doctests, just for finding descending runs.
    >>> find_runs2([5, 4, 3, 2, 1])
    [(0, 5)]
    >>> find_runs2([1, 4, 7, 10, 2, 5, 3, -1])
    [(0, 4), (4, 6), (6, 8)]
    >>> find_runs2([0, 1, 2, 3, 4, 5])
    [(0, 6)]
    >>> find_runs2([10, 4, -2, 1])
    [(0, 3), (3, 4)]

    The second set of doctests, to check that descending runs are reversed.
    >>> lst1 = [5, 4, 3, 2, 1]
    >>> find_runs2(lst1)
    [(0, 5)]
    >>> lst1  # The entire run is reversed
    [1, 2, 3, 4, 5]
    >>> lst2 = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> find_runs2(lst2)
    [(0, 4), (4, 6), (6, 8)]
    >>> lst2  # The -1 and 3 are switched
    [1, 4, 7, 10, 2, 5, -1, 3]
    """
    if not lst:
        return []
    elif len(lst) == 1:
        return [(0, 1)]

    runs = []

    direction = sign(lst[1] - lst[0])
    run_start = 0
    run_end = 1

    while run_end < len(lst):
        if direction == 0:
            direction = sign(lst[run_end] - lst[run_end - 1])
        elif sign(lst[run_end] - lst[run_end - 1]) != direction:
            if direction == -1:
                reverse(lst, run_start, run_end)

            runs.append((run_start, run_end))
            run_start = run_end
            direction = 0

        run_end += 1

    runs.append((run_start, run_end))
    if direction == -1:
        reverse(lst, run_start, run_end)

    return runs


###############################################################################
# Task 4: Minimum run length
###############################################################################
MIN_RUN = 64


@check_contracts
def find_runs3(lst: list) -> list[tuple[int, int]]:
    """Same as find_runs2, but each run (except the last one)
    must be of length >= MIN_RUN.

    Precondition: lst is non-empty

    >>> lst2 = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> find_runs3(lst2)
    [(0, 8)]
    >>> lst2
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    if not lst:
        return []
    elif len(lst) == 1:
        return [(0, 1)]

    runs = []
    last_run_start = -1

    direction = sign(lst[1] - lst[0])
    run_start = 0
    run_end = 1

    while run_end < len(lst):
        if direction == 0:
            direction = sign(lst[run_end] - lst[run_end - 1])
        elif sign(lst[run_end] - lst[run_end - 1]) != direction:
            if direction == -1:
                reverse(lst, run_start, run_end)

            if last_run_start == -1:
                last_run_start = run_start

            if run_end - last_run_start >= MIN_RUN:
                last_run_start = -1
                runs.append((last_run_start, run_end))
            else:
                _merge(lst, last_run_start, run_start, run_end)

            direction = 0
            run_start = run_end
        run_end += 1

    if direction == -1:
        reverse(lst, run_start, run_end)

    if last_run_start == -1:
        last_run_start = run_start

    if last_run_start != -1:
        _merge(lst, last_run_start, run_start, run_end)

    runs.append((last_run_start, run_end))

    return runs


@check_contracts
def insertion_sort(lst: list, start: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.
    """
    for i in range(start + 1, end):
        num = lst[i]
        left = start
        right = i
        while right - left > 1:
            mid = (left + right) // 2
            if num < lst[mid]:
                right = mid
            else:
                left = mid + 1

        # insert
        if lst[left] > num:
            lst[left + 1:i + 1] = lst[left:i]
            lst[left] = num
        else:
            lst[right + 1:i + 1] = lst[right:i]
            lst[right] = num


###############################################################################
# Task 5: Optimizing merge
###############################################################################
@check_contracts
def _merge2(lst: list, start: int, mid: int, end: int) -> None:
    """Sort the items in lst[start:end] in non-decreasing order.

    Precondition: lst[start:mid] and lst[mid:end] are sorted.
    """

    temp = lst[start:mid]
    counter = 0

    left = 0
    right = mid

    while left < len(temp) and right < end:
        if temp[left] < lst[right]:
            lst[start + counter] = temp[left]
            left += 1
        else:
            lst[start + counter] = lst[right]
            right += 1
        counter += 1

    lst[start + counter:end] = temp[left:] + lst[right:end]


###############################################################################
# Task 6: Limiting the 'runs' stack
###############################################################################
def find_next_run(lst: list, run_start: int) -> tuple[int, int]:
    """Same as find_runs2, but each run (except the last one)
    must be of length >= MIN_RUN.

    Precondition: lst is non-empty
    """
    if not lst[run_start:]:
        return (0, 0)
    elif len(lst[run_start:]) == 1:
        return (0, 1)

    last_run_start = run_start
    direction = sign(lst[run_start + 1] - lst[run_start])
    run_end = run_start + 1

    while run_end < len(lst):
        if direction == 0:
            direction = sign(lst[run_end] - lst[run_end - 1])
        elif sign(lst[run_end] - lst[run_end - 1]) != direction:
            if direction == -1:
                reverse(lst, run_start, run_end)

            if last_run_start == -1:
                last_run_start = run_start

            if run_end - last_run_start >= MIN_RUN:
                last_run_start = -1
                return (last_run_start, run_end)
            else:
                _merge(lst, last_run_start, run_start, run_end)

            direction = 0
            run_start = run_end
        run_end += 1

    if direction == -1:
        reverse(lst, run_start, run_end)

    if last_run_start == -1:
        last_run_start = run_start

    if last_run_start != -1:
        _merge2(lst, last_run_start, run_start, run_end)

    return (last_run_start, run_end)


@check_contracts
def timsort2(lst: list) -> None:
    """Sort the given list using the version of timsort from Task 6.

    >>> lst = []
    >>> timsort(lst)
    >>> lst
    []
    >>> lst = [1]
    >>> timsort(lst)
    >>> lst
    [1]
    >>> lst = [1, 4, 7, 10, 2, 5, 3, -1]
    >>> timsort(lst)
    >>> lst
    [-1, 1, 2, 3, 4, 5, 7, 10]
    """
    if not lst:
        return

    last_run_end = 0
    runs = []

    while last_run_end < len(lst):
        runs.append(find_next_run(lst, last_run_end))
        last_run_end = runs[-1][1]

        if len(runs) >= 3:
            c, b, a = runs.pop(), runs.pop(), runs.pop()

            if b[1] - b[0] <= c[1] - c[0]:
                _merge2(lst, b[0], b[1], c[1])
                runs.append(a)
                runs.append((b[0], c[1]))
            elif a[1] - a[0] <= b[1] - b[0] + c[1] - c[0]:
                if a[1] - a[0] < c[1] - c[0]:
                    _merge2(lst, a[0], a[1], b[1])
                    runs.append((a[0], b[1]))
                    runs.append(c)
                else:
                    _merge2(lst, b[0], b[1], c[1])
                    runs.append(a)
                    runs.append((b[0], c[1]))
            else:
                runs.append(a)
                runs.append(b)
                runs.append(c)

    while len(runs) > 1:
        (_, b), (c, d) = runs.pop(), runs.pop()

        _merge2(lst, c, d, b)
        runs.append((c, b))


def remove_duplicates(lst: list) -> list:
    """A"""
    to_return = []

    for i in lst:
        if not to_return:
            to_return.append(i)
        elif i != to_return[-1]:
            to_return.append(i)

    return to_return


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={'max-nested-blocks': 6, 'max-branches': 20,
                                'output-format':
                                    'python_ta.reporters.PlainReporter'})
