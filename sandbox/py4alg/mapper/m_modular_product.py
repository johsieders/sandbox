from __future__ import annotations

from typing import Sequence
from sandbox.py4alg.util.primes import gcd, is_prime, chinese_remainder, mod_inverse


class ZmProduct:
    """
    Elements of the product ring Z/m₀Z × Z/m₁Z × ... × Z/mₖ₋₁Z
    where m₀, ..., mₖ₋₁ are pairwise coprime.

    By the Chinese Remainder Theorem, this is isomorphic to Z/MZ where M = ∏mᵢ.
    Elements are stored as tuples (n₀, ..., nₖ₋₁) where nᵢ ∈ Z/mᵢZ.
    """

    def __init__(self, moduli: Sequence[int], values: Sequence[int]):
        """
        Initialize an element of the product ring.

        :param moduli: tuple of pairwise coprime moduli (m₀, ..., mₖ₋₁)
        :param values: tuple of values (n₀, ..., nₖ₋₁) where nᵢ ∈ Z/mᵢZ
        """
        if len(moduli) != len(values):
            raise TypeError(f"moduli and values must have same length (got {len(moduli)} and {len(values)})")

        if len(moduli) == 0:
            raise ValueError("moduli cannot be empty")

        # Check all moduli are valid
        for m in moduli:
            if not isinstance(m, int) or m <= 1:
                raise ValueError(f"All moduli must be integers > 1 (got {m})")

        # Check pairwise coprimality
        for i in range(len(moduli)):
            for j in range(i + 1, len(moduli)):
                if gcd(moduli[i], moduli[j]) != 1:
                    raise ValueError(f"Moduli must be pairwise coprime (gcd({moduli[i]}, {moduli[j]}) = {gcd(moduli[i], moduli[j])})")

        self._moduli = tuple(moduli)
        self._values = tuple(v % m for v, m in zip(values, moduli))
        self._M = 1
        for m in self._moduli:
            self._M *= m

    @property
    def moduli(self) -> tuple[int, ...]:
        return self._moduli

    @property
    def values(self) -> tuple[int, ...]:
        return self._values

    @property
    def M(self) -> int:
        """Total modulus M = ∏mᵢ"""
        return self._M

    def to_int(self) -> int:
        """Convert to canonical integer representative via Chinese Remainder Theorem"""
        return chinese_remainder(self._values, self._moduli)

    @classmethod
    def from_int(cls, moduli: Sequence[int], n: int) -> ZmProduct:
        """Create from integer n by reducing modulo each mᵢ"""
        values = [n % m for m in moduli]
        return cls(moduli, values)

    def _assert_compatible(self, other: ZmProduct) -> None:
        if not isinstance(other, ZmProduct) or self._moduli != other._moduli:
            raise TypeError(f"Incompatible ZmProduct elements: moduli {self._moduli} vs {getattr(other, '_moduli', '?')}")

    def __add__(self, other: ZmProduct) -> ZmProduct:
        self._assert_compatible(other)
        new_values = [(a + b) % m for a, b, m in zip(self._values, other._values, self._moduli)]
        return ZmProduct(self._moduli, new_values)

    def __sub__(self, other: ZmProduct) -> ZmProduct:
        self._assert_compatible(other)
        new_values = [(a - b) % m for a, b, m in zip(self._values, other._values, self._moduli)]
        return ZmProduct(self._moduli, new_values)

    def __mul__(self, other: ZmProduct) -> ZmProduct:
        self._assert_compatible(other)
        new_values = [(a * b) % m for a, b, m in zip(self._values, other._values, self._moduli)]
        return ZmProduct(self._moduli, new_values)

    def __neg__(self) -> ZmProduct:
        new_values = [(-v) % m for v, m in zip(self._values, self._moduli)]
        return ZmProduct(self._moduli, new_values)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ZmProduct) and self._moduli == other._moduli and self._values == other._values

    def __floordiv__(self, other: ZmProduct) -> ZmProduct:
        self._assert_compatible(other)
        new_values = []
        for a, b, m in zip(self._values, other._values, self._moduli):
            if b == 0:
                raise ZeroDivisionError("Division by zero in ZmProduct")
            try:
                inverse = mod_inverse(b, m)
                new_values.append((a * inverse) % m)
            except ValueError:
                raise ZeroDivisionError(f"Division by {b} in Z/{m}Z is undefined (no inverse exists)")
        return ZmProduct(self._moduli, new_values)

    def __mod__(self, other: ZmProduct) -> ZmProduct:
        return self.zero()

    def __divmod__(self, other: ZmProduct) -> tuple[ZmProduct, ZmProduct]:
        return (self // other, self.zero())

    def norm(self) -> float:
        """Norm as sum of component absolute values"""
        return sum(abs(v) for v in self._values)

    def __bool__(self) -> bool:
        return any(v != 0 for v in self._values)

    def gcd(self, other: ZmProduct) -> ZmProduct:
        self._assert_compatible(other)
        new_values = [gcd(a, b) for a, b in zip(self._values, other._values)]
        return ZmProduct(self._moduli, new_values)

    def zero(self) -> ZmProduct:
        return ZmProduct(self._moduli, [0] * len(self._moduli))

    def one(self) -> ZmProduct:
        return ZmProduct(self._moduli, [1] * len(self._moduli))

    def __str__(self) -> str:
        return f"({', '.join(str(v) for v in self._values)}) (mod {', '.join(str(m) for m in self._moduli)})"

    def __repr__(self) -> str:
        return f"ZmProduct({list(self._moduli)}, {list(self._values)})"


class FpProduct(ZmProduct):
    """
    Elements of the product field F_p₀ × F_p₁ × ... × F_pₖ₋₁
    where p₀, ..., pₖ₋₁ are distinct primes.

    This is a field where every non-zero element has a multiplicative inverse.
    """

    def __init__(self, primes: Sequence[int], values: Sequence[int], check: bool = False):
        """
        Initialize an element of the product field.

        :param primes: tuple of distinct prime numbers (p₀, ..., pₖ₋₁)
        :param values: tuple of values (n₀, ..., nₖ₋₁) where nᵢ ∈ Fpᵢ
        :param check: if True, verify that all moduli are prime
        """
        if check:
            for p in primes:
                if not is_prime(p):
                    raise ValueError(f"{p} is not prime")

        super().__init__(primes, values)

    @property
    def primes(self) -> tuple[int, ...]:
        """Alias for moduli (emphasizes they are primes)"""
        return self._moduli

    @classmethod
    def from_int(cls, primes: Sequence[int], n: int) -> FpProduct:
        """Create from integer n by reducing modulo each pᵢ"""
        values = [n % p for p in primes]
        return cls(primes, values)

    # Override operations to return FpProduct instances
    def __add__(self, other: FpProduct) -> FpProduct:
        result = super().__add__(other)
        return FpProduct(result._moduli, result._values)

    def __sub__(self, other: FpProduct) -> FpProduct:
        result = super().__sub__(other)
        return FpProduct(result._moduli, result._values)

    def __mul__(self, other: FpProduct) -> FpProduct:
        result = super().__mul__(other)
        return FpProduct(result._moduli, result._values)

    def __neg__(self) -> FpProduct:
        result = super().__neg__()
        return FpProduct(result._moduli, result._values)

    def __eq__(self, other: object) -> bool:
        return super().__eq__(other)

    def __truediv__(self, other: FpProduct) -> FpProduct:
        self._assert_compatible(other)
        return self * other.inverse()

    def __floordiv__(self, other: FpProduct) -> FpProduct:
        return self / other

    def __mod__(self, other: FpProduct) -> FpProduct:
        return self.zero()

    def __divmod__(self, other: FpProduct) -> tuple[FpProduct, FpProduct]:
        return (self / other, self.zero())

    def inverse(self) -> FpProduct:
        """Multiplicative inverse (exists since all components are in fields)"""
        if not self:
            raise ZeroDivisionError("Zero has no inverse in FpProduct")

        new_values = []
        for v, p in zip(self._values, self._moduli):
            if v == 0:
                raise ZeroDivisionError(f"Component {v} (mod {p}) has no inverse")
            new_values.append(mod_inverse(v, p))

        return FpProduct(self._moduli, new_values)

    def gcd(self, other: FpProduct) -> FpProduct:
        """In a field, gcd is 1 unless both components are 0"""
        self._assert_compatible(other)
        new_values = []
        for a, b in zip(self._values, other._values):
            new_values.append(0 if (a == 0 and b == 0) else 1)
        return FpProduct(self._moduli, new_values)

    def zero(self) -> FpProduct:
        return FpProduct(self._moduli, [0] * len(self._moduli))

    def one(self) -> FpProduct:
        return FpProduct(self._moduli, [1] * len(self._moduli))

    def __str__(self) -> str:
        return f"({', '.join(str(v) for v in self._values)}) (mod {', '.join(str(p) for p in self._moduli)})"

    def __repr__(self) -> str:
        return f"FpProduct({list(self._moduli)}, {list(self._values)})"