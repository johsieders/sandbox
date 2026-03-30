from __future__ import annotations

from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring


class Polynomial[T: Ring]:

    def __init__(self, *args: T | Polynomial[T]):
        """
        This constructor accepts a nonempty list of coefficients of type T or Polynomial[T].
        Case type == Polynomial: The result p is a Polynomial[T] (flattening)
        p(x) = p_0(x) + p_1(x)*x + p_2(x)*x^2...
        If the list contains only one element, it is assumed to be a polynomial,
        and the constructor makes a copy of it.
        Case type <= EuclideanRing: The result is a polynomial with given coefficients.
        Trailing zeros are eliminated.

        Let ps = [p_0, p_1, p_2, ...] a list of polynomials and x an arbitrary argument.
        There are two ways to construct a polynomial:

        q = Polynomial(*ps)
        r(x) = Polynomial((p(x) for p in ps))
        Then for all x, we have:
        q(x) == r(x)(x)
        """

        if len(args) == 0:
            raise TypeError(f"expected at least one argument, got {len(args)}")
        elif isinstance(args[0], Polynomial):
            self._descent = args[0].descent()
            ps = list(args)  # list of polynomials
            zero = ps[0]._coeffs[0].zero()
            coeffs = []
            for k, p in enumerate(ps):
                coeffs += [zero] * len(p._coeffs)
                coeffs[k:k + len(p._coeffs)] = [a + b for a, b in zip(coeffs[k:k + len(p._coeffs)], p._coeffs)]
        else:
            self._descent = [type(self)] + args[0].descent()
            coeffs = list(args)  # list of coefficients

        while len(coeffs) > 1 and not coeffs[-1]:
            coeffs.pop()
        self._coeffs = tuple(coeffs)

    def __add__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [
            (self._coeffs[i] if i < m else self._coeffs[0].zero()) +
            (other._coeffs[i] if i < n else other._coeffs[0].zero())
            for i in range(max(m, n))
        ]
        return type(self)(*result)

    def __sub__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [
            (self._coeffs[i] if i < m else self._coeffs[0].zero()) -
            (other._coeffs[i] if i < n else other._coeffs[0].zero())
            for i in range(max(m, n))
        ]
        return type(self)(*result)

    def __mul__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [self._coeffs[0].zero() for _ in range(m + n - 1)]
        for i in range(m):
            for j in range(n):
                result[i + j] = result[i + j] + self._coeffs[i] * other._coeffs[j]
        return type(self)(*result)

    def __neg__(self) -> Polynomial[T]:
        return type(self)(*[-a for a in self._coeffs])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Polynomial) and self._coeffs == other._coeffs

    def __bool__(self) -> bool:
        # return len(self._coeffs) > 1 or bool(self._coeffs[0])
        return bool(self._coeffs[-1])

    def degree(self) -> int:
        return len(self._coeffs) - 1

    def zero(self) -> Polynomial[T]:
        return type(self)(self._coeffs[0].zero())

    def one(self) -> Polynomial[T]:
        return type(self)(self._coeffs[0].one())

    def __call__(self, x: T) -> T:
        # Horner's method
        result = self._coeffs[-1]
        for coeff in reversed(self._coeffs[:-1]):
            result = result * x + coeff
        return result

    def __str__(self) -> str:
        return " + ".join(f"{a}*x^{i}" if i > 0 else str(a)
                          for i, a in enumerate(self._coeffs))

    def __repr__(self) -> str:
        return f"Polynomial({self._coeffs})"

    def coeffs(self) -> tuple[T, ...]:
        return self._coeffs

    def descent(self):
        return self._descent


class FieldPolynomial[T: Field](Polynomial[T]):

    def __floordiv__(self, other: FieldPolynomial[T]) -> FieldPolynomial[T]:
        q, _ = self.__divmod__(other)
        return q

    def __mod__(self, other: FieldPolynomial[T]) -> FieldPolynomial[T]:
        _, r = self.__divmod__(other)
        return r

    def gcd(self, other: FieldPolynomial[T]) -> FieldPolynomial[T]:
        """Numerically stable GCD via monic Euclidean algorithm.

        Normalizes (makes monic) at each step to prevent coefficient explosion
        that occurs with floating-point arithmetic.
        """
        a, b = self, other
        while b:
            a, b = b, (a % b)
            if b:
                b = b.normalize()
        return a.normalize()

    def __divmod__(self, other: FieldPolynomial[T]) -> tuple[FieldPolynomial[T], FieldPolynomial[T]]:
        if not other:
            raise ZeroDivisionError("Polynomial division by zero")

        a = list(self._coeffs)
        b = list(other._coeffs)
        m, n = len(a) - 1, len(b) - 1
        if m < n:
            return FieldPolynomial(a[0].zero()), FieldPolynomial(*a)
        q = [a[0].zero() for _ in range(m - n + 1)]
        d = b[-1]
        r = a[:]
        for k in range(m - n, -1, -1):
            qk = r[n + k] / d
            q[k] = qk
            for j in range(n + 1):
                r[j + k] = r[j + k] - qk * b[j]
        # Normalize remainder (remove trailing zeros)
        while len(r) > 1 and not r[-1]:
            r.pop()
        return FieldPolynomial(*q), FieldPolynomial(*r)

    def euclidean_function(self) -> int:
        if not self:
            raise ValueError("euclidean_function is undefined on zero")
        return self.degree()

    def normalize(self) -> FieldPolynomial[T]:
        if self._coeffs[-1]:
            return FieldPolynomial(*[c / self._coeffs[-1] for c in self._coeffs])
        else:
            return self

    def __repr__(self) -> str:
        return f"FieldPolynomial({self._coeffs})"
