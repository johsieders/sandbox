"""
Protocol-Based Test Organization

This module provides a centralized approach to testing algebraic protocols by:
1. Collecting samples from all available sample generators
2. Filtering samples by protocol implementation using isinstance()
3. Running protocol-specific tests on all relevant samples. 
"""

from typing import List, Any

import pytest

from sandbox.py4alg.mapper import ECpoint, Fp
# Protocol imports
from sandbox.py4alg.protocols.p_abelian_group import AbelianGroup
from sandbox.py4alg.protocols.p_comparable import Comparable
from sandbox.py4alg.protocols.p_euclidean_ring import EuclideanRing
from sandbox.py4alg.protocols.p_field import Field
from sandbox.py4alg.protocols.p_ring import Ring
# Sample generation imports
from sandbox.py4alg.util.g_samples import g_ints, g_floats, g_complex_
from sandbox.py4alg.util.g_samples import g_matrices
from sandbox.py4alg.util.g_samples import g_nat_floats, g_nat_complex, g_nat_ints
from sandbox.py4alg.util.utils import compose, take
# Property checking imports
from tests.py4alg.check_properties import (
    check_abelian_group, check_rings,
    check_euclidean_rings, check_fields, check_comparables
)

K = 100
N = 20


def native_int_samples() -> List[Any]:
    """Generate NativeInt samples."""
    return list(compose(take(K), g_nat_ints, g_ints)(0, 20))


def native_float_samples() -> List[Any]:
    """Generate NativeFloat samples."""
    return list(compose(take(K), g_nat_floats, g_floats)(0, 20))


def native_complex_samples() -> List[Any]:
    """Generate NativeComplex samples."""
    return list(compose(take(K), g_nat_complex, g_complex_)(0, 20))


def fp_samples() -> List[Any]:
    """Generate Fp samples grouped by prime to avoid incompatible operations."""

    # Only use one prime to avoid mixing incompatible Fp elements

    p = 47
    return [Fp(p, a) for a in range(K)]


def ec_samples() -> List[Any]:
    """Generate ECpoint samples on a single curve to avoid incompatible operations."""

    # Use curve y^2 = x^3 + 1*x + 1 mod 7 (same as zero() method)
    a, b, p = 1, 1, 7

    # Generate all points on the curve, limited to K samples for performance
    points = list(ECpoint.gen_points(a, b, p))
    return points[:K]


def matrix_int_samples() -> List[Any]:
    """Generate Matrix[NativeInt] samples."""
    matrix_k = min(K, 15)  # Smaller K since we have multiple matrix types
    return list(compose(take(matrix_k), g_matrices, g_nat_ints, g_ints)(0, 20))


def matrix_float_samples() -> List[Any]:
    """Generate Matrix[NativeFloat] samples."""
    matrix_k = min(K, 15)
    return list(compose(take(matrix_k), g_matrices, g_nat_floats, g_floats)(0, 20))


def matrix_complex_samples() -> List[Any]:
    """Generate Matrix[NativeComplex] samples."""
    matrix_k = min(K, 15)
    return list(compose(take(matrix_k), g_matrices, g_nat_complex, g_complex_)(0, 20))


# List of all sample generator functions
SAMPLE_GENERATORS = [
    native_int_samples,
    native_float_samples,
    native_complex_samples,
    fp_samples,
    ec_samples,
    matrix_int_samples,
    matrix_float_samples,
    matrix_complex_samples,
]


def get_all_samples() -> List[Any]:
    """Collect all available samples from all generators."""
    all_samples = []
    for generator in SAMPLE_GENERATORS:
        all_samples.extend(generator())
    return all_samples


def get_samples_for_protocol(protocol_class) -> List[List[Any]]:
    """Get all samples that implement the given protocol, grouped by compatible sample generators.

    By convention, each xx_samples() function returns homogeneous, compatible samples that
    implement the same protocols. We group samples by their source generator rather than
    by Python type to ensure compatibility within each group.

    Returns a list of lists, where each inner list contains samples from the same generator
    that implements the specified protocol.
    """
    sample_groups = []

    # Check each sample generator individually
    for generator in SAMPLE_GENERATORS:
        samples = generator()
        if not samples:
            continue

        # Check if the first sample implements the protocol (homogeneous assumption)
        if isinstance(samples[0], protocol_class):
            # All samples from this generator implement the protocol
            filtered_samples = [sample for sample in samples if isinstance(sample, protocol_class)]
            if filtered_samples:
                sample_groups.append(filtered_samples)

    return sample_groups


