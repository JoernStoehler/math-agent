import numpy as np
import sympy as sp

# Define the symbolic variables
t, c = sp.symbols('t c', real=True, positive=True)

# Define the parametric curve
x = sp.exp(c*t) * sp.cos(t)
y = sp.exp(c*t) * sp.sin(t)

# Calculate derivatives
dx_dt = sp.diff(x, t)
dy_dt = sp.diff(y, t)

print("f(t) = (e^(ct)cos(t), e^(ct)sin(t))")
print(f"\nx(t) = {x}")
print(f"y(t) = {y}")

print(f"\ndx/dt = {dx_dt}")
print(f"dy/dt = {dy_dt}")

# Simplify the derivatives
dx_dt_simplified = sp.simplify(dx_dt)
dy_dt_simplified = sp.simplify(dy_dt)

print(f"\nSimplified dx/dt = {dx_dt_simplified}")
print(f"Simplified dy/dt = {dy_dt_simplified}")

# Calculate (dx/dt)^2 + (dy/dt)^2
speed_squared = dx_dt**2 + dy_dt**2
speed_squared_simplified = sp.simplify(speed_squared)

print(f"\n(dx/dt)^2 + (dy/dt)^2 = {speed_squared_simplified}")

# Factor out e^(2ct)
speed_squared_factored = sp.factor(speed_squared_simplified)
print(f"\nFactored: {speed_squared_factored}")

# Calculate the speed |f'(t)|
speed = sp.sqrt(speed_squared_simplified)
speed_simplified = sp.simplify(speed)

print(f"\n|f'(t)| = sqrt((dx/dt)^2 + (dy/dt)^2) = {speed_simplified}")

# The arc length integral from -infinity to 0
print("\nArc length = integral from -infinity to 0 of |f'(t)| dt")
print(f"         = integral from -infinity to 0 of {speed_simplified} dt")

# For the specific calculation
print("\nLet's verify with manual calculation:")
print("dx/dt = c*e^(ct)*cos(t) - e^(ct)*sin(t) = e^(ct)*(c*cos(t) - sin(t))")
print("dy/dt = c*e^(ct)*sin(t) + e^(ct)*cos(t) = e^(ct)*(c*sin(t) + cos(t))")
print("\n(dx/dt)^2 + (dy/dt)^2 = e^(2ct) * [(c*cos(t) - sin(t))^2 + (c*sin(t) + cos(t))^2]")
print("                      = e^(2ct) * [c^2*cos^2(t) - 2c*cos(t)*sin(t) + sin^2(t) + c^2*sin^2(t) + 2c*sin(t)*cos(t) + cos^2(t)]")
print("                      = e^(2ct) * [c^2*(cos^2(t) + sin^2(t)) + (sin^2(t) + cos^2(t))]")
print("                      = e^(2ct) * [c^2 + 1]")
print("\n|f'(t)| = e^(ct) * sqrt(c^2 + 1)")

# Calculate the integral
print("\nArc length = integral from -infinity to 0 of e^(ct) * sqrt(c^2 + 1) dt")
print("         = sqrt(c^2 + 1) * integral from -infinity to 0 of e^(ct) dt")
print("         = sqrt(c^2 + 1) * [e^(ct)/c] from -infinity to 0")
print("         = sqrt(c^2 + 1) * [e^0/c - lim(t->-infinity) e^(ct)/c]")
print("         = sqrt(c^2 + 1) * [1/c - 0]")
print("         = sqrt(c^2 + 1) / c")

# Verify with sympy integration
t_var = sp.Symbol('t', real=True)
integrand = sp.exp(c*t_var) * sp.sqrt(c**2 + 1)
integral_result = sp.integrate(integrand, (t_var, -sp.oo, 0))
print(f"\nSympy verification: {integral_result}")
print(f"Simplified: {sp.simplify(integral_result)}")