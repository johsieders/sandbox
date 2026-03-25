"""
Euler-Lagrange equation via sympy's LagrangesMethod.

Plain vanilla case: T = 1/2 m x_dot^2, L = T - V(x), no constraints.

LagrangesMethod API
===================
Constructor:
    LagrangesMethod(Lagrangian, qs, forcelist=None, bodies=None, frame=None,
                    hol_coneqs=None, nonhol_coneqs=None)

    For the plain conservative case only two arguments are needed:
        - Lagrangian:  a sympy expression L = T - V
        - qs:          list of generalized coordinates (dynamicsymbols)
    The remaining arguments (forcelist, frame, constraints) are for
    non-conservative forces and constrained systems.

Generalized coordinates:
    dynamicsymbols('x')     creates x(t), an implicit function of t.
    dynamicsymbols('x', 1)  creates d/dt x(t), the first time derivative.
    These are the building blocks for T and V.

Workflow:
    1. LM = LagrangesMethod(L, [x])
    2. eom = LM.form_lagranges_equations()   # must be called first
    3. Access results via properties and methods (see below).

    form_lagranges_equations() computes:
        d/dt (dL/d x_dot) - dL/dx = 0
    and returns the left-hand side as a Matrix (each row = 0).

Key properties after form_lagranges_equations():
    mass_matrix  Matrix M such that M * x'' = forcing
    forcing      Matrix f, everything except the x'' terms (sign-flipped)
                 Together: mass_matrix * [x''] = forcing, i.e. m x'' = -V'(x).

Key method:
    rhs()        Solves for the state derivative vector [x', x''].
                 Returns a column vector ready for numerical ODE integration:
                    [  x'(t)       ]
                    [ -V'(x(t))/m  ]

Three examples below:
    1. Generic V(x)         -->  m x'' + V'(x) = 0
    2. Harmonic oscillator  -->  m x'' + k x   = 0
    3. Free fall            -->  m x'' + m g   = 0
"""

from sympy import symbols, Function, Rational, pprint
from sympy.physics.mechanics import dynamicsymbols, LagrangesMethod

# --- Symbols and generalized coordinate ---
m = symbols('m', positive=True)
x = dynamicsymbols('x')        # x(t)
xdot = dynamicsymbols('x', 1)  # dx/dt

# --- Lagrangian with generic V(x) ---
V = Function('V')
T = Rational(1, 2) * m * xdot**2
L = T - V(x)

LM = LagrangesMethod(L, [x])
eom = LM.form_lagranges_equations()

print("=== Generic potential V(x) ===")
print("Euler-Lagrange equation (= 0):")
pprint(eom)
print("\nmass_matrix:", LM.mass_matrix)
print("forcing:    ", LM.forcing)
print("\nFirst-order form [x', x'']:")
pprint(LM.rhs())

# --- Harmonic oscillator: V = 1/2 k x^2 ---
k = symbols('k', positive=True)
L_ho = Rational(1, 2) * m * xdot**2 - Rational(1, 2) * k * x**2

LM_ho = LagrangesMethod(L_ho, [x])
eom_ho = LM_ho.form_lagranges_equations()

print("\n=== Harmonic oscillator V = 1/2 k x^2 ===")
print("EOM (= 0):")
pprint(eom_ho)
print("rhs:")
pprint(LM_ho.rhs())

# --- Free fall: V = m g x ---
g = symbols('g', positive=True)
L_ff = Rational(1, 2) * m * xdot**2 - m * g * x

LM_ff = LagrangesMethod(L_ff, [x])
eom_ff = LM_ff.form_lagranges_equations()

print("\n=== Free fall V = m g x ===")
print("EOM (= 0):")
pprint(eom_ff)
print("rhs:")
pprint(LM_ff.rhs())
