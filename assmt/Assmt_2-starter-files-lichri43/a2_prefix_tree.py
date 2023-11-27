"""CSC148 Assignment 2: Autocompleter classes

=== CSC148 Fall 2023 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This file contains the definition of an Abstract Data Type (Autocompleter) and two
implementations of this interface, SimplePrefixTree and CompressedPrefixTree.
You'll complete both of these subclasses over the course of this assignment.

As usual, be sure not to change any parts of the given *public interface* in the
starter code---and this includes the instance attributes, which we will be
testing directly! You may, however, add new private attributes, methods, and
top-level functions to this file.
"""
from __future__ import annotations
from typing import Any
from python_ta.contracts import check_contracts


################################################################################
# The Autocompleter ADT
################################################################################
class Autocompleter:
    """An abstract class representing the Autocompleter Abstract Data Type.
    """

    def __len__(self) -> int:
        """Return the number of values stored in this Autocompleter."""
        raise NotImplementedError

    def insert(self, value: Any, weight: float, prefix: list) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence
        """
        raise NotImplementedError

    def autocomplete(self, prefix: list,
                     limit: int | None = None) -> list[tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        sorted by non-increasing weight. You can decide how to break ties.

        If limit is None, return *every* match for the given prefix.

        Preconditions:
        - limit is None or limit > 0
        """
        raise NotImplementedError

    def remove(self, prefix: list) -> None:
        """Remove all values that match the given prefix.
        """
        raise NotImplementedError


################################################################################
# SimplePrefixTree (Tasks 1-3)
################################################################################
@check_contracts
class SimplePrefixTree(Autocompleter):
    """A simple prefix tree.

    Instance Attributes:
    - root:
        The root of this prefix tree.
        - If this tree is empty, <root> equals [].
        - If this tree is a leaf, <root> represents a value stored in the Autocompleter
          (e.g., 'cat').
        - If this tree is not a leaf and non-empty, <root> is a list representing a prefix
          (e.g., ['c', 'a']).
    - subtrees:
        A list of subtrees of this prefix tree.
    - weight:
        The weight of this prefix tree.
        - If this tree is empty, this equals 0.0.
        - If this tree is a leaf, this stores the weight of the value stored in the leaf.
        - If this tree is not a leaf and non-empty, this stores the *total weight* of
          the leaf weights in this tree.

    Representation invariants:
    - self.weight >= 0

    - (EMPTY TREE):
        If self.weight == 0.0, then self.root == [] and self.subtrees == [].
        This represents an empty prefix tree.
    - (LEAF):
        If self.subtrees == [] and self.weight > 0, then this tree is a leaf.
        (self.root is a value that was inserted into this tree.)
    - (NON-EMPTY, NON-LEAF):
        If self.subtrees != [], then self.root is a list (representing a prefix),
        and self.weight is equal to the sum of the weights of all leaves in self.

    - self.subtrees does not contain any empty prefix trees.
    - self.subtrees is *sorted* in non-increasing order of weight.
      (You can break ties any way you like.)
      Note that this applies to both leaves and non-leaf subtrees:
      both can appear in the same self.subtrees list, and both have a weight
      attribute.
    """
    root: Any
    weight: float
    subtrees: list[SimplePrefixTree]

    ###########################################################################
    # Part 1(a)
    ###########################################################################
    def __init__(self) -> None:
        """Initialize an empty simple prefix tree.
        """
        self.root = []
        self.weight = 0.0
        self.subtrees = []

    def is_empty(self) -> bool:
        """Return whether this simple prefix tree is empty."""
        #     - (EMPTY TREE):
        #         If self.weight == 0.0, then self.root == [] and self.subtrees == [].
        #         This represents an empty prefix tree.

        return bool(self.weight == 0 and not self.root and not self.subtrees)

    def is_leaf(self) -> bool:
        """Return whether this simple prefix tree is a leaf."""
        #     - (LEAF):
        #         If self.subtrees == [] and self.weight > 0, then this tree is a leaf.
        #         (self.root is a value that was inserted into this tree.)

        return bool(not self.subtrees and self.weight > 0)

    def __len__(self) -> int:
        """Return the number of LEAF values stored in this prefix tree.

        Note that this is a different definition than how we calculate __len__
        of regular trees from lecture!
        """
        return self.is_leaf() + sum(map(len, self.subtrees))

    ###########################################################################
    # Extra helper methods
    ###########################################################################
    def __str__(self) -> str:
        """Return a string representation of this prefix tree.

        You may find this method helpful for debugging. You should not change this method
        (nor the helper _str_indented).
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this prefix tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + f'{self.root} ({self.weight})\n'
            for subtree in self.subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def insert(self, value: Any, weight: float, prefix: list) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence
        """
        if prefix == self.root:
            for i in self.subtrees:
                if i.is_leaf() and i.root == value:
                    # Weight addition
                    i.weight += weight
                    break
            else:
                pt = SimplePrefixTree()
                pt.root, pt.weight = value, weight
                self.subtrees.append(pt)

            # Weight addition
            self.weight += weight
        else:
            prefix_to_find = prefix[:len(self.root) + 1]
            for i in self.subtrees:
                if i.root == prefix_to_find:
                    i.insert(value, weight, prefix)
                    break
            else:
                pt = SimplePrefixTree()
                pt.root = prefix_to_find
                self.subtrees.append(pt)

                pt.insert(value, weight, prefix)

            # Weight addition - repeated to separate the cases better
            self.weight += weight

    def autocomplete(self, prefix: list, limit: int | None = None) -> list[tuple[Any, float]]:
        """Return up to <limit> matches for the given prefix.

        The return value is a list of tuples (value, weight), and must be
        sorted by non-increasing weight. You can decide how to break ties.

        If limit is None, return *every* match for the given prefix.

        Preconditions:
        - limit is None or limit > 0
        """
        to_return = []
        sorted_nodes = sorted(self.subtrees, key=lambda x: x.weight)

        while sorted_nodes and (limit is None or limit > 0):
            node = sorted_nodes.pop()

            if node.is_leaf():
                # Cuts our root to the length of the prefix
                #  - longer roots are fine but shorter roots are not
                if self.root[:len(prefix)] == prefix:
                    to_return.append((node.root, node.weight))
                    if limit:
                        limit -= 1
            elif node.root[:len(prefix)] == prefix[:len(node.root)]:
                # Cuts root and prefix to the shortest and compares them
                # If root shorter than prefix, then we want to try and autocomplete on it since
                #     there may be an auto-completable pattern lower on the tree
                # If prefix is shorter than route, then we know that this should autocomplete

                temp = node.autocomplete(prefix, limit)

                to_return += temp
                if limit:
                    limit -= len(temp)

        return sorted(to_return, key=lambda x: x[1], reverse=True)

    def remove(self, prefix: list) -> None:
        """Remove all values that match the given prefix.
        """
        if prefix == self.root:
            self.subtrees = []
            self.weight = 0.0
            self.root = []
        else:
            # Creating a new list so we can modify self.subtrees without doing weird stuff
            for node in list(self.subtrees):
                if node.is_leaf():
                    continue
                elif node.root[:len(prefix)] == prefix:
                    # node.root starts with prefix

                    self.weight -= node.weight
                    self.subtrees.remove(node)
                elif prefix[:len(node.root)] == node.root:
                    # prefix starts with node.root

                    old_weight = node.weight
                    node.remove(prefix)
                    new_weight = node.weight

                    # Node is empty so get rid of it
                    if not node.subtrees:
                        self.subtrees.remove(node)

                    # Difference is removed weight
                    self.weight -= (old_weight - new_weight)

            # Removing Root Node on Compressed Tree
            # This method should never be called on a leaf node
            if not self.subtrees:
                self.root = []
                self.weight = 0.0


