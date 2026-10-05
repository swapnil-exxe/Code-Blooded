from typing import List, Tuple

Point = Tuple[float, float]

def cross_product(o: Point, a: Point, b: Point) -> float:
    """
    2D cross product of OA and OB vectors:
    Returns positive if O -> A -> B is counter-clockwise turn,
    negative if clockwise turn,
    0 if collinear.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points: List[Point]) -> List[Point]:
    """
    Computes the 2D Convex Hull of a set of points using Andrew's Monotone Chain algorithm.
    Time Complexity: O(N log N)
    Space Complexity: O(N)

    Returns: List of points on the convex hull in counter-clockwise order.
    """
    if len(points) <= 1:
        return points[:]

    # Sort points lexicographically by x, then by y
    sorted_pts = sorted(set(points))
    if len(sorted_pts) <= 1:
        return sorted_pts

    # Build lower hull
    lower: List[Point] = []
    for p in sorted_pts:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper: List[Point] = []
    for p in reversed(sorted_pts):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hulls (excluding last point of each as it's repeated)
    return lower[:-1] + upper[:-1]
