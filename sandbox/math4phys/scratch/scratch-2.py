from sympy import symbols, sin, Matrix, pprint, latex
from sympy.abc import r, s, t

from sandbox.math4phys.diff_ops import (divergence, gradient, make_vector_field, make_scalar_field, evaluate)

if __name__ == "__main__":
    n_dim = 3

    x_1, x_2, x_3 = x = symbols(f'x_1:{n_dim + 1}', real=True)
    p_1, p_2, p_3 = p = symbols(f'p_1:{n_dim + 1}', real=True)
    v_1, v_2, v_3 = v = symbols(f'v_1:{n_dim + 1}', real=True)

    # x_1, x_2, x_3 = x = make_vector_field('x', [t], 3)

    # v = diff(x, t)

    f = make_scalar_field('f', x)
    g = make_scalar_field('g', x)
    h = make_scalar_field('h', [r, s, t])

    val1 = evaluate(f + sin(x_1), x_1=1, x_2=1)
    val2 = evaluate(h + sin(r), r=1, s=1)
    pprint(val1)
    pprint(val2)

    print('\n', latex(val1))
    print('\n', latex(val2))

    F = make_vector_field('F', x)
    G = make_vector_field('G', x)

    A = make_scalar_field('A', x + p)
    B = make_scalar_field('B', x + p)
    C = make_scalar_field('C', x + p)

    # Lagrangian (kinetic - potential)                                                                                                                                                                                                                        
    m = symbols('m', positive=True)
    V = Matrix(v)
    X = Matrix(x)
    P = Matrix(p)
    L = m * (V.T * V)[0, 0] / 2 - X.norm() ** 2

    pprint(gradient(L, v))
    pprint(gradient(L, x))

    # Hamiltonian                                                                                                                                                                                                                                             
    H = (P.T * P)[0, 0] / (2 * m) + X.norm() ** 2

    # pprint(poisson(A, H, x, p))

    X2 = X.T * X
    gx = gradient(X2, x)
    dx = divergence(X, x)

    g = gradient(x_1, x)
    pprint(g)
