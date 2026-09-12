import pytest
from algorithms.heap import MaxHeap

def test_max_heap_insert_and_extract():
    heap = MaxHeap()
    elements = [10, 50, 20, 40, 30]
    for el in elements:
        heap.insert(el)

    assert heap.peek() == 50
    assert heap.is_valid_heap() is True

    extracted = [heap.extract_max() for _ in range(len(elements))]
    assert extracted == [50, 40, 30, 20, 10]

def test_max_heapify_array():
    unsorted_arr = [3, 9, 2, 1, 4, 5, 8]
    heap = MaxHeap(unsorted_arr)

    assert heap.is_valid_heap() is True
    assert heap.peek() == 9

def test_empty_heap_exceptions():
    heap = MaxHeap()
    with pytest.raises(IndexError, match="empty MaxHeap"):
        heap.peek()

    with pytest.raises(IndexError, match="empty MaxHeap"):
        heap.extract_max()
