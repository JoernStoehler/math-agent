import numpy as np
import sympy as sp
from sympy import sin, cos, pi, solve, diff, simplify

# Define the parameter t symbolically
t = sp.Symbol('t', real=True)

# Define the curve components
x = sin(2*t) * cos(t)
y = sin(2*t) * sin(t)

# Calculate derivatives
dx_dt = diff(x, t)
dy_dt = diff(y, t)

print("Curve components:")
print(f"x(t) = {x}")
print(f"y(t) = {y}")
print()

print("First derivatives:")
print(f"x'(t) = {dx_dt}")
print(f"y'(t) = {dy_dt}")
print()

# Simplify derivatives
dx_dt_simplified = simplify(dx_dt)
dy_dt_simplified = simplify(dy_dt)

print("Simplified derivatives:")
print(f"x'(t) = {dx_dt_simplified}")
print(f"y'(t) = {dy_dt_simplified}")
print()

# Find singular points where both derivatives are zero
singular_eqs = [dx_dt_simplified, dy_dt_simplified]
print("Finding singular points by solving x'(t) = 0 and y'(t) = 0:")

# Solve for singular points
singular_sols = solve(singular_eqs, t)
print(f"Solutions: {singular_sols}")

# Check specific values
test_values = [0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4]
print("\nChecking specific t values:")
for t_val in test_values:
    x_val = float(x.subs(t, t_val))
    y_val = float(y.subs(t, t_val))
    dx_val = float(dx_dt_simplified.subs(t, t_val))
    dy_val = float(dy_dt_simplified.subs(t, t_val))
    print(f"t = {t_val}: f({t_val}) = ({x_val:.4f}, {y_val:.4f}), f'({t_val}) = ({dx_val:.4f}, {dy_val:.4f})")

# Find double points
print("\nLooking for double points (where f(t1) = f(t2) for t1 ≠ t2):")
# Using the fact that sin(2t)cos(t) = sin(2t)cos(t) and sin(2t)sin(t) = sin(2t)sin(t)
# We need sin(2t1)cos(t1) = sin(2t2)cos(t2) and sin(2t1)sin(t1) = sin(2t2)sin(t2)