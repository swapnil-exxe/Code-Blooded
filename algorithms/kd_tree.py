import math
from typing import List, Tuple, Optional, Sequence

Point = Tuple[float, ...]

class KDNode:
    def __init__(self, point: Point, axis: int):
        self.point = point
        self.axis = axis
        self.left: Optional['KDNode'] = None
        self.right: Optional['KDNode'] = None

class KDTree:
    """
    k-d Tree (k-dimensional tree) for spatial point indexing,
    fast nearest-neighbor search, and orthogonal range bounding-box queries.
    """

    def __init__(self, points: Optional[List[Sequence[float]]] = None, k: Optional[int] = None):
        self._size = 0
        if points:
            first_point = points[0]
            self.k = len(first_point)
            if self.k == 0:
                raise ValueError("Points must have at least 1 dimension.")
            for p in points:
                if len(p) != self.k:
                    raise ValueError("All points must have the same dimension.")
            tuples = [tuple(float(x) for x in p) for p in points]
            self._size = len(tuples)
            self.root = self._build(tuples, 0)
        else:
            if k is None or k <= 0:
                raise ValueError("Dimension k must be specified and positive when initializing empty KDTree.")
            self.k = k
            self.root = None

    def __len__(self) -> int:
        return self._size

    def _build(self, points: List[Point], depth: int) -> Optional[KDNode]:
        if not points:
            return None

        axis = depth % self.k
        points.sort(key=lambda p: p[axis])
        median_idx = len(points) // 2

        node = KDNode(points[median_idx], axis)
        node.left = self._build(points[:median_idx], depth + 1)
        node.right = self._build(points[median_idx + 1:], depth + 1)
        return node

    def insert(self, point: Sequence[float]) -> None:
        """Inserts a new point into the KD-Tree."""
        if len(point) != self.k:
            raise ValueError(f"Point dimension must match tree dimension ({self.k}).")
        pt = tuple(float(x) for x in point)

        def _insert(node: Optional[KDNode], depth: int) -> KDNode:
            if node is None:
                return KDNode(pt, depth % self.k)
            axis = node.axis
            if pt[axis] < node.point[axis]:
                node.left = _insert(node.left, depth + 1)
            else:
                node.right = _insert(node.right, depth + 1)
            return node

        self.root = _insert(self.root, 0)
        self._size += 1

    @staticmethod
    def _distance_sq(p1: Point, p2: Point) -> float:
        return sum((a - b) ** 2 for a, b in zip(p1, p2))

    def nearest_neighbor(self, target: Sequence[float]) -> Tuple[Optional[Point], float]:
        """
        Finds the closest point to target using Euclidean distance.
        Returns (closest_point, distance).
        """
        if self.root is None:
            return None, float('inf')
        if len(target) != self.k:
            raise ValueError(f"Target dimension must match tree dimension ({self.k}).")
        tgt = tuple(float(x) for x in target)

        best_point: Optional[Point] = None
        best_dist_sq = float('inf')

        def _search(node: Optional[KDNode]):
            nonlocal best_point, best_dist_sq
            if node is None:
                return

            dist_sq = self._distance_sq(node.point, tgt)
            if dist_sq < best_dist_sq:
                best_dist_sq = dist_sq
                best_point = node.point

            axis = node.axis
            diff = tgt[axis] - node.point[axis]

            first = node.left if diff < 0 else node.right
            second = node.right if diff < 0 else node.left

            _search(first)
            # Prune opposite subtree if hyper-plane distance exceeds current best
            if diff * diff < best_dist_sq:
                _search(second)

        _search(self.root)
        return best_point, math.sqrt(best_dist_sq)

    def range_search(self, lower: Sequence[float], upper: Sequence[float]) -> List[Point]:
        """
        Returns all points lying in the axis-aligned box [lower[i], upper[i]].
        """
        if len(lower) != self.k or len(upper) != self.k:
            raise ValueError(f"Boundaries must match tree dimension ({self.k}).")

        results: List[Point] = []

        def _search(node: Optional[KDNode]):
            if node is None:
                return

            # Check if current point is within bounds
            in_range = all(lower[i] <= node.point[i] <= upper[i] for i in range(self.k))
            if in_range:
                results.append(node.point)

            axis = node.axis
            if node.point[axis] >= lower[axis]:
                _search(node.left)
            if node.point[axis] <= upper[axis]:
                _search(node.right)

        _search(self.root)
        return results
