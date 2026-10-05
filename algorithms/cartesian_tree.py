from typing import List, Optional, Any

class CartesianNode:
    def __init__(self, val: Any, idx: int):
        self.val = val
        self.idx = idx
        self.left: Optional['CartesianNode'] = None
        self.right: Optional['CartesianNode'] = None

class CartesianTree:
    """
    Cartesian Tree built in linear O(N) time using a monotonic stack.
    Maintains two properties:
    1. In-order traversal of nodes visits them in original array index order.
    2. Min-heap property: parent's value <= child's value.
    """

    def __init__(self, arr: List[Any]):
        if not arr:
            raise ValueError("Array cannot be empty.")
        self.arr = arr
        self.root = self._build(arr)

    def _build(self, arr: List[Any]) -> CartesianNode:
        stack: List[CartesianNode] = []

        for idx, val in enumerate(arr):
            node = CartesianNode(val, idx)
            last_popped: Optional[CartesianNode] = None

            while stack and stack[-1].val > val:
                last_popped = stack.pop()

            node.left = last_popped
            if stack:
                stack[-1].right = node

            stack.append(node)

        # The bottom-most element of stack is the root (minimum element of array)
        return stack[0]

    def inorder(self) -> List[Any]:
        """Returns in-order traversal of values (should equal original array)."""
        res = []
        def _dfs(node: Optional[CartesianNode]):
            if node:
                _dfs(node.left)
                res.append(node.val)
                _dfs(node.right)
        _dfs(self.root)
        return res

    def is_valid_min_heap(self) -> bool:
        """Verifies min-heap property across all nodes."""
        def _check(node: Optional[CartesianNode]) -> bool:
            if node is None:
                return True
            if node.left and node.left.val < node.val:
                return False
            if node.right and node.right.val < node.val:
                return False
            return _check(node.left) and _check(node.right)

        return _check(self.root)
