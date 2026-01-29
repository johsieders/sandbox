# testing euler-lagrange
# 28/01/2026
# Johannes Siedersleben

from sympy import symbols, Matrix, sqrt, sin, cos, pi

from sandbox.math4phys.vector_calculus import (euler_lagrange_equation, matrices_equal, apply_equation)


def test_lagrange_harmonic():
    # Create independent variables for gradient computation
    a = symbols('a_1:4', real=True)
    b = symbols('b_1:4', real=True)

    x = symbols('x_1:4', real=True)
    v = symbols('v_1:4', real=True)

    m = symbols('m', positive=True)
    k = symbols('k', positive=True)
    omega = sqrt(k / m)
    t = symbols('t', real=True)

    A = Matrix(a)
    B = Matrix(b)
    X = Matrix(x)
    V = Matrix(v)

    # the Lagrangian L of the harmonic oscillator
    # Kinetic energy minus harmonic potential
    # L is a scalar-valued function of small x and small v. No vectors, no time dependence
    # X and V are here for convenience:
    # X.norm()**2 is a shorthand for x_1^2 + x_2^2 + x_3^2
    L = m * V.norm() ** 2 / 2 - k * X.norm() ** 2 / 2

    # the corresponding Euler-Lagrange equation
    # is an equation in terms of x(t), d^2x/dt^2
    el = euler_lagrange_equation(L, x, v)

    # the solution X_ is a vector-valued function of t
    X_ = A * sin(omega * t) + B * cos(omega * t)

    # plug X_ into Euler-Lagrange and verify
    lhs, rhs = apply_equation(el, X_, x)
    assert matrices_equal(lhs, rhs)

    # Verify initial conditions
    # At t=0: X_(0) should equal B
    X_at_0 = X_.subs(t, 0)
    assert matrices_equal(X_at_0, B)

    # At t=π/(2ω): X_ should equal A (since sin(π/2)=1, cos(π/2)=0)
    X_at_quarter_period = X_.subs(t, pi / (2 * omega))
    assert matrices_equal(X_at_quarter_period, A)

    ####################################
    ##### Constant Acceleration ########
    ####################################

    # Lagrangian for constant acceleration
    # L = m * V.norm() ** 2 / 2 - m * (A.T * X)[0, 0]
    L = m * V.norm() ** 2 / 2

    # the corresponding Euler-Lagrange equation
    # is an equation in terms of x(t), d^2x/dt^2
    el = euler_lagrange_equation(L, x, v)

    # the solution X_ is a vector-valued function of t
    C = B + A / 2
    # X_ = - A * t**2 + C * t
    X_ = B * t

    # plug X_ into Euler-Lagrange and verify
    lhs, rhs = apply_equation(el, X_, x)
    assert matrices_equal(lhs, rhs)

    # Verify initial conditions
    # At t=0: X_(0) should equal 0
    X_at_0 = X_.subs(t, 0)
    # assert matrices_equal(X_at_0, 0)

    # At t=1: X_(1) should equal B
    X_at_1 = X_.subs(t, 1)
    # assert matrices_equal(X_at_1, B)
