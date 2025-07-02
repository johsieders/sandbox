# py4m/tests/test_polynomials.py

import pytest

from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.util.utils import close_to
from sandbox.py4m.wrapper.w_int import NativeInt
from tests.py4m.check_properties import check_euclidean_rings
from tests.py4m.test_fractions import frac_int_samples
from tests.py4m.test_natives import float_samples, complex_native_samples

# ----- Type/sample groupings -----


N = 10


# table = [
#     [NativeInt, [[1, 0], [1, 0, 1, 0], [1, 0, -1, 0, 0], [1, 0, 0, -1]]],
#     [NativeFloat, [[1., 0.], [1., 0., 1., 0.], [1., 0., -1., 0., 0.], [1., 0., 0., -1.]]],
#     [NativeComplex, [complex(a, b) for a, b in [[1., 0.], [1., 0.], [1., 0.], [1., 0., 0., -1.]]]]
# ]


# poly_table1 = [
#     [[[1, 0], [1, 0, 1, 0], [1, 0, -1, 0, 0], [1, 0, 0, -1]], range(-N, N)],
#     [NativeFloat, [[1., 0.], [1., 0., 1., 0.], [1., 0., -1., 0., 0.], [1., 0., 0., -1.]]],
#     [NativeComplex, [complex(a, b) for a, b in [[1., 0.], [1., 0.], [1., 0.], [1., 0., 0., -1.]]]]
# ]


def poly_float_samples(n):
    return make_samples([Polynomial], float_samples(n))


def poly_complex_samples(n):
    return make_samples([Polynomial], complex_native_samples(n))


def poly_frac_samples(n):
    non_zero_samples = [f for f in frac_int_samples(n) if not close_to(f, f.zero())]
    return make_samples([Polynomial], non_zero_samples)


def poly_poly_samples(n):
    return make_samples([Polynomial, Polynomial], float_samples(10))


def poly_samples(n: int):
    return (
        poly_float_samples(n),
        poly_complex_samples(n),
        poly_frac_samples(n))


@pytest.mark.parametrize("samples", poly_samples(N))
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


def poly_table(n):
    return ([poly_float_samples(n), float_samples(n)],
            [poly_complex_samples(n), complex_native_samples(n)],
            [poly_frac_samples(n), frac_int_samples(n)])

@pytest.mark.parametrize("samples,args", poly_table(N))
def test_poly_poly(args, samples):
    q = Polynomial(*samples)
    for x in args:
        r = lambda x: Polynomial(*(p(x) for p in samples))
        y = r(x)(x)
        z = q(x)
        assert close_to(y, z)



# def _test_gcd():
#     my_floats_1 = [[1., 1.], [1.]]  # [1., 1.]        [1., 1.]
#     my_floats_2 = [[1., 1.], [1., -1.]]  # [1.]            [1., -1.]
#     my_floats_3 = [[-1., 0., 1.], [-1., 1.]]  # [-1., 1.]      [-1., 1.]
#     my_floats_4 = [[1., -2., 1.], [-1., 0., 1.]]  # [-1., 1.]    [-2., 2.]
#     my_floats_5 = [[1., 0., 1.], [1., 1.]]  # [1.]         [1., 1.]
#     my_floats_6 = [[1., 1.], [1., 0., 1.]]  # [1.]          [1., 1.]
#     my_floats_7 = [[0., -1., 0., 1.], [-1., 0., 1.]]  # [-1., 0., 1.]          [1., 1.]
#
#     my_coeffs = [make_samples([NativeFloat], samples) for samples in my_floats_2]
#     ps = [Polynomial(*coeffs) for coeffs in my_coeffs]
#     a = ps[0]
#     b = ps[1]
#     d = a // b
#     r = a % b
#     g0 = gcd(a, b)
#     g1, g2, g3 = ext_gcd(a, b)
#
#     print()
#     print(d)
#     print(r)
#     print(g0)
#     print(g1)
#
#     pass
# d = divmod(a, b)
#
# r = a % b   # r == [1, 1]
# # u, v = a._divmod(b)   # u = [0], v == [1, 1]
#
# g = gcd(a, b)
#
# a, b = u, v
# print()
# print(a)
# print(b)
#
#
# a = ps[0] // ps[1]
# b = ps[0] % ps[1]
# c = ps[1] // b

