from sympy import symbols, sin, Function
from sympy.abc import r, s, t

x_1, x_2, x_3 = symbols('x_1 x_2 x_3', real=True)
f = Function('f', real=True)(x_1, x_2, x_3)
expr1 = f + sin(x_1)

h = Function('h', real=True)(r, s, t)
expr2 = h + sin(r)

print("=" * 60)
print("The Bug: kwargs passes STRINGS, not Symbol objects")
print("=" * 60)


# This simulates what evaluate() does
def evaluate_buggy(expr, **kwargs):
    print(f"kwargs = {kwargs}")
    print(f"kwargs keys type: {type(list(kwargs.keys())[0])}")
    return expr.subs(kwargs)


result1 = evaluate_buggy(expr1, x_1=1, x_2=2)
print(f"Result for x_1 (with underscores): {result1}")
print()

result2 = evaluate_buggy(expr2, r=1, s=2)
print(f"Result for r (simple name): {result2}")
print()

print("=" * 60)
print("Why does 'r' work but 'x_1' doesn't?")
print("=" * 60)

# SymPy's .subs() can accept strings for simple symbol names
# but NOT for names with underscores when using kwargs!

# This works:
print("Test: expr2.subs({'r': 1, 's': 2})")
print(f"  Result: {expr2.subs({'r': 1, 's': 2})}")

# This doesn't:
print("Test: expr1.subs({'x_1': 1, 'x_2': 2})")
print(f"  Result: {expr1.subs({'x_1': 1, 'x_2': 2})}")
