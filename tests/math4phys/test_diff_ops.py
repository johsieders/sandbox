# testing differential operators
# 25/01/2026
# Johannes Siedersleben

from sympy import zeros, symbols

from sandbox.math4phys.diff_ops import (curl, divergence, gradient, hessian, jacobian, laplacian,
                                        make_vector_field, make_scalar_field, expr_equal, matrices_equal)


def test_jacobian():
    n_dim = 3
    x = symbols(f'x_1:{n_dim + 1}', real=True)

    F = make_vector_field('F', x, n_dim + 1)

    J = jacobian(F)

    # print()
    # pprint(J)
    # pprint(F.diff(x[0]).T)


def test_diff_ops():
    n_dim = 5

    x = symbols(f'x_1:{n_dim + 1}', real=True)

    f = make_scalar_field('f', x)
    g = make_scalar_field('g', x)

    F = make_vector_field('F', x, n_dim)
    G = make_vector_field('G', x, n_dim)

    assert expr_equal(divergence(F * g), divergence(F) * g + (F.T * gradient(g))[0, 0])
    assert expr_equal(divergence(F * g), divergence(F) * g + (gradient(g).T * F)[0, 0])

    assert matrices_equal(gradient(f * g), gradient(f) * g + f * gradient(g))
    assert matrices_equal(gradient(F.T * G), jacobian(F) * G + jacobian(G) * F)
    assert matrices_equal(hessian(f), jacobian(gradient(f)))
    assert matrices_equal(hessian(f * g),
                          (hessian(f) * g +
                           gradient(f) * gradient(g).T +
                           gradient(g) * gradient(f).T +
                           hessian(g) * f))


def test_curl():
    n_dim = 3
    x = symbols(f'x_1:{n_dim + 1}', real=True)

    f = make_scalar_field('f', x)

    F = make_vector_field('F', x)
    G = make_vector_field('G', x)

    assert expr_equal(divergence(curl(F)), 0)
    assert expr_equal(divergence(F.cross(G)), (G.T * curl(F) - F.T * curl(G))[0, 0])
    assert matrices_equal(curl(gradient(f)), zeros(3, 1))
    assert matrices_equal(curl(curl(F)), gradient(divergence(F)) - laplacian(F))
