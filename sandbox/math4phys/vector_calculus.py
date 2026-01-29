# vector calculus
# 26/01/2026
# Johannes Siedersleben

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
"""


from __future__ import annotations

from typing import Dict, List, Tuple

from sympy import (
    diff, Eq, symbols, Function, Matrix, Symbol, Expr, simplify
)


# ============================================================================
# Helper Functions
# ============================================================================
def make_scalar_field(name: str, args: List[Symbol]) -> Expr:
    """
    Create a real scalar field 
    """
    return Function(f'{name}', real=True)(*args)


def make_vector_field(name: str, args: List[Symbol], dim: int=3) -> Matrix:
    """
    Create a real vector field with components name_1, name_2, ..., name_n
    """
    components = [Function(f'{name}_{i + 1}', real=True)(*args) for i in range(dim)]
    return Matrix(components)


def create_mechanics_variables(n_dim=3):
    q_vars = symbols(f'q1:{n_dim + 1}', real=True)
    p_vars = symbols(f'p1:{n_dim + 1}', real=True)
    v_vars = symbols(f'v1:{n_dim + 1}', real=True)

    q = Matrix(q_vars)
    p = Matrix(p_vars)
    v = Matrix(v_vars)

    return q, v, p


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
    # Convert string keys to Symbol objects by matching against free_symbols
    free_syms = expr.free_symbols
    subs_dict = {}
    for key_str, value in kwargs.items():
        # Find the symbol with matching name
        matching_sym = next((sym for sym in free_syms if sym.name == key_str), None)
        if matching_sym is not None:
            subs_dict[matching_sym] = value
        else:
            # If no match found, try string substitution (works for simple names)
            subs_dict[key_str] = value
    return expr.subs(subs_dict)


def expr_equal(f, g: Expr) -> bool:
    """Check if two expressions are mathematically equal."""
    return simplify(f - g) == 0


def matrices_equal(F, G: Matrix) -> bool:
    """Check if two matrices are mathematically equal."""
    return all(simplify(element) == 0 for element in F - G)


def gradient(f: Expr, args: List[Symbol] = None) -> Matrix:
    """
    return the gradient of f as a (nx1) Matrix of Expr
    If args is None, uses f.free_symbols sorted alphabetically by name.
    """
    if args is None:
        args = sorted(f.free_symbols, key=lambda s: s.name)
    return Matrix([f.diff(arg) for arg in args])


def laplacian(F: Expr | Matrix, args: List[Symbol] = None) -> Expr | Matrix:
    """
    return laplacian of f as an Expr if f is scalar
    return vector of laplacian(f) if F is a vector
    If args is None, uses f.free_symbols sorted alphabetically by name.
    """
    if args is None:
        args = sorted(F.free_symbols, key=lambda s: s.name)
    if isinstance(F, Expr):
        return sum(F.diff(arg, 2) for arg in args)
    else:
        return Matrix([laplacian(f, args) for f in F])


def divergence(F: Matrix, args: List[Symbol] = None) -> Expr:
    """
    return the divergence of F as an Expr
    If args is None, uses f.free_symbols sorted alphabetically by name.
    """
    if args is None:
        args = sorted(F.free_symbols, key=lambda s: s.name)
    return sum(F[i].diff(args[i]) for i in range(len(args)))


def curl(F: Matrix, args: List[Symbol] = None) -> Matrix:
    """
    return the curl of F as a (3x1) Matrix of Expr
    If args is None, uses f.free_symbols sorted alphabetically by name.
    """
    if args is None:
        args = sorted(F.free_symbols, key=lambda s: s.name)
    if not (len(args) == 3 and F.shape == (3, 1)):
        raise TypeError
    components = [
        F[2].diff(args[1]) - F[1].diff(args[2]),
        F[0].diff(args[2]) - F[2].diff(args[0]),
        F[1].diff(args[0]) - F[0].diff(args[1]),
    ]
    return Matrix(components)


def hessian(f: Expr, args: List[Symbol] = None) -> Matrix:
    """
    return the hessian of f as a (mxm) Matrix of Expr
    If args is None, uses f.free_symbols sorted alphabetically by name.
    """
    if args is None:
        args = sorted(f.free_symbols, key=lambda s: s.name)
    return Matrix([[diff(f, i, j) for i in args] for j in args])


def jacobian(F: Matrix, args: List[Symbol] = None) -> Matrix:
    """
    return the Jacobian of F as a (mxn) Matrix of Expr
    If args is None, uses F.free_symbols sorted alphabetically by name.
    """
    if args is None:
        args = sorted(F.free_symbols, key=lambda s: s.name)
    rows = [F.diff(arg).T for arg in args]
    return Matrix.vstack(*rows)


def poisson(A, B: Expr, x, p: List[Symbol]) -> Expr:
    """
    return {A, B}
    x, p are supposed to be disjoint subsets of the arguments of A and B.
    Normally: x = (x_1, x_2, x_3), p = (p_1, p_2, p_3), 
    """
    return (gradient(A, x).T * gradient(B, p) - gradient(A, p).T * gradient(B, x))[0, 0]


def euler_lagrange_equation(L: Expr, x, v: List[Symbol]) -> Eq:
    """
    euler_lagrange accepts any function L of x_1,...x_n, v_1,..., v_n.
    It returns the Euler-Lagrange equation of L.
    """

    # Define time  variable
    t = symbols('t', real=True)

    # substitute time-dependent functions:
    # substitute x_1, x_2, x_3 -> x_1(t), x_2(t), x_3(t)
    # substitute v_1, v_2, v_3 -> dx_1(t)/dt, dx_2(t)/dt, dx_3(t)/dt
    subs_dict = {}
    for i in range(len(x)):
        xi_name = Function(x[i].name)(t)
        subs_dict[x[i]] = xi_name 
        subs_dict[v[i]] = diff(xi_name, t)

    # The gradients are first computed in terms of x and v.
    # Then substitute x -> x(t), v -> dx(t)/dt
    dL_x = gradient(L, x).subs(subs_dict)
    dL_v = gradient(L, v).subs(subs_dict)

    # The Euler-Lagrange equation is an equation in terms of x(t), d^2x/dt^2
    return Eq(diff(dL_v, t), dL_x).doit()


def apply_equation(eq: Eq, X: Expr, x: List[Symbol]) -> Tuple[Expr, Expr]:
    """
    eq: an Euler-Lagrange equation in terms of x_i(t) functions
    and a presumed solution X with free symbols x_1, ... x_n
    """
    
    t = symbols('t', real=True)
    
    # Substitute x_i(t) -> X[i] into eq
    subs_dict = {}
    for i in range(len(x)):
        xi_name = Function(x[i].name)(t)
        subs_dict[xi_name] = X[i]

    # Substitute into both sides of the equation
    eq_lhs = eq.lhs.subs(subs_dict).doit().simplify()
    eq_rhs = eq.rhs.subs(subs_dict).doit().simplify()

    return eq_lhs, eq_rhs


def verify_euler_lagrange(L, X: Expr, x, v: List[Symbol], bc: Dict[Symbol, Expr]) -> List[Bool]:
    """
    Verify that a solution X satisfies the Euler-Lagrange equation and boundary conditions.

    Args:
        L: Lagrangian expression (scalar function of x and v)
        X: Proposed solution (vector-valued function of t)
        x: Position symbols (e.g., [x_1, x_2, x_3])
        v: Velocity symbols (e.g., [v_1, v_2, v_3])
        bc: Boundary conditions as dict {time_value: expected_position_vector}

    Returns:
        List of Bool: One Bool per boundary condition + one for equation satisfaction
    """
    t = symbols('t', real=True)
    result = []

    # Verify each boundary condition: X(t_i) == expected_value
    for k, V in bc.items():
        result.append(matrices_equal(X.subs(t, k), V))

    # Verify X satisfies the Euler-Lagrange equation
    eq = euler_lagrange_equation(L, x, v)
    lhs, rhs = apply_equation(eq, X, x)
    result.append(matrices_equal(lhs, rhs))

    return result


class Lagrange(object):
    """
    A Lagrangian system with its solution and boundary conditions.

    Represents a complete Lagrangian mechanics problem:
    - The Lagrangian L(x, v) defining the system
    - A proposed solution X(t) as a trajectory
    - Position and velocity coordinate symbols
    - Boundary/initial conditions to verify

    Example:
        # Harmonic oscillator
        x = symbols('x_1:4', real=True)
        v = symbols('v_1:4', real=True)
        L = m * V.norm()**2 / 2 - k * X.norm()**2 / 2
        X_ = A * sin(omega * t) + B * cos(omega * t)
        bc = {0: B, pi/(2*omega): A}
        system = Lagrange('harmonic', L, X_, x, v, bc)
        assert system.verify()  # Check solution satisfies equation & BC
    """

    def __init__(self, name, L: Expr, X: Matrix, x: List[Symbol], v: List[Symbol], border_conditions: Dict[Symbol, Expr]):
        """
        Initialize a Lagrangian system.

        Args:
            name: Descriptive name for the system (e.g., 'harmonic oscillator')
            L: Lagrangian expression - scalar function of x and v
            X: Solution trajectory - vector-valued function of t
            x: Position symbols (e.g., [x_1, x_2, x_3])
            v: Velocity symbols (e.g., [v_1, v_2, v_3])
            border_conditions: Dict mapping time values to expected positions
                              e.g., {0: initial_position, T: final_position}

        Raises:
            AssertionError: If dimensions don't match or L doesn't depend on x or v
        """
        # Validate dimensions match
        assert len(x) == len(v) == len(X), \
            f"Dimension mismatch: len(x)={len(x)}, len(v)={len(v)}, len(X)={len(X)}"

        # Validate L depends on at least some of x or v
        # (both is normal, only v is free particle, only x is static potential)
        L_symbols = L.free_symbols
        x_in_L = any(xi in L_symbols for xi in x)
        v_in_L = any(vi in L_symbols for vi in v)
        assert x_in_L or v_in_L, \
            f"Lagrangian must depend on at least some position or velocity symbols. " \
            f"L depends on {L_symbols}, but x={x} and v={v}"

        self.name = name
        self.L = L                          # Lagrangian L(x, v)
        self.X = X                          # Solution X(t)
        self.x = x                          # Position symbols
        self.v = v                          # Velocity symbols
        self.border_conditions = border_conditions  # Boundary conditions

    def verify(self):
        """
        Verify that the solution satisfies the Euler-Lagrange equation and all boundary conditions.

        Returns:
            bool: True if all conditions are satisfied, False otherwise
        """
        result = verify_euler_lagrange(self.L, self.X, self.x, self.v, self.border_conditions)
        return all(result)
