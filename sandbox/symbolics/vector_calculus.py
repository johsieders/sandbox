"""
Symbolic Vector Calculus Engine

A wrapper around SymPy that provides dimension-aware vector fields, scalar fields,
and differential operators for proving vector calculus identities and deriving
equations like Maxwell's equations.

Design philosophy:
- Leverage SymPy's differentiation engine (don't rebuild it)
- Provide clean mathematical notation
- Work with arbitrary dimensions
- Automatic identity verification

Example usage:
    >>> coords = make_coords('x y z')
    >>> f = ScalarField('f', coords)
    >>> grad_f = gradient(f)
    >>> curl_grad_f = curl(grad_f)
    >>> curl_grad_f.simplify()  # Should be zero vector
"""

from sympy import (
    symbols, Function, Matrix, diff, simplify, expand,
    latex, Symbol, Derivative
)
from typing import List, Union, Tuple
from dataclasses import dataclass


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


@dataclass
class ScalarField:
    """
    Represents a scalar field f: R^n → R.

    A scalar-valued function of n coordinates with dimension awareness.

    Attributes:
        name: Name of the scalar field (e.g., 'f', 'phi', 'T')
        coords: List of coordinate symbols [x₁, x₂, ..., xₙ]
        dim: Dimension of the domain (automatically computed)
        func: SymPy Function object representing the field

    Example:
        >>> coords = make_coords('x y z')
        >>> temperature = ScalarField('T', coords)
        >>> temperature.func
        T(x, y, z)
    """
    name: str
    coords: List[Symbol]

    def __post_init__(self):
        """Initialize the SymPy function and dimension."""
        self.dim = len(self.coords)
        self.func = Function(self.name)(*self.coords)

    def __call__(self, *args):
        """Allow evaluation with different coordinates."""
        if len(args) != self.dim:
            raise ValueError(f"Expected {self.dim} arguments, got {len(args)}")
        return Function(self.name)(*args)

    def __repr__(self):
        coord_str = ', '.join(str(c) for c in self.coords)
        return f"ScalarField({self.name}({coord_str}))"

    def __str__(self):
        return self.name

    def diff(self, coord: Symbol, order: int = 1):
        """
        Compute partial derivative with respect to a coordinate.

        Args:
            coord: Coordinate to differentiate with respect to
            order: Order of differentiation (default: 1)

        Returns:
            SymPy expression for the derivative
        """
        return diff(self.func, coord, order)

    def gradient(self) -> 'VectorField':
        """
        Compute gradient: ∇f = (∂f/∂x₁, ∂f/∂x₂, ..., ∂f/∂xₙ)

        Returns:
            VectorField representing the gradient
        """
        components = [diff(self.func, coord) for coord in self.coords]
        return VectorField(components, self.coords, name=f'∇{self.name}')

    def laplacian(self):
        """
        Compute Laplacian: ∇²f = ∂²f/∂x₁² + ∂²f/∂x₂² + ... + ∂²f/∂xₙ²

        Returns:
            SymPy expression for the Laplacian
        """
        return sum(diff(self.func, coord, 2) for coord in self.coords)

    def hessian(self) -> Matrix:
        """
        Compute Hessian matrix: H[i,j] = ∂²f/∂xᵢ∂xⱼ

        Returns:
            SymPy Matrix representing the Hessian
        """
        n = self.dim
        H = Matrix.zeros(n, n)
        for i in range(n):
            for j in range(n):
                H[i, j] = diff(self.func, self.coords[i], self.coords[j])
        return H


