import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot the domain U = B1 ∪ B2
for ax in [ax1, ax2]:
    # Draw the two balls
    circle1 = Circle((-2, 0), 1, fill=False, edgecolor='blue', linewidth=2)
    circle2 = Circle((2, 0), 1, fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    # Label the balls
    ax.text(-2, 0, 'B₁', fontsize=12, ha='center', va='center')
    ax.text(2, 0, 'B₂', fontsize=12, ha='center', va='center')
    
    # Set axis properties
    ax.set_xlim(-4, 4)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

# Left plot: Show orientation
ax1.set_title('Diffeomorphism Φ: U → U')
ax1.arrow(-2, 0.5, 0.5, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue', alpha=0.7)
ax1.text(-1.8, 0.7, 'det(DΦ) = 1', fontsize=10, color='blue')

ax1.arrow(2, 0.5, -0.5, 0, head_width=0.1, head_length=0.1, fc='red', ec='red', alpha=0.7)
ax1.text(1.5, 0.7, 'det(DΦ) = -1', fontsize=10, color='red')

# Right plot: Show the mapping
ax2.set_title('Action of Φ')
# Show identity on B1
ax2.arrow(-2.5, 0, 0.3, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
ax2.text(-2.7, -0.3, 'Φ(x) = x', fontsize=9, color='blue')

# Show reflection on B2
ax2.arrow(1.5, 0, 1, 0, head_width=0.1, head_length=0.1, fc='red', ec='red')
ax2.arrow(2.5, 0, -1, 0, head_width=0.1, head_length=0.1, fc='red', ec='red')
ax2.text(2, -0.3, 'Φ reflects', fontsize=9, color='red', ha='center')
ax2.axvline(x=2, color='red', linestyle='--', alpha=0.5)
ax2.text(2.1, 1.5, 'x₁ = 2', fontsize=9, color='red')

plt.tight_layout()
plt.savefig('diffeomorphism_visualization.png', dpi=150, bbox_inches='tight')
plt.close()

print("Visualization saved as diffeomorphism_visualization.png")