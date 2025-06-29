# p4m/tests/test_natives.py

from functools import reduce
from operator import mul

from sandbox.p4m.natives.n_complex import NativeComplex
from sandbox.p4m.natives.n_float import NativeFloat
from sandbox.p4m.natives.n_int import NativeInt
from sandbox.p4m.util.utils import close_to
from sandbox.p4m.util.make_samples import make_samples

# ----- Type/sample groupings -----
n = 30


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


def test_int_samples():
    int_samples = make_samples([NativeInt], range(1, 10))
    int_samples_reversed = list(int_samples)
    int_samples_reversed.reverse()
    int_zero = int_samples[0].zero()
    int_one = int_samples[0].one()
    total = sum(int_samples, int_zero)
    total_rev = sum(int_samples_reversed, int_zero)
    assert total == total_rev
    prod = reduce(mul, int_samples, int_one)
    prod_rev = reduce(mul, int_samples_reversed, int_one)
    assert prod == prod_rev


def test_float_samples():
    float_samples = make_samples([NativeFloat], [0.0 + k for k in range(1, 10)])
    float_samples_reversed = list(float_samples)
    float_samples_reversed.reverse()
    float_zero = float_samples[0].zero()
    float_one = float_samples[0].one()
    total = sum(float_samples, float_zero)
    total_rev = sum(float_samples_reversed, float_zero)
    assert total == total_rev
    prod = reduce(mul, float_samples, float_one)
    prod_rev = reduce(mul, float_samples_reversed, float_one)
    assert close_to(prod, prod_rev)


field_samples = [
    (NativeFloat, float_samples(n)),
    (NativeComplex, complex_samples(n))
]

euclidian_ring_samples = (
        [(NativeInt, int_samples(n))] +
        field_samples)