################################################################################
# CompressedPrefixTree (Part 6)
################################################################################
@check_contracts
class CompressedPrefixTree(SimplePrefixTree):
    """A compressed prefix tree implementation.

    While this class has the same public interface as SimplePrefixTree,
    (including the initializer!) this version follows the definitions
    described in Part 6 of the assignment handout, which reduces the number of
    tree objects used to store values in the tree.

    Representation Invariants:
    - (NEW) This tree does not contain any compressible internal values.
    """
    subtrees: list[CompressedPrefixTree]  # Note the different type annotation

    def insert(self, value: Any, weight: float, prefix: list) -> None:
        """Insert the given value into this Autocompleter.

        The value is inserted with the given weight, and is associated with
        the prefix sequence <prefix>.

        If the value has already been inserted into this autocompleter
        (compare values using ==), then the given weight should be *added* to
        the existing weight of this value.

        Preconditions:
        - weight > 0
        - the given value is either:
            1) not in this Autocompleter, or
            2) was previously inserted with the SAME prefix sequence
        """
        if not self.root and not self.subtrees:
            # The tree is empty so we can just put the value in
            self.root = prefix
            self.weight += weight

            leaf = CompressedPrefixTree()
            leaf.root, leaf.weight = value, weight
            self.subtrees.append(leaf)
        elif not self.root:
            # The tree is not empty but the root is [], we can just call _insert

            self._insert(value, weight, prefix)
        else:
            # I coded _insert to think that the root node is []
            # This is not always the case with CompressedPrefixTree, so this spoofs it

            temp_self = CompressedPrefixTree()
            temp_self.root, temp_self.weight, temp_self.subtrees = \
                self.root, self.weight, self.subtrees

            self.root, self.subtrees = [], [temp_self]

            self._insert(value, weight, prefix)

            # If we didn't add a new child node then we can compress
            if len(self.subtrees) == 1:
                self.root, self.weight, self.subtrees = \
                    self.subtrees[0].root, self.subtrees[0].weight, self.subtrees[0].subtrees

    def _insert(self, value: Any, weight: float, prefix: list) -> None:
        """
        Internal method to insert the given value into this Autocompleter.

        This method assumes we started at the root and that root = []

        This has the same preconditions as CompressedPrefixTree.insert
        """
        if self.root == prefix:  # Prefix is the same
            for i in self.subtrees:
                if i.is_leaf() and i.root == value:
                    # Weight addition
                    i.weight += weight
                    break
            else:
                pt = CompressedPrefixTree()
                pt.root, pt.weight = value, weight
                self.subtrees.append(pt)

            # Weight addition
            self.weight += weight
        elif node := self._find_prefix_exists(prefix):  # We have a node that prefixes the prefix
            node._insert(value, weight, prefix)

            # Weight addition
            self.weight += weight
        elif vals := self._find_closest_match(prefix):  # We can split a node
            node, match = vals

            self.subtrees.remove(node)

            st_p = CompressedPrefixTree()
            st_p.root, st_p.weight = match, node.weight

            st_p.subtrees.append(node)
            self.subtrees.append(st_p)

            # Being lazy, fallback to else case
            st_p._insert(value, weight, prefix)

            # Weight addition
            self.weight += weight
        else:  # We have to create a new node
            st1 = CompressedPrefixTree()
            st1.root, st1.weight = prefix, weight

            st2 = CompressedPrefixTree()
            st2.root, st2.weight = value, weight

            st1.subtrees.append(st2)
            self.subtrees.append(st1)
            # Weight addition
            self.weight += weight

    def _find_prefix_exists(self, prefix: list[Any]) -> CompressedPrefixTree | None:
        """
        Checks to see if there's a prefix of this prefix in the tree already.
        If this returns something, we do not have to split any node

        Returns the node if found, otherwise return None
        """
        for i in self.subtrees:
            if prefix[:len(i.root)] == i.root:
                return i
        return None

    def _find_closest_match(self, prefix: list) -> tuple[CompressedPrefixTree, list] | None:
        """
        Tries to find the closest match in the tree.
        If this returns something, we need to split a node

        Returns [node, prefix_in_common] if found, otherwise return None

        Preconditions:
         - prefix != []
        """

        for i in self.subtrees:
            if i.is_leaf():
                continue

            # This method should ALWAYS be called after CompressedPrefixTree._find_prefix_exists
            # Rationale is that we know that there aren't any prefixes in the tree, (i.e. there
            # aren't any things like [a, b, c] as a subtree root when the prefix is [a, b, c, d, e]
            # We are doing len(self.root) because we KNOW that subtrees's root will always be at
            # least 1 bigger than the root's length, so this should never error out
            # When we check this value, if these are the same that means they share *more* letters
            # then this node's root, so we can group them together! This will be the only one with
            # this property since we would've grouped any others if we had any
            if i.root[len(self.root)] == prefix[len(self.root)]:
                counter = 0
                for j in range(min(len(i.root), len(prefix))):
                    if i.root[j] == prefix[j]:
                        counter += 1
                    else:
                        break

                return i, prefix[:counter]
        return None


