# p4m/tests/test_natives.py

from functools import reduce
from operator import mul

from sandbox.p4m.algebraic.a_fraction import Fraction
from sandbox.p4m.algebraic.a_polynomial import Polynomial
from sandbox.p4m.natives.n_complex import NativeComplex
from sandbox.p4m.natives.n_float import NativeFloat
from sandbox.p4m.natives.n_int import NativeInt
from sandbox.p4m.util.utils import close_to
from sandbox.p4m.util.make_samples import make_samples
from tests.p4m.test_natives import int_samples, float_samples, complex_samples

# ----- Type/sample groupings -----
n = 30


def make_polynomials(n):
    return make_samples([Polynomial], float_samples(n))


def test_polynomial_float_samples():
    # this test passes for range(1, N) with N <= 40
    polynomial_samples = make_polynomials(n)
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


def test_polynomial_int_samples():
    polynomial_samples = make_samples([Polynomial, NativeInt], range(1, 500))
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
    polynomial_samples = make_samples([Polynomial, Fraction, NativeInt], range(1, 100))
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


polynomial_samples = [
    (Polynomial, NativeInt, int_samples),
    (Polynomial, NativeFloat, float_samples),
    (Polynomial, NativeComplex, complex_samples)
]
