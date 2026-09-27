# tests/py4alg/test_axioms.py
# Plain vanilla version — descent_str as test ID

# run with pytest tests/py4alg/test_axioms.py -n auto

import pytest

from sandbox.py4alg.util.gen_samples import gen_tree, gen_ints, gen_floats, gen_complex_
from sandbox.py4alg.util.utils import set_test_seed, descent_str
from tests.py4alg.check_protocols import check_axioms

DEPTH = 6
N = 3
set_test_seed()

int_samples = gen_tree((gen_ints,), depth=DEPTH, n=N)
# float_samples = gen_tree((gen_floats,), depth=DEPTH, n=N)
# complex_samples = gen_tree((gen_complex_,), depth=DEPTH, n=N)

float_samples = []
complex_samples = []

TIMEOUT = 10

# Cases that exceed TIMEOUT (coefficient explosion in nested fraction/polynomial GCDs).
# On the Pi, this one ran > 38 min in a full xdist run although its timeout had not fired.
STRESS = {
    "Complex > Matrix > Fraction > FieldPolynomial > Fraction > NativeInt",
}


def with_marks(samples):
    ds = descent_str(samples)
    return pytest.param(samples, marks=pytest.mark.stress if ds in STRESS else (), id=ds)


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("samples", [with_marks(s) for s in int_samples])
def test_int(samples):
    check_axioms(samples)


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("samples", float_samples, ids=[descent_str(s) for s in float_samples])
def test_float(samples):
    check_axioms(samples)


@pytest.mark.timeout(TIMEOUT)
@pytest.mark.parametrize("samples", complex_samples, ids=[descent_str(s) for s in complex_samples])
def test_complex(samples):
    check_axioms(samples)
