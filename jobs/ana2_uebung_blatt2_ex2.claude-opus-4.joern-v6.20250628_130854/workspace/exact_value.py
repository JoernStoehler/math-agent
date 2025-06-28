import sympy as sp
from sympy import *
import numpy as np

# Let me find the exact value of the integral
# After Weierstrass substitution, the antiderivative is:
# -8*(t + 1)/(8*t**2 + 8) + sqrt(2)*log(t - 1 + sqrt(2))/4 - sqrt(2)*log(t - sqrt(2) - 1)/4

t = sp.Symbol('t', real=True)

# The antiderivative (from partial fractions)
F = -(t + 1)/(t**2 + 1) + sqrt(2)*log(abs(t - 1 - sqrt(2)))/4 - sqrt(2)*log(abs(t + sqrt(2) - 1))/4

print("Antiderivative F(t) =", F)

# We need to compute the principal value of ∫₀^∞ with singularity at t = 1 + √2

# Let's denote t₀ = 1 + √2
t0 = 1 + sqrt(2)

# Principal value = lim[ε→0] [F(t₀-ε) - F(0) + F(∞) - F(t₀+ε)]

# First, evaluate F(0)
F_0 = F.subs(t, 0)
print("\nF(0) =", F_0)
F_0_simplified = simplify(F_0)
print("F(0) simplified =", F_0_simplified)

# For F(∞), we need the limit as t → ∞
# The log terms dominate, but they cancel out asymptotically
# -(t+1)/(t²+1) → 0 as t → ∞
# The log difference approaches 0 as well

# Let's be more careful about the singularity
# Near t = 1 + √2, the integrand behaves like 1/(t - (1 + √2))

# Actually, let me compute the residue at the pole
# The integrand after substitution is:
integrand = 8*t**2 / ((1 + t**2)**2 * (-t**2 + 2*t + 1))

# Factor the denominator
# -t² + 2t + 1 = -(t - (1+√2))(t - (1-√2))

# So near t = 1 + √2:
# Residue = lim[t→1+√2] (t - (1+√2)) * integrand

residue_expr = (t - (1 + sqrt(2))) * integrand
residue = limit(residue_expr, t, 1 + sqrt(2))
print("\nResidue at t = 1 + √2:", residue)
residue_simplified = simplify(residue)
print("Residue simplified:", residue_simplified)

# The principal value integral can be related to the residue
# For a simple pole on the real axis, P.V. ∫ f(x)dx = ∫ f(x)dx (regular part)

# Let me try a different approach: use the symmetry I found earlier
# The integral equals:
# -2∫₀^{π/2} sin³(x)/cos(2x) dx

# This can be computed using the substitution u = sin(x)
# Then sin³(x)/cos(2x) = u³/(1-2u²)

# Actually, let me just evaluate the principal value numerically with high precision
from mpmath import mp
mp.dps = 50  # 50 decimal places

def integrand_mp(x):
    return mp.sin(x)**2 / (mp.sin(x) + mp.cos(x))

# Compute with high precision
x_sing = 3*mp.pi/4
eps = mp.mpf('1e-30')

left = mp.quad(integrand_mp, [0, x_sing - eps])
right = mp.quad(integrand_mp, [x_sing + eps, mp.pi])
total = left + right

print(f"\nHigh precision principal value: {total}")
print(f"In decimal: {float(total)}")

# Let's check some special values
print(f"\nπ/2 = {float(mp.pi/2)}")
print(f"ln(2) = {float(mp.log(2))}")
print(f"√2 = {float(mp.sqrt(2))}")
print(f"π/2 + ln(2)/4 = {float(mp.pi/2 + mp.log(2)/4)}")
print(f"π/2 + ln(√2)/2 = {float(mp.pi/2 + mp.log(mp.sqrt(2))/2)}")

# Actually, the value seems to be related to elliptic integrals or other special functions
# Let's see if it matches any combination of common constants

val = float(total)
# Check if it's related to π, e, ln(2), √2, etc.

# From the numerical value ≈ 1.6232, let's see...
# This is close to π/2 + something small

diff = val - np.pi/2
print(f"\nDifference from π/2: {diff}")
print(f"Is this ln(2)/2? {np.log(2)/2} - No, doesn't match")
print(f"Is this ln(√2)? {np.log(np.sqrt(2))} - No, doesn't match")

# The exact value requires more advanced techniques