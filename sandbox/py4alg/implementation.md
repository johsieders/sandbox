# py4alg — Implementation

## Overview

`py4alg` is a compositional algebra library that builds arbitrary tower types (polynomials, fractions, matrices, complex
numbers, finite fields, ...) on top of
a tiny stack of `@runtime_checkable` protocols. The driving idea is that
algebraic structure is carried by methods (`__add__`, `one()`, `normalize()`, ...)
rather than by classes, and that **type constructors are functors**: applying
`Polynomial`, `Fraction`, `Matrix`, ... to a type that already satisfies a
protocol produces a new type whose protocol can be inferred from the input.

Concretely the library lets you write:

```python
Fraction[FieldPolynomial[Fraction[NativeInt]]]  # rational functions over Q
Matrix[Polynomial[Complex[Fraction[NativeInt]]]]
```

and have `isinstance(x, Field)` / `isinstance(x, Ring)` answer correctly at
runtime. Mathematical axioms (ring/field/Euclidean ring) are checked by a
property suite (`../../tests/py4alg/check_protocols.py`) that is itself protocol-aware
— it picks the relevant axioms from `isinstance(samples[0], Field|EuclideanRing|Ring)`.

## Directory layout

```
sandbox/py4alg/
|-- __init__.py                 (empty)
|-- README.md                   long-form design narrative
|-- implementation.md           this file: structure, conventions, open plan
|-- roadmap.md                  earlier plan (R1-R7, March 2026) and its status as of 29.09.2026
|-- testing.md                  open todos for the test suite
|-- protocols/
|   |-- __init__.py             (empty)
|   |-- p_abelian_group.py      AbelianGroup: + - neg, ==, __bool__, zero()
|   |-- p_ring.py               Ring(AbelianGroup): __mul__, one()
|   |-- p_euclidean_ring.py     EuclideanRing(Ring): __floordiv__, __mod__, __divmod__, euclidean_function(), normalize()
|   |-- p_field.py              Field(EuclideanRing): __truediv__
|   |-- p_comparable.py         Comparable: __lt__ (orthogonal)
|   |-- p_table.py              experimental Mtype/protocol-transition table (unused outside this file)
|-- wrapper/
|   |-- __init__.py             (empty; nothing re-exported)
|   |-- w_int.py                NativeInt over int                 -> EuclideanRing + Comparable
|   |-- w_float.py              NativeFloat over float (tol eq)    -> Field + Comparable
|   |-- w_complex.py            NativeComplex over complex (tol eq) -> Field (no __lt__)
|   |-- s_int.py                SymbolicInt over sympy.Symbol      -> Ring/EuclideanRing (euclidean_function raises NotImplementedError)
|-- mapper/
|   |-- __init__.py             re-exports Fp, Zm, ZmProduct, Polynomial, FieldPolynomial,
|   |                             Fraction, Complex, FieldComplex, Matrix, ECpoint
|   |-- m_polynomial.py         Polynomial[T:Ring], FieldPolynomial[T:Field](Polynomial[T])
|   |-- m_fraction.py           Fraction[T:EuclideanRing]
|   |-- m_complex.py            Complex[T:Ring], FieldComplex[T:Field](Complex[T])
|   |-- m_matrix.py             Matrix[T:Ring] (also acts as block-matrix / tensor product)
|   |-- m_modular.py            Zm (mod m), Fp(Zm) (mod p)
|   |-- m_modular_product.py    ZmProduct via CRT
|   |-- m_ec.py                 ECpoint (elliptic curve points; AbelianGroup only)
|-- util/
    |-- __init__.py             (empty)
    |-- utils.py                compose(), take(), params dict, set_test_seed(), comparable_works(), descent_str()
    |-- primes.py               is_prime, gcd (generic), gcd_extended, mod_inverse, chinese_remainder, factorize, phi, ord, find_generator, lcm
    |-- gen_samples.py          infinite-iterator factories (gen_ints, gen_polynomials, ...) + SUCCESSORS table + gen_tree
    |-- def_samples.py          finite list factories (def_nat_ints, def_polynomials, ...) + to_pairs, to_coeffs
```

`../../tests/py4alg` contains `check_protocols.py` (the axiom suite), `conftest.py`
(report aggregation across xdist workers), and one `test_*.py` per concept.

## Protocol hierarchy

```
        AbelianGroup        (+, -, neg, ==, __bool__, zero)
              |
             Ring           (* , one)
              |
        EuclideanRing       (__floordiv__, __mod__, __divmod__,
              |              euclidean_function, normalize)
            Field           (__truediv__)


        Comparable          (__lt__)      -- orthogonal, lifted at runtime
                                              via comparable_works(sample)
```

All protocols are `@runtime_checkable`, so `isinstance(x, Ring)` is the only
discriminator used by the property suite. `Comparable` is intentionally not in
the inheritance chain — it is added a la carte and detected by trying
`sample <= sample` at runtime (`util/utils.py:56`).

