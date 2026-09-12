from enum import Enum

class Color(Enum):
    RED = 1
    BLACK = 2

class RBNode:
    """Node in a Red-Black Tree."""
    def __init__(self, key: int, color: Color = Color.RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    """Self-balancing Red-Black Binary Search Tree."""

    def __init__(self):
        self.NIL = RBNode(key=0, color=Color.BLACK)
        self.root = self.NIL

    def insert(self, key: int) -> None:
        """Inserts a key into the Red-Black Tree and fixes color/rotation violations."""
        node = RBNode(key)
        node.left = self.NIL
        node.right = self.NIL
        
        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
            else:
                # Duplicate keys not inserted
                return

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        node.color = Color.RED
        self._fix_insert(node)

    def _fix_insert(self, k: RBNode) -> None:
        while k.parent and k.parent.color == Color.RED:
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == Color.RED:
                    u.color = Color.BLACK
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self._left_rotate(k)
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    self._right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == Color.RED:
                    u.color = Color.BLACK
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self._right_rotate(k)
                    k.parent.color = Color.BLACK
                    k.parent.parent.color = Color.RED
                    self._left_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = Color.BLACK

    def _left_rotate(self, x: RBNode) -> None:
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x: RBNode) -> None:
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def search(self, key: int) -> bool:
        """Returns True if the key exists in the Red-Black Tree."""
        curr = self.root
        while curr != self.NIL:
            if key == curr.key:
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def inorder_traversal(self) -> list[int]:
        """Returns sorted list of keys via in-order traversal."""
        res = []
        self._inorder_helper(self.root, res)
        return res

    def _inorder_helper(self, node: RBNode, res: list[int]) -> None:
        if node != self.NIL:
            self._inorder_helper(node.left, res)
            res.append(node.key)
            self._inorder_helper(node.right, res)

    def verify_properties(self) -> bool:
        """Verifies Red-Black Tree invariant properties."""
        if self.root == self.NIL:
            return True

        # Property 2: Root must be BLACK
        if self.root.color != Color.BLACK:
            return False

        # Verify no consecutive RED nodes & uniform black height
        return self._verify_node(self.root)[0]

    def _verify_node(self, node: RBNode) -> tuple[bool, int]:
        if node == self.NIL:
            return True, 1

        # Property 4: If node is RED, children must be BLACK
        if node.color == Color.RED:
            if node.left.color == Color.RED or node.right.color == Color.RED:
                return False, 0

        left_ok, left_bh = self._verify_node(node.left)
        right_ok, right_bh = self._verify_node(node.right)

        if not left_ok or not right_ok:
            return False, 0

        # Property 5: Equal black height on all root-to-leaf paths
        if left_bh != right_bh:
            return False, 0

        add_bh = 1 if node.color == Color.BLACK else 0
        return True, left_bh + add_bh
