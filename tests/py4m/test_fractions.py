# py4m/tests/test_fractions.py

import pytest

from sandbox.py4m.util.g_samples import (g_ints, g_floats, g_complex_,
                                         g_nat_complex, g_nat_ints, g_nat_floats,
                                         g_fractions, g_polynomials)
from sandbox.py4m.util.utils import compose, take
from tests.py4m.check_properties import check_fields, check_euclidean_rings, check_division_algorithm, check_divmod


# ----- Type/sample groupings -----

def fraction_samples(n: int):
    return (compose(take(n), g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_fractions, g_fractions, g_fractions, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_fractions, g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_fractions, g_fractions, g_nat_floats, g_floats)(10., 20.),
            compose(take(n), g_fractions, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_fractions, g_polynomials, g_nat_floats, g_floats)(1., 10.))


@pytest.mark.parametrize("samples", fraction_samples(5)[-1:])
def test_divmod(samples):
    check_division_algorithm(samples)
    check_divmod(samples)

@pytest.mark.parametrize("samples", fraction_samples(10)[-1:])
def test_euclidean_ring(samples):
    check_euclidean_rings(samples)


@pytest.mark.parametrize("samples", fraction_samples(20)[:-1])
def test_fields(samples):
    check_fields(samples)
