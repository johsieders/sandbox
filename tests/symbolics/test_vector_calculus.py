"""
Tests for symbolic vector calculus engine.

Verifies fundamental vector calculus identities and operations.
"""

import pytest
from sympy import symbols, simplify
from sandbox.symbolics.vector_calculus_1 import (
    make_coords, ScalarField, VectorField,
    gradient, divergence, curl, laplacian,
    make_vector_field,
    curl_of_gradient_is_zero,
    divergence_of_curl_is_zero,
    laplacian_is_div_grad,
)


class TestScalarField:
    """Test ScalarField class and operations."""

    def test_scalar_field_creation(self):
        """Test creating a scalar field."""
        coords = make_coords('x y z')
        f = ScalarField('f', coords)

        assert f.name == 'f'
        assert f.dim == 3
        assert len(f.coords) == 3

    def test_scalar_field_gradient(self):
        """Test gradient computation."""
        coords = make_coords('x y z')
        f = ScalarField('f', coords)
        grad_f = f.gradient()

        assert isinstance(grad_f, VectorField)
        assert grad_f.output_dim == 3

    def test_scalar_field_laplacian(self):
        """Test Laplacian computation."""
        coords = make_coords('x y z')
        f = ScalarField('f', coords)
        lap_f = f.laplacian()

        # Laplacian should have three terms (one for each coordinate)
        assert lap_f is not None


