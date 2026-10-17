import pytest
from algorithms.bloom_filter import BloomFilter

def test_bloom_filter_no_false_negatives():
    bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
    words = [f"item_{i}" for i in range(500)]

    for w in words:
        bf.add(w)

    assert len(bf) == 500

    # No false negatives: every added word must return True
    for w in words:
        assert w in bf
        assert bf.contains(w) is True

def test_bloom_filter_false_positive_rate():
    expected = 2000
    target_fp = 0.05
    bf = BloomFilter(expected_elements=expected, false_positive_rate=target_fp)

    for i in range(expected):
        bf.add(f"present_{i}")

    # Check non-present elements
    test_queries = 2000
    false_positives = sum(1 for i in range(test_queries) if f"absent_{i}" in bf)
    observed_fp = false_positives / test_queries

    # Observed false positive rate should be reasonably close to target (within tolerance)
    assert observed_fp < target_fp + 0.03

def test_bloom_filter_approximate_count():
    bf = BloomFilter(expected_elements=500, false_positive_rate=0.01)
    assert bf.approximate_item_count() == 0

    for i in range(200):
        bf.add(f"data_{i}")

    est = bf.approximate_item_count()
    # Estimate should be close to 200 (within 15%)
    assert 160 <= est <= 240

def test_bloom_filter_invalid_args():
    with pytest.raises(ValueError):
        BloomFilter(0, 0.01)
    with pytest.raises(ValueError):
        BloomFilter(100, 0.0)
    with pytest.raises(ValueError):
        BloomFilter(100, 1.0)
