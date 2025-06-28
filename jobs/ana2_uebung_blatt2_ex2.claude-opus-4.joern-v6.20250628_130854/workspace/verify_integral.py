import sympy as sp
import numpy as np
from sympy import integrate, sin, cos, tan, atan, pi, oo, simplify, apart

# Define symbols
x = sp.Symbol('x')
t = sp.Symbol('t', real=True)

# Part a) verification
# Check the substitution formulas
print("Part a) Verification:")
print("sin(x) in terms of t:")
sin_x_formula = 2*t/(1 + t**2)
print(f"sin(x) = {sin_x_formula}")

print("\ncos(x) in terms of t:")
cos_x_formula = (1 - t**2)/(1 + t**2)
print(f"cos(x) = {cos_x_formula}")

print("\ndx in terms of dt:")
dx_formula = 2/(1 + t**2)
print(f"dx = {dx_formula} dt")

# Part b) solution
print("\n\nPart b) Solution:")
print("Original integral: ∫₀^π sin²(x)/(sin(x)+cos(x)) dx")

# After substitution t = tan(x/2)
sin_t = 2*t/(1 + t**2)
cos_t = (1 - t**2)/(1 + t**2)
dx_t = 2/(1 + t**2)

# The integrand becomes
integrand_original = sin_t**2 / (sin_t + cos_t) * dx_t
print(f"\nIntegrand after substitution: {integrand_original}")

# Simplify
integrand_simplified = simplify(integrand_original)
print(f"\nSimplified integrand: {integrand_simplified}")

# Let's simplify step by step
numerator = sin_t**2 * dx_t
denominator = sin_t + cos_t

print(f"\nNumerator: {simplify(numerator)}")
print(f"Denominator: {simplify(denominator)}")

# Final integrand
final_integrand = simplify(numerator/denominator)
print(f"\nFinal integrand: {final_integrand}")

# Try partial fractions
print("\nAttempting partial fraction decomposition...")
pf = apart(final_integrand, t)
print(f"Partial fractions: {pf}")

# Try to integrate
print("\nIntegrating from 0 to ∞...")
try:
    result = integrate(final_integrand, (t, 0, oo))
    print(f"Result: {result}")
except:
    print("Direct integration failed, trying alternative approach...")
    
# Let's also verify with numerical integration
import scipy.integrate as integrate_num

def integrand_numeric(x):
    if x == 0 or x == np.pi:
        return 0  # Handle endpoints
    return np.sin(x)**2 / (np.sin(x) + np.cos(x))

result_numeric, error = integrate_num.quad(integrand_numeric, 0, np.pi)
print(f"\nNumerical result: {result_numeric:.6f} ± {error:.2e}")