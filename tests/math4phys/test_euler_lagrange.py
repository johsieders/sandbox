# testing euler-lagrange
# 28/01/2026
# Johannes Siedersleben

from sympy import symbols, Matrix, sqrt, sin, cos, pi, zeros
from sandbox.math4phys.vector_calculus import (Lagrange)


def test_euler_lagrange():
    # a catalogue of Lagrange systems
    catalogue = []

    # Symbols we need for Lagrangians and solutions
    c = symbols('c_1:4', real=True)
    d = symbols('d_1:4', real=True)

    x = symbols('x_1:4', real=True)
    y = symbols('y_1:4', real=True)
    v = symbols('v_1:4', real=True)
    w = symbols('w_1:4', real=True)

    m = symbols('m', positive=True)
    k = symbols('k', positive=True)
    omega = sqrt(k / m)
    t = symbols('t', real=True)

    # Helper variables for matrix operations 
    C = Matrix(c)
    D = Matrix(d)
    X = Matrix(x)
    Y = Matrix(y)
    V = Matrix(v)
    W = Matrix(w)

    # no acceleration
    L = m * W.norm() ** 2 / 2
    X_ = D * t
    border_conditions = {0: zeros(3, 1), 1: D}
    catalogue.append(Lagrange('no acceleration', L, X_, y, w, border_conditions))

    # constant acceleration
    L = m * V.norm() ** 2 / 2 - m * (C.T * Y)[0, 0]
    X_ = - C * t ** 2 / 2 + (D + C / 2) * t
    border_conditions = {0: zeros(3, 1), 1: D}
    catalogue.append(Lagrange('constant acceleration', L, X_, y, v, border_conditions))

    # the Lagrangian L of the harmonic oscillator
    # Kinetic energy minus harmonic potential
    # L is a scalar-valued function of small x and small v. No vectors, no time dependence
    # X and V are here for convenience only:
    # X.norm()**2 is a shorthand for x_1^2 + x_2^2 + x_3^2
    # the solution X_ is a vector-valued function of t
    # Border conditions: X_(0) == B, X_0(pi / (2 * omega)) == A
    L = m * V.norm() ** 2 / 2 - k * X.norm() ** 2 / 2
    X_ = C * sin(omega * t) + D * cos(omega * t)
    border_conditions = {0: D, pi / (2 * omega): C}
    catalogue.append(Lagrange('harmonic oscillator', L, X_, x, v, border_conditions))

    for sys in catalogue:
        assert sys.verify()
