"""
Quick demonstration of symbolic vector calculus engine.

Run this to see the engine in action verifying fundamental vector calculus identities.
"""

from sympy import simplify

from math4phys.archive.vector_calculus_1 import (
    make_coords, ScalarField, make_vector_field,
    gradient, divergence, curl, laplacian,
    curl_of_gradient_is_zero,
    divergence_of_curl_is_zero,
    laplacian_is_div_grad
)


def demo_basic_operations():
    """Demonstrate basic scalar and vector field operations."""
    print("=" * 70)
    print("DEMO: Basic Operations")
    print("=" * 70)
    print()

    # Create 3D coordinates
    coords = make_coords('x y z')
    x, y, z = coords
    print("Created coordinates: x, y, z")
    print()

    # Create scalar field
    f = ScalarField('f', coords)
    print(f"Scalar field: f(x, y, z) = {f.func}")
    print()

    # Gradient
    grad_f = gradient(f)
    print(f"Gradient: ∇f = {grad_f.components.T}")
    print()

    # Laplacian
    lap_f = laplacian(f)
    print(f"Laplacian: ∇²f = {lap_f}")
    print()

    # Create vector field
    F = make_vector_field('F', coords)
    print(f"Vector field: F = (F₁(x,y,z), F₂(x,y,z), F₃(x,y,z))")
    print()

    # Divergence
    div_F = divergence(F)
    print(f"Divergence: ∇·F = {div_F}")
    print()

    # Curl
    curl_F = curl(F)
    print(f"Curl: ∇×F = {curl_F.components.T}")
    print()


def demo_fundamental_identities():
    """Verify the three fundamental vector calculus identities."""
    print("=" * 70)
    print("DEMO: Fundamental Vector Calculus Identities")
    print("=" * 70)
    print()

    coords = make_coords('x y z')

    # Identity 1: ∇×(∇f) = 0
    print("Identity 1: Curl of Gradient")
    print("-" * 70)
    f = ScalarField('f', coords)

    grad_f = gradient(f)
    curl_grad_f = curl(grad_f)

    print(f"Given: f(x,y,z)")
    print(f"Compute: ∇×(∇f)")
    print(f"Result: {curl_grad_f.components.T}")
    print(f"Simplified: {curl_grad_f.simplify().components.T}")

    is_zero = curl_of_gradient_is_zero(f)
    print(f"Is zero? {is_zero} ✓")
    print()

    # Identity 2: ∇·(∇×F) = 0
    print("Identity 2: Divergence of Curl")
    print("-" * 70)
    F = make_vector_field('F', coords)

    curl_F = curl(F)
    div_curl_F = divergence(curl_F)

    print(f"Given: F = (F₁, F₂, F₃)")
    print(f"Compute: ∇·(∇×F)")
    print(f"Result (before simplification): {div_curl_F}")
    print(f"Simplified: {simplify(div_curl_F)}")

    is_zero = divergence_of_curl_is_zero(F)
    print(f"Is zero? {is_zero} ✓")
    print()

    # Identity 3: ∇²f = ∇·(∇f)
    print("Identity 3: Laplacian = Divergence of Gradient")
    print("-" * 70)
    f = ScalarField('f', coords)

    lap_f = laplacian(f)
    grad_f = gradient(f)
    div_grad_f = divergence(grad_f)

    print(f"Given: f(x,y,z)")
    print(f"∇²f = {lap_f}")
    print(f"∇·(∇f) = {div_grad_f}")
    print(f"Difference: {simplify(lap_f - div_grad_f)}")

    is_equal = laplacian_is_div_grad(f)
    print(f"Are equal? {is_equal} ✓")
    print()


def demo_product_rules():
    """Demonstrate product rules for divergence and curl."""
    print("=" * 70)
    print("DEMO: Product Rules")
    print("=" * 70)
    print()

    coords = make_coords('x y z')

    # Product rule for divergence: ∇·(fF) = f(∇·F) + F·(∇f)
    print("Product Rule for Divergence: ∇·(fF) = f(∇·F) + F·(∇f)")
    print("-" * 70)

    f = ScalarField('f', coords)
    F = make_vector_field('F', coords)

    # Left side
    fF = f.func * F
    div_fF = divergence(fF)

    # Right side
    div_F = divergence(F)
    grad_f = gradient(f)
    right_side = f.func * div_F + F.dot(grad_f)

    difference = simplify(div_fF - right_side)

    print(f"Left side: ∇·(fF)")
    print(f"Right side: f(∇·F) + F·(∇f)")
    print(f"Difference after simplification: {difference}")
    print(f"Identity verified? {difference == 0} ✓")
    print()

    # Product rule for curl: ∇×(fF) = f(∇×F) + (∇f)×F
    print("Product Rule for Curl: ∇×(fF) = f(∇×F) + (∇f)×F")
    print("-" * 70)

    # Left side
    curl_fF = curl(fF)

    # Right side
    curl_F = curl(F)
    right_side_curl = f.func * curl_F + grad_f.cross(F)

    print(f"Left side: ∇×(fF)")
    print(f"Right side: f(∇×F) + (∇f)×F")

    all_equal = True
    for i in range(3):
        diff = simplify(curl_fF[i] - right_side_curl[i])
        if diff != 0:
            all_equal = False
        print(f"  Component {i}: difference = {diff}")

    print(f"Identity verified? {all_equal} ✓")
    print()


def demo_vector_operations():
    """Demonstrate vector field arithmetic."""
    print("=" * 70)
    print("DEMO: Vector Field Operations")
    print("=" * 70)
    print()

    coords = make_coords('x y z')
    E = make_vector_field('E', coords)
    B = make_vector_field('B', coords)

    print("Electric field: E = (E₁, E₂, E₃)")
    print("Magnetic field: B = (B₁, B₂, B₃)")
    print()

    # Addition
    print("Addition: E + B")
    H = E + B
    print(f"Result: {H}")
    print()

    # Scalar multiplication
    print("Scalar multiplication: 2·E")
    two_E = 2 * E
    print(f"Result: {two_E}")
    print()

    # Dot product
    print("Dot product: E·B")
    dot = E.dot(B)
    print(f"Result: {dot}")
    print()

    # Cross product (Poynting vector)
    print("Cross product: E×B (Poynting vector)")
    S = E.cross(B)
    S.name = 'S'
    print(f"Result: {S}")
    print(f"Components: {S.components.T}")
    print()


def demo_dimensions():
    """Demonstrate working in different dimensions."""
    print("=" * 70)
    print("DEMO: Different Dimensions")
    print("=" * 70)
    print()

    # 2D
    print("2D Example (Complex Analysis)")
    print("-" * 70)
    coords_2d = make_coords('x y')
    f_2d = ScalarField('f', coords_2d)
    grad_f_2d = gradient(f_2d)
    print(f"Scalar field: f(x, y)")
    print(f"Gradient: ∇f = {grad_f_2d.components.T}")
    print()

    # 4D (spacetime)
    print("4D Example (Spacetime)")
    print("-" * 70)
    coords_4d = make_coords('t x y z')
    phi = ScalarField('phi', coords_4d)
    grad_phi = gradient(phi)
    print(f"Scalar field: φ(t, x, y, z)")
    print(f"Gradient: ∇φ = {grad_phi.components.T}")
    print(f"Dimensions: {phi.dim}D → {grad_phi.output_dim}D")
    print()


if __name__ == "__main__":
    # Run all demos
    demo_basic_operations()
    print("\n")

    demo_fundamental_identities()
    print("\n")

    demo_product_rules()
    print("\n")

    demo_vector_operations()
    print("\n")

    demo_dimensions()

    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. See sandbox/math4phys/maxwell_example.py for Maxwell's equations")
    print("  2. See sandbox/math4phys/poisson.py for Poisson brackets")
    print("  3. See sandbox/math4phys/jacobi_proof.py for algebraic proofs")
    print("  4. Run tests: python3 -m pytest tests/math4phys/test_vector_calculus.py -v")
    print("=" * 70)
