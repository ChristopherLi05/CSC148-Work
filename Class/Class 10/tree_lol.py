class Tree:
    def __init__(self, root, subtrees):
        self._root = root
        self._subtrees: list[Tree] = subtrees

    def is_empty(self):
        return self._root is None

    def leaves(self):
        if self.is_empty():
            return []
        elif not self._subtrees:
            return [self]
        else:
            return [j for i in self._subtrees for j in i.leaves()]

    def delete_root_promote(self):
        if self._subtrees:
            temp = self._subtrees.pop()
            self._root = temp._root
            self._subtrees.extend(temp._subtrees)

    def delete_root_leaf(self):
        temp = self.find_leftmost_leaf_parent()
        leaf = temp._subtrees.pop(0)

        self._root = leaf._root

    def find_leftmost_leaf_parent(self):
        if not self._subtrees[0]._subtrees:
            return self
        return self._subtrees[0].find_leftmost_leaf_parent()


class Foo:
    @staticmethod
    def foo():
        print("hello")

        Foo.bar()

    # foo()

    @staticmethod
    def bar():
        print("world")


Foo.foo()
