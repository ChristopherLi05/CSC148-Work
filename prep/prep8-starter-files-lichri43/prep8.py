"""CSC148 Prep 8: Trees

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
Your task in this prep is to implement each of the unimplemented Tree methods
in this file.

The starter code has a recursive template that treats both the "empty tree"
and the "size-one" tree ("leaf") as base cases. You may not need both of these
base cases -- it depends on the method you are writing. You can simplify your
code by removing redundant cases from the provided recursive template, but
are not required to do so.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


@check_contracts
class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Attributes:
    - _root:
        The item stored at this tree's root, or None if the tree is empty.
    - _subtrees:
        The list of all subtrees of this tree.

    Representation Invariants:
    - (self._root is None and self._subtrees == []) or self._root is not None
        # i.e. If self._root is None then self._subtrees is an empty list.
        # This setting of attributes represents an empty Tree.

    Note: self._subtrees may be empty when self._root is not None.
    This setting of attributes represents a tree consisting of just one
    node (a 'leaf')
    """
    _root: Any | None
    _subtrees: list[Tree]

    def __init__(self, root: Any | None, subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Preconditions:
            - (root is None and subtrees == []) or root is not None
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree) here
            return size

    def num_negatives(self) -> int:
        """Return the number of negative integers in this tree.

        Precondition: all items in this tree are integers.

        Remember, 0 is *not* negative.

        >>> t1 = Tree(17, [])
        >>> t1.num_negatives()
        0
        >>> t2 = Tree(-10, [])
        >>> t2.num_negatives()
        1
        >>> t3 = Tree(-11, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t3.num_negatives()
        3
        """
        if self.is_empty():
            return 0
        else:
            return (self._root < 0) + sum([i.num_negatives() for i in self._subtrees])

    def maximum(self: Tree) -> int:
        """Return the maximum item stored in this tree.

        Return 0 if this tree is empty.

        Precondition: all values in this tree are positive integers.

        >>> t1 = Tree(17, [])
        >>> t1.maximum()
        17
        >>> t3 = Tree(1, [Tree(22, []), Tree(100, []), Tree(30, [])])
        >>> t3.maximum()
        100
        >>> t1 = Tree(-17, [])
        >>> t1.maximum()
        -17
        """
        if self.is_empty():
            return 0
        else:
            return max([i.maximum() for i in self._subtrees] + [self._root])

    def height(self: Tree) -> int:
        """Return the height of this tree.

        Please refer to the prep readings for the definition of tree height.

        >>> t1 = Tree(17, [])
        >>> t1.height()
        1
        >>> t2 = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t2.height()
        2
        >>> t3 = Tree(1, [Tree(-2, []), Tree(10, [Tree(5, [])]), Tree(-30, [])])
        >>> t3.height()
        3
        >>> t3 = Tree(1, [Tree(-2, []), Tree(10, [Tree(5, [Tree(None, [])])]), Tree(-30, [])])
        >>> t3.height()
        3
        """
        if self.is_empty():
            return 0
        else:
            return max([i.height() for i in self._subtrees] + [0]) + 1

    def __contains__(self, item: Any) -> bool:
        """Return whether this tree contains <item>.

        >>> t = Tree(1, [Tree(-2, []), Tree(10, []), Tree(-30, [])])
        >>> t.__contains__(-30)  # Could also write -30 in t.
        True
        >>> t.__contains__(148)
        False
        """
        if self.is_empty():
            return False
        else:
            return (self._root == item) or any(item in i for i in self._subtrees)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        "output-format": "python_ta.reporters.PlainReporter"
    })
