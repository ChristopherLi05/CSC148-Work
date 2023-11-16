"""CSC148 Lab 9: Binary Search Trees

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains some code for running some timing experiments on
binary search trees.
"""
import random
import sys
from timeit import timeit

import python_ta.contracts

# This disables PythonTA's contract checking (to make the experiment run faster).
# Note: this should be written above the import statement for bst.
python_ta.contracts.ENABLE_CONTRACT_CHECKING = False

from bst import BinarySearchTree

SIZES = [100, 200, 400, 800, 1600]


# ------------------------------------------------------------------------
# Task 3
# ------------------------------------------------------------------------
def insert_delete_all(items: list[int]) -> None:
    """Insert the items in <items> into an empty BinarySearchTree, and then
    remove them in the same order they were added.

    Note: you'll need to first create your own BinarySearchTree here,
    and then call insert and delete on it.
    """
    tree = BinarySearchTree(None)

    for i in items:
        tree.insert(i)

    for i in items:
        tree.delete(i)


def get_items(size: int, is_sorted: bool) -> list[int]:
    """Return a list of <size> items.

    Preconditions:
    - size >= 0

    If is_sorted is True, return the list in sorted order.
    Otherwise, return the list in a *random* order (using random.shuffle).
    """
    items = list(range(size))
    if not is_sorted:
        random.shuffle(items)

    return items


def time_experiment():
    """Run the timing experiment on insert_delete_all for various BST
    sizes and items.

    This function is implemented for you; you should not change it.
    """
    # Limit the depth of recursion to a level greater than is needed
    # for this lab exercise.  This will prevent incorrect code that has
    # infinite recursion from crashing Python. We'll discuss this more in
    # lecture.
    sys.setrecursionlimit(2000)

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from a RANDOMLY ORDERED list of that size.
    random_times = []
    for size in SIZES:
        lst = get_items(size, False)
        time = timeit('insert_delete_all(lst)', number=10, globals={**globals(), 'lst': lst})
        random_times.append(time)
        print(f'Random list of size {size:>7}, time {round(time, 6)}')

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from a SORTED list of that size.
    sorted_times = []
    for size in SIZES:
        lst = get_items(size, True)
        time = timeit('insert_delete_all(lst)', number=10, globals={**globals(), 'lst': lst})
        sorted_times.append(time)
        print(f'Sorted list of size {size:>7}, time {round(time, 6)}')

    return random_times, sorted_times


def plot_experiment():
    """Run the experiment and plot the times in a graph.
    You do not have to change the code below. You may wish to review the timing
    experiment code from Labs 4 and 5.
    """
    import matplotlib.pyplot as plt

    # Run the experiments and store the results
    random_time, sorted_times = time_experiment()

    (start_plt,) = plt.plot(SIZES, random_time, 'ro')
    start_plt.set_label("Random list")

    (end_plt,) = plt.plot(SIZES, sorted_times, 'bo')
    end_plt.set_label("Sorted list")

    plt.legend()
    plt.xlabel("Size")
    plt.ylabel("Average Time (μs)")

    plt.show()


if __name__ == '__main__':
    plot_experiment()
