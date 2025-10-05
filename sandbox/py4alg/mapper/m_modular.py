from __future__ import annotations

from sandbox.py4alg.util.primes import gcd, is_prime, mod_inverse


class Zm:
    def __init__(self, *args: int):
        if len(args) != 2:
            raise TypeError(f"Zm expects exactly two arguments: m, n (got {args})")
        m, n = args
        if not isinstance(m, int) or not isinstance(n, int):
            raise TypeError("Both m and n must be integers")
        if m <= 1:
            raise ValueError("Zm requires a modulus m > 1")
        self._m = m
        self._n = n % m

    @property
    def m(self) -> int:
        return self._m

    @property
    def n(self) -> int:
        return self._n

    def _assert_compatible(self, other: Zm) -> None:
        if not isinstance(other, Zm) or self._m != other._m:
            raise TypeError(f"Incompatible Zm elements: {self._m} vs {getattr(other, '_m', '?')}")

    def __add__(self, other: Zm) -> Zm:
        self._assert_compatible(other)
        return Zm(self._m, self._n + other._n)

    def __sub__(self, other: Zm) -> Zm:
        self._assert_compatible(other)
        return Zm(self._m, self._n - other._n)

    def __mul__(self, other: Zm) -> Zm:
        self._assert_compatible(other)
        return Zm(self._m, self._n * other._n)

    def __neg__(self) -> Zm:
        return Zm(self._m, -self._n)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Zm) and self._m == other._m and self._n == other._n

    def __floordiv__(self, other: Zm) -> Zm:
        self._assert_compatible(other)
        if other._n == 0:
            raise ZeroDivisionError("Division by zero in Zm")
        # For rings, division is only possible when the divisor has an inverse
        # i.e., when gcd(other._n, self._m) == 1
        try:
            inverse = mod_inverse(other._n, self._m)
            return Zm(self._m, (self._n * inverse) % self._m)
        except ValueError:
            # If no inverse exists, division is undefined in this ring
            raise ZeroDivisionError(f"Division by {other._n} in Z/{self._m}Z is undefined (no inverse exists)")

    def __mod__(self, other: Zm) -> Zm:
        return Zm(self._m, 0)

    def __divmod__(self, other: Zm) -> tuple[Zm, Zm]:
        return (self // other, self.zero())

    def norm(self) -> float:
        return abs(self._n)

    def __bool__(self) -> bool:
        return bool(self._n)

    def gcd(self, a: Zm) -> Zm:
        result = gcd(self._n, a._n)
        return Zm(self._m, result)

    def zero(self) -> Zm:
        return Zm(self._m, 0)

    def one(self) -> Zm:
        return Zm(self._m, 1)

    def __str__(self) -> str:
        return f"{self._n} (mod {self._m})"

    def __repr__(self) -> str:
        return f"Zm({self._m}, {self._n})"


class Fp(Zm):
    def __init__(self, *args: int, check=False):
        p, n = args
        # Initialize the parent Zm class
        super().__init__(p, n)
        if check:
            self.check_prime()

    @property
    def p(self) -> int:
        return self._m

    def check_prime(self):
        if not is_prime(self._m):
            raise ValueError(f"{self._m} is not a prime")

    # Override operations to return Fp instances instead of Zm
    def __add__(self, other: Fp) -> Fp:
        result = super().__add__(other)
        return Fp(result._m, result._n)

    def __sub__(self, other: Fp) -> Fp:
        result = super().__sub__(other)
        return Fp(result._m, result._n)

    def __mul__(self, other: Fp) -> Fp:
        result = super().__mul__(other)
        return Fp(result._m, result._n)

    def __neg__(self) -> Fp:
        return Fp(self._m, -self._n)

    def __lt__(self, other: Fp) -> bool:
        self._assert_compatible(other)
        return self._n < other._n

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)

    def __truediv__(self, other: Fp) -> Fp:
        if not isinstance(other, Fp) or self._m != other._m:
            raise TypeError(f"Incompatible Fp elements: {self._m} vs {getattr(other, '_m', '?')}")
        return self * other.inverse()

    def __floordiv__(self, other: Fp) -> Fp:
        return self / other

    def __mod__(self, other: Fp) -> Fp:
        return Fp(self._m, 0)

    def __divmod__(self, other: Fp) -> tuple[Fp, Fp]:
        return self / other, self.zero()

    def inverse(self) -> Fp:
        if self._n == 0:
            raise ZeroDivisionError("Zero has no inverse in Fp")
        inverse = mod_inverse(self._n, self._m)
        return Fp(self._m, inverse)

    def gcd(self, a: Fp) -> Fp:
        """In a field, gcd is 1 unless both components are 0"""
        return self.zero() if (self._n == 0 and a._n == 0) else self.one()

    def zero(self) -> Fp:
        return Fp(self._m, 0)

    def one(self) -> Fp:
        return Fp(self._m, 1)

    def __str__(self) -> str:
        return f"{self._n} (mod {self._m})"

    def __repr__(self) -> str:
        return f"Fp({self._m}, {self._n})"
