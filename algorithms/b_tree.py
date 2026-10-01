from typing import List, Optional, Any

class BTreeNode:
    def __init__(self, leaf: bool = True):
        self.leaf = leaf
        self.keys: List[Any] = []
        self.children: List['BTreeNode'] = []

class BTree:
    """
    B-Tree self-balancing search tree data structure.
    t: Minimum degree (every non-root node must contain at least t-1 keys; max 2t-1 keys).
    """

    def __init__(self, t: int = 3):
        if t < 2:
            raise ValueError("B-Tree minimum degree t must be at least 2.")
        self.t = t
        self.root = BTreeNode(leaf=True)

    def search(self, key: Any, node: Optional[BTreeNode] = None) -> bool:
        """Searches for key in B-Tree in O(log N) time."""
        curr = node if node is not None else self.root

        i = 0
        while i < len(curr.keys) and key > curr.keys[i]:
            i += 1

        if i < len(curr.keys) and curr.keys[i] == key:
            return True

        if curr.leaf:
            return False

        return self.search(key, curr.children[i])

    def insert(self, key: Any) -> None:
        """Inserts key into B-Tree maintaining B-Tree invariants."""
        root = self.root

        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(self.root, key)
        else:
            self._insert_non_full(root, key)

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent: BTreeNode, i: int) -> None:
        t = self.t
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)

        # y has 2t-1 keys. Median is at index t-1.
        median_key = y.keys[t - 1]

        # z receives last t-1 keys of y (indices t to 2t-2)
        z.keys = y.keys[t:]
        # y retains first t-1 keys (indices 0 to t-2)
        y.keys = y.keys[:t - 1]

        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        parent.children.insert(i + 1, z)
        parent.keys.insert(i, median_key)

    def traverse(self, node: Optional[BTreeNode] = None) -> List[Any]:
        """Returns in-order traversal of keys in sorted order."""
        curr = node if node is not None else self.root
        res = []

        def _dfs(n: BTreeNode):
            for i in range(len(n.keys)):
                if not n.leaf:
                    _dfs(n.children[i])
                res.append(n.keys[i])
            if not n.leaf:
                _dfs(n.children[len(n.keys)])

        _dfs(curr)
        return res
