# KI-Gilde
# QAware GmbH, Munich
# 10.3.2021
# revived 17.10.2025

import torch
from torch import Tensor, tensor

from sandbox.ai.binary_classifiers.classifier_fcts import _and, _or, _xor, circle, rings, square, plane


# Test data
X_BOOL = tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)


def test_and() -> None:
    """Test AND function on boolean inputs"""
    result = _and(X_BOOL)
    expected = tensor([[0.], [0.], [0.], [1.]])
    assert result.shape == (4, 1)
    assert torch.allclose(result, expected)


def test_or() -> None:
    """Test OR function on boolean inputs"""
    result = _or(X_BOOL)
    expected = tensor([[0.], [1.], [1.], [1.]])
    assert result.shape == (4, 1)
    assert torch.allclose(result, expected)


def test_xor() -> None:
    """Test XOR function on boolean inputs"""
    result = _xor(X_BOOL)
    expected = tensor([[0.], [1.], [1.], [0.]])
    assert result.shape == (4, 1)
    assert torch.allclose(result, expected)


def test_plane_and() -> None:
    """Test plane function configured for AND"""
    f_and = plane([1, 1], -1.5)
    result = f_and(X_BOOL)
    expected = tensor([[0.], [0.], [0.], [1.]])
    assert result.shape == (4, 1)
    assert torch.allclose(result, expected)


def test_plane_or() -> None:
    """Test plane function configured for OR"""
    f_or = plane([1, 1], -0.5)
    result = f_or(X_BOOL)
    expected = tensor([[0.], [1.], [1.], [1.]])
    assert result.shape == (4, 1)
    assert torch.allclose(result, expected)


def test_plane_general() -> None:
    """Test plane function with various configurations"""
    # Test vertical line at x=0.5
    f = plane([1, 0], -0.5)
    X = tensor([[0, 0], [0.5, 0], [1, 0]], dtype=torch.float32)
    result = f(X)
    expected = tensor([[0.], [1.], [1.]])
    assert torch.allclose(result, expected)


def test_circle_unit() -> None:
    """Test circle with radius 1"""
    c = circle(1)
    X = tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    result = c(X)

    # (0,0): norm=0 <= 1 -> 1
    # (0,1): norm=1 <= 1 -> 1
    # (1,0): norm=1 <= 1 -> 1
    # (1,1): norm=sqrt(2) > 1 -> 0
    expected = tensor([[1.], [1.], [1.], [0.]])
    assert result.shape == (4, 1)
    assert torch.allclose(result, expected)


def test_circle_various_radii() -> None:
    """Test circle with various radii"""
    X = tensor([[0, 0], [0.5, 0.5], [1, 1], [2, 0]], dtype=torch.float32)

    # radius=0.5: only origin inside
    c = circle(0.5)
    result = c(X)
    assert result[0].item() == 1.0  # origin
    assert result[2].item() == 0.0  # (1,1) outside

    # radius=2: more points inside
    c = circle(2)
    result = c(X)
    assert result[0].item() == 1.0  # origin
    assert result[3].item() == 1.0  # (2,0) inside


def test_square_unit() -> None:
    """Test square with half-side length 1"""
    s = square(1)
    X = tensor([[0, 0], [0.5, 0.5], [1, 0], [1, 1], [1.5, 0]], dtype=torch.float32)
    result = s(X)

    # max norm <= 1: inside
    # (0,0): max=0 -> 1
    # (0.5,0.5): max=0.5 -> 1
    # (1,0): max=1 -> 1
    # (1,1): max=1 -> 1
    # (1.5,0): max=1.5 -> 0
    expected = tensor([[1.], [1.], [1.], [1.], [0.]])
    assert result.shape == (5, 1)
    assert torch.allclose(result, expected)


def test_square_various_sizes() -> None:
    """Test square with various sizes"""
    X = tensor([[0, 0], [0.5, 0.5], [2, 0]], dtype=torch.float32)

    # half-side=0.5
    s = square(0.5)
    result = s(X)
    assert result[0].item() == 1.0  # origin
    assert result[1].item() == 1.0  # (0.5,0.5) on boundary
    assert result[2].item() == 0.0  # (2,0) outside


def test_rings_basic() -> None:
    """Test rings function with radius 1"""
    r = rings(1)
    X = tensor([[0, 0], [0, 0.5], [0, 1], [0, 1.5], [0, 2]], dtype=torch.float32)
    result = r(X)

    # norm=0: 0//1=0, 1-0%2=1
    # norm=0.5: 0//1=0, 1-0%2=1
    # norm=1: 1//1=1, 1-1%2=0
    # norm=1.5: 1//1=1, 1-1%2=0
    # norm=2: 2//1=2, 1-2%2=1
    expected = tensor([[1.], [1.], [0.], [0.], [1.]])
    assert result.shape == (5, 1)
    assert torch.allclose(result, expected)


def test_rings_alternating_pattern() -> None:
    """Test rings create alternating pattern"""
    r = rings(1)

    # Points at increasing distances
    X = tensor([[0, 0], [0, 0.9], [0, 1.5], [0, 2.5], [0, 3.5]], dtype=torch.float32)
    result = r(X)

    # Check pattern: norm//1 gives ring index, pattern alternates with %2
    # 0: 0//1=0, 1-0%2=1
    # 0.9: 0//1=0, 1-0%2=1
    # 1.5: 1//1=1, 1-1%2=0
    # 2.5: 2//1=2, 1-2%2=1
    # 3.5: 3//1=3, 1-3%2=0
    assert result.shape == (5, 1)
    assert result[0].item() == 1.0  # first ring
    assert result[1].item() == 1.0  # first ring
    assert result[2].item() == 0.0  # second ring
    assert result[3].item() == 1.0  # third ring
    assert result[4].item() == 0.0  # fourth ring


def test_functions_return_correct_shape() -> None:
    """Test all functions return correct output shape"""
    X = tensor([[0, 0], [1, 1], [2, 2]], dtype=torch.float32)

    assert _and(X[:, :2]).shape == (3, 1)
    assert _or(X[:, :2]).shape == (3, 1)
    assert _xor(X[:, :2]).shape == (3, 1)
    assert circle(1)(X).shape == (3, 1)
    assert square(1)(X).shape == (3, 1)
    assert rings(1)(X).shape == (3, 1)
    assert plane([1, 1], 0)(X).shape == (3, 1)


def test_boolean_functions_with_floats() -> None:
    """Test boolean functions work with float values"""
    X = tensor([[0.5, 0.5], [0.3, 0.7], [1.0, 0.0]], dtype=torch.float32)

    result_and = _and(X)
    result_or = _or(X)
    result_xor = _xor(X)

    assert result_and.shape == (3, 1)
    assert result_or.shape == (3, 1)
    assert result_xor.shape == (3, 1)

    # Verify formulas with specific values
    assert torch.isclose(result_and[0], tensor(0.25))  # 0.5 * 0.5
    assert torch.isclose(result_or[0], tensor(0.75))  # 0.5 + 0.5 - 0.25
    assert torch.isclose(result_xor[0], tensor(0.5))  # 0.5 + 0.5 - 2*0.25
