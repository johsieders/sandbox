# Euler-Lagrange
# 01/02/2026
# Johannes Siedersleben

"""
Euler-Lagrange equation solver for classical mechanics.

This module provides functions to:
- Derive Euler-Lagrange equations from a Lagrangian
- Solve the equations with boundary conditions
- Verify solutions satisfy the equations and boundary conditions

Mathematical background:
The Euler-Lagrange equation for a Lagrangian L(x, ẋ, t) is:
    d/dt(∂L/∂ẋ) - ∂L/∂x = 0

This gives the equations of motion for a classical mechanical system.
"""

from __future__ import annotations

from typing import Dict, List, Union

from sympy import (
    diff, dsolve, Eq, symbols, Function, Matrix, Symbol, Expr, solve, pprint
)

from math4phys.diff_ops import gradient, matrices_equal


def get_euler_lagrange(L: Expr, x: List[Symbol], v: List[Symbol]) -> Eq:
    """
    Derive the Euler-Lagrange equation from a Lagrangian.

    Args:
        L: Lagrangian expression as a function of position variables x and velocity variables v
        x: List of position symbols (e.g., [x_1, x_2, x_3])
        v: List of velocity symbols (e.g., [v_1, v_2, v_3])

    Returns:
        An equation d/dt(∂L/∂v) = ∂L/∂x in terms of time-dependent functions x(t)

    Example:
        >>> x = symbols('x_1:3', real=True)
        >>> v = symbols('v_1:3', real=True)
        >>> m, k = symbols('m k', positive=True)
        >>> L = m * sum(vi**2 for vi in v) / 2 - k * sum(xi**2 for xi in x) / 2
        >>> eq = get_euler_lagrange(L, x, v)
    """
    # Define time variable and time-dependent position functions x_i(t)
    t = symbols('t', real=True)
    x_t = [Function(x[i].name)(t) for i in range(len(x))]

    # Build substitution dictionary: x_i -> x_i(t), v_i -> dx_i(t)/dt
    # This transforms the Lagrangian from L(x, v) to L(x(t), ẋ(t))
    subs_dict = {x[i]: x_t[i] for i in range(len(x))}
    subs_dict.update({v[i]: diff(x_t[i], t) for i in range(len(x))})

    # Compute partial derivatives ∂L/∂x and ∂L/∂v, then substitute time-dependent functions
    dL_dx = gradient(L, x).subs(subs_dict)
    dL_dv = gradient(L, v).subs(subs_dict)

    # Return the Euler-Lagrange equation: d/dt(∂L/∂v) = ∂L/∂x
    return Eq(diff(dL_dv, t), dL_dx).doit()


