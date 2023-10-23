from __future__ import annotations
from typing import Any


class _Node:
    """A node in a linked list."""
    item: Any
    next: _Node | None

    def __init__(self, val):
        self.item = val
        self.next = None


class LinkedList:
    """A linked list implementation of the List ADT."""
    _first: _Node | None

    def __init__(self) -> None:
        """Initialize an empty linked list."""
        self._first = None

    def append(self, val):
        if self._first is None:
            self._first = _Node(val)
            return

        curr = self._first
        while curr.next is not None:
            curr = curr.next

        curr.next = _Node(val)

    def insert(self, i, val):
        if i == 0:
            temp = _Node(val)
            temp.next, self._first = self._first, temp
            return

        curr = self._first
        for j in range(i - 1):
            if curr is None:
                break
            curr = curr.next

        if curr is None:
            raise IndexError

        temp = _Node(val)
        temp.next, curr.next = curr.next, temp

    def __getitem__(self, i):
        curr = self._first

        for j in range(i):
            if curr is None:
                break
            curr = curr.next

        if curr is None:
            raise IndexError
        return curr.item
