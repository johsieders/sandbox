# testing differential operators
# 25/01/2026
# Johannes Siedersleben

from sympy import zeros, symbols, pprint

from sandbox.math4phys.diff_ops import (curl, divergence, gradient, hessian, jacobian, laplacian,
                                        make_vector_field, make_scalar_field, expr_equal, matrices_equal)


def test_jacobian():
    n_dim = 3
    x = symbols(f'x_1:{n_dim + 1}', real=True)

    F = make_vector_field('F', x, n_dim + 1)

    J = jacobian(F)
    assert J.shape == (n_dim + 1, n_dim)


def test_chain_rule():
    m_dim = 4
    n_dim = 5
    p_dim = 6

    x = symbols(f'x_1:{m_dim+1}', real=True)
    y = symbols(f'y_1:{n_dim+1}', real=True)
    F = make_vector_field('F', y, p_dim)
    G = make_vector_field('G', x, n_dim)

    subs_y_G = {y[j]: G[j] for j in range(len(y))}
    FoG = F.subs(subs_y_G) 
    JFoG = jacobian(F).subs(subs_y_G)

    # J(F o G) = (JF o G) * JG
    assert matrices_equal(jacobian(FoG), JFoG * jacobian(G))
    
    
def test_diff_ops():
    n_dim = 5

    x = symbols(f'x_1:{n_dim + 1}', real=True)
    y = symbols(f'x_1:{n_dim + 1}', real=True)

    f = make_scalar_field('f', x)
    g = make_scalar_field('g', x)

    F = make_vector_field('F', x, n_dim)
    G = make_vector_field('G', y, n_dim)
    H = make_vector_field('G', x, 1)

    assert matrices_equal(gradient(H[0]), jacobian(H).T)
    
    assert expr_equal(divergence(F * g), divergence(F) * g + (F.T * gradient(g))[0, 0])
    assert expr_equal(divergence(F * g), divergence(F) * g + (gradient(g).T * F)[0, 0])

    assert matrices_equal(gradient(f * g), gradient(f) * g + f * gradient(g))
    assert matrices_equal(gradient(F.T * G), jacobian(F).T * G + jacobian(G).T * F)
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
    assert matrices_equal(curl(F.cross(G)), 
                          divergence(G) * F - divergence(F) * G + jacobian(F) * G - jacobian(G) * F)  


def test_cross():
    n_dim = 3
    x = symbols(f'x_1:{n_dim + 1}', real=True)

    F = make_vector_field('F', x)
    G = make_vector_field('G', x)
    H = make_vector_field('H', x)

    assert matrices_equal(F.T * G.cross(H), H.T * F.cross(G))
    assert matrices_equal(F.cross(G.cross(H)), (F.T * H)[0, 0] * G - (F.T * G)[0,0] * H) 
    
