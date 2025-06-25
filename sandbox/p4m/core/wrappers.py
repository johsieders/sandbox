# p4m/core/wrappers.py

from .algebraic import EuclideanRing, Field

# --- Int ---

class Int(int, EuclideanRing):
    def __new__(cls, value):
        return int.__new__(cls, value)

    def __add__(self, other): return Int(int(self) + int(other))

    def __sub__(self, other): return Int(int(self) - int(other))

    def __mul__(self, other): return Int(int(self) * int(other))

    def __neg__(self): return Int(-int(self))

    def __eq__(self, other): return int(self) == int(other)

    @classmethod
    def zero(cls): return cls(0)

    @classmethod
    def one(cls): return cls(1)

    def __floordiv__(self, other): return Int(int(self) // int(other))

    def __mod__(self, other): return Int(int(self) % int(other))

    def divmod(self, other):
        q, r = divmod(int(self), int(other))
        return (Int(q), Int(r))

    def degree(self): return abs(int(self))

    def norm(self): return abs(int(self))

    def __str__(self): return str(int(self))


# --- Float ---

class Float(float, Field):
    def __new__(cls, value):
        return float.__new__(cls, value)

    def __add__(self, other): return Float(float(self) + float(other))

    def __sub__(self, other): return Float(float(self) - float(other))

    def __mul__(self, other): return Float(float(self) * float(other))

    def __neg__(self): return Float(-float(self))

    def __eq__(self, other): return float(self) == float(other)

    @classmethod
    def zero(cls): return cls(0.0)

    @classmethod
    def one(cls): return cls(1.0)

    def __floordiv__(self, other): return Float(float(self) // float(other))

    def __mod__(self, other): return Float(float(self) % float(other))

    def divmod(self, other):
        q, r = divmod(float(self), float(other))
        return (Float(q), Float(r))

    def degree(self): return abs(float(self))

    def norm(self): return abs(float(self))

    def __truediv__(self, other): return Float(float(self) / float(other))

    def inverse(self):
        if self == 0.0:
            raise ZeroDivisionError("Division by zero")
        return Float(1.0 / float(self))

    def __str__(self): return str(float(self))


# --- Complex ---

class Complex(complex, Field):
    def __new__(cls, value):
        if isinstance(value, complex):
            return complex.__new__(cls, value)
        return complex.__new__(cls, value)

    def __add__(self, other):
        return Complex(complex(self) + complex(other))

    def __sub__(self, other):
        return Complex(complex(self) - complex(other))

    def __mul__(self, other):
        return Complex(complex(self) * complex(other))

    def __neg__(self):
        return Complex(-complex(self))

    def __eq__(self, other):
        return complex(self) == complex(other)

    @classmethod
    def zero(cls):
        return cls(0 + 0j)

    @classmethod
    def one(cls):
        return cls(1 + 0j)

    def degree(self):
        return abs(complex(self))

    def norm(self):
        return abs(complex(self))

    def __truediv__(self, other):
        return Complex(complex(self) / complex(other))

    def inverse(self):
        if self == Complex.zero():
            raise ZeroDivisionError("Division by zero")
        return Complex(1.0 / complex(self))

    def __str__(self):
        return str(complex(self))


# --- Tensor  ---
# p4m/core/wrappers.py
# p4m/core/wrappers.py

import torch
from .algebraic import Ring

class Tensor(Ring):
    """Ring wrapper for torch.Tensor."""

    def __init__(self, data):
        if isinstance(data, torch.Tensor):
            self.data = data
        else:
            self.data = torch.tensor(data)

    def __add__(self, other):
        return Tensor(self.data + self._as_tensor(other))

    def __sub__(self, other):
        return Tensor(self.data - self._as_tensor(other))

    def __mul__(self, other):
        return Tensor(self.data * self._as_tensor(other))

    def __neg__(self):
        return Tensor(-self.data)

    def __eq__(self, other):
        other_tensor = self._as_tensor(other)
        # Use allclose for floats, equal for ints/bools
        if self.data.dtype.is_floating_point or other_tensor.dtype.is_floating_point:
            return torch.allclose(self.data, other_tensor, atol=1e-9)
        else:
            return torch.equal(self.data, other_tensor)

    def zero(self):
        """Return a zero tensor with the same shape/dtype/device as self."""
        return Tensor(torch.zeros_like(self.data))

    def one(self):
        """Return a one tensor with the same shape/dtype/device as self."""
        return Tensor(torch.ones_like(self.data))

    def norm(self):
        return self.data.norm().item()

    def __str__(self):
        return str(self.data)

    @staticmethod
    def _as_tensor(val):
        if isinstance(val, Tensor):
            return val.data
        elif isinstance(val, torch.Tensor):
            return val
        else:
            return torch.tensor(val)

