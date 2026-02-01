# Symbolic Vector Calculus Engine

An operator-based symbolic vector calculus engine built on SymPy for proving vector calculus identities and working with
Hamiltonian mechanics.

## Overview

This module provides clean, mathematical abstractions for vector calculus and Hamiltonian mechanics:

- **Scalar and vector fields**: Work directly with SymPy Functions and Matrices
- **Differential operators**: gradient, divergence, curl, Laplacian, Hessian, Jacobian
- **Poisson brackets**: For Hamiltonian mechanics and phase space analysis
- **Identity verification**: Automatic checking of vector calculus identities
- **Dimension-agnostic**: Works in arbitrary dimensions (2D, 3D, 5D, n-D)

## Design Philosophy

**Operators as first-class objects:**

- Operators are composable transformations applied to SymPy expressions
- Work directly with SymPy Functions and Matrices
- Dimension checking at operator level
- Mathematical notation matches standard vector calculus

**Leverage SymPy's power:**

- SymPy handles all differentiation (product rule, chain rule, mixed partials)
- We provide dimension-aware wrappers and clean notation
- All results are exact symbolic expressions

## Installation

No additional dependencies beyond SymPy (already in requirements.txt).

```python
from sandbox.math4phys.diff_ops import (
    gradient, divergence, curl, laplacian, hessian, jacobian, poisson,
    make_scalar_field, make_vector_field,
    expr_equal, matrices_equal
)
```

## Quick Start

### Creating Fields

```python
from sympy import symbols
from sandbox.math4phys.diff_ops import make_scalar_field, make_vector_field

# Create coordinate symbols
x = symbols('x_1:4', real=True)  # x_1, x_2, x_3

# Create a scalar field f(x_1, x_2, x_3)
f = make_scalar_field('f', x)

# Create a vector field F(x_1, x_2, x_3) = (F_1, F_2, F_3)
F = make_vector_field('F', x, dim=3)
```

### Differential Operators

```python
# Gradient: ∇f (returns Matrix)
grad_f = gradient(f)  # With explicit args
grad_f = gradient(f, x)  # Args auto-detected from free_symbols

# Divergence: ∇·F (returns Expr)
div_F = divergence(F, x)

# Curl: ∇×F (returns Matrix, 3D only)
curl_F = curl(F, x)

# Laplacian: ∇²f (returns Expr or Matrix)
lap_f = laplacian(f, x)

# Hessian: ∂²f/∂x_i∂x_j (returns Matrix)
hess_f = hessian(f, x)

# Jacobian: ∂F_i/∂x_j (returns Matrix)
jac_F = jacobian(F, x)


```

### Optional Arguments

Most operators support optional `args` parameter:

```python
# If args is None, uses f.free_symbols sorted alphabetically by name
grad_f = gradient(f)  # Auto-detect variables
grad_f = gradient(f, x)  # Explicit variables (when order matters)
```

### Poisson Brackets (Hamiltonian Mechanics)

```python
from sympy import symbols, Matrix
from sandbox.math4phys.diff_ops import poisson

# Phase space coordinates
x = symbols('x_1:4', real=True)  # Position
p = symbols('p_1:4', real=True)  # Momentum

# Scalar functions on phase space
f = make_scalar_field('f', x + p)
g = make_scalar_field('g', x + p)

# Poisson bracket: {f, g} = ∑(∂f/∂x_i ∂g/∂p_i - ∂f/∂p_i ∂g/∂x_i)
bracket = poisson(f, g, x, p)

# Canonical commutation: {x_i, p_j} = δ_ij
poisson(x[0], p[0], x, p)  # Returns 1
poisson(x[0], p[1], x, p)  # Returns 0
```

## Examples

### 1. Vector Calculus Identities (Arbitrary Dimensions)

Verified in `tests/math4phys/test_diff_ops.py` for 5D:

