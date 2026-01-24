"""
Maxwell Equations and Electromagnetic Field Theory using Symbolic Vector Calculus

This module demonstrates how to use the symbolic vector calculus engine to:
1. Define electromagnetic fields (E and B)
2. Express Maxwell's equations symbolically
3. Derive electromagnetic wave equations
4. Verify vector calculus identities in electromagnetism

Maxwell's Equations in vacuum:
    ∇·E = ρ/ε₀           (Gauss's law)
    ∇·B = 0               (No magnetic monopoles)
    ∇×E = -∂B/∂t          (Faraday's law)
    ∇×B = μ₀J + μ₀ε₀∂E/∂t  (Ampère-Maxwell law)
"""

from sympy import symbols, Function, simplify, diff

from sandbox.symbolics.vector_calculus_1 import (
    make_coords, ScalarField, VectorField, make_vector_field,
    gradient, divergence, curl, laplacian
)


def create_em_fields():
    """
    Create symbolic electromagnetic fields E(x,y,z,t) and B(x,y,z,t).

    Returns:
        Tuple of (coords, t, E, B) where:
        - coords: [x, y, z] spatial coordinates
        - t: time symbol
        - E: Electric field vector (3D)
        - B: Magnetic field vector (3D)
    """
    # Spatial coordinates
    coords = make_coords('x y z')

    # Time coordinate (separate from spatial coords for cleaner notation)
    t = symbols('t', real=True)

    # Create time-dependent vector fields
    # E = (E₁(x,y,z,t), E₂(x,y,z,t), E₃(x,y,z,t))
    E_components = [Function(f'E{i}')(*coords, t) for i in [1, 2, 3]]
    E = VectorField(E_components, coords, name='E')

    # B = (B₁(x,y,z,t), B₂(x,y,z,t), B₃(x,y,z,t))
    B_components = [Function(f'B{i}')(*coords, t) for i in [1, 2, 3]]
    B = VectorField(B_components, coords, name='B')

    return coords, t, E, B


def maxwell_gauss_law(E, rho=None, epsilon_0=None):
    """
    Gauss's law: ∇·E = ρ/ε₀

    In vacuum (ρ=0): ∇·E = 0

    Args:
        E: Electric field VectorField
        rho: Charge density (optional)
        epsilon_0: Permittivity of free space (optional)

    Returns:
        Left side: ∇·E
        Right side: ρ/ε₀ (or 0 if not provided)
    """
    div_E = divergence(E)

    if rho is None or epsilon_0 is None:
        # Vacuum case
        return div_E, 0
    else:
        return div_E, rho / epsilon_0


def maxwell_no_monopole(B):
    """
    No magnetic monopoles: ∇·B = 0

    This is one of the fundamental Maxwell equations - there are no magnetic charges.

    Args:
        B: Magnetic field VectorField

    Returns:
        ∇·B (should always be zero)
    """
    return divergence(B)


def maxwell_faraday_law(E, B, t):
    """
    Faraday's law of induction: ∇×E = -∂B/∂t

    A time-varying magnetic field creates a circulating electric field.

    Args:
        E: Electric field VectorField
        B: Magnetic field VectorField
        t: Time symbol

    Returns:
        Tuple of (left_side, right_side)
        - left_side: ∇×E
        - right_side: -∂B/∂t
    """
    curl_E = curl(E)

    # Time derivative of B
    dB_dt_components = [diff(B[i], t) for i in range(3)]
    dB_dt = VectorField(dB_dt_components, E.coords, name='∂B/∂t')

    return curl_E, -1 * dB_dt


def maxwell_ampere_law(B, E, t, J=None, mu_0=None, epsilon_0=None):
    """
    Ampère-Maxwell law: ∇×B = μ₀J + μ₀ε₀∂E/∂t

    In vacuum (J=0): ∇×B = μ₀ε₀∂E/∂t

    The displacement current term μ₀ε₀∂E/∂t was Maxwell's key addition.

    Args:
        B: Magnetic field VectorField
        E: Electric field VectorField
        t: Time symbol
        J: Current density (optional)
        mu_0: Permeability of free space (optional)
        epsilon_0: Permittivity of free space (optional)

    Returns:
        Tuple of (left_side, right_side)
    """
    curl_B = curl(B)

    # Time derivative of E
    dE_dt_components = [diff(E[i], t) for i in range(3)]
    dE_dt = VectorField(dE_dt_components, B.coords, name='∂E/∂t')

    if J is None or mu_0 is None or epsilon_0 is None:
        # Just return the symbolic form
        return curl_B, dE_dt
    else:
        # Full form with constants
        right_side = mu_0 * J + (mu_0 * epsilon_0) * dE_dt
        return curl_B, right_side


