# p4m/tests/test_fractions.py

from _operator import mul
from functools import reduce

from sandbox.p4m.algebraic.a_fraction import Fraction
from sandbox.p4m.algebraic.a_polynomial import Polynomial
from sandbox.p4m.natives.n_int import NativeInt
from sandbox.p4m.util.utils import close_to
from sandbox.p4m.util.make_samples import make_samples
from tests.p4m.test_natives import int_samples

# ----- Type/sample groupings -----

n = 30


def fraction_samples(n):
    return make_samples([Fraction], int_samples(2 * n))


def test_fractions():
    frac_samples = fraction_samples(n)
    frac_samples_reversed = list(frac_samples)
    frac_samples_reversed.reverse()
    frac_zero = frac_samples[0].zero()
    frac_one = frac_samples[0].one()
    total = sum(frac_samples, frac_zero)
    total_rev = sum(frac_samples_reversed, frac_zero)
    assert total == total_rev
    prod = reduce(mul, frac_samples, frac_one)
    prod_rev = reduce(mul, frac_samples_reversed, frac_one)
    assert close_to(prod, prod_rev)


def _test_fraction_polynomial_int_samples():
    # todo
    # fraction_samples = make_composite_samples([Fraction, Polynomial, IntNative], range(1, 10))
    polynomial_samples = make_samples([Polynomial, NativeInt], range(1, 10))
    fraction_samples = make_samples([Fraction], polynomial_samples)

    fraction_samples_reversed = list(fraction_samples)
    fraction_samples_reversed.reverse()
    fraction_zero = fraction_samples[0].zero()
    fraction_one = fraction_samples[0].one()
    total = sum(fraction_samples, fraction_zero)
    total_rev = sum(fraction_samples_reversed, fraction_zero)
    assert total == total_rev
    prod = reduce(mul, fraction_samples, fraction_one)
    prod_rev = reduce(mul, fraction_samples_reversed, fraction_one)
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
