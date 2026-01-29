from sympy import diff, symbols, sin, cos, Matrix, Function, Derivative, Subs
from sympy.abc import t, x

if __name__ == "__main__":
    n_dim = 3

    # x_1, x_2, x_3 = x = symbols(f'x_1:{n_dim + 1}', real=True)
    p_1, p_2, p_3 = p = symbols(f'p_1:{n_dim + 1}', real=True)
    # v_1, v_2, v_3 = v = symbols(f'v_1:{n_dim + 1}', real=True)

    P = Matrix(p)
    Q = Subs(P, (p_1, p_2, p_3), (1, 2, 3)).doit()

    # x_1, x_2, x_3 = x = [Function(f'x_1:{n_dim + 1}', real=True)(t) for i in range(n_dim)]
    # v_1, v_2, v_3 = v = [Function(f'v_1:{n_dim + 1}', real=True)(t) for i in range(n_dim)]

    f = Function('f', real=True)
    d0 = f(x).diff(x).subs(x, 0).subs(f, sin).doit()

    d1 = diff(cos(sin(x)), x)

    g = f(sin(x), cos(x), x ** 2)
    d2 = g.diff(x).doit()

    Subs(Derivative(f(sin(x), cos(x), t), t), t, x ** 2)

    # (2 * x  * Subs(Derivative(f(sin(x), cos(x), t), t), t, x ** 2) - 
    #  sin(x) * Subs(
    #     Derivative(f(sin(x), _xi_2, x ** 2), _xi_2), _xi_2, cos(x)) + cos(x) * Subs(
    #     Derivative(f(_xi_1, cos(x), x ** 2), _xi_1), _xi_1, sin(x)))

    r, t = symbols('r t')  # r (radius), t (angle theta)
    f = symbols('f', cls=Function)
    x = r * cos(t)
    y = r * sin(t)
    g = f(x, y)

    d1 = Derivative(g, r, 1)
    d2 = g.diff(r, 1)

    d11 = d1.doit()
    d22 = d2.doit()

    pass
    # m = symbols('m', positive=True)
    # 
    # 
    # X = Matrix(x)
    # 
    # V = Matrix(v)
    # 
    # # P = Matrix(p)
    # 
    # L = m * (V.T * V)[0, 0] / 2 - X.norm() ** 2
    # 
    # F = L.diff(x)
    # 
    # P1 = L.diff(t)
    # P2 = gradient(L, v)
    # 
    # P = P1.T * P2
    # 
    # F = L.diff(x)
    # 
    # pass
    # # x_1, x_2, x_3 = x = make_vector_field('x', [t], 3)
    # 
    # 
    # 
    # f = make_scalar_field('f', x)
    # g = make_scalar_field('g', x)
    # h = make_scalar_field('h', [r, s, t])
    # 
    # val1 = evaluate(f + sin(x_1), x_1=1, x_2=1)
    # val2 = evaluate(h + sin(r), r=1, s=1)
    # pprint(val1)
    # pprint(val2)
    # 
    # print('\n', latex(val1))
    # print('\n', latex(val2))
    # 
    # # F = make_vector_field('F', x)
    # # G = make_vector_field('G', x)
    # 
    # A = make_scalar_field('A', x + p)
    # B = make_scalar_field('B', x + p)
    # C = make_scalar_field('C', x + p)
    # 
    # 
    # 
    # g = gradient(x_1, x)
    # pprint(g)
