from typing import Optional

class Line:
    def __init__(self, m: float, c: float):
        self.m = m
        self.c = c

    def eval(self, x: float) -> float:
        return self.m * x + self.c


class LiChaoNode:
    def __init__(self, line: Optional[Line] = None):
        self.line = line
        self.left: Optional['LiChaoNode'] = None
        self.right: Optional['LiChaoNode'] = None


class LiChaoTree:
    """
    Dynamic Li Chao Segment Tree for maintaining linear functions y = m * x + c
    and querying the minimum (or maximum) value at any x in O(log(X_max - X_min)) time.
    """

    def __init__(self, x_min: int = -10**6, x_max: int = 10**6, is_min: bool = True):
        if x_min >= x_max:
            raise ValueError("x_min must be strictly less than x_max.")
        self.x_min = x_min
        self.x_max = x_max
        self.is_min = is_min
        self.root: Optional[LiChaoNode] = None

    def _is_better(self, line1: Line, line2: Line, x: float) -> bool:
        v1 = line1.eval(x)
        v2 = line2.eval(x)
        return v1 < v2 if self.is_min else v1 > v2

    def add_line(self, m: float, c: float) -> None:
        """Adds an infinite line y = m * x + c to the tree."""
        new_line = Line(m, c)
        if self.root is None:
            self.root = LiChaoNode(new_line)
            return

        def _insert(node: LiChaoNode, l: int, r: int, line: Line) -> None:
            if node.line is None:
                node.line = line
                return

            mid = (l + r) // 2
            better_mid = self._is_better(line, node.line, mid)
            if better_mid:
                node.line, line = line, node.line

            if l == r:
                return

            better_left = self._is_better(line, node.line, l)
            if better_left:
                if node.left is None:
                    node.left = LiChaoNode()
                _insert(node.left, l, mid, line)
            else:
                better_right = self._is_better(line, node.line, r)
                if better_right:
                    if node.right is None:
                        node.right = LiChaoNode()
                    _insert(node.right, mid + 1, r, line)

        _insert(self.root, self.x_min, self.x_max, new_line)

    def add_segment(self, m: float, c: float, seg_l: int, seg_r: int) -> None:
        """Adds a line segment y = m * x + c active on [seg_l, seg_r]."""
        if seg_l > seg_r:
            raise ValueError("seg_l cannot be greater than seg_r.")
        seg_l = max(self.x_min, seg_l)
        seg_r = min(self.x_max, seg_r)
        if seg_l > seg_r:
            return

        line = Line(m, c)
        if self.root is None:
            self.root = LiChaoNode()

        def _insert_segment(node: LiChaoNode, l: int, r: int, ql: int, qr: int, cur_line: Line) -> None:
            if ql <= l and r <= qr:
                # Segment completely covers current node, delegate to standard line insert
                def _insert_in_sub(sub_node: LiChaoNode, sl: int, sr: int, l_in: Line) -> None:
                    if sub_node.line is None:
                        sub_node.line = l_in
                        return
                    mid = (sl + sr) // 2
                    if self._is_better(l_in, sub_node.line, mid):
                        sub_node.line, l_in = l_in, sub_node.line
                    if sl == sr:
                        return
                    if self._is_better(l_in, sub_node.line, sl):
                        if sub_node.left is None:
                            sub_node.left = LiChaoNode()
                        _insert_in_sub(sub_node.left, sl, mid, l_in)
                    elif self._is_better(l_in, sub_node.line, sr):
                        if sub_node.right is None:
                            sub_node.right = LiChaoNode()
                        _insert_in_sub(sub_node.right, mid + 1, sr, l_in)

                _insert_in_sub(node, l, r, cur_line)
                return

            mid = (l + r) // 2
            if ql <= mid:
                if node.left is None:
                    node.left = LiChaoNode()
                _insert_segment(node.left, l, mid, ql, qr, cur_line)
            if qr > mid:
                if node.right is None:
                    node.right = LiChaoNode()
                _insert_segment(node.right, mid + 1, r, ql, qr, cur_line)

        _insert_segment(self.root, self.x_min, self.x_max, seg_l, seg_r, line)

    def query(self, x: int) -> float:
        """Queries the optimal value among all lines/segments at x."""
        if not (self.x_min <= x <= self.x_max):
            raise IndexError("Query point x out of bounds.")
        if self.root is None:
            raise ValueError("LiChaoTree is empty.")

        best = float('inf') if self.is_min else float('-inf')

        node: Optional[LiChaoNode] = self.root
        l, r = self.x_min, self.x_max

        while node is not None:
            if node.line is not None:
                val = node.line.eval(x)
                if self.is_min:
                    best = min(best, val)
                else:
                    best = max(best, val)

            if l == r:
                break

            mid = (l + r) // 2
            if x <= mid:
                node = node.left
                r = mid
            else:
                node = node.right
                l = mid + 1

        if (self.is_min and best == float('inf')) or (not self.is_min and best == float('-inf')):
            raise ValueError("No active line covers query point x.")

        return best
