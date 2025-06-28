import numpy as np
import matplotlib.pyplot as plt

def peano_curve(n):
    """Generate n-th approximation of Peano curve"""
    if n == 0:
        # Base case: just the corners of the unit square
        return np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    
    # Get previous iteration
    prev = peano_curve(n - 1)
    points = []
    
    # Define the 9 transformations for the 3x3 grid
    # Each transformation maps [0,1]² to a subsquare
    transformations = [
        # Bottom row (left to right)
        lambda p: np.array([p[0]/3, p[1]/3]),
        lambda p: np.array([p[0]/3 + 1/3, p[1]/3]),
        lambda p: np.array([p[0]/3 + 2/3, p[1]/3]),
        # Middle row (right to left)
        lambda p: np.array([2/3 - p[0]/3 + 1/3, p[1]/3 + 1/3]),
        lambda p: np.array([1/3 - p[0]/3 + 1/3, p[1]/3 + 1/3]),
        lambda p: np.array([-p[0]/3 + 1/3, p[1]/3 + 1/3]),
        # Top row (left to right)
        lambda p: np.array([p[0]/3, p[1]/3 + 2/3]),
        lambda p: np.array([p[0]/3 + 1/3, p[1]/3 + 2/3]),
        lambda p: np.array([p[0]/3 + 2/3, p[1]/3 + 2/3])
    ]
    
    # Apply transformations
    for i, transform in enumerate(transformations):
        if i in [3, 4, 5]:  # Middle row goes right to left
            for p in reversed(prev):
                points.append(transform(p))
        else:
            for p in prev:
                points.append(transform(p))
    
    return np.array(points)

# Create visualizations for different iterations
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
axes = axes.flatten()

for i in range(4):
    curve = peano_curve(i)
    ax = axes[i]
    
    # Plot the curve
    ax.plot(curve[:, 0], curve[:, 1], 'b-', linewidth=1)
    ax.plot(curve[:, 0], curve[:, 1], 'ro', markersize=3)
    
    # Set equal aspect ratio and limits
    ax.set_aspect('equal')
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_title(f'Iteration {i}')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('peano_curve_iterations.png', dpi=150)
plt.close()

# Create a high-resolution version
fig, ax = plt.subplots(figsize=(8, 8))
curve = peano_curve(4)
ax.plot(curve[:, 0], curve[:, 1], 'b-', linewidth=0.5)
ax.set_aspect('equal')
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_title('Peano Curve (4th iteration)')
ax.grid(True, alpha=0.3)
plt.savefig('peano_curve_detailed.png', dpi=200)
plt.close()

print("Visualizations saved as peano_curve_iterations.png and peano_curve_detailed.png")