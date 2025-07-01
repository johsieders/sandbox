# tests/py4m/make_samples.py

from itertools import cycle
from typing import Any, Sequence

from sandbox.py4m.mapper.m_complex import Complex
from sandbox.py4m.mapper.m_fraction import Fraction
from sandbox.py4m.mapper.m_matrix import Matrix
from sandbox.py4m.mapper.m_polynomial import Polynomial
from sandbox.py4m.wrapper.w_complex import NativeComplex
from sandbox.py4m.wrapper.w_float import NativeFloat
from sandbox.py4m.wrapper.w_int import NativeInt

# --------------------------
# 1. Base sample generators
# --------------------------

R = "Ring"
E = "EuclideanRing"
F = "Field"

RANK = {R: 1, E: 2, F: 3, int: -1, float: -1, complex: -1}

REQUIRES = 0
RETURNS = 1
NEEDS = 2
FORMAT = 3

NO_ARG = 0
STAR_ARG = 1
TUPLE_ARG = 2
MATRIX_ARG = 3

MAP = {
    int: ("builtin", int, lambda: (0,), NO_ARG),
    float: ("builtin", float, lambda: (0,), NO_ARG),
    complex: ("builtin", complex, lambda: (2,), STAR_ARG),
    NativeInt: (int, E, lambda: (1,), STAR_ARG),
    NativeFloat: (float, F, lambda: (1,), STAR_ARG),
    NativeComplex: (complex, F, lambda: (1,), STAR_ARG),
    Complex: (F, F, lambda: (1,), STAR_ARG),
    Fraction: (E, F, lambda: (2,), STAR_ARG),
    Polynomial: (E, E, lambda: next(POLY_CYCLE), STAR_ARG),
    Matrix: (R, R, lambda: next(MATRIX_CYCLE), MATRIX_ARG),
}

POLY_CYCLE = cycle((k,) for k in range(4, 5))
MATRIX_CYCLE = cycle((k, k) for k in range(4, 5))


def satisfies_requirement(receiver: Any, producer: Any) -> bool:
    """Return True if producer satisfies the mapper requirement"""
    rank_required = RANK[MAP[receiver][REQUIRES]]  # what the receiver requires
    rank_provided = RANK[MAP[producer][RETURNS]]  # what the producer returns
    return rank_required <= rank_provided


# --- Sample composition ---

def make_flat_samples(type: Any, samples: Sequence[int | float | complex]) -> list[Any]:
    """
    Create objects of 'type' using data in 'samples', according to the constructor arity specified in MAP[type][NEEDS]().
    - type: a class (wrapper/mapper)
    - samples: flat Sequence of elements (already-wrapped or builtins)
    Returns: list of constructed objects.
    """
    if not samples:
        return []
        # Check type requirements
    if not satisfies_requirement(type, samples[0].__class__):
        raise TypeError(
            f"{type.__name__} requires {MAP[type][REQUIRES]}, "
            f"but got {samples[0].__class__.__name__} "
            f"(returns {MAP[samples[0].__class__][RETURNS]})"
        )
    # Read the samples in chunks with size == arg_needed
    # Example 1: args_needed == (2,): pass two elements from samples to result
    # Example 2: args_needed == (3, 3): pass 9 elements from samples to result as a 3x3 matrix (tuple of tuple)
    #
    # walk through samples, make chunks of required size (called args), apply type and append to result
    # stop, if you cannot fill the last chunk and ignore the rest.
    # producing Fractions from 9 ints would give 4 Fractions
    #
    sample_len = len(samples)
    result = []
    index = 0
    while True:
        args_needed = MAP[type][NEEDS]()
        args_format = MAP[type][FORMAT]
        n = args_needed[0]
        if len(args_needed) not in (1, 2):
            raise NotImplementedError(
                f"Cannot handle argument shape {args_needed} for {type.__name__}"
            )
        elif len(args_needed) == 1 and index + n <= sample_len:
            args = samples[index:index + n]
            if args_format == STAR_ARG:
                result.append(type(*args))
            else:
                result.append(type(args))
            index += n
        elif len(args_needed) == 2 and index + n ** 2 < sample_len:
            args = []
            for row in range(n):
                args.append(samples[index:index + n])
                index += n
            result.append(type(args))
        else:
            return result


def make_samples(types: Sequence[Any], samples: Sequence[Any]) -> list:
    """
    Compose mappers/wrappers and produce legal sample objects.
    types: outermost to innermost
    samples: a list of builtin types (int, float, complex), or already-wrapped elements
    """
    result = samples
    types = list(types)
    types.reverse()
    for t in types:
        result = make_flat_samples(t, result)
    return result