if __name__ == '__main__':
    # ...
    #
    # words = ["car", "cat", "cart", "care", "danger", "door"]
    #
    # orig = CompressedPrefixTree()
    # for i in words:
    #     orig.insert(i, 1.0, list(i))
    #
    # print(orig.check_weight())
    #
    # orig.remove(["c", "a"])
    #
    # print(orig.check_weight())

    # t = CompressedPrefixTree()
    #
    # t.insert("car", 1.0, ["c", "a", "r"])
    # print(t)
    # t.insert("cart", 1.0, ["c", "a", "r", "t"])
    # print(t)

    # import doctest
    #
    # doctest.testmod()

    # Uncomment the python_ta lines below and run this module.
    # This is different that just running doctests! To run this file in PyCharm,
    # right-click in the file and select "Run a2_prefix_tree" or
    # "Run File in Python Console".
    #
    # python_ta will check your work and open up your web browser to display
    # its report. For full marks, you must fix all issues reported, so that
    # you see "None!" under both "Code Errors" and "Style and Convention Errors".
    # TIP: To quickly uncomment lines in PyCharm, select the lines below and press
    # "Ctrl + /" or "⌘ + /".
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 100,
        'max-nested-blocks': 4,
        "output-format": "python_ta.reporters.PlainReporter"
    })