def solve_euler_lagrange(eq: Eq, x: List[Symbol], bcs: Dict[Union[float, Expr], Matrix] = None) -> Matrix:
    """
    Solve the Euler-Lagrange equation with boundary conditions.

    This is a two-step process:
    1. Find the general solution with arbitrary constants (using dsolve)
    2. Apply boundary conditions to determine the constants

    Args:
        eq: Euler-Lagrange equation from euler_lagrange_equation()
        x: List of position symbols (same as used in euler_lagrange_equation)
        bcs: Boundary conditions as {time: position_vector}
              Time can be numeric or symbolic (e.g., pi/2, sqrt(2), etc.)
              Example: {0: Matrix([0, 0, 0]), 1: Matrix([1, 1, 1])}
              means x(0) = (0,0,0) and x(1) = (1,1,1)
              Symbolic example: {0: c_vec, pi/(2*omega): d_vec}

    Returns:
        Solution vector x(t) as a Matrix with boundary conditions applied

    Note:
        - For nth order ODE, you need n boundary conditions per component
        - Boundary conditions can be at different times (boundary value problem)
        - Constants are determined by solving a linear system
    """
    # Define time variable and time-dependent position functions x_i(t)
    # Use x[i].name to maintain consistency with input symbols
    t = symbols('t', real=True)
    x_t = [Function(x[i].name)(t) for i in range(len(x))]

    # Get general solution with arbitrary constants (C1, C2, ...)
    # dsolve returns a list of Eq objects: [Eq(x_1(t), C1 + C2*t), ...]
    x_sol = dsolve(eq.lhs - eq.rhs, x_t)

    if bcs is None:
        return Matrix(x_sol)

    # Extract integration constants from all solution components
    # These are the unknowns we'll solve for using boundary conditions
    all_constants = set()
    for sol_eq in x_sol:
        all_constants.update(sol_eq.rhs.free_symbols - {t})
    all_constants = sorted(all_constants, key=lambda s: s.name)

    # Build system of equations from boundary conditions
    # For each time point and each component: x_i(t_val) = boundary_value
    bc_eqs = [
        Eq(x_sol[i].rhs.subs(t, t_val), boundary_vec[i])
        for t_val, boundary_vec in bcs.items()
        for i in range(len(x))
    ]

    # Solve the linear system for all integration constants
    # solve() can return:
    # - dict: {C1: value1, C2: value2, ...} for simple cases
    # - list of tuples: [(value1, value2, ...)] where values match all_constants order
    constants = solve(bc_eqs, all_constants)

    # Handle different return types from solve()
    if isinstance(constants, list):
        if len(constants) == 0:
            raise ValueError("No solution found for the given boundary conditions")
        # Take the first solution if multiple exist
        solution_tuple = constants[0]
        # Convert tuple to dict by zipping with all_constants
        if isinstance(solution_tuple, tuple):
            constants = dict(zip(all_constants, solution_tuple))
        else:
            constants = solution_tuple

    # Substitute constants back into general solution
    return Matrix([x_sol[i].rhs.subs(constants) for i in range(len(x))])


def check_euler_lagrange(solution: Matrix, eq: Eq, x: List[Symbol], bcs: Dict[Union[float, Expr], Matrix] = None) -> \
List[
    bool]:
    """
    Verify that a solution satisfies the Euler-Lagrange equation and boundary conditions.

    Args:
        solution: Proposed solution vector x(t) as a Matrix
        eq: Euler-Lagrange equation to verify against
        x: List of position symbols (same as used in euler_lagrange_equation)
        bcs: Boundary conditions to verify as {time: position_vector}
             Time can be numeric or symbolic

    Returns:
        List of boolean values:
        - First element: True if solution satisfies the differential equation
        - Remaining elements: True if solution satisfies each boundary condition

    Example:
        >>> success = check_euler_lagrange(solution, eq, x, {0: C, 1: D})
        >>> assert all(success)  # Verify all checks pass
    """
    # Define time variable and symbolic functions x_i(t)
    t = symbols('t', real=True)
    x_t = [Function(x[i].name)(t) for i in range(len(x))]

    # Build substitution: replace x_i(t) with actual solution expressions
    subs_dict = {x_t[i]: solution[i] for i in range(len(x))}

    # Verify the differential equation: substitute solution into both sides
    lhs = eq.lhs.subs(subs_dict).doit().simplify()
    rhs = eq.rhs.subs(subs_dict).doit().simplify()
    result = [matrices_equal(lhs, rhs)]

    if bcs is None:
        return result

    # Verify each boundary condition: x(t_val) should equal boundary_vec
    for t_val, boundary_vec in bcs.items():
        result.append(matrices_equal(solution.subs(t, t_val), boundary_vec))

    return result


def run_euler_lagrange(lagrangian: Expr, x, v: List[Symbol],
                       bcs: Dict[Union[float, Expr], Matrix]):
    """
    Euler-Lagrange test runner for Lagrangians
    """

    # Solve the system and check solution
    eq = get_euler_lagrange(lagrangian, x, v)
    x_sol = solve_euler_lagrange(eq, x, bcs)
    success = check_euler_lagrange(x_sol, eq, x, bcs)
    assert all(success), "Solution failed verification"

    # Display results
    print('\nSolution with boundary conditions x(0)=c, x(1)=d:')
    pprint(x_sol)
