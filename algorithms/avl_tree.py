class AVLNode:
    """Node in an AVL Tree."""
    def __init__(self, key: int):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

class AVLTree:
    """Self-balancing AVL Binary Search Tree."""

    def get_height(self, node: AVLNode | None) -> int:
        if not node:
            return 0
        return node.height

    def get_balance(self, node: AVLNode | None) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y: AVLNode) -> AVLNode:
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def left_rotate(self, x: AVLNode) -> AVLNode:
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root: AVLNode | None, key: int) -> AVLNode:
        """Inserts a key into the AVL tree and maintains height balance."""
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            # Duplicate keys not allowed
            return root

        # Update height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Check balance factor
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def inorder_traversal(self, root: AVLNode | None) -> list[int]:
        """Returns in-order list of keys."""
        res = []
        if root:
            res.extend(self.inorder_traversal(root.left))
            res.append(root.key)
            res.extend(self.inorder_traversal(root.right))
        return res
