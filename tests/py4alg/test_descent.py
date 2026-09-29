# tests/py4alg/test_descent.py
# descent() tells the truth: structure for every tower type, flattening of the idempotent
# constructors, and block matrices.

from functools import reduce
from operator import add

import pytest

from sandbox.py4alg.mapper import Complex, FieldComplex, FieldPolynomial, Fraction, Matrix, Polynomial
from sandbox.py4alg.util.gen_samples import gen_tree, gen_ints, gen_floats, gen_complex_
from sandbox.py4alg.util.utils import set_test_seed, descent_str
from sandbox.py4alg.wrapper.w_complex import NativeComplex
from sandbox.py4alg.wrapper.w_float import NativeFloat
from sandbox.py4alg.wrapper.w_int import NativeInt

DEPTH = 4
N = 3
set_test_seed()

# all towers up to DEPTH over ints, floats and complex (descent does not care about rounding)
tower_samples = [s for source in (gen_ints, gen_floats, gen_complex_)
                 for s in gen_tree((source,), depth=DEPTH, n=N)]
tower_ids = [descent_str(s) for s in tower_samples]

BASE_TYPES = (NativeInt, NativeFloat, NativeComplex)

# constructors that never appear directly on top of their own family:
# Polynomial, Complex and Fraction flatten, Matrix builds a block matrix over the scalars
FAMILIES = ({Polynomial, FieldPolynomial}, {Complex, FieldComplex}, {Fraction}, {Matrix})


def component(x):
    """An element one construction level below x, or None for a base type."""
    if isinstance(x, Polynomial):
        return x.coeffs()[0]
    if isinstance(x, Complex):
        return x.re
    if isinstance(x, Fraction):
        return x.numerator
    if isinstance(x, Matrix):
        return x[0][0]
    return None


def ints(*values):
    return [NativeInt(v) for v in values]


# ----- Step 9: descent() structure for every tower type -----

@pytest.mark.parametrize("samples", tower_samples, ids=tower_ids)
def test_descent_structure(samples):
    d = samples[0].descent()
    assert isinstance(d, list) and d, "descent() must be a nonempty list"
    assert all(isinstance(c, type) for c in d), "all entries must be classes"
    assert d[0] is type(samples[0]), "first entry is the type of the element"
    assert d[-1] in BASE_TYPES, "last entry is a base type"
    assert all(x.descent() == d for x in samples), "samples are homogeneous"
    for outer, inner in zip(d, d[1:]):
        assert not any(outer in f and inner in f for f in FAMILIES), \
            f"{outer.__name__} directly on {inner.__name__}: should have been flattened"


@pytest.mark.parametrize("samples", tower_samples, ids=tower_ids)
def test_descent_matches_components(samples):
    """descent() is [type(x)] + descent of the components, all the way down."""
    for x in samples:
        c = component(x)
        if c is None:
            assert len(x.descent()) == 1
        else:
            assert x.descent() == [type(x)] + c.descent()


# ----- Step 10: flattening of the idempotent constructors -----

def test_polynomial_of_polynomials_flattens():
    # Polynomial(p0, p1, ...) == p0 + p1*x + p2*x^2 + ...
    p0 = Polynomial(*ints(1, 2))
    p1 = Polynomial(*ints(3, 0, 4))
    p2 = Polynomial(*ints(5))
    x = Polynomial(*ints(0, 1))
    q = Polynomial(p0, p1, p2)
    assert q == p0 + p1 * x + p2 * x * x
    assert q.descent() == [Polynomial, NativeInt]
    assert Polynomial(p0) == p0


def test_field_polynomial_of_field_polynomials_flattens():
    f = [NativeFloat(v) for v in (1.0, 2.0, 3.0)]
    p0 = FieldPolynomial(f[0], f[1])
    p1 = FieldPolynomial(f[2])
    x = FieldPolynomial(f[0].zero(), f[0].one())
    q = FieldPolynomial(p0, p1)
    assert q == p0 + p1 * x
    assert q.descent() == [FieldPolynomial, NativeFloat]


def test_complex_of_complexes_flattens():
    # Complex(a, b) == a + i*b (Gauss)
    a = Complex(*ints(1, 2))
    b = Complex(*ints(3, 4))
    i = Complex(*ints(0, 1))
    c = Complex(a, b)
    assert c == a + i * b
    assert c.descent() == [Complex, NativeInt]
    assert Complex(a) == a


def test_field_complex_of_field_complexes_flattens():
    f = [NativeFloat(v) for v in (1.0, 2.0, 3.0, 4.0)]
    a = FieldComplex(f[0], f[1])
    b = FieldComplex(f[2], f[3])
    i = FieldComplex(f[0].zero(), f[0].one())
    c = FieldComplex(a, b)
    assert c == a + i * b
    assert c.descent() == [FieldComplex, NativeFloat]


def test_fraction_of_fractions_flattens():
    # Fraction(a, b) == a / b
    a = Fraction(*ints(1, 2))
    b = Fraction(*ints(3, 4))
    c = Fraction(a, b)
    assert c == a / b
    assert c.descent() == [Fraction, NativeInt]
    assert Fraction(a) == a


def test_complex_of_polynomials_does_not_flatten():
    # flattening only applies to the constructor's own family
    c = Complex(Polynomial(*ints(1, 2)), Polynomial(*ints(3)))
    assert c.descent() == [Complex, Polynomial, NativeInt]


# ----- Step 10: block matrices with varied block sizes -----

def square(m, start):
    """m x m matrix with entries start, start+1, ..."""
    return Matrix(*ints(*range(start, start + m * m)))


@pytest.mark.parametrize("m", [1, 2, 3], ids=lambda m: f"block{m}x{m}")
@pytest.mark.parametrize("n", [1, 2, 3], ids=lambda n: f"{n}x{n}blocks")
def test_block_matrix(n, m):
    blocks = [square(m, 10 * k) for k in range(n * n)]
    b = Matrix(*blocks)
    assert b.descent() == [Matrix, NativeInt]
    size = n * m
    assert len(b[0]) == size and len(b[size - 1]) == size
    with pytest.raises(IndexError):
        b[size]
    for bi in range(n):
        for bj in range(n):
            for i in range(m):
                for j in range(m):
                    assert b[bi * m + i][bj * m + j] == blocks[bi * n + bj][i][j]


@pytest.mark.parametrize("m", [1, 2], ids=lambda m: f"block{m}x{m}")
@pytest.mark.parametrize("n", [1, 2, 3], ids=lambda n: f"{n}x{n}blocks")
def test_block_matrix_product(n, m):
    # (A_ij) * (B_ij) == (sum_k A_ik B_kj): block multiplication agrees with the flattened product
    a = [square(m, 3 * k + 1) for k in range(n * n)]
    b = [square(m, 5 * k + 2) for k in range(n * n)]
    c = [reduce(add, (a[i * n + k] * b[k * n + j] for k in range(n))) for i in range(n) for j in range(n)]
    assert Matrix(*a) * Matrix(*b) == Matrix(*c)


def test_nested_block_matrix_stays_flat():
    inner = Matrix(*[square(1, k) for k in range(4)])  # 2x2 from four 1x1 blocks
    outer = Matrix(inner, inner, inner, inner)  # 4x4
    assert outer.descent() == [Matrix, NativeInt]
    assert len(outer[0]) == 4
