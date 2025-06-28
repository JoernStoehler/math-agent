import sympy as sp
import numpy as np

# Define variable
x = sp.Symbol('x')

print("Part (a): x^5/(x-1)")
print("=" * 50)

# Polynomial division for x^5/(x-1)
numerator = x**5
denominator = x - 1

# Perform polynomial division
quotient, remainder = sp.div(numerator, denominator)
print(f"x^5 = ({x-1}) * ({quotient}) + {remainder}")
print(f"Therefore: x^5/(x-1) = {quotient} + {remainder}/{x-1}")

# Verify
verification = sp.expand((x-1) * quotient + remainder)
print(f"Verification: (x-1)*({quotient}) + {remainder} = {verification}")

print("\nPart (b): x/(x^3+x^2-x-1)")
print("=" * 50)

# Factor the denominator
denom_b = x**3 + x**2 - x - 1
factors_b = sp.factor(denom_b)
print(f"x^3 + x^2 - x - 1 = {factors_b}")

# Find roots
roots_b = sp.solve(denom_b, x)
print(f"Roots: {roots_b}")

# Partial fraction decomposition
pfd_b = sp.apart(x/denom_b, x)
print(f"Partial fraction decomposition: {pfd_b}")

print("\nPart (c): x/(x^3-x^2+x-1)")
print("=" * 50)

# Factor the denominator
denom_c = x**3 - x**2 + x - 1
factors_c = sp.factor(denom_c)
print(f"x^3 - x^2 + x - 1 = {factors_c}")

# Find roots
roots_c = sp.solve(denom_c, x)
print(f"Roots: {roots_c}")

# Partial fraction decomposition
pfd_c = sp.apart(x/denom_c, x)
print(f"Partial fraction decomposition: {pfd_c}")

# Integrate all parts
print("\n" + "=" * 50)
print("ANTIDERIVATIVES:")
print("=" * 50)

# Part (a)
integral_a = sp.integrate(quotient, x) + sp.integrate(remainder/(x-1), x)
print(f"(a) ∫ x^5/(x-1) dx = {integral_a} + C")

# Part (b)
integral_b = sp.integrate(pfd_b, x)
print(f"(b) ∫ x/(x^3+x^2-x-1) dx = {integral_b} + C")

# Part (c)
integral_c = sp.integrate(pfd_c, x)
print(f"(c) ∫ x/(x^3-x^2+x-1) dx = {integral_c} + C")