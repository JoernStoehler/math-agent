import numpy as np
import sympy as sp
from sympy import sin, cos, pi, solve, diff, simplify, sqrt

# Define the parameter t symbolically
t = sp.Symbol('t', real=True)

# Use a polar-like representation
# Note that sin(2t)cos(t) = sin(2t)cos(t) and sin(2t)sin(t) = sin(2t)sin(t)
# We can write f(t) = sin(2t) * (cos(t), sin(t)) = sin(2t) * e^(it) in complex notation
# Or f(t) = r(t) * (cos(t), sin(t)) where r(t) = sin(2t)

print("Analysis of the curve f(t) = (sin(2t)cos(t), sin(2t)sin(t))")
print("This can be written as f(t) = sin(2t) * (cos(t), sin(t))")
print()

# The curve passes through origin when sin(2t) = 0
print("The curve passes through origin when sin(2t) = 0")
print("This happens when 2t = kπ, i.e., t = kπ/2 for k = 0, 1, 2, 3")
print("In [0, 2π): t = 0, π/2, π, 3π/2")
print()

# Calculate derivatives more carefully
x = sin(2*t) * cos(t)
y = sin(2*t) * sin(t)

# Using product rule
dx_dt = diff(sin(2*t), t) * cos(t) + sin(2*t) * diff(cos(t), t)
dy_dt = diff(sin(2*t), t) * sin(t) + sin(2*t) * diff(sin(t), t)

dx_dt = 2*cos(2*t)*cos(t) - sin(2*t)*sin(t)
dy_dt = 2*cos(2*t)*sin(t) + sin(2*t)*cos(t)

print("Derivatives:")
print(f"x'(t) = 2cos(2t)cos(t) - sin(2t)sin(t)")
print(f"y'(t) = 2cos(2t)sin(t) + sin(2t)cos(t)")
print()

# At the origin points
print("At the origin points:")
for t_val in [0, pi/2, pi, 3*pi/2]:
    dx_val = float(dx_dt.subs(t, t_val))
    dy_val = float(dy_dt.subs(t, t_val))
    print(f"t = {t_val}: f'({t_val}) = ({dx_val:.4f}, {dy_val:.4f})")
    
# Find where derivative is zero
print("\nLooking for singular points where f'(t) = 0:")
# Both dx/dt = 0 and dy/dt = 0
# Using trigonometric identities
# dx/dt = 2cos(2t)cos(t) - sin(2t)sin(t) = cos(t) + cos(3t)
# dy/dt = 2cos(2t)sin(t) + sin(2t)cos(t) = sin(t) + sin(3t)

dx_dt_simplified = cos(t) + cos(3*t)
dy_dt_simplified = sin(t) + sin(3*t)

print(f"x'(t) = cos(t) + cos(3t)")
print(f"y'(t) = sin(t) + sin(3t)")

# For both to be zero:
# cos(t) + cos(3t) = 0 and sin(t) + sin(3t) = 0
# This means cos(t) = -cos(3t) and sin(t) = -sin(3t)
# So (cos(t), sin(t)) = -(cos(3t), sin(3t))
# This means e^(it) = -e^(i3t), so e^(it) = e^(i(3t + π))
# Therefore t = 3t + π (mod 2π)
# So -2t = π (mod 2π)
# t = -π/2 (mod π) = π/2 or 3π/2

print("\nChecking potential singular points:")
for t_val in [pi/2, 3*pi/2]:
    dx_val = float((cos(t_val) + cos(3*t_val)))
    dy_val = float((sin(t_val) + sin(3*t_val)))
    print(f"t = {t_val}: x'({t_val}) = {dx_val:.6f}, y'({t_val}) = {dy_val:.6f}")
    
# Length calculation setup
print("\nFor length calculation:")
print("L = ∫₀^{2π} |f'(t)| dt")
print("where |f'(t)|² = (x'(t))² + (y'(t))²")

# Calculate |f'(t)|²
dx_squared = (cos(t) + cos(3*t))**2
dy_squared = (sin(t) + sin(3*t))**2
speed_squared = simplify(dx_squared + dy_squared)

print(f"\n|f'(t)|² = {speed_squared}")

# Using trig identity: cos²(a) + sin²(a) = 1
# |f'(t)|² = (cos(t) + cos(3t))² + (sin(t) + sin(3t))²
#         = cos²(t) + 2cos(t)cos(3t) + cos²(3t) + sin²(t) + 2sin(t)sin(3t) + sin²(3t)
#         = 1 + 1 + 2(cos(t)cos(3t) + sin(t)sin(3t))
#         = 2 + 2cos(2t)  (using cos(a-b) = cos(a)cos(b) + sin(a)sin(b))

print("\nUsing trigonometric identities:")
print("|f'(t)|² = 2 + 2cos(2t) = 4cos²(t)")
print("|f'(t)| = 2|cos(t)|")