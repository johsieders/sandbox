# py4m/tests/test_complex.py

import pytest

from sandbox.py4m.mapper.m_complex import Complex
from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.util.utils import close_to
from tests.py4m.check_properties import check_fields
from tests.py4m.test_fractions import frac_int_samples
from tests.py4m.test_natives import complex_native_samples

# ----- Type/sample groupings -----

N = 20


def complex_float_samples(n):
    return make_samples([Complex], complex_native_samples(n))


def complex_complex_samples(n):
    return make_samples([Complex, Complex], complex_native_samples(n))


def complex_frac_samples(n):
    non_zero_samples = [f for f in frac_int_samples(n) if not close_to(f, f.zero())]
    return make_samples([Complex], non_zero_samples)


def complex_samples(n: int):
    return (complex_float_samples(n),
            complex_complex_samples(n),
            complex_frac_samples(n))


@pytest.mark.parametrize("samples", complex_samples(N))
def test_properties(samples):
    check_fields(samples)
