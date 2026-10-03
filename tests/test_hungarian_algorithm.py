import pytest
from algorithms.hungarian_algorithm import hungarian_algorithm

def test_hungarian_algorithm_basic():
    cost_matrix = [
        [4, 2, 8],
        [4, 3, 7],
        [3, 1, 6]
    ]
    # Optimal assignments:
    # Worker 0 -> Job 1 (cost 2)
    # Worker 1 -> Job 0 (cost 4)
    # Worker 2 -> Job 2 (cost 6)
    # Total cost = 12
    # Or Worker 0 -> Job 0 (4), Worker 1 -> Job 2 (7), Worker 2 -> Job 1 (1) -> 12
    # Check if min cost is 12
    min_cost, assignment = hungarian_algorithm(cost_matrix)
    assert min_cost == 12.0
    assert len(assignment) == 3
    # Check each worker assigned to distinct job
    workers = [w for w, j in assignment]
    jobs = [j for w, j in assignment]
    assert sorted(workers) == [0, 1, 2]
    assert sorted(jobs) == [0, 1, 2]
    # Check total cost matches sum of assigned cells
    actual_cost = sum(cost_matrix[w][j] for w, j in assignment)
    assert actual_cost == 12.0

def test_hungarian_algorithm_empty():
    assert hungarian_algorithm([]) == (0.0, [])

def test_hungarian_algorithm_non_square():
    with pytest.raises(ValueError):
        hungarian_algorithm([[1, 2], [3, 4], [5, 6]])
