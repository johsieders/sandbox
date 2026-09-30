# tests/py4alg/test_symbolics.py

import pytest
from sympy import Symbol, floor

from sandbox.py4alg.mapper.m_complex import Complex
from sandbox.py4alg.mapper.m_matrix import Matrix
from sandbox.py4alg.mapper.m_polynomial import Polynomial
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.gen_samples import gen_tree, gen_symbolic_
from sandbox.py4alg.util.utils import comparable_works, descent_str, set_test_seed
from sandbox.py4alg.wrapper.s_int import SymbolicInt
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from tests.py4alg.check_protocols import check_axioms


# ----- Type/sample groupings -----

def test_isinstance():
    # NativeInt tests
    n = SymbolicInt('a')
    # Positive assertions
    assert isinstance(n, SymbolicInt)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    # Negative assertions
    assert not comparable_works(n)  # a < b has no truth value (isinstance(n, Comparable) is useless:
    #                                 every object inherits __lt__ from object)
    assert not isinstance(n, EuclideanRing)  # Z[a, b, ...] has no division with remainder
    assert not isinstance(n, Field)  # Integers don't have multiplicative inverses
    assert not isinstance(n, NativeFloat)
    assert not isinstance(n, NativeComplex)


def test_zero_test_is_exact():
    a = SymbolicInt('a')
    one = SymbolicInt.one()
    z = (a + one) * (a + one) - a * a - a - a - one  # zero, although sympy keeps it unexpanded
    assert not z
    assert z == SymbolicInt.zero()
    assert a
    assert Polynomial(one, z) == Polynomial(one)  # the zero leading coefficient is trimmed


def test_divmod():
    a = Symbol('a', integer=True)
    b = Symbol('b', integer=True)
    q, r = divmod(a, b)
    t = q * b + r

    # t == a in symbolic terms
    assert (t - a).rewrite(floor).simplify() == 0


symbols = [chr(i) for i in range(ord('a'), ord('z') + 1)] * 2
sym_int_samples = [SymbolicInt(s) for s in symbols]


def test_polynomial():
    p = Polynomial(*sym_int_samples[:3])
    q = Polynomial(*sym_int_samples[1:4])
    x = SymbolicInt(5)
    check_axioms((p, q))

    assert p(x) + q(x) == (p + q)(x)
    assert p(x) - q(x) == (p - q)(x)
    assert p(x) * q(x) == (p * q)(x)


def test_complex():
    s = Complex(*sym_int_samples[:2])
    t = Complex(*sym_int_samples[1:3])
    u = Complex(*sym_int_samples[2:4])
    check_axioms((s, t, u))


def test_matrix():
    a = Matrix(*sym_int_samples[:9])
    b = Matrix(*sym_int_samples[9:18])
    check_axioms((a, b))


@pytest.mark.timeout(10)
@pytest.mark.parametrize("samples", (sym_int_samples[:10],))
def test_symbolics(samples):
    check_axioms(samples)


# ----- towers over SymbolicInt: Polynomial, Complex, Matrix (the constructors whose bound is Ring) -----
# own settings: exact symbolic arithmetic is slow, depth 3 / N = 3 takes about 8 s on the Mac

SYM_DEPTH = 3
SYM_N = 3
set_test_seed()
sym_towers = gen_tree((gen_symbolic_,), depth=SYM_DEPTH, n=SYM_N)


@pytest.mark.timeout(30)
@pytest.mark.parametrize("samples", sym_towers, ids=[descent_str(s) for s in sym_towers])
def test_symbolic_towers(samples):
    check_axioms(samples)
