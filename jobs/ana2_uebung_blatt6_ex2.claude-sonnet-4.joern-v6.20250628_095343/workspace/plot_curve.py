import numpy as np
import matplotlib.pyplot as plt

# Define the parameter range
t = np.linspace(0, 2*np.pi, 1000)

# Define the curve
x = np.sin(2*t) * np.cos(t)
y = np.sin(2*t) * np.sin(t)

# Create the plot
plt.figure(figsize=(8, 8))
plt.plot(x, y, 'b-', linewidth=2)
plt.grid(True, alpha=0.3)
plt.axis('equal')
plt.xlabel('x')
plt.ylabel('y')
plt.title(r'Kurve $f(t) = (\sin(2t)\cos t, \sin(2t)\sin t)$')

# Mark special points
# t = 0, π/2, π, 3π/2
special_t = [0, np.pi/2, np.pi, 3*np.pi/2]
for t_val in special_t:
    x_val = np.sin(2*t_val) * np.cos(t_val)
    y_val = np.sin(2*t_val) * np.sin(t_val)
    plt.plot(x_val, y_val, 'ro', markersize=8)
    plt.annotate(f't={t_val:.2f}', (x_val, y_val), xytext=(5, 5), textcoords='offset points')

plt.savefig('curve_plot.png', dpi=300, bbox_inches='tight')
plt.close()

print("Plot saved as curve_plot.png")