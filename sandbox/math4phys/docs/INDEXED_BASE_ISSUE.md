# IndexedBase vs Symbols: Mixed Partial Derivatives Issue

## Problem Summary

SymPy's `IndexedBase` doesn't automatically recognize that mixed partial derivatives commute (Schwarz's theorem),
causing vector calculus identities to fail.

## Demonstration

### With Regular Symbols (Works ✓)

```python
from sympy import symbols, Function

x = symbols('x_1:4', real=True)  # (x_1, x_2, x_3)
f = Function('f', real=True)(*x)

f_12 = f.diff(x[0]).diff(x[1])  # ∂²f/∂x₁∂x₂
f_21 = f.diff(x[1]).diff(x[0])  # ∂²f/∂x₂∂x₁

print(f_12 == f_21)  # True ✓
print(f_12 - f_21)   # 0 ✓
```

### With IndexedBase (Fails ✗)

```python
from sympy import IndexedBase, Function

x = IndexedBase('x', real=True)
x_list = [x[i] for i in range(1, 4)]  # [x[1], x[2], x[3]]
f = Function('f', real=True)(*x_list)

f_12 = f.diff(x_list[0]).diff(x_list[1])  # ∂²f/∂x[1]∂x[2]
f_21 = f.diff(x_list[1]).diff(x_list[0])  # ∂²f/∂x[2]∂x[1]

print(f_12 == f_21)  # False ✗
print(f_12 - f_21)   # Derivative(...) - Derivative(...) ✗
```

## Impact on Vector Calculus

This breaks fundamental vector calculus identities:

1. **div(curl(F)) = 0** - Fails because mixed partials don't cancel
2. **curl(grad(f)) = 0** - Fails for the same reason
3. **curl(curl(F)) = grad(div(F)) - lap(F)** - Fails

## Recommendations

### For Symbolic Vector Calculus: Use Regular Symbols

```python
# ✓ RECOMMENDED
x = symbols('x_1:4', real=True)
p = symbols('p_1:4', real=True)
```

**Advantages:**

- Mixed partials commute automatically
- All vector calculus identities work
- Cleaner mathematical notation
- SymPy better optimized for this use case

### When to Use IndexedBase

Use IndexedBase for:

- Tensor algebra (summation convention)
- Array/matrix indexing notation
- Code generation
- When you're NOT doing symbolic differentiation

**NOT recommended for:**

- Symbolic vector calculus
- Computing gradients, curls, divergences
- Verifying differential identities

## Workarounds (if you must use IndexedBase)

1. **Manual simplification**: After computing expressions, manually apply rules for mixed partial equality
2. **Custom simplify function**: Write a function that canonicalizes derivative orders
3. **Hybrid approach**: Use IndexedBase for display, convert to regular symbols for computation

## Bottom Line

**For scratch-0.py to work like scratch-0a.py: Use regular `symbols()` instead of `IndexedBase`.**

The mathematical notation `x[1], x[2], x[3]` looks nice, but SymPy's differentiation engine isn't designed to handle it
properly for symbolic calculus operations.
