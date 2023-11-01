class Tree:
    def __init__(self, root, subtrees):
        self._root = root
        self._subtrees = subtrees

    def is_empty(self):
        return self._root is None

    def leaves(self):
        if self.is_empty():
            return []
        elif not self._subtrees:
            return [self]
        else:
            return [j for i in self._subtrees for j in i.leaves()]
