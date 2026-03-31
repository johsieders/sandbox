# py4alg/tests/test_natives.py

import pytest

from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.gen_samples import gen_ints, gen_floats, gen_complex_
from sandbox.py4alg.util.gen_samples import gen_nat_floats, gen_nat_complex, gen_nat_ints
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt
from tests.py4alg.check_protocols import check_axioms


# ----- Type/sample groupings -----

def test_isinstance():
    # NativeInt tests
    n = NativeInt(4)
    # Positive assertions
    assert isinstance(n, NativeInt)
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    assert isinstance(n, EuclideanRing)
    # Negative assertions
    assert not isinstance(n, Field)  # Integers don't have multiplicative inverses
    assert not isinstance(n, NativeFloat)
    assert not isinstance(n, NativeComplex)

    # NativeFloat tests
    n = NativeFloat(4.)
    # Positive assertions
    assert isinstance(n, NativeFloat)
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    assert isinstance(n, EuclideanRing)
    assert isinstance(n, Field)  # Floats have division
    # Negative assertions
    assert not isinstance(n, NativeInt)
    assert not isinstance(n, NativeComplex)

    # NativeComplex tests
    n = NativeComplex(complex(4., 2.))
    # Positive assertions
    assert isinstance(n, NativeComplex)
    assert isinstance(n, Comparable)
    assert isinstance(n, AbelianGroup)
    assert isinstance(n, Ring)
    assert isinstance(n, EuclideanRing)
    assert isinstance(n, Field)  # Complex numbers have division
    # Negative assertions
    assert not isinstance(n, NativeInt)
    assert not isinstance(n, NativeFloat)


N = 50
LB = 0
UB = 20


def native_samples(n: int):
    return (compose(take(n), gen_nat_ints, gen_ints)(LB, UB),
            compose(take(n), gen_nat_ints, gen_nat_ints, gen_ints)(LB, UB),
            compose(take(n), gen_nat_floats, gen_floats)(LB, UB),
            compose(take(n), gen_nat_floats, gen_nat_floats, gen_floats)(LB, UB),
            compose(take(n), gen_nat_complex, gen_complex_)(LB, UB),
            compose(take(n), gen_nat_complex, gen_nat_complex, gen_complex_)(LB, UB))


@pytest.mark.parametrize("samples", native_samples(N))
def test_any(samples):
    check_axioms(samples)
