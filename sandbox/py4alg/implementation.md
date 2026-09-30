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
|   |-- p_field.py              Field(EuclideanRing): __truediv__, inverse()
|   |-- p_comparable.py         Comparable: __lt__ (orthogonal)
|-- wrapper/
|   |-- __init__.py             (empty; nothing re-exported)
|   |-- w_int.py                NativeInt over int                 -> EuclideanRing + Comparable
|   |-- w_float.py              NativeFloat over float (tol eq)    -> Field + Comparable
|   |-- w_complex.py            NativeComplex over complex (tol eq) -> Field (no __lt__)
|   |-- s_int.py                SymbolicInt over sympy.Symbol      -> Ring + Comparable (no euclidean_function)
|-- mapper/
|   |-- __init__.py             re-exports Fp, Zm, ZmProduct, Polynomial, FieldPolynomial,
|   |                             Fraction, Complex, FieldComplex, Matrix, ECpoint
|   |-- m_polynomial.py         Polynomial[T:Ring], FieldPolynomial[T:Field](Polynomial[T])
|   |-- m_fraction.py           Fraction[T:EuclideanRing]
|   |-- m_complex.py            Complex[T:Ring], FieldComplex[T:Field](Complex[T])
|   |-- m_matrix.py             Matrix[T:Ring] (also builds block matrices), FieldMatrix[T:Field](Matrix[T])
|   |-- m_modular.py            Zm (mod m), Fp(Zm) (mod p)
|   |-- m_modular_product.py    ZmProduct via CRT
|   |-- m_ec.py                 ECpoint (elliptic curve points; AbelianGroup only)
|-- util/
    |-- __init__.py             (empty)
    |-- utils.py                compose(), take(), params dict, set_test_seed(), comparable_works(), descent_str()
    |-- primes.py               is_prime, gcd (generic), gcd_extended, mod_inverse, chinese_remainder, factorize, phi, ord, find_generator, lcm
    |-- gen_samples.py          infinite-iterator factories (gen_ints, gen_polynomials, ...) + CONSTRUCTORS, SOURCES, accepts(), gen_tree
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
            Field           (__truediv__, inverse)


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
- `inverse()` is part of the `Field` protocol (since 29.09.2026); the field property tests
  (`check_truediv_and_inverse`) rely on it.
- The test wrappers in `tests/py4alg/test_builtins.py` satisfy the full protocols (since
  29.09.2026): `IntWrapper` is a `EuclideanRing`, `FloatWrapper` and `ComplexWrapper` are
  `Field`s, and `test_any` runs `check_axioms` on all three.

## Wrappers (base types)

| Class           | Wraps                 | Protocols satisfied                                  | Notes                                                            |
|-----------------|-----------------------|------------------------------------------------------|------------------------------------------------------------------|
| `NativeInt`     | `int`                 | AbelianGroup, Ring, EuclideanRing, Comparable        | `zero`/`one` are `@classmethod`. Exact equality.                 |
| `NativeFloat`   | `float`               | AbelianGroup, Ring, EuclideanRing, Field, Comparable | Tolerance `__eq__` from `params['atol'/'rtol']`.                 |
| `NativeComplex` | `complex`             | AbelianGroup, Ring, EuclideanRing, Field             | Tolerance `__eq__`; no `__lt__` (correctly not Comparable).      |
| `SymbolicInt`   | `sympy.Symbol`/`Expr` | AbelianGroup, Ring (Comparable)                      | Experimental; no `euclidean_function` (Ring since 29.09.2026). |

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
| `Matrix[T]`                            | `T: Ring   -> Matrix[T]` (square only) | Ring                                             | Block matrix: `Matrix(Matrix, ...)` is a `Matrix[T]` over the entries |
| `FieldMatrix[T]` (`<: Matrix`)         | `T: Field  -> FieldMatrix[T]`          | Ring (+ `det`, `inverse`, `/`)                   | Block matrix (via parent)                                            |
| `Fp`                                   | parameterless (modulus is data)        | Field + Comparable                               | n/a                                                                  |
| `Zm`                                   | parameterless (modulus is data)        | EuclideanRing + Comparable                       | n/a                                                                  |
| `ZmProduct`                            | parameterless (moduli are data)        | Ring (zero divisors; `//` by units only)          | n/a                                                                  |
| `ECpoint`                              | parameterless (curve is data)          | AbelianGroup                                     | n/a                                                                  |

