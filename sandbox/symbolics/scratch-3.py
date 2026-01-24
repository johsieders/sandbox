from sympy import symbols, IndexedBase
from sympy.abc import r, s, t

from sandbox.symbolics.vector_calculus import (make_scalar_field)

if __name__ == "__main__":
    n_dim = 3

    # x = symbols(f'x_1:{n_dim + 1}', real=True)
    # p = symbols(f'p_1:{n_dim + 1}', real=True)
    # v = symbols(f'v_1:{n_dim + 1}', real=True)

    z = IndexedBase('z', real=True)

    x_1, x_2, x_3 = symbols('x_1, x_2, x_3', real=True)
    p_1, p_2, p_3 = symbols('p_1, p_2, p_3', real=True)
    v_1, v_2, v_3 = symbols('v1, v_2, v_3', real=True)
    x = [x_1, x_2, x_3]
    p = [p_1, p_2, p_3]
    v = [v_1, v_2, v_3]

    xp = x + p

    # f = make_scalar_field('f', z[1:4])

    h = make_scalar_field('h', [r, s, t])
    # print('\n', f.free_symbols)
    print('\n', h.free_symbols)
    # val1 = evaluate(f + sin(z[1]), z[1]=1, z[2]=1)
    # val2 = evaluate(fi + sin(x_1), x_1=1, x_2=1)
    # val3 = evaluate(h + sin(r), r=1, s=1)
    # pprint(val1)
    # pprint(val2)
    # pprint(val3)
