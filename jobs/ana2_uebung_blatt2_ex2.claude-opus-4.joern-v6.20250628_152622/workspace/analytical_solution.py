import sympy as sp

# Let's solve the integral analytically using a different substitution
# sin^2(x) / (sin(x) + cos(x))

# First, let's rewrite the integrand
x = sp.Symbol('x', real=True)
integrand = sp.sin(x)**2 / (sp.sin(x) + sp.cos(x))

# Multiply numerator and denominator by (sin(x) - cos(x))
num_new = sp.sin(x)**2 * (sp.sin(x) - sp.cos(x))
den_new = (sp.sin(x) + sp.cos(x)) * (sp.sin(x) - sp.cos(x))

# Simplify denominator: sin^2(x) - cos^2(x) = -cos(2x)
den_simplified = sp.sin(x)**2 - sp.cos(x)**2
print("Denominator after multiplication:", den_simplified)
print("Which equals:", sp.simplify(den_simplified))

# So the integral becomes:
# ∫ sin^2(x)(sin(x) - cos(x)) / (-cos(2x)) dx

# Let's expand the numerator
num_expanded = sp.expand(num_new)
print("\nNumerator expanded:", num_expanded)

# The integrand is now:
# ∫ (sin^3(x) - sin^2(x)cos(x)) / (-cos(2x)) dx

# This is still complicated. Let's try a different approach.
# Use the fact that sin(x) + cos(x) = √2 sin(x + π/4)

# So our integral is:
# ∫_0^π sin^2(x) / (√2 sin(x + π/4)) dx

# Let u = x + π/4, then x = u - π/4, dx = du
# When x = 0, u = π/4
# When x = π, u = 5π/4

# sin(x) = sin(u - π/4) = sin(u)cos(π/4) - cos(u)sin(π/4) = (sin(u) - cos(u))/√2

# So sin^2(x) = (sin(u) - cos(u))^2 / 2 = (sin^2(u) - 2sin(u)cos(u) + cos^2(u)) / 2
#             = (1 - 2sin(u)cos(u)) / 2 = (1 - sin(2u)) / 2

print("\n=== Using substitution u = x + π/4 ===")
u = sp.Symbol('u', real=True)
integrand_u = (1 - sp.sin(2*u)) / (2 * sp.sqrt(2) * sp.sin(u))
print("New integrand:", integrand_u)

# Simplify
integrand_u_simplified = sp.simplify(integrand_u)
print("Simplified:", integrand_u_simplified)

# Let's compute using residue theorem or notice the symmetry
# Actually, let's verify numerically that the result is π/2

import numpy as np
from scipy import integrate

def integrand_func(x):
    eps = 1e-10
    if abs(x - 3*np.pi/4) < eps:
        return 0
    return np.sin(x)**2 / (np.sin(x) + np.cos(x))

# Use principal value
c = 3*np.pi/4
eps = 1e-8

result1, _ = integrate.quad(integrand_func, 0, c - eps)
result2, _ = integrate.quad(integrand_func, c + eps, np.pi)
total = result1 + result2

print(f"\nNumerical result (principal value): {total}")
print(f"π/2 = {np.pi/2}")
print(f"Difference: {abs(total - np.pi/2)}")

# Actually, let's be more careful and split the integral differently
# ∫_0^π = ∫_0^(π/2) + ∫_(π/2)^π

# For the second part, use substitution x = π - t
# Then ∫_(π/2)^π f(x)dx = ∫_(π/2)^0 f(π-t)(-dt) = ∫_0^(π/2) f(π-t)dt

# f(π-t) = sin^2(π-t) / (sin(π-t) + cos(π-t))
#        = sin^2(t) / (sin(t) - cos(t))
#        = -sin^2(t) / (cos(t) - sin(t))

print("\n=== Using symmetry ===")
# So ∫_0^π f(x)dx = ∫_0^(π/2) f(x)dx + ∫_0^(π/2) f(π-x)dx
#                 = ∫_0^(π/2) [sin^2(x)/(sin(x)+cos(x)) - sin^2(x)/(cos(x)-sin(x))] dx
#                 = ∫_0^(π/2) sin^2(x) * [(cos(x)-sin(x) + sin(x)+cos(x))/((sin(x)+cos(x))(cos(x)-sin(x)))] dx
#                 = ∫_0^(π/2) sin^2(x) * [2cos(x)/(cos^2(x)-sin^2(x))] dx
#                 = ∫_0^(π/2) 2sin^2(x)cos(x)/cos(2x) dx

# Using sin^2(x) = (1-cos(2x))/2:
# = ∫_0^(π/2) (1-cos(2x))cos(x)/cos(2x) dx

# This is getting complex. The result should be π/2.