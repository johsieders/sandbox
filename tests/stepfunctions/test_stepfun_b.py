# generated by GPT 4.1, 22.06.2025
# project Owner: Johannes Siedersleben
#

from sandbox.stepfunctions.stepfun import NumericStepfun as Stepfun


def tv(*pairs):
    return tuple(pairs)


def test_undefined_everywhere():
    f = Stepfun(tv((0, None)))
    assert f(0) is None
    assert f(100) is None


def test_blank_intervals():
    f = Stepfun(tv((0, 10), (2, None), (5, 20)))
    assert f(1) == 10
    assert f(3) is None
    assert f(5) == 20


def test_arbitrary_non_numeric_values():
    f = Stepfun(tv((0, 10), (2, "Hello"), (5, 20)))
    assert f(1) == 10
    assert f(3) == "Hello"
    assert f(6) == 20


def test_add_ignores_non_numeric():
    f = Stepfun(tv((0, 10), (2, None), (5, 20)))
    g = Stepfun(tv((0, 2), (3, 3), (5, "x")))
    # [0,2): 10+2 = 12
    assert (f + g)(1) == 12
    # [2,3): None + 2 = None
    assert (f + g)(2.5) is None
    # [3,5): None + 3 = None
    assert (f + g)(4) is None
    # [5,inf): 20 + "x" = "x"
    assert (f + g)(5.5) == "x"


def test_comparison_with_blanks():
    f = Stepfun(tv((0, 1), (2, None), (5, 1)))
    g = Stepfun(tv((0, 2), (2, 2), (5, 2)))
    # f-g is undefined on [2,5), so f < g and f > g are both False
    assert not (f < g)
    assert not (f > g)


def test_equality_with_blanks():
    f = Stepfun(tv((0, None), (5, 10)))
    g = Stepfun(tv((0, None), (5, 10)))
    assert f == g


def test_integrate_ignores_non_numeric():
    f = Stepfun(tv((0, 10), (2, None), (5, 20)))
    # [0,2): value=10; [2,5): None (ignored); [5,7): value=20
    assert f.integrate(0, 7) == 2 * 10 + 2 * 20


def test_abs_neg_with_non_numeric():
    f = Stepfun(tv((0, -10), (2, None), (5, 10)))
    assert abs(f)(0.5) == 10
    assert abs(f)(3) is None
    assert abs(f)(6) == 10
    assert (-f)(0) == 10  # -(-10) = 10
    assert (-f)(3) is None


def test_str_repr_with_blanks():
    f = Stepfun(tv((0, None), (3, "hello"), (6, 5)))
    assert "None" in repr(f)
    assert "hello" in str(f)


def test_division_numerical():
    f = Stepfun(tv((0, 10), (5, 20)))
    g = Stepfun(tv((0, 2), (5, 4)))
    h = f / g
    assert h(1) == 5  # 10/2
    assert h(5.5) == 5  # 20/4


def test_division_by_zero():
    f = Stepfun(tv((0, 10), (5, 20)))
    g = Stepfun(tv((0, 2), (5, 0)))
    h = f / g
    assert h(1) == 5  # 10/2
    # Division by zero yields error/indicator, e.g., "division by zero"
    val = h(5.5)
    assert val == "DIV/0"  # Implementation defined; see below


def test_division_by_non_numeric():
    f = Stepfun(tv((0, 10), (5, 20)))
    g = Stepfun(tv((0, 2), (5, None)))
    h = f / g
    assert h(1) == 5  # 10/2
    assert h(5.5) is None  # Divided by None yields None


def test_division_with_blank_numerator():
    f = Stepfun(tv((0, None), (5, 20)))
    g = Stepfun(tv((0, 2), (5, 2)))
    h = f / g
    assert h(1) is None  # None / 2 is None
    assert h(6) == 10  # 20 / 2


def test_division_with_both_non_numeric():
    f = Stepfun(tv((0, None), (5, "foo")))
    g = Stepfun(tv((0, "bar"), (5, 2)))
    h = f / g
    assert h(1) is None
    assert h(5.5) == "foo"  # non-numeric / numeric yields non-numeric


def test_division_repr_str():
    f = Stepfun(tv((0, 10), (5, 0)))
    g = Stepfun(tv((0, 2), (5, 4)))
    h = f / g
    assert isinstance(str(h), str)
    assert isinstance(repr(h), str)