class VectorField:
    """
    Represents a vector field F: R^n → R^m.

    A vector-valued function of n coordinates returning m-dimensional vectors.

    Attributes:
        components: List or Matrix of SymPy expressions representing field components
        coords: List of coordinate symbols [x₁, x₂, ..., xₙ]
        input_dim: Dimension of the domain (n)
        output_dim: Dimension of the codomain (m)
        name: Optional name for the field

    Example:
        >>> coords = make_coords('x y z')
        >>> # Create electric field E = (E₁(x,y,z), E₂(x,y,z), E₃(x,y,z))
        >>> E1, E2, E3 = [Function(f'E{i}')(*coords) for i in [1, 2, 3]]
        >>> E = VectorField([E1, E2, E3], coords, name='E')
    """

    def __init__(self, components: Union[List, Matrix], coords: List[Symbol], name: str = None):
        """
        Initialize a vector field.

        Args:
            components: List or Matrix of symbolic expressions
            coords: Coordinate symbols
            name: Optional name for pretty printing
        """
        self.coords = coords
        self.input_dim = len(coords)

        if isinstance(components, Matrix):
            self.components = components
        else:
            self.components = Matrix(components)

        self.output_dim = len(self.components)
        self.name = name

    def __repr__(self):
        if self.name:
            return f"VectorField({self.name}, {self.input_dim}D→{self.output_dim}D)"
        return f"VectorField({self.input_dim}D→{self.output_dim}D)"

    def __str__(self):
        return self.name if self.name else str(self.components)

    def __getitem__(self, index):
        """Access components by index."""
        return self.components[index]

    def __add__(self, other: 'VectorField') -> 'VectorField':
        """Vector field addition."""
        if not isinstance(other, VectorField):
            raise TypeError("Can only add VectorField to VectorField")
        if self.output_dim != other.output_dim:
            raise ValueError(f"Dimension mismatch: {self.output_dim} vs {other.output_dim}")

        new_components = self.components + other.components
        new_name = f"({self.name} + {other.name})" if self.name and other.name else None
        return VectorField(new_components, self.coords, name=new_name)

    def __mul__(self, scalar) -> 'VectorField':
        """Scalar multiplication."""
        new_components = scalar * self.components
        new_name = f"{scalar}*{self.name}" if self.name else None
        return VectorField(new_components, self.coords, name=new_name)

    def __rmul__(self, scalar) -> 'VectorField':
        """Right scalar multiplication."""
        return self.__mul__(scalar)

    def dot(self, other: 'VectorField'):
        """
        Dot product: F · G = Σᵢ Fᵢ Gᵢ

        Returns:
            SymPy expression for the dot product
        """
        if not isinstance(other, VectorField):
            raise TypeError("Can only compute dot product with VectorField")
        if self.output_dim != other.output_dim:
            raise ValueError(f"Dimension mismatch: {self.output_dim} vs {other.output_dim}")

        return sum(self.components[i] * other.components[i]
                   for i in range(self.output_dim))

    def cross(self, other: 'VectorField') -> 'VectorField':
        """
        Cross product: F × G (only for 3D vectors)

        Returns:
            VectorField representing the cross product
        """
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
        return VectorField(cross_components, self.coords, name=new_name)

    def divergence(self):
        """
        Compute divergence: ∇·F = ∂F₁/∂x₁ + ∂F₂/∂x₂ + ... + ∂Fₙ/∂xₙ

        Note: Requires input_dim == output_dim

        Returns:
            SymPy expression for the divergence
        """
        if self.input_dim != self.output_dim:
            raise ValueError(f"Divergence requires square field: "
                           f"input_dim={self.input_dim}, output_dim={self.output_dim}")

        return sum(diff(self.components[i], self.coords[i])
                   for i in range(self.input_dim))

    def curl(self) -> 'VectorField':
        """
        Compute curl: ∇×F (only for 3D vector fields)

        For F = (F₁, F₂, F₃):
        ∇×F = (∂F₃/∂y - ∂F₂/∂z, ∂F₁/∂z - ∂F₃/∂x, ∂F₂/∂x - ∂F₁/∂y)

        Returns:
            VectorField representing the curl
        """
        if self.input_dim != 3 or self.output_dim != 3:
            raise ValueError("Curl only defined for 3D vector fields")

        x, y, z = self.coords
        F1, F2, F3 = self.components[0], self.components[1], self.components[2]

        curl_components = [
            diff(F3, y) - diff(F2, z),  # i component
            diff(F1, z) - diff(F3, x),  # j component
            diff(F2, x) - diff(F1, y),  # k component
        ]

        new_name = f"∇×{self.name}" if self.name else "curl"
        return VectorField(curl_components, self.coords, name=new_name)

    def jacobian(self) -> Matrix:
        """
        Compute Jacobian matrix: J[i,j] = ∂Fᵢ/∂xⱼ

        Returns:
            SymPy Matrix of shape (output_dim, input_dim)
        """
        J = Matrix.zeros(self.output_dim, self.input_dim)
        for i in range(self.output_dim):
            for j in range(self.input_dim):
                J[i, j] = diff(self.components[i], self.coords[j])
        return J

    def simplify(self) -> 'VectorField':
        """
        Simplify all components.

        Returns:
            New VectorField with simplified components
        """
        simplified_components = [simplify(c) for c in self.components]
        return VectorField(simplified_components, self.coords, name=self.name)

    def expand(self) -> 'VectorField':
        """
        Expand all components.

        Returns:
            New VectorField with expanded components
        """
        expanded_components = [expand(c) for c in self.components]
        return VectorField(expanded_components, self.coords, name=self.name)

    def is_zero(self) -> bool:
        """
        Check if all components are zero (after simplification).

        Returns:
            True if the field is identically zero
        """
        simplified = self.simplify()
        return all(simplify(c) == 0 for c in simplified.components)


