# testing euler-lagrange
# 31/01/2026
# Johannes Siedersleben

from typing import List
from sympy import diff, Symbol, symbols, Expr, Function, Matrix, sqrt, sin, cos, pi, zeros, pprint, solve, Eq, exp

from math4phys.vector_calculus import euler_lagrange_equation
from sandbox.math4phys.vector_calculus import (curl, jacobian, gradient, make_vector_field, matrices_equal)


def lagrange_mf(A: Matrix, x: List[Symbol]):
   
    n_dim = len(x)
    v = symbols(f'v_1:{n_dim + 1}', real=True)
    m = symbols('m', positive=True)
    q = symbols('q', real=True)
    t = symbols('t', real=True)
    
    V = Matrix(v)

    L = m * V.norm() ** 2 / 2 + q * (A.T * V)[0, 0]
    el = euler_lagrange_equation(L, x, v)
    
    # Create symbols for x_t, x_ddot_t
    # x_t = [x_1(t), x_2(t), x_3(t)]
    # x_ddot_t = [d^2x_1(t)/dt^2, d^2x_2(t)/dt^2, d^2x_3(t)/dt^2]
    x_t = [Function(x[i].name)(t) for i in range(len(x))]
    x_ddot_t = [diff(xi, t, 2) for xi in x_t]

    # Solve el.lhs - el.rhs = 0 for the second derivatives
    # This gives us ẍ = (RHS - other terms) / m
    solutions = solve(el.lhs - el.rhs, x_ddot_t)
    RHS = Matrix([solutions[xi] for xi in x_ddot_t])

    # Substitute x -> x(t) in B
    subs_dict = {x[i]: x_t[i] for i in range(len(x))}
    B = curl(A, x).subs(subs_dict)
    
    print("\nMagnetic field B = curl(A):")
    pprint(B)
    print("\nAcceleration d²x/dt²:")
    pprint(RHS)


def test_lagrange_mf():
    n_dim = 3
    x = symbols(f'x_1:{n_dim + 1}', real=True)

    # Linear: A(x) = (0, b_1*x, 0) gives B = (0, 0, b_1)
    b_1 = symbols('b_1', real=True)
    A = Matrix([0, b_1 * x[0], 0])
    lagrange_mf(A, x)

    # Nonlinear: A(x) = (-y³, x³, 0) gives B = (0, 0, 3(x²+y²))
    A = Matrix([-x[1] ** 3, x[0] ** 3, 0])
    lagrange_mf(A, x)

    # Uniform B field: A = (-B_z*y/2, B_z*x/2, 0)
    B_z = symbols('B_z', real=True)
    A = Matrix([-B_z * x[1] / 2, B_z * x[0] / 2, 0])
    lagrange_mf(A, x)
