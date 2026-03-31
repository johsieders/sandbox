# py4alg/tests/test_natives.py

import pytest

from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.wrapper.s_int import SymbolicInt
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from tests.py4alg.check_protocols import check_euclidean_rings, check_axioms

from sympy import Symbol, S, core, floor


# ----- Type/sample groupings -----

def test_isinstance():
    # NativeInt tests
    n = SymbolicInt('a')
    # Positive assertions
    assert isinstance(n, SymbolicInt)
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    assert isinstance(n, EuclideanRing)
    # Negative assertions
    assert not isinstance(n, Field)  # Integers don't have multiplicative inverses
    assert not isinstance(n, NativeFloat)
    assert not isinstance(n, NativeComplex)


# def native_samples(n: int):
#     return (compose(take(n), gen_nat_ints, gen_ints)(LB, UB),
#             compose(take(n), gen_nat_ints, gen_nat_ints, gen_ints)(LB, UB),
#             compose(take(n), gen_nat_floats, gen_floats)(LB, UB),
#             compose(take(n), gen_nat_floats, gen_nat_floats, gen_floats)(LB, UB),
#             compose(take(n), gen_nat_complex, gen_complex_)(LB, UB),
#             compose(take(n), gen_nat_complex, gen_nat_complex, gen_complex_)(LB, UB))

symbols = [chr(i) for i in range(ord('a'), ord('z') + 1)]
sym_int_samples = [SymbolicInt(s) for s in symbols]


def _test_symb1():
    seven = SymbolicInt(7)
    eight = SymbolicInt(8)
    a = SymbolicInt('a')
    b = SymbolicInt('b')
    print()
    print(seven + eight)

    q, r = divmod(a, b)
    t = q * b + r

    print()
    print(q, r, t)
    print(t == a)
    
def _test_symb2():
    a = Symbol('a', integer=True)
    b = Symbol('b', integer=True)
    q, r = divmod(a, b)
    t = q * b + r
    
    print()
    print(q, r, t)
    print(t == a)
    print((t - a).rewrite(floor).simplify())
 
@pytest.mark.timeout(5)
@pytest.mark.parametrize("samples", (sym_int_samples[:3],))
def test_symbolics(samples):
    check_axioms(samples)
