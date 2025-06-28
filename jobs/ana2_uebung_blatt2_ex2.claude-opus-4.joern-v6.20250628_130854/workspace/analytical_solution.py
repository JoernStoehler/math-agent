import sympy as sp
from sympy import *

# Let's solve this integral analytically
# I = ∫₀^π sin²(x)/(sin(x)+cos(x)) dx

# Method: Use the identity sin(x) + cos(x) = √2 sin(x + π/4)
# So: I = ∫₀^π sin²(x)/(√2 sin(x + π/4)) dx

# Let's also use: sin²(x) = (1 - cos(2x))/2
# I = (1/2√2) ∫₀^π (1 - cos(2x))/sin(x + π/4) dx

# Split into two integrals:
# I = (1/2√2) ∫₀^π 1/sin(x + π/4) dx - (1/2√2) ∫₀^π cos(2x)/sin(x + π/4) dx

# For the first integral, let u = x + π/4:
# ∫₀^π 1/sin(x + π/4) dx = ∫_{π/4}^{5π/4} 1/sin(u) du

# This integral has a singularity at u = π (i.e., x = 3π/4)

# Let's try a different approach using residues or a known result

# Actually, let me use integration by parts on the original integral
# But first, let's verify the numerical result more carefully

# Using the substitution t = tan(x/2), we get:
t = sp.Symbol('t', real=True)

# The transformed integrand is:
integrand_t = 8*t**2 / ((1 + t**2)**2 * (-t**2 + 2*t + 1))

# Partial fractions:
pf = apart(integrand_t, t)
print("Partial fraction decomposition:")
print(pf)

# Now integrate each term
# Note: the integral goes from 0 to ∞ with a pole at t = 1 + √2

# Let's compute the antiderivative
antideriv = integrate(pf, t)
print(f"\nAntiderivative: {antideriv}")

# The issue is that we need to handle the logarithmic singularity carefully

# Let me try yet another approach: use the fact that
# ∫₀^{π/2} f(x) dx + ∫_{π/2}^π f(x) dx
# and use substitution u = π - x in the second integral

print("\n\nUsing symmetry approach:")
print("Split the integral at π/2:")
print("I = ∫₀^{π/2} sin²(x)/(sin(x)+cos(x)) dx + ∫_{π/2}^π sin²(x)/(sin(x)+cos(x)) dx")

# In the second integral, substitute u = π - x:
print("\nIn the second integral, let u = π - x:")
print("∫_{π/2}^π sin²(x)/(sin(x)+cos(x)) dx = ∫_{π/2}^0 sin²(π-u)/(sin(π-u)+cos(π-u)) (-du)")
print("= ∫₀^{π/2} sin²(u)/(sin(u)-cos(u)) du")

# So:
print("\nTherefore:")
print("I = ∫₀^{π/2} sin²(x)/(sin(x)+cos(x)) dx + ∫₀^{π/2} sin²(x)/(sin(x)-cos(x)) dx")
print("I = ∫₀^{π/2} sin²(x)[1/(sin(x)+cos(x)) + 1/(sin(x)-cos(x))] dx")
print("I = ∫₀^{π/2} sin²(x)[2sin(x)/(sin²(x)-cos²(x))] dx")

# Now sin²(x) - cos²(x) = -cos(2x)
print("\nUsing sin²(x) - cos²(x) = -cos(2x):")
print("I = -2∫₀^{π/2} sin³(x)/cos(2x) dx")

# Let's compute this numerically
import numpy as np
from scipy import integrate

def integrand_final(x):
    return -2 * np.sin(x)**3 / np.cos(2*x)

# This has a singularity at x = π/4 where cos(2x) = 0
# Split the integral
result1, _ = integrate.quad(integrand_final, 0, np.pi/4 - 1e-8)
result2, _ = integrate.quad(integrand_final, np.pi/4 + 1e-8, np.pi/2)
total = result1 + result2

print(f"\nNumerical result: {total}")

# Actually, I realize the issue. Let me recalculate the principal value correctly
# by being more careful about the contributions from both sides of the singularity

def original_integrand(x):
    return np.sin(x)**2 / (np.sin(x) + np.cos(x))

# The singularity is at 3π/4
# Let's compute the Cauchy principal value properly
from scipy.integrate import quad

# Define integration with principal value
def principal_value_integral():
    x_sing = 3*np.pi/4
    
    # For a proper principal value, we need symmetric limits
    eps = 1e-10
    
    # Split into three parts: [0, 3π/4-ε], [3π/4+ε, π]
    I1, _ = quad(original_integrand, 0, x_sing - eps, limit=1000)
    I2, _ = quad(original_integrand, x_sing + eps, np.pi, limit=1000)
    
    return I1 + I2

pv = principal_value_integral()
print(f"\n\nFinal principal value: {pv}")
print(f"π/2 = {np.pi/2}")

# I think the answer is NOT π/2, but rather the value ≈ 1.623
# Let me verify this is correct by checking the calculation once more