Notes:

- `Field` is declared as a subclass of `EuclideanRing` (not `Ring`), so every
  field automatically supplies `__floordiv__ = __truediv__`, `__mod__ = 0`,
  `euclidean_function = 1`. All field implementations honour this convention.
- `inverse()` is **not** part of the `Field` protocol but is required by the
  field property tests (`check_truediv_and_inverse`). Every concrete field
  provides it, but the contract is implicit.

## Wrappers (base types)

| Class           | Wraps                 | Protocols satisfied                                  | Notes                                                            |
|-----------------|-----------------------|------------------------------------------------------|------------------------------------------------------------------|
| `NativeInt`     | `int`                 | AbelianGroup, Ring, EuclideanRing, Comparable        | `zero`/`one` are `@classmethod`. Exact equality.                 |
| `NativeFloat`   | `float`               | AbelianGroup, Ring, EuclideanRing, Field, Comparable | Tolerance `__eq__` from `params['atol'/'rtol']`.                 |
| `NativeComplex` | `complex`             | AbelianGroup, Ring, EuclideanRing, Field             | Tolerance `__eq__`; no `__lt__` (correctly not Comparable).      |
| `SymbolicInt`   | `sympy.Symbol`/`Expr` | AbelianGroup, Ring, EuclideanRing (Comparable)       | Experimental; `euclidean_function` raises `NotImplementedError`. |

All wrappers expose `descent()` returning `[Cls]` and raise `TypeError` on foreign input
(`NativeFloat(1)` is rejected like `NativeInt(1.0)`; since 29.09.2026).

## Mappers (type constructors)

| Class                                  | Type signature                         | Resulting protocol                               | Idempotent?                                                          |
|----------------------------------------|----------------------------------------|--------------------------------------------------|----------------------------------------------------------------------|
| `Polynomial[T]`                        | `T: Ring   -> Polynomial[T]`           | Ring                                             | Yes (flattens nested polys via Horner-style coefficient combination) |
| `FieldPolynomial[T]` (`<: Polynomial`) | `T: Field -> FieldPolynomial[T]`       | EuclideanRing (not Field; `truediv` not defined) | Yes (via parent)                                                     |
| `Fraction[T]`                          | `T: EuclideanRing -> Fraction[T]`      | Field                                            | Yes (cross-multiplies on `Fraction(Fraction)`)                       |
| `Complex[T]`                           | `T: Ring   -> Complex[T]`              | Ring                                             | Yes (collapses nested Complex via Gauss identity in `__init__`)      |
| `FieldComplex[T]` (`<: Complex`)       | `T: Field  -> FieldComplex[T]`         | Field                                            | Yes (via parent)                                                     |
| `Matrix[T]`                            | `T: Ring   -> Matrix[T]` (square only) | Ring                                             | No — `Matrix(Matrix, ...)` builds a block matrix (Kronecker-like)    |
| `Fp`                                   | parameterless (modulus is data)        | Field + Comparable                               | n/a                                                                  |
| `Zm`                                   | parameterless (modulus is data)        | EuclideanRing + Comparable                       | n/a                                                                  |
| `ZmProduct`                            | parameterless (moduli are data)        | Ring (claimed)                                   | n/a                                                                  |
| `ECpoint`                              | parameterless (curve is data)          | AbelianGroup                                     | n/a                                                                  |

Both `Polynomial.__init__` and `Complex.__init__` use `type(self)` when building
the result, so the subclasses `FieldPolynomial` and `FieldComplex` propagate
through arithmetic — a clean trick. `Matrix.__init__`, however, always returns
a `Matrix` (no `type(self)`), so subclassing would lose information; right now
no subclass exists, but the inconsistency is worth noting.

## Cross-cutting conventions

- **`descent()`** is the runtime construction trace, e.g.
  `Fraction(Polynomial(NativeInt(1)), ...).descent() == [Fraction, Polynomial, NativeInt]`.
  Every type implements it (since 28.09.2026 also `Zm`, `Fp`, `ZmProduct`, `ECpoint`, which
  return `[Cls]`). A block matrix `Matrix(m1, m2, m3, m4)` is flattened into a matrix over the
  blocks' scalars, so its descent is `[Matrix, T]`, which is correct.
- **`zero()`/`one()`** are instance methods on every parameterised type so they
  preserve type parameters (modulus for `Zm`/`Fp`, curve for `ECpoint`, etc.),
  but they are `@classmethod` on `NativeInt`, `NativeFloat`, `NativeComplex`,
  `SymbolicInt`. The protocol does not enforce one or the other.
- **`euclidean_function()`** raises `ValueError` on zero everywhere except in
  `SymbolicInt` (which raises `NotImplementedError`).
