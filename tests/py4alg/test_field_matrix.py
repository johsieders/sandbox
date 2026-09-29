# tests/py4alg/test_field_matrix.py
# FieldMatrix: matrices over a field with det(), inverse() and division; type(self) propagation in Matrix.

import random
from itertools import permutations

import pytest

from sandbox.py4alg.mapper import FieldComplex, FieldMatrix, Fp, Fraction, Matrix
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt
from tests.py4alg.check_protocols import check_axioms

# element factories: int -> field element
FIELDS = {
    "Fraction": lambda k: Fraction(NativeInt(k)),
    "Fp": lambda k: Fp(17, k),
    "NativeFloat": lambda k: NativeFloat(float(k)),
    "FieldComplex": lambda k: FieldComplex(NativeFloat(float(k)), NativeFloat(float(k % 3 - 1))),
}
EXACT = ("Fraction", "Fp")


def matrix(field, values):
    make = FIELDS[field]
    return FieldMatrix(*[make(v) for v in values])


def random_matrices(field, size, count, seed=1):
    rng = random.Random(seed)
    return [matrix(field, [rng.randint(0, 9) for _ in range(size * size)]) for _ in range(count)]


def invertible(ms):
    return [m for m in ms if m.det()]


def leibniz(m):
    """det by the Leibniz formula: sum over permutations, independent of Gaussian elimination."""
    n = len(m[0])
    total = m[0][0].zero()
    for p in permutations(range(n)):
        inversions = sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
        term = m[0][0].one()
        for i in range(n):
            term = term * m[i][p[i]]
        total = total + term if inversions % 2 == 0 else total - term
    return total


# ----- protocols, descent, type propagation (step 11) -----

def test_protocols_and_descent():
    a = matrix("Fraction", [2, 1, 1, 3])
    assert isinstance(a, Ring)
    assert not isinstance(a, EuclideanRing)  # no //, %, euclidean_function
    assert not isinstance(a, Field)  # matrices do not commute; singular ones have no inverse
    assert a.descent() == [FieldMatrix, Fraction, NativeInt]


def test_type_propagates_through_arithmetic():
    a = matrix("Fraction", [2, 1, 1, 3])
    b = matrix("Fraction", [1, 4, 0, 1])
    for result in (a + b, a - b, a * b, -a, a.zero(), a.one(), a.inverse(), a / b):
        assert type(result) is FieldMatrix
    m = Matrix(*[NativeInt(k) for k in (1, 2, 3, 4)])
    for result in (m + m, m * m, -m, m.zero(), m.one()):
        assert type(result) is Matrix


def test_block_matrices_keep_their_own_class():
    a = matrix("Fraction", [2, 1, 1, 3])
    z = a.zero()
    fb = FieldMatrix(a, z, z, a)
    assert type(fb) is FieldMatrix and fb.descent() == [FieldMatrix, Fraction, NativeInt]
    mb = Matrix(a, z, z, a)  # a plain Matrix built from FieldMatrix blocks
    assert type(mb) is Matrix and mb.descent() == [Matrix, Fraction, NativeInt]


# ----- det -----

@pytest.mark.parametrize("size", [1, 2, 3, 4])
@pytest.mark.parametrize("field", EXACT)
def test_det_equals_leibniz(field, size):
    for m in random_matrices(field, size, 5):
        assert m.det() == leibniz(m)


@pytest.mark.parametrize("field", FIELDS)
def test_det_is_multiplicative(field):
    ms = random_matrices(field, 3, 6)
    for a, b in zip(ms, ms[1:]):
        assert (a * b).det() == a.det() * b.det()


@pytest.mark.parametrize("field", FIELDS)
def test_det_of_identity_and_singular(field):
    a = matrix(field, [1, 2, 3, 4, 5, 6, 7, 8, 10])
    assert a.one().det() == a[0][0].one()
    singular = matrix(field, [1, 2, 3, 1, 2, 3, 4, 5, 6])  # two equal rows
    assert singular.det() == a[0][0].zero()
    assert not singular.det()


def test_det_needs_pivoting():
    swap = matrix("Fraction", [0, 1, 1, 0])  # zero at [0][0]
    assert swap.det() == -swap[0][0].one()
    assert swap.inverse() == swap


def test_det_of_block_diagonal_is_product():
    a = matrix("Fraction", [2, 1, 1, 3])
    b = matrix("Fraction", [1, 4, 2, 1])
    z = a.zero()
    assert FieldMatrix(a, z, z, b).det() == a.det() * b.det()


# ----- inverse and division -----

@pytest.mark.parametrize("size", [1, 2, 3])
@pytest.mark.parametrize("field", FIELDS)
def test_inverse(field, size):
    ms = invertible(random_matrices(field, size, 6))
    assert ms, "no invertible samples"
    for m in ms:
        inv = m.inverse()
        assert m * inv == m.one()
        assert inv * m == m.one()


@pytest.mark.parametrize("field", FIELDS)
def test_singular_inverse_raises(field):
    singular = matrix(field, [1, 2, 1, 2])  # two equal rows: singular over every field
    with pytest.raises(ZeroDivisionError):
        singular.inverse()
    with pytest.raises(ZeroDivisionError):
        singular.one() / singular


@pytest.mark.parametrize("field", FIELDS)
def test_division(field):
    ms = random_matrices(field, 3, 6)
    bs = invertible(ms)
    for a in ms:
        for b in bs:
            assert (a / b) * b == a
            assert a / b == a * b.inverse()


# ----- ring axioms via the standard suite -----

@pytest.mark.parametrize("field", EXACT)
def test_axioms(field):
    check_axioms(random_matrices(field, 2, 3))
