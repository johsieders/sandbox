# generated by GPT 4.1, 22.06.2025
# project Owner: Johannes Siedersleben
#
# Test driver for BoolStepfun
# Checks creation, evaluation, all logical ops, and pointwise comparison (<, <=, >, >=, ==, !=).
# Pytest compatible.

import operator

import pytest

from sandbox.stepfunctions.stepfun import AbstractStepfun, BoolStepfun, NumericStepfun


def test_aux():
    f = NumericStepfun([(None, 0)])
    g = BoolStepfun([(None, True)])


def test_eval_and_init_boolstepfun():
    f = BoolStepfun([(None, False), (1, True), (3, False)])
    assert f(-100) is False
    assert f(0) is False
    assert f(1) is True
    assert f(2.9) is True
    assert f(3) is False
    assert f(100) is False


def test_factory_detects_bool():
    f = AbstractStepfun.make_stepfun([(None, True), (2, False)])
    assert isinstance(f, BoolStepfun)
    assert f(1) is True
    assert f(3) is False


def test_and_or_xor_not():
    f = BoolStepfun([(None, False), (2, True)])
    g = BoolStepfun([(None, True), (3, False)])

    h_and = f & g
    # [-inf,2): False & True = False; [2,3): True & True = True; [3,∞): True & False = False
    assert h_and(-10) is False
    assert h_and(2.5) is True
    assert h_and(5) is False

    h_or = f | g
    # [-inf,2): False | True = True; [2,3): True | True = True; [3,∞): True | False = True
    assert h_or(-10) is True
    assert h_or(2.5) is True
    assert h_or(5) is True

    h_xor = f ^ g
    # [-inf,2): False ^ True = True; [2,3): True ^ True = False; [3,∞): True ^ False = True
    assert h_xor(-10) is True
    assert h_xor(2.5) is False
    assert h_xor(5) is True

    h_not = ~f
    # [-inf,2): not False = True; [2,∞): not True = False
    assert h_not(-1) is True
    assert h_not(3) is False


def test_comparisons():
    f = BoolStepfun([(None, False), (3, True)])
    g = BoolStepfun([(None, True), (3, False)])

    # Pointwise: [-inf,3): False < True (True), [3,∞): True < False (False) => overall False
    assert not (f < g)
    # Pointwise: [-inf,3): False <= True (True), [3,∞): True <= False (False) => overall False
    assert not (f <= g)
    # Pointwise: [-inf,3): False > True (False), [3,∞): True > False (True) => overall False
    assert not (f > g)
    # Pointwise: [-inf,3): False >= True (False), [3,∞): True >= False (True) => overall False
    assert not (f >= g)
    # Test all True (for <=, >=) if always satisfied
    h = BoolStepfun([(None, False), (3, False)])
    assert (h <= g)
    assert not (h > g)
    # == and !=
    assert not (f == g)
    assert (f != g)
    assert (h == h)


def test_factory_raises_on_mixed_types():
    with pytest.raises(TypeError):
        AbstractStepfun.make_stepfun([(None, True), (1, 5)])


def test_sum_and_multiply_bools():
    f = BoolStepfun([(None, False), (2, True)])
    g = BoolStepfun([(None, True), (3, False)])
    # & == multiply, | == sum, in bool logic
    assert (f & g).tv_list == (BoolStepfun._combine([f, g], operator.and_)).tv_list
    assert (f | g).tv_list == (BoolStepfun._combine([f, g], operator.or_)).tv_list
