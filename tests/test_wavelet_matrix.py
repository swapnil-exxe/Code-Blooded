import pytest
from algorithms.wavelet_matrix import WaveletMatrix

def test_wavelet_matrix_quantile_and_rank():
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    wm = WaveletMatrix(arr)

    # 0-indexed element access
    assert wm.access(0) == 3
    assert wm.access(5) == 9

    # Rank count of val 5 in prefix [0, 9)
    assert wm.rank(5, 9) == 2  # indices 4 and 8 contain 5

    # Range quantile (k-th smallest element in subsegment)
    # Range [0, 4] -> arr[0..4] = [3, 1, 4, 1, 5] -> sorted: [1, 1, 3, 4, 5]
    assert wm.quantile(0, 4, 0) == 1  # 0th smallest = 1
    assert wm.quantile(0, 4, 2) == 3  # 2nd smallest = 3
    assert wm.quantile(0, 4, 4) == 5  # 4th smallest = 5

def test_wavelet_matrix_invalid_inputs():
    with pytest.raises(ValueError):
        WaveletMatrix([])
    with pytest.raises(ValueError):
        WaveletMatrix([-1, 5])

    wm = WaveletMatrix([10, 20, 30])
    with pytest.raises(IndexError):
        wm.quantile(0, 5, 0)
