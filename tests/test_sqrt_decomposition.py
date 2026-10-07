import pytest
from algorithms.sqrt_decomposition import SqrtDecomposition, mos_algorithm_distinct_count

def test_sqrt_decomposition_sum_and_updates():
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sqrt_dec = SqrtDecomposition(arr)

    # Full sum
    assert sqrt_dec.query_sum(0, 9) == sum(arr)
    # Subarray sum
    assert sqrt_dec.query_sum(2, 6) == sum(arr[2:7])

    # Point update
    sqrt_dec.point_update(3, 14) # arr[3] was 4, now 14 (+10)
    assert sqrt_dec.query_sum(0, 9) == 65
    assert sqrt_dec.query_sum(3, 3) == 14

    # Range add
    sqrt_dec.range_add(1, 4, 5) # add 5 to indices 1, 2, 3, 4
    assert sqrt_dec.query_sum(0, 9) == 65 + 4 * 5
    assert sqrt_dec.query_sum(1, 4) == (2 + 5) + (3 + 5) + (14 + 5) + (5 + 5)

def test_sqrt_decomposition_boundaries_and_exceptions():
    with pytest.raises(ValueError):
        SqrtDecomposition([])

    sd = SqrtDecomposition([42])
    assert sd.query_sum(0, 0) == 42
    sd.point_update(0, 100)
    assert sd.query_sum(0, 0) == 100

    with pytest.raises(IndexError):
        sd.query_sum(0, 2)
    with pytest.raises(IndexError):
        sd.range_add(-1, 0, 5)

def test_mos_algorithm_distinct_count():
    arr = [1, 2, 1, 3, 4, 2, 3]
    queries = [
        (0, 4),  # [1, 2, 1, 3, 4] -> 4 distinct (1, 2, 3, 4)
        (1, 3),  # [2, 1, 3] -> 3 distinct
        (2, 6),  # [1, 3, 4, 2, 3] -> 4 distinct (1, 3, 4, 2)
        (0, 6),  # all elements -> 4 distinct
        (0, 0),  # [1] -> 1 distinct
    ]
    results = mos_algorithm_distinct_count(arr, queries)
    assert results == [4, 3, 4, 4, 1]

def test_mos_algorithm_empty():
    assert mos_algorithm_distinct_count([], []) == []
    assert mos_algorithm_distinct_count([1, 2], []) == []
