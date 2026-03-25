# py4alg: A Compositional Algebra Library for Python

**A mathematically rigorous, protocol-based algebraic type system for Python**

## Overview

`py4alg` implements a compositional approach to algebraic structures, allowing the construction of arbitrarily complex
mathematical types from simple building blocks. The library combines Python's protocol system with mathematical
precision to create a type-safe, extensible framework for computational algebra.

## Architectural Philosophy

### The Compositional Type Tree

The library is built around two fundamental concepts:

1. **Base Types** (parameterless): Concrete implementations of basic algebraic structures
2. **Type Constructors** (parameterized): Functors that lift algebraic properties through type composition

This design creates a **tree of algebraic types** where any valid combination of constructors can be applied to base
types, automatically inheriting the appropriate algebraic properties.

```
Base Types → Type Constructors → Composite Types
    ↓              ↓                   ↓
NativeInt  →  Polynomial[·]  →  Polynomial[NativeInt]
    ↓              ↓                   ↓
EuclideanRing → Ring → Ring    →    EuclideanRing
```

## Base Types (Foundation Layer)

These parameterless classes provide the foundation of the algebraic hierarchy:

| Type            | Protocols                     | Description                         |
|-----------------|-------------------------------|-------------------------------------|
| `NativeInt`     | `EuclideanRing`, `Comparable` | Integers with division algorithm    |
| `NativeFloat`   | `Field`, `Comparable`         | Floating-point field (with tolerance) |
| `NativeComplex` | `Field`                       | Complex number field                |
| `Fp`            | `Field`, `Comparable`         | Finite field Z/pZ (prime modulus)   |
| `Zm`            | `EuclideanRing`, `Comparable` | Integers mod m (any modulus)        |
| `ZmProduct`     | `Ring`                        | Direct product of Zm rings          |
| `ECpoint`       | `AbelianGroup`                | Elliptic curve points over Fp       |

Each base type implements specific **protocols** that define their algebraic behavior through method signatures.

## Type Constructors (Functor Layer)

These parameterized classes are **functors** that lift algebraic structures to more complex domains:

| Constructor          | Signature               | Result Protocol | Description                             |
|----------------------|-------------------------|-----------------|-----------------------------------------|
| `Matrix[T]`          | `Ring → Ring`           | `Ring`          | Matrix algebra over rings               |
| `Complex[T]`         | `Field → Field`         | `Field`         | Complex numbers over arbitrary fields   |
| `Fraction[T]`        | `EuclideanRing → Field` | `Field`         | Field of fractions (quotient field)     |
| `Polynomial[T]`      | `Ring → Ring`           | `Ring`          | Polynomial rings                        |
| `FieldPolynomial[T]` | `Field → EuclideanRing` | `EuclideanRing` | Polynomials over fields (with division) |

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
AbelianGroup          __bool__, zero()
    ↓
   Ring               __mul__, one()
    ↓
EuclideanRing         __floordiv__, __mod__, __divmod__, euclidean_function(), normalize()
    ↓
  Field               __truediv__, inverse()
```

**Comparable** forms an orthogonal hierarchy for ordered structures.

### Required Method Contracts

- **`normalize()`**: Maps associates to the same canonical form. Fields/units: `one()` if nonzero, `zero()` if zero. Integers: `abs(self)`. Polynomials over fields: divide by leading coefficient (monic).
- **`euclidean_function()`**: Returns `int`. Raises `ValueError` on zero. Fields: `1`. Integers: `abs(value)`. Polynomials: `degree()`.
- **`zero()`**: Instance method (not classmethod) for parameterized types, preserving instance parameters.
- **`__bool__()`**: Tests for non-zeroness. NativeFloat uses tolerance from `cockpit.params`.
- **GCD**: Free function in `util/primes.py` using the generic Euclidean algorithm. Not a method on types.

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

### Property Verification (`check_properties.py`)

The testing system validates algebraic axioms through composable check functions:

- **`check_abelian_group(samples)`**: Identity, inverse, commutativity, associativity of addition
- **`check_rings(samples)`**: All abelian group checks + multiplicative identity, associativity, commutativity, distributivity, annihilator
- **`check_euclidean_rings(samples)`**: All ring checks + division, divmod, GCD properties (divisibility, commutativity, associativity, identity)
- **`check_fields(samples)`**: All Euclidean ring checks + true division and inverse

### Sample Generation (`util/gen_samples.py`)

Factory functions create typed sample lists for testing:

- `def_nat_ints(...)`, `def_nat_floats(...)`, `def_nat_complex(...)` — base types
- `def_fractions(...)`, `def_polynomials(...)`, `def_field_polynomials(...)` — composite types

### Known Limitations

- Deep type towers over floats (e.g., `Fraction[FieldPolynomial[NativeFloat]]`) can fail associativity due to floating-point accumulation in polynomial GCD and cross-multiplication

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

### Fraction Simplification

The `Fraction` constructor divides numerator and denominator by their GCD directly (without normalizing the GCD first). This ensures that field-valued fractions (e.g., `Fraction[NativeFloat]`) actually simplify, preventing coefficient blowup in deep type towers.

## Usage Examples

### Basic Usage

```python
from py4alg.wrapper import NativeInt
from py4alg.mapper import Polynomial

# Create a polynomial ring over integers
P = Polynomial[NativeInt]
p = P([1, 2, 3])  # represents 1 + 2x + 3x²
q = P([4, 5])  # represents 4 + 5x

result = p * q  # polynomial multiplication
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

**py4alg** represents a new paradigm in computational algebra: a system where mathematical correctness, type safety, and
compositional flexibility converge to create an infinitely extensible, rigorously tested algebraic universe.
