# Using Equations in SymPy Simplification

SymPy doesn't have a built-in "assume equation is true" mechanism for simplification, but you can work around it using
substitution and rewriting. This guide shows how to incorporate known equations (like Euler-Lagrange) into
simplification.

## 1. Manual Substitution with `.subs()`

If you have an equation, extract the relationship and substitute:

```python
from sympy import symbols, diff, Function, Eq, simplify

t = symbols('t')
x = Function('x')(t)

# Euler-Lagrange equation (example): d²x/dt² + x = 0
euler_lagrange = Eq(diff(x, t, 2) + x, 0)

# Extract: d²x/dt² = -x
second_deriv = diff(x, t, 2)

# Now when simplifying other expressions, substitute:
expr = diff(x, t, 2) + 2 * x
simplified = expr.subs(second_deriv, -x)  # Uses the EL equation
print(simplified)  # x (instead of d²x/dt² + 2x)
```

## 2. Solve for One Term and Substitute

```python
from sympy import solve

# Euler-Lagrange: m·d²x/dt² = -2x
m = symbols('m', positive=True)
euler_lagrange = Eq(m * diff(x, t, 2), -2 * x)

# Solve for d²x/dt²
solution = solve(euler_lagrange, diff(x, t, 2))[0]  # -2*x/m

# Use in other expressions
expr = m * diff(x, t, 2) + 3 * x
simplified = expr.subs(diff(x, t, 2), solution)
simplified = simplify(simplified)
print(simplified)  # x (since m*(-2x/m) + 3x = x)
```

## 3. For Multiple Equations: Use `eliminate()`

```python
from sympy import eliminate

# System: Euler-Lagrange for x_1, x_2, x_3
x1, x2, x3 = [Function(f'x_{i}')(t) for i in [1, 2, 3]]
m = symbols('m', positive=True)

eqs = [
    Eq(m * diff(x1, t, 2), -2 * x1),
    Eq(m * diff(x2, t, 2), -2 * x2),
    Eq(m * diff(x3, t, 2), -2 * x3),
]

# Eliminate second derivatives from another expression
# (This is more complex and context-dependent)
```

## 4. Create Substitution Dictionary from Equation

```python
def eq_to_subs(eq, solve_for):
    """Convert equation to substitution dictionary."""
    from sympy import solve
    solution = solve(eq, solve_for)[0]
    return {solve_for: solution}


# Euler-Lagrange: m·x''(t) + 2x(t) = 0
euler_lagrange = Eq(m * diff(x, t, 2) + 2 * x, 0)

# Create substitution dict
subs_dict = eq_to_subs(euler_lagrange, diff(x, t, 2))
# {Derivative(x(t), (t, 2)): -2*x(t)/m}

# Use it
expr = m * diff(x, t, 2) + 5 * x
simplified = expr.subs(subs_dict).simplify()
print(simplified)  # 3*x(t)
```

## 5. Pattern Matching with `.replace()`

For more complex pattern-based substitution:

```python
# Replace any occurrence of the pattern
expr = expr.replace(diff(x, t, 2), -2 * x / m)
```

## Practical Example: Euler-Lagrange and Energy Conservation

```python
from sympy import *

t = symbols('t', real=True)
m = symbols('m', positive=True)
x = Function('x', real=True)(t)

# Euler-Lagrange gives: m·x''(t) = -2·x(t)
euler_lagrange = Eq(m * diff(x, t, 2), -2 * x)

# Solve for x''(t)
x_ddot_expr = solve(euler_lagrange, diff(x, t, 2))[0]

# Now any expression involving x''(t) can use this:
energy = m * diff(x, t) ** 2 / 2 + x ** 2  # Kinetic + potential

# Compute time derivative
dE_dt = diff(energy, t)
print("Before substitution:")
pprint(dE_dt)

# Substitute Euler-Lagrange relation
dE_dt_simplified = dE_dt.subs(diff(x, t, 2), x_ddot_expr)
dE_dt_simplified = simplify(dE_dt_simplified)
print("\nAfter using Euler-Lagrange:")
pprint(dE_dt_simplified)  # Should be 0 (energy conservation)
```

## Complete Example: Verifying Energy Conservation

```python
from sympy import symbols, Function, diff, Eq, solve, simplify, pprint

# Setup
t = symbols('t', real=True)
m, k = symbols('m k', positive=True)
x = Function('x', real=True)(t)

# Lagrangian: L = (m/2)v² - (k/2)x²
v = diff(x, t)
L = m * v ** 2 / 2 - k * x ** 2 / 2

# Euler-Lagrange equation: d/dt(∂L/∂v) - ∂L/∂x = 0
dL_dv = diff(L, v)
dL_dx = diff(L, x)
euler_lagrange = Eq(diff(dL_dv, t) - dL_dx, 0)

print("Euler-Lagrange equation:")
pprint(euler_lagrange)
# m·x''(t) + k·x(t) = 0

# Solve for x''(t)
x_ddot = solve(euler_lagrange, diff(x, t, 2))[0]
print("\nSolved for x''(t):")
pprint(x_ddot)
# -k·x(t)/m

# Total energy
E = m * v ** 2 / 2 + k * x ** 2 / 2  # Kinetic + Potential

# Verify energy conservation: dE/dt should be 0
dE_dt = diff(E, t)
print("\ndE/dt before using Euler-Lagrange:")
pprint(dE_dt)

# Substitute Euler-Lagrange equation
dE_dt_simplified = dE_dt.subs(diff(x, t, 2), x_ddot)
dE_dt_simplified = simplify(dE_dt_simplified)

print("\ndE/dt after using Euler-Lagrange:")
pprint(dE_dt_simplified)
# 0 (energy is conserved!)

assert dE_dt_simplified == 0
print("\n✓ Energy conservation verified!")
```

## Summary

**Bottom line**: SymPy doesn't have automatic "assume equation" machinery, but `.subs()` combined with `solve()` is the
standard workflow for incorporating known equations into simplifications.

**Typical workflow:**

1. Define your equation with `Eq(lhs, rhs)`
2. Solve for the term you want to eliminate: `solve(eq, target)[0]`
3. Substitute in other expressions: `expr.subs(target, solution)`
4. Simplify: `simplify(result)`
