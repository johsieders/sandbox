from sympy import zeros, symbols

from sandbox.symbolics.vector_calculus import (curl, divergence, gradient, hessian, jacobian, laplacian, poisson,
                                               make_vector_field, make_scalar_field, expr_equal, matrices_equal)

if __name__ == "__main__":
    n_dim = 3

    x = symbols(f'x_1:{n_dim + 1}', real=True)
    p = symbols(f'p_1:{n_dim + 1}', real=True)
    v = symbols(f'v_1:{n_dim + 1}', real=True)
    xp = x + p

    f = make_scalar_field('f', x)
    g = make_scalar_field('g', x)

    F = make_vector_field('F', x)
    G = make_vector_field('G', x)

    A = make_scalar_field('A', xp)
    B = make_scalar_field('B', xp)
    C = make_scalar_field('C', xp)

    assert expr_equal(divergence(F * g, x), divergence(F, x) * g + (F.T * gradient(g, x))[0, 0])
    assert expr_equal(divergence(curl(F, x), x), 0)
    assert expr_equal(divergence(F * g, x), divergence(F, x) * g + (gradient(g, x).T * F)[0, 0])
    assert expr_equal(divergence(F.cross(G), x), (G.T * curl(F, x) - F.T * curl(G, x))[0, 0])

    assert matrices_equal(gradient(f * g, x), gradient(f, x) * g + f * gradient(g, x))
    assert matrices_equal(curl(gradient(f, x), x), zeros(3, 1))
    assert matrices_equal(curl(curl(F, x), x), gradient(divergence(F, x), x) - laplacian(F, x))
    assert matrices_equal(gradient(F.T * G, x), jacobian(F, x) * G + jacobian(G, x) * F)

    assert expr_equal(poisson(A, B, x, p) + poisson(B, A, x, p), 0)
    assert expr_equal(poisson(A, poisson(B, C, x, p), x, p) +
                      poisson(B, poisson(C, A, x, p), x, p) +
                      poisson(C, poisson(A, B, x, p), x, p), 0)
    
    h1 = hessian(f * g, x)
    h2 = (hessian(f, x) * g + 
          gradient(f, x) * gradient(g, x).T + 
          gradient(g, x) * gradient(f, x).T + 
          hessian(g, x) * f) 
    
