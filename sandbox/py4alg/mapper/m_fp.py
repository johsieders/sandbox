from __future__ import annotations


# AlgebraicType import removed - using protocol-based system instead


class Fp:
    def __init__(self, *args: int):
        if len(args) != 2:
            raise TypeError(f"Fp expects exactly two arguments: p, n (got {args})")
        p, n = args
        if not isinstance(p, int) or not isinstance(n, int):
            raise TypeError("Both p and n must be integers")
        if p <= 1:
            raise ValueError("Fp requires a prime modulus p > 1")
        self._p = p
        self._n = n % p

    @property
    def p(self) -> int:
        return self._p

    @property
    def n(self) -> int:
        return self._n

    def _assert_compatible(self, other: Fp) -> None:
        if not isinstance(other, Fp) or self._p != other._p:
            raise TypeError(f"Incompatible Fp elements: {self._p} vs {getattr(other, '_p', '?')}")

    def __add__(self, other: Fp) -> Fp:
        self._assert_compatible(other)
        return Fp(self._p, self._n + other._n)

    def __sub__(self, other: Fp) -> Fp:
        self._assert_compatible(other)
        return Fp(self._p, self._n - other._n)

    def __mul__(self, other: Fp) -> Fp:
        self._assert_compatible(other)
        return Fp(self._p, self._n * other._n)

    def __neg__(self) -> Fp:
        return Fp(self._p, -self._n)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Fp) and self._p == other._p and self._n == other._n

    def __lt__(self, other: Fp) -> bool:
        self._assert_compatible(other)
        return self._n < other._n

    def __truediv__(self, other: Fp) -> Fp:
        self._assert_compatible(other)
        return self * other.inverse()

    def __floordiv__(self, other: Fp) -> Fp:
        return self / other

    def __mod__(self, other: Fp) -> Fp:
        return Fp(self._p, 0)

    def __divmod__(self, other: Fp) -> tuple[Fp, Fp]:
        return (self / other, self.zero())

    def inverse(self) -> Fp:
        if self._n == 0:
            raise ZeroDivisionError("Zero has no inverse in Fp")
        # Extended Euclidean algorithm for modular inverse
        a, b = self._n, self._p
        x0, x1 = 1, 0
        while b != 0:
            q, a, b = a // b, b, a % b
            x0, x1 = x1, x0 - q * x1
        inv = x0 % self._p
        return Fp(self._p, inv)

    def norm(self) -> float:
        # For a finite field element, norm is just abs(n)
        return abs(self._n)

    def __bool__(self) -> bool:
        return bool(self._n)

    def gcd(self, a: Fp) -> Fp:
        return Fp(self._p, 1) \
            if (self._n > 0 or a._n > 0) \
            else Fp(self._p, 0)

    def zero(self) -> Fp:
        return Fp(self._p, 0)

    def one(self) -> Fp:
        return Fp(self._p, 1)

    # implements() method removed - using protocol-based system instead

    def __str__(self) -> str:
        return f"{self._n} (mod {self._p})"

    def __repr__(self) -> str:
        return f"Fp({self._p}, {self._n})"