- **`normalize()`** is the canonical-associate function. Fields and units
  collapse to `one() if self else zero()`; `NativeInt` returns `abs`;
  `FieldPolynomial` makes monic; `Zm/Fp/ZmProduct/FieldComplex/Fraction` use
  the field-style rule. `Polynomial` (the ring-only version) has **no**
  `normalize()` — consistent with its `Ring` protocol, but it makes
  `gcd` over `Polynomial[NativeInt]` unable to take advantage of normalization (and indeed
  `test_polynomials.test_gcd_basics` only checks `Polynomial[int]`
  for ring axioms).
- **`__bool__()`** is required by `AbelianGroup`. `Polynomial.__bool__` returns
  `bool(self._coeffs[-1])` (always trimmed, so equivalent to non-zero); the
  alternative form on the commented line is more conservative. `NativeFloat`
  uses tolerance equality through `not self == self.zero()`.
- **Equality**: `NativeFloat`/`NativeComplex` use absolute+relative tolerance
  with `params['atol']`, `params['rtol']`. `Fraction.__eq__` uses
  `a.num*b.den == a.den*b.num` so it inherits whatever equality the underlying
  ring uses. All other types use structural equality.
- **GCD** is a single free function in `util/primes.py` (since 29.09.2026 the only one; the
  `hasattr(a, 'gcd')` dispatch, `FieldPolynomial.gcd` and the test wrappers' `gcd` are gone):
  ```python
  def gcd[T: EuclideanRing](a, b):
      while b:
          a, b = b, a % b
      return a
  ```
  It does **not** normalize, so `gcd(a, b)` and `gcd(b, a)` may differ by a unit; that is why
  the gcd checks in `check_protocols.py` normalize both results before comparing. Normalizing the
  running remainder (the old `FieldPolynomial.gcd`) was measured and dropped: with the plain loop
  the py4alg report has 19 findings instead of 30 (fewer in the float towers), with normalized
  remainders 29 — and plain ints, which `primes.gcd` also serves, have no `normalize()`.
- **Idempotent constructors** (`Polynomial`, `Complex`, `Fraction`) detect
  `isinstance(args[0], Cls)` and flatten. `Matrix` instead treats a sequence of
  matrix blocks as a block matrix — this is documented but easy to forget.

## Testing approach

`../../tests/py4alg/check_protocols.py` defines one function per axiom:

| Layer         | Functions                                                                                                                                                                                                            |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AbelianGroup  | `check_additive_identity`, `check_additive_inverse`, `check_commutativity_addition`, `check_associativity_addition`, `check_bulk_add`                                                                                |
| Ring          | + `check_multiplicative_identity`, `check_associativity_multiplication`, `check_commutativity_multiplication`, `check_annihilator_properties`, `check_left/right_distributivity`, `check_bulk_mul`                   |
| EuclideanRing | + `check_division` (verifies `a == q*b+r` and `r.euclidean_function() < b.euclidean_function()`), `check_divmod`, `check_gcd_properties`, `check_gcd_commutativity`, `check_gcd_associativity`, `check_gcd_identity` |
| Field         | + `check_truediv_and_inverse`, `check_field_division_by_zero`                                                                                                                                                        |
| Comparable    | `check_reflexivity`, `check_antisymmetry`, `check_transitivity`, `check_totality`, `check_comparison_consistency`                                                                                                    |

The entry point is `check_axioms(samples)` which:

1. Picks the strongest matching protocol via
   `isinstance(samples[0], Field|EuclideanRing|Ring|AbelianGroup)` (abelian groups since
   28.09.2026, e.g. `ECpoint`).
2. Adds `Comparable` checks iff `comparable_works(samples[0])` returns `True`.
3. Reports instead of failing: a violated axiom or a numerical problem (`GRACEFUL`:
   AssertionError, ArithmeticError, ValueError, NotImplementedError, RecursionError) is recorded
   per case and the loop continues; any other exception is recorded under the check's name by the
   `@graceful` decorator and the next check runs; a pytest-timeout is recorded as `timeout`.
   Records go to the module-level `exception_report`; the `black_box` deque stores the last
   5 sample descents to survive hangs.
4. Both lists are aggregated across xdist workers in `conftest.py`, printed in
   `pytest_terminal_summary` and written to `reports/py4alg_exceptions_<host>.txt`.

Samples are produced in two complementary styles:

- **Infinite iterators** (`util/gen_samples.py`): `gen_nat_ints`, `gen_fractions`,
  `gen_polynomials`, ... are `gen_make(Cls, min, max)`-wrapped generators that
  retry on `ZeroDivisionError`/`ValueError` and skip zero results. A
  `SUCCESSORS` adjacency table plus `gen_tree(sources, depth, n)` enumerates *all* compositional paths up to a fixed
  depth — this is the test-of-the-tower
  machinery used by `test_axioms.py`.
- **Finite list factories** (`util/def_samples.py`): `def_nat_ints(*nn)` etc.
  for deterministic, small, debuggable samples used in
  `test_polynomials.test_gcd_basics`, `test_poly_gcd`, etc.

Coverage at a glance:

- `test_natives.py`, `test_builtins.py`, `test_complex.py`, `test_fractions.py`,
  `test_polynomials.py`, `test_many.py`, `test_matrices.py`, `test_fp.py`,
  `test_zm.py`, `test_zm_product.py`, `test_ec.py`, `test_symbolics.py` — one
  per concept, each producing homogeneous sample sequences and calling
  `check_axioms`.
- `test_axioms.py` is the “tower” test that enumerates compositions through
  `gen_tree` up to depth 4, currently only for the `gen_ints` source (float and complex
  sources are commented out — the known floating-point associativity failures
  under "Known Limitations" in `README.md`). `test_zm_product.py` does not call
  `check_axioms` yet (plan, step 7); `test_table.py` prints the `p_table.py` successors.
- `test_primes.py`, `test_gen_tools.py` — utility coverage.

## Plan

Phases 1 and 2 are done (29.09.2026; details in `roadmap.md`): strict `NativeFloat`, docs
corrected, and a single `gcd` in `util/primes.py`. The earlier suggestions S1, S2, S4 and S9 are
done or resolved; the second half of S6 (block-matrix `descent()`) was not an issue. Everything
still open is below; step numbers continue those of `roadmap.md`.

### Phase 3: protocols that tell the truth

6. **`inverse()` into the `Field` protocol** (S3). `check_truediv_and_inverse` calls
   `a.inverse()` on every field sample, and every field (`NativeFloat`, `NativeComplex`, `Fp`,
   `Fraction`, `FieldComplex`, the test wrappers) already has it, but `Field` declares only
   `__truediv__`. Check afterwards that all fields still pass `isinstance(x, Field)`.
7. **`ZmProduct` is no Euclidean ring.** It has `//`, `%`, `normalize()` and
   `euclidean_function()`, so it passes `isinstance(x, EuclideanRing)`, but Z₃×Z₅ has zero
   divisors, and `check_division`/`check_divmod` fail with `ZeroDivisionError`. Downgrade to
   `Ring` (drop `//`, `%`, `divmod`, `euclidean_function`, `normalize`) and give
   `test_zm_product.py` a `check_axioms` test (S8). *Decision needed.*
8. **`SymbolicInt`**: `euclidean_function` raises `NotImplementedError` (6 findings in the report,
   plus one timeout). Either a real, degree-based `euclidean_function` (cf. phase 7) or a
   downgrade to `Ring`. *Decision needed.*

### Phase 4: missing tests (S8)

9. **`test_descent.py`**: `descent()` is a flat list of classes of the right length for every type
   of `gen_tree(depth=4)`; flattening invariants of `Polynomial`, `Complex`, `Fraction`
   (`Fraction(Fraction(x)).descent() == Fraction(x).descent()`); block-matrix semantics.
10. **Explicit tests** for `Complex(Complex)` flattening and for block matrices with varied block
    sizes (`test_matrices.test_matrix_matrix` uses one size).

### Phase 5: `Matrix` consistent, `FieldMatrix` (S6, S5)

11. **`type(self)` instead of `Matrix(...)`** in `mapper/m_matrix.py` (6 places), as in
    `Polynomial` and `Complex`, so that subclasses propagate through arithmetic.
12. **`FieldMatrix[T: Field](Matrix[T])`** with `inverse()`, `det()` and Gauss-Jordan
    `__truediv__` — the ring-class-plus-field-subclass pattern of `Polynomial`/`FieldPolynomial`
    and `Complex`/`FieldComplex`, and linear algebra over any field. Needs step 6.

### Phase 6: one table of type combinations (S7)

13. **Mappers declare their signature**: input protocol, output protocol, flattening (class
    attributes); `SUCCESSORS` in `util/gen_samples.py` is derived from them instead of being
    written by hand.
14. **`protocols/p_table.py`** (an experimental second encoding of the same idea) becomes the
    single source of truth or is removed. New mappers (`FieldMatrix`, symbolic types) then plug
    into the axiom tests and the docs automatically.

### Phase 7: symbolic wrappers (S10)

15. **`SymbolicFloat` / `SymbolicComplex`** over `sympy.Symbol(name, real=True)` /
    `sympy.Symbol(name)`, and `gen_sym_*` generators in the table of phase 6. Property tests over
    exact symbolic values give reproducible failures without the floating-point excuse.

### Decisions needed

- `ZmProduct`: downgrade to `Ring` (step 7)?
- `SymbolicInt`: real `euclidean_function`, or downgrade to `Ring` (step 8)?
