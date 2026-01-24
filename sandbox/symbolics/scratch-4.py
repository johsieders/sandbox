from sympy import symbols, sin, Matrix, pprint, IndexedBase
from sympy.abc import r, s, t

from sandbox.symbolics.vector_calculus import (divergence, gradient, make_vector_field, make_scalar_field, evaluate)

if __name__ == "__main__":
    n_dim = 3

    # Define IndexedBase variables
    x = IndexedBase('x', real=True)
    p = IndexedBase('p', real=True)
    v = IndexedBase('v', real=True)

    # Create lists of indexed elements for use with vector calculus functions
    # Using 1-based indexing to match mathematical convention
    x_list = [x[i] for i in range(1, n_dim + 1)]  # [x[1], x[2], x[3]]
    p_list = [p[i] for i in range(1, n_dim + 1)]  # [p[1], p[2], p[3]]
    v_list = [v[i] for i in range(1, n_dim + 1)]  # [v[1], v[2], v[3]]

    xp_list = x_list + p_list

    # Create scalar fields
    f = make_scalar_field('f', x_list)
    fi = make_scalar_field('fi', x_list)
    g = make_scalar_field('g', x_list)
    h = make_scalar_field('h', [r, s, t])

    # Test evaluate function with IndexedBase
    print("Testing evaluate with IndexedBase:")
    print("=" * 60)

    # For IndexedBase, we build a substitution dict and pass it as kwargs
    # The evaluate() function will match the symbol names correctly
    subs_dict_1 = {str(x[1]): 1, str(x[2]): 1}
    subs_dict_2 = {str(x[1]): 1, str(x[2]): 1}

    val1 = evaluate(f + sin(x[1]), **subs_dict_1)
    val2 = evaluate(fi + sin(x[1]), **subs_dict_2)
    val3 = evaluate(h + sin(r), r=1, s=1)

    print("f + sin(x[1]) with x[1]=1, x[2]=1:")
    pprint(val1)
    print()

    print("fi + sin(x[1]) with x[1]=1, x[2]=1:")
    pprint(val2)
    print()

    print("h + sin(r) with r=1, s=1:")
    pprint(val3)
    print()

    # Create vector fields
    F = make_vector_field('F', x_list)
    G = make_vector_field('G', x_list)

    # Scalar fields depending on position and momentum
    A = make_scalar_field('A', xp_list)
    B = make_scalar_field('B', xp_list)
    C = make_scalar_field('C', xp_list)

    print("Lagrangian mechanics:")
    print("=" * 60)

    # Lagrangian (kinetic - potential)
    m = symbols('m', positive=True)
    V = Matrix(v_list)
    X = Matrix(x_list)
    P = Matrix(p_list)
    L = m * (V.T * V)[0, 0] / 2 - X.norm() ** 2

    print("∂L/∂v (momentum):")
    pprint(gradient(L, v_list))
    print()

    print("∂L/∂x (force):")
    pprint(gradient(L, x_list))
    print()

    print("Hamiltonian mechanics:")
    print("=" * 60)

    # Hamiltonian
    H = (P.T * P)[0, 0] / (2 * m) + X.norm() ** 2

    print("Hamiltonian H:")
    pprint(H)
    print()

    # Poisson bracket example (commented out in original)
    # print("Poisson bracket {A, H}:")
    # pprint(poisson(A, H, x_list, p_list))
    # print()

    print("Additional vector calculus operations:")
    print("=" * 60)

    # Some additional calculations
    X2 = (X.T * X)[0, 0]
    gx = gradient(X2, x_list)
    dx = divergence(X, x_list)

    print("Gradient of X·X:")
    pprint(gx)
    print()

    print("Divergence of X:")
    pprint(dx)
    print()
