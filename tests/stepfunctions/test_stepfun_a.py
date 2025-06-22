import pytest

from sandbox.stepfunctions.stepfun import NumericStepfun as Stepfun


def tv(*pairs):
    return tuple(pairs)


def test_normalization_merges_equal_values():
    # Should merge intervals with identical values
    f = Stepfun(tv((0, 1), (5, 1), (10, 2)))
    # Normalized: duplicate value at 5 should be merged away
    assert f == Stepfun(tv((0, 1), (10, 2)))


def test_normalization_sorts_by_timestamp():
    # Out-of-order timestamps should be sorted
    f = Stepfun(tv((10, 2), (0, 1)))
    assert f == Stepfun(tv((0, 1), (10, 2)))


def _test_invalid_start_raises():
    # Should raise if tv_list does not start at 0
    with pytest.raises(ValueError):
        Stepfun(tv((1, 1), (5, 2)))


# def test_invalid_non_strictly_ascending_timestamps_raises():
#     # Should raise if timestamps are not strictly ascending
#     with pytest.raises(ValueError):
#         aux = tv((0, 1), (0, 2), (5, 3))
#         Stepfun(aux)

def _test_invalid_value_type_raises():
    # Should raise if values are not numbers
    with pytest.raises(TypeError):
        Stepfun(tv((0, 1), (10, 'a')))


def test_integrate_zero_length_interval():
    # Integral over zero-length interval should be zero
    f = Stepfun(tv((0, 1), (10, 2)))
    assert f.integrate(5, 5) == 0


def test_integrate_partial_interval():
    # Integral should handle partial intervals correctly
    f = Stepfun(tv((0, 1), (10, 2)))
    assert f.integrate(5, 15) == (10 - 5) * 1 + (15 - 10) * 2


def _test_integrate_out_of_bounds():
    # Integration should be defined on [0, +∞), clamp or raise for out of bounds
    f = Stepfun(tv((0, 2), (10, 1)))
    with pytest.raises(ValueError):
        f.integrate(-1, 5)


def test_comparison_unequal_lengths():
    # Should handle comparison with differing numbers of intervals
    f = Stepfun(tv((0, 1), (5, 3)))
    g = Stepfun(tv((0, 4)))
    assert f < g


def test_add_merges_redundant_timestamps():
    # Adding two functions whose sums have constant value should normalize timestamps away
    f = Stepfun(tv((0, 2), (10, 1)))
    g = Stepfun(tv((0, 3), (10, 4)))
    result = f + g
    # Should merge to one interval, since sum is constant
    assert result == Stepfun(tv((0, 5)))


def test_empty_tv_list_raises():
    with pytest.raises(ValueError):
        Stepfun([])


def test_repr_and_str_non_empty():
    f = Stepfun(tv((0, 1), (5, 2)))
    assert "Stepfun" in repr(f)
    assert "(" in str(f) and ")" in str(f)


def generate_tvlist(n):
    # Generates n intervals: [(0,0), (1,1), (2,2), ..., (n-1, n-1)]
    return tuple((i, float(i)) for i in range(n))


################################################
####  benchmarks for performance tests #########
################################################

def test_large_stepfun_construction(benchmark):
    N = 1_000
    tvlist = generate_tvlist(N)
    benchmark(lambda: Stepfun(tvlist))


def test_large_stepfun_addition(benchmark):
    N = 1_000
    f = Stepfun(generate_tvlist(N))
    g = Stepfun(generate_tvlist(N))
    benchmark(lambda: f + g)


def test_large_stepfun_integrate(benchmark):
    N = 1_000
    f = Stepfun(generate_tvlist(N))
    benchmark(lambda: f.integrate(0, N))


def test_large_stepfun_equality(benchmark):
    N = 1_000
    f = Stepfun(generate_tvlist(N))
    g = Stepfun(generate_tvlist(N))
    benchmark(lambda: f == g)


def test_large_stepfun_abs_neg(benchmark):
    N = 10_000
    f = Stepfun(generate_tvlist(N))
    benchmark(lambda: abs(-f))
