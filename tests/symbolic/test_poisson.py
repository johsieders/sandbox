"""
Tests for Poisson Brackets

Includes formal verification of the Jacobi identity and concrete examples.
"""

import pytest
from sympy import symbols, sin, cos, exp, simplify
from sandbox.symbolic.poisson import poisson_bracket, verify_jacobi_identity, create_phase_space
from sandbox.symbolic.jacobi_proof import prove_jacobi_algebraically


class TestPoissonBracket:
    """Test basic Poisson bracket properties."""

    def test_canonical_commutation_relation(self):
        """Test that {x, p} = 1 (canonical commutation relation)."""
        x, p = symbols('x p', real=True)
        bracket = poisson_bracket(x, p, [x], [p])
        assert bracket == 1

    def test_antisymmetry(self):
        """Test that {f, g} = -{g, f} (antisymmetry)."""
        x, p = symbols('x p', real=True)
        f = x**2 + p**2
        g = x * p

        bracket_fg = poisson_bracket(f, g, [x], [p])
        bracket_gf = poisson_bracket(g, f, [x], [p])

        assert bracket_fg == -bracket_gf

    def test_linearity(self):
        """Test linearity: {af + bg, h} = a{f, h} + b{g, h}."""
        x, p = symbols('x p', real=True)
        a, b = symbols('a b', real=True)

        f = x**2
        g = p**2
        h = x * p

        # Left side: {af + bg, h}
        left = poisson_bracket(a*f + b*g, h, [x], [p])

        # Right side: a{f, h} + b{g, h}
        right = a * poisson_bracket(f, h, [x], [p]) + b * poisson_bracket(g, h, [x], [p])

        assert simplify(left - right) == 0

    def test_leibniz_rule(self):
        """Test Leibniz rule: {fg, h} = f{g, h} + g{f, h}."""
        x, p = symbols('x p', real=True)

        f = x**2
        g = p**2
        h = x * p

        # Left side: {fg, h}
        left = poisson_bracket(f * g, h, [x], [p])

        # Right side: f{g, h} + g{f, h}
        right = f * poisson_bracket(g, h, [x], [p]) + g * poisson_bracket(f, h, [x], [p])

        assert simplify(left - right) == 0

    def test_constant_bracket_is_zero(self):
        """Test that {f, c} = 0 for constant c."""
        x, p = symbols('x p', real=True)
        f = x**2 + p**2
        c = 42

        bracket = poisson_bracket(f, c, [x], [p])
        assert bracket == 0

    def test_harmonic_oscillator(self):
        """Test Poisson bracket with harmonic oscillator Hamiltonian."""
        x, p = symbols('x p', real=True)
        m, omega = symbols('m omega', positive=True, real=True)

        # Hamiltonian: H = p²/2m + mω²x²/2
        H = p**2 / (2*m) + m * omega**2 * x**2 / 2

        # {x, H} should give dx/dt = ∂H/∂p = p/m
        bracket_x_H = poisson_bracket(x, H, [x], [p])
        assert simplify(bracket_x_H - p/m) == 0

        # {p, H} should give dp/dt = -∂H/∂x = -mω²x
        bracket_p_H = poisson_bracket(p, H, [x], [p])
        assert simplify(bracket_p_H + m * omega**2 * x) == 0

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
        H = x[0]**2 + p[0]**2 + x[1]**2 + p[1]**2
        bracket_x0_H = poisson_bracket(x[0], H, x, p)
        assert simplify(bracket_x0_H - 2*p[0]) == 0


class TestJacobiIdentity:
    """Test the Jacobi identity formally and with concrete examples."""

    def test_jacobi_identity_1d_formal(self):
        """
        Formal proof of Jacobi identity in 1D phase space.

        Tests: {f, {g, h}} + {g, {h, f}} + {h, {f, g}} = 0
        for arbitrary functions f, g, h.
        """
        result, is_zero = verify_jacobi_identity(n_dim=1)
        assert is_zero, f"Jacobi identity failed in 1D: result = {result}"

    def test_jacobi_identity_2d_formal(self):
        """
        Formal proof of Jacobi identity in 2D phase space.

        Tests: {f, {g, h}} + {g, {h, f}} + {h, {f, g}} = 0
        for arbitrary functions f, g, h.
        """
        result, is_zero = verify_jacobi_identity(n_dim=2)
        assert is_zero, f"Jacobi identity failed in 2D: result = {result}"

    def test_jacobi_identity_3d_formal(self):
        """
        Formal proof of Jacobi identity in 3D phase space.

        Tests: {f, {g, h}} + {g, {h, f}} + {h, {f, g}} = 0
        for arbitrary functions f, g, h.
        """
        result, is_zero = verify_jacobi_identity(n_dim=3)
        assert is_zero, f"Jacobi identity failed in 3D: result = {result}"

    def test_jacobi_concrete_polynomials(self):
        """Test Jacobi identity with concrete polynomial functions."""
        x, p = symbols('x p', real=True)

        f = x**2
        g = p**2
        h = x * p

        # Compute the three terms
        term1 = poisson_bracket(f, poisson_bracket(g, h, [x], [p]), [x], [p])
        term2 = poisson_bracket(g, poisson_bracket(h, f, [x], [p]), [x], [p])
        term3 = poisson_bracket(h, poisson_bracket(f, g, [x], [p]), [x], [p])

        jacobi_sum = term1 + term2 + term3

        assert simplify(jacobi_sum) == 0

    def test_jacobi_concrete_trigonometric(self):
        """Test Jacobi identity with trigonometric functions."""
        x, p = symbols('x p', real=True)

        f = sin(x)
        g = cos(p)
        h = x * p

        # Compute the three terms
        term1 = poisson_bracket(f, poisson_bracket(g, h, [x], [p]), [x], [p])
        term2 = poisson_bracket(g, poisson_bracket(h, f, [x], [p]), [x], [p])
        term3 = poisson_bracket(h, poisson_bracket(f, g, [x], [p]), [x], [p])

        jacobi_sum = term1 + term2 + term3

        assert simplify(jacobi_sum) == 0

    def test_jacobi_algebraic_proof(self):
        """
        Dimension-independent algebraic proof of Jacobi identity.

        Uses abstract gradient symbols with no concrete functions or dimension expansion.
        This is the most general proof - works for any dimension.
        """
        result, is_zero, _ = prove_jacobi_algebraically(verbose=False)
        assert is_zero, f"Algebraic Jacobi proof failed: result = {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])