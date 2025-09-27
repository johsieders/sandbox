# py4alg/tests/test_matrices.py


import pytest

from sandbox.py4alg.mapper.m_matrix import Matrix
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.g_samples import (g_ints, g_floats, g_complex_,
                                           g_nat_complex, g_nat_ints, g_nat_floats,
                                           g_complex, g_fractions, g_matrices)
from sandbox.py4alg.util.utils import compose, take
from sandbox.py4alg.wrapper.w_int import NativeInt
from tests.py4alg.check_properties import check_rings


# ----- Type/sample groupings -----

def matrix_samples(n: int):
    return (compose(take(n), g_matrices, g_nat_ints, g_ints)(10, 20),
            compose(take(n), g_matrices, g_matrices, g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_matrices, g_nat_floats, g_floats)(10, 20),
            compose(take(n), g_matrices, g_complex, g_nat_complex, g_complex_)(10, 20),
            compose(take(n), g_matrices, g_fractions, g_nat_ints, g_ints)(10, 20))


@pytest.mark.parametrize("samples", matrix_samples(10))
def test_properties(samples):
    check_rings(samples)


def test_matrix_matrix():
    n = 16  # must be square
    # this produces 2 matrices of size sqrt(k*n) x sqrt(k*n)
    # with k = params[matrix_size]
    ms1 = Matrix(*compose(take(n), g_matrices, g_nat_ints, g_ints)(10, 20))
    ms2 = Matrix(*compose(take(n), g_matrices, g_nat_ints, g_ints)(50, 60))
    check_rings((ms1, ms2))


def test_is_instance():
    entries = (NativeInt(k) for k in range(4))
    m = Matrix(*entries)
    print()
    print(type(m))
    print(isinstance(m, Matrix))
    print(isinstance(m, AbelianGroup))
    print(isinstance(m, Ring))
