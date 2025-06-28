import sympy as sp
from sympy import *
import numpy as np

# Let me carefully trace through the calculation
# The integral is ∫₀^π sin²(x)/(sin(x)+cos(x)) dx

# After substitution t = tan(x/2), we get:
# ∫₀^∞ 8t²/[(1+t²)²(-t²+2t+1)] dt

# The partial fraction decomposition gave us:
# 2*(t - 1)/(t**2 + 1)**2 - 1/(t**2 - 2*t - 1) + 1/(t**2 + 1)

t = sp.Symbol('t', real=True)

# Let's integrate each term separately
# Term 1: 2*(t - 1)/(t**2 + 1)**2
# This integrates to: -(t + 1)/(t**2 + 1)

# Term 2: -1/(t**2 - 2*t - 1)
# Factor: t² - 2t - 1 = (t - (1+√2))(t - (1-√2))
# Partial fractions: -1/[(t - (1+√2))(t - (1-√2))]
# = A/(t - (1+√2)) + B/(t - (1-√2))
# -1 = A(t - (1-√2)) + B(t - (1+√2))

# Setting t = 1+√2: -1 = A(2√2), so A = -1/(2√2) = -√2/4
# Setting t = 1-√2: -1 = B(-2√2), so B = 1/(2√2) = √2/4

# So: -1/(t² - 2t - 1) = -√2/4 * 1/(t-(1+√2)) + √2/4 * 1/(t-(1-√2))
# This integrates to: -√2/4 * ln|t-(1+√2)| + √2/4 * ln|t-(1-√2)|

# Term 3: 1/(t**2 + 1)
# This integrates to: arctan(t)

# Full antiderivative:
F = -(t + 1)/(t**2 + 1) - sqrt(2)/4 * log(Abs(t - 1 - sqrt(2))) + sqrt(2)/4 * log(Abs(t - 1 + sqrt(2))) + atan(t)

print("Antiderivative F(t) =")
print(F)

# Now we need the principal value of ∫₀^∞ with pole at t = 1+√2

# Split as: ∫₀^(1+√2-ε) + ∫_(1+√2+ε)^∞

# For 0 ≤ t < 1+√2:
# t - (1+√2) < 0, so |t - (1+√2)| = -(t - (1+√2)) = (1+√2) - t
# t - (1-√2) > 0 (since 1-√2 < 0), so |t - (1-√2)| = t - (1-√2)

# For t > 1+√2:
# Both arguments are positive

# Let's evaluate at the boundaries:
# F(0):
F_0 = F.subs(t, 0)
print("\nF(0) =", F_0)

# Substitute specific values:
# arctan(0) = 0
# |0 - (1+√2)| = 1+√2
# |0 - (1-√2)| = |-(1-√2)| = 1-√2 (but 1-√2 < 0, so = √2-1)

F_0_value = -1 - sqrt(2)/4 * log(1 + sqrt(2)) + sqrt(2)/4 * log(sqrt(2) - 1) + 0
print("F(0) exact =", F_0_value)
print("F(0) numerical =", float(F_0_value))

# F(∞):
# As t → ∞:
# -(t+1)/(t²+1) → 0
# arctan(t) → π/2
# log|t-(1+√2)| - log|t-(1-√2)| → log[(t-(1+√2))/(t-(1-√2))] → log(1) = 0

F_inf = pi/2
print("\nF(∞) =", F_inf)

# The principal value integral excluding a symmetric interval around the pole is:
# lim[ε→0] [F(1+√2-ε) - F(0) + F(∞) - F(1+√2+ε)]

# Due to the logarithmic singularity, the contributions from both sides cancel
# So the principal value is simply:
PV = F_inf - F_0_value
print("\nPrincipal value = F(∞) - F(0) =", PV)
print("Simplified =", simplify(PV))
print("Numerical =", float(PV))

# Let's simplify the log term
# log(1+√2) - log(√2-1) = log[(1+√2)/(√2-1)]
# (1+√2)/(√2-1) = (1+√2)(√2+1)/[(√2-1)(√2+1)] = (1+√2)²/(2-1) = (1+√2)² = 3+2√2

log_term = log((1 + sqrt(2))/(sqrt(2) - 1))
print("\nlog[(1+√2)/(√2-1)] =", simplify(log_term))
print("= log(3+2√2)")

# So the exact answer is:
answer = 1 + sqrt(2)/4 * log(3 + 2*sqrt(2)) + pi/2
print("\nFinal answer:")
print("P.V. ∫₀^π sin²(x)/(sin(x)+cos(x)) dx =", answer)
print("= 1 + √2/4 * log(3+2√2) + π/2")
print("Numerical value =", float(answer))

# Verify this matches our numerical calculation
print("\nNumerical principal value from before: 1.6232252401402305")
print("Difference:", abs(float(answer) - 1.6232252401402305))