import pytest
from algorithms.sparse_table import SparseTable

def test_sparse_table_range_min():
    arr = [7, 2, 3, 0, 5, 10, 3, 12, 18]
    st = SparseTable(arr, min)

    assert st.query(0, 4) == 0  # min([7, 2, 3, 0, 5])
    assert st.query(4, 7) == 3  # min([5, 10, 3, 12])
    assert st.query(1, 2) == 2  # min([2, 3])
    assert st.query(5, 5) == 10 # single element

def test_sparse_table_range_max():
    arr = [4, 6, 1, 5, 7, 3]
    st = SparseTable(arr, max)

    assert st.query(0, 5) == 7
    assert st.query(1, 3) == 6
    assert st.query(2, 2) == 1

def test_sparse_table_invalid_inputs():
    with pytest.raises(ValueError):
        SparseTable([])

    st = SparseTable([1, 2, 3])
    with pytest.raises(IndexError):
        st.query(2, 1)
    with pytest.raises(IndexError):
        st.query(0, 5)
