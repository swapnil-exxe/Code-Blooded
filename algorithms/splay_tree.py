from typing import Optional, List, Any

class SplayNode:
    def __init__(self, key: Any):
        self.key = key
        self.left: Optional['SplayNode'] = None
        self.right: Optional['SplayNode'] = None
        self.parent: Optional['SplayNode'] = None

class SplayTree:
    """
    Splay Tree self-adjusting binary search tree data structure.
    Brings recently accessed key to the root via splay rotations (Zig, Zig-Zig, Zig-Zag).
    Amortized O(log N) operations.
    """

    def __init__(self):
        self.root: Optional[SplayNode] = None

    def _rotate_left(self, x: SplayNode) -> None:
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
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

    def _rotate_right(self, x: SplayNode) -> None:
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
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

    def _splay(self, x: SplayNode) -> None:
        while x.parent is not None:
            p = x.parent
            g = p.parent
            if g is None:
                # Zig rotation
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            elif x == p.left and p == g.left:
                # Zig-Zig rotation
                self._rotate_right(g)
                self._rotate_right(p)
            elif x == p.right and p == g.right:
                # Zig-Zig rotation
                self._rotate_left(g)
                self._rotate_left(p)
            elif x == p.right and p == g.left:
                # Zig-Zag rotation
                self._rotate_left(p)
                self._rotate_right(g)
            else:
                # Zig-Zag rotation
                self._rotate_right(p)
                self._rotate_left(g)

    def search(self, key: Any) -> bool:
        """Searches for key and splays node to root. Returns True if found."""
        curr = self.root
        last = None
        while curr is not None:
            last = curr
            if key == curr.key:
                self._splay(curr)
                return True
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        if last is not None:
            self._splay(last)
        return False

    def insert(self, key: Any) -> None:
        """Inserts key into Splay Tree and splays inserted node to root."""
        if self.root is None:
            self.root = SplayNode(key)
            return

        curr = self.root
        parent = None
        while curr is not None:
            parent = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                # Key already exists; splay to root
                self._splay(curr)
                return

        new_node = SplayNode(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)

    def delete(self, key: Any) -> bool:
        """Deletes key from Splay Tree if present."""
        if not self.search(key):
            return False

        # Node with key is now at root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if left_subtree:
            left_subtree.parent = None
        if right_subtree:
            right_subtree.parent = None

        if left_subtree is None:
            self.root = right_subtree
        else:
            # Find max in left subtree and splay to root of left subtree
            curr = left_subtree
            while curr.right is not None:
                curr = curr.right
            # Splay max node to root of left subtree
            # Temporarily isolate left_subtree
            self.root = left_subtree
            self._splay(curr)
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

        return True

    def inorder(self) -> List[Any]:
        """Returns in-order traversal of keys in sorted order."""
        res = []
        def _dfs(n: Optional[SplayNode]):
            if n:
                _dfs(n.left)
                res.append(n.key)
                _dfs(n.right)
        _dfs(self.root)
        return res
