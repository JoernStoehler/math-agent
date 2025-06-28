import numpy as np
import matplotlib.pyplot as plt

# Check where sin(x) + cos(x) = 0 in [0, π]
x = np.linspace(0, np.pi, 1000)
y = np.sin(x) + np.cos(x)

# Plot
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(x, y)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('x')
plt.ylabel('sin(x) + cos(x)')
plt.title('sin(x) + cos(x) on [0, π]')
plt.grid(True)

# Find zeros
zeros_idx = np.where(np.diff(np.sign(y)))[0]
zeros = x[zeros_idx]
print(f"Zeros of sin(x) + cos(x) in [0, π]: {zeros}")

# sin(x) + cos(x) = 0 when tan(x) = -1, i.e., x = 3π/4
exact_zero = 3*np.pi/4
print(f"Exact zero: x = 3π/4 = {exact_zero:.6f}")

# Plot the integrand
plt.subplot(2, 1, 2)
# Avoid division by zero
mask = np.abs(y) > 1e-10
x_safe = x[mask]
integrand = np.sin(x_safe)**2 / (np.sin(x_safe) + np.cos(x_safe))
plt.plot(x_safe, integrand)
plt.xlabel('x')
plt.ylabel('sin²(x)/(sin(x)+cos(x))')
plt.title('Integrand (with singularity at x = 3π/4)')
plt.grid(True)
plt.tight_layout()
plt.savefig('singularity_check.png')
plt.close()

print("\nThe integral has a singularity at x = 3π/4, so it's an improper integral!")
print("We need to split the integral at this point.")

# Let's also check what happens with the t substitution
t_values = np.linspace(0, 10, 1000)
denominator = -t_values**2 + 2*t_values + 1
plt.figure(figsize=(8, 6))
plt.plot(t_values, denominator)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('t')
plt.ylabel('-t² + 2t + 1')
plt.title('Denominator after substitution')
plt.grid(True)
plt.savefig('denominator_t.png')
plt.close()

# Find zeros of -t² + 2t + 1
# -t² + 2t + 1 = 0
# t² - 2t - 1 = 0
# t = (2 ± √(4 + 4))/2 = (2 ± 2√2)/2 = 1 ± √2
t_zero1 = 1 - np.sqrt(2)
t_zero2 = 1 + np.sqrt(2)
print(f"\nZeros of denominator in t: t = {t_zero1:.6f} and t = {t_zero2:.6f}")
print(f"Since t = tan(x/2) and x ∈ [0,π], t ∈ [0,∞)")
print(f"The relevant zero is t = 1 + √2 = {t_zero2:.6f}")

# What x corresponds to t = 1 + √2?
x_critical = 2 * np.arctan(1 + np.sqrt(2))
print(f"\nCritical x value: x = 2*arctan(1 + √2) = {x_critical:.6f}")
print(f"Compare with 3π/4 = {3*np.pi/4:.6f}")

# These should be equal!
print(f"\nVerification: tan(3π/8) = {np.tan(3*np.pi/8):.6f}")
print(f"1 + √2 = {1 + np.sqrt(2):.6f}")