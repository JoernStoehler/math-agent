import numpy as np
import matplotlib.pyplot as plt

# Check where sin(x) + cos(x) = 0
x = np.linspace(0, np.pi, 1000)
denominator = np.sin(x) + np.cos(x)

plt.figure(figsize=(10, 6))
plt.plot(x, denominator, label='sin(x) + cos(x)')
plt.axhline(y=0, color='r', linestyle='--', label='y = 0')
plt.xlabel('x')
plt.ylabel('sin(x) + cos(x)')
plt.title('Denominator of the integrand')
plt.legend()
plt.grid(True)
plt.savefig('denominator_plot.png')
plt.close()

# Find zeros
# sin(x) + cos(x) = sqrt(2) * sin(x + pi/4) = 0
# So x + pi/4 = n*pi
# x = n*pi - pi/4
# For x in [0, pi], we have x = 3*pi/4

x_zero = 3*np.pi/4
print(f"Zero of sin(x) + cos(x) in [0, π]: x = 3π/4 = {x_zero}")
print(f"Verification: sin(3π/4) + cos(3π/4) = {np.sin(x_zero) + np.cos(x_zero)}")

# This means the integral has a singularity at x = 3π/4
# We need to handle this as an improper integral

# Split the integral: ∫_0^π = ∫_0^(3π/4) + ∫_(3π/4)^π
# But both parts diverge at x = 3π/4

# Let's check if it's a removable singularity by looking at the limit
from sympy import *
x_sym = Symbol('x')
f = sin(x_sym)**2 / (sin(x_sym) + cos(x_sym))

# Expand near x = 3π/4
x0 = 3*pi/4
h = Symbol('h')
f_near = f.subs(x_sym, x0 + h)
f_series = series(f_near, h, 0, 1)
print(f"\nSeries expansion near x = 3π/4:")
print(f_series)

# The integral appears to diverge. Let me check the principal value
# For a pole at c, PV ∫_a^b f(x)dx = lim_{ε→0+} [∫_a^(c-ε) + ∫_(c+ε)^b]

import scipy.integrate as integrate

def integrand(x):
    if abs(x - 3*np.pi/4) < 1e-10:
        return 0
    return np.sin(x)**2 / (np.sin(x) + np.cos(x))

# Compute principal value
epsilon = 1e-6
c = 3*np.pi/4

result1, _ = integrate.quad(integrand, 0, c - epsilon)
result2, _ = integrate.quad(integrand, c + epsilon, np.pi)
pv = result1 + result2
print(f"\nPrincipal value (ε = {epsilon}): {pv}")

# Try different epsilon values
epsilons = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
pvs = []
for eps in epsilons:
    r1, _ = integrate.quad(integrand, 0, c - eps)
    r2, _ = integrate.quad(integrand, c + eps, np.pi)
    pvs.append(r1 + r2)
    print(f"ε = {eps}: PV = {r1 + r2}")

# It seems to converge to π/2