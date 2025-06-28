import matplotlib.pyplot as plt
import numpy as np

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Define the curve for t > 0
t = np.linspace(0.001, 1, 10000)
x = t
y = t * np.cos(np.pi / t)

# Plot the full curve
ax1.plot(x, y, 'b-', linewidth=0.5)
ax1.plot(0, 0, 'ro', markersize=5)  # Mark the origin
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('Curve $f(t) = (t, t\\cos(\\pi/t))$ for $t \\in [0,1]$')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-0.1, 1.1)
ax1.set_ylim(-0.5, 0.5)

# Zoom in near t=0 to show oscillations
t_zoom = np.linspace(0.001, 0.1, 5000)
x_zoom = t_zoom
y_zoom = t_zoom * np.cos(np.pi / t_zoom)

ax2.plot(x_zoom, y_zoom, 'b-', linewidth=0.8)
ax2.plot(0, 0, 'ro', markersize=5)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('Zoomed view near $t=0$ showing infinite oscillations')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-0.01, 0.11)
ax2.set_ylim(-0.11, 0.11)

# Mark some key points where cos(π/t) = ±1
key_points_t = [1/k for k in range(1, 11)]
for k, t_val in enumerate(key_points_t, 1):
    if t_val <= 0.1:  # Only show in zoom plot
        ax2.plot(t_val, t_val * np.cos(np.pi / t_val), 'go' if k % 2 == 0 else 'mo', 
                markersize=4, alpha=0.7)

plt.tight_layout()
plt.savefig('curve_visualization.png', dpi=150, bbox_inches='tight')
plt.close()

# Create another plot showing the arc length accumulation
fig, ax = plt.subplots(figsize=(8, 6))

# Calculate distances between consecutive points t = 1/k
k_values = np.arange(2, 100)
distances = []
for k in k_values:
    t1 = 1/k
    t2 = 1/(k+1)
    # Points on the curve
    p1 = np.array([t1, t1 * np.cos(np.pi * k)])
    p2 = np.array([t2, t2 * np.cos(np.pi * (k+1))])
    dist = np.linalg.norm(p2 - p1)
    distances.append(dist)

# Plot the distances
ax.bar(k_values, distances, width=0.8, alpha=0.7, color='blue')
ax.set_xlabel('k')
ax.set_ylabel('Distance $||f(1/k) - f(1/(k+1))||$')
ax.set_title('Distances between consecutive points showing divergent sum')
ax.grid(True, alpha=0.3)

# Add cumulative sum line
cumsum = np.cumsum(distances)
ax2 = ax.twinx()
ax2.plot(k_values, cumsum, 'r-', linewidth=2, label='Cumulative sum')
ax2.set_ylabel('Cumulative sum of distances', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.tight_layout()
plt.savefig('arc_length_divergence.png', dpi=150, bbox_inches='tight')
plt.close()

print("Visualizations saved as curve_visualization.png and arc_length_divergence.png")