`Polynomial`, `Complex` and (since 29.09.2026) `Matrix` use `type(self)` when building
results, so the subclasses `FieldPolynomial`, `FieldComplex` and `FieldMatrix` propagate
through arithmetic. When a constructor flattens (or builds a block matrix), `descent()` starts
with the constructor's own class, not the argument's: `Polynomial(FieldPolynomial(...))` is a
`Polynomial` with descent `[Polynomial, T]`.

`FieldMatrix` is still a `Ring`: matrices do not commute and singular ones have no inverse.
`det()` uses Gaussian elimination, `inverse()` Gauss-Jordan elimination (`ZeroDivisionError` if
singular), `a / b == a * b.inverse()`. Pivots are the first nonzero entry of a column, so entries
only need `__bool__`; for floats there is no partial pivoting by magnitude.

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
- **`euclidean_function()`** raises `ValueError` on zero everywhere. `ZmProduct` and
  `SymbolicInt` have none: they are rings, not Euclidean rings (since 29.09.2026).
- **`normalize()`** is the canonical-associate function. Fields and units
  collapse to `one() if self else zero()`; `NativeInt` returns `abs`;
  `FieldPolynomial` makes monic; `Zm/Fp/FieldComplex/Fraction` use
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
   `pytest_terminal_summary` and written to a new file
   `reports/<YYYYMMDD-HHMMSS>_py4alg_exceptions_<host>.txt` per run, in
   `pytest_sessionfinish` — not in the terminal summary, which PyCharm's test runner never calls.

Samples are produced in two complementary styles:

- **Infinite iterators** (`util/gen_samples.py`): `gen_nat_ints`, `gen_fractions`,
  `gen_polynomials`, ... are `gen_make(Cls, min, max)`-wrapped generators that
  retry on `ZeroDivisionError`/`ValueError` and skip zero results.
  `gen_tree(sources, depth, n)` enumerates *all* compositional paths up to a fixed depth — the
  test-of-the-tower machinery of `test_axioms.py` and `test_descent.py`. A path starts with a
  source and its wrapper (`SOURCES`: `gen_ints → gen_nat_ints`, ...), then constructors from
  `CONSTRUCTORS`. Which constructor may follow is not tabulated but derived (since 29.09.2026):
  `accepts(cls, x)` is true if `x` satisfies the bound of `cls`'s type parameter
  (`Fraction[T: EuclideanRing]`), read at runtime from `cls.__type_params__`, or if `x` belongs to
  `cls` itself (flattening, block matrices). A new constructor only needs an entry in
  `CONSTRUCTORS`.
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
  `check_axioms` yet (plan, step 7).
- `test_descent.py` — `descent()` of every tower type, flattening, block matrices.
- `test_primes.py`, `test_gen_tools.py` — utility coverage.

## Floats: rational functions with float coefficients

Investigated 30.09.2026 with `test_axioms.py` at depth 4, N = 5, over ints, floats and complex.

**Finding.** 1,121 findings in the report, none over ints. All 1,117 violated axioms were in the 12
towers containing `Fraction > FieldPolynomial > NativeFloat/NativeComplex` (rational functions
with float coefficients): associativity of multiplication 544, distributivity 539, division and
divmod 24, a few others; matrices on top amplify them (up to 262 per tower). Plus 4 timeouts.

**Mechanisms**, found by tracing failing checks step by step:

1. *Division algorithm.* `FieldPolynomial.__divmod__` computed the eliminated coefficients as
   `r[n+k] - qk·b[n]`, mathematically 0, numerically a residue such as `1.8e-12`; it survived the
   trimming against the absolute `atol = 1e-12`, so the remainder had too high a degree, and the
   next gcd step divided by the residue (a "gcd" of `1.4e14`). **Fixed**: the remainder is cut to
   degree < n (`r[:n]`).
