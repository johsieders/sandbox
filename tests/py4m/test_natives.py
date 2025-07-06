# py4m/tests/test_natives.py

import pytest

from sandbox.py4m.util.g_samples import g_ints, g_floats, g_complex_
from sandbox.py4m.util.g_samples import g_nat_floats, g_nat_complex, g_nat_ints
from sandbox.py4m.util.utils import compose, take
from tests.py4m.check_properties import check_euclidean_rings, check_fields


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