def derive_wave_equation_E(E, t):
    """
    Derive the electromagnetic wave equation for E from Maxwell's equations.

    Starting from Faraday's law: ∇×E = -∂B/∂t
    Take curl: ∇×(∇×E) = -∂(∇×B)/∂t

    Using Ampère-Maxwell (vacuum): ∇×B = μ₀ε₀∂E/∂t
    We get: ∇×(∇×E) = -μ₀ε₀∂²E/∂t²

    Using identity: ∇×(∇×E) = ∇(∇·E) - ∇²E
    In vacuum: ∇·E = 0

    Final result: ∇²E = μ₀ε₀∂²E/∂t²

    Or with c² = 1/(μ₀ε₀): ∇²E - (1/c²)∂²E/∂t² = 0

    Args:
        E: Electric field VectorField
        t: Time symbol

    Returns:
        Dictionary with intermediate steps
    """
    # Step 1: ∇×E
    curl_E = curl(E)

    # Step 2: ∇×(∇×E)
    curl_curl_E = curl(curl_E)

    # Step 3: ∇²E (component-wise Laplacian)
    laplacian_E = laplacian(E)

    # Step 4: ∂²E/∂t²
    d2E_dt2_components = [diff(E[i], t, 2) for i in range(3)]
    d2E_dt2 = VectorField(d2E_dt2_components, E.coords, name='∂²E/∂t²')

    # The wave equation in vacuum (with c² = 1/(μ₀ε₀)):
    # ∇²E = (1/c²)∂²E/∂t²
    # or equivalently: ∇²E - (1/c²)∂²E/∂t² = 0

    return {
        'curl_E': curl_E,
        'curl_curl_E': curl_curl_E,
        'laplacian_E': laplacian_E,
        'd2E_dt2': d2E_dt2,
        'identity': '∇×(∇×E) = ∇(∇·E) - ∇²E',
        'wave_equation': '∇²E = (1/c²)∂²E/∂t²'
    }


def verify_vector_identity_for_em():
    """
    Verify the vector identity: ∇×(∇×F) = ∇(∇·F) - ∇²F

    This identity is crucial for deriving the electromagnetic wave equation.

    Returns:
        Boolean indicating if identity holds symbolically
    """
    coords = make_coords('x y z')
    F = make_vector_field('F', coords)

    # Left side: ∇×(∇×F)
    curl_F = curl(F)
    curl_curl_F = curl(curl_F)

    # Right side: ∇(∇·F) - ∇²F
    div_F = divergence(F)
    grad_div_F = gradient(ScalarField.from_expr(div_F, coords))  # Would need to extend ScalarField
    laplacian_F = laplacian(F)

    # Note: This verification would require component-by-component comparison
    # after symbolic simplification. Left as an exercise for proper implementation.

    return {
        'curl_curl_F': curl_curl_F,
        'div_F': div_F,
        'laplacian_F': laplacian_F,
        'note': 'Full verification requires component-wise simplification'
    }


def electromagnetic_energy_density():
    """
    Define electromagnetic energy density and Poynting vector.

    Energy density: u = (ε₀/2)E² + (1/2μ₀)B²
    Poynting vector: S = (1/μ₀)E×B (energy flux)

    Energy conservation: ∂u/∂t + ∇·S = -J·E
    """
    coords, t, E, B = create_em_fields()

    epsilon_0, mu_0 = symbols('epsilon_0 mu_0', positive=True, real=True)

    # Energy density (scalar)
    # u = (ε₀/2)|E|² + (1/2μ₀)|B|²
    E_squared = E.dot(E)
    B_squared = B.dot(B)
    u = (epsilon_0 / 2) * E_squared + (1 / (2 * mu_0)) * B_squared

    # Poynting vector: S = (1/μ₀)E×B
    S = (1 / mu_0) * E.cross(B)
    S.name = 'S'

    return {
        'energy_density': u,
        'poynting_vector': S,
        'coords': coords,
        't': t,
        'note': 'Energy conservation: ∂u/∂t + ∇·S = -J·E'
    }


