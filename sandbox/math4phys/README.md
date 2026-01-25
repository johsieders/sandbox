# Symbolic Vector Calculus Engine

A dimension-aware symbolic calculus engine built on SymPy for proving vector calculus identities
and deriving fundamental equations in mathematical physics.

## Overview

This module provides clean, mathematical abstractions for:

- **Scalar fields**: f: R^n → R
- **Vector fields**: F: R^n → R^m
- **Differential operators**: gradient, divergence, curl, Laplacian, Jacobian
- **Identity verification**: Automatic checking of vector calculus identities
- **Applications**: Maxwell equations, fluid mechanics, Hamiltonian mechanics

## Philosophy

**Leverage SymPy, don't rebuild it:**

- SymPy's differentiation engine handles all the calculus
- Product rule, chain rule, mixed partials all work automatically
- We provide dimension-aware wrappers and domain-specific notation

**Work symbolically:**

- No numerical values needed
- Proofs work for arbitrary dimensions and functions
- Follows the approach of `jacobi_proof.py`: pure symbol manipulation

## Installation

No additional dependencies beyond SymPy (already in requirements.txt).

```python
from math4phys.archive.vector_calculus_1 import (
   make_coords, ScalarField, VectorField,
   gradient, divergence, curl, laplacian
)
```

## Quick Start

### Basic Usage

```python
# Create 3D coordinate system
coords = make_coords('x y z')

# Create a scalar field f(x,y,z)
f = ScalarField('f', coords)

# Compute gradient: ∇f
grad_f = gradient(f)  # Returns VectorField

# Compute Laplacian: ∇²f
lap_f = f.laplacian()  # Returns scalar expression
```

### Vector Fields

```python
from math4phys.archive.vector_calculus_1 import make_vector_field

# Create electric field E = (E₁(x,y,z), E₂(x,y,z), E₃(x,y,z))
coords = make_coords('x y z')
E = make_vector_field('E', coords)

# Compute divergence: ∇·E
div_E = divergence(E)

# Compute curl: ∇×E (3D only)
curl_E = curl(E)

# Vector operations
B = make_vector_field('B', coords)
cross_product = E.cross(B)  # E×B
dot_product = E.dot(B)  # E·B
```

### Verifying Identities

```python
from math4phys.archive.vector_calculus_1 import (
   curl_of_gradient_is_zero,
   divergence_of_curl_is_zero,
   laplacian_is_div_grad
)

coords = make_coords('x y z')
f = ScalarField('f', coords)
F = make_vector_field('F', coords)

# Verify: ∇×(∇f) = 0
assert curl_of_gradient_is_zero(f)

# Verify: ∇·(∇×F) = 0
assert divergence_of_curl_is_zero(F)

# Verify: ∇²f = ∇·(∇f)
assert laplacian_is_div_grad(f)
```

## Examples

### 1. Vector Calculus Identities

All fundamental identities are verified in `tests/symbolics/test_vector_calculus.py`:

- ✓ ∇×(∇f) = 0 (curl of gradient is zero)
- ✓ ∇·(∇×F) = 0 (divergence of curl is zero)
- ✓ ∇²f = ∇·(∇f) (Laplacian definition)
- ✓ ∇·(fF) = f(∇·F) + F·(∇f) (product rule for divergence)
- ✓ ∇×(fF) = f(∇×F) + (∇f)×F (product rule for curl)

### 2. Maxwell's Equations

See `sandbox/symbolics/maxwell_example.py` for a complete implementation:

```python
from math4phys.scratch.maxwell_example import (
   create_em_fields,
   print_maxwell_equations,
   example_plane_wave
)

# Print all four Maxwell equations symbolically
print_maxwell_equations()

# Verify a plane wave solution
E, B = example_plane_wave()
```

Output:

```
1. Gauss's Law: ∇·E = 0
2. No Magnetic Monopoles: ∇·B = 0
3. Faraday's Law: ∇×E = -∂B/∂t
4. Ampère-Maxwell Law: ∇×B = μ₀ε₀∂E/∂t
```

### 3. Poisson Brackets (Hamiltonian Mechanics)

See `sandbox/symbolics/poisson.py` and `sandbox/symbolics/jacobi_proof.py`:

```python
from math4phys.archive.poisson import poisson_bracket, verify_jacobi_identity

# Verify Jacobi identity: {f, {g, h}} + {g, {h, f}} + {h, {f, g}} = 0
result, is_zero = verify_jacobi_identity(n_dim=3)
assert is_zero  # True!
```

The algebraic proof in `jacobi_proof.py` works for **any dimension** without expanding components.

### 4. Different Dimensions

The engine works in arbitrary dimensions:

```python
# 2D (e.g., complex analysis)
coords_2d = make_coords('x y')
f_2d = ScalarField('f', coords_2d)
grad_f_2d = gradient(f_2d)  # 2D gradient

# 4D (e.g., spacetime)
coords_4d = make_coords('t x y z')
phi = ScalarField('phi', coords_4d)
grad_phi = gradient(phi)  # 4D gradient
lap_phi = phi.laplacian()   # 4D Laplacian
```

**Note**: Curl is only defined for 3D fields.

## Architecture

### Core Classes

**ScalarField**: Represents scalar-valued functions

- `f.gradient()` → VectorField
- `f.laplacian()` → scalar
- `f.hessian()` → Matrix
- `f.diff(coord, order)` → derivative

**VectorField**: Represents vector-valued functions

- `F.divergence()` → scalar
- `F.curl()` → VectorField (3D only)
- `F.jacobian()` → Matrix
- `F.dot(G)` → scalar
- `F.cross(G)` → VectorField (3D only)
- `F + G`, `scalar * F` → VectorField

### Design Patterns