2. *The gcd over floats is ill-conditioned.* Whether a remainder counts as zero decides the gcd's
   degree, and a fixed `atol` misjudges both ways: remainders that should vanish do not (fractions
   stay less reduced), real ones are dropped (spurious common factors; `//` then silently discards
   a remainder and changes the fraction's value; degenerate denominators like `-1.1e-34`).
3. *Coefficient-wise equality.* Two correct but differently reduced representations have cross
   products that agree to about 1e-8 relative to their largest coefficient, but the small
   coefficients carry the same absolute error, up to 1.5e-5 relative to themselves — far above
   `rtol = 1e-9`: `NativeFloat.__eq__` measures each coefficient only against itself.

**Changes.**

- `Fraction` normalizes its denominator by its unit after the gcd reduction
  (`u = den // den.normalize()`): positive for integers, monic for polynomials over a field (keeps
  the coefficient scale near 1; floats drifted to 1e14 and 1e-10), `1` over a field. A canonical
  form in itself; it also made degenerate float denominators visible (`ZeroDivisionError`
  instead of silently wrong fractions).
- The divmod fix above.
- `gen_tree` no longer builds `Fraction` over polynomials with float coefficients
  (`INEXACT` in `accepts`). Mechanisms 2 and 3 would need an approximate gcd and scale-aware
  equality — substantial work and still heuristic; rational functions with float coefficients
  are a known weak spot of computer algebra. The same structure over exact coefficients
  (`Fraction > FieldPolynomial > Fraction > NativeInt`, over `Fp`) stays in the tower tests.

| `test_axioms.py`, depth 4, N = 5 | findings | of which timeouts |
|---|---|---|
| before | 1,121 | 4 |
| + canonical denominator | 978 | 5 |
| + divmod fix | 928 | 6 |
| + no `Fraction` over float polynomials | **5** | 5 |

The remaining 5 are timeouts of large block matrices over floats and complex (three nested block
steps give 27×27 matrices; associativity at N = 5 needs 125 triples), a performance matter.
`test_polynomials.py` and `test_many.py` still build such fractions by hand and report a few
violated axioms: they document the limitation.


## Plan

Phases 1 to 6 are done (29.09.2026; float findings 30.09.2026, see above; phases 1-2 in `roadmap.md`): strict `NativeFloat`, docs
corrected, a single `gcd` in `util/primes.py`, `inverse()` in the `Field` protocol, and
`ZmProduct` and `SymbolicInt` downgraded to `Ring`. The earlier suggestions S1, S2, S4 and S9 are
done or resolved; the second half of S6 (block-matrix `descent()`) was not an issue. Everything
still open is below; step numbers continue those of `roadmap.md`.

### Phase 3: protocols that tell the truth — done 29.09.2026

6. **`inverse()` is in the `Field` protocol.** `NativeFloat`, `NativeComplex`, `Fp`, `Fraction` and
   `FieldComplex` still pass `isinstance(x, Field)`.
7. **`ZmProduct` is a `Ring`.** `%` (which returned zero), `divmod`, `euclidean_function` and
   `normalize` are gone; `//` stays as division by units (`ZeroDivisionError` for zero divisors).
   `test_zm_product.py` asserts `not isinstance(z, EuclideanRing)`, checks ring axioms in its
   adapter tests and has a `check_axioms` test; the gcd and `%` tests are removed.
8. **`SymbolicInt` is a `Ring`** (and `Comparable`): `euclidean_function` (which only raised
   `NotImplementedError`) and `normalize` are gone; `//`, `%` and `divmod` stay (sympy's `floor`
   and `Mod`).

Result: the py4alg report went from 19 to 12 findings (the 6 `NotImplementedError`s and the
timeout of `SymbolicInt` are gone); 259 tests pass on the Mac and the Pi, with identical reports.
The remaining 12 are the known float towers `Fraction > FieldPolynomial > NativeFloat/NativeComplex`.

Also done in phase 3: the test wrappers in `test_builtins.py` got `euclidean_function()` (`abs`
for `IntWrapper`, `1` for the float and complex wrappers, `ValueError` on zero). Before, they
passed only as `Ring`, so their division, gcd and inverse axioms were never checked; and
`builtin_samples` listed the int samples three times, so the float and complex wrappers were not
tested at all. Now `check_axioms` runs the full Euclidean and field checks on all three; they pass.

### Phase 4: missing tests (S8) — done 29.09.2026

9. **`tests/py4alg/test_descent.py`**, for every tower of `gen_tree(depth=4)` over ints, floats and
   complex (255 sample lists, 147 distinct types): `descent()` is a nonempty list of classes,
   starts with `type(x)`, ends with a base type, is the same for all samples, never has a
   constructor directly on its own family (flattening), and equals `[type(x)] + descent()` of the
   components (coefficient, real part, numerator, matrix entry) all the way down.
10. **Explicit tests**: `Polynomial(p0, p1, ...) == p0 + p1·x + ...`, `Complex(a, b) == a + i·b`,
    `Fraction(a, b) == a / b`, likewise for `FieldPolynomial` and `FieldComplex`; no flattening
    across families; block matrices with 1-3 × 1-3 blocks of size 1-3 (entries in place,
    descent `[Matrix, T]`), block multiplication equals the flattened product, nested block
    matrices stay flat.

Result: 532 new tests, all pass (1.6 s); a deliberately planted error (block matrix with an extra
`Matrix` in its descent) made 48 of them fail. py4alg: 791 tests, report unchanged at 12 findings,
Mac and Pi identical.

### Phase 5: `Matrix` consistent, `FieldMatrix` (S6, S5) — done 29.09.2026

11. **`type(self)` in `Matrix`** for all results (`+`, `-`, `*`, negation, `zero`, `one`), for the
    descent and in `__repr__`. On the way: a block matrix took its descent from its first block,
    so `Matrix(FieldMatrix, ...)` claimed `[FieldMatrix, T]`; now `[type(self)] + T`. The same
    bug in the flattening branches of `Polynomial` and `Complex` is fixed as well
    (`Polynomial(FieldPolynomial(...))`, `Complex(FieldComplex, FieldComplex)`).
12. **`FieldMatrix[T: Field](Matrix[T])`** with `det()`, `inverse()` and `/` (see Mappers).
    `gen_field_matrices` follows every generator whose entries form a field, so the tower
    tests cover it: 4 new types in `test_axioms.py`, 32 in `test_descent.py`.
    `tests/py4alg/test_field_matrix.py`: protocols (Ring, not Field), type propagation, block
    matrices keep their class; `det()` equals the Leibniz formula (sizes 1-4, exact fields), is
    multiplicative, `det(1) = 1`, singular matrices have det 0 and no inverse, pivoting;
    `a·a⁻¹ = a⁻¹·a = 1` and `(a/b)·b = a` over `Fraction`, `Fp`, `NativeFloat` and `FieldComplex`.

Result: py4alg 959 tests (all pass on the Mac and the Pi), report unchanged at 12 findings.

### Phase 6: no table of type combinations (S7) — done 29.09.2026

13. **Derived instead of declared.** The plan was to declare input and output protocols as class
    attributes. That turned out to be unnecessary: the input protocol is the bound of the type
    parameter (`class Fraction[T: EuclideanRing]`), readable at runtime, and the output protocol
    is what `isinstance` says about a constructed element. `gen_tree` now probes one element of
    each partial path and extends it by every constructor that `accepts` it (bound, or own
    family); the hand-written `SUCCESSORS` table is gone. Compared with it, the derived rule adds
    what the table had left out (`Complex` over `NativeInt`, i.e. Z[i]; `Polynomial`, `Complex`,
    `Matrix` over `FieldComplex`; `Matrix` over `FieldMatrix`) and drops the wrapper self-loops
    (`NativeInt(NativeInt)`), which only produced duplicates: over ints 44 types (was 35), over
    floats and complex 86 each (was 74). All new towers pass the axioms; the report is unchanged.
14. **`protocols/p_table.py` is removed** (with `test_table.py`): a second, hand-written encoding
    of the same information, already wrong in places (`Fraction` over a `Ring`; no
    `FieldMatrix`). `test_gen_tools.py` tests `accepts` on the cases above and that every
    `gen_tree` path is constructible.

Result: py4alg 948 tests (all pass on the Mac and the Pi), report unchanged at 12 findings.

### Phase 7: symbolic wrappers (S10)

15. **`SymbolicFloat` / `SymbolicComplex`** over `sympy.Symbol(name, real=True)` /
    `sympy.Symbol(name)`, and `gen_sym_*` generators registered in `SOURCES`. Property tests over
    exact symbolic values give reproducible failures without the floating-point excuse.
