import numpy as np
import matplotlib.pyplot as plt

# Create a figure with subplots for different values of c
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

# Different values of c to show the effect
c_values = [0.1, 0.2, 0.5, 1.0]

for idx, c in enumerate(c_values):
    ax = axes[idx]
    
    # Parameter t from -infinity to 0, but we'll use a practical range
    t = np.linspace(-10, 0, 1000)
    
    # Calculate x and y coordinates
    x = np.exp(c * t) * np.cos(t)
    y = np.exp(c * t) * np.sin(t)
    
    # Plot the spiral
    ax.plot(x, y, 'b-', linewidth=2)
    ax.plot(x[-1], y[-1], 'ro', markersize=8)  # Mark the endpoint at t=0
    ax.plot(0, 0, 'ko', markersize=6)  # Mark the origin
    
    # Set aspect ratio to equal
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_title(f'Logarithmic Spiral with c = {c}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    # Add arrow to show direction
    if len(t) > 10:
        mid_idx = len(t) // 2
        ax.annotate('', xy=(x[mid_idx+5], y[mid_idx+5]), 
                    xytext=(x[mid_idx], y[mid_idx]),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2))

plt.tight_layout()
plt.savefig('logarithmic_spiral.png', dpi=150, bbox_inches='tight')
plt.close()

# Create a single detailed plot for c = 0.2
plt.figure(figsize=(8, 8))
c = 0.2
t = np.linspace(-15, 0, 2000)
x = np.exp(c * t) * np.cos(t)
y = np.exp(c * t) * np.sin(t)

plt.plot(x, y, 'b-', linewidth=2, label=f'$f(t) = (e^{{ct}}\\cos t, e^{{ct}}\\sin t)$, c = {c}')
plt.plot(x[-1], y[-1], 'ro', markersize=10, label='End point at t=0: (1, 0)')
plt.plot(0, 0, 'ko', markersize=8, label='Origin (0, 0)')

# Add some points along the curve
t_points = [-10, -5, -2*np.pi, -np.pi, -np.pi/2, 0]
for tp in t_points:
    if tp >= -15:
        xp = np.exp(c * tp) * np.cos(tp)
        yp = np.exp(c * tp) * np.sin(tp)
        plt.plot(xp, yp, 'go', markersize=6)
        if tp == 0:
            plt.annotate(f't = {tp}', (xp, yp), xytext=(xp+0.1, yp+0.1), fontsize=10)
        else:
            plt.annotate(f't = {tp:.2f}', (xp, yp), xytext=(xp+0.02, yp+0.02), fontsize=8)

plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.xlabel('x', fontsize=12)
plt.ylabel('y', fontsize=12)
plt.title('Logarithmic Spiral', fontsize=14)
plt.legend(fontsize=10)
plt.savefig('logarithmic_spiral_detailed.png', dpi=150, bbox_inches='tight')
plt.close()

print("Plots saved as 'logarithmic_spiral.png' and 'logarithmic_spiral_detailed.png'")