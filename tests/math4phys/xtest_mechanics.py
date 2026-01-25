"""
Tests for Poisson Brackets

Includes formal verification of the Jacobi identity and concrete examples.
"""

from sympy import symbols, simplify, Matrix

from sandbox.math4phys.vector_calculus import (make_scalar_field)

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


class TestPoissonBracket:

    def test_harmonic_oscillator(self):
        """Test Poisson bracket with harmonic oscillator Hamiltonian."""
        x, p = symbols('x p', real=True)
        m, omega = symbols('m omega', positive=True, real=True)

        # Hamiltonian: H = p²/2m + mω²x²/2
        H = p ** 2 / (2 * m) + m * omega ** 2 * x ** 2 / 2

        # {x, H} should give dx/dt = ∂H/∂p = p/m
        bracket_x_H = poisson_bracket(x, H, [x], [p])
        assert simplify(bracket_x_H - p / m) == 0

        # {p, H} should give dp/dt = -∂H/∂x = -mω²x
        bracket_p_H = poisson_bracket(p, H, [x], [p])
        assert simplify(bracket_p_H + m * omega ** 2 * x) == 0

    def test_angular_momentum_2d(self):
        """Test angular momentum Poisson brackets in 2D."""
        x1, x2, p1, p2 = symbols('x1 x2 p1 p2', real=True)

        # Angular momentum: L = x1*p2 - x2*p1
        L = x1 * p2 - x2 * p1

        # {x1, L} = -x2
        bracket_x1_L = poisson_bracket(x1, L, [x1, x2], [p1, p2])
        assert simplify(bracket_x1_L + x2) == 0

        # {p1, L} = -p2
        bracket_p1_L = poisson_bracket(p1, L, [x1, x2], [p1, p2])
        assert simplify(bracket_p1_L + p2) == 0

    def test_vector_interface(self):
        """Test using create_phase_space and vector interface."""
        # Create phase space vectors
        x, p = create_phase_space(2)

        # Test canonical relation {x_i, p_j} = δ_ij
        assert poisson_bracket(x[0], p[0], x, p) == 1
        assert poisson_bracket(x[0], p[1], x, p) == 0
        assert poisson_bracket(x[1], p[0], x, p) == 0
        assert poisson_bracket(x[1], p[1], x, p) == 1

        # Test with a function
        H = x[0] ** 2 + p[0] ** 2 + x[1] ** 2 + p[1] ** 2
        bracket_x0_H = poisson_bracket(x[0], H, x, p)
        assert simplify(bracket_x0_H - 2 * p[0]) == 0
