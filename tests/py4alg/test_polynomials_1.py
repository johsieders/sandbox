# py4alg/tests/test_polynomials.py

import pytest

from typing import Any, List, Sequence, Tuple

from tests.py4alg.check_properties import check_gcd_commutativity
from tests.py4alg.check_properties import check_gcd_associativity
from sandbox.py4alg.mapper import Polynomial, FieldPolynomial
from sandbox.py4alg.util.primes import gcd
from sandbox.py4alg.util.gen_samples import (def_nat_complex, def_nat_ints, def_nat_floats,
                                             def_fractions, def_polynomials, def_field_polynomials)
from sandbox.py4alg.wrapper.w_float import NativeFloat
from tests.py4alg.check_properties import check_rings, check_euclidean_rings, check_fields

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
    check_euclidean_rings(ints)

    poly_samples_int = def_polynomials(*to_coeffs(ints, (1, 1, 3)))
    check_rings(poly_samples_int)

    floats = def_nat_floats(0., 7., 1., 0., 1.)
    poly_samples_float = def_field_polynomials(*to_coeffs(floats, (1, 1, 3)))
    check_euclidean_rings(poly_samples_float)


def test_poly_gcd():
    floats_1 = def_nat_floats(0., 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 6.0, 7.0, 8.0, 9.0, 4.0, 5.0, 6.0, 7.0)
    floats_2 = def_nat_floats(-1., 1., -1., 1., 1., 1., 1., 1., -1., 1., -1., 1., 1., 1., 1., 1.)

    poly_1 = def_field_polynomials(*to_coeffs(floats_1, (4, 4, 4, 4)))
    poly_2 = def_field_polynomials(*to_coeffs(floats_2, (4, 4, 4, 4)))

    check_euclidean_rings(poly_1)
    check_euclidean_rings(poly_2)


def test_d():
    ints = def_nat_ints(0, 3, 4, 5, 6, 7, 8, 9, 6, 7, 8, 9, 4, 5, 6, 7)
    floats = def_nat_floats(0., 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 6.0, 7.0, 8.0, 9.0, 4.0, 5.0, 6.0, 7.0)
    complexs = def_nat_complex(0+0j, 3.0+1j, 4.0+2j, 5+0j, 0+0j, 3.0+1j, 4.0+2j, 5+0j, 0+0j, 3.0+1j, 4.0+2j, 5+0j, 4.0+2j, 5+0j, 0+0j, 3.0+1j)

    fractions_int = def_fractions(*to_pairs(ints))
    fractions_float = def_fractions(*to_pairs(floats))
    fractions_complex = def_fractions(*to_pairs(complexs))
    fractions_fractions_int = def_fractions(*to_pairs(fractions_int))

    polynomials_int = def_polynomials(*to_coeffs(ints, (4, 4, 4, 4)))
    polynomials_float = def_field_polynomials(*to_coeffs(floats, (4, 4, 4, 4)))
    polynomials_complex = def_field_polynomials(*to_coeffs(complexs, (4, 4, 4, 4)))
    polynomials_fractions_int = def_field_polynomials(*to_coeffs(fractions_int, (4, 4)))
    polynomials_fractions_float = def_field_polynomials(*to_coeffs(fractions_float, (4, 4)))
    polynomials_fractions_complex = def_field_polynomials(*to_coeffs(fractions_complex, (4, 4)))
    polynomials_polynomials_int = def_polynomials(*to_coeffs(polynomials_int, (4, 4)))
    polynomials_polynomials_float = def_field_polynomials(*to_coeffs(polynomials_float, (4, 4)))

    fractions_polynomials_float = def_fractions(*to_pairs(polynomials_float))
    fractions_polynomials_complex = def_fractions(*to_pairs(polynomials_complex))

    check_fields(floats)
    check_fields(complexs)
    check_fields(fractions_int)
    check_fields(fractions_fractions_int)
    check_fields(fractions_float)
    check_fields(fractions_complex)

    check_euclidean_rings(ints)
    check_euclidean_rings(polynomials_float)
    check_euclidean_rings(polynomials_complex)
    check_euclidean_rings(polynomials_fractions_float)
    check_euclidean_rings(polynomials_fractions_complex)
    check_euclidean_rings(polynomials_polynomials_float)

    # check_euclidean_rings(fractions_polynomials_float)
    # check_euclidean_rings(fractions_polynomials_complex)

    check_rings(polynomials_int)
    check_rings(polynomials_polynomials_int)
    check_rings(polynomials_fractions_int)
