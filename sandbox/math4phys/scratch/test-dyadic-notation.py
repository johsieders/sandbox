from sympy import pprint
from sympy.vector import CoordSys3D

if __name__ == "__main__":
    N = CoordSys3D('N')

    print("=" * 60)
    print("Clarifying SymPy's (x|y) notation")
    print("=" * 60)
    print()

    print("The notation (x|y) in SymPy represents a DYADIC,")
    print("which is the outer/tensor product x ⊗ y")
    print()

    print("=" * 60)
    print("Example: N.i.outer(N.j)")
    print("=" * 60)

    dyadic = N.i.outer(N.j)
    print(f"SymPy notation: {dyadic}")
    print(f"Math notation:  N.i ⊗ N.j")
    print()

    print("As a matrix:")
    mat = dyadic.to_matrix(N)
    pprint(mat)
    print()

    print("This is the outer product: i ⊗ j")
    print()

    print("=" * 60)
    print("Comparison with inner product")
    print("=" * 60)

    v = 2 * N.i + 3 * N.j + 5 * N.k
    w = 7 * N.i + 11 * N.j + 13 * N.k

    print(f"v = {v}")
    print(f"w = {w}")
    print()

    # Inner product (dot product)
    inner = v.dot(w)
    print(f"Inner product ⟨v,w⟩ = v.dot(w) = {inner}")
    print(f"Result: scalar")
    print()

    # Outer product (tensor product)
    outer = v.outer(w)
    print(f"Outer product v ⊗ w = v.outer(w) =")
    print(f"SymPy notation: {outer}")
    print()
    print("As a 3×3 matrix:")
    pprint(outer.to_matrix(N))
    print()

    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    print("SymPy notation | Math notation | Type          | Result")
    print("---------------|---------------|---------------|------------------")
    print("v.dot(w)       | ⟨v,w⟩ or v·w  | Inner product | Scalar")
    print("v.outer(w)     | v ⊗ w         | Outer product | Dyadic (3×3 matrix)")
    print("(v|w)          | v ⊗ w         | Display form  | Same as outer")
    print()
    print("So YES: (x|y) is the outer/tensor product x ⊗ y")
