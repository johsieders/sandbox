# py4m/tests/test_complex.py

import pytest

from sandbox.py4m.util.g_samples import (g_ints, g_floats, g_complex_,
                                         g_nat_complex, g_nat_ints, g_nat_floats,
                                         g_complex, g_fractions)
from sandbox.py4m.util.utils import compose, take
from tests.py4m.check_properties import check_fields


# ----- Type/sample groupings -----

def complex_samples(n: int):
    return (compose(take(n), g_complex, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_complex, g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_complex, g_complex, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_complex, g_fractions, g_nat_ints, g_ints)(10, 20))


@pytest.mark.parametrize("samples", complex_samples(20))
def test_properties(samples):
    check_fields(samples)
