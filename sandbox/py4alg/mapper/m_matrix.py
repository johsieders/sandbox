from __future__ import annotations

from math import sqrt

from sandbox.py4alg.protocols.p_ring import Ring
from sandbox.py4alg.util.utils import close_to
from sandbox.py4alg.cockpit import AlgebraicType


class Matrix[T: Ring]:

    functor_map = \
        {AlgebraicType.RING: AlgebraicType.RING,
         AlgebraicType.COMMUTATIVE_RING: AlgebraicType.RING,
         AlgebraicType.EUCLIDEAN_RING: AlgebraicType.RING,
         AlgebraicType.FIELD: AlgebraicType.RING}

    def __init__(self, *args: T | Matrix[T]):
        """
        Accepts either:
        - n^2 entries of type T (creates an n x n matrix)
        - n^2 Matrix[T] blocks of equal size m x m (creates a block matrix of size (n*m) x (n*m))
        """
        count = len(args)
        n = int(sqrt(count))
        if n == 0 or n ** 2 != count:
            raise TypeError(f"expected n^2 arguments, got {count}")

        # Block matrix case
        if isinstance(args[0], Matrix):
            # All blocks must be matrices of the same size
            m = args[0]._size
            if not all(isinstance(x, Matrix) and x._size == m for x in args):
                raise TypeError("All blocks must be Matrix objects of the same size")

            self._descent = args[0].descent()
            self._implements = args[0].implements()
            self._size = n * m
            # Build the block matrix using tuple-of-tuples for immutability
            rows = []
            for block_row in range(n):
                for inner_row in range(m):
                    row = []
                    for block_col in range(n):
                        block = args[block_row * n + block_col]
                        row.extend(block[inner_row])
                    rows.append(tuple(row))
            self._data = tuple(rows)
        else:
            # Scalar matrix case
            self._descent = [Matrix] + args[0].descent()
            self._implements = self.functor_map[args[0].implements()]
            self._size = n
            self._data = tuple(
                tuple(args[i * n + j] for j in range(n))
                for i in range(n)
            )

    def __add__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        data = []
        for row_a, row_b in zip(self._data, other._data):
            data += [a + b for a, b in zip(row_a, row_b)]
        return Matrix(*data)

    def __sub__(self, other: Matrix[T]) -> Matrix[T]:
        self._check_shape(other)
        data = []
        for row_a, row_b in zip(self._data, other._data):
            data += [a - b for a, b in zip(row_a, row_b)]
        return Matrix(*data)

    def __mul__(self, other: Matrix[T]) -> Matrix[T]:
        # Matrix multiplication
        if self._size != other._size:
            raise ValueError("Incompatible shapes for multiplication")
        data = []
        for i in range(self._size):
            for j in range(other._size):
                val = self._data[i][0] * other._data[0][j]
                for k in range(1, self._size):
                    val += self._data[i][k] * other._data[k][j]
                data.append(val)

        return Matrix(*data)

    def __neg__(self) -> Matrix[T]:
        data = []
        for row in self._data:
            data += [-a for a in row]
        return Matrix(*data)

    def __eq__(self, other: object) -> bool:
        return (
                isinstance(other, Matrix)
                and self._size == other._size
                and close_to(self, other)
        )

    def zero(self) -> Matrix[T]:
        """Return the zero matrix of the same shape and type as self."""
        zero = self._data[0][0].zero()
        return Matrix(*[zero for _ in range(self._size) for _ in range(self._size)])

    def one(self) -> Matrix[T]:
        """Return the identity matrix of the same shape and type as self (square only)."""
        zero = self._data[0][0].zero()
        one = self._data[0][0].one()
        return Matrix(*[
            one if i == j else zero
            for j in range(self._size)
            for i in range(self._size)])

    def norm(self) -> float:
        return max(a.norm() for row in self._data for a in row)

    def degree(self) -> int:
        return max(a.degree() for row in self._data for a in row)

    def shape(self) -> tuple[int, int]:
        return (self._size, self._size)

    def to_tuples(self) -> tuple[tuple[T, ...], ...]:
        return self._data

    def __str__(self) -> str:
        return "\n[" + "\n".join("[" + ", ".join(str(a) for a in row) + "]," for row in self._data) + "]"
        # return str(self._data)

    def __repr__(self) -> str:
        return f"Matrix({self._data})"

    def _check_shape(self, other: Matrix[T]):
        if not isinstance(other, Matrix):
            raise TypeError("Can only operate with another Matrix of same type.")
        if self.shape() != other.shape():
            raise ValueError(f"Matrix shape mismatch: {self.shape()} != {other.shape()}")

    # Optionally, support item access
    def __getitem__(self, idx):
        return self._data[idx]

    def descent(self):
        return self._descent

    def implements(self):
        return self._implements
