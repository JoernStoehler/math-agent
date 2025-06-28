import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Part (b) calculation
t = sp.Symbol('t')

# Check the substitution formulas
x = sp.Symbol('x')
sin_x = 2*t/(1+t**2)
cos_x = (1-t**2)/(1+t**2)

# The integrand after substitution
numerator = sin_x**2
denominator = sin_x + cos_x
integrand_original = numerator/denominator

# Simplify
integrand_original_simplified = sp.simplify(integrand_original)
print("Original integrand in terms of t:", integrand_original_simplified)

# Including the dx = 2/(1+t^2) dt factor
integrand_full = integrand_original_simplified * 2/(1+t**2)
integrand_full_simplified = sp.simplify(integrand_full)
print("Full integrand with dx substitution:", integrand_full_simplified)

# Let's factor the denominator 1 + 2t - t^2
denominator_expr = 1 + 2*t - t**2
roots = sp.solve(denominator_expr, t)
print("Roots of 1 + 2t - t^2:", roots)

# Factor it
factored = sp.factor(denominator_expr)
print("Factored form:", factored)

# Rewrite as -(t^2 - 2t - 1) = -(t - (1 + sqrt(2)))(t - (1 - sqrt(2)))
# So the integrand is 8t^2 / ((1+t^2) * (-(t - (1 + sqrt(2)))(t - (1 - sqrt(2)))))

# Let's do partial fractions - note the integral is from 0 to infinity
# First check if there's a singularity issue
print("\nChecking denominator zeros:")
print("1 + t^2 = 0 has no real solutions")
print("1 + 2t - t^2 = 0 at t =", roots)
print("Since 1 + sqrt(2) > 0 and 1 - sqrt(2) < 0, we have a pole at t = 1 + sqrt(2) in (0, ∞)")

# The integral might not converge. Let's check the behavior near the pole
pole = 1 + sp.sqrt(2)
print(f"\nPole at t = {pole} ≈ {float(pole)}")

# Let's compute the integral more carefully
# First simplify the integrand
integrand = 8*t**2 / ((1+t**2) * (1 + 2*t - t**2))
print("\nIntegrand:", integrand)

# Try a different approach - substitute back
x_var = sp.Symbol('x', real=True)
original_integrand = sp.sin(x_var)**2 / (sp.sin(x_var) + sp.cos(x_var))
print("\nOriginal integrand:", original_integrand)

# Let's compute symbolically
integral_result = sp.integrate(original_integrand, (x_var, 0, sp.pi))
print("\nDirect integration result:", integral_result)

# Numerical check
def integrand_func(x_val):
    if x_val == np.pi:
        return 0  # Handle singularity at x = pi
    return np.sin(x_val)**2 / (np.sin(x_val) + np.cos(x_val))

# Plot the integrand
x_vals = np.linspace(0.001, np.pi - 0.001, 1000)
y_vals = [integrand_func(x) for x in x_vals]

plt.figure(figsize=(10, 6))
plt.plot(x_vals, y_vals)
plt.xlabel('x')
plt.ylabel('sin²(x)/(sin(x)+cos(x))')
plt.title('Integrand function')
plt.grid(True)
plt.savefig('integrand_plot.png')
plt.close()

# Numerical integration
from scipy import integrate
result, error = integrate.quad(integrand_func, 0, np.pi - 0.0001)
print(f"\nNumerical integration result: {result} ± {error}")
print(f"π/2 = {np.pi/2}")