# Convenience functions for differential operators

def gradient(f: Union[ScalarField, Function]) -> VectorField:
    """
    Compute gradient of a scalar field: ∇f

    Args:
        f: ScalarField or SymPy function with coordinates

    Returns:
        VectorField representing the gradient
    """
    if isinstance(f, ScalarField):
        return f.gradient()
    else:
        # Try to extract coordinates from the function
        coords = list(f.free_symbols)
        components = [diff(f, coord) for coord in coords]
        return VectorField(components, coords, name=f'∇{f.func}')


def divergence(F: VectorField):
    """
    Compute divergence of a vector field: ∇·F

    Args:
        F: VectorField

    Returns:
        SymPy expression for the divergence
    """
    return F.divergence()


def curl(F: VectorField) -> VectorField:
    """
    Compute curl of a vector field: ∇×F (3D only)

    Args:
        F: 3D VectorField

    Returns:
        VectorField representing the curl
    """
    return F.curl()


def laplacian(f: Union[ScalarField, VectorField]):
    """
    Compute Laplacian: ∇²f = ∇·(∇f)

    Args:
        f: ScalarField or VectorField

    Returns:
        For scalar: SymPy expression
        For vector: VectorField (component-wise Laplacian)
    """
    if isinstance(f, ScalarField):
        return f.laplacian()
    elif isinstance(f, VectorField):
        # Component-wise Laplacian
        laplacian_components = []
        for component in f.components:
            lap = sum(diff(component, coord, 2) for coord in f.coords)
            laplacian_components.append(lap)
        return VectorField(laplacian_components, f.coords, name=f'∇²{f.name}')
    else:
        raise TypeError("laplacian requires ScalarField or VectorField")


def directional_derivative(f: ScalarField, v: VectorField):
    """
    Compute directional derivative: v·∇f

    Args:
        f: ScalarField
        v: VectorField (direction)

    Returns:
        SymPy expression for the directional derivative
    """
    grad_f = f.gradient()
    return grad_f.dot(v)


# Vector calculus identity verification functions

def verify_identity(left, right, tolerance=0) -> Tuple[bool, any]:
    """
    Verify a vector calculus identity by symbolic simplification.

    Args:
        left: Left side of identity (VectorField, ScalarField, or expression)
        right: Right side of identity
        tolerance: Not used (for API compatibility)

    Returns:
        Tuple of (is_equal, difference)
    """
    if isinstance(left, VectorField) and isinstance(right, VectorField):
        diff_field = left + (-1 * right)
        simplified = diff_field.simplify()
        is_equal = simplified.is_zero()
        return is_equal, simplified
    else:
        # Scalar expressions
        diff_expr = simplify(left - right)
        is_equal = (diff_expr == 0)
        return is_equal, diff_expr


def curl_of_gradient_is_zero(f: ScalarField) -> bool:
    """
    Verify identity: ∇×(∇f) = 0 (curl of gradient is always zero)

    Args:
        f: ScalarField (must be 3D)

    Returns:
        True if identity holds
    """
    if f.dim != 3:
        raise ValueError("This identity requires 3D scalar field")

    grad_f = gradient(f)
    curl_grad_f = curl(grad_f)

    return curl_grad_f.is_zero()


def divergence_of_curl_is_zero(F: VectorField) -> bool:
    """
    Verify identity: ∇·(∇×F) = 0 (divergence of curl is always zero)

    Args:
        F: VectorField (must be 3D)

    Returns:
        True if identity holds
    """
    if F.input_dim != 3 or F.output_dim != 3:
        raise ValueError("This identity requires 3D vector field")

    curl_F = curl(F)
    div_curl_F = divergence(curl_F)

    return simplify(div_curl_F) == 0


def laplacian_is_div_grad(f: ScalarField) -> bool:
    """
    Verify identity: ∇²f = ∇·(∇f) (Laplacian equals divergence of gradient)

    Args:
        f: ScalarField

    Returns:
        True if identity holds
    """
    lap_f = f.laplacian()
    grad_f = f.gradient()
    div_grad_f = grad_f.divergence()

    return simplify(lap_f - div_grad_f) == 0


# Helper function for creating vector fields from function names

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
    if dim is None:
        dim = len(coords)

    components = [Function(f'{name}{i+1}')(*coords) for i in range(dim)]
    return VectorField(components, coords, name=name)