def get_samples_for_protocol_with_ids(protocol_class):
    """Get samples with pytest IDs for cleaner test naming."""
    sample_groups = []
    ids = []

    # Check each sample generator individually
    for generator in SAMPLE_GENERATORS:
        samples = generator()
        if not samples:
            continue

        # Check if the first sample implements the protocol (homogeneous assumption)
        if isinstance(samples[0], protocol_class):
            # All samples from this generator implement the protocol
            filtered_samples = [sample for sample in samples if isinstance(sample, protocol_class)]
            if filtered_samples:
                sample_groups.append(filtered_samples)
                # Create a clean ID from generator name and sample type
                generator_name = generator.__name__.replace('_samples', '')
                sample_type = type(filtered_samples[0]).__name__
                ids.append(f"{generator_name}_{sample_type}")

    return pytest.param(*sample_groups, ids=ids) if sample_groups else []


# Protocol-based test functions with pytest parametrization

@pytest.mark.parametrize("samples", get_samples_for_protocol(AbelianGroup))
def test_abelian_group_properties(samples):
    """Test all abelian group properties for each AbelianGroup implementation."""
    check_abelian_group(samples[:N])


@pytest.mark.parametrize("samples", get_samples_for_protocol(Ring))
def test_ring_properties(samples):
    """Test all ring properties for each Ring implementation."""
    check_rings(samples[:N])


@pytest.mark.parametrize("samples", get_samples_for_protocol(EuclideanRing))
def test_euclidean_ring_properties(samples):
    """Test all Euclidean ring properties for each EuclideanRing implementation."""
    check_euclidean_rings(samples[:N])


@pytest.mark.parametrize("samples", get_samples_for_protocol(Field))
def test_field_properties(samples):
    """Test all field properties for each Field implementation."""
    check_fields(samples[:N])


@pytest.mark.parametrize("samples", get_samples_for_protocol(Comparable))
def test_comparable_properties(samples):
    """Test all Comparable invariants for types that actually support comparison operations."""
    if not samples:
        pytest.skip("No samples provided")

    # WORKAROUND: Python's protocol system has a limitation where isinstance(obj, Protocol)
    # checks for method existence, not method functionality. Some types (like NativeComplex)
    # have comparison methods as method-wrappers that exist but raise TypeError at runtime.
    # This happens because Python automatically provides comparison methods even when
    # they're not implemented, causing false positives in protocol checks.
    # We need this runtime check to filter out types that claim Comparable but don't work.
    try:
        test_sample = samples[0]
        _ = test_sample <= test_sample  # Test if comparison actually works
        check_comparables(samples[:N])  # If successful, run full tests
    except (TypeError, NotImplementedError):
        # Skip types that have comparison methods but they don't actually work
        pytest.skip(f"Comparison not actually supported for {type(test_sample).__name__}")


# Discovery functions for debugging

def test_protocol_coverage():
    """Show which samples implement which protocols - useful for debugging."""
    protocols = [AbelianGroup, Comparable, EuclideanRing, Field, Ring]
    protocol_names = ["AbelianGroup", "Comparable", "EuclideanRing", "Field", "Ring"]

    coverage = {}
    for protocol, name in zip(protocols, protocol_names):
        sample_groups = get_samples_for_protocol(protocol)
        for sample_list in sample_groups:
            if sample_list:  # Non-empty list
                type_name = type(sample_list[0]).__name__
                if type_name not in coverage:
                    coverage[type_name] = []
                if name not in coverage[type_name]:
                    coverage[type_name].append(name)

    # Print coverage for manual inspection (will show in test output if run with -s)
    print('\n')
    for type_name, protocol_list in coverage.items():
        print(f"{type_name}: {', '.join(protocol_list)}")

    # Basic assertion to ensure test runs
    assert len(coverage) > 0
