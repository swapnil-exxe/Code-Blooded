import bisect
from typing import List, Optional

class Line:
    def __init__(self, m: float, c: float, p: float = float('inf')):
        self.m = m
        self.c = c
        self.p = p  # intersection x-coordinate with the next line

    def eval(self, x: float) -> float:
        return self.m * x + self.c

    def intersect(self, other: 'Line') -> float:
        """Returns the x-coordinate where self and other intersect."""
        if self.m == other.m:
            return float('inf') if self.c >= other.c else float('-inf')
        return (other.c - self.c) / (self.m - other.m)


class ConvexHullTrick:
    """
    Dynamic Convex Hull Trick (Line Container) maintaining the upper envelope
    of linear functions y = m * x + c for maximum queries in O(log N) time.
    """

    def __init__(self, is_max: bool = True):
        self.is_max = is_max
        self.lines: List[Line] = []

    def __len__(self) -> int:
        return len(self.lines)

    def add_line(self, m: float, c: float) -> None:
        """Adds a line y = m * x + c into the container."""
        if not self.is_max:
            m = -m
            c = -c

        new_line = Line(m, c)

        # Insert line maintaining ascending order of slope m
        idx = bisect.bisect_left([l.m for l in self.lines], m)
        if idx < len(self.lines) and self.lines[idx].m == m:
            if self.lines[idx].c >= c:
                return  # Existing parallel line is already higher/equal
            else:
                self.lines.pop(idx)

        self.lines.insert(idx, new_line)

        # Prune redundant lines to the right
        while idx + 1 < len(self.lines):
            nxt = self.lines[idx + 1]
            inter = self.lines[idx].intersect(nxt)
            self.lines[idx].p = inter
            if inter >= nxt.p:
                self.lines.pop(idx + 1)
            else:
                break

        # Prune redundant lines to the left
        while idx > 0:
            prev = self.lines[idx - 1]
            inter = prev.intersect(self.lines[idx])
            prev.p = inter
            if idx + 1 < len(self.lines) and inter >= self.lines[idx].p:
                self.lines.pop(idx)
                idx -= 1
            else:
                break

    def query(self, x: float) -> float:
        """
        Evaluates the optimal line at x in O(log N) time using binary search.
        """
        if not self.lines:
            raise ValueError("ConvexHullTrick container is empty.")

        p_coords = [l.p for l in self.lines]
        idx = bisect.bisect_left(p_coords, x)
        idx = min(idx, len(self.lines) - 1)

        val = self.lines[idx].eval(x)
        return val if self.is_max else -val
