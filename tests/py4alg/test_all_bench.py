# tests/py4alg/test_all_bench.py
# Benchmark version — use with: pytest tests/py4alg/test_all_bench.py --benchmark-only --benchmark-sort=mean

import pytest

from sandbox.py4alg.util.gen_samples import gen_gen, gen_ints, gen_floats, gen_complex_
from sandbox.py4alg.util.utils import set_test_seed, compose, descent_str
from tests.py4alg.check_protocols import check_any

DEPTH = 2
N = 3

set_test_seed()


int_samples = [compose(*t)(1, 10) for t in gen_gen((gen_ints,), depth=DEPTH, n=N)]
float_samples = [compose(*t)(1, 10) for t in gen_gen((gen_floats,), depth=DEPTH, n=N)]
complex_samples = [compose(*t)(1, 10) for t in gen_gen((gen_complex_,), depth=DEPTH, n=N)]


@pytest.mark.parametrize("samples", int_samples, ids=[descent_str(s) for s in int_samples])
def test_int(samples, benchmark):
    benchmark(check_any, samples)


@pytest.mark.parametrize("samples", float_samples, ids=[descent_str(s) for s in float_samples])
def test_float(samples, benchmark):
    benchmark(check_any, samples)


@pytest.mark.parametrize("samples", complex_samples, ids=[descent_str(s) for s in complex_samples])
def test_complex(samples, benchmark):
    benchmark(check_any, samples)
