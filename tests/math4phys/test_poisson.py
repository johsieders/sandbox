# Tests for Poisson Brackets
# 25/01/2026
# Johannes Siedersleben

"""
Includes formal verification of the Jacobi identity and concrete examples.
"""

import pytest
from sympy import symbols, sin, cos, simplify, Matrix, sympify, Expr
from sympy.abc import a, b

from sandbox.math4phys.vector_calculus import (poisson,
                                               make_scalar_field, expr_equal)

n_dim = 3

x_1, x_2, x_3 = x = symbols(f'x_1:{n_dim + 1}', real=True)
p_1, p_2, p_3 = p = symbols(f'p_1:{n_dim + 1}', real=True)
xp = x + p

# X, P are n x 1 vectors
X = Matrix(x)
P = Matrix(p)

# A, B, C are scalars
A = make_scalar_field('A', xp)
B = make_scalar_field('B', xp)
C = make_scalar_field('C', xp)

# f, g, h are scalars, therefore we need [0, 0]
f = (X.T * X + P.T * P)[0, 0]
g = (P.T * P)[0, 0]
h = (X.T * P)[0, 0]


def test_canonical_commutation_relation():
    """Test that {x, p} = 1 (canonical commutation relation)."""

    for i in range(len(x)):
        for j in range(len(p)):
            assert expr_equal(poisson(x[i], p[j], x, p), i == j)


def test_antisymmetry():
    """Test that {f, g} = -{g, f} (antisymmetry)."""

    assert expr_equal(poisson(f, g, x, p) + poisson(g, f, x, p), 0)
    assert expr_equal(poisson(A, B, x, p) + poisson(B, A, x, p), 0)


def test_linearity():
    """Test linearity: {af + bg, h} = a{f, h} + b{g, h}."""

    assert expr_equal(poisson(a * f + b * g, h, x, p),
                      a * poisson(f, h, x, p) + b * poisson(g, h, x, p))
    assert expr_equal(poisson(a * A + b * B, C, x, p),
                      a * poisson(A, C, x, p) + b * poisson(B, C, x, p))


def test_leibniz():
    """Test Leibniz rule: {fg, h} = f{g, h} + g{f, h}."""

    assert expr_equal(poisson(f * g, h, x, p), (f * poisson(g, h, x, p) + g * poisson(f, h, x, p)))
    assert expr_equal(poisson(A * B, C, x, p), A * poisson(B, C, x, p) + B * poisson(A, C, x, p))


def test_constant_bracket_is_zero():
    """Test that {f, c} = 0 for constant c."""

    assert expr_equal(poisson(f, sympify(42), x, p), 0)


def check_jacobi(R, S, T: Expr) -> None:

    assert expr_equal(poisson(R, S, x, p) + poisson(S, R, x, p), 0)
    assert expr_equal(poisson(R, poisson(S, T, x, p), x, p) +
                      poisson(S, poisson(T, R, x, p), x, p) +
                      poisson(T, poisson(R, S, x, p), x, p), 0)

def test_jacobi():
    """Test Jacobi identity with various functions."""
    check_jacobi(A, B, C)
    check_jacobi(f, g, h)
    
    u = sin(x_1)
    v = cos(p_1)
    w = u * v
    check_jacobi(u, v, w)