```python
from sympy import symbols, zeros
from sandbox.math4phys.diff_ops import *

n_dim = 5
x = symbols(f'x_1:{n_dim + 1}', real=True)

f = make_scalar_field('f', x)
g = make_scalar_field('g', x)
F = make_vector_field('F', x, n_dim)
G = make_vector_field('G', x, n_dim)

# Product rule for divergence: ∇·(gF) = g(∇·F) + F·(∇g)
assert expr_equal(
    divergence(F * g),
    divergence(F) * g + (F.T * gradient(g))[0, 0]
)

# Product rule for gradient: ∇(fg) = f(∇g) + g(∇f)
assert matrices_equal(
    gradient(f * g),
    gradient(f) * g + f * gradient(g)
)

# Gradient of dot product: ∇(F·G) = J_F·G + J_G·F
assert matrices_equal(
    gradient(F.T * G),
    jacobian(F) * G + jacobian(G) * F
)

# Hessian equals Jacobian of gradient
assert matrices_equal(hessian(f), jacobian(gradient(f)))

# Product rule for Hessian
assert matrices_equal(
    hessian(f * g),
    hessian(f) * g + gradient(f) * gradient(g).T +
    gradient(g) * gradient(f).T + hessian(g) * f
)
```

### 2. Curl Identities (3D Only)

Verified in `tests/math4phys/test_diff_ops.py`:

```python
x = symbols('x_1:4', real=True)
f = make_scalar_field('f', x)
F = make_vector_field('F', x)
G = make_vector_field('G', x)

# Divergence of curl is zero: ∇·(∇×F) = 0
assert expr_equal(divergence(curl(F)), 0)

# Curl of gradient is zero: ∇×(∇f) = 0
assert matrices_equal(curl(gradient(f)), zeros(3, 1))

# Vector identity: ∇·(F×G) = G·(∇×F) - F·(∇×G)
assert expr_equal(
    divergence(F.cross(G)),
    (G.T * curl(F) - F.T * curl(G))[0, 0]
)

# Double curl: ∇×(∇×F) = ∇(∇·F) - ∇²F
assert matrices_equal(
    curl(curl(F)),
    gradient(divergence(F)) - laplacian(F)
)
```

### 3. Poisson Bracket Axioms

Verified in `tests/math4phys/test_poisson.py`:

```python
from sympy import symbols, Matrix
from sympy.abc import a, b
from sandbox.math4phys.diff_ops import poisson, make_scalar_field

x = symbols('x_1:4', real=True)
p = symbols('p_1:4', real=True)
X = Matrix(x)
P = Matrix(p)

A = make_scalar_field('A', x + p)
B = make_scalar_field('B', x + p)
C = make_scalar_field('C', x + p)

f = (X.T * X + P.T * P)[0, 0]
g = (P.T * P)[0, 0]
h = (X.T * P)[0, 0]

# Antisymmetry: {f, g} = -{g, f}
assert expr_equal(poisson(f, g, x, p) + poisson(g, f, x, p), 0)

# Linearity: {af + bg, h} = a{f, h} + b{g, h}
assert expr_equal(
    poisson(a * f + b * g, h, x, p),
    a * poisson(f, h, x, p) + b * poisson(g, h, x, p)
)

# Leibniz rule: {fg, h} = f{g, h} + g{f, h}
assert expr_equal(
    poisson(f * g, h, x, p),
    f * poisson(g, h, x, p) + g * poisson(f, h, x, p)
)

# Jacobi identity: {f, {g, h}} + {g, {h, f}} + {h, {f, g}} = 0
assert expr_equal(
    poisson(f, poisson(g, h, x, p), x, p) +
    poisson(g, poisson(h, f, x, p), x, p) +
    poisson(h, poisson(f, g, x, p), x, p),
    0
)

# Canonical commutation relation: {x_i, p_j} = δ_ij
for i in range(len(x)):
    for j in range(len(p)):
        assert expr_equal(poisson(x[i], p[j], x, p), i == j)
```

## API Reference

### Field Creation

**`make_scalar_field(name, args)`**

- Creates a real scalar field (SymPy Function)
- `name`: Function name (e.g., 'f')
- `args`: List of coordinate symbols
- Returns: SymPy Function object

**`make_vector_field(name, args, dim=3)`**

- Creates a real vector field (SymPy Matrix)
- Components named `name_1`, `name_2`, ..., `name_n`
- Returns: Matrix of Function objects

### Differential Operators

**`gradient(f, args=None)`**

