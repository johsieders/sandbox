# py4alg/tests/test_fractions.py
import pytest

from sandbox.py4alg.mapper import Fraction, Polynomial, FieldPolynomial
from sandbox.py4alg.util.gen_samples import (gen_cycle, gen_ints, gen_floats, gen_complex_,
                                             gen_nat_complex, gen_nat_ints, gen_nat_floats,
                                             gen_fractions, gen_field_polynomials, def_nat_ints, def_nat_floats, def_nat_complex,
                                             def_fractions)
from sandbox.py4alg.util.utils import compose, take
from tests.py4alg.check_properties import check_division, check_divmod, check_euclidean_rings, check_fields


# ----- Type/sample groupings -----

def fraction_samples(n: int):
    return (compose(take(n), gen_fractions, gen_nat_ints, gen_ints)(1, 100),
            compose(take(n), gen_fractions, gen_fractions, gen_fractions, gen_nat_ints, gen_ints)(1, 100),
            compose(take(n), gen_fractions, gen_nat_floats, gen_floats)(1., 100.),
            compose(take(n), gen_fractions, gen_fractions, gen_nat_floats, gen_floats)(1., 100.),
            compose(take(n), gen_fractions, gen_nat_complex, gen_complex_)(1, 100),)
            
            # compose(take(n), gen_fractions, gen_field_polynomials, gen_nat_floats, gen_floats)(1., 100.))


@pytest.mark.parametrize("samples", fraction_samples(10))
def test_divmod(samples):
    check_division(samples)
    check_divmod(samples)


@pytest.mark.parametrize("samples", fraction_samples(10))
def test_euclidean_ring(samples):
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", fraction_samples(10))
def test_fields(samples):
    check_fields(samples)


def test_rat_poly():
    coeffs_p = compose(take(3), gen_nat_floats, gen_cycle)((1., 0., -1.))
    coeffs_q = compose(take(2), gen_nat_floats, gen_cycle)((1., 1.))
    coeffs_one = compose(take(1), gen_nat_floats, gen_cycle)((1.,))
    p = FieldPolynomial(*coeffs_p)
    q = FieldPolynomial(*coeffs_q)
    one = FieldPolynomial(*coeffs_one)

    r = Fraction(p, q)
    s = r * Fraction(q, one)
    assert s == Fraction(p, one)


def test_poly_rat():
    n = 3
    coeffs_p = compose(take(n), gen_fractions, gen_nat_ints, gen_cycle)((2, 3))
    coeffs_q = compose(take(n), gen_fractions, gen_nat_ints, gen_cycle)((3, 4))
    coeffs_one = compose(take(1), gen_fractions, gen_nat_ints, gen_cycle)((1,))
    p = Polynomial(*coeffs_p)
    q = Polynomial(*coeffs_q)
    one = Polynomial(*coeffs_one)

    r = p * q
    s = r * one
    assert s == r




