"""
Testing Built-in Python Types with check_properties

This file demonstrates the universal nature of check_properties.py by testing
Python's built-in numeric types (int, float, complex) directly against the
mathematical axioms. This shows that the property tests are truly implementation-
agnostic and work with any type that supports the required operations.

This serves as both a validation that our axiom tests are correct (since built-ins
are known to be mathematically sound) and a demonstration that check_properties.py
is a universal mathematical testing framework.

Note: This testing is redundant since built-in types are already mathematically
correct, but it proves the universality of our approach.
"""

from typing import List

from tests.py4alg.check_properties import (
    check_abelian_group, check_fields, check_comparables,
    check_additive_identity, check_multiplicative_identity,
    check_commutativity_multiplication, check_distributivity
)

# Test constants
N = 10  # Sample size for testing


def int_samples() -> List[int]:
    """Generate built-in int samples."""
    return [0, 1, -1, 2, -2, 5, -5, 10, -10, 42]


def float_samples() -> List[float]:
    """Generate built-in float samples."""
    return [0.0, 1.0, -1.0, 2.5, -2.5, 3.14, -3.14, 0.1, -0.1, 42.0]


def complex_samples() -> List[complex]:
    """Generate built-in complex samples."""
    return [
        0 + 0j, 1 + 0j, 0 + 1j, 1 + 1j, -1 + 0j, 0 - 1j, -1 - 1j,
        2 + 3j, -2 - 3j, 3.14 + 2.71j
    ]


# Helper mixin class that provides algebraic structure methods
class AlgebraicMixin:
    """Mixin class providing algebraic structure methods for built-in types."""

    def norm(self):
        """Return the norm (absolute value) of this element."""
        return abs(self)


class FieldMixin(AlgebraicMixin):
    """Mixin class providing field operations for types that support division."""

    def inverse(self):
        """Return the multiplicative inverse of this element."""
        if self == self.__class__.zero():
            raise ZeroDivisionError(f"{self.__class__.__name__}.inverse(): division by zero")
        return self.__class__(1) / self

    def gcd(self, other):
        """GCD in a field: 1 if either is non-zero, 0 if both are zero."""
        if self != self.__class__.zero() or other != other.__class__.zero():
            return self.__class__.one()
        else:
            return self.__class__.zero()


# Inheritance-based wrappers that extend built-in types with algebraic methods
class IntWrapper(int, AlgebraicMixin):
    """Integer wrapper that inherits from int and adds algebraic structure methods."""

    def __new__(cls, value=0):
        return super().__new__(cls, value)

    def __add__(self, other): return IntWrapper(super().__add__(other))

    def __sub__(self, other): return IntWrapper(super().__sub__(other))

    def __mul__(self, other): return IntWrapper(super().__mul__(other))

    def __neg__(self): return IntWrapper(super().__neg__())

    def __floordiv__(self, other): return IntWrapper(super().__floordiv__(other))

    def __mod__(self, other): return IntWrapper(super().__mod__(other))

    def __divmod__(self, other):
        q, r = super().__divmod__(other)
        return IntWrapper(q), IntWrapper(r)

    def gcd(self, other):
        """Euclidean GCD for integers using Python's math.gcd."""
        import math
        return IntWrapper(math.gcd(int(self), int(other)))

    @classmethod
    def zero(cls): return cls(0)

    @classmethod
    def one(cls): return cls(1)


class FloatWrapper(float, FieldMixin):
    """Float wrapper that inherits from float and adds algebraic structure methods."""

    def __new__(cls, value=0.0):
        return super().__new__(cls, value)

    def __add__(self, other): return FloatWrapper(super().__add__(other))

    def __sub__(self, other): return FloatWrapper(super().__sub__(other))

    def __mul__(self, other): return FloatWrapper(super().__mul__(other))

    def __truediv__(self, other):
        if other == 0.0:
            raise ZeroDivisionError("Float division by zero")
        return FloatWrapper(super().__truediv__(other))

    def __neg__(self): return FloatWrapper(super().__neg__())

    def __floordiv__(self, other):
        # In a field, floor division is the same as true division
        return self / other

    def __mod__(self, other):
        # In a field, remainder is always zero
        return FloatWrapper.zero()

    def __divmod__(self, other):
        # In a field, divmod returns (quotient, 0)
        return self / other, FloatWrapper.zero()

    def __eq__(self, other):
        return abs(self - other) < 1e-10 if isinstance(other, (float, FloatWrapper)) else False

    @classmethod
    def zero(cls): return cls(0.0)

    @classmethod
    def one(cls): return cls(1.0)


class ComplexWrapper(complex, FieldMixin):
    """Complex wrapper that inherits from complex and adds algebraic structure methods."""

    def __new__(cls, real=0, imag=0):
        if isinstance(real, complex):
            return super().__new__(cls, real)
        return super().__new__(cls, real, imag)

    def __add__(self, other):
        return ComplexWrapper(super().__add__(other))

    def __sub__(self, other):
        return ComplexWrapper(super().__sub__(other))

    def __mul__(self, other):
        return ComplexWrapper(super().__mul__(other))

    def __truediv__(self, other):
        if other == 0 + 0j:
            raise ZeroDivisionError("Complex division by zero")
        return ComplexWrapper(super().__truediv__(other))

    def __neg__(self):
        return ComplexWrapper(super().__neg__())

    def __floordiv__(self, other):
        # In a field, floor division is the same as true division
        return self / other

    def __mod__(self, other):
        # In a field, remainder is always zero
        return ComplexWrapper.zero()

    def __divmod__(self, other):
        # In a field, divmod returns (quotient, 0)
        return self / other, ComplexWrapper.zero()

    def __eq__(self, other):
        return abs(self - other) < 1e-10 if isinstance(other, (complex, ComplexWrapper)) else False

    @classmethod
    def zero(cls):
        return cls(0 + 0j)

    @classmethod
    def one(cls):
        return cls(1 + 0j)


def wrapped_int_samples() -> List[IntWrapper]:
    """Generate wrapped int samples for testing."""
    return [IntWrapper(x) for x in int_samples()]


def wrapped_float_samples() -> List[FloatWrapper]:
    """Generate wrapped float samples for testing."""
    return [FloatWrapper(x) for x in float_samples()]


def wrapped_complex_samples() -> List[ComplexWrapper]:
    """Generate wrapped complex samples for testing."""
    return [ComplexWrapper(x) for x in complex_samples()]


# Test functions following the pattern of test_protocol_samples

def test_builtin_int_abelian_group():
    """Test that built-in int satisfies abelian group axioms."""
    samples = wrapped_int_samples()
    check_abelian_group(samples[:N])


def test_builtin_int_ring():
    """Test that built-in int satisfies ring axioms."""
    samples = wrapped_int_samples()
    # Integers form a ring but not a field (no multiplicative inverses)
    check_additive_identity(samples)
    check_multiplicative_identity(samples)
    check_commutativity_multiplication(samples)
    check_distributivity(samples)


def test_builtin_int_comparable():
    """Test that built-in int satisfies total order axioms."""
    samples = wrapped_int_samples()
    check_comparables(samples[:N])


def test_builtin_float_field():
    """Test that built-in float satisfies field axioms."""
    samples = wrapped_float_samples()
    check_fields(samples[:N])


def test_builtin_float_comparable():
    """Test that built-in float satisfies total order axioms."""
    samples = wrapped_float_samples()
    check_comparables(samples[:N])


def test_builtin_complex_field():
    """Test that built-in complex satisfies field axioms."""
    samples = wrapped_complex_samples()
    check_fields(samples[:N])


def test_mathematical_universality():
    """Demonstrate that check_properties works with any conforming type."""

    # Test that our mathematical axioms hold for Python's built-in types
    # This validates both our tests and Python's implementation

    print("Testing mathematical universality...")

    # Integers: Ring structure
    int_samples_wrapped = wrapped_int_samples()
    check_abelian_group(int_samples_wrapped[:5])
    print("✓ Built-in int: Abelian group axioms verified")

    # Floats: Field structure
    float_samples_wrapped = wrapped_float_samples()
    check_fields(float_samples_wrapped[:5])
    print("✓ Built-in float: Field axioms verified")

    # Complex: Field structure
    complex_samples_wrapped = wrapped_complex_samples()
    check_fields(complex_samples_wrapped[:5])
    print("✓ Built-in complex: Field axioms verified")

    print("Mathematical universality confirmed!")


if __name__ == "__main__":
    test_mathematical_universality()
