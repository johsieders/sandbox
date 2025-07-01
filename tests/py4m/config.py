# config.py

from sandbox.py4m.util.make_samples import E, F, R
from tests.py4m.test_complex import complex_samples as complex_algs
from tests.py4m.test_fractions import fraction_samples as fractions
from tests.py4m.test_matrices import matrix_samples as matrices
from tests.py4m.test_natives import (
    int_samples as ints,
    float_samples as floats,
    complex_samples as complex_nats)
from tests.py4m.test_polynomials import polynomial_samples as polynomials

samples = {R: [matrices],
           E: [ints, fractions, polynomials],
           F: [floats, complex_nats, complex_algs]}

# from .native_samples import (
#     RING_SAMPLES as NATIVE_RING_SAMPLES,
#     EUCLIDIAN_RING_SAMPLES as NATIVE_EUCLIDIAN_RING_SAMPLES,
#     FIELD_SAMPLES as NATIVE_FIELD_SAMPLES,
# )
#
# from .handmade_samples import (
#     RING_SAMPLES as HANDMADE_RING_SAMPLES,
#     EUCLIDIAN_RING_SAMPLES as HANDMADE_EUCLIDIAN_RING_SAMPLES,
#     FIELD_SAMPLES as HANDMADE_FIELD_SAMPLES,
# )
#
# # List all sets you want to test; you can add as many as you like!
# SAMPLE_SETS = [
#     ("native", NATIVE_RING_SAMPLES, NATIVE_EUCLIDIAN_RING_SAMPLES, NATIVE_FIELD_SAMPLES),
#     ("handmade", HANDMADE_RING_SAMPLES, HANDMADE_EUCLIDIAN_RING_SAMPLES, HANDMADE_FIELD_SAMPLES),
#     # Add more sample sets here as needed
# ]

# @pytest.fixture(params=SAMPLE_SETS, ids=lambda x: x[0])
# def sample_set(request):
#     """Fixture that supplies (name, RING_SAMPLES, EUCLIDIAN_RING_SAMPLES, FIELD_SAMPLES)."""
#     return request.param
