# py4m/tests/test_polynomials.py

import pytest

from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.util.g_samples import (g_ints, g_floats, g_complex_,
                                         g_nat_complex, g_nat_ints, g_nat_floats,
                                         g_fractions, g_polynomials)
from sandbox.py4m.util.utils import close_to
from sandbox.py4m.util.utils import compose, take
from tests.py4m.check_properties import check_rings, check_euclidean_rings


# ----- Type/sample groupings -----


def poly_samples(n: int):
    return (compose(take(n), g_polynomials, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_polynomials, g_polynomials, g_polynomials, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_polynomials, g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_polynomials, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_polynomials, g_fractions, g_nat_floats, g_floats)(10., 20.))


def poly_args(n):
    """
    this list contains the arguments for the polynomials from poly_samples
    """
    return (compose(take(n), g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_fractions, g_nat_floats, g_floats)(10, 20))


@pytest.mark.parametrize("samples", poly_samples(20))
def test_rings(samples):
    check_rings(samples)


@pytest.mark.parametrize("samples", poly_samples(20)[2:])
# samples 0 and 1 are just rings
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


def poly_table(n):
    return zip(poly_samples(n), poly_args(n))


@pytest.mark.parametrize("samples,args", poly_table(20))
def test_poly_poly(samples, args):
    q = Polynomial(*samples)
    for x in args:
        r = lambda x: Polynomial(*(p(x) for p in samples))
        assert close_to(r(x)(x), q(x))
