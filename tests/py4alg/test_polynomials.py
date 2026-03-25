# py4alg/tests/test_polynomials.py

import pytest

from sandbox.py4alg.mapper import Polynomial, FieldPolynomial
from sandbox.py4alg.util.primes import gcd
from sandbox.py4alg.util.gen_samples import (gen_ints, gen_floats, gen_complex_,
                                             gen_nat_complex, gen_nat_ints, gen_nat_floats,
                                             gen_fractions, gen_polynomials, gen_field_polynomials)
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_float import NativeFloat
from tests.py4alg.check_properties import check_rings, check_euclidean_rings


# ----- Type/sample groupings -----
def test_gcd():
    p = FieldPolynomial(NativeFloat(0.))
    q = FieldPolynomial(NativeFloat(2.), NativeFloat(7.))
    g = gcd(p, q)
    assert gcd(p, q).normalize() == q.normalize()
    assert gcd(q, p).normalize() == q.normalize()
    assert p == p // g * g
    assert q == q // g * g

    p = FieldPolynomial(NativeFloat(1.), NativeFloat(0.), NativeFloat(-1.))
    q = FieldPolynomial(NativeFloat(1.), NativeFloat(1.))
    g = gcd(q, p)
    assert g.normalize() == q.normalize()
    assert p == p // g * g
    assert q == q // g * g


def poly_samples(n: int):
    return (compose(take(n), gen_polynomials, gen_nat_ints, gen_ints)(10, 20),
            compose(take(n), gen_polynomials, gen_polynomials, gen_polynomials, gen_nat_ints, gen_ints)(10, 20),
            compose(take(n), gen_field_polynomials, gen_nat_floats, gen_floats)(10, 20),
            compose(take(n), gen_field_polynomials, gen_nat_complex, gen_complex_)(10, 20),
            compose(take(n), gen_field_polynomials, gen_fractions, gen_nat_ints, gen_ints)(10, 20),
            compose(take(n), gen_field_polynomials, gen_fractions, gen_nat_floats, gen_floats)(10., 20.))


def poly_args(n):
    """
    this list contains the arguments for the polynomials from poly_samples
    """
    return (compose(take(n), gen_nat_ints, gen_ints)(10, 20),
            compose(take(n), gen_nat_ints, gen_ints)(10, 20),
            compose(take(n), gen_nat_floats, gen_floats)(10, 20),
            compose(take(n), gen_nat_complex, gen_complex_)(10, 20),
            compose(take(n), gen_fractions, gen_nat_ints, gen_ints)(10, 20),
            compose(take(n), gen_fractions, gen_nat_floats, gen_floats)(10, 20))


@pytest.mark.parametrize("samples", poly_samples(2)[2:])
def test_gcd(samples):
    for p in samples:
        for q in samples:
            g = gcd(p, q)
            assert p == p // g * g
            assert q == q // g * g


@pytest.mark.parametrize("samples", poly_samples(10))
def test_rings(samples):
    check_rings(samples)


@pytest.mark.parametrize("samples", poly_samples(10)[2:])
# samples 0 and 1 are non-euclidean rings
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


def poly_table(n):
    return zip(poly_samples(n), poly_args(n))


@pytest.mark.parametrize("samples, args", poly_table(100))
def test_poly_poly(samples, args):
    q = Polynomial(*samples)
    for x in args:
        r = lambda x: Polynomial(*(p(x) for p in samples))
        assert r(x)(x) == q(x)
