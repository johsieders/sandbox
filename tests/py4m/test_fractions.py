# py4m/tests/test_fractions.py

from functools import reduce
from operator import mul

import pytest

from sandbox.py4m.mapper.m_fraction import Fraction
from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.util.utils import close_to
from sandbox.py4m.wrapper.w_int import NativeInt
from tests.py4m.test_natives import int_samples
from tests.py4m.test_properties import test_fields

# ----- Type/sample groupings -----

n = 30


@pytest.fixture
def size_n():
    return 5


def test_constructor_with_native_int():
    my_ints = [[0, 1], [1, 1], [3, 2], [4, 2]]
    my_ab = [make_samples([NativeInt], samples) for samples in my_ints]
    rs = [Fraction(a, b) for a, b in my_ab]

    for r in rs:
        for s in rs[1:]:
            assert Fraction(r, s) == r / s

@pytest.fixture
def size():
    return 10


@pytest.fixture
def samples(size):
    return make_samples([Fraction], int_samples(2 * n))


def test_fraction_properties(samples):
    test_fields(samples)


def test_fractions(samples):
    samples_rev = list(reversed(samples))
    zero = samples[0].zero()
    one = samples[0].one()
    total = sum(samples, zero)
    total_rev = sum(samples_rev, zero)
    assert total == total_rev
    prod = reduce(mul, samples, one)
    prod_rev = reduce(mul, samples_rev, one)
    assert close_to(prod, prod_rev)


def test_fraction_polynomial_int_samples():

    p_samples = make_samples([Polynomial, NativeInt], range(1, 10))
    f_samples = make_samples([Fraction], p_samples)
    print()
    print(f_samples)

    # fraction_samples_rev = list(reversed(fraction_samples))
    # fraction_zero = fraction_samples[0].zero()
    # fraction_one = fraction_samples[0].one()
    # total = sum(fraction_samples, fraction_zero)
    # total_rev = sum(fraction_samples_reversed, fraction_zero)
    # assert total == total_rev
    # prod = reduce(mul, fraction_samples, fraction_one)
    # prod_rev = reduce(mul, fraction_samples_reversed, fraction_one)
    # # assert close_to(prod, prod_rev)
    # if not close_to(prod, prod_rev):
    #     p = iter(prod._coeffs)
    #     r = iter(prod_rev._coeffs)
    #     idx = 0
    #     while True:
    #         try:
    #             print(idx, '   ', next(p) - next(r))
    #             idx += 1
    #         except StopIteration:
    #             break
