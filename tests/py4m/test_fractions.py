# py4m/tests/test_fractions.py

import pytest

from sandbox.py4m.mapper.m_fraction import Fraction
from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.util.utils import close_to
from tests.py4m.check_properties import check_fields
from tests.py4m.test_natives import int_samples, float_samples

# ----- Type/sample groupings -----

# todo
N = 5


def frac_int_samples(n: int):
    non_zero_samples = [f for f in int_samples(n) if f != f.zero()]
    return make_samples([Fraction], non_zero_samples)


def frac_frac_samples(n: int):
    non_zero_samples = [f for f in frac_int_samples(n) if not close_to(f, f.zero())]
    return make_samples([Fraction], non_zero_samples)


def frac_poly_samples(n: int):
    non_zero_samples = [f for f in float_samples(n) if not close_to(f, f.zero())]
    return make_samples([Fraction, Polynomial], non_zero_samples)


def frac_samples(n: int):
    return (frac_poly_samples(n),
            frac_int_samples(n),
            frac_frac_samples(n))


@pytest.mark.parametrize("samples", frac_samples(N)[1:])
# todo
def test_fields(samples):
    check_fields(samples)


@pytest.mark.parametrize("samples", [frac_int_samples(N)])
def test_constructor(samples):
    while samples:
        f = samples.pop()
        if samples:
            g = samples.pop()
            if g != g.zero():
                h = Fraction(f, g)
                assert h == f / g