1. **SymPy does the heavy lifting**: All derivatives computed by SymPy's `diff()`
2. **Dimension awareness**: Classes track input/output dimensions and enforce rules
3. **Immutable operations**: Operations return new objects (functional style)
4. **Clean notation**: `gradient(f)` instead of manually computing `[∂f/∂x₁, ∂f/∂x₂, ...]`

### What SymPy Provides (we don't reimplement):

- ✓ Partial derivatives of any order
- ✓ Product rule, chain rule, quotient rule
- ✓ Mixed partials (Schwarz's theorem)
- ✓ Symbolic simplification and expansion
- ✓ LaTeX output generation
- ✓ Substitution and evaluation

### What We Add:

- ✓ Dimension-aware field abstractions
- ✓ Vector calculus operators as methods
- ✓ Identity verification functions
- ✓ Domain-specific applications (Maxwell, Poisson, etc.)
- ✓ Clean mathematical notation

## Testing

Run all tests:

```bash
python3 -m pytest tests/math4phys/test_vector_calculus.py -v
```

23 tests covering:

- Scalar and vector field operations
- All differential operators
- Fundamental vector calculus identities
- Product rules for divergence and curl
- Multi-dimensional support
- Jacobian matrices

All tests pass in ~0.2 seconds.

## Applications

### Current Examples

1. **Poisson Brackets** (`poisson.py`, `jacobi_proof.py`)
    - Hamiltonian mechanics
    - Phase space formulation
    - Jacobi identity proof (dimension-independent)

2. **Electromagnetism** (`maxwell_example.py`)
    - Maxwell's equations
    - Electromagnetic wave equation
    - Plane wave solutions
    - Poynting vector and energy conservation

### Future Applications

Ideas for extending the engine:

- **Fluid Mechanics**: Navier-Stokes equations, vorticity, stream functions
- **General Relativity**: Ricci tensor, Einstein equations, geodesics
- **Thermodynamics**: Maxwell relations, Legendre transforms
- **Differential Geometry**: Connections, curvature, differential forms
- **Quantum Mechanics**: Operators, commutators, Heisenberg equations

## Comparison with SymPy's Vector Module

SymPy has `sympy.vector` with `CoordSys3D`, `gradient()`, `divergence()`, `curl()`, etc.

**When to use SymPy's vector module:**

- Working specifically in 3D
- Need built-in coordinate transformations (cylindrical, spherical)
- Want integrated coordinate system management

**When to use this engine:**

- Need arbitrary dimensions (2D, 4D, n-D)
- Want cleaner programmatic interface
- Building domain-specific applications
- Following the algebraic proof pattern from `jacobi_proof.py`

**Best practice**: Use both! This engine can complement SymPy's tools.

## API Reference

### Functions

- `make_coords(coord_str)` - Create coordinate symbols from string
- `gradient(f)` - Compute ∇f
- `divergence(F)` - Compute ∇·F
- `curl(F)` - Compute ∇×F (3D only)
- `laplacian(f)` - Compute ∇²f
- `directional_derivative(f, v)` - Compute v·∇f
- `make_vector_field(name, coords, dim)` - Create symbolic vector field

### Identity Verification

- `curl_of_gradient_is_zero(f)` - Verify ∇×(∇f) = 0
- `divergence_of_curl_is_zero(F)` - Verify ∇·(∇×F) = 0
- `laplacian_is_div_grad(f)` - Verify ∇²f = ∇·(∇f)
- `verify_identity(left, right)` - General identity checker

### Classes

**ScalarField(name, coords)**

- `.func` - SymPy Function object
- `.dim` - Dimension
- `.gradient()` - Compute gradient
- `.laplacian()` - Compute Laplacian
- `.hessian()` - Compute Hessian matrix
- `.diff(coord, order)` - Partial derivative

**VectorField(components, coords, name)**

- `.components` - Matrix of components
- `.input_dim`, `.output_dim` - Dimensions
- `.divergence()` - Compute divergence
- `.curl()` - Compute curl (3D)
- `.jacobian()` - Compute Jacobian matrix
- `.dot(other)` - Dot product
- `.cross(other)` - Cross product (3D)
- `.simplify()`, `.expand()` - Simplification
- `.is_zero()` - Check if identically zero

## Performance

The engine is optimized for **symbolic** computation, not numerical:

- Fast for moderate expression sizes
- May be slow for very large expanded expressions
- Use `simplify()` to reduce expression complexity
- Test suite runs in ~0.2 seconds (23 tests)

For numerical computation, use NumPy/SciPy instead.

## References

### Implemented Examples

- `sandbox/symbolics/jacobi_proof.py` - Dimension-independent Jacobi identity
- `sandbox/symbolics/poisson.py` - Poisson brackets with concrete functions
- `sandbox/symbolics/maxwell_example.py` - Electromagnetic field theory
- `tests/symbolics/test_vector_calculus.py` - Complete test suite
- `tests/symbolic/test_poisson.py` - Poisson bracket tests

### Mathematical Background

- Vector calculus identities
- Maxwell's equations
- Hamiltonian mechanics and Poisson brackets
- Differential geometry (for future extensions)

## Contributing

To add new applications:

1. Create new module in `sandbox/symbolics/`
2. Import from `vector_calculus.py`
3. Add tests in `tests/symbolics/`
4. Follow the pattern: define fields → apply operators → verify identities

Example template:

```python
from math4phys.archive.vector_calculus_1 import (
   make_coords, ScalarField, VectorField,
   gradient, divergence, curl
)


def my_application():
   coords = make_coords('x y z')
   # ... define your fields and operators ...
   # ... verify your identities ...
   return results
```

## License

Part of the sandbox project. See main repository for license information.

## Contact

Questions? See `CLAUDE.md` in the repository root for guidance on working with this codebase.
