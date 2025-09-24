# py4alg/tests/test_ec.py


from sandbox.py4alg.mapper.m_ec import ECPoint


def test_add_mul():
    P = ECPoint(a=2, b=3, p=97, x=3, y=6)
    Q = ECPoint(a=2, b=3, p=97, x=80, y=10)
    R = P + Q
    S = 5 * P

    print()
    print(P)
    print(Q)
    print(R)
    print(S)


def test_gen():
    print()
    for pt in ECPoint.gen_points(a=2, b=2, p=17):
        print(pt)