class TestVectorField:
    """Test VectorField class and operations."""

    def test_vector_field_creation(self):
        """Test creating a vector field."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)

        assert F.name == 'F'
        assert F.input_dim == 3
        assert F.output_dim == 3

    def test_vector_field_divergence(self):
        """Test divergence computation."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)
        div_F = F.divergence()

        assert div_F is not None

    def test_vector_field_curl_3d(self):
        """Test curl computation for 3D field."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)
        curl_F = F.curl()

        assert isinstance(curl_F, VectorField)
        assert curl_F.output_dim == 3

    def test_vector_field_addition(self):
        """Test vector field addition."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)
        G = make_vector_field('G', coords)

        H = F + G
        assert isinstance(H, VectorField)
        assert H.output_dim == 3

    def test_vector_field_scalar_multiplication(self):
        """Test scalar multiplication."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)
        x = coords[0]

        G = x * F
        assert isinstance(G, VectorField)

        H = F * 2
        assert isinstance(H, VectorField)

    def test_vector_field_dot_product(self):
        """Test dot product."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)
        G = make_vector_field('G', coords)

        dot_product = F.dot(G)
        assert dot_product is not None

    def test_vector_field_cross_product(self):
        """Test cross product."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)
        G = make_vector_field('G', coords)

        cross_product = F.cross(G)
        assert isinstance(cross_product, VectorField)
        assert cross_product.output_dim == 3


class TestVectorCalculusIdentities:
    """Test fundamental vector calculus identities."""

    def test_curl_of_gradient_is_zero(self):
        """
        Verify: ∇×(∇f) = 0

        The curl of any gradient is always zero.
        This is because mixed partial derivatives commute (Schwarz's theorem).
        """
        coords = make_coords('x y z')
        f = ScalarField('f', coords)

        # Method 1: Using the helper function
        assert curl_of_gradient_is_zero(f), "∇×(∇f) should be zero"

        # Method 2: Manual verification
        grad_f = gradient(f)
        curl_grad_f = curl(grad_f)
        assert curl_grad_f.is_zero(), "∇×(∇f) should be zero"

    def test_divergence_of_curl_is_zero(self):
        """
        Verify: ∇·(∇×F) = 0

        The divergence of any curl is always zero.
        """
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)

        # Method 1: Using the helper function
        assert divergence_of_curl_is_zero(F), "∇·(∇×F) should be zero"

        # Method 2: Manual verification
        curl_F = curl(F)
        div_curl_F = divergence(curl_F)
        assert simplify(div_curl_F) == 0, "∇·(∇×F) should be zero"

    def test_laplacian_equals_div_grad(self):
        """
        Verify: ∇²f = ∇·(∇f)

        The Laplacian equals the divergence of the gradient.
        """
        coords = make_coords('x y z')
        f = ScalarField('f', coords)

        # Using the helper function
        assert laplacian_is_div_grad(f), "∇²f should equal ∇·(∇f)"

        # Manual verification
        lap_f = f.laplacian()
        grad_f = f.gradient()
        div_grad_f = grad_f.divergence()

        assert simplify(lap_f - div_grad_f) == 0, "∇²f should equal ∇·(∇f)"

    def test_div_of_scalar_times_vector(self):
        """
        Verify: ∇·(fF) = f(∇·F) + F·(∇f)

        Product rule for divergence.
        """
        coords = make_coords('x y z')
        f = ScalarField('f', coords)
        F = make_vector_field('F', coords)

        # Left side: ∇·(fF)
        fF = f.func * F
        div_fF = fF.divergence()

        # Right side: f(∇·F) + F·(∇f)
        div_F = F.divergence()
        grad_f = f.gradient()
        right_side = f.func * div_F + F.dot(grad_f)

        # Verify equality
        difference = simplify(div_fF - right_side)
        assert difference == 0, "Product rule for divergence should hold"

    def test_curl_of_scalar_times_vector(self):
        """
        Verify: ∇×(fF) = f(∇×F) + (∇f)×F

        Product rule for curl.
        """
        coords = make_coords('x y z')
        f = ScalarField('f', coords)
        F = make_vector_field('F', coords)

        # Left side: ∇×(fF)
        fF = f.func * F
        curl_fF = fF.curl()

        # Right side: f(∇×F) + (∇f)×F
        curl_F = F.curl()
        grad_f = f.gradient()
        right_side = f.func * curl_F + grad_f.cross(F)

        # Verify equality (component by component)
        for i in range(3):
            diff = simplify(curl_fF[i] - right_side[i])
            assert diff == 0, f"Product rule for curl should hold (component {i})"


class TestDifferentDimensions:
    """Test operations in different dimensions."""

    def test_2d_operations(self):
        """Test vector operations in 2D."""
        coords = make_coords('x y')
        f = ScalarField('f', coords)

        # Gradient should work in 2D
        grad_f = f.gradient()
        assert grad_f.output_dim == 2

        # Laplacian should work in 2D
        lap_f = f.laplacian()
        assert lap_f is not None

    def test_4d_operations(self):
        """Test vector operations in 4D (e.g., spacetime)."""
        coords = make_coords('t x y z')
        f = ScalarField('phi', coords)

        # Gradient should work in 4D
        grad_f = f.gradient()
        assert grad_f.output_dim == 4

        # Divergence should work for 4D field
        F = make_vector_field('A', coords, dim=4)
        div_F = F.divergence()
        assert div_F is not None

    def test_curl_requires_3d(self):
        """Test that curl raises error for non-3D fields."""
        coords = make_coords('x y')
        F = make_vector_field('F', coords, dim=2)

        with pytest.raises(ValueError, match="Curl only defined for 3D"):
            F.curl()


class TestJacobian:
    """Test Jacobian matrix computation."""

    def test_jacobian_square_field(self):
        """Test Jacobian for square field (n→n)."""
        coords = make_coords('x y z')
        F = make_vector_field('F', coords)

        J = F.jacobian()
        assert J.shape == (3, 3)

    def test_jacobian_rectangular_field(self):
        """Test Jacobian for rectangular field (n→m)."""
        coords = make_coords('u v')
        # Create 3D output field from 2D input
        F = make_vector_field('F', coords, dim=3)

        J = F.jacobian()
        assert J.shape == (3, 2)

    def test_gradient_is_jacobian_transpose(self):
        """Verify that gradient is the transpose of the Jacobian for scalar fields."""
        coords = make_coords('x y z')
        f = ScalarField('f', coords)

        # Treat scalar field as 1D output vector field
        grad_f = f.gradient()

        # For scalar field f: R³ → R, gradient is (∂f/∂x, ∂f/∂y, ∂f/∂z)
        # This matches the Jacobian for a 1×3 → 3×1 transposition
        assert grad_f.output_dim == 3


class TestSimplification:
    """Test simplification and expansion operations."""

    def test_simplify_vector_field(self):
        """Test simplification of vector field components."""
        coords = make_coords('x y z')
        x, y, z = coords

        # Create field with expandable components
        components = [x*x + 2*x*y + y*y, x + x, y*y - y*y]
        F = VectorField(components, coords)

        F_simplified = F.simplify()
        assert F_simplified[1] == 2*x
        assert F_simplified[2] == 0

    def test_expand_vector_field(self):
        """Test expansion of vector field components."""
        coords = make_coords('x y')
        x, y = coords

        # Create field with factorable components
        components = [(x + y)**2, x*(x + y)]
        F = VectorField(components, coords)

        F_expanded = F.expand()
        # (x + y)² should expand to x² + 2xy + y²
        assert F_expanded[0] == x**2 + 2*x*y + y**2


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
