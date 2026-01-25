from sympy import zeros, IndexedBase

from sandbox.math4phys.vector_calculus import (curl, divergence, gradient, jacobian, laplacian, poisson,
                                               make_vector_field, make_scalar_field, expr_equal, matrices_equal)

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

    f = make_scalar_field('f', x_list)
    g = make_scalar_field('g', x_list)

    F = make_vector_field('F', x_list)
    G = make_vector_field('G', x_list)

    A = make_scalar_field('A', xp_list)
    B = make_scalar_field('B', xp_list)
    C = make_scalar_field('C', xp_list)

    assert expr_equal(divergence(F * g, x_list), divergence(F, x_list) * g + (F.T * gradient(g, x_list))[0, 0])
    assert expr_equal(divergence(curl(F, x_list), x_list), 0)
    assert expr_equal(divergence(F * g, x_list), divergence(F, x_list) * g + (gradient(g, x_list).T * F)[0, 0])
    assert expr_equal(divergence(F.cross(G), x_list), (G.T * curl(F, x_list) - F.T * curl(G, x_list))[0, 0])

    assert matrices_equal(gradient(f * g, x_list), gradient(f, x_list) * g + f * gradient(g, x_list))
    assert matrices_equal(curl(gradient(f, x_list), x_list), zeros(3, 1))
    assert matrices_equal(curl(curl(F, x_list), x_list), gradient(divergence(F, x_list), x_list) - laplacian(F, x_list))
    assert matrices_equal(gradient(F.T * G, x_list), jacobian(F, x_list) * G + jacobian(G, x_list) * F)

    assert expr_equal(poisson(A, B, x_list, p_list) + poisson(B, A, x_list, p_list), 0)
    assert expr_equal(poisson(A, poisson(B, C, x_list, p_list), x_list, p_list) +
                      poisson(B, poisson(C, A, x_list, p_list), x_list, p_list) +
                      poisson(C, poisson(A, B, x_list, p_list), x_list, p_list), 0)
