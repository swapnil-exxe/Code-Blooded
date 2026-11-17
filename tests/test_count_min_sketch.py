import pytest
from algorithms.count_min_sketch import CountMinSketch

def test_count_min_sketch_exact_under_no_collisions():
    cms = CountMinSketch(width=500, depth=5)
    cms.add("apple", 10)
    cms.add("banana", 25)
    cms.add("orange", 5)

    assert cms.total_count == 40
    # True frequency <= estimate
    assert cms.estimate("apple") >= 10
    assert cms.estimate("banana") >= 25
    assert cms.estimate("orange") >= 5
    assert cms.estimate("grape") == 0

def test_count_min_sketch_error_bound():
    # Epsilon = 0.05, Delta = 0.01
    cms = CountMinSketch(epsilon=0.05, delta=0.01)
    true_counts = {}

    for i in range(100):
        key = f"item_{i % 20}"
        cms.add(key, 1)
        true_counts[key] = true_counts.get(key, 0) + 1

    assert cms.total_count == 100

    for key, count in true_counts.items():
        est = cms.estimate(key)
        assert est >= count
        # Within epsilon * N error bound
        assert est <= count + 0.05 * 100 + 1

def test_count_min_sketch_merge():
    s1 = CountMinSketch(width=200, depth=4)
    s2 = CountMinSketch(width=200, depth=4)

    s1.add("x", 15)
    s1.add("y", 10)

    s2.add("y", 20)
    s2.add("z", 30)

    merged = s1.merge(s2)
    assert merged.total_count == 75
    assert merged.estimate("x") >= 15
    assert merged.estimate("y") >= 30
    assert merged.estimate("z") >= 30

def test_count_min_sketch_inner_product():
    s1 = CountMinSketch(width=500, depth=5)
    s2 = CountMinSketch(width=500, depth=5)

    s1.add("apple", 2)
    s1.add("banana", 3)

    s2.add("apple", 4)
    s2.add("orange", 5)

    # Dot product: 2*4 = 8
    dot = s1.inner_product(s2)
    assert dot >= 8

def test_count_min_sketch_exceptions():
    with pytest.raises(ValueError):
        CountMinSketch(epsilon=0.0, delta=0.5)
    with pytest.raises(ValueError):
        CountMinSketch(epsilon=0.1, delta=1.0)
    with pytest.raises(ValueError):
        CountMinSketch(width=0, depth=5)

    cms = CountMinSketch()
    with pytest.raises(ValueError):
        cms.add("item", -1)

    other = CountMinSketch(width=10, depth=2)
    with pytest.raises(ValueError):
        cms.merge(other)
