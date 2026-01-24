from sympy import IndexedBase, symbols, Function, simplify, pprint

if __name__ == "__main__":
    print("=" * 60)
    print("Testing mixed partial derivatives with IndexedBase")
    print("=" * 60)

    x = IndexedBase('x', real=True)
    x_list = [x[i] for i in range(1, 4)]

    # Create a function
    f = Function('f', real=True)(*x_list)

    print(f"f = {f}")
    print()

    # Compute mixed partials
    f_12 = f.diff(x_list[0]).diff(x_list[1])
    f_21 = f.diff(x_list[1]).diff(x_list[0])

    print("Mixed partial ∂²f/∂x[1]∂x[2]:")
    pprint(f_12)
    print()

    print("Mixed partial ∂²f/∂x[2]∂x[1]:")
    pprint(f_21)
    print()

    print(f"Are they equal? {f_12 == f_21}")
    print(f"Difference: {f_12 - f_21}")
    print(f"Simplified difference: {simplify(f_12 - f_21)}")
    print()

    print("=" * 60)
    print("Testing with regular symbols")
    print("=" * 60)

    x2 = symbols('x_1:4', real=True)
    g = Function('g', real=True)(*x2)

    print(f"g = {g}")
    print()

    g_12 = g.diff(x2[0]).diff(x2[1])
    g_21 = g.diff(x2[1]).diff(x2[0])

    print("Mixed partial ∂²g/∂x_1∂x_2:")
    pprint(g_12)
    print()

    print("Mixed partial ∂²g/∂x_2∂x_1:")
    pprint(g_21)
    print()

    print(f"Are they equal? {g_12 == g_21}")
    print(f"Difference: {g_12 - g_21}")
    print(f"Simplified difference: {simplify(g_12 - g_21)}")