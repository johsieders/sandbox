# py4alg/tests/test_polynomials.py

import pytest

from sandbox.py4alg.mapper import FieldPolynomial
from sandbox.py4alg.util.def_samples import (def_nat_ints, def_nat_floats, def_nat_complex, def_fractions,
                                             def_polynomials, def_field_polynomials, to_pairs, to_coeffs)
from sandbox.py4alg.util.primes import gcd
from sandbox.py4alg.wrapper.w_float import NativeFloat
from tests.py4alg.check_protocols import check_any


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


ints = def_nat_ints(0, 3, 4, 5, 6, 7, 8, 9, 6, 7, 8, 9, 4, 5, 6, 7)
floats = def_nat_floats(0., 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 6.0, 7.0, 8.0, 9.0, 4.0, 5.0, 6.0, 7.0)
complexs = def_nat_complex(0 + 0j, 3.0 + 1j, 4.0 + 2j, 5 + 0j, 0 + 0j, 3.0 + 1j, 4.0 + 2j, 5 + 0j, 0 + 0j, 3.0 + 1j,
                           4.0 + 2j, 5 + 0j, 4.0 + 2j, 5 + 0j, 0 + 0j, 3.0 + 1j)

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

samples = (ints, floats, complexs, fractions_int, fractions_fractions_int,
           fractions_float, fractions_complex, polynomials_float, polynomials_complex, polynomials_polynomials_float,  
           polynomials_fractions_float,
           polynomials_fractions_complex, 
           # fractions_polynomials_float,
           # fractions_polynomials_complex
           )


@pytest.mark.parametrize("samples", samples)
def test_any(samples):
    check_any(samples)
