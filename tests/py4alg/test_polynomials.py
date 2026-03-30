# py4alg/tests/test_polynomials.py

from typing import Any, List, Sequence, Tuple

import pytest

from sandbox.py4alg.mapper import Polynomial, FieldPolynomial
from sandbox.py4alg.util.def_samples import (def_nat_ints, def_nat_floats, def_polynomials, def_field_polynomials)
from sandbox.py4alg.util.gen_samples import (gen_ints, gen_floats, gen_complex_,
                                             gen_nat_complex, gen_nat_ints, gen_nat_floats,
                                             gen_fractions, gen_polynomials, gen_field_polynomials)
from sandbox.py4alg.util.primes import gcd
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_float import NativeFloat
from tests.py4alg.check_protocols import check_any


def to_pairs(xs: Sequence[Any]) -> List[Tuple[Any, Any]]:
    return list(zip(xs[::2], xs[1::2]))


def to_coeffs(xs: Sequence[Any], cs: Sequence[int]) -> List[Sequence[Any]]:
    result = []
    cursor = 0
    for c in cs:
        d = min(cursor + c, len(xs))
        result.append(xs[cursor:d])
        cursor += c
        if cursor >= len(xs):
            break
    return result


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


def test_gcd_basics():
    ints = def_nat_ints(0, 7, 17, 27, 37)
    check_any(ints)

    poly_samples_int = def_polynomials(*to_coeffs(ints, (1, 1, 3)))
    check_any(poly_samples_int)

    floats = def_nat_floats(0., 7., 1., 0., 1.)
    poly_samples_float = def_field_polynomials(*to_coeffs(floats, (1, 1, 3)))
    check_any(poly_samples_float)


def test_poly_gcd():
    floats_1 = def_nat_floats(0., 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 6.0, 7.0, 8.0, 9.0, 4.0, 5.0, 6.0, 7.0)
    floats_2 = def_nat_floats(-1., 1., -1., 1., 1., 1., 1., 1., -1., 1., -1., 1., 1., 1., 1., 1.)

    poly_1 = def_field_polynomials(*to_coeffs(floats_1, (4, 4, 4, 4)))
    poly_2 = def_field_polynomials(*to_coeffs(floats_2, (4, 4, 4, 4)))

    check_any(poly_1)
    check_any(poly_2)


# ----- Type/sample groupings -----
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
# samples 0 and 1 are non-euclidean rings
def test_any(samples):
    check_any(samples)


def poly_table(n):
    return zip(poly_samples(n), poly_args(n))


@pytest.mark.parametrize("samples, args", poly_table(100))
def test_poly_poly(samples, args):
    q = Polynomial(*samples)
    for x in args:
        r = lambda x: Polynomial(*(p(x) for p in samples))
        assert r(x)(x) == q(x)