- Returns gradient ∇f as (n×1) Matrix
- If `args=None`, uses `f.free_symbols` sorted alphabetically

**`divergence(F, args=None)`**

- Returns divergence ∇·F as Expr
- `F`: Vector field (Matrix)

**`curl(F, args=None)`**

- Returns curl ∇×F as (3×1) Matrix
- 3D only (raises TypeError otherwise)

**`laplacian(F, args=None)`**

- Returns Laplacian ∇²F
- If `F` is Expr: returns Expr
- If `F` is Matrix: returns Matrix of component Laplacians

**`hessian(f, args=None)`**

- Returns Hessian matrix of second derivatives
- Returns (n×n) Matrix

**`jacobian(F, args=None)`**

- Returns Jacobian matrix ∂F_i/∂x_j
- Returns (n×m) Matrix

**`poisson(A, B, x, p)`**

- Returns Poisson bracket {A, B}
- `A, B`: Scalar functions (Expr or 1×1 Matrix elements)
- `x, p`: Disjoint coordinate lists (position, momentum)
- Formula: ∑(∂A/∂x_i ∂B/∂p_i - ∂A/∂p_i ∂B/∂x_i)

### Utilities

**`expr_equal(f, g)`**

- Checks if two expressions are mathematically equal
- Uses `simplify(f - g) == 0`

**`matrices_equal(F, G)`**

- Checks if two matrices are mathematically equal
- Simplifies element-wise

## Testing

Run all tests:

```bash
# Differential operator tests (5D identities)
pytest tests/math4phys/test_diff_ops.py -v

# Poisson bracket tests (3D phase space)
pytest tests/math4phys/test_poisson.py -v

# All tests
pytest tests/math4phys/ -v
```

Tests cover:

- Differential operator identities in arbitrary dimensions
- Product rules (gradient, divergence, curl, Hessian)
- Curl identities (3D)
- Poisson bracket axioms (antisymmetry, linearity, Leibniz, Jacobi)
- Canonical commutation relations

All tests use **axiomatic verification** - no numerical values, pure symbolic manipulation.

## Architecture

### What SymPy Provides (we don't reimplement):

- ✓ Partial derivatives of any order
- ✓ Product rule, chain rule, quotient rule
- ✓ Mixed partials (Schwarz's theorem)
- ✓ Symbolic simplification
- ✓ Matrix operations

### What We Add:

- ✓ Clean operator-based API
- ✓ Dimension-aware operations
- ✓ Automatic argument detection (sorted free_symbols)
- ✓ Poisson bracket formalism for Hamiltonian mechanics
- ✓ Identity verification utilities

### Design Patterns:

1. **Operators return new objects** (immutable, functional style)
2. **Dimension checking** (e.g., curl only for 3D)
3. **Optional arguments** (auto-detect variables when possible)
4. **Pure symbolic** (no numerical evaluation)

## Performance

Optimized for **symbolic** computation:

- Fast for moderate expression sizes
- Test suite runs in ~0.1 seconds
- Use `simplify()` to reduce expression complexity
- For numerical computation, use NumPy/SciPy

## Comparison with SymPy's Vector Module

SymPy has `sympy.vector` with built-in coordinate systems.

**When to use SymPy's vector module:**

- Working specifically in 3D
- Need coordinate transformations (cylindrical, spherical)
- Want integrated coordinate system management

**When to use this engine:**

- Need arbitrary dimensions (works in any n-D)
- Want cleaner programmatic interface
- Building Hamiltonian mechanics applications
- Proving general identities

**Best practice**: Use both! This engine complements SymPy's tools.

## Applications

### Current Examples

- **Vector calculus identities** (arbitrary dimensions)
- **Hamiltonian mechanics** (Poisson brackets, phase space)
- **Jacobi identity** (dimension-independent proof)

### Future Extensions

- **Fluid mechanics**: Navier-Stokes, vorticity, stream functions
- **Electromagnetism**: Maxwell equations, gauge transformations
- **Differential geometry**: Connections, curvature, differential forms
- **Quantum mechanics**: Commutators, Heisenberg equations

## License

Part of the sandbox project. See main repository for license information.

## Contact

Questions? See `CLAUDE.md` in the repository root for guidance on working with this codebase.
