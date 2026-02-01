# Symbolic Differentiation Engine - IMPLEMENTED ✓

## Status: Initial version complete (2026-01-18)

I wanted to implement an engine for symbolic calculus with SymPy that calculates exactly as a mathematician would do.
Applications: deriving the numerous laws concerning div, grad, curl; deriving the Maxwell equations
and related equations, and so on.

**Good news: SymPy already provides most of what we need!** I've built a clean wrapper layer on top of SymPy.

## What's Been Built

### Core Module: `vector_calculus.py`

A dimension-aware symbolic calculus engine with:

- ✓ **ScalarField**: f: R^n → R with gradient, Laplacian, Hessian
- ✓ **VectorField**: F: R^n → R^m with divergence, curl, Jacobian
- ✓ **Differential operators**: gradient, divergence, curl, Laplacian (all dimensions)
- ✓ **Vector operations**: dot product, cross product, addition, scalar multiplication
- ✓ **Identity verification**: Automatic checking of vector calculus identities
- ✓ **Product rules**: Automatically applied by SymPy

### Examples and Applications

1. **Test Suite** (`tests/symbolics/test_vector_calculus.py`)
    - 23 tests, all passing in ~0.2 seconds
    - Verifies all fundamental identities:
        - ∇×(∇f) = 0
        - ∇·(∇×F) = 0
        - ∇²f = ∇·(∇f)
        - Product rules for divergence and curl

2. **Maxwell Equations** (`maxwell_example.py`)
    - All four Maxwell equations in symbolic form
    - Wave equation derivation
    - Plane wave solution verification
    - Poynting vector and energy conservation

3. **Poisson Brackets** (already had: `poisson.py`, `jacobi_proof.py`)
    - Hamiltonian mechanics
    - Jacobi identity proof (dimension-independent)

4. **Demo Script** (`demo.py`)
    - Quick introduction to all features
    - Run: `python3 -m sandbox.symbolics.demo`

### Architecture

