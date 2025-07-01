# py4m/tests/test_natives.py

from functools import reduce
from operator import mul

import pytest

from sandbox.py4m.mapper.m_fraction import Fraction, gcd, ext_gcd
from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.util.utils import close_to
from sandbox.py4m.wrapper.w_complex import NativeComplex
from sandbox.py4m.wrapper.w_float import NativeFloat
from sandbox.py4m.wrapper.w_int import NativeInt
from tests.py4m.test_natives import float_samples, int_samples

# ----- Type/sample groupings -----
@pytest.fixture
def size_n():
    return 5

def test_constructor_with_native_int(size_n):
    my_ints = [[1, 0], [1, 0, 1, 0], [1, 0, -1, 0, 0],[1, 0, 0, -1]]
    my_coeffs = [make_samples([NativeInt], samples) for samples in my_ints]
    ps = [Polynomial(*coeffs) for coeffs in my_coeffs]

    q = Polynomial(*ps)
    for x in range(-size_n, size_n):
        x = NativeInt(x)
        r = lambda x: Polynomial(*(p(x) for p in ps))
        assert r(x)(x) == q(x)

def test_gcd():
    my_ints = [[1, 0, 0, 0, -1], [1, 0, 1]]
    # my_ints = [[1, 1], [2]]
    my_coeffs = [make_samples([NativeInt], samples) for samples in my_ints]
    ps = [Polynomial(*coeffs) for coeffs in my_coeffs]
    a = ps[0]
    b = ps[1]
    g1, g2, g3 = ext_gcd(a, b)

    d = divmod(a, b)

    r = a % b   # r == [1, 1]
    # u, v = a._divmod(b)   # u = [0], v == [1, 1]

    g = gcd(a, b)

    a, b = u, v
    print()
    print(a)
    print(b)


    a = ps[0] // ps[1]
    b = ps[0] % ps[1]
    c = ps[1] // b

    assert a * ps[1] + b == ps[0]
    print()
    print(a)
    print(b)
    print(c)



def test_constructor_with_native_float(size_n):
    my_floats = [[1., 0.], [1., 0., 1., 0.], [1., 0., -1., 0., 0.],[1., 0., 0., -1.]]
    my_coeffs = [make_samples([NativeFloat], samples) for samples in my_floats]
    ps = [Polynomial(*coeffs) for coeffs in my_coeffs]

    q = Polynomial(*ps)
    for x in range(-size_n, size_n):
        x = NativeInt(x)
        r = lambda x: Polynomial(*(p(x) for p in ps))
        assert close_to(r(x)(x), q(x))


from tests.py4m.test_properties import test_euclidean_rings


def test_props():
    test_euclidean_rings(make_samples([Polynomial], int_samples(20)))
    samples = make_samples([Polynomial], float_samples(20))
    test_euclidean_rings(samples)



def test_polynomial_float_samples(size_n,):
    # this test passes for range(1, N) with N <= 40

    samples_rev = list(reversed(samples))
    zero = samples[0].zero()
    one = samples[0].one()
    total = sum(samples, zero)
    total_rev = sum(samples_rev, zero)
    assert close_to(total, total_rev)
    prod = reduce(mul, samples, one)
    prod_rev = reduce(mul, samples_rev, one)
    # assert close_to(prod, prod_rev)
    if not close_to(prod, prod_rev, 1e-7):
        p = iter(prod._coeffs)
        r = iter(prod_rev._coeffs)
        idx = 0
        while True:
            try:
                print(idx, '   ', next(p) - next(r))
                idx += 1
            except StopIteration:
                break


def test_polynomial_int_samples(size_n):
    polynomial_samples = make_samples([Polynomial, NativeInt], range(1, 500))
    polynomial_samples_reversed = list(reversed(polynomial_samples))
    polynomial_zero = polynomial_samples[0].zero()
    polynomial_one = polynomial_samples[0].one()
    total = sum(polynomial_samples, polynomial_zero)
    total_rev = sum(polynomial_samples_reversed, polynomial_zero)
    assert total == total_rev
    prod = reduce(mul, polynomial_samples, polynomial_one)
    prod_rev = reduce(mul, polynomial_samples_reversed, polynomial_one)
    assert prod == prod_rev


def test_polynomial_complex_samples():
    # same problem with complex: ok for N <= 40
    polynomial_samples = make_samples([Polynomial, NativeComplex],
                                      [complex(k, 2 * k) + k for k in range(1, 40)])
    polynomial_samples_reversed = list(polynomial_samples)
    polynomial_samples_reversed.reverse()
    polynomial_zero = polynomial_samples[0].zero()
    polynomial_one = polynomial_samples[0].one()
    total = sum(polynomial_samples, polynomial_zero)
    total_rev = sum(polynomial_samples_reversed, polynomial_zero)
    assert total == total_rev
    prod = reduce(mul, polynomial_samples, polynomial_one)
    prod_rev = reduce(mul, polynomial_samples_reversed, polynomial_one)
    # assert close_to(prod, prod_rev)
    if not close_to(prod, prod_rev):
        p = iter(prod._coeffs)
        r = iter(prod_rev._coeffs)
        idx = 0
        while True:
            try:
                print(idx, '   ', next(p) - next(r))
                idx += 1
            except StopIteration:
                break


def test_polynomial_fraction_int_samples():
    polynomial_samples = make_samples([Polynomial, Fraction, NativeInt], range(1, 10))
    polynomial_samples_reversed = list(polynomial_samples)
    polynomial_samples_reversed.reverse()
    polynomial_zero = polynomial_samples[0].zero()
    polynomial_one = polynomial_samples[0].one()
    total = sum(polynomial_samples, polynomial_zero)
    total_rev = sum(polynomial_samples_reversed, polynomial_zero)
    assert total == total_rev
    prod = reduce(mul, polynomial_samples, polynomial_one)
    prod_rev = reduce(mul, polynomial_samples_reversed, polynomial_one)
    # assert close_to(prod, prod_rev)
    if not close_to(prod, prod_rev):
        p = iter(prod._coeffs)
        r = iter(prod_rev._coeffs)
        idx = 0
        while True:
            try:
                print(idx, '   ', next(p) - next(r))
                idx += 1
            except StopIteration:
                break


polynomial_int_samples = make_samples([Polynomial, NativeInt], range(1, 10))

polynomial_float_samples = make_samples([Polynomial, NativeFloat],
                                        [float(n) for n in range(1, 10)])
polynomial_complex_samples = make_samples([Polynomial, NativeComplex],
                                          [complex(n, n) for n in range(1, 10)])

samples = (polynomial_int_samples +
           polynomial_float_samples +
           polynomial_complex_samples)


@pytest.mark.parametrize("samples", samples)
def test_properties(samples):
    check_euclidian_rings(samples)
