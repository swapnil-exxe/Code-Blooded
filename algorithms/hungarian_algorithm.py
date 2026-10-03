from typing import List, Tuple

def hungarian_algorithm(cost_matrix: List[List[float]]) -> Tuple[float, List[Tuple[int, int]]]:
    """
    Hungarian Algorithm (Kuhn-Munkres algorithm) for optimal weighted bipartite matching / assignment problem.
    Finds the minimum cost assignment for an N x N square cost matrix in O(N^3) time.

    Returns:
        (total_minimum_cost, list_of_(worker_idx, job_idx)_pairs)
    """
    if not cost_matrix or not cost_matrix[0]:
        return 0.0, []

    n = len(cost_matrix)
    for row in cost_matrix:
        if len(row) != n:
            raise ValueError("cost_matrix must be an N x N square matrix.")

    # 1-indexed internal arrays for standard Kuhn-Munkres implementation
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [float('inf')] * (n + 1)
        used = [False] * (n + 1)

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = 0

            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost_matrix[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j

            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1
            if p[j0] == 0:
                break

        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    min_cost = -v[0]
    assignment = []
    for j in range(1, n + 1):
        worker = p[j] - 1
        job = j - 1
        assignment.append((worker, job))

    assignment.sort(key=lambda x: x[0])
    return min_cost, assignment
