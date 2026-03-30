30.03.2026

Here is my testing plan:

1. check_protocols (formerly test_properties) is near perfect.
   It contains functions like 
   `check_totality(samples)`
   that accept a Sequence of Sequence of Ring, EuclideanRing, or Field elements.
   Each inner Sequence is homogenous (all elements are of the same type).
   The type is determined by `instanceof(element, Protocol)` for Ring, EuclideanRing, or Field.
   Comparable is determined by `comparable_works`.
   Each sample should contain not more that a few elements (say 5),
   because some checks are O(n^3).
   The main test is `check_any`that accepts a sequence of homogenous sequences and
   performs the relevant tests.
   The Axiom registry becomes redundant.


2. There are small tests and big tests. They all define homogenous sequences of samples 
   and just call `check_any`. test_natives and test_builtins
   are examples of small ones. Small tests do one or two types, large tests do many.
   Small tests my contain any number of special, type-related tests. The small tests are:
   
   test_builtins
   test_natives
   test_complex 
   test_fractions 
   test_polynomials
   test_fp
   test_zm
   test_ec
   
