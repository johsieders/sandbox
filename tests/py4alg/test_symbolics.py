# py4alg/tests/test_natives.py

import pytest
from sympy import Symbol, floor

from sandbox.py4alg.mapper.m_complex import Complex
from sandbox.py4alg.mapper.m_matrix import Matrix
from sandbox.py4alg.mapper.m_polynomial import Polynomial
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
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
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    # Negative assertions
    assert not isinstance(n, EuclideanRing)  # no euclidean_function on symbolic expressions
    assert not isinstance(n, Field)  # Integers don't have multiplicative inverses
    assert not isinstance(n, NativeFloat)
    assert not isinstance(n, NativeComplex)


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
