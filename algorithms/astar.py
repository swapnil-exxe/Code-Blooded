import heapq
import math
from typing import List, Tuple, Optional, Callable

def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def euclidean_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def astar_search(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    heuristic: str = "manhattan"
) -> Optional[List[Tuple[int, int]]]:
    """
    A* Search Algorithm on a 2D grid map with obstacles.
    grid: 2D list where 0 represents walkable cell and 1 represents obstacle.
    start: (row, col) starting position.
    goal: (row, col) target position.
    heuristic: "manhattan" or "euclidean".

    Time Complexity: O(E log V)
    Returns: List of (row, col) coordinates forming optimal path, or None if unreachable.
    """
    rows = len(grid)
    if rows == 0:
        return None
    cols = len(grid[0])

    r_start, c_start = start
    r_goal, c_goal = goal

    if not (0 <= r_start < rows and 0 <= c_start < cols):
        raise IndexError(f"Start position {start} out of grid bounds ({rows}x{cols}).")
    if not (0 <= r_goal < rows and 0 <= c_goal < cols):
        raise IndexError(f"Goal position {goal} out of grid bounds ({rows}x{cols}).")

    if grid[r_start][c_start] == 1 or grid[r_goal][c_goal] == 1:
        return None  # Start or goal is blocked

    h_func: Callable[[Tuple[int, int], Tuple[int, int]], float]
    if heuristic == "manhattan":
        h_func = manhattan_distance
    elif heuristic == "euclidean":
        h_func = euclidean_distance
    else:
        raise ValueError(f"Unknown heuristic: {heuristic}")

    # Min-heap stores tuples of (f_score, g_score, (row, col))
    open_set = [(h_func(start, goal), 0.0, start)]
    g_score = {start: 0.0}
    came_from = {}
    visited = set()

    # 4-directional movements (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        f, g, current = heapq.heappop(open_set)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        r, c = current
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = g + 1.0  # Cost per move is 1.0
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    came_from[neighbor] = current
                    f_score = tentative_g + h_func(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return None
