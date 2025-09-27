# Benchmark test for histogram implementations
# Comparing performance of histogram_1, histogram_2, histogram_3, histogram_4

import random

import pytest

from sandbox.basics.histogram import histogram_1, histogram_2, histogram_3, histogram_4


# Test data generators
def generate_small_data():
    """Small dataset: 100 elements, 10 unique values"""
    return [random.randint(0, 9) for _ in range(100)]


def generate_medium_data():
    """Medium dataset: 1000 elements, 50 unique values"""
    return [random.randint(0, 49) for _ in range(1000)]


def generate_large_data():
    """Large dataset: 10000 elements, 100 unique values"""
    return [random.randint(0, 99) for _ in range(10000)]


def generate_high_unique_data():
    """High uniqueness: 1000 elements, 800 unique values"""
    return [random.randint(0, 999) for _ in range(1000)]


# Benchmark fixtures
@pytest.fixture
def small_data():
    random.seed(42)  # For reproducible results
    return generate_small_data()


@pytest.fixture
def medium_data():
    random.seed(42)
    return generate_medium_data()


@pytest.fixture
def large_data():
    random.seed(42)
    return generate_large_data()


@pytest.fixture
def high_unique_data():
    random.seed(42)
    return generate_high_unique_data()


# Benchmark tests
class TestHistogramBenchmarks:

    def test_histogram_1_small(self, benchmark, small_data):
        result = benchmark(histogram_1, small_data)
        assert isinstance(result, dict)

    def test_histogram_2_small(self, benchmark, small_data):
        result = benchmark(histogram_2, small_data)
        assert isinstance(result, dict)

    def test_histogram_3_small(self, benchmark, small_data):
        result = benchmark(histogram_3, small_data)
        assert isinstance(result, dict)

    def test_histogram_4_small(self, benchmark, small_data):
        result = benchmark(histogram_4, small_data)
        assert isinstance(result, dict)

    def test_histogram_1_medium(self, benchmark, medium_data):
        result = benchmark(histogram_1, medium_data)
        assert isinstance(result, dict)

    def test_histogram_2_medium(self, benchmark, medium_data):
        result = benchmark(histogram_2, medium_data)
        assert isinstance(result, dict)

    def test_histogram_3_medium(self, benchmark, medium_data):
        result = benchmark(histogram_3, medium_data)
        assert isinstance(result, dict)

    def test_histogram_4_medium(self, benchmark, medium_data):
        result = benchmark(histogram_4, medium_data)
        assert isinstance(result, dict)

    def test_histogram_1_large(self, benchmark, large_data):
        result = benchmark(histogram_1, large_data)
        assert isinstance(result, dict)

    def test_histogram_2_large(self, benchmark, large_data):
        result = benchmark(histogram_2, large_data)
        assert isinstance(result, dict)

    def test_histogram_3_large(self, benchmark, large_data):
        result = benchmark(histogram_3, large_data)
        assert isinstance(result, dict)

    def test_histogram_4_large(self, benchmark, large_data):
        result = benchmark(histogram_4, large_data)
        assert isinstance(result, dict)

    def test_histogram_1_high_unique(self, benchmark, high_unique_data):
        result = benchmark(histogram_1, high_unique_data)
        assert isinstance(result, dict)

    def test_histogram_2_high_unique(self, benchmark, high_unique_data):
        result = benchmark(histogram_2, high_unique_data)
        assert isinstance(result, dict)

    def test_histogram_3_high_unique(self, benchmark, high_unique_data):
        result = benchmark(histogram_3, high_unique_data)
        assert isinstance(result, dict)

    def test_histogram_4_high_unique(self, benchmark, high_unique_data):
        result = benchmark(histogram_4, high_unique_data)
        assert isinstance(result, dict)


# Comparative benchmark test
@pytest.mark.parametrize("histogram_func", [histogram_1, histogram_2, histogram_3, histogram_4])
def test_all_histograms_comparison(benchmark, histogram_func):
    """Comparative benchmark across all implementations with medium dataset"""
    random.seed(42)
    data = generate_medium_data()
    result = benchmark(histogram_func, data)
    assert isinstance(result, dict)
    # Verify correctness
    for x in set(data):
        assert result[x] == data.count(x)
