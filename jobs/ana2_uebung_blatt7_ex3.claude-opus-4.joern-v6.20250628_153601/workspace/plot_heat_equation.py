import numpy as np
import matplotlib.pyplot as plt

# Define the heat kernel function
def f(x, t, k=1):
    """Heat kernel function f(x,t) = 1/sqrt(4πkt) * exp(-x²/4kt)"""
    return (1 / np.sqrt(4 * np.pi * k * t)) * np.exp(-x**2 / (4 * k * t))

# Create x values
x = np.linspace(-10, 10, 1000)

# Create different time values
t_values = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

# Create the plot
plt.figure(figsize=(10, 6))

for t in t_values:
    y = f(x, t)
    plt.plot(x, y, label=f't = {t}')

plt.xlabel('x')
plt.ylabel('f(x,t)')
plt.title('Heat Kernel f(x,t) for k=1 and various values of t')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.5)
plt.xlim(-10, 10)

# Save the plot
plt.savefig('heat_kernel_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Create a second plot showing the limiting behaviors
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot for t → 0 (showing increasingly peaked distributions)
t_small_values = [0.01, 0.05, 0.1, 0.2]
for t in t_small_values:
    x_small = np.linspace(-2, 2, 1000)
    y_small = f(x_small, t)
    ax1.plot(x_small, y_small, label=f't = {t}')

ax1.set_xlabel('x')
ax1.set_ylabel('f(x,t)')
ax1.set_title('Behavior as t → 0')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-2, 2)

# Plot for t → ∞ (showing flattening distributions)
t_large_values = [1, 5, 10, 20, 50]
for t in t_large_values:
    y_large = f(x, t)
    ax2.plot(x, y_large, label=f't = {t}')

ax2.set_xlabel('x')
ax2.set_ylabel('f(x,t)')
ax2.set_title('Behavior as t → ∞')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-10, 10)

plt.savefig('heat_kernel_limits.png', dpi=300, bbox_inches='tight')
plt.close()

print("Plots saved as 'heat_kernel_plot.png' and 'heat_kernel_limits.png'")

# Analyze the integral of f over all x for any t > 0
# This should equal 1 (it's a probability distribution)
t_test = 1.0
x_test = np.linspace(-50, 50, 10000)
y_test = f(x_test, t_test)
integral = np.trapz(y_test, x_test)
print(f"\nIntegral of f(x,{t_test}) over x from -50 to 50: {integral:.6f}")
print("(This should be approximately 1.0)")