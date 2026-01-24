from sympy import zeros, IndexedBase, symbols, pprint, simplify

from sandbox.symbolics.vector_calculus import (curl, divergence, gradient, jacobian, laplacian, poisson,
                                               make_vector_field, make_scalar_field, expr_equal, matrices_equal)

if __name__ == "__main__":
    n_dim = 3

    print("=" * 60)
    print("Testing with IndexedBase (scratch-0.py style)")
    print("=" * 60)

    # Define IndexedBase variables
    x = IndexedBase('x', real=True)
    x_list = [x[i] for i in range(1, n_dim + 1)]

    print(f"x_list = {x_list}")
    print(f"Type of x_list: {type(x_list)}")
    print()

    F = make_vector_field('F', x_list)
    print("F =")
    pprint(F)
    print()

    curl_F = curl(F, x_list)
    print("curl(F) =")
    pprint(curl_F)
    print()

    div_curl_F = divergence(curl_F, x_list)
    print("divergence(curl(F)) =")
    pprint(div_curl_F)
    print()

    simplified = simplify(div_curl_F)
    print("simplified divergence(curl(F)) =")
    pprint(simplified)
    print()

    print(f"Is it zero? {simplified == 0}")
    print(f"expr_equal result: {expr_equal(div_curl_F, 0)}")
    print()

    print("=" * 60)
    print("Testing with symbols (scratch-0a.py style)")
    print("=" * 60)

    x2 = symbols(f'x_1:{n_dim + 1}', real=True)
    print(f"x2 = {x2}")
    print(f"Type of x2: {type(x2)}")
    print()

    F2 = make_vector_field('F2', x2)
    print("F2 =")
    pprint(F2)
    print()

    curl_F2 = curl(F2, x2)
    print("curl(F2) =")
    pprint(curl_F2)
    print()

    div_curl_F2 = divergence(curl_F2, x2)
    print("divergence(curl(F2)) =")
    pprint(div_curl_F2)
    print()

    simplified2 = simplify(div_curl_F2)
    print("simplified divergence(curl(F2)) =")
    pprint(simplified2)
    print()

    print(f"Is it zero? {simplified2 == 0}")
    print(f"expr_equal result: {expr_equal(div_curl_F2, 0)}")