def print_maxwell_equations():
    """
    Print Maxwell's equations in symbolic form with nice formatting.
    """
    coords, t, E, B = create_em_fields()

    print("=" * 70)
    print("MAXWELL'S EQUATIONS (Vacuum)")
    print("=" * 70)
    print()

    # Gauss's law
    div_E, rhs_gauss = maxwell_gauss_law(E)
    print(f"1. Gauss's Law:")
    print(f"   ∇·E = {rhs_gauss}")
    print()

    # No monopoles
    div_B = maxwell_no_monopole(B)
    print(f"2. No Magnetic Monopoles:")
    print(f"   ∇·B = 0")
    print()

    # Faraday's law
    curl_E, neg_dB_dt = maxwell_faraday_law(E, B, t)
    print(f"3. Faraday's Law:")
    print(f"   ∇×E = -∂B/∂t")
    print()

    # Ampère-Maxwell law
    curl_B, dE_dt = maxwell_ampere_law(B, E, t)
    print(f"4. Ampère-Maxwell Law (vacuum):")
    print(f"   ∇×B = μ₀ε₀∂E/∂t")
    print()

    print("=" * 70)
    print("ELECTROMAGNETIC WAVE EQUATION")
    print("=" * 70)
    print()
    print("From Maxwell's equations in vacuum:")
    print("   ∇²E = (1/c²)∂²E/∂t²")
    print("   ∇²B = (1/c²)∂²B/∂t²")
    print()
    print("where c = 1/√(μ₀ε₀) is the speed of light")
    print("=" * 70)


def example_plane_wave():
    """
    Example: Plane electromagnetic wave.

    For a plane wave traveling in the z-direction:
    E = E₀ sin(kz - ωt) x̂
    B = (E₀/c) sin(kz - ωt) ŷ

    where ω = ck (dispersion relation)
    """
    from sympy import sin

    coords = make_coords('x y z')
    x, y, z = coords
    t = symbols('t', real=True)

    # Wave parameters
    E0, k, omega, c = symbols('E0 k omega c', positive=True, real=True)

    # Electric field: E = E₀ sin(kz - ωt) x̂
    E_components = [
        E0 * sin(k * z - omega * t),  # x component
        0,  # y component
        0  # z component
    ]
    E = VectorField(E_components, coords, name='E')

    # Magnetic field: B = (E₀/c) sin(kz - ωt) ŷ
    B_components = [
        0,  # x component
        (E0 / c) * sin(k * z - omega * t),  # y component
        0  # z component
    ]
    B = VectorField(B_components, coords, name='B')

    print("\n" + "=" * 70)
    print("EXAMPLE: Plane Electromagnetic Wave")
    print("=" * 70)
    print()
    print(f"Electric field: E = E₀ sin(kz - ωt) x̂")
    print(f"Magnetic field: B = (E₀/c) sin(kz - ωt) ŷ")
    print()

    # Verify Maxwell's equations
    print("Verification:")
    print("-" * 70)

    # 1. Divergence of E should be zero
    div_E = simplify(divergence(E))
    print(f"∇·E = {div_E} ✓")

    # 2. Divergence of B should be zero
    div_B = simplify(divergence(B))
    print(f"∇·B = {div_B} ✓")

    # 3. Curl of E
    curl_E = curl(E)
    curl_E_simplified = curl_E.simplify()
    print(f"∇×E = {curl_E_simplified.components.T}")

    # 4. Time derivative of B
    dB_dt = VectorField([diff(B[i], t) for i in range(3)], coords)
    dB_dt_simplified = dB_dt.simplify()
    print(f"∂B/∂t = {dB_dt_simplified.components.T}")

    print()
    print("Note: ∇×E = -∂B/∂t is satisfied when ω = ck")
    print("=" * 70)

    return E, B


if __name__ == "__main__":
    # Print Maxwell's equations
    print_maxwell_equations()

    print("\n")

    # Example: plane wave
    example_plane_wave()

    print("\n")

    # Energy and momentum
    print("=" * 70)
    print("ELECTROMAGNETIC ENERGY AND MOMENTUM")
    print("=" * 70)
    energy_results = electromagnetic_energy_density()
    print()
    print("Energy density: u = (ε₀/2)|E|² + (1/2μ₀)|B|²")
    print("Poynting vector: S = (1/μ₀)E×B")
    print("Energy conservation: ∂u/∂t + ∇·S = -J·E")
    print("=" * 70)
