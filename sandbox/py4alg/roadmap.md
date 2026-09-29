24.03.2026

Here is my plam:

1. The only gcd () remaining is the one in util.primes.py. It normalizes the result
   to make the result predictable. Remove all gcd methods. Replace calls like a.gcd (b) with gcd (a, b)

2. all classes implement __bool__. self. __bool__() returns True iff
   abs (self) > atol or self.norm () > atol, with abs and norm depending on the class.

3. All classes implement __equals__. self. __equals__(other) returns True if not (self - other)
   Tests like "if close_to (a, zero)" are replaced with "if a", tests like "if close_to (a, b)"
   are replaced with "if a == b". close_to becomes redundant.

4. Typing is clear for all classes but for Polynomial.
   NatInt implements EuclideanRing, i.e. isinstance (n, EuclideanRing) is True if n is a NatInt
   NatFloat implements Field, i.e. ...
   NatComplex implements Field, i.e. ...
   Complex[T: Field] implements Field, i.e. ...
   Fraction[T: EuclideanRing] implements Field, i.e. ...
   Matrix[T: Ring] implements Ring, i.e. ...

   Tests easily find out what an object is and run the appropriate tests.

   now Polynomial
   Should be like:
   Polynomial[T: Field] implements EuclideanRing, i.e. ...
   Polynomial[T: Ring] implements Ring, i.e. ...

   Is:
   Polynomial[T: Ring] implements EuclideanRing, i.e....

   which is wrong.
   I see two options: (a) class Polynomial gets a discriminator which means that all classes need one, (unless all tests
   treat Polynomial as a special case). (b) I have two classes Polynomial_Ring and
   Polynomial_Field, with the field class as subclass of the other one.
   Decision: Two classes, Polynomial and FieldPolynomial.

25.3.2026 A

5. Remove normalize from primes.gcd, because (a) it is mathematically wrong (b) it makes checks asymmetric.
   It is up to the caller to normalize ot not to normalize (see constructor of Fraction)
   Add the necessary normalize calls to all relevant tests.

6. Testing divmod and %: After r = a%b I want to add something like
   assert r.euclidean_function () < b.euclidean_function ().
   Euclidean_function is undefined on zero and should raise an exception (ValueError)

7. replace all prefixes "g_" with "gen_", all "d_" with "def_" (functions and files)

29.09.2026 Status and plan

Collected from this roadmap (R1-R7) and from the suggested improvements in
py4alg_structure.md (S1-S10), checked against the code.

Done:

- R2 all classes implement __bool__
- R3 in substance: close_to is gone; tolerance lives in __eq__ of NativeFloat/NativeComplex,
  __bool__ builds on it (not via "not (self - other)")
- R4 Polynomial / FieldPolynomial
- R5 no normalize in primes.gcd; the tests normalize
- R6 check_division checks r.euclidean_function() < b.euclidean_function();
  euclidean_function raises ValueError on zero (except SymbolicInt, see 8)
- R7 prefixes gen_ / def_
- S1 descent() on Zm, Fp, ZmProduct, ECpoint (the HasDescent mixin was not done)
- also: check_axioms checks abelian groups (ECpoint); robust exception handling in
  check_protocols; exception report in reports/py4alg_exceptions_<host>.txt

Not an issue:

- S6, second half: a block matrix Matrix(Matrix, ...) is flattened (4 blocks 2x2 -> 4x4 over the
  scalars), so descent() == [Matrix, T] is correct. py4alg_structure.md and CLAUDE.md
  ("Matrix(Matrix) is a matrix of matrices") are wrong here.

Open, in this order:

Phase 1: quick fixes
1. S9 NativeFloat.__init__ gets "else: raise TypeError" (NativeFloat(1) is accepted silently and
   fails later with AttributeError); delete the duplicate normalize in ComplexWrapper
   (tests/py4alg/test_builtins.py).
2. S2 there is no cockpit.py (params live in util/utils.py): fix the references in CLAUDE.md and
   README, or rename. Also in CLAUDE.md: check_properties.py -> check_protocols.py, and the
   Matrix(Matrix) sentence. Bring py4alg_structure.md up to date (done items, S6).

Phase 2: one gcd (R1 = S4)
3. Delete FieldPolynomial.gcd, the hasattr(a, 'gcd') dispatch in primes.gcd, and the two gcd
   methods of the test wrappers in test_builtins.py.
4. Keep float polynomials stable: the generic loop normalizes the running remainder if it has
   normalize() (changes the gcd only by a unit, so R5 still holds).
5. Compare the exception report before and after (float towers).

Phase 3: protocols that tell the truth
6. S3 inverse() into the Field protocol; check that all fields (incl. test wrappers) still pass
   isinstance(x, Field).
7. ZmProduct has zero divisors, so it is no Euclidean ring (check_division fails with
   ZeroDivisionError): downgrade to Ring (drop //, %, divmod, euclidean_function, normalize);
   test_zm_product.py gets check_axioms (S8).
8. SymbolicInt: real euclidean_function (degree-based, cf. S10) or downgrade to Ring.

Phase 4: missing tests (S8)
9. test_descent.py: descent() structure for all types of gen_tree(depth=4); flattening invariants
   of Polynomial, Complex, Fraction; block-matrix semantics.
10. Explicit Complex(Complex) flattening test; block matrices with varied block sizes.

Phase 5: Matrix consistent, FieldMatrix (S6, S5)
11. type(self) instead of Matrix(...) in Matrix (6 places), so subclasses propagate.
12. FieldMatrix[T: Field] with inverse(), det(), Gauss-Jordan __truediv__ (needs 6).

Phase 6: one table of type combinations (S7)
13. Each mapper declares input protocol, output protocol, flattening; SUCCESSORS is derived.
14. p_table.py becomes the single source of truth or is removed; new mappers (FieldMatrix,
    symbolic) plug in automatically.

Phase 7: symbolic wrappers (S10)
15. SymbolicFloat / SymbolicComplex, gen_sym_* in the table from phase 6: property tests over
    exact values, no floating-point excuse.

Decisions needed:
- S2: rename to cockpit.py, or fix the docs?
- NativeFloat(1): reject ints, or convert to float?
- ZmProduct: downgrade to Ring?
- SymbolicInt: real euclidean_function, or downgrade to Ring?
