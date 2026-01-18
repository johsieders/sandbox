"""
Poisson Brackets with SymPy

Implementation of Poisson brackets using vector notation:
{f, g} = ∇ₓf · ∇ₚg - ∇ₚf · ∇ₓg

where x = (x₁, ..., xₙ) are position coordinates
and p = (p₁, ..., pₙ) are momentum coordinates.
"""

from sympy import Matrix, Function, symbols, simplify, expand, diff


def create_phase_space(n_dim: int):
    """
    Create symbolics phase space coordinates as vectors.

    Args:
        n_dim: Number of degrees of freedom (dimension of phase space / 2)

    Returns:
        Tuple of (x, p) where each is a Matrix (column vector) of symbolics variables
    """
    x_vars = symbols(f'x1:{n_dim+1}', real=True)
    p_vars = symbols(f'p1:{n_dim+1}', real=True)

    x = Matrix(x_vars)
    p = Matrix(p_vars)

    return x, p


def poisson_bracket(f, g, x, p):
    """
    Compute the Poisson bracket {f, g} using vector notation.

    {f, g} = ∇ₓf · ∇ₚg - ∇ₚf · ∇ₓg

    Args:
        f: SymPy expression or Function
        g: SymPy expression or Function
        x: Position coordinates - either a Matrix/sequence of symbols
        p: Momentum coordinates - either a Matrix/sequence of symbols

    Returns:
        SymPy expression representing {f, g}
    """
    # Handle both Matrix and sequence inputs
    # Extract components for iteration
    if isinstance(x, Matrix):
        x_components = list(x)
    else:
        x_components = list(x)

    if isinstance(p, Matrix):
        p_components = list(p)
    else:
        p_components = list(p)

    # Compute gradient vectors (as column vectors)
    grad_x_f = Matrix([diff(f, xi) for xi in x_components])
    grad_p_f = Matrix([diff(f, pi) for pi in p_components])
    grad_x_g = Matrix([diff(g, xi) for xi in x_components])
    grad_p_g = Matrix([diff(g, pi) for pi in p_components])

    # Poisson bracket: ∇ₓf · ∇ₚg - ∇ₚf · ∇ₓg
    result = grad_x_f.dot(grad_p_g) - grad_p_f.dot(grad_x_g)

    return result


def verify_jacobi_identity(n_dim: int = 2):
    """
    Formally verify the Jacobi identity for arbitrary functions f, g, h.

    Jacobi identity: {f, {g, h}} + {g, {h, f}} + {h, {f, g}} = 0

    Args:
        n_dim: Number of degrees of freedom (dimension of phase space / 2)

    Returns:
        Tuple of (simplified_result, is_zero)
        where simplified_result is the SymPy expression and is_zero is True if it equals 0
    """
    # Create phase space coordinates as vectors
    x, p = create_phase_space(n_dim)

    # Create arbitrary symbolics functions
    # These represent generic functions f(x, p), g(x, p), h(x, p)
    f = Function('f')(*x, *p)
    g = Function('g')(*x, *p)
    h = Function('h')(*x, *p)

    # Compute the three terms of the Jacobi identity
    # Now we just pass x and p directly!
    term1 = poisson_bracket(f, poisson_bracket(g, h, x, p), x, p)
    term2 = poisson_bracket(g, poisson_bracket(h, f, x, p), x, p)
    term3 = poisson_bracket(h, poisson_bracket(f, g, x, p), x, p)

    # Sum the three terms
    jacobi_sum = term1 + term2 + term3
    jacobi_expanded = expand(jacobi_sum)

    # Simplify - should be exactly zero
    simplified = simplify(jacobi_expanded)

    is_zero = (simplified == 0)

    return simplified, is_zero


if __name__ == "__main__":
    # Example: 1D phase space (using sequences)
    print("=" * 60)
    print("Example 1: Simple 1D case (sequence interface)")
    print("=" * 60)
    x, p = symbols('x p', real=True)

    # Example functions
    f_example = x**2 + p**2  # Energy-like function
    g_example = x * p        # Angular momentum-like

    bracket = poisson_bracket(f_example, g_example, [x], [p])
    print(f"f = {f_example}")
    print(f"g = {g_example}")
    print(f"{{f, g}} = {bracket}")
    print()

    # Canonical coordinates: {x, p} = 1
    canonical_bracket = poisson_bracket(x, p, [x], [p])
    print(f"Canonical relation: {{x, p}} = {canonical_bracket}")
    print()

    # Example: 2D phase space (using create_phase_space)
    print("=" * 60)
    print("Example 2: 2D case (vector interface)")
    print("=" * 60)
    x, p = create_phase_space(2)
    print(f"x = {x.T}")  # Transpose for row display
    print(f"p = {p.T}")
    print()

    # Angular momentum in 2D: L = x1*p2 - x2*p1
    L = x[0]*p[1] - x[1]*p[0]
    print(f"L = {L}")

    # Now compute brackets directly with x and p vectors!
    bracket_x1_L = poisson_bracket(x[0], L, x, p)
    bracket_p1_L = poisson_bracket(p[0], L, x, p)
    print(f"{{x1, L}} = {bracket_x1_L}")
    print(f"{{p1, L}} = {bracket_p1_L}")
    print()

    print("=" * 60)
    print("Jacobi Identity Verification (Formal Proof)")
    print("=" * 60)

    # Verify for 1D
    print("\n1D Phase Space (n=1):")
    result_1d, is_zero_1d = verify_jacobi_identity(n_dim=1)
    print(f"{{f, {{g, h}}}} + {{g, {{h, f}}}} + {{h, {{f, g}}}} = {result_1d}")
    print(f"Is zero? {is_zero_1d}")

    # Verify for 2D
    print("\n2D Phase Space (n=2):")
    result_2d, is_zero_2d = verify_jacobi_identity(n_dim=2)
    print(f"{{f, {{g, h}}}} + {{g, {{h, f}}}} + {{h, {{f, g}}}} = {result_2d}")
    print(f"Is zero? {is_zero_2d}")

    # Verify for 3D
    print("\n3D Phase Space (n=3):")
    result_3d, is_zero_3d = verify_jacobi_identity(n_dim=3)
    print(f"{{f, {{g, h}}}} + {{g, {{h, f}}}} + {{h, {{f, g}}}} = {result_3d}")
    print(f"Is zero? {is_zero_3d}")

    print("\n" + "=" * 60)
    if is_zero_1d and is_zero_2d and is_zero_3d:
        print("✓ Jacobi identity verified formally for arbitrary functions!")
    else:
        print("✗ Jacobi identity verification failed")
    print("=" * 60)
