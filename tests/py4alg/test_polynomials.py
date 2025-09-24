# py4alg/tests/test_polynomials.py

import pytest

from sandbox.py4alg.mapper.m_polynomial import Polynomial
from sandbox.py4alg.util.g_samples import (g_cycle, g_ints, g_floats, g_complex_,
                                           g_nat_complex, g_nat_ints, g_nat_floats,
                                           g_fractions, g_polynomials)
from sandbox.py4alg.mapper.m_fraction import gcd
from sandbox.py4alg.util.utils import close_to
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_float import NativeFloat
from tests.py4alg.check_properties import check_rings, check_euclidean_rings


# ----- Type/sample groupings -----
# todo
def xxx_test_gcd():
    p = Polynomial(NativeFloat(1.), NativeFloat(0.), NativeFloat(-1.))
    q = Polynomial(NativeFloat(1.), NativeFloat(1.))
    g = gcd(p, q)
    print()
    print(g)
    assert gcd(p, q) == Polynomial(NativeFloat(1.), NativeFloat(1.))

    p = Polynomial(NativeFloat(2.), NativeFloat(3.), NativeFloat(1.))
    q = Polynomial(NativeFloat(1.), NativeFloat(0.), NativeFloat(-1.))
    assert gcd(p, q) == Polynomial(NativeFloat(1.), NativeFloat(1.))


def poly_samples(n: int):
    return (compose(take(n), g_polynomials, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_polynomials, g_polynomials, g_polynomials, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_polynomials, g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_polynomials, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_polynomials, g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_polynomials, g_fractions, g_nat_floats, g_floats)(10., 20.))


def poly_args(n):
    """
    this list contains the arguments for the polynomials from poly_samples
    """
    return (compose(take(n), g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_fractions, g_nat_floats, g_floats)(10, 20))


@pytest.mark.parametrize("samples", poly_samples(20))
def test_rings(samples):
    check_rings(samples)


@pytest.mark.parametrize("samples", poly_samples(20)[2:])
# samples 0 and 1 are rings
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


def poly_table(n):
    return zip(poly_samples(n), poly_args(n))


@pytest.mark.parametrize("samples,args", poly_table(100))
def test_poly_poly(samples, args):
    q = Polynomial(*samples)
    for x in args:
        r = lambda x: Polynomial(*(p(x) for p in samples))
        assert close_to(r(x)(x), q(x))
