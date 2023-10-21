"""CSC148 Prep 4: Abstract Data Types
=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto
=== Module Description ===
This module contains four functions for you to implement, where each
operates on either a stack or a queue.
We've provided deliberately confusing implementations of these ADTs in
adts.py. This is because we don't want you to care at all about the
implementations of these classes, but instead ONLY use the public methods
defined in by the Stack or Queue ADTs. These are the following:
    Stack
        - is_empty()
        - push()
        - pop()
    Queue
        - is_empty()
        - enqueue()
        - dequeue()
In particular, this means that you shouldn't try to access any attributes
of either class, since the ADT descriptions only define what *operations*
(methods) can be used for the ADTs.
GENERAL HINT: save values in local variables! Even if you pop an item off of
a stack, it's not "gone forever" if you assign it to a variable.
"""
from typing import Any
from python_ta.contracts import check_contracts
from adts import Stack, Queue


################################################################################
# Part 1
# In this part of the prep, you will various Stack and Queue functions.
#
# You must NOT access any attributes of the Stack/Queues passed into each
# function.
#
# You may ONLY use the is_empty(), push(), and pop() methods of Stack, and
# the is_empty(), enqueue(), and dequeue() methods of Queue.
################################################################################
@check_contracts
def peek(stack: Stack) -> Any | None:
    """Return the top item on <stack>.
    If the stack is empty, return None.
    Unlike Stack.pop, this function should leave the stack unchanged when the
    function ends. You can (and should) still call pop and push, just make
    sure that if you take any items off the stack, you put them back on!
    >>> my_stack = Stack()
    >>> my_stack.push(1)
    >>> my_stack.push(2)
    >>> peek(my_stack)
    2
    >>> my_stack.pop()
    2
    """

    if stack.is_empty():
        return None

    stack.push(a := stack.pop())
    return a
@check_contracts
def reverse_top_two(my_stack: Stack) -> None:
    """Reverse the top two elements on <stack>.
    Precondition: <stack> has at least two items.
    >>> my_stack = Stack()
    >>> my_stack.push(1)
    >>> my_stack.push(2)
    >>> reverse_top_two(my_stack)
    >>> my_stack.pop()
    1
    >>> my_stack.pop()
    2
    >>> my_stack.is_empty()
    True
    """
    a, b = [my_stack.pop() for i in range(2)]
    my_stack.push(a)
    my_stack.push(b)
@check_contracts
def remove_all(queue: Queue) -> None:
    """Remove all items from <queue>.
    >>> my_queue = Queue()
    >>> my_queue.enqueue(1)
    >>> my_queue.enqueue(2)
    >>> my_queue.enqueue(3)
    >>> remove_all(my_queue)
    >>> my_queue.is_empty()
    True
    """
    while not queue.is_empty():
        queue.dequeue()
@check_contracts
def remove_all_but_one(queue: Queue) -> None:
    """Remove all items from the given queue except the last one.
    Precondition: not queue.is_empty() # <queue> contains at least one item.
    >>> my_queue = Queue()
    >>> my_queue.enqueue(1)
    >>> my_queue.enqueue(2)
    >>> my_queue.enqueue(3)
    >>> remove_all_but_one(my_queue)
    >>> my_queue.is_empty()
    False
    >>> my_queue.dequeue()
    3
    >>> my_queue.is_empty()
    True
    """

    a = None
    while not queue.is_empty():
        a = queue.dequeue()
    queue.enqueue(a)


################################################################################
# Part 2
# In Part 2 of the prep, we have given you the buggy function add_in_order().
# While the documentation of this function is correct, the implementation is
# not.
#
# In prep4_starter_tests.py, you must write a test case that will fail this
# buggy implementation, but pass on a working version of add_in_order().
#
# You are not required to fix the bug, although you may do so if you'd like.
################################################################################
@check_contracts
def add_in_order(stack: Stack, lst: list) -> None:
    """
    Add all items in <lst> to <stack>, so that when items are removed from
    <stack>, they are returned in <lst> order.
    Precondition: stack.is_empty()
    >>> my_stack = Stack()
    >>> my_lst = [1, 1]
    >>> add_in_order(my_stack, my_lst)
    >>> my_results = []
    >>> my_results.append(my_stack.pop())
    >>> my_results.append(my_stack.pop())
    >>> my_lst == my_results
    True
    >>> my_stack.is_empty()
    True
    """
    # for item in lst:
    #     stack.push(item)

    for item in lst[::-1]:
        stack.push(item)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run prep4" or "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['adts'],
        'max-line-length': 100,
        "output-format": "python_ta.reporters.PlainReporter"
    })