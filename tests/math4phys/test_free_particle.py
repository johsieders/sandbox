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

from sympy import symbols, Matrix, sqrt, pi

from math4phys.euler_lagrange import (
    run_euler_lagrange
)


def test_free_particle():
    """
    Test Euler-Lagrange for free particles
    """
    n_dim = 3
    m = symbols('m', positive=True)

    # Boundary condition values
    c = symbols(f'c_1:{n_dim + 1}', real=True)
    d = symbols(f'd_1:{n_dim + 1}', real=True)
    c_vec = Matrix(c)
    d_vec = Matrix(d)

    # Position and velocity symbols
    x = symbols(f'x_1:{n_dim + 1}', real=True)
    v = symbols(f'v_1:{n_dim + 1}', real=True)
    x_vec = Matrix(x)
    v_vec = Matrix(v)

    ### Lagrangian of zero acceleration: L = T = (m/2)|v|²
    L = m * v_vec.norm() ** 2 / 2
    bcs = {0: c_vec, 1: d_vec}
    run_euler_lagrange(L, x, v, bcs)

    ### Lagrangian of constant acceleration: L = T = (m/2)|v|² - m ax
    a = symbols(f'a_1:{n_dim + 1}', real=True)
    a_vec = Matrix(a)
    L = m * v_vec.norm() ** 2 / 2 - m * (a_vec.T * x_vec)[0, 0]
    bcs = {0: c_vec, 1: d_vec}
    run_euler_lagrange(L, x, v, bcs)

    ### Lagrangian of a harmonic oscillator
    k = symbols('k', positive=True)
    omega = sqrt(k / m)
    L = m * v_vec.norm() ** 2 / 2 - k * x_vec.norm() ** 2 / 2
    bcs = {0: c_vec, pi / (2 * omega): d_vec}
    run_euler_lagrange(L, x, v, bcs)
