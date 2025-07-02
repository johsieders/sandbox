from __future__ import annotations

from typing import TypeVar, Generic

from sandbox.py4m.protocols.p_field import Field

T = TypeVar("T", bound=Field)


class Polynomial(Generic[T]):

    def __init__(self, *args: T | Polynomial[T]):
        """
        This constructor accepts a nonempty list of coefficients of type T or Polynomial[T].
        Case type == Polynomial: The result p is a Polynomial[T] (flattening)
        p(x) = p_0(x) + p_1(x)*x + p_2(x)*x^2...
        This is the copy constructor if the list contains only one element.
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
            raise TypeError(f"expected 1 or 2 arguments, got {len(args)}")
        elif isinstance(args[0], Polynomial):
            ps = list(args)  # list of polynomials
            zero = ps[0]._coeffs[0].zero()
            coeffs = []
            for k, p in enumerate(ps):
                coeffs += [zero] * len(p._coeffs)
                coeffs[k:k + len(p._coeffs)] = [a + b for a, b in zip(coeffs[k:k + len(p._coeffs)], p._coeffs)]
        else:
            coeffs = list(args)  # list of coefficients

        while len(coeffs) > 1 and coeffs[-1] == coeffs[-1].zero():
            coeffs.pop()
        if len(coeffs) == 0:
            raise TypeError("Polynomial constructor expects at least one non-zero argument")
        self._coeffs = tuple(coeffs)

    def __add__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [
            (self._coeffs[i] if i < m else self._coeffs[0].zero()) +
            (other._coeffs[i] if i < n else other._coeffs[0].zero())
            for i in range(max(m, n))
        ]
        return Polynomial(*result)

    def __sub__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [
            (self._coeffs[i] if i < m else self._coeffs[0].zero()) -
            (other._coeffs[i] if i < n else other._coeffs[0].zero())
            for i in range(max(m, n))
        ]
        return Polynomial(*result)

    def __mul__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [self._coeffs[0].zero() for _ in range(m + n - 1)]
        for i in range(m):
            for j in range(n):
                result[i + j] = result[i + j] + self._coeffs[i] * other._coeffs[j]
        return Polynomial(*result)

    def __neg__(self) -> Polynomial[T]:
        return Polynomial(*[-a for a in self._coeffs])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Polynomial) and self._coeffs == other._coeffs

    def __floordiv__(self, other: Polynomial[T]) -> Polynomial[T]:
        q, _ = self.__divmod__(other)
        return q

    def __mod__(self, other: Polynomial[T]) -> Polynomial[T]:
        _, r = self.__divmod__(other)
        return r

    # def divmod(self, other: Polynomial[T]) -> tuple[Polynomial[T], Polynomial[T]]:
    #     return self.__divmod__(other)

    def degree(self) -> int:
        return len(self._coeffs) - 1

    def norm(self) -> float:
        return max(abs(a.norm()) for a in self._coeffs)
        # return len(self._coeffs) - 1

    def zero(self) -> Polynomial[T]:
        return Polynomial(self._coeffs[0].zero())

    def one(self) -> Polynomial[T]:
        return Polynomial(self._coeffs[0].one())

    def __call__(self, x: T) -> T:
        # Horner's method
        result = self._coeffs[-1]
        for coeff in reversed(self._coeffs[:-1]):
            result = result * x + coeff
        return result

    def __divmod__(self, other: Polynomial[T]) -> tuple[Polynomial[T], Polynomial[T]]:
        # Polynomial long division
        if other == other.zero():
            raise ZeroDivisionError("Polynomial division by zero")
        a = list(self._coeffs)
        b = list(other._coeffs)
        m, n = len(a) - 1, len(b) - 1
        if m < n:
            return Polynomial(a[0].zero()), Polynomial(*a)
        q = [a[0].zero() for _ in range(m - n + 1)]
        d = b[-1]
        r = a[:]
        for k in range(m - n, -1, -1):
            qk = r[n + k] // d
            q[k] = qk
            for j in range(n + 1):
                r[j + k] = r[j + k] - qk * b[j]
        # Normalize remainder (remove trailing zeros)
        while len(r) > 1 and r[-1] == r[-1].zero():
            r.pop()
        return Polynomial(*q), Polynomial(*r)

    def __str__(self) -> str:
        return " + ".join(f"{a}*x^{i}" if i > 0 else str(a)
                          for i, a in enumerate(self._coeffs))

    def __repr__(self) -> str:
        return f"Polynomial({self._coeffs})"

    def coeffs(self) -> tuple[T, ...]:
        return self._coeffs
