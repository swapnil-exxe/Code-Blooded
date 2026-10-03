import math
from typing import Optional, List, Any, Tuple

class ScapegoatNode:
    def __init__(self, key: Any):
        self.key = key
        self.left: Optional['ScapegoatNode'] = None
        self.right: Optional['ScapegoatNode'] = None

class ScapegoatTree:
    """
    Scapegoat Tree self-balancing binary search tree.
    Does not require storing overhead balance or height values per node.
    Maintains alpha-weight balance property with amortized O(log N) operations.
    """

    def __init__(self, alpha: float = 2.0 / 3.0):
        if not (0.5 <= alpha < 1.0):
            raise ValueError("alpha must be in [0.5, 1.0).")
        self.alpha = alpha
        self.root: Optional[ScapegoatNode] = None
        self.n = 0      # Current number of nodes
        self.max_n = 0  # High watermark for node count since last rebuild

    def _size(self, node: Optional[ScapegoatNode]) -> int:
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def _flatten(self, node: Optional[ScapegoatNode], nodes: List[ScapegoatNode]) -> None:
        if node is None:
            return
        self._flatten(node.left, nodes)
        nodes.append(node)
        self._flatten(node.right, nodes)

    def _build_balanced(self, nodes: List[ScapegoatNode], start: int, end: int) -> Optional[ScapegoatNode]:
        if start > end:
            return None
        mid = (start + end) // 2
        mid_node = nodes[mid]
        mid_node.left = self._build_balanced(nodes, start, mid - 1)
        mid_node.right = self._build_balanced(nodes, mid + 1, end)
        return mid_node

    def _rebuild(self, u: ScapegoatNode) -> ScapegoatNode:
        nodes: List[ScapegoatNode] = []
        self._flatten(u, nodes)
        return self._build_balanced(nodes, 0, len(nodes) - 1)

    def search(self, key: Any) -> bool:
        curr = self.root
        while curr is not None:
            if key == curr.key:
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def insert(self, key: Any) -> None:
        new_node = ScapegoatNode(key)
        if self.root is None:
            self.root = new_node
            self.n = 1
            self.max_n = 1
            return

        curr = self.root
        depth = 0
        path = []

        while curr is not None:
            path.append(curr)
            depth += 1
            if key < curr.key:
                if curr.left is None:
                    curr.left = new_node
                    break
                curr = curr.left
            elif key > curr.key:
                if curr.right is None:
                    curr.right = new_node
                    break
                curr = curr.right
            else:
                # Key already exists
                return

        path.append(new_node)
        depth += 1
        self.n += 1
        self.max_n = max(self.max_n, self.n)

        # Check if depth exceeds h_alpha = floor(log_{1/alpha}(n))
        h_alpha = math.floor(math.log(self.n, 1.0 / self.alpha)) if self.n > 0 else 0
        if depth > h_alpha:
            # Find scapegoat node on the path
            scapegoat = None
            scapegoat_parent = None
            for i in range(len(path) - 1, 0, -1):
                parent = path[i - 1]
                child = path[i]
                child_size = self._size(child)
                parent_size = self._size(parent)
                if child_size > self.alpha * parent_size:
                    scapegoat = parent
                    scapegoat_parent = path[i - 2] if i >= 2 else None

            if scapegoat is not None:
                rebuilt_sub = self._rebuild(scapegoat)
                if scapegoat_parent is None:
                    self.root = rebuilt_sub
                elif scapegoat_parent.left == scapegoat:
                    scapegoat_parent.left = rebuilt_sub
                else:
                    scapegoat_parent.right = rebuilt_sub

    def delete(self, key: Any) -> bool:
        def _delete_node(node: Optional[ScapegoatNode], k: Any) -> Tuple[Optional[ScapegoatNode], bool]:
            if node is None:
                return None, False

            deleted = False
            if k < node.key:
                node.left, deleted = _delete_node(node.left, k)
            elif k > node.key:
                node.right, deleted = _delete_node(node.right, k)
            else:
                deleted = True
                if node.left is None:
                    return node.right, True
                elif node.right is None:
                    return node.left, True
                else:
                    succ = node.right
                    while succ.left is not None:
                        succ = succ.left
                    node.key = succ.key
                    node.right, _ = _delete_node(node.right, succ.key)

            return node, deleted

        self.root, deleted = _delete_node(self.root, key)
        if deleted:
            self.n -= 1
            if self.n < self.alpha * self.max_n and self.root is not None:
                self.root = self._rebuild(self.root)
                self.max_n = self.n

        return deleted

    def inorder(self) -> List[Any]:
        nodes: List[ScapegoatNode] = []
        self._flatten(self.root, nodes)
        return [node.key for node in nodes]
