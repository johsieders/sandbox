from sympy import sin, cos, trigsimp, diff, pprint
from sympy.abc import a, b, c
from sympy.vector import CoordSys3D, Dyadic, Vector

if __name__ == "__main__":
    N = CoordSys3D('N')

    print(N.i)
    print(N.j)
    print(N.k)

    v = N.i + N.j + N.k
    print(v)

    w = N.i - N.j - N.k
    print(w)
    print(v.cross(w))
    print(v.dot(w))

    print()
    v = (a * b + a * c + b ** 2 + b * c) * N.i + N.j
    print(v)
    print(v.factor())
    print()

    v = (sin(a) ** 2 + cos(a) ** 2) * N.i - (2 * cos(b) ** 2 - 1) * N.k
    print(v)
    trigsimp(v)
    print(trigsimp(v))
    v.simplify()
    print(v.simplify())
    d = diff(v, b)
    print(d)

    print(N.origin)

    from sympy.abc import a, b, c

    print(N.i.outer(N.j))
    print(Dyadic.zero)


    def f(a, b, c) -> Vector:
        return a * N.i + b * N.j + c * N.k


    def g(b) -> Vector:
        return -b * N.j


    P = N.origin.locate_new('P', f(a, b, c))
    Q = P.locate_new('Q', g(b))

    A = CoordSys3D('A')
    B = A.orient_new_axis('B', a, A.k)
    pprint(B.rotation_matrix(A))
    pprint(B.rotation_matrix(B))

    print()
    A = CoordSys3D('A', transformation='spherical')
    B = CoordSys3D('B', transformation=lambda x, y, z: (x * sin(y), x * cos(y), z))
    pprint(A)
    pprint(B)
