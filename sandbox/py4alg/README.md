# py4alg: A Compositional Algebra Library for Python

**A mathematically rigorous, protocol-based algebraic type system for Python**

## Overview

`py4alg` implements a compositional approach to algebraic structures, allowing the construction of arbitrarily complex mathematical types from simple building blocks. The library combines Python's protocol system with mathematical precision to create a type-safe, extensible framework for computational algebra.

## Architectural Philosophy

### The Compositional Type Tree

The library is built around two fundamental concepts:

1. **Base Types** (parameterless): Concrete implementations of basic algebraic structures
2. **Type Constructors** (parameterized): Functors that lift algebraic properties through type composition

This design creates a **tree of algebraic types** where any valid combination of constructors can be applied to base types, automatically inheriting the appropriate algebraic properties.

```
Base Types → Type Constructors → Composite Types
    ↓              ↓                   ↓
NativeInt  →  Polynomial[·]  →  Polynomial[NativeInt]
    ↓              ↓                   ↓
EuclideanRing → Ring → Ring    →    EuclideanRing
```

## Base Types (Foundation Layer)

These parameterless classes provide the foundation of the algebraic hierarchy:

| Type | Protocols | Description |
|------|-----------|-------------|
| `NativeInt` | `EuclideanRing`, `Comparable` | Integers with division algorithm |
| `NativeFloat` | `Field`, `Comparable` | Floating-point field |
| `NativeComplex` | `Field`, `Comparable` | Complex number field |
| `Fp` | `Field`, `Comparable` | Finite field Z/pZ |
| `ECpoint` | `AbelianGroup` | Elliptic curve points |

Each base type implements specific **protocols** that define their algebraic behavior through method signatures.

## Type Constructors (Functor Layer)

These parameterized classes are **functors** that lift algebraic structures to more complex domains:

| Constructor | Signature | Result Protocol | Description |
|-------------|-----------|----------------|-------------|
| `Matrix[T]` | `Ring → Ring` | `Ring` | Matrix algebra over rings |
| `Complex[T]` | `Field → Field` | `Field` | Complex numbers over arbitrary fields |
| `Fraction[T]` | `EuclideanRing → Field` | `Field` | Field of fractions (quotient field) |
| `Polynomial[T]` | `Ring → Ring` | `Ring` | Polynomial rings |
| `Polynomial[T]` | `Field → EuclideanRing` | `EuclideanRing` | Polynomials over fields (with division) |

### Functor Properties

Each type constructor preserves and transforms algebraic structure:
- **Covariant**: If `S ⊆ T` in the protocol hierarchy, then `F[S] ⊆ F[T]`
- **Structure-preserving**: Algebraic operations are lifted consistently
- **Composable**: Multiple constructors can be applied sequentially

## Protocol System

The library uses Python's `@runtime_checkable` protocols to define algebraic structures:

```python
@runtime_checkable
class Ring(AbelianGroup, Protocol):
    def __mul__(self, other: Any) -> Any: ...
    def one(self) -> Any: ...
    # ... inherits additive structure from AbelianGroup
```

### Protocol Hierarchy

```
AbelianGroup
    ↓
   Ring
    ↓
EuclideanRing  ←→  Field
    ↓               ↓
    └─── (both) ────┘
```

**Comparable** forms an orthogonal hierarchy for ordered structures.

## Compositional Examples

The power of this system lies in its **compositional nature**. Here are some valid type combinations:

### Simple Compositions
```python
# Polynomials over integers
Polynomial[NativeInt]  # → EuclideanRing

# Complex numbers over rationals
Complex[Fraction[NativeInt]]  # → Field

# Matrices over finite fields
Matrix[Fp]  # → Ring
```

### Deep Compositions
```python
# Matrices of polynomials over complex rationals
Matrix[Polynomial[Complex[Fraction[NativeInt]]]]  # → Ring

# Polynomials over matrix rings
Polynomial[Matrix[NativeFloat]]  # → Ring

# Fractions of polynomial rings (rational functions)
Fraction[Polynomial[NativeInt]]  # → Field
```

