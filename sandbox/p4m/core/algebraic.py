# p4m/core/algebraic.py

from abc import ABC, abstractmethod


class Ring(ABC):
    """Abstract base class for Rings."""

    @abstractmethod
    def __add__(self, other): ...

    @abstractmethod
    def __sub__(self, other): ...

    @abstractmethod
    def __mul__(self, other): ...

    @abstractmethod
    def __neg__(self): ...

    @abstractmethod
    def __eq__(self, other): ...

    # @classmethod
    @abstractmethod
    def zero(cls): ...

    # @classmethod
    @abstractmethod
    def one(cls): ...

    @abstractmethod
    def norm(self):
        """A non-negative measure of the element's 'size' (default: abs value)."""
        ...


class EuclideanRing(Ring):
    @abstractmethod
    def __floordiv__(self, other): ...

    @abstractmethod
    def __mod__(self, other): ...

    @abstractmethod
    def divmod(self, other): ...

    @abstractmethod
    def degree(self): ...


class Field(EuclideanRing):
    @abstractmethod
    def __truediv__(self, other): ...

    @abstractmethod
    def inverse(self): ...

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __mod__(self, other):
        return self.zero()

    def divmod(self, other):
        return (self.__truediv__(other), self.zero())
