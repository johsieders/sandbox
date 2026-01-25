from sympy import symbols, sin, Function
from sympy.abc import r, s, t

# Test 1: Symbols with underscores
x_1, x_2, x_3 = symbols('x_1 x_2 x_3', real=True)
f = Function('f', real=True)(x_1, x_2, x_3)
expr1 = f + sin(x_1)

print("=" * 60)
print("Test 1: Symbols with underscores")
print("=" * 60)
print(f"x_1 symbol: {x_1}")
print(f"x_1 name: {x_1.name}")
print(f"f = {f}")
print(f"f.args = {f.args}")
print(f"expr1 = {expr1}")
print(f"Free symbols in expr1: {expr1.free_symbols}")
print(f"Attempting substitution x_1=1, x_2=2:")
result1 = expr1.subs({x_1: 1, x_2: 2})
print(f"Result: {result1}")
print()

# Test 2: Simple symbols from sympy.abc
h = Function('h', real=True)(r, s, t)
expr2 = h + sin(r)

print("=" * 60)
print("Test 2: Simple symbols from sympy.abc")
print("=" * 60)
print(f"r symbol: {r}")
print(f"r name: {r.name}")
print(f"h = {h}")
print(f"h.args = {h.args}")
print(f"expr2 = {expr2}")
print(f"Free symbols in expr2: {expr2.free_symbols}")
print(f"Attempting substitution r=1, s=2:")
result2 = expr2.subs({r: 1, s: 2})
print(f"Result: {result2}")
print()

# Test 3: Check if issue is with Function definition
print("=" * 60)
print("Test 3: Comparing Function behavior")
print("=" * 60)
print(f"Is x_1 in expr1.free_symbols? {x_1 in expr1.free_symbols}")
print(f"Is r in expr2.free_symbols? {r in expr2.free_symbols}")
print(f"x_1 assumptions: {x_1.assumptions0}")
print(f"r assumptions: {r.assumptions0}")