# assert a * ps[1] + b == ps[0]
# print()
# print(a)
# print(b)
# print(c)

# def _test_props():
#     test_euclidean_rings(make_samples([Polynomial], int_samples(20)))
#     samples = make_samples([Polynomial], float_samples(20))
#     test_euclidean_rings(samples)
#

# def test_polynomial_int_samples(size_n):
#     polynomial_samples = make_samples([Polynomial, NativeInt], range(1, 500))
#     polynomial_samples_reversed = list(reversed(polynomial_samples))
#     polynomial_zero = polynomial_samples[0].zero()
#     polynomial_one = polynomial_samples[0].one()
#     total = sum(polynomial_samples, polynomial_zero)
#     total_rev = sum(polynomial_samples_reversed, polynomial_zero)
#     assert total == total_rev
#     prod = reduce(mul, polynomial_samples, polynomial_one)
#     prod_rev = reduce(mul, polynomial_samples_reversed, polynomial_one)
#     assert prod == prod_rev


# def test_polynomial_complex_samples():
#     # same problem with complex: ok for N <= 40
#     polynomial_samples = make_samples([Polynomial, NativeComplex],
#                                       [complex(k, 2 * k) + k for k in range(1, 40)])
#     polynomial_samples_reversed = list(polynomial_samples)
#     polynomial_samples_reversed.reverse()
#     polynomial_zero = polynomial_samples[0].zero()
#     polynomial_one = polynomial_samples[0].one()
#     total = sum(polynomial_samples, polynomial_zero)
#     total_rev = sum(polynomial_samples_reversed, polynomial_zero)
#     assert total == total_rev
#     prod = reduce(mul, polynomial_samples, polynomial_one)
#     prod_rev = reduce(mul, polynomial_samples_reversed, polynomial_one)
#     # assert close_to(prod, prod_rev)
#     if not close_to(prod, prod_rev):
#         p = iter(prod._coeffs)
#         r = iter(prod_rev._coeffs)
#         idx = 0
#         while True:
#             try:
#                 print(idx, '   ', next(p) - next(r))
#                 idx += 1
#             except StopIteration:
#                 break


# def test_polynomial_fraction_int_samples():
#     polynomial_samples = make_samples([Polynomial, Fraction, NativeInt], range(1, 10))
#     polynomial_samples_reversed = list(polynomial_samples)
#     polynomial_samples_reversed.reverse()
#     polynomial_zero = polynomial_samples[0].zero()
#     polynomial_one = polynomial_samples[0].one()
#     total = sum(polynomial_samples, polynomial_zero)
#     total_rev = sum(polynomial_samples_reversed, polynomial_zero)
#     assert total == total_rev
#     prod = reduce(mul, polynomial_samples, polynomial_one)
#     prod_rev = reduce(mul, polynomial_samples_reversed, polynomial_one)
#     # assert close_to(prod, prod_rev)
#     if not close_to(prod, prod_rev):
#         p = iter(prod._coeffs)
#         r = iter(prod_rev._coeffs)
#         idx = 0
#         while True:
#             try:
#                 print(idx, '   ', next(p) - next(r))
#                 idx += 1
#             except StopIteration:
#                 break
#
#
# polynomial_int_samples = make_samples([Polynomial, NativeInt], range(1, 10))
#
# polynomial_float_samples = make_samples([Polynomial, NativeFloat],
#                                         [float(n) for n in range(1, 10)])
# polynomial_complex_samples = make_samples([Polynomial, NativeComplex],
#                                           [complex(n, n) for n in range(1, 10)])
#
# samples = (polynomial_int_samples +
#            polynomial_float_samples +
#            polynomial_complex_samples)
#
#
# @pytest.mark.parametrize("samples", samples)
# def test_properties(samples):
#     check_euclidian_rings(samples)
