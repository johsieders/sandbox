# py4m/tests/test_natives.py

import pytest

from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.wrapper.w_complex import NativeComplex
from sandbox.py4m.wrapper.w_float import NativeFloat
from sandbox.py4m.wrapper.w_int import NativeInt
from tests.py4m.check_properties import check_euclidean_rings, check_fields

# ----- Type/sample groupings -----

N = 30


def int_samples(n: int):
    return make_samples([NativeInt], range(-n, n))


def float_samples(n: int):
    return make_samples([NativeFloat], [float(x) for x in range(-n, n)])


def complex_native_samples(n: int):
    return make_samples([NativeComplex], [complex(x, x) for x in range(-n, n)])


def native_samples(n: int):
    return (int_samples(n),
            float_samples(n),
            complex_native_samples(n))


@pytest.mark.parametrize("samples", native_samples(N))
def test_euclidean_rings(samples):
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", native_samples(N)[1:])
def test_fields(samples):
    check_fields(samples)
