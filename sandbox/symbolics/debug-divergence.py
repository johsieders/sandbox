from sympy import IndexedBase, symbols, pprint, Matrix

if __name__ == "__main__":
    n_dim = 3

    print("=" * 60)
    print("Testing divergence implementation")
    print("=" * 60)

    # IndexedBase
    x = IndexedBase('x', real=True)
    x_list = [x[i] for i in range(1, n_dim + 1)]

    print("With IndexedBase list:")
    print(f"x_list = {x_list}")
    print(f"x_list[0] = {x_list[0]}, type = {type(x_list[0])}")
    print(f"x_list[1] = {x_list[1]}, type = {type(x_list[1])}")
    print(f"x_list[2] = {x_list[2]}, type = {type(x_list[2])}")
    print()

    # Create a simple matrix
    F_list = Matrix(x_list)
    print("F =")
    pprint(F_list)
    print()

    # Check what divergence does
    print("Computing divergence manually:")
    from sandbox.symbolics.vector_calculus import divergence
    div_result = divergence(F_list, x_list)
    print("divergence(F, x_list) =")
    pprint(div_result)
    print()

    # Now with symbols tuple
    x2 = symbols(f'x_1:{n_dim + 1}', real=True)

    print("=" * 60)
    print("With symbols tuple:")
    print(f"x2 = {x2}")
    print(f"x2[0] = {x2[0]}, type = {type(x2[0])}")
    print(f"x2[1] = {x2[1]}, type = {type(x2[1])}")
    print(f"x2[2] = {x2[2]}, type = {type(x2[2])}")
    print()

    F2 = Matrix(x2)
    print("F2 =")
    pprint(F2)
    print()

    div_result2 = divergence(F2, x2)
    print("divergence(F2, x2) =")
    pprint(div_result2)
    print()

    print("=" * 60)
    print("The divergence function implementation:")
    print("=" * 60)
    print("def divergence(F: Matrix, args: List[Symbol]) -> Expr:")
    print("    return sum(F[i].diff(args[i]) for i in range(len(args)))")
    print()
    print("The problem: F[i].diff(args[i])")
    print()

    # Let's check how differentiation works
    print("Differentiation test:")
    print(f"F_list[0] = {F_list[0]}")
    print(f"x_list[0] = {x_list[0]}")
    print(f"F_list[0].diff(x_list[0]) = {F_list[0].diff(x_list[0])}")
    print()
    print(f"F2[0] = {F2[0]}")
    print(f"x2[0] = {x2[0]}")
    print(f"F2[0].diff(x2[0]) = {F2[0].diff(x2[0])}")