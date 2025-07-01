# py4m/tests/test_complex.py

from _operator import mul
from functools import reduce

from sandbox.py4m.mapper.m_matrix import Matrix
from sandbox.py4m.util.make_samples import make_samples
from sandbox.py4m.util.utils import close_to
from tests.py4m.test_natives import int_samples

# ----- Type/sample groupings -----

n = 100


def make_matrices(n):
    return make_samples([Matrix], int_samples(n))


def test_matrix():
    # todo
    matrix_samples = make_matrices(n)
    matrix_samples_reversed = list(matrix_samples)
    matrix_samples_reversed.reverse()
    matrix_zero = matrix_samples[0].zero()
    matrix_one = matrix_samples[0].one()
    total = sum(matrix_samples, matrix_zero)
    total_rev = sum(matrix_samples_reversed, matrix_zero)
    assert total == total_rev
    prod = reduce(mul, matrix_samples, matrix_one)
    prod_rev = reduce(mul, matrix_samples_reversed, matrix_one)
    assert close_to(prod, prod_rev, 1e-6)


matrix_samples = make_matrices(n)
