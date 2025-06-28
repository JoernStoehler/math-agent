import numpy as np
import matplotlib.pyplot as plt

# Let's compute the integral for part (b)
# The curves are f_k(t) = (cos(kt), sin(kt)) for t in [0, 2π]

# We have α = (x dy - y dx)/(x^2 + y^2)
# For the curve f_k(t), we have:
# x = cos(kt), y = sin(kt)
# dx = -k sin(kt) dt, dy = k cos(kt) dt
# x^2 + y^2 = 1

# So f_k^*α = (cos(kt) * k cos(kt) dt - sin(kt) * (-k sin(kt) dt))/1
#           = k cos^2(kt) dt + k sin^2(kt) dt
#           = k dt

# Therefore: ∫_{[0,2π]} f_k^*α = ∫_0^{2π} k dt = 2πk

print("Integral calculation for part (b):")
print("For the curve f_k(t) = (cos(kt), sin(kt)), t ∈ [0, 2π]:")
print("f_k^*α = k dt")
print("∫_{[0,2π]} f_k^*α = 2πk")

# Let's verify this with the pullback from part (a)
# We found Φ^*α = dφ in polar coordinates
# The curve f_k can be written in polar as (r=1, φ=kt)
# So the integral becomes ∫_0^{2π} d(kt) = k∫_0^{2π} dt = 2πk

print("\nVerification using pullback:")
print("In polar coordinates: f_k corresponds to r=1, φ=kt")
print("Using Φ^*α = dφ, we get ∫ dφ = ∫ d(kt) = k∫dt = 2πk")

# Plot some of these curves
fig, ax = plt.subplots(1, 1, figsize=(8, 8))

t = np.linspace(0, 2*np.pi, 1000)
for k in [-2, -1, 1, 2, 3]:
    x = np.cos(k*t)
    y = np.sin(k*t)
    ax.plot(x, y, label=f'k={k}')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Curves $f_k(t) = (\\cos(kt), \\sin(kt))$')
ax.legend()
ax.grid(True)
ax.axis('equal')
plt.savefig('curves_fk.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nPlot saved as curves_fk.png")
print("\nInterpretation:")
print("- k > 0: curve winds k times counterclockwise")
print("- k < 0: curve winds |k| times clockwise")
print("- k = 0: constant point (1,0)")
print("- The integral counts the winding number around the origin")