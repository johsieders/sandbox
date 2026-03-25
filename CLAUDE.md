# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python mathematical sandbox project containing AI-generated code (primarily from GPT 4.1) for mathematical
libraries and algorithms. The project demonstrates AI-assisted programming for rapid, mathematically sound library
development.

## Key Modules

### Step Functions (`sandbox/stepfunctions/`)

- **Primary file**: `stepfun.py` - Main step function implementation
- **Evolution**: `stepfun_n.py` files document progressive versions
- **Core concept**: Right-continuous step functions with (timestamp, value) pairs
- **Features**: Immutable, normalized, supports arithmetic operations, efficient N-ary operations
- **Tests**: `tests/stepfunctions/test_stepfun_f.py` (main test suite)

### Algebraic Structures (`sandbox/py4alg/`)

- **Architecture**: Protocol-based design with wrappers and mappers
- **Protocols** (`protocols/`): Abstract algebraic structures (Ring, Field, EuclideanRing, etc.)
- **Wrappers** (`wrapper/`): Native type wrappers (NativeInt, NativeFloat, NativeComplex)
- **Mappers** (`mapper/`): Complex algebraic types (Polynomial, FieldPolynomial, Matrix, Complex, Fraction, Fp, Zm, ZmProduct, ECpoint)
- **Configuration**: `cockpit.py` contains test parameters; `util/gen_samples.py` for sample generation
- **Key pattern**: Types use `_descent` attribute to track construction hierarchy

### Other Modules

- **Basics** (`sandbox/basics/`): Fundamental algorithms (sorting, heap, hanoi, etc.)
- **Interpreters** (`sandbox/interpreters/`): Formula parser, Forth interpreter
- **Tensors** (`sandbox/tensors/`): Tensor operations
- **Enigma** (`sandbox/enigma/`): Enigma machine simulation

## Development Commands

### Testing

```bash
# Run all tests
pytest

# Run specific test module
pytest tests/stepfunctions/test_stepfun_f.py
pytest tests/py4alg/test_polynomials.py

# Run tests with benchmark
pytest tests/ --benchmark-only
```

### Dependencies

Install requirements: `pip install -r requirements.txt`

Key dependencies: numpy, pandas, pytest, matplotlib, scikit-learn, torch, pytest-benchmark

## Architecture Patterns

### Protocol-Based Design

- Abstract algebraic structures defined as protocols in `protocols/`
- Concrete implementations in `wrapper/` (native types) and `mapper/` (complex types)
- Runtime type checking with `@runtime_checkable`

### Type System

- Uses Python 3.13+ generics syntax: `class Polynomial[T: Ring]`
- `_descent` attribute tracks type construction hierarchy
- Functor system maps algebraic properties through type constructors
- `Polynomial[T: Ring]` is the base ring; `FieldPolynomial[T: Field]` adds `//`, `%`, `divmod`, and `normalize`

### Key Conventions for Algebraic Types

- **`normalize()`**: Required by the `EuclideanRing` protocol. Must map associates to the same canonical form. For fields/units, return `one()` for nonzero, `zero()` for zero. For integers, return `abs(self)`. For polynomials over fields, make monic (divide by leading coefficient).
- **`euclidean_function()`**: Required by `EuclideanRing`. Returns an `int`. Must raise `ValueError` on zero. For fields return `1`; for integers return `abs(value)`; for polynomials return `degree()`.
- **`zero()`**: Must be an instance method (not classmethod) for parameterized types so it preserves the instance's parameters (e.g., curve parameters for ECpoint, modulus for Zm).
- **`__bool__()`**: Required by `AbelianGroup`. Tests for non-zeroness. Used for trailing-zero trimming in polynomials and for GCD termination.
- **`__eq__()`**: Fraction uses cross-multiplication (`a.num * b.den == a.den * b.num`), not `close_to`. NativeFloat uses tolerance-based comparison (configured via `cockpit.params`).
- **GCD**: Defined as a free function in `util/primes.py`, not as a method. Uses the generic Euclidean algorithm on any `EuclideanRing`. Commutativity depends on correct `normalize()`.
- **Fraction simplification**: The `Fraction` constructor divides numerator and denominator by their GCD directly (without normalizing the GCD first), so that field-valued fractions actually simplify.

### Testing Strategy

- **Property-based testing**: Tests mathematical axioms and invariants rather than specific expected values
- **Axiomatic approach**: `check_properties.py` verifies ring/field/Euclidean ring axioms (commutativity, associativity, distributivity, GCD properties)
- **Tolerance-based equality**: NativeFloat uses `atol`/`rtol` from `cockpit.params`; all other types use exact equality
- **Sample generation**: `util/gen_samples.py` provides factory functions (`def_nat_ints`, `def_nat_floats`, `def_polynomials`, `def_field_polynomials`, `def_fractions`, etc.)
- **Known limitation**: Deep type towers over floats (e.g., `Fraction[FieldPolynomial[NativeFloat]]`) can fail associativity due to floating-point accumulation in polynomial GCD and cross-multiplication

### Error Handling

- Step functions support "undefined" values (None, str) with Excel-style error propagation
- Non-numeric values propagate through operations

## Code Style

- Modern Python 3.13+ syntax
- Immutable data structures where possible
- Comprehensive docstrings with mathematical explanations
- Type hints throughout
- Generated code follows consistent patterns

## Performance Considerations

- Step functions use binary search for O(log n) evaluation
- Efficient N-ary operations via single-pass breakpoint merging
- Normalized canonical forms eliminate redundant breakpoints
- Test suite runs in ~15 seconds on MacBook Air M4
