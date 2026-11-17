from typing import Optional, List, Any

class LCTNode:
    def __init__(self, val: int = 0, node_id: int = 0):
        self.node_id = node_id
        self.val = val
        self.sum = val
        self.rev = False
        self.parent: Optional['LCTNode'] = None
        self.left: Optional['LCTNode'] = None
        self.right: Optional['LCTNode'] = None

    def is_root(self) -> bool:
        """Returns True if this node is the root of an auxiliary splay tree."""
        if not self.parent:
            return True
        return self.parent.left is not self and self.parent.right is not self

    def push(self) -> None:
        """Pushes lazy reversal flag to children."""
        if self.rev:
            self.left, self.right = self.right, self.left
            if self.left:
                self.left.rev = not self.left.rev
            if self.right:
                self.right.rev = not self.right.rev
            self.rev = False

    def update(self) -> None:
        """Updates aggregate statistics from children."""
        self.sum = self.val
        if self.left:
            self.sum += self.left.sum
        if self.right:
            self.sum += self.right.sum


class LinkCutTree:
    """
    Link-Cut Tree (Sleator & Tarjan) for dynamic forest connectivity
    and path aggregate sum queries in amortized O(log N) time.
    Vertices are 0-indexed: 0, 1, ..., num_vertices - 1.
    """

    def __init__(self, values: List[int]):
        if not values:
            raise ValueError("Values list cannot be empty.")
        self.nodes = [LCTNode(val=v, node_id=i) for i, v in enumerate(values)]

    def _rotate(self, x: LCTNode) -> None:
        p = x.parent
        if not p:
            return
        g = p.parent
        is_p_root = p.is_root()

        if p.left is x:
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p

        p.parent = x
        x.parent = g

        if not is_p_root and g:
            if g.left is p:
                g.left = x
            else:
                g.right = x

        p.update()
        x.update()

    def _splay(self, x: LCTNode) -> None:
        # Push down lazy tags from root of auxiliary tree to x
        ancestors = []
        curr: Optional[LCTNode] = x
        while curr:
            ancestors.append(curr)
            if curr.is_root():
                break
            curr = curr.parent

        while ancestors:
            ancestors.pop().push()

        # Perform rotations
        while not x.is_root():
            p = x.parent
            if p and not p.is_root():
                g = p.parent
                if (p.left is x) == (g.left is p if g else False):
                    self._rotate(p)
                else:
                    self._rotate(x)
            self._rotate(x)

    def access(self, u_idx: int) -> None:
        """Creates a preferred path from the root of the tree to u."""
        if not (0 <= u_idx < len(self.nodes)):
            raise IndexError("Vertex index out of bounds.")
        u = self.nodes[u_idx]
        last: Optional[LCTNode] = None
        curr: Optional[LCTNode] = u

        while curr:
            self._splay(curr)
            curr.right = last
            curr.update()
            last = curr
            curr = curr.parent

        self._splay(u)

    def make_root(self, u_idx: int) -> None:
        """Makes vertex u the root of its represented tree."""
        self.access(u_idx)
        u = self.nodes[u_idx]
        u.rev = not u.rev

    def find_root(self, u_idx: int) -> int:
        """Finds the root vertex ID of the tree containing u."""
        self.access(u_idx)
        curr = self.nodes[u_idx]
        curr.push()
        while curr.left:
            curr = curr.left
            curr.push()
        self._splay(curr)
        return curr.node_id

    def connected(self, u_idx: int, v_idx: int) -> bool:
        """Checks if vertices u and v are connected in the forest."""
        if not (0 <= u_idx < len(self.nodes) and 0 <= v_idx < len(self.nodes)):
            raise IndexError("Vertex index out of bounds.")
        if u_idx == v_idx:
            return True
        return self.find_root(u_idx) == self.find_root(v_idx)

    def link(self, u_idx: int, v_idx: int) -> bool:
        """
        Adds an undirected edge between u and v if they belong to different trees.
        Returns True if linked successfully, False if already connected.
        """
        if not (0 <= u_idx < len(self.nodes) and 0 <= v_idx < len(self.nodes)):
            raise IndexError("Vertex index out of bounds.")
        if self.connected(u_idx, v_idx):
            return False

        self.make_root(u_idx)
        self.nodes[u_idx].parent = self.nodes[v_idx]
        return True

    def cut(self, u_idx: int, v_idx: int) -> bool:
        """
        Removes the undirected edge between u and v.
        Returns True if the edge was cut, False if no edge exists between them.
        """
        if not (0 <= u_idx < len(self.nodes) and 0 <= v_idx < len(self.nodes)):
            raise IndexError("Vertex index out of bounds.")
        if not self.connected(u_idx, v_idx):
            return False

        self.make_root(u_idx)
        self.access(v_idx)
        v = self.nodes[v_idx]
        u = self.nodes[u_idx]

        # v must be right child of u or u is left child of v in splay tree
        if v.left is u and u.right is None:
            v.left = None
            u.parent = None
            v.update()
            return True
        return False

    def path_sum(self, u_idx: int, v_idx: int) -> int:
        """Computes sum of node values along path from u to v."""
        if not self.connected(u_idx, v_idx):
            raise ValueError(f"Vertices {u_idx} and {v_idx} are not connected.")
        self.make_root(u_idx)
        self.access(v_idx)
        return self.nodes[v_idx].sum

    def update_value(self, u_idx: int, new_val: int) -> None:
        """Updates the value stored at vertex u."""
        if not (0 <= u_idx < len(self.nodes)):
            raise IndexError("Vertex index out of bounds.")
        self.access(u_idx)
        self.nodes[u_idx].val = new_val
        self.nodes[u_idx].update()
