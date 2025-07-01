# py4m/tests/test_natives.py

from _operator import mul
from functools import reduce

from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.wrapper.w_complex import NativeComplex
from sandbox.py4m.wrapper.w_float import NativeFloat
from sandbox.py4m.wrapper.w_int import NativeInt

from tests.py4m.test_properties import test_euclidean_rings, test_fields

# ----- Type/sample groupings -----
n = 30

def multiply(factors, start=1):
    return reduce(mul, factors, start)

def int_samples(N: int) -> list[NativeInt]:
    return [NativeInt(k) for k in range(-N, N + 1)]


def float_samples(N: int) -> list[NativeFloat]:
    samples = [NativeFloat(float(k)) for k in range(-N, N + 1)]
    samples += [NativeFloat(k / 3.0) for k in range(-N, N + 1) if k != 0]
    return samples


def complex_samples(N: int) -> list[NativeComplex]:
    floats = float_samples(N)
    return [
        NativeComplex(complex(f.to_float(), g.to_float()))
        for f in floats
        for g in floats
        if abs(f.to_float()) + abs(g.to_float()) != 0  # Exclude 0+0j if you wish
    ]


def test_add(samples):
    samples_rev = reversed(list(samples))
    zero = samples[0].zero()
    total = sum(samples, zero)
    total_rev = sum(samples_rev, zero)
    assert total == total_rev


def test_mul(samples):
    samples_rev = reversed(list(samples))
    one = samples[0].one()
    prod = multiply(samples, start=one)
    prod_rev = multiply(samples_rev, start=one)
    assert prod == prod_rev


def test_add_mul():
    int_samples = make_samples([NativeInt], range(1, 30))
    float_samples = make_samples([NativeFloat], [float(x) for x in range(1, 30)])
    complex_samples = make_samples([NativeComplex], [complex(x, x) for x in range(1, 30)])
    test_add(int_samples)
    test_add(float_samples)
    test_add(complex_samples)
    test_mul(int_samples)
    test_mul(float_samples)
    test_mul(complex_samples)


def test_natives():
    int_samples = make_samples([NativeInt], range(1, 30))
    float_samples = make_samples([NativeFloat], [float(x) for x in range(1, 30)])
    complex_samples = make_samples([NativeComplex], [complex(x, x) for x in range(1, 30)])
    test_euclidean_rings(int_samples)
    test_fields(float_samples)
    test_fields(complex_samples)


