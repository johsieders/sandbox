# Testing Euler-Lagrange equation solver
# 02/02/2026
# Johannes Siedersleben

"""
Tests for the Euler-Lagrange equation solver.

These tests verify that the solver correctly:
1. Derives Euler-Lagrange equations from Lagrangians
2. Solves the equations with boundary conditions
3. Verifies solutions satisfy both the equation and boundary conditions
"""

from sympy import diff, solve, symbols, Function, Matrix, pi, pprint, dsolve

from math4phys.diff_ops import (
    curl, jacobian, make_vector_field, matrices_equal
)
from math4phys.euler_lagrange import (
    get_euler_lagrange,
    run_euler_lagrange
)


def test_magnetic_field():
    """
    Test Euler-Lagrange for magnetic fields
    """
    n_dim = 3
    m = symbols('m', positive=True)
    q = symbols('q', real=True)

    # Boundary condition values
    c = symbols(f'c_1:{n_dim + 1}', real=True)
    d = symbols(f'd_1:{n_dim + 1}', real=True)
    c_vec = Matrix(c)
    d_vec = Matrix(d)

    # Position and velocity symbols
    x = symbols(f'x_1:{n_dim + 1}', real=True)
    t = symbols('t', real=True)
    x_t = [Function(x[i].name)(t) for i in range(len(x))]
    x_dot_t = [diff(xi, t, 1) for xi in x_t]
    x_ddot_t = [diff(xi, t, 2) for xi in x_t]
    v = symbols(f'v_1:{n_dim + 1}', real=True)
    v_vec = Matrix(v)

    # Create dictionary for x -> x(t), v -> x_dot(t)
    subs_x_v = {x[i]: x_t[i] for i in range(len(x))}
    subs_x_v.update({v[i]: x_dot_t[i] for i in range(len(x))})

    #############################################
    ### Lagrangian of general magnetic field  ###
    #############################################
    A = make_vector_field('A', x, n_dim)
    # A = Matrix([Function(f'A_{i + 1}', real=True)(*x) for i in range(n_dim)])
    L = m * v_vec.norm() ** 2 / 2 + q * (A.T * v_vec)[0, 0]


    ###################################################################
    ### (1) Substituting A(x) = (0, a_1*x, 0) gives B = (0, 0, a_1) ###
    ###################################################################
    a_1 = symbols('a_1', real=True)
    A1 = Matrix([0, a_1 * x[0], 0])
    subs_A1 = {A[i]: A1[i] for i in range(n_dim)}
    L1 = L.subs(subs_A1)

    omega = a_1 * q / m
    bcs = {0: c_vec, pi / (2 * omega): d_vec}
    run_euler_lagrange(L1, x, v, bcs)

    # compute RHS of euler-lagrange directly
    B = curl(A1, x).subs(subs_x_v)
    LHS = Matrix(x_ddot_t)
    RHS = (q / m * v_vec.cross(B)).subs(subs_x_v)
    eqs = [LHS[i] - RHS[i] for i in range(n_dim)]
    x_sol = dsolve(eqs, x_t)
    pprint(x_sol)


    #####################################################
    ### (2) Substituting A = (-a_3*y/2, a_3*x/2, 0)   ###
    #####################################################
    a_3 = symbols('a_3', real=True)
    A2 = Matrix([-a_3 * x[1] / 2, a_3 * x[0] / 2, 0])
    subs_A2 = {A[i]: A2[i] for i in range(n_dim)}
    L2 = L.subs(subs_A2)

    omega = a_3 * q / m
    bcs = {0: c_vec, pi / (2 * omega): d_vec}
    run_euler_lagrange(L2, x, v, bcs)

    # compute RHS of euler-lagrange directly
    B = curl(A2, x).subs(subs_x_v)
    LHS = Matrix(x_ddot_t)
    RHS = (q / m * v_vec.cross(B)).subs(subs_x_v)
    eqs = [LHS[i] - RHS[i] for i in range(n_dim)]
    x_sol = dsolve(eqs, x_t)
    pprint(x_sol)


def test_general_mf():
    n_dim = 3

    x = symbols(f'x_1:{n_dim + 1}', real=True)
    v = symbols(f'v_1:{n_dim + 1}', real=True)
    m = symbols('m', positive=True)
    q = symbols('q', real=True)

    # Create symbols for x_t, x_dot_t, x_ddot_t
    t = symbols('t', real=True)
    x_t = [Function(x[i].name)(t) for i in range(len(x))]
    x_dot_t = [diff(xi, t, 1) for xi in x_t]
    x_ddot_t = [diff(xi, t, 2) for xi in x_t]

    # Create dictionnary for x -> x(t), v -> x_dot(t)
    subs_xt_xdot = {x[i]: x_t[i] for i in range(len(x))}
    subs_xt_xdot.update({v[i]: x_dot_t[i] for i in range(len(x))})

    A = make_vector_field('A', x, n_dim)
    V = Matrix(v)

    # L is a function of x and v
    L = m * V.norm() ** 2 / 2 + q * (A.T * V)[0, 0]
    eq = get_euler_lagrange(L, x, v)

    # Solve el.lhs - el.rhs = 0 for the second derivatives
    # This gives us ẍ = (RHS - other terms) / m
    rhs = solve(eq, x_ddot_t)
    RHS = Matrix([rhs[xi] for xi in x_ddot_t])

    # RHS2: Using Jacobian difference
    # The formula is: q/m * (∇A - (∇A)^T) * v = q/m * (J_A - J_A^T) * v
    RHS2 = (q / m * (jacobian(A, x) - jacobian(A, x).T) * V).subs(subs_xt_xdot)

    # RHS3: Using cross product v × B
    B = curl(A, x)
    RHS3 = (q / m * V.cross(B)).subs(subs_xt_xdot)

    RHS = RHS.applyfunc(lambda x: x.simplify())
    RHS2 = RHS2.applyfunc(lambda x: x.simplify())
    RHS3 = RHS3.applyfunc(lambda x: x.simplify())

    assert matrices_equal(RHS, RHS2)
    assert matrices_equal(RHS2, RHS3)
