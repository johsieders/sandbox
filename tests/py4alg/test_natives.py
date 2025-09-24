# py4alg/tests/test_natives.py

import pytest

from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.util.g_samples import g_ints, g_floats, g_complex_
from sandbox.py4alg.util.g_samples import g_nat_floats, g_nat_complex, g_nat_ints
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_int import NativeInt
from tests.py4alg.check_properties import check_euclidean_rings, check_fields


# ----- Type/sample groupings -----

def native_samples(n: int):
    return (compose(take(n), g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_nat_ints, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_nat_floats, g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_nat_complex, g_nat_complex, g_complex_)(10, 20))


@pytest.mark.parametrize("samples", native_samples(40))
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", native_samples(40)[2:])
def test_fields(samples):
    check_fields(samples)


def test_xx():
    n = NativeInt(4)
    b = isinstance(n, NativeInt)
    c = isinstance(n, EuclideanRing)
    # d = issubclass(NativeInt, EuclideanRing) // does not work
    print()
    print(b, c)
