import pytest
from algorithms.skip_list import SkipList

def test_skip_list_insert_search_delete():
    sl = SkipList()
    keys = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]
    for k in keys:
        sl.insert(k)

    assert sl.to_list() == sorted(keys)

    for k in keys:
        assert sl.search(k) is True

    assert sl.search(100) is False

    assert sl.delete(19) is True
    assert sl.search(19) is False
    assert sl.delete(19) is False
    assert sl.to_list() == sorted([k for k in keys if k != 19])

def test_skip_list_invalid_params():
    with pytest.raises(ValueError):
        SkipList(max_level=0)
    with pytest.raises(ValueError):
        SkipList(p=1.5)
