import random
from typing import Optional, List, Any

class TreapNode:
    """Node in a Treap storing key (BST invariant) and priority (Heap invariant)."""
    def __init__(self, key: Any, priority: Optional[float] = None):
        self.key = key
        self.priority = priority if priority is not None else random.random()
        self.left: Optional['TreapNode'] = None
        self.right: Optional['TreapNode'] = None

class Treap:
    """
    Treap (Tree + Heap) randomized balanced binary search tree data structure.
    Average O(log N) operations for insert, search, delete.
    """

    def __init__(self):
        self.root: Optional[TreapNode] = None

    def _rotate_right(self, y: TreapNode) -> TreapNode:
        x = y.left
        assert x is not None
        y.left = x.right
        x.right = y
        return x

    def _rotate_left(self, x: TreapNode) -> TreapNode:
        y = x.right
        assert y is not None
        x.right = y.left
        y.left = x
        return y

    def insert(self, key: Any, priority: Optional[float] = None) -> None:
        """Inserts key into the Treap maintaining BST and Max-Heap invariants."""
        self.root = self._insert_node(self.root, key, priority)

    def _insert_node(self, node: Optional[TreapNode], key: Any, priority: Optional[float]) -> TreapNode:
        if node is None:
            return TreapNode(key, priority)

        if key < node.key:
            node.left = self._insert_node(node.left, key, priority)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert_node(node.right, key, priority)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)

        return node

    def search(self, key: Any) -> bool:
        """Searches for key in O(log N) expected time."""
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def delete(self, key: Any) -> None:
        """Deletes key from the Treap."""
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, node: Optional[TreapNode], key: Any) -> Optional[TreapNode]:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            elif node.left.priority > node.right.priority:
                node = self._rotate_right(node)
                node.right = self._delete_node(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete_node(node.left, key)

        return node

    def inorder(self) -> List[Any]:
        """Returns in-order traversal of keys (sorted order)."""
        result = []
        def _dfs(node: Optional[TreapNode]):
            if node:
                _dfs(node.left)
                result.append(node.key)
                _dfs(node.right)
        _dfs(self.root)
        return result

    def is_valid_treap(self) -> bool:
        """Helper to verify BST and Max-Heap invariants across the tree."""
        def _check(node: Optional[TreapNode], min_k: Any, max_k: Any) -> bool:
            if node is None:
                return True
            if (min_k is not None and node.key <= min_k) or (max_k is not None and node.key >= max_k):
                return False
            if node.left and node.left.priority > node.priority:
                return False
            if node.right and node.right.priority > node.priority:
                return False
            return _check(node.left, min_k, node.key) and _check(node.right, node.key, max_k)

        return _check(self.root, None, None)
