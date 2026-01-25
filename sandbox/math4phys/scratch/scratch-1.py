from sympy import Function, Matrix
from sympy.abc import x, y, z, u, v, w

if __name__ == "__main__":
    f = Function('f', real=True)(x, y, z)
    g = Function('g', real=True)(x, y, z)
    p = Function('p', real=True)(x, y, z)
    q = Function('q', real=True)(x, y, z)
    F = Matrix([f, g])
    G = Matrix([[f, g], [p, q]])

    df = diff(f, x)
    print('\n', df)

    H = G.copy()
    K = G.copy()
    G.col_op(0, lambda f, i: f.diff(x))
    H.row_op(0, lambda f, i: f.diff(x))
    K = K.applyfunc(lambda f: f.diff(x))
    print('\n', G)
    print('\n', H)
    print('\n', K)

    c = G.cols
    r = G.rows
    s = G.shape
    H = G.T
    print('\n', H)

    m1 = Matrix([x, y, z])
    m2 = Matrix([u, v, w])
    m3 = m1.cross(m2)
    print('\n', m3)

    print('\n', G.det())
    print('\n', f.args)
    print('\n', f)
    print('\n', repr(f))

    partial_F = diff(F, x)
    partial_G = diff(G, x)
    print('\n', partial_F)
    print('\n', partial_G)
    print('\n')
#     
#     a = f + g
#     b = f * g
#     c = f / g
#     d = f + sin(x) + cos(y) + tan(z)
#     
#     for u in [a, b, c, d]:
#         dx_u = diff(u)
#         grad_u = gradient(u)
#         print('\n', dx_u)
#         print('\n', grad_u)
#     
#     
#     h = f / g
#     
#     d = f + h.diff(x) + sin(x)
# 
# 
# from sympy.physics.vector import ReferenceFrame
# from sympy.physics.vector import gradient
# 
# R = ReferenceFrame('R')
# s1 = R[0]*R[1]*R[2]
# g1 = gradient(s1, R)
# s2 = 5*R[0]**2*R[2]
# g2 = gradient(s2, R)
# pass
