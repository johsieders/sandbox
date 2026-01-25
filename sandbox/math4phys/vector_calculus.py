# vector calculus
# 25/01/2026
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

# todo
# review evaluate and substitution
# replace x with x(t), apply chain rule


from __future__ import annotations

from typing import List

from sympy import (
    diff, symbols, Function, Matrix, Symbol, Expr, simplify
)


# ============================================================================
# Helper Functions
# ============================================================================
def make_scalar_field(name: str, args: List[Symbol]) -> Expr:
    """
    Create a real scalar field 
    """
    return Function(f'{name}', real=True)(*args)


def make_vector_field(name: str, args: List[Symbol], dim: int = 3) -> Matrix:
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
    """How would you modify 
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
