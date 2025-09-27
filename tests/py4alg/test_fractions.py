# py4alg/tests/test_fractions.py

from sandbox.py4alg.mapper.m_fraction import Fraction
from sandbox.py4alg.mapper.m_polynomial import Polynomial
from sandbox.py4alg.util.g_samples import (g_cycle, g_ints, g_floats, g_complex_,
                                           g_nat_complex, g_nat_ints, g_nat_floats,
                                           g_fractions, g_polynomials)
from sandbox.py4alg.util.utils import compose, take


# ----- Type/sample groupings -----

def fraction_samples(n: int):
    return (compose(take(n), g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_fractions, g_fractions, g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_fractions, g_nat_floats, g_floats)(10., 20.),
            compose(take(n), g_fractions, g_fractions, g_nat_floats, g_floats)(10., 20.),
            compose(take(n), g_fractions, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_fractions, g_polynomials, g_nat_floats, g_floats)(1., 10.))


# @pytest.mark.parametrize("samples", fraction_samples(3)[-1:])
# def test_divmod(samples):
#     check_division_algorithm(samples)
#     check_divmod(samples)


# @pytest.mark.parametrize("samples", fraction_samples(10)[-1:])
# def test_euclidean_ring(samples):
#     check_euclidean_rings(samples)
#
#
# @pytest.mark.parametrize("samples", fraction_samples(20)[:-1])
# def test_fields(samples):
#     check_fields(samples)

# todo
def test_rat_poly():
    coeffs_p = compose(take(3), g_nat_floats, g_cycle)((1., 0., -1.))
    coeffs_q = compose(take(2), g_nat_floats, g_cycle)((1., 1.))
    p = Polynomial(*coeffs_p)
    q = Polynomial(*coeffs_q)
    r = Fraction(p, q)

    print()
    print(coeffs_p)
    print(coeffs_q)
    print(p)
    print(q)
    print(r)
    print(r * q)


def test_poly_rat():
    n = 8
    rs = compose(take(n), g_fractions, g_nat_ints, g_cycle)((2,))
    p = Polynomial(*rs)

    print()
    print(rs)
    print(p)
