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
- **Configuration**: the `params` dict in `util/utils.py` (tolerances `atol`/`rtol`, sample sizes, seed); samples from `util/gen_samples.py` (infinite generators, `gen_tree`) and `util/def_samples.py` (finite lists)
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

# Benchmarks: disabled by default (addopts), i.e. benchmarked tests run once as plain tests.
# Measure (without -n auto); --benchmark-autosave keeps runs in .benchmarks/ for --benchmark-compare
pytest tests/py4alg/test_axioms_bench.py --benchmark-enable --benchmark-only --benchmark-sort=mean

# Exploratory print output of passed tests: -rP (or -s without -n auto).
# tests/py4alg writes its exception report to reports/py4alg_exceptions_<host>.txt
```

### Dependencies

Python 3.14.7 on Mac, Pi and Windows, managed by uv and pinned in `.python-version`. Dependencies are declared in
`pyproject.toml` (test tools in the `dev` group) and pinned in `uv.lock`; commit both together.

- Install / update the venv: `uv sync` (creates `.venv`, installs exact locked versions, editable `sandbox`)
- Add a dependency: `uv add <pkg>` (test tool: `uv add --dev <pkg>`); upgrade: `uv lock --upgrade && uv sync`
- On the Pi: after syncing the mirror, `bash ~/sandbox/remote-setup.sh` (runs `uv sync --locked`)
- torch via `[tool.uv.sources]`: PyPI build on the Mac (MPS), CPU-only build on Linux/Pi, CUDA 13.0 (`cu130`) on Windows

Mac/Pi 5 setup (Pi `~/sandbox` is a git-free mirror, never edit/pull there; run `tools/sync_pi.sh`
after edits made outside PyCharm; `python tools/check_pi.py` checks the whole setup, e.g. after a reconnect;
the Pi is the SSH alias `pi5`): see `docs/multi_platform.md`.

Windows PC (Intel, NVIDIA GPU; `docs/multi_platform.md` §10): its own git clone from GitHub, same uv
environment via `uv sync` (torch `2.14.0+cu130`), no mirroring, no Pi access — the Mac/Pi scripts
(`sync_pi.sh`, `check_pi.py`, `compare_hosts.py`, `remote-setup.sh`) are not used there. Two clones
now: pull before working; after a `git pull` on the Mac, run `tools/sync_pi.sh`. `.gitattributes` keeps
`*.sh` LF. On Windows pytest-timeout has no SIGALRM and ends the process on a timeout, so
`check_axioms` cannot report it as a graceful `timeout`.

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
- **Idempotent (flattening) constructors**: `Polynomial`, `Complex`, and `Fraction` flatten when applied to their own type (e.g., `Fraction(Fraction)` → `Fraction`). `Matrix` builds a block matrix instead: `Matrix(m1, m2, m3, m4)` with n×n blocks is a 2n×2n matrix over the blocks' scalars (so its `descent()` stays `[Matrix, T]`).

### Key Conventions for Algebraic Types

- **`normalize()`**: Required by the `EuclideanRing` protocol. Must map associates to the same canonical form. For fields/units, return `one()` for nonzero, `zero()` for zero. For integers, return `abs(self)`. For polynomials over fields, make monic (divide by leading coefficient).
- **`euclidean_function()`**: Required by `EuclideanRing`. Returns an `int`. Must raise `ValueError` on zero. For fields return `1`; for integers return `abs(value)`; for polynomials return `degree()`.
- **`zero()`**: Must be an instance method (not classmethod) for parameterized types so it preserves the instance's parameters (e.g., curve parameters for ECpoint, modulus for Zm).
- **`__bool__()`**: Required by `AbelianGroup`. Tests for non-zeroness. Used for trailing-zero trimming in polynomials and for GCD termination.
- **`__eq__()`**: Fraction uses cross-multiplication (`a.num * b.den == a.den * b.num`), not `close_to`. NativeFloat uses tolerance-based comparison (configured via `params` in `util/utils.py`).
- **GCD**: Defined as a free function in `util/primes.py`, not as a method. Uses the generic Euclidean algorithm on any `EuclideanRing`. Commutativity depends on correct `normalize()`.
- **Fraction simplification**: The `Fraction` constructor divides numerator and denominator by their GCD directly (without normalizing the GCD first), so that field-valued fractions actually simplify.

### Testing Strategy

- **Property-based testing**: Tests mathematical axioms and invariants rather than specific expected values
- **Axiomatic approach**: `tests/py4alg/check_protocols.py` verifies ring/field/Euclidean ring axioms (commutativity, associativity, distributivity, GCD properties)
- **Tolerance-based equality**: NativeFloat/NativeComplex use `atol`/`rtol` from `params` in `util/utils.py`; all other types use exact equality
- **Sample generation**: `util/gen_samples.py` provides infinite generators (`gen_ints`, `gen_polynomials`, …) and `gen_tree`; `util/def_samples.py` provides finite lists (`def_nat_ints`, `def_nat_floats`, `def_polynomials`, `def_field_polynomials`, `def_fractions`, etc.)
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
- The full suite has ~31,200 tests (~30,000 of them parametrized step function tests); with `pytest -n auto` it takes
  about 1 minute on the Mac (MacBook Air M4) and about 3 minutes on the Pi; `tests/py4alg` alone ≈ 10 s on the Mac
