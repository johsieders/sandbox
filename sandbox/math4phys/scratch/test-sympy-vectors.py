from sympy import Matrix, symbols, pprint
from sympy.vector import CoordSys3D

if __name__ == "__main__":
    N = CoordSys3D('N')

    print("=" * 60)
    print("Question 1: Is N.i.outer(N.j) a 3x3 matrix?")
    print("=" * 60)

    dyadic = N.i.outer(N.j)
    print(f"N.i.outer(N.j) = {dyadic}")
    print(f"Type: {type(dyadic)}")
    print(f"Is it a Dyadic? {type(dyadic).__name__}")
    print()

    # A Dyadic is NOT a matrix, it's a tensor product representation
    # But it can be converted to a matrix
    print("Converting to matrix:")
    mat = dyadic.to_matrix(N)
    print("dyadic.to_matrix(N) =")
    pprint(mat)
    print(f"Shape: {mat.shape}")
    print()

    # Let's see a few more outer products
    print("Other outer products:")
    print("N.i.outer(N.i):")
    pprint(N.i.outer(N.i).to_matrix(N))
    print()

    print("N.j.outer(N.k):")
    pprint(N.j.outer(N.k).to_matrix(N))
    print()

    print("=" * 60)
    print("Question 2: Bridge between (i,j,k) and usual vectors/matrices")
    print("=" * 60)

    # From (i, j, k) world to Matrix
    v = 2 * N.i + 3 * N.j + 5 * N.k
    print(f"SymPy vector: v = {v}")
    print()

    # Convert to column vector
    v_matrix = Matrix([v.dot(N.i), v.dot(N.j), v.dot(N.k)])
    print("As Matrix (column vector):")
    pprint(v_matrix)
    print()

    # Alternative: use to_matrix
    print("Using v.to_matrix(N):")
    pprint(v.to_matrix(N))
    print()

    # From Matrix to (i, j, k) world
    m = Matrix([7, 11, 13])
    v_from_matrix = m[0] * N.i + m[1] * N.j + m[2] * N.k
    print("From Matrix back to vector:")
    print(f"Matrix = {m.T}")
    print(f"Vector = {v_from_matrix}")
    print()

    print("=" * 60)
    print("Question 3: Extending beyond 3 dimensions")
    print("=" * 60)

    print("SymPy's vector module is explicitly 3D only.")
    print("CoordSys3D is hardcoded for 3 dimensions.")
    print()

    print("For higher dimensions, use:")
    print("1. Regular SymPy Matrix operations")
    print("2. SymPy's tensor module (sympy.tensor)")
    print()

    print("Example with 4D vectors using Matrix:")
    x = symbols('x_1:5')  # x_1, x_2, x_3, x_4
    v1 = Matrix(x)
    v2 = Matrix([1, 2, 3, 4])

    print("v1 (4D) =")
    pprint(v1)
    print()

    print("v2 (4D) =")
    pprint(v2)
    print()

    print("Dot product: v1.T * v2 =")
    pprint((v1.T * v2)[0])
    print()

    print("Outer product: v1 * v2.T =")
    pprint(v1 * v2.T)
    print()

    print("For tensor calculus in arbitrary dimensions,")
    print("see: sympy.tensor.tensor module")
    print("Example: TensorIndexType, tensor_indices, TensorHead")
