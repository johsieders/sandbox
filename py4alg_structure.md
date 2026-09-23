# py4alg — Structure and Suggested Improvements

## Overview

`py4alg` is a compositional algebra library that builds arbitrary tower types
(polynomials, fractions, matrices, complex numbers, finite fields, ...) on top of
a tiny stack of `@runtime_checkable` protocols. The driving idea is that
algebraic structure is carried by methods (`__add__`, `one()`, `normalize()`, ...)
rather than by classes, and that **type constructors are functors**: applying
`Polynomial`, `Fraction`, `Matrix`, ... to a type that already satisfies a
protocol produces a new type whose protocol can be inferred from the input.

Concretely the library lets you write:

```python
Fraction[Polynomial[NativeInt]]            # rational functions over Z
Matrix[Polynomial[Complex[Fraction[NativeInt]]]]
```

and have `isinstance(x, Field)` / `isinstance(x, Ring)` answer correctly at
runtime. Mathematical axioms (ring/field/Euclidean ring) are checked by a
property suite (`tests/py4alg/check_protocols.py`) that is itself protocol-aware
— it picks the relevant axioms from `isinstance(samples[0], Field|EuclideanRing|Ring)`.

## Directory layout

```
sandbox/py4alg/
|-- __init__.py                 (empty)
|-- README.md                   long-form design narrative
|-- roadmap.md                  open todos (gcd cleanup, Polynomial vs FieldPolynomial split, prefixes...)
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

`tests/py4alg/` contains `check_protocols.py` (the axiom suite), `conftest.py`
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

| Class           | Wraps      | Protocols satisfied                          | Notes                                                                 |
|-----------------|------------|----------------------------------------------|-----------------------------------------------------------------------|
| `NativeInt`     | `int`      | AbelianGroup, Ring, EuclideanRing, Comparable| `zero`/`one` are `@classmethod`. Exact equality.                      |
| `NativeFloat`   | `float`    | AbelianGroup, Ring, EuclideanRing, Field, Comparable | Tolerance `__eq__` from `params['atol'/'rtol']`.              |
| `NativeComplex` | `complex`  | AbelianGroup, Ring, EuclideanRing, Field     | Tolerance `__eq__`; no `__lt__` (correctly not Comparable).           |
| `SymbolicInt`   | `sympy.Symbol`/`Expr` | AbelianGroup, Ring, EuclideanRing (Comparable) | Experimental; `euclidean_function` raises `NotImplementedError`. |

All wrappers expose `descent()` returning `[Cls]`. `NativeFloat.__init__` is
silent on bad input (no raise on unknown type); the other wrappers raise
`TypeError`.

## Mappers (type constructors)

| Class             | Type signature                         | Resulting protocol            | Idempotent? |
|-------------------|----------------------------------------|-------------------------------|-------------|
| `Polynomial[T]`   | `T: Ring   -> Polynomial[T]`           | Ring                          | Yes (flattens nested polys via Horner-style coefficient combination) |
| `FieldPolynomial[T]` (`<: Polynomial`) | `T: Field -> FieldPolynomial[T]` | EuclideanRing (not Field; `truediv` not defined) | Yes (via parent) |
| `Fraction[T]`     | `T: EuclideanRing -> Fraction[T]`      | Field                         | Yes (cross-multiplies on `Fraction(Fraction)`) |
| `Complex[T]`      | `T: Ring   -> Complex[T]`              | Ring                          | Yes (collapses nested Complex via Gauss identity in `__init__`)      |
| `FieldComplex[T]` (`<: Complex`) | `T: Field  -> FieldComplex[T]` | Field                         | Yes (via parent)  |
| `Matrix[T]`       | `T: Ring   -> Matrix[T]` (square only) | Ring                          | No — `Matrix(Matrix, ...)` builds a block matrix (Kronecker-like)    |
| `Fp`              | parameterless (modulus is data)         | Field + Comparable            | n/a         |
| `Zm`              | parameterless (modulus is data)         | EuclideanRing + Comparable    | n/a         |
| `ZmProduct`       | parameterless (moduli are data)         | Ring (claimed)                | n/a         |
| `ECpoint`         | parameterless (curve is data)           | AbelianGroup                  | n/a         |

Both `Polynomial.__init__` and `Complex.__init__` use `type(self)` when building
the result, so the subclasses `FieldPolynomial` and `FieldComplex` propagate
through arithmetic — a clean trick. `Matrix.__init__`, however, always returns
a `Matrix` (no `type(self)`), so subclassing would lose information; right now
no subclass exists, but the inconsistency is worth noting.

## Cross-cutting conventions

- **`descent()`** is the runtime construction trace, e.g.
  `Fraction(Polynomial(NativeInt(1)), ...).descent() == [Fraction, Polynomial, NativeInt]`.
  It is **only** implemented on the four wrappers and on `Polynomial`,
  `FieldPolynomial`, `Fraction`, `Complex`, `FieldComplex`, `Matrix`.
  **`Zm`, `Fp`, `ZmProduct`, and `ECpoint` do not implement `descent()`** — so
  `descent_str(samples)` (`util/utils.py:64`) will crash on these types and the
  axiom report cannot label their failures. This is an outright gap.
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
  `gcd` over `Polynomial[NativeInt]` unable to take advantage of normalization
  (and indeed `test_polynomials.test_gcd_basics` only checks `Polynomial[int]`
  for ring axioms).
- **`__bool__()`** is required by `AbelianGroup`. `Polynomial.__bool__` returns
  `bool(self._coeffs[-1])` (always trimmed, so equivalent to non-zero); the
  alternative form on the commented line is more conservative. `NativeFloat`
  uses tolerance equality through `not self == self.zero()`.
- **Equality**: `NativeFloat`/`NativeComplex` use absolute+relative tolerance
  with `params['atol']`, `params['rtol']`. `Fraction.__eq__` uses
  `a.num*b.den == a.den*b.num` so it inherits whatever equality the underlying
  ring uses. All other types use structural equality.
- **GCD** is a free function in `util/primes.py`:
  ```python
  def gcd[T: EuclideanRing](a, b):
      if hasattr(a, 'gcd'):
          return a.gcd(b)
      while b:
          a, b = b, a % b
      return a
  ```
  The `hasattr(a, 'gcd')` dispatch exists solely so that
  `FieldPolynomial.gcd` (a stabilised, monic-at-each-step variant) is picked up
  — but the roadmap (`roadmap.md` item 1) explicitly says this should go away.
  The fallback does **not** normalize at the end, which makes
  `gcd(a, b)` and `gcd(b, a)` differ by a unit; that is why
  `check_gcd_commutativity` (`check_protocols.py:215`) normalises both
  results before comparing.
- **Idempotent constructors** (`Polynomial`, `Complex`, `Fraction`) detect
  `isinstance(args[0], Cls)` and flatten. `Matrix` instead treats a sequence of
  matrix blocks as a block matrix — this is documented but easy to forget.

## Testing approach

`tests/py4alg/check_protocols.py` defines one function per axiom:

| Layer | Functions |
|-------|-----------|
| AbelianGroup | `check_additive_identity`, `check_additive_inverse`, `check_commutativity_addition`, `check_associativity_addition`, `check_bulk_add` |
| Ring          | + `check_multiplicative_identity`, `check_associativity_multiplication`, `check_commutativity_multiplication`, `check_annihilator_properties`, `check_left/right_distributivity`, `check_bulk_mul` |
| EuclideanRing | + `check_division` (verifies `a == q*b+r` and `r.euclidean_function() < b.euclidean_function()`), `check_divmod`, `check_gcd_properties`, `check_gcd_commutativity`, `check_gcd_associativity`, `check_gcd_identity` |
| Field         | + `check_truediv_and_inverse`, `check_field_division_by_zero` |
| Comparable    | `check_reflexivity`, `check_antisymmetry`, `check_transitivity`, `check_totality`, `check_comparison_consistency` |

The entry point is `check_axioms(samples)` which:

1. Picks the strongest matching protocol via `isinstance(samples[0], Field|EuclideanRing|Ring)`.
2. Adds `Comparable` checks iff `comparable_works(samples[0])` returns `True`.
3. Wraps each axiom in `try/except (AssertionError, ZeroDivisionError, ...)` and
   appends failures to the module-level `exception_report`. The companion
   `black_box` deque stores the last 5 sample descents to survive timeouts.
4. Both lists are aggregated across xdist workers in `conftest.py` and dumped
   in `pytest_terminal_summary`.

Samples are produced in two complementary styles:

- **Infinite iterators** (`util/gen_samples.py`): `gen_nat_ints`, `gen_fractions`,
  `gen_polynomials`, ... are `gen_make(Cls, min, max)`-wrapped generators that
  retry on `ZeroDivisionError`/`ValueError` and skip zero results. A
  `SUCCESSORS` adjacency table plus `gen_tree(sources, depth, n)` enumerates
  *all* compositional paths up to a fixed depth — this is the test-of-the-tower
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
  `gen_tree`, currently only for the `gen_ints` source (float and complex
  sources are commented out — the known floating-point associativity failures
  mentioned in `README.md`).
- `test_primes.py`, `test_gen_tools.py` — utility coverage.

## Suggested improvements

### 1. Fix `descent()` coverage on `Zm`, `Fp`, `ZmProduct`, `ECpoint`

**Observation.** `Zm` (`mapper/m_modular.py:6`), `Fp`
(`mapper/m_modular.py:94`), `ZmProduct` (`mapper/m_modular_product.py:8`),
and `ECpoint` (`mapper/m_ec.py:102`) have no `descent()` method. Yet
`check_axioms` (`check_protocols.py:392`) and every exception report calls
`descent_str(samples)` (`util/utils.py:64`), which does `cls.descent()` on the
first sample. Running the full property suite on a `Zm` sample today therefore
crashes with `AttributeError` before any axiom is checked.

**Proposed change.** Add `def descent(self): return [type(self)]` to those four
classes (and any future parameterless base type). Even better: factor a tiny
mixin `class HasDescent: def descent(self): return [type(self)]` and use it
across all wrappers.

**Benefit.** Restores the property tests for finite rings / curves and removes
a class of silent failures in the axiom reporter.

### 2. Consolidate `cockpit.py` (or fix the name everywhere)

**Observation.** `CLAUDE.md` and `README.md` (line 106) both reference
`cockpit.py`/`cockpit.params`, but the actual configuration lives in
`util/utils.py` as a free dict `params` (lines 35-46) imported as
`from sandbox.py4alg.util.utils import params`. There is no `cockpit` module.

**Proposed change.** Either rename `utils.py` to `cockpit.py` and split out
`compose/take/comparable_works/descent_str` into a `runtime.py`, or update the
docs. Pure-data parameters and runtime helpers don’t belong in the same
file, and the file naming convention (`s_int.py`, `w_int.py`, `m_complex.py`,
`p_ring.py`) makes the "utils" name an outlier.

**Benefit.** A single, named place for tunables (`atol`, `poly_min`,
`matrix_size`, ...). Docs and code align.

### 3. Promote `inverse()` to the `Field` protocol

**Observation.** `Field` (`protocols/p_field.py`) declares only
`__truediv__`. But `check_truediv_and_inverse` (`check_protocols.py:267`)
calls `a.inverse()` for every Field sample, and every Field implementation
already exposes it (`NativeFloat`, `NativeComplex`, `Fp`, `Fraction`,
`FieldComplex`). The contract is implicit.

**Proposed change.** Add `def inverse(self) -> Any: ...` to the `Field`
protocol. Optionally promote `norm()` similarly — many types implement it
(`Zm`, `ZmProduct`, `Matrix`, `ECpoint`) but it is never a typed obligation.

**Benefit.** Closes a documented gap; `isinstance(x, Field)` becomes a true
guarantee for callers (e.g. linear algebra over a field needs `inverse()`).

### 4. Remove the `hasattr(a, 'gcd')` dispatch in `gcd()` and the `gcd` method on `FieldPolynomial`

**Observation.** `util/primes.py:82-97` falls back from `a.gcd(b)` to the
generic Euclidean loop. The only beneficiary is
`FieldPolynomial.gcd` (`mapper/m_polynomial.py:122`), which normalises at every
step to avoid float blow-up. The roadmap (`roadmap.md` item 1) calls for
removal. The current arrangement is also leaky: `IntWrapper.gcd` in
`tests/py4alg/test_builtins.py:96` participates in dispatch, which silently
swaps the algorithm out from under callers.

**Proposed change.** Fold monic-at-each-step into the generic loop *when the
operand has* `normalize()` *and* is in a Euclidean ring whose units include
non-trivial inverses — or just always call `normalize()` on the running
remainder. Then delete `FieldPolynomial.gcd` and the `hasattr` branch.
Drop `IntWrapper.gcd` too.

**Benefit.** One canonical GCD; removes a hidden polymorphism that defeats
the "axioms are universal" claim of the test suite.

### 5. Split `Polynomial` vs `FieldPolynomial` symmetrically with `Complex` vs `FieldComplex`

**Observation.** `Polynomial` and `Complex` follow the same pattern (use
`type(self)` in arithmetic so the field-subclass propagates), but the *naming*
is asymmetric: ring constructor is `Polynomial`, field-extension subclass is
`FieldPolynomial`; ring constructor is `Complex`, field-extension subclass is
`FieldComplex`. Good. But `Fraction` does not have a `RingFraction` variant
— it always requires `EuclideanRing`. The roadmap (`roadmap.md` item 4)
explicitly motivated the `Polynomial` split, and the same logic could be
applied to `Matrix` (a `FieldMatrix` could expose inverse / determinant /
solve when the entries form a field).

**Proposed change.** Introduce `FieldMatrix[T: Field](Matrix[T])` with
`inverse()`, `det()`, and Gauss–Jordan-based `__truediv__`. Make `Matrix`
strictly `Ring`-typed and remove `type(self)`-less constructors so the
specialisation propagates.

**Benefit.** Symmetric API, opens the door to linear algebra over arbitrary
fields, and exercises another corner of the functor lattice. Fits the
existing pattern of "ring class + Field subclass".

### 6. Make `Matrix` consistent with the other constructors (`type(self)` + `descent()` correctness)

**Observation.** `Matrix.__add__`/`__sub__`/`__mul__`/`__neg__`/`zero`/`one`
in `mapper/m_matrix.py:49-103` all hard-code the bare class `Matrix(...)` —
unlike `Polynomial` (`type(self)`) or `Complex` (`type(self)`). The
`_descent` building (`mapper/m_matrix.py:28,42`) similarly hardcodes the class
`Matrix`. This blocks any subclass (see item 5) and the block-matrix branch
records `descent = args[0].descent()` without prepending the wrapping `Matrix`,
so a block matrix of matrices loses one level of descent compared with a
nested fraction or polynomial.

**Proposed change.** Replace `Matrix(*...)` with `type(self)(*...)`, and in the
block-matrix branch prepend `[type(self)]`. Provide explicit `Matrix(Matrix)`
flattening semantics in the docstring (block matrix vs tensor product) so the
non-idempotent contract is documented at the call site.

**Benefit.** Subclassing works; `descent_str` and the type table accurately
reflect nesting depth.

### 7. Replace the ad-hoc `gen_tree`/`SUCCESSORS` adjacency with a generated cartesian product

**Observation.** `util/gen_samples.py:104-118` hand-encodes the legal
constructor combinations. `protocols/p_table.py` is a separate
stub at experimenting with the same idea via `(Cls, in_protocol) ->
out_protocol`. The two encodings will drift. The roadmap (project memory:
"compound type generator") explicitly wants a single source of truth.

**Proposed change.** Tag each mapper with a class attribute or pair like
`SOURCE_PROTOCOL = Ring`, `TARGET_PROTOCOL = Ring`, plus an `IDEMPOTENT`
flag. Then derive `SUCCESSORS` automatically by enumerating
`{cls : input_protocol matched by output_protocol}`. Make `p_table.py` the
authoritative table and drive both the property-test enumerator and the
documentation table in `README.md` from it.

**Benefit.** Single source of truth; new mappers (e.g. `FieldMatrix`,
`PowerSeries`, `Quaternion`, `Gaussian`) plug in automatically into both the
property runner and the docs.

### 8. Add the missing test corners

**Observation.** Several known weak spots are not covered:

- `Fraction[Fraction[NativeInt]]` flattening is mentioned in the docs and the
  README but only `test_fractions.py` covers `gen_fractions(gen_fractions(...))`
  superficially (it is in `fraction_samples` but only with `nat_ints`).
- `Complex[Complex[...]]` flattening is documented but no test exercises it.
- `Polynomial[Polynomial[NativeInt]]` is tested via
  `polynomials_polynomials_int` in `test_many.py` but only for the int case;
  the `_descent` of the flattened result is not asserted.
- `Matrix[Matrix[...]]` block matrix axioms get one quick test
  (`test_matrices.test_matrix_matrix`) but the block dimensions aren't varied.
- `ZmProduct` claims to be a `Ring`, but `test_zm_product.py` is not even
  imported by the axiom runner — it doesn't use `check_axioms`. Need to
  confirm it actually satisfies the ring axioms via the standard suite.
- `SymbolicInt.euclidean_function` raises `NotImplementedError`, which the
  axiom suite handles gracefully — but that means `check_division` silently
  skips the euclidean-function size constraint for symbolic inputs.

**Proposed change.** Add a `test_descent.py` that, for every reachable type in
`gen_tree(depth=4)`, asserts:
1. `descent()` is a flat `list[type]` of length equal to nesting depth + 1,
2. all entries are classes,
3. flattening invariants hold (`Fraction(Fraction(x)).descent() == Fraction(x).descent()`).
Add `check_axioms` parametrisation to `test_zm_product.py`. Add an explicit
test that `SymbolicInt` either implements a real `euclidean_function` (using
sympy degree on the polynomial form) or that it is downgraded to `Ring`
(no `__floordiv__` / `__mod__`).

**Benefit.** The compositional promises become testable instead of
documentation-only, and the symbolic wrapper is forced to either deliver or
declare a smaller protocol.

### 9. Fix the silent `NativeFloat` constructor and the duplicated `normalize` in `ComplexWrapper`

**Observation.** `NativeFloat.__init__` (`wrapper/w_float.py:12-16`) is the
only wrapper without a final `else: raise TypeError(...)`. Passing `NativeFloat(1)`
silently produces an object with `_value` *unset* — subsequent operations raise
opaque `AttributeError`. Meanwhile `ComplexWrapper` in
`tests/py4alg/test_builtins.py:195-199` declares `normalize` twice, the second
overriding the first identically — almost certainly a copy-paste bug.

**Proposed change.** Add the `else: raise TypeError(...)` branch to
`NativeFloat.__init__` mirroring `NativeInt` and `NativeComplex`. Delete the
duplicate `normalize` in `ComplexWrapper`.

**Benefit.** Fail-fast at construction time; no dead duplicate code in tests.

### 10. Add the symbolic wrappers planned in the roadmap

**Observation.** `s_int.py` (`SymbolicInt`) is a stub: `euclidean_function`
raises `NotImplementedError`, and there is no `SymbolicFloat`/`SymbolicComplex`.
The memory note explicitly lists "symbolic wrappers" as the next milestone.
The test suite already has `test_symbolics.py` but it tests only three samples
and skips division.

**Proposed change.** Implement `SymbolicFloat`/`SymbolicComplex` over
`sympy.Symbol(name, real=True)` / `sympy.Symbol(name)`. Replace
`euclidean_function = NotImplementedError` with `degree`-based logic for
polynomial-of-symbol expressions, falling back to `1` for atoms. Wire
`gen_sym_ints/floats/complex` into `gen_samples.py` and `SUCCESSORS` so the
compositional axiom suite runs over symbolic samples too — this is the
cleanest way to detect *real* axiom violations (no floating-point excuse).

**Benefit.** Property tests over symbolic samples give exact, reproducible
failures; eliminates the "deep towers over floats fail" loophole; unlocks
symbolic differentiation/integration once polynomial APIs are exposed.
