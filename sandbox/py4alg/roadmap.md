24.03.2026

Here is my plam:

1. The only gcd() remaining is the one in util.primes.py. It normalizes the result
   to make the result predictable. Remove all gcd methods. Replace calls like a.gcd(b) with gcd(a, b)

2. all classes implement __bool__. self.__bool__() returns True iff
   abs(self) > atol or self.norm() > atol, with abs and norm depending on the class.

3. All classes implement __equals__. self.__equals__(other) returns True if not (self - other)
   Tests like "if close_to (a, zero)" are replaced with "if a", tests like "if close_to(a, b)"
   are replaced with "if a == b". close_to becomes redundant.

4. Typing is clear for all classes but for Polynomial.
   NatInt implements EuclideanRing, i.e. isinstance(n, EuclideanRing) is True if n is a NatInt
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
   I see two options: (a) class Polynomial gets a discriminator which means that all classes need one,
   (unless all tests treat Polynomial as a special case). (b) I have two classes Polynomial_Ring and
   Polynomial_Field, with the field class as subclass of the other one.
   Decision: Two classes, Polynomial and FieldPolynomial.

25.3.2026

5. Remove normalize from primes.gcd, because (a) it is mathematically wrong (b) it makes checks asymmetric.
   It is up to the caller to normalize ot not to normalize (see constructor of Fraction) 
   Add the necessary normalize calls to all relevant tests.

6. Testing divmod and %: After r = a%b I want to add something like 
   assert r.euclidean_function() < b.euclidean_function().
   Euclidean_function is undefined on zero and should raise an exception (ValueError)

7. replace all prefixes "g_" with "gen_", all "d_" with "def_" (functions and files)
