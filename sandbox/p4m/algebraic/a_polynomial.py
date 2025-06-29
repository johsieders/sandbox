from __future__ import annotations

from typing import TypeVar, Generic, Sequence

from sandbox.p4m.protocols.p_euclidean_ring import EuclideanRing

T = TypeVar("T", bound=EuclideanRing)


class Polynomial(Generic[T]):
    __slots__ = ("_coeffs",)

    def __init__(self, coeffs: Sequence[T] | Polynomial[T]):
        if isinstance(coeffs, Polynomial):
            self._coeffs = coeffs._coeffs  # Shallow copy is enough; tuple is immutable
        elif isinstance(coeffs, Sequence):
            if not coeffs:
                raise ValueError("Polynomial must have at least one coefficient")
            # Remove trailing zeros (normalize)
            coeffs = list(coeffs)
            while len(coeffs) > 1 and coeffs[-1] == coeffs[-1].zero():
                coeffs.pop()
            self._coeffs = tuple(coeffs)
        else:
            raise TypeError("Polynomial constructor expects a Sequence or a Polynomial")

    def __add__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [
            (self._coeffs[i] if i < m else self._coeffs[0].zero()) +
            (other._coeffs[i] if i < n else other._coeffs[0].zero())
            for i in range(max(m, n))
        ]
        return Polynomial(result)

    def __sub__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [
            (self._coeffs[i] if i < m else self._coeffs[0].zero()) -
            (other._coeffs[i] if i < n else other._coeffs[0].zero())
            for i in range(max(m, n))
        ]
        return Polynomial(result)

    def __mul__(self, other: Polynomial[T]) -> Polynomial[T]:
        m, n = len(self._coeffs), len(other._coeffs)
        result = [self._coeffs[0].zero() for _ in range(m + n - 1)]
        for i in range(m):
            for j in range(n):
                result[i + j] = result[i + j] + self._coeffs[i] * other._coeffs[j]
        return Polynomial(result)

    def __neg__(self) -> Polynomial[T]:
        return Polynomial([-a for a in self._coeffs])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Polynomial) and self._coeffs == other._coeffs

    def __floordiv__(self, other: Polynomial[T]) -> Polynomial[T]:
        q, _ = self._divmod(other)
        return q

    def __mod__(self, other: Polynomial[T]) -> Polynomial[T]:
        _, r = self._divmod(other)
        return r

    def divmod(self, other: Polynomial[T]) -> tuple[Polynomial[T], Polynomial[T]]:
        return self._divmod(other)

    def degree(self) -> int:
        return len(self._coeffs) - 1

    def norm(self) -> float:
        return max(abs(a.norm()) for a in self._coeffs)

    def zero(self) -> Polynomial[T]:
        return Polynomial([self._coeffs[0].zero()])

    def one(self) -> Polynomial[T]:
        return Polynomial([self._coeffs[0].one()])

    def __call__(self, x: T) -> T:
        # Horner's method
        result = self._coeffs[-1]
        for coeff in reversed(self._coeffs[:-1]):
            result = result * x + coeff
        return result

    def _divmod(self, other: Polynomial[T]) -> tuple[Polynomial[T], Polynomial[T]]:
        # Polynomial long division
        if other == other.zero():
            raise ZeroDivisionError("Polynomial division by zero")
        a = list(self._coeffs)
        b = list(other._coeffs)
        m, n = len(a) - 1, len(b) - 1
        if m < n:
            return Polynomial([a[0].zero()]), Polynomial(a)
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
        return Polynomial(q), Polynomial(r)

    def __str__(self) -> str:
        return " + ".join(f"{a}*x^{i}" if i > 0 else str(a)
                          for i, a in enumerate(self._coeffs))

    def __repr__(self) -> str:
        return f"Polynomial({self._coeffs})"

    def coeffs(self) -> tuple[T, ...]:
        return self._coeffs
