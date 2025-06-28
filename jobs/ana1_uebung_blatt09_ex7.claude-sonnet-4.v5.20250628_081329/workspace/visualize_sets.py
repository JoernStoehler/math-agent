import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure with subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Part (a): {z ∈ ℂ | -3 ≤ Im(z+5-3i) ≤ 2}
# Let z = x + iy, then z + 5 - 3i = (x+5) + i(y-3)
# So Im(z+5-3i) = y-3
# The condition becomes: -3 ≤ y-3 ≤ 2
# Which gives us: 0 ≤ y ≤ 5

ax1.axhspan(0, 5, alpha=0.3, color='blue', label='$0 \\leq y \\leq 5$')
ax1.set_xlim(-8, 8)
ax1.set_ylim(-2, 7)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.set_xlabel('Real axis')
ax1.set_ylabel('Imaginary axis')
ax1.set_title('(a) $\\{z \\in \\mathbb{C} | -3 \\leq \\mathrm{Im}(z+5-3i) \\leq 2\\}$')
ax1.legend()

# Part (b): {z ∈ ℂ | |z + 2 - i| ≥ 3}
# This is the exterior of a circle centered at -2 + i with radius 3
center = (-2, 1)
circle = plt.Circle(center, 3, fill=False, edgecolor='red', linewidth=2)
ax2.add_patch(circle)

# Fill the exterior
x = np.linspace(-8, 4, 400)
y = np.linspace(-5, 7, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j*Y
mask = np.abs(Z + 2 - 1j) >= 3
ax2.contourf(X, Y, mask, levels=[0.5, 1.5], colors=['lightblue'], alpha=0.3)

ax2.plot(center[0], center[1], 'ro', markersize=8, label='Center: $-2+i$')
ax2.set_xlim(-8, 4)
ax2.set_ylim(-5, 7)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.set_xlabel('Real axis')
ax2.set_ylabel('Imaginary axis')
ax2.set_title('(b) $\\{z \\in \\mathbb{C} | |z + 2 - i| \\geq 3\\}$')
ax2.legend()
ax2.set_aspect('equal')

# Part (c): {z ∈ ℂ | z·conj(z) - (z + conj(z))² ≤ 1}
# Let z = x + iy, then conj(z) = x - iy
# z·conj(z) = |z|² = x² + y²
# z + conj(z) = 2x
# So the condition becomes: x² + y² - 4x² ≤ 1
# Which simplifies to: y² - 3x² ≤ 1
# This is a hyperbola: y²/1 - x²/(1/3) ≤ 1

x = np.linspace(-2, 2, 400)
y = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(x, y)
condition = Y**2 - 3*X**2 <= 1
ax3.contourf(X, Y, condition, levels=[0.5, 1.5], colors=['lightgreen'], alpha=0.3)

# Draw the boundary hyperbola
x_boundary = np.linspace(-2, 2, 1000)
y_pos = np.sqrt(1 + 3*x_boundary**2)
y_neg = -np.sqrt(1 + 3*x_boundary**2)
ax3.plot(x_boundary, y_pos, 'g-', linewidth=2, label='Boundary: $y^2 - 3x^2 = 1$')
ax3.plot(x_boundary, y_neg, 'g-', linewidth=2)

ax3.set_xlim(-2, 2)
ax3.set_ylim(-3, 3)
ax3.grid(True, alpha=0.3)
ax3.axhline(y=0, color='k', linewidth=0.5)
ax3.axvline(x=0, color='k', linewidth=0.5)
ax3.set_xlabel('Real axis')
ax3.set_ylabel('Imaginary axis')
ax3.set_title('(c) $\\{z \\in \\mathbb{C} | z\\overline{z} - (z + \\overline{z})^2 \\leq 1\\}$')
ax3.legend()

plt.tight_layout()
plt.savefig('complex_sets.png', dpi=300, bbox_inches='tight')
plt.show()

# Create individual plots for better clarity
for i, (ax, title) in enumerate([(ax1, 'set_a'), (ax2, 'set_b'), (ax3, 'set_c')]):
    fig_single = plt.figure(figsize=(6, 6))
    ax_single = fig_single.add_subplot(111)
    
    if i == 0:  # Part (a)
        ax_single.axhspan(0, 5, alpha=0.3, color='blue', label='$0 \\leq y \\leq 5$')
        ax_single.set_xlim(-8, 8)
        ax_single.set_ylim(-2, 7)
    elif i == 1:  # Part (b)
        circle = plt.Circle(center, 3, fill=False, edgecolor='red', linewidth=2)
        ax_single.add_patch(circle)
        mask = np.abs(Z + 2 - 1j) >= 3
        ax_single.contourf(X, Y, mask, levels=[0.5, 1.5], colors=['lightblue'], alpha=0.3)
        ax_single.plot(center[0], center[1], 'ro', markersize=8)
        ax_single.set_xlim(-8, 4)
        ax_single.set_ylim(-5, 7)
        ax_single.set_aspect('equal')
    else:  # Part (c)
        ax_single.contourf(X, Y, condition, levels=[0.5, 1.5], colors=['lightgreen'], alpha=0.3)
        ax_single.plot(x_boundary, y_pos, 'g-', linewidth=2)
        ax_single.plot(x_boundary, y_neg, 'g-', linewidth=2)
        ax_single.set_xlim(-2, 2)
        ax_single.set_ylim(-3, 3)
    
    ax_single.grid(True, alpha=0.3)
    ax_single.axhline(y=0, color='k', linewidth=0.5)
    ax_single.axvline(x=0, color='k', linewidth=0.5)
    ax_single.set_xlabel('Real axis')
    ax_single.set_ylabel('Imaginary axis')
    
    plt.savefig(f'{title}.png', dpi=300, bbox_inches='tight')
    plt.close()