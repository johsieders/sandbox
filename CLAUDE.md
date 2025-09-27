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
- **Mappers** (`mapper/`): Complex algebraic types (Polynomial, Matrix, Complex, Fraction, Fp)
- **Configuration**: `cockpit.py` contains all test parameters and sample generation
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

### Testing Strategy

- **Property-based testing**: Tests mathematical axioms and invariants rather than specific expected values
- **Axiomatic approach**: Ring/field axioms, commutativity, associativity, distributivity
- **Tolerance-based equality**: Uses `close_to` predicate for numerical stability
- **Sample generation**: Centralized in `cockpit.py` with configurable parameters

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