**What SymPy provides (we leverage, don't rebuild):**

- Partial derivatives with product rule, chain rule
- Mixed partials (Schwarz's theorem)
- Symbolic simplification
- LaTeX output

**What we added (thin wrapper layer):**

- Dimension-aware field abstractions
- Clean vector calculus operator notation
- Identity verification functions
- Domain-specific applications

## Original Requirements vs Implementation

| Requirement                                    | Status | Implementation                                   |
|------------------------------------------------|--------|--------------------------------------------------|
| Symbolic vectors/matrices with dimension       | ✓      | VectorField class with input_dim, output_dim     |
| Vector operations (add, multiply, scalar mult) | ✓      | Overloaded operators: +, *, dot(), cross()       |
| Standard element names (a_ij)                  | ✓      | Auto-generated: F1, F2, F3 or custom names       |
| Symbolic functions with signatures             | ✓      | ScalarField, VectorField with dimension tracking |
| diff-1 operator                                | ✓      | ScalarField.diff(), gradient()                   |
| Partial diff operator (∂ᵢFⱼ)                   | ✓      | VectorField.jacobian()                           |
| Jacobian matrix JF(x)                          | ✓      | VectorField.jacobian()                           |
| Integration                                    | ⚬      | Not yet (future work)                            |

## Next Steps: Future Applications

Now that the engine is built, here are ideas for extending it:

### 1. Fluid Mechanics

- Navier-Stokes equations
- Vorticity: ω = ∇×v
- Stream functions
- Incompressibility: ∇·v = 0

### 2. General Relativity

- Ricci tensor
- Einstein field equations
- Geodesic equations
- Schwarzschild metric

### 3. Thermodynamics

- Maxwell relations
- Legendre transforms
- Thermodynamic potentials

### 4. Differential Geometry

- Covariant derivatives
- Curvature tensors
- Differential forms
- Exterior calculus (d, ∧, *)

### 5. Quantum Mechanics

- Commutators: [A, B]
- Heisenberg equations
- Angular momentum operators
- Quantum field operators

### 6. Integration (if needed)

- Line integrals: ∫_C F·dr
- Surface integrals: ∬_S F·dS
- Volume integrals: ∭_V f dV
- Divergence theorem, Stokes' theorem

## Files Created

```
sandbox/symbolics/
├── vector_calculus.py      # Core engine (510 lines)
├── maxwell_example.py      # Electromagnetic applications (350 lines)
├── demo.py                 # Quick demo script (270 lines)
├── README.md               # Complete documentation
├── jacobi_proof.py         # Already had (algebraic proof)
└── poisson.py              # Already had (Poisson brackets)

tests/symbolics/
└── test_vector_calculus.py # Test suite (23 tests, all passing)
```

## Quick Start

```python
from math4phys.archive.vector_calculus_1 import (
    make_coords, ScalarField, make_vector_field,
    gradient, divergence, curl
)

# Create 3D coordinates
coords = make_coords('x y z')

# Scalar field
f = ScalarField('f', coords)
grad_f = gradient(f)  # ∇f
lap_f = f.laplacian()  # ∇²f

# Vector field
E = make_vector_field('E', coords)
div_E = divergence(E)  # ∇·E
curl_E = curl(E)  # ∇×E

# Verify identity: ∇×(∇f) = 0
assert curl(gradient(f)).is_zero()
```

## Conclusion

**SymPy was the right choice.** The hard mathematics is already there - we just needed:

1. Clean abstractions (ScalarField, VectorField)
2. Dimension awareness
3. Domain-specific applications

The engine follows the elegant pattern from `jacobi_proof.py`: work symbolically with abstract functions,
let SymPy handle derivatives, verify identities through simplification.

Ready to derive Maxwell, Navier-Stokes, Einstein equations, and more!

## An operator based approach.

I am still thinking and weighing options.

The basic operator is the partial derivative, diff(f, x).
My preferred notation is $\partial_x$ if the variables have names, or  $\partial_i$, if they are indexed.

diff accepts a function R^n -> R^1 and a variable by name or index.

The gradient operator, denoted by $\partial$ is the column vector of all $\partial_i$ (i = 1 ... n),
and the gradient of a scalar valued function $f$ $\partial \cdot f$ is the formal product of the gradient operator
and $f$ (a scalar).

The Laplacian operator is $\partial^2$

The Hessian operator is $\partial \ocross \partial = \partial^{\ocross 2}$ the formal outer product (tensor product) of
\partial with itself

The higher derivatives that appear e.g. in the general Taylor formula are just $\partial^{\ocross k}$

Poisson brackets applied to A, B is $\partial_x A \partial_p B - \partial_p A \partial_x B$,
the Poisson brackets operator is lambda A, B : $\partial_x A \partial_p B - \partial_p A \partial_x B$

Let $F$ be a vector field:

The curl of $F$ is $\partial \cross F$, the curl operator would be lambda F: $\partial \cross F$
The Jacobian of $F$ is $\partial \ocross F$, the Jacobian operator would be lambda F: $\partial \ocross F$

Here is my approach: It should be easy to write a class that implements this strictly formal mechanism.
Many identities can be formally proven.

The elements of this class are operators that can be applied to SymPy Functions and Matrices of Functions.
I wonder if we can do without the existing classes ScalarField and VectorField and possibly TensorField.
No problem if we keep them, but I like the operator based thinking.

I want to make sure that dimensions match, that a curl works only in three dimension and so on.

```{math}
\left[\begin{matrix}\frac{d^{2}}{d \frac{d}{d t} x_{1}{\left(t \right)}^{2}} 
L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \frac{d^{2}}{d t^{2}} x_{1}{\left(t \right)} + \frac{d}{d t} x_{1}{\left(t \right)} \left. \frac{\partial^{2}}{\partial x_{1}{\left(t \right)}\partial \xi} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\xi,\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi=\frac{d}{d t} x_{1}{\left(t \right)} }} + \frac{d}{d t} x_{2}{\left(t \right)} \left. \frac{\partial^{2}}{\partial \frac{d}{d t} x_{1}{\left(t \right)}\partial \xi_{2}} L{\left(x_{1}{\left(t \right)},\xi_{2},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi_{2}=x_{2}{\left(t \right)} }} + \frac{d^{2}}{d t^{2}} x_{2}{\left(t \right)} \frac{d^{2}}{d \frac{d}{d t} x_{2}{\left(t \right)}d \frac{d}{d t} x_{1}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} + \frac{d}{d t} x_{3}{\left(t \right)} \left. \frac{\partial^{2}}{\partial \frac{d}{d t} x_{1}{\left(t \right)}\partial \xi_{3}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},\xi_{3},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi_{3}=x_{3}{\left(t \right)} }} + \frac{d^{2}}{d t^{2}} x_{3}{\left(t \right)} \frac{d^{2}}{d \frac{d}{d t} x_{3}{\left(t \right)}d \frac{d}{d t} x_{1}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} + \left. \frac{\partial}{\partial x_{1}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\xi,\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi=\frac{d}{d t} x_{1}{\left(t \right)} }}\\\frac{d^{2}}{d \frac{d}{d t} x_{2}{\left(t \right)}^{2}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \frac{d^{2}}{d t^{2}} x_{2}{\left(t \right)} + \frac{d}{d t} x_{1}{\left(t \right)} \left. \frac{\partial^{2}}{\partial \frac{d}{d t} x_{2}{\left(t \right)}\partial \xi_{1}} L{\left(\xi_{1},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi_{1}=x_{1}{\left(t \right)} }} + \frac{d^{2}}{d t^{2}} x_{1}{\left(t \right)} \frac{d^{2}}{d \frac{d}{d t} x_{2}{\left(t \right)}d \frac{d}{d t} x_{1}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} + \frac{d}{d t} x_{2}{\left(t \right)} \left. \frac{\partial^{2}}{\partial x_{2}{\left(t \right)}\partial \xi} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\xi,\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi=\frac{d}{d t} x_{2}{\left(t \right)} }} + \frac{d}{d t} x_{3}{\left(t \right)} \left. \frac{\partial^{2}}{\partial \frac{d}{d t} x_{2}{\left(t \right)}\partial \xi_{3}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},\xi_{3},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi_{3}=x_{3}{\left(t \right)} }} + \frac{d^{2}}{d t^{2}} x_{3}{\left(t \right)} \frac{d^{2}}{d \frac{d}{d t} x_{3}{\left(t \right)}d \frac{d}{d t} x_{2}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} + \left. \frac{\partial}{\partial x_{2}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\xi,\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi=\frac{d}{d t} x_{2}{\left(t \right)} }}\\\frac{d^{2}}{d \frac{d}{d t} x_{3}{\left(t \right)}^{2}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \frac{d^{2}}{d t^{2}} x_{3}{\left(t \right)} + \frac{d}{d t} x_{1}{\left(t \right)} \left. \frac{\partial^{2}}{\partial \frac{d}{d t} x_{3}{\left(t \right)}\partial \xi_{1}} L{\left(\xi_{1},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi_{1}=x_{1}{\left(t \right)} }} + \frac{d^{2}}{d t^{2}} x_{1}{\left(t \right)} \frac{d^{2}}{d \frac{d}{d t} x_{3}{\left(t \right)}d \frac{d}{d t} x_{1}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} + \frac{d}{d t} x_{2}{\left(t \right)} \left. \frac{\partial^{2}}{\partial \frac{d}{d t} x_{3}{\left(t \right)}\partial \xi_{2}} L{\left(x_{1}{\left(t \right)},\xi_{2},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ \xi_{2}=x_{2}{\left(t \right)} }} + \frac{d^{2}}{d t^{2}} x_{2}{\left(t \right)} \frac{d^{2}}{d \frac{d}{d t} x_{3}{\left(t \right)}d \frac{d}{d t} x_{2}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} + \frac{d}{d t} x_{3}{\left(t \right)} \left. \frac{\partial^{2}}{\partial x_{3}{\left(t \right)}\partial \xi} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\xi \right)} \right|_{\substack{ \xi=\frac{d}{d t} x_{3}{\left(t \right)} }} + \left. \frac{\partial}{\partial x_{3}{\left(t \right)}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\xi \right)} \right|_{\substack{ \xi=\frac{d}{d t} x_{3}{\left(t \right)} }}\end{matrix}\right] = \left[\begin{matrix}\left. \frac{\partial}{\partial x_{1}} L{\left(x_{1},x_{2}{\left(t \right)},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ x_{1}=x_{1}{\left(t \right)} }}\\\left. \frac{\partial}{\partial x_{2}} L{\left(x_{1}{\left(t \right)},x_{2},x_{3}{\left(t \right)},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ x_{2}=x_{2}{\left(t \right)} }}\\\left. \frac{\partial}{\partial x_{3}} L{\left(x_{1}{\left(t \right)},x_{2}{\left(t \right)},x_{3},\frac{d}{d t} x_{1}{\left(t \right)},\frac{d}{d t} x_{2}{\left(t \right)},\frac{d}{d t} x_{3}{\left(t \right)} \right)} \right|_{\substack{ x_{3}=x_{3}{\left(t \right)} }}\end{matrix}\right]
```
