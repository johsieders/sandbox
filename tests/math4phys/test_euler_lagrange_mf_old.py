# testing euler-lagrange
# 31/01/2026
# Johannes Siedersleben

from sympy import diff, symbols, Function, Matrix, sqrt, sin, cos, pi, zeros, pprint, solve, Eq, exp

from math4phys.vector_calculus import euler_lagrange_equation
from sandbox.math4phys.vector_calculus import (curl, jacobian, gradient, make_vector_field, matrices_equal)


def test_lagrange_mf():
   
    n_dim = 3
    x = symbols(f'x_1:{n_dim + 1}', real=True)
    v = symbols(f'v_1:{n_dim + 1}', real=True)
    m = symbols('m', positive=True)
    q = symbols('q', real=True)
    t = symbols('t', real=True)

    A = make_vector_field('A', x, n_dim)
    V = Matrix(v)
    
    # L is a function of x and v
    L = m * V.norm() ** 2 / 2 + q * (A.T * V)[0, 0]
    el = euler_lagrange_equation(L, x, v)

    # Create symbols for x_t, x_dot_t, x_ddot_t
    # x_t = [x_1(t), x_2(t), x_3(t)]
    # x_dot_t = [dx_1(t)/dt, dx_2(t)/dt, dx_3(t)/dt]
    # x_ddot_t = [d^2x_1(t)/dt^2, d^2x_2(t)/dt^2, d^2x_3(t)/dt^2]
    x_t = [Function(x[i].name)(t) for i in range(len(x))]
    x_dot_t = [diff(xi, t, 1) for xi in x_t]
    x_ddot_t = [diff(xi, t, 2) for xi in x_t]

    # Solve el.lhs - el.rhs = 0 for the second derivatives
    # This gives us ẍ = (RHS - other terms) / m
    solutions = solve(el.lhs - el.rhs, x_ddot_t)
    RHS1 = Matrix([solutions[xi] for xi in x_ddot_t])

    # Substitute x -> x(t), v -> x_dot(t)  for RHS2 and RHS3
    subs_dict = {}
    for i in range(len(x)):
        subs_dict[x[i]] = x_t[i]
        subs_dict[v[i]] = x_dot_t[i]

    # RHS2: Using Jacobian difference
    # The formula is: q/m * (∇A - (∇A)^T) * v = q/m * (J_A - J_A^T) * v
    RHS2 = (q / m * (jacobian(A, x) - jacobian(A, x).T) * V).subs(subs_dict)

    # RHS3: Using cross product v × B
    B = curl(A, x)
    RHS3 = (q / m * V.cross(B)).subs(subs_dict)

    RHS1 = RHS1.applyfunc(lambda x: x.simplify())
    RHS2 = RHS2.applyfunc(lambda x: x.simplify())
    RHS3 = RHS3.applyfunc(lambda x: x.simplify())

    assert matrices_equal(RHS1, RHS2)
    assert matrices_equal(RHS2, RHS3)


def test_mf_examples():
    """Test three specific magnetic field configurations."""

    n_dim = 3
    x = symbols('x_1:4', real=True)
    v = symbols('v_1:4', real=True)
    m = symbols('m', positive=True)
    q = symbols('q', positive=True)
    t = symbols('t', real=True)

    # X = Matrix(x)
    V = Matrix(v)

    print("\n" + "="*70)
    print("EXAMPLE 1: Linear vector potential A = (0, b_1*x, 0)")
    print("Gives uniform magnetic field B = (0, 0, b_1)")
    print("="*70)

    # (1) Linear: A(x) = (0, b_1*x, 0) gives B = (0, 0, b_1)
    b_1 = symbols('b_1', real=True)
    A1 = Matrix([0, b_1*x[0], 0])
    B1 = curl(A1, x)

    L1 = m * V.norm() ** 2 / 2 + q * (A1.T * V)[0, 0]

    # Compute equation of motion
    x_t = [Function(x[i].name)(t) for i in range(len(x))]
    x_dot = [diff(xi, t, 1) for xi in x_t]
    x_ddot = [diff(xi, t, 2) for xi in x_t]

    subs_dict = {x[i]: x_t[i] for i in range(len(x))}
    subs_dict.update({v[i]: x_dot[i] for i in range(len(v))})

    dL_x = gradient(L1, x).subs(subs_dict)
    dL_v = gradient(L1, v).subs(subs_dict)

    lhs = diff(dL_v, t)
    rhs = dL_x

    solutions1 = solve(lhs - rhs, x_ddot)
    accel1 = Matrix([solutions1[xi] for xi in x_ddot])

    print("\nMagnetic field B = curl(A):")
    pprint(B1)
    print("\nAcceleration d²x/dt²:")
    pprint(accel1)

    print("\n" + "="*70)
    print("EXAMPLE 2: Nonlinear vector potential A = (-y³, x³, 0)")
    print("Gives nonlinear magnetic field B = (0, 0, 3x² + 3y²)")
    print("="*70)

    # (2) Nonlinear: A(x) = (-y³, x³, 0) gives B = (0, 0, 3(x²+y²))
    A2 = Matrix([-x[1]**3, x[0]**3, 0])
    B2 = curl(A2, x)

    L2 = m * V.norm() ** 2 / 2 + q * (A2.T * V)[0, 0]

    subs_dict = {x[i]: x_t[i] for i in range(len(x))}
    subs_dict.update({v[i]: x_dot[i] for i in range(len(v))})

    dL_x2 = gradient(L2, x).subs(subs_dict)
    dL_v2 = gradient(L2, v).subs(subs_dict)

    lhs2 = diff(dL_v2, t)
    rhs2 = dL_x2

    solutions2 = solve(lhs2 - rhs2, x_ddot)
    accel2 = Matrix([solutions2[xi] for xi in x_ddot])

    print("\nMagnetic field B = curl(A):")
    pprint(B2)
    print("\nAcceleration d²x/dt² (first component):")
    pprint(accel2[0])

    print("\n" + "="*70)
    print("EXAMPLE 3: Uniform magnetic field B = (0, 0, B_z)")
    print("="*70)

    # (3) Uniform B field: A = (-B_z*y/2, B_z*x/2, 0)
    # This gives B = (0, 0, B_z) and leads to circular motion
    B_z = symbols('B_z', real=True)
    A3 = Matrix([-B_z*x[1]/2, B_z*x[0]/2, 0])
    B3 = curl(A3, x)

    L3 = m * V.norm() ** 2 / 2 + q * (A3.T * V)[0, 0]

    subs_dict = {x[i]: x_t[i] for i in range(len(x))}
    subs_dict.update({v[i]: x_dot[i] for i in range(len(v))})

    dL_x3 = gradient(L3, x).subs(subs_dict)
    dL_v3 = gradient(L3, v).subs(subs_dict)

    lhs3 = diff(dL_v3, t)
    rhs3 = dL_x3

    solutions3 = solve(lhs3 - rhs3, x_ddot)
    accel3 = Matrix([solutions3[xi] for xi in x_ddot])

    print("\nMagnetic field B = curl(A):")
    pprint(B3)
    print("\nAcceleration d²x/dt²:")
    pprint(accel3)
    print("\nCyclotron frequency: ω_c = q*B_z/m")
    omega_c = q * B_z / m
    print(f"ω_c = {omega_c}")
    print("\nThe motion is circular in the x-y plane with frequency ω_c")
    print("Solution: x(t) = R*cos(ω_c*t), y(t) = R*sin(ω_c*t), z(t) = v_z*t")