### Infinite Possibilities
The compositional system generates **infinitely many valid types**:
- Any constructor can be applied to any compatible base type
- Multiple constructors can be chained in any valid order
- The resulting type automatically implements appropriate protocols

## Rigorous Testing Framework

### Protocol-Based Testing

The testing system automatically validates algebraic properties:

```python
def test_ring_properties():
    """Test all ring axioms for any Ring implementation."""
    sample_groups = get_samples_for_protocol(Ring)
    for sample_list in sample_groups:
        check_rings(sample_list)  # Verifies all ring axioms
```

### Axiomatic Property Verification

Tests verify mathematical **axioms directly**:
- **Associativity**: `(a + b) + c = a + (b + c)`
- **Commutativity**: `a + b = b + a`
- **Distributivity**: `a × (b + c) = (a × b) + (a × c)`
- **Identity elements**: `a + 0 = a`, `a × 1 = a`
- **Inverse elements**: `a + (-a) = 0`

### Automatic Type Discovery

The framework automatically:
1. **Discovers** all types implementing each protocol
2. **Groups** samples by type to avoid mixing incompatible structures
3. **Tests** each group against appropriate axioms
4. **Reports** which types satisfy which protocols

## Implementation Details

### Type Safety Through Protocols
```python
# Runtime protocol checking ensures type safety
isinstance(polynomial_ring, Ring)  # → True
isinstance(polynomial_ring, Field)  # → False (unless over a field)
```

### Descent Tracking
Each composite type tracks its construction history:
```python
complex_poly = Complex[Polynomial[NativeInt]]()
complex_poly.descent()  # → [Complex, Polynomial, NativeInt]
```

### Error Propagation
The system gracefully handles undefined values (like division by zero) using Excel-style error propagation through string values.

## Usage Examples

### Basic Usage
```python
from py4alg.wrapper import NativeInt
from py4alg.mapper import Polynomial

# Create a polynomial ring over integers
P = Polynomial[NativeInt]
p = P([1, 2, 3])  # represents 1 + 2x + 3x²
q = P([4, 5])     # represents 4 + 5x

result = p * q    # polynomial multiplication
assert isinstance(result, Ring)  # automatic protocol satisfaction
```

### Advanced Compositions
```python
# Build complex rational functions
from py4alg.mapper import Complex, Fraction, Polynomial

# Rational functions over complex numbers
RationalComplex = Fraction[Polynomial[Complex[NativeFloat]]]
f = RationalComplex(numerator_poly, denominator_poly)

# This type automatically implements Field protocol!
assert isinstance(f, Field)
```

## Mathematical Foundations

### Category Theory Inspiration
The design draws from **category theory**:
- **Objects**: Algebraic types and their protocol implementations
- **Morphisms**: Structure-preserving maps between types
- **Functors**: Type constructors that preserve algebraic relationships
- **Composition**: Sequential application of type constructors

### Algebraic Correctness
Every operation is mathematically sound:
- **Closure**: Operations never leave their algebraic structure
- **Consistency**: Axioms are verified by property-based testing
- **Completeness**: All standard algebraic structures are representable

## Educational Value

This library serves as a **computational textbook** of abstract algebra:
- **Concepts**: Each protocol corresponds to a mathematical definition
- **Examples**: Infinite variety of concrete algebraic structures
- **Verification**: Axioms are tested, not assumed
- **Exploration**: Easy to construct and experiment with new combinations

## Research Applications

The compositional approach enables:
- **Algorithm development** for generic algebraic structures
- **Performance analysis** across different implementations
- **Correctness verification** through property-based testing
- **Educational tools** for teaching abstract algebra

## Future Extensions

The architecture naturally accommodates:
- **New base types**: Additional number systems, geometric objects
- **New constructors**: Tensor products, group algebras, Lie algebras
- **New protocols**: Categories, topological structures, differential forms
- **Performance optimization**: Specialized implementations for common patterns

---

**py4alg** represents a new paradigm in computational algebra: a system where mathematical correctness, type safety, and compositional flexibility converge to create an infinitely extensible, rigorously tested algebraic universe.