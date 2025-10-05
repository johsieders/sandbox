# py4alg/tests/test_natives.py

import pytest

from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.g_samples import g_ints, g_floats, g_complex_
from sandbox.py4alg.util.g_samples import g_nat_floats, g_nat_complex, g_nat_ints
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt
from tests.py4alg.check_properties import check_euclidean_rings, check_fields, check_comparables


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


def native_samples(n: int):
    return (compose(take(n), g_nat_ints, g_ints)(0, 20),
            compose(take(n), g_nat_ints, g_nat_ints, g_ints)(0, 20),
            compose(take(n), g_nat_floats, g_floats)(0, 20),
            compose(take(n), g_nat_floats, g_nat_floats, g_floats)(0, 20),
            compose(take(n), g_nat_complex, g_complex_)(0, 20),
            compose(take(n), g_nat_complex, g_nat_complex, g_complex_)(0, 20))


@pytest.mark.parametrize("samples", native_samples(40)[:4])
def test_comparables(samples):
    check_comparables(samples)


@pytest.mark.parametrize("samples", native_samples(40))
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", native_samples(40)[2:])
def test_fields(samples):
    check_fields(samples)


@pytest.mark.parametrize("samples", native_samples(20))
def test_gcd(samples):
    for a in samples:
        for b in samples:
            g = a.gcd(b)
            assert not g or a == a // g * g
            assert not g or b == b // g * g
