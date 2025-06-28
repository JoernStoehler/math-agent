import numpy as np
import matplotlib.pyplot as plt

# Set up the figure with subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('Trigonometrische und Hyperbolische Funktionen', fontsize=16)

# Define x-axis ranges for different functions
x_trig = np.linspace(-2*np.pi, 2*np.pi, 1000)
x_tan = np.linspace(-2*np.pi, 2*np.pi, 1000)
x_hyp = np.linspace(-3, 3, 1000)

# Plot trigonometric functions
# sin(x)
ax1 = axes[0, 0]
ax1.plot(x_trig, np.sin(x_trig), 'b-', linewidth=2)
ax1.grid(True, alpha=0.3)
ax1.set_title('$\\sin(x)$', fontsize=14)
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
ax1.set_ylim(-1.5, 1.5)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
# Add pi markers
pi_ticks = [-2*np.pi, -np.pi, 0, np.pi, 2*np.pi]
pi_labels = ['$-2\\pi$', '$-\\pi$', '0', '$\\pi$', '$2\\pi$']
ax1.set_xticks(pi_ticks)
ax1.set_xticklabels(pi_labels)

# cos(x)
ax2 = axes[0, 1]
ax2.plot(x_trig, np.cos(x_trig), 'r-', linewidth=2)
ax2.grid(True, alpha=0.3)
ax2.set_title('$\\cos(x)$', fontsize=14)
ax2.set_xlabel('$x$')
ax2.set_ylabel('$y$')
ax2.set_ylim(-1.5, 1.5)
ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.set_xticks(pi_ticks)
ax2.set_xticklabels(pi_labels)

# tan(x)
ax3 = axes[0, 2]
# Remove points near asymptotes
tan_vals = np.tan(x_tan)
tan_vals[np.abs(tan_vals) > 10] = np.nan
ax3.plot(x_tan, tan_vals, 'g-', linewidth=2)
ax3.grid(True, alpha=0.3)
ax3.set_title('$\\tan(x)$', fontsize=14)
ax3.set_xlabel('$x$')
ax3.set_ylabel('$y$')
ax3.set_ylim(-5, 5)
ax3.axhline(y=0, color='k', linewidth=0.5)
ax3.axvline(x=0, color='k', linewidth=0.5)
# Add vertical asymptotes
for k in range(-2, 3):
    ax3.axvline(x=np.pi/2 + k*np.pi, color='gray', linestyle='--', alpha=0.5)
ax3.set_xticks(pi_ticks)
ax3.set_xticklabels(pi_labels)

# Plot hyperbolic functions
# sinh(x)
ax4 = axes[1, 0]
ax4.plot(x_hyp, np.sinh(x_hyp), 'b-', linewidth=2)
ax4.grid(True, alpha=0.3)
ax4.set_title('$\\sinh(x)$', fontsize=14)
ax4.set_xlabel('$x$')
ax4.set_ylabel('$y$')
ax4.set_ylim(-10, 10)
ax4.axhline(y=0, color='k', linewidth=0.5)
ax4.axvline(x=0, color='k', linewidth=0.5)

# cosh(x)
ax5 = axes[1, 1]
ax5.plot(x_hyp, np.cosh(x_hyp), 'r-', linewidth=2)
ax5.grid(True, alpha=0.3)
ax5.set_title('$\\cosh(x)$', fontsize=14)
ax5.set_xlabel('$x$')
ax5.set_ylabel('$y$')
ax5.set_ylim(0, 10)
ax5.axhline(y=0, color='k', linewidth=0.5)
ax5.axvline(x=0, color='k', linewidth=0.5)

# tanh(x)
ax6 = axes[1, 2]
ax6.plot(x_hyp, np.tanh(x_hyp), 'g-', linewidth=2)
ax6.grid(True, alpha=0.3)
ax6.set_title('$\\tanh(x)$', fontsize=14)
ax6.set_xlabel('$x$')
ax6.set_ylabel('$y$')
ax6.set_ylim(-1.5, 1.5)
ax6.axhline(y=0, color='k', linewidth=0.5)
ax6.axvline(x=0, color='k', linewidth=0.5)
# Add horizontal asymptotes
ax6.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
ax6.axhline(y=-1, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('function_graphs.pdf', dpi=150, bbox_inches='tight')
plt.savefig('function_graphs.png', dpi=150, bbox_inches='tight')
plt.close()

# Create individual plots for better detail
functions = [
    (np.sin, '$\\sin(x)$', x_trig, (-1.5, 1.5), 'sin'),
    (np.cos, '$\\cos(x)$', x_trig, (-1.5, 1.5), 'cos'),
    (lambda x: np.where(np.abs(np.tan(x)) > 10, np.nan, np.tan(x)), '$\\tan(x)$', x_tan, (-5, 5), 'tan'),
    (np.sinh, '$\\sinh(x)$', x_hyp, (-10, 10), 'sinh'),
    (np.cosh, '$\\cosh(x)$', x_hyp, (0, 10), 'cosh'),
    (np.tanh, '$\\tanh(x)$', x_hyp, (-1.5, 1.5), 'tanh')
]

for func, title, x_range, y_range, filename in functions:
    plt.figure(figsize=(8, 6))
    plt.plot(x_range, func(x_range), linewidth=2)
    plt.grid(True, alpha=0.3)
    plt.title(title, fontsize=16)
    plt.xlabel('$x$', fontsize=14)
    plt.ylabel('$y$', fontsize=14)
    plt.ylim(y_range)
    plt.axhline(y=0, color='k', linewidth=0.5)
    plt.axvline(x=0, color='k', linewidth=0.5)
    
    if filename in ['sin', 'cos', 'tan']:
        plt.xticks(pi_ticks, pi_labels)
    
    if filename == 'tan':
        for k in range(-2, 3):
            plt.axvline(x=np.pi/2 + k*np.pi, color='gray', linestyle='--', alpha=0.5)
    
    if filename == 'tanh':
        plt.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
        plt.axhline(y=-1, color='gray', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(f'{filename}.pdf', dpi=150, bbox_inches='tight')
    plt.savefig(f'{filename}.png', dpi=150, bbox_inches='tight')
    plt.close()

print("Graphs generated successfully!")