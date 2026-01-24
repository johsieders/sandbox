"""
Operator-Based Symbolic Vector Calculus Engine

A clean operator-based approach to vector calculus built on SymPy.
Operators (∂, lap_op, ∂×, etc.) are first-class objects that can be applied to
SymPy functions and matrices.

Design philosophy:
- Operators as composable transformations
- Work directly with SymPy Functions and Matrices
- Dimension checking at operator level
- Mathematical notation matches standard vector calculus
- Lightweight wrappers for convenience (ScalarField, VectorField)

Example usage:
    >>> coords = make_coords('x y z')
    >>> grad_op = GradientOperator(coords)
    >>> f = Function('f')(*coords)
    >>> grad_f = grad_op(f)  # Returns Matrix (column vector)

    >>> # Or use lightweight wrapper
    >>> f = ScalarField('f', coords)
    >>> grad_f = grad_op(f)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Union

from sympy import (
    symbols, Function, Matrix, diff, simplify, expand,
    Symbol
)


# ============================================================================
# Helper Functions
# ============================================================================

def make_coords(coord_str: str) -> List[Symbol]:
    """
    Create symbolic coordinates from a space-separated string.

    Args:
        coord_str: Space-separated coordinate names, e.g., 'x y z' or 'x1 x2 x3'

    Returns:
        List of SymPy symbols representing coordinates

    Example:
        >>> coords = make_coords('x y z')
        >>> coords
        [x, y, z]
    """
    return list(symbols(coord_str, real=True))


def evaluate(expr, **kwargs):
    """
    Substitute values into a symbolic expression.

    Args:
        expr: SymPy expression, Function, or Matrix
        **kwargs: Variable substitutions (e.g., x=1, y=2)

    Returns:
        Expression with substituted values

    Example:
        >>> f = Function('f')(x, y)
        >>> evaluate(f + sin(x), x=0, y=1)
        f(0, 1)
    """
    return expr.subs(kwargs)


# ============================================================================
# Base Operator Class
# ============================================================================

class DifferentialOperator(ABC):
    """
    Abstract base class for differential operators.

    Operators are callable objects that transform SymPy expressions.
    """

    @abstractmethod
    def __call__(self, expr):
        """Apply the operator to an expression."""
        pass

    @abstractmethod
    def __repr__(self):
        """String representation of the operator."""
        pass


# ============================================================================
# Core Differential Operators
# ============================================================================

class PartialDerivativeOperator(DifferentialOperator):
    """
    ∂ᵢ - Partial derivative operator with respect to a single coordinate.

    Attributes:
        coord: The coordinate to differentiate with respect to
        order: Order of differentiation (default: 1)

    Example:
        >>> ∂x = PartialDerivativeOperator(x, order=1)
        >>> ∂x(f)  # Returns df/dx
    """

    def __init__(self, coord: Symbol, order: int = 1):
        self.coord = coord
        self.order = order

    def __call__(self, expr):
        """Apply partial derivative to expression."""
        if isinstance(expr, Matrix):
            # Apply element-wise to matrices
            return expr.applyfunc(lambda e: diff(e, self.coord, self.order))
        return diff(expr, self.coord, self.order)

    def __repr__(self):
        if self.order == 1:
            return f"∂_{self.coord}"
        return f"∂_{self.coord}^{self.order}"


class GradientOperator(DifferentialOperator):
    """
    ∂ - Gradient operator (column vector of partial derivatives).

    For scalar f: R^n → R, returns ∂f = [∂₁f, ∂₂f, ..., ∂ₙf]ᵀ (column vector)

    Attributes:
        coords: List of coordinate symbols
        dim: Dimension of the space

    Example:
        >>> coords = make_coords('x y z')
        >>> grad_op = GradientOperator(coords)
        >>> f = Function('f')(*coords)
        >>> grad_op(f)  # Returns column vector of derivatives
    """

    def __init__(self, coords: List[Symbol]):
        self.coords = coords
        self.dim = len(coords)

    def __call__(self, expr):
        """
        Apply gradient to scalar expression.

        Returns:
            Matrix (column vector) of partial derivatives
        """
        if isinstance(expr, Matrix):
            raise TypeError("Gradient applies to scalar functions, not vector fields")

        components = [diff(expr, coord) for coord in self.coords]
        return Matrix(components)

    def __repr__(self):
        return f"∂ (gradient in {self.dim}D)"


class LaplacianOperator(DifferentialOperator):
    """
    lap_op - Laplacian operator (sum of second partial derivatives).

    For scalar f: lap_opf = ∂₁²f + ∂₂²f + ... + ∂ₙ²f = div(grad(f))
    For vector F: applies component-wise

    Attributes:
        coords: List of coordinate symbols
        dim: Dimension of the space

    Example:
        >>> coords = make_coords('x y z')
        >>> lap_op = LaplacianOperator(coords)
        >>> f = Function('f')(*coords)
        >>> lap_op(f)  # Returns lap_opf/∂x² + lap_opf/∂y² + lap_opf/∂z²
    """

    def __init__(self, coords: List[Symbol]):
        self.coords = coords
        self.dim = len(coords)

    def __call__(self, expr):
        """Apply Laplacian to expression."""
        if isinstance(expr, Matrix):
            # Component-wise for vector fields
            return expr.applyfunc(lambda e: sum(diff(e, coord, 2) for coord in self.coords))

        # Scalar Laplacian
        return sum(diff(expr, coord, 2) for coord in self.coords)

    def __repr__(self):
        return f"lap_op (Laplacian in {self.dim}D)"


class DivergenceOperator(DifferentialOperator):
    """
    ∂· - Divergence operator (dot product of gradient with vector field).

    For vector field F: R^n → R^n, returns ∂·F = ∂₁F₁ + ∂₂F₂ + ... + ∂ₙFₙ

    Attributes:
        coords: List of coordinate symbols
        dim: Dimension of the space

    Example:
        >>> coords = make_coords('x y z')
        >>> div = DivergenceOperator(coords)
        >>> F = Matrix([Function(f'F{i}')(*coords) for i in [1,2,3]])
        >>> div(F)  # Returns ∂F₁/∂x + ∂F₂/∂y + ∂F₃/∂z
    """

    def __init__(self, coords: List[Symbol]):
        self.coords = coords
        self.dim = len(coords)

    def __call__(self, F):
        """
        Apply divergence to vector field.

        Args:
            F: Matrix (column vector) representing vector field

        Returns:
            Scalar expression
        """
        if not isinstance(F, Matrix):
            raise TypeError("Divergence applies to vector fields (Matrix)")

        if len(F) != self.dim:
            raise ValueError(f"Vector field dimension {len(F)} doesn't match coordinate dimension {self.dim}")

        return sum(diff(F[i], self.coords[i]) for i in range(self.dim))

    def __repr__(self):
        return f"∂· (divergence in {self.dim}D)"


class CurlOperator(DifferentialOperator):
    """
    ∂× - Curl operator (cross product of gradient with vector field).

    Only defined in 3D. For F = (F₁, F₂, F₃):
    ∂×F = (∂yF₃ - ∂zF₂, ∂zF₁ - ∂xF₃, ∂xF₂ - ∂yF₁)

    Attributes:
        coords: List of 3 coordinate symbols [x, y, z]

    Example:
        >>> coords = make_coords('x y z')
        >>> curl = CurlOperator(coords)
        >>> F = Matrix([Function(f'F{i}')(*coords) for i in [1,2,3]])
        >>> curl(F)  # Returns curl vector
    """

    def __init__(self, coords: List[Symbol]):
        if len(coords) != 3:
            raise ValueError(f"Curl only defined for 3D")
        self.coords = coords
        self.dim = 3

    def __call__(self, F):
        """
        Apply curl to 3D vector field.

        Args:
            F: Matrix (column vector) with 3 components

        Returns:
            Matrix (column vector) representing curl
        """
        if not isinstance(F, Matrix):
            raise TypeError("Curl applies to vector fields (Matrix)")

        if len(F) != 3:
            raise ValueError(f"Curl requires 3D vector field, got {len(F)}D")

        x, y, z = self.coords
        F1, F2, F3 = F[0], F[1], F[2]

        curl_components = [
            diff(F3, y) - diff(F2, z),  # i component
            diff(F1, z) - diff(F3, x),  # j component
            diff(F2, x) - diff(F1, y),  # k component
        ]

        return Matrix(curl_components)

    def __repr__(self):
        return "∂× (curl in 3D)"


class JacobianOperator(DifferentialOperator):
    """
    ∂⊗ - Jacobian operator (outer product of gradient with vector field).

    For vector field F: R^n → R^m, returns Jacobian matrix J[i,j] = ∂Fᵢ/∂xⱼ
    Shape: (m, n) where m = len(F), n = len(coords)

    Attributes:
        coords: List of coordinate symbols
        dim: Input dimension (n)

    Example:
        >>> coords = make_coords('x y z')
        >>> J = JacobianOperator(coords)
        >>> F = Matrix([Function(f'F{i}')(*coords) for i in [1,2,3]])
        >>> J(F)  # Returns 3×3 Jacobian matrix
    """

    def __init__(self, coords: List[Symbol]):
        self.coords = coords
        self.dim = len(coords)

    def __call__(self, F):
        """
        Compute Jacobian matrix.

        Args:
            F: Matrix (column vector) representing vector field

        Returns:
            Matrix representing Jacobian (output_dim × input_dim)
        """
        if not isinstance(F, Matrix):
            raise TypeError("Jacobian applies to vector fields (Matrix)")

        output_dim = len(F)
        input_dim = self.dim

        J = Matrix.zeros(output_dim, input_dim)
        for i in range(output_dim):
            for j in range(input_dim):
                J[i, j] = diff(F[i], self.coords[j])

        return J

    def __repr__(self):
        return f"∂⊗ (Jacobian in {self.dim}D)"


class HessianOperator(DifferentialOperator):
    """
    ∂⊗∂ (or ∂⊗²) - Hessian operator (outer product of gradient with itself).

    For scalar f: R^n → R, returns Hessian matrix H[i,j] = ∂ᵢ∂ⱼf
    Shape: (n, n) - always square matrix

    Attributes:
        coords: List of coordinate symbols
        dim: Dimension of the space

    Example:
        >>> coords = make_coords('x y z')
        >>> H = HessianOperator(coords)
        >>> f = Function('f')(*coords)
        >>> H(f)  # Returns 3×3 Hessian matrix
    """

    def __init__(self, coords: List[Symbol]):
        self.coords = coords
        self.dim = len(coords)

    def __call__(self, f):
        """
        Compute Hessian matrix.

        Args:
            f: Scalar expression

        Returns:
            Matrix representing Hessian (n × n)
        """
        if isinstance(f, Matrix):
            raise TypeError("Hessian applies to scalar functions, not vector fields")

        n = self.dim
        H = Matrix.zeros(n, n)
        for i in range(n):
            for j in range(n):
                H[i, j] = diff(f, self.coords[i], self.coords[j])

        return H

    def __repr__(self):
        return f"∂⊗∂ (Hessian in {self.dim}D)"


# ============================================================================
# Lightweight Wrappers (Optional Convenience)
# ============================================================================

class ScalarField:
    """
    Lightweight wrapper for scalar-valued functions f: R^n → R.

    Just creates a SymPy Function and stores coordinates for convenience.
    Use operators to compute derivatives, gradients, etc.

    Attributes:
        name: Name of the field
        coords: List of coordinate symbols
        func: Underlying SymPy Function
        dim: Dimension

    Example:
        >>> coords = make_coords('x y z')
        >>> f = ScalarField('f', coords)
        >>> grad_op = GradientOperator(coords)
        >>> grad_op(f)  # Applies gradient to f.func
    """

    def __init__(self, name: str, coords: List[Symbol]):
        self.name = name
        self.coords = coords
        self.dim = len(coords)
        self.func = Function(name)(*coords)

    def __call__(self, **kwargs):
        """Evaluate with substituted coordinates."""
        return self.func.subs(kwargs)

    def __repr__(self):
        coord_str = ', '.join(str(c) for c in self.coords)
        return f"{self.name}({coord_str})"

    def __str__(self):
        return self.name

    # Enable operators to work directly with ScalarField
    # They'll extract .func automatically in __call__
    def _sympy_expr(self):
        """Return underlying SymPy expression."""
        return self.func

    # Convenience methods (use operators under the hood)
    def gradient(self) -> 'VectorField':
        """Compute gradient using GradientOperator."""
        grad_op = GradientOperator(self.coords)
        grad_matrix = grad_op(self.func)
        return VectorField._from_matrix(grad_matrix, self.coords, name=f'∇{self.name}')

    def laplacian(self):
        """Compute Laplacian using LaplacianOperator."""
        lap_op = LaplacianOperator(self.coords)
        return lap_op(self.func)

    def hessian(self) -> Matrix:
        """Compute Hessian using HessianOperator."""
        H = HessianOperator(self.coords)
        return H(self.func)

    def diff(self, coord: Symbol, order: int = 1):
        """Compute partial derivative."""
        grad_op = PartialDerivativeOperator(coord, order)
        return grad_op(self.func)


class VectorField:
    """
    Lightweight wrapper for vector-valued functions F: R^n → R^m.

    Just wraps a Matrix of SymPy Functions.
    Use operators to compute divergence, curl, Jacobian, etc.

    Attributes:
        name: Optional name
        coords: List of coordinate symbols
        components: Matrix (column vector) of expressions
        input_dim: Dimension of domain (n)
        output_dim: Dimension of codomain (m)

    Example:
        >>> coords = make_coords('x y z')
        >>> F = VectorField('E', coords, dim=3)
        >>> curl = CurlOperator(coords)
        >>> curl(F)  # Applies curl to F.components
    """

    def __init__(self, name_or_components, coords: List[Symbol], dim: int = None, name: str = None):
        """
        Create a vector field with symbolic components.

        Args:
            name_or_components: Either a string name (creates symbolic components)
                               or a list/Matrix of expressions
            coords: Coordinate symbols
            dim: Output dimension (default: same as len(coords))
            name: Optional name (used when name_or_components is a list/Matrix)
        """
        self.coords = coords
        self.input_dim = len(coords)

        if isinstance(name_or_components, (list, Matrix)):
            # Create from explicit components
            self.components = Matrix(name_or_components) if isinstance(name_or_components, list) else name_or_components
            self.output_dim = len(self.components)
            self.name = name
        else:
            # Create with symbolic function names
            self.name = name_or_components
            self.output_dim = dim if dim is not None else self.input_dim
            components = [Function(f'{self.name}{i + 1}')(*coords) for i in range(self.output_dim)]
            self.components = Matrix(components)

    def __call__(self, **kwargs):
        """Evaluate with substituted coordinates."""
        return self.components.subs(kwargs)

    def __repr__(self):
        return f"{self.name}: R^{self.input_dim} → R^{self.output_dim}"

    def __str__(self):
        return self.name

    def __getitem__(self, index):
        """Access individual components."""
        return self.components[index]

    # Enable operators to work directly with VectorField
    def _sympy_expr(self):
        """Return underlying SymPy Matrix."""
        return self.components

    @classmethod
    def _from_matrix(cls, matrix: Matrix, coords: List[Symbol], name: str = None):
        """Create VectorField from a Matrix."""
        return cls(matrix, coords, name=name)

    # Convenience methods (use operators under the hood)
    def divergence(self):
        """Compute divergence using DivergenceOperator."""
        div = DivergenceOperator(self.coords)
        return div(self.components)

    def curl(self) -> 'VectorField':
        """Compute curl using CurlOperator (3D only)."""
        curl_op = CurlOperator(self.coords)
        curl_matrix = curl_op(self.components)
        return VectorField._from_matrix(curl_matrix, self.coords, name=f'∇×{self.name}' if self.name else 'curl')

    def jacobian(self) -> Matrix:
        """Compute Jacobian using JacobianOperator."""
        J = JacobianOperator(self.coords)
        return J(self.components)

    # Arithmetic and transformations
    def __add__(self, other: 'VectorField') -> 'VectorField':
        """Vector field addition."""
        if not isinstance(other, VectorField):
            raise TypeError("Can only add VectorField to VectorField")
        if self.output_dim != other.output_dim:
            raise ValueError(f"Dimension mismatch: {self.output_dim} vs {other.output_dim}")

        new_components = self.components + other.components
        new_name = f"({self.name} + {other.name})" if self.name and other.name else None
        return VectorField._from_matrix(new_components, self.coords, name=new_name)

    def __mul__(self, scalar) -> 'VectorField':
        """Scalar multiplication (field * scalar)."""
        new_components = self.components * scalar
        new_name = f"{self.name}*{scalar}" if self.name else None
        return VectorField._from_matrix(new_components, self.coords, name=new_name)

    def __rmul__(self, scalar) -> 'VectorField':
        """Right scalar multiplication (scalar * field)."""
        new_components = scalar * self.components
        new_name = f"{scalar}*{self.name}" if self.name else None
        return VectorField._from_matrix(new_components, self.coords, name=new_name)

    def dot(self, other: 'VectorField'):
        """Dot product with another vector field."""
        if not isinstance(other, VectorField):
            raise TypeError("Can only compute dot product with VectorField")
        if self.output_dim != other.output_dim:
            raise ValueError(f"Dimension mismatch: {self.output_dim} vs {other.output_dim}")

        return sum(self.components[i] * other.components[i] for i in range(self.output_dim))

    def cross(self, other: 'VectorField') -> 'VectorField':
        """Cross product with another vector field (3D only)."""
        if self.output_dim != 3 or other.output_dim != 3:
            raise ValueError("Cross product only defined for 3D vectors")

        F = self.components
        G = other.components

        cross_components = [
            F[1] * G[2] - F[2] * G[1],  # i component
            F[2] * G[0] - F[0] * G[2],  # j component
            F[0] * G[1] - F[1] * G[0],  # k component
        ]

        new_name = f"({self.name} × {other.name})" if self.name and other.name else None
        return VectorField._from_matrix(Matrix(cross_components), self.coords, name=new_name)

    def simplify(self) -> 'VectorField':
        """Simplify all components."""
        simplified_components = self.components.applyfunc(simplify)
        return VectorField._from_matrix(simplified_components, self.coords, name=self.name)

    def expand(self) -> 'VectorField':
        """Expand all components."""
        expanded_components = self.components.applyfunc(expand)
        return VectorField._from_matrix(expanded_components, self.coords, name=self.name)

    def is_zero(self) -> bool:
        """Check if all components are zero (after simplification)."""
        simplified = self.simplify()
        return all(simplify(c) == 0 for c in simplified.components)


# ============================================================================
# Operator Enhancement: Allow operators to work with wrappers
# ============================================================================

def _extract_expr(obj):
    """Extract SymPy expression from wrapper objects."""
    if hasattr(obj, '_sympy_expr'):
        return obj._sympy_expr()
    return obj


# Enhance all operators to auto-extract from wrappers
for op_class in [PartialDerivativeOperator, GradientOperator, LaplacianOperator,
                 DivergenceOperator, CurlOperator, JacobianOperator, HessianOperator]:
    original_call = op_class.__call__


    def enhanced_call(self, expr, _original=original_call):
        return _original(self, _extract_expr(expr))


    op_class.__call__ = enhanced_call


# ============================================================================
# Identity Verification Functions
# ============================================================================

def verify_identity(left, right) -> tuple[bool, any]:
    """
    Verify a vector calculus identity by symbolic simplification.

    Args:
        left: Left side (expression or Matrix)
        right: Right side

    Returns:
        Tuple of (is_equal, difference)
    """
    if isinstance(left, Matrix) and isinstance(right, Matrix):
        diff_field = left - right
        simplified = diff_field.applyfunc(simplify)
        is_equal = all(simplify(c) == 0 for c in simplified)
        return is_equal, simplified
    else:
        # Scalar expressions
        diff_expr = simplify(left - right)
        is_equal = (diff_expr == 0)
        return is_equal, diff_expr


def curl_of_gradient_is_zero(f, coords: List[Symbol] = None) -> bool:
    """
    Verify identity: ∂×(∂f) = 0 (curl of gradient is always zero).

    Args:
        f: ScalarField or expression
        coords: Optional coordinates (extracted from ScalarField if not provided)

    Requires 3D.
    """
    if coords is None:
        if hasattr(f, 'coords'):
            coords = f.coords
        else:
            raise ValueError("Must provide coords for raw expressions")

    grad_op = GradientOperator(coords)
    curl = CurlOperator(coords)

    grad_f = grad_op(_extract_expr(f))
    curl_grad_f = curl(grad_f)

    return all(simplify(c) == 0 for c in curl_grad_f)


def divergence_of_curl_is_zero(F, coords: List[Symbol] = None) -> bool:
    """
    Verify identity: ∂·(∂×F) = 0 (divergence of curl is always zero).

    Args:
        F: VectorField or expression
        coords: Optional coordinates (extracted from VectorField if not provided)

    Requires 3D.
    """
    if coords is None:
        if hasattr(F, 'coords'):
            coords = F.coords
        else:
            raise ValueError("Must provide coords for raw expressions")

    curl = CurlOperator(coords)
    div = DivergenceOperator(coords)

    curl_F = curl(_extract_expr(F))
    div_curl_F = div(curl_F)

    return simplify(div_curl_F) == 0


def laplacian_is_div_grad(f, coords: List[Symbol] = None) -> bool:
    """
    Verify identity: ∂²f = ∂·(∂f) (Laplacian equals divergence of gradient).

    Args:
        f: ScalarField or expression
        coords: Optional coordinates (extracted from ScalarField if not provided)
    """
    if coords is None:
        if hasattr(f, 'coords'):
            coords = f.coords
        else:
            raise ValueError("Must provide coords for raw expressions")

    grad_op = GradientOperator(coords)
    div = DivergenceOperator(coords)
    lap_op = LaplacianOperator(coords)

    lap_f = lap_op(_extract_expr(f))
    grad_f = grad_op(_extract_expr(f))
    div_grad_f = div(grad_f)

    return simplify(lap_f - div_grad_f) == 0


# ============================================================================
# Standalone Convenience Functions (for backward compatibility)
# ============================================================================

def gradient(f: Union[ScalarField, any]) -> VectorField:
    """
    Compute gradient of a scalar field or expression.

    Args:
        f: ScalarField or SymPy expression

    Returns:
        VectorField representing the gradient

    Example:
        >>> coords = make_coords('x y z')
        >>> f = ScalarField('f', coords)
        >>> grad_f = gradient(f)
    """
    if isinstance(f, ScalarField):
        return f.gradient()
    else:
        # For raw expressions, extract coordinates and create operator
        coords = sorted(f.free_symbols, key=lambda s: s.name)
        grad_op = GradientOperator(coords)
        grad_matrix = grad_op(f)
        return VectorField._from_matrix(grad_matrix, coords, name=f'∇{f.func}' if hasattr(f, 'func') else None)


def divergence(F: Union[VectorField, any]):
    """
    Compute divergence of a vector field.

    Args:
        F: VectorField

    Returns:
        Scalar expression representing the divergence

    Example:
        >>> coords = make_coords('x y z')
        >>> F = VectorField('F', coords)
        >>> div_F = divergence(F)
    """
    if isinstance(F, VectorField):
        return F.divergence()
    else:
        raise TypeError("divergence() requires a VectorField")


def curl(F: Union[VectorField, any]) -> VectorField:
    """
    Compute curl of a vector field (3D only).

    Args:
        F: VectorField (must be 3D)

    Returns:
        VectorField representing the curl

    Example:
        >>> coords = make_coords('x y z')
        >>> F = VectorField('F', coords)
        >>> curl_F = curl(F)
    """
    if isinstance(F, VectorField):
        return F.curl()
    else:
        raise TypeError("curl() requires a VectorField")


def laplacian(f: Union[ScalarField, VectorField, any]):
    """
    Compute Laplacian of a scalar field or vector field.

    Args:
        f: ScalarField or VectorField

    Returns:
        For scalar: expression
        For vector: VectorField (component-wise Laplacian)

    Example:
        >>> coords = make_coords('x y z')
        >>> f = ScalarField('f', coords)
        >>> lap_f = laplacian(f)
    """
    if isinstance(f, ScalarField):
        return f.laplacian()
    elif isinstance(f, VectorField):
        lap_op = LaplacianOperator(f.coords)
        lap_matrix = lap_op(f.components)
        return VectorField._from_matrix(lap_matrix, f.coords, name=f'∇²{f.name}' if f.name else None)
    else:
        # For raw expressions
        coords = sorted(f.free_symbols, key=lambda s: s.name)
        lap_op = LaplacianOperator(coords)
        return lap_op(f)


def make_vector_field(name: str, coords: List[Symbol], dim: int = None) -> VectorField:
    """
    Create a symbolic vector field with standard component names.

    Args:
        name: Base name (e.g., 'E', 'B', 'v')
        coords: Coordinate symbols
        dim: Output dimension (default: same as len(coords))

    Returns:
        VectorField with components named name₁, name₂, ...

    Example:
        >>> coords = make_coords('x y z')
        >>> E = make_vector_field('E', coords)
        >>> # Creates E = (E₁(x,y,z), E₂(x,y,z), E₃(x,y,z))
    """
    return VectorField(name, coords, dim=dim)
