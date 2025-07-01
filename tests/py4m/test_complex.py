# py4m/tests/test_complex.py

from _operator import mul
from functools import reduce

from sandbox.py4m.mapper.m_complex import Complex
from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.util.utils import close_to
from tests.py4m.test_natives import complex_samples

# ----- Type/sample groupings -----

n = 30


def make_complex_samples(n):
    return make_samples([Complex], complex_samples(n))


def test_complex():
    # todo
    complex_samples = make_complex_samples(n)
    complex_samples_reversed = list(complex_samples)
    complex_samples_reversed.reverse()
    complex_zero = complex_samples[0].zero()
    complex_one = complex_samples[0].one()
    total = sum(complex_samples, complex_zero)
    total_rev = sum(complex_samples_reversed, complex_zero)
    assert total == total_rev
    prod = reduce(mul, complex_samples, complex_one)
    prod_rev = reduce(mul, complex_samples_reversed, complex_one)
    assert close_to(prod, prod_rev)
