from typing import List, Optional

class PersistentSegmentNode:
    def __init__(self, val: int = 0, left: Optional['PersistentSegmentNode'] = None, right: Optional['PersistentSegmentNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class PersistentSegmentTree:
    """
    Persistent Segment Tree data structure.
    Creates new root version pointers on point update while sharing unchanged branch nodes.
    Time & Space Complexity: O(log N) per update, O(N) initial build.
    """

    def __init__(self, arr: List[int]):
        if not arr:
            raise ValueError("Array cannot be empty.")

        self.n = len(arr)
        self.roots: List[PersistentSegmentNode] = []
        root0 = self._build(arr, 0, self.n - 1)
        self.roots.append(root0)

    def _build(self, arr: List[int], start: int, end: int) -> PersistentSegmentNode:
        if start == end:
            return PersistentSegmentNode(val=arr[start])

        mid = (start + end) // 2
        left_child = self._build(arr, start, mid)
        right_child = self._build(arr, mid + 1, end)
        return PersistentSegmentNode(val=left_child.val + right_child.val, left=left_child, right=right_child)

    def update(self, version_id: int, idx: int, delta: int) -> int:
        """
        Creates a new version of the tree by adding delta to element at idx in version_id.
        Returns the new version_id index.
        """
        if not (0 <= version_id < len(self.roots)):
            raise IndexError(f"Version {version_id} does not exist.")
        if not (0 <= idx < self.n):
            raise IndexError(f"Index {idx} out of bounds.")

        old_root = self.roots[version_id]
        new_root = self._update_node(old_root, 0, self.n - 1, idx, delta)
        self.roots.append(new_root)
        return len(self.roots) - 1

    def _update_node(self, node: PersistentSegmentNode, start: int, end: int, idx: int, delta: int) -> PersistentSegmentNode:
        if start == end:
            return PersistentSegmentNode(val=node.val + delta)

        mid = (start + end) // 2
        if idx <= mid:
            new_left = self._update_node(node.left, start, mid, idx, delta)
            return PersistentSegmentNode(val=new_left.val + node.right.val, left=new_left, right=node.right)
        else:
            new_right = self._update_node(node.right, mid + 1, end, idx, delta)
            return PersistentSegmentNode(val=node.left.val + new_right.val, left=node.left, right=new_right)

    def query(self, version_id: int, left: int, right: int) -> int:
        """Queries range sum [left, right] inclusive on historical tree version_id."""
        if not (0 <= version_id < len(self.roots)):
            raise IndexError(f"Version {version_id} does not exist.")
        if not (0 <= left <= right < self.n):
            raise IndexError(f"Invalid range [{left}, {right}].")

        root = self.roots[version_id]
        return self._query_node(root, 0, self.n - 1, left, right)

    def _query_node(self, node: Optional[PersistentSegmentNode], start: int, end: int, left: int, right: int) -> int:
        if node is None or left > end or right < start:
            return 0

        if left <= start and end <= right:
            return node.val

        mid = (start + end) // 2
        return self._query_node(node.left, start, mid, left, right) + self._query_node(node.right, mid + 1, end, left, right)
