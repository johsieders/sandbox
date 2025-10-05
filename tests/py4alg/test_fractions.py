# py4alg/tests/test_fractions.py
import pytest

from sandbox.py4alg.mapper import Fraction, Polynomial
from sandbox.py4alg.util.g_samples import (g_cycle, g_ints, g_floats, g_complex_,
                                           g_nat_complex, g_nat_ints, g_nat_floats,
                                           g_fractions, g_polynomials)
from sandbox.py4alg.util.utils import compose, take
from tests.py4alg.check_properties import check_division_algorithm, check_divmod, check_euclidean_rings, check_fields


# ----- Type/sample groupings -----

def fraction_samples(n: int):
    return (compose(take(n), g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_fractions, g_fractions, g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_fractions, g_nat_floats, g_floats)(10., 20.),
            compose(take(n), g_fractions, g_fractions, g_nat_floats, g_floats)(10., 20.),
            compose(take(n), g_fractions, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_fractions, g_polynomials, g_nat_floats, g_floats)(1., 10.))


@pytest.mark.parametrize("samples", fraction_samples(10))
def test_divmod(samples):
    check_division_algorithm(samples)
    check_divmod(samples)


@pytest.mark.parametrize("samples", fraction_samples(10))
def test_euclidean_ring(samples):
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", fraction_samples(20)[:-1])
def test_fields(samples):
    check_fields(samples)


def test_rat_poly():
    coeffs_p = compose(take(3), g_nat_floats, g_cycle)((1., 0., -1.))
    coeffs_q = compose(take(2), g_nat_floats, g_cycle)((1., 1.))
    coeffs_one = compose(take(1), g_nat_floats, g_cycle)((1.,))
    p = Polynomial(*coeffs_p)
    q = Polynomial(*coeffs_q)
    one = Polynomial(*coeffs_one)

    r = Fraction(p, q)
    s = r * Fraction(q, one)
    assert s == Fraction(p, one)


def test_poly_rat():
    n = 8
    rs = compose(take(n), g_fractions, g_nat_ints, g_cycle)((2,))
    p = Polynomial(*rs)
