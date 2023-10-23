"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will develop an implementation of the Queue ADT.
It will be helpful to review the stack implementation from lecture.

After you've implemented the Queue, you'll write two different functions that
operate on a queue, paying attention to whether or not the queue should be
modified.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


@check_contracts
class Node:
    used_nodes = []

    def __init__(self, value: Any, prev: Node | None):
        self.value = value
        self.prev = prev
        self.next = None

    def __new__(cls, *args, **kwargs):
        if Node.used_nodes:
            return Node.used_nodes.pop().__init__(*args, **kwargs)
        return super().__new__(cls)

    def mark(self):
        Node.used_nodes.append(self)


@check_contracts
class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the first item added is the one that is removed.

    Private Attributes:
     - head: head node of queue
     - tail: tail node of queue
    """

    # _head: list[Any, list | None, list | None] | None
    # _tail: list[Any, list | None, None] | None

    _tail: Node | None
    _head: Node | None

    _used_nodes: list[Node]

    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._head = None
        self._tail = None
        self._used_nodes = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        return self._head is None

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        if self._head:
            # self._tail[2] = [item, self._tail, None]
            # self._tail = self._tail[2]

            self._tail.next = Node(item, self._tail)
            self._tail = self._tail.next
        else:
            self._head = self._tail = Node(item, None)
            # self._head = self._tail = [item, None, None]

    def dequeue(self) -> Any | None:
        """Remove and return the item at the front of this queue.

        Return None if this Queue is empty.
        (We illustrate a different mechanism for handling an erroneous case.)

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """
        if self._head is None:
            return None
        elif self._head.next is None:
            # elif self._head[2] is None:
            temp = self._head
            self._head = self._tail = None
            return temp[0]
        else:
            temp = self._head
            self._head = self._head.next
            return temp.value

            # self._head = self._head[2]
            # return temp[0]


@check_contracts
def product(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Remove all items from the queue.

    Precondition: integer_queue contains only integers.

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> q.enqueue(6)
    >>> product(q)
    48
    >>> q.is_empty()
    True
    """
    val = 1
    while not integer_queue.is_empty():
        val *= integer_queue.dequeue()

    return val


@check_contracts
def product_star(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Precondition: integer_queue contains only integers.

    >>> primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    >>> prime_line = Queue()
    >>> for prime in primes:
    ...     prime_line.enqueue(prime)
    ...
    >>> product_star(prime_line)
    6469693230
    >>> prime_line.is_empty()
    False
    """
    val = 1
    temp = []
    while not integer_queue.is_empty():
        temp.append(integer_queue.dequeue())
        val *= temp[-1]

    for i in temp:
        integer_queue.enqueue(i)

    return val


if __name__ == '__main__':
    import doctest

    doctest.testmod()
