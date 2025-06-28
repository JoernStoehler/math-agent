import sympy as sp
from sympy import *

# From the residue calculation, we found the residue is -√2/4
# This suggests the integral might be related to logarithms

# Let me recalculate the principal value more carefully
# The antiderivative is:
t = sp.Symbol('t', real=True)
F = -(t + 1)/(t**2 + 1) + sqrt(2)*log(t - 1 - sqrt(2))/4 - sqrt(2)*log(t - 1 + sqrt(2))/4

# Note: we need to be careful about the branch cut of the logarithm
# For t < 1 + √2, log(t - 1 - √2) involves a negative argument

# Let's compute F at key points
# F(0)
F_0 = F.subs(t, 0)
print("F(0) =", F_0)

# The log terms need careful handling:
# log(-1 - √2) = log(|-1 - √2|) + iπ = log(1 + √2) + iπ
# log(√2 - 1) = log(√2 - 1) (positive)

# So F(0) = -1 + √2/4 * [log(1 + √2) + iπ] - √2/4 * log(√2 - 1)
#         = -1 + √2/4 * log(1 + √2) + i√2π/4 - √2/4 * log(√2 - 1)

# But wait, we need the principal value, which is real
# Let's approach this differently

# The principal value can be computed as:
# P.V. = ∫₀^(1+√2-ε) + ∫_(1+√2+ε)^∞

# For the first part, near the singularity from below:
# The antiderivative has a log(t - 1 - √2) term which becomes log(negative)
# We need to use the correct branch

# Actually, let me verify the numerical result using a different method
# The value 1.6232... might have a closed form

# Let's check if it's related to the Catalan constant
G = 0.915965594177219015054603514932384110774  # Catalan's constant
print(f"\nCatalan's constant G = {G}")
print(f"Our value = 1.6232...")
print(f"π/2 = {float(pi/2)}")

# Check various combinations
val = 1.6232252401402305
print(f"\nval - π/2 = {val - float(pi/2)}")
print(f"π²/4 - π/2 = {float(pi**2/4 - pi/2)}")

# Actually, let me use the fact that the residue is -√2/4
# This suggests the principal value might be:
# Regular integral + πi * Residue (but we want real part)

# Let me try one more approach: evaluate the integral using the substitution x = 2*arctan(t)
# Then the integral from 0 to π becomes an integral from 0 to ∞

# The integrand transforms to a rational function whose antiderivative we computed
# The issue is the pole at t = 1 + √2

# Given the residue -√2/4, the principal value integral should be:
# [Antiderivative evaluated at boundaries] + [contribution from pole]

# Let's compute F(∞) - F(0) carefully
# As t → ∞: 
# -(t+1)/(t²+1) → 0
# log(t - 1 - √2) - log(t - 1 + √2) → log((t - 1 - √2)/(t - 1 + √2)) → log(1) = 0

# So F(∞) = 0

# For F(0), we need to handle the complex logarithm carefully
# When t = 0:
# log(-1 - √2) - log(√2 - 1)
# = log(1 + √2) + iπ - log(√2 - 1)
# = log((1 + √2)/(√2 - 1)) + iπ

# Simplify (1 + √2)/(√2 - 1)
frac = (1 + sqrt(2))/(sqrt(2) - 1)
frac_simplified = simplify(frac)
print(f"\n(1 + √2)/(√2 - 1) = {frac_simplified}")

# Actually, let me compute this more carefully
# (1 + √2)/(√2 - 1) = (1 + √2)(√2 + 1)/((√2 - 1)(√2 + 1))
#                   = (1 + √2)²/(2 - 1) = (1 + 2√2 + 2) = 3 + 2√2

print(f"= {float(frac_simplified)}")

# So log((1 + √2)/(√2 - 1)) = log(3 + 2√2)

# Therefore F(0) = -1 + √2/4 * [log(3 + 2√2) + iπ]

# The real part is: -1 + √2/4 * log(3 + 2√2)

F_0_real = -1 + sqrt(2)/4 * log(3 + 2*sqrt(2))
print(f"\nReal part of F(0) = {F_0_real}")
print(f"Numerical value = {float(F_0_real)}")

# So the principal value should be:
# P.V. = F(∞) - F(0) = 0 - F_0_real = -F_0_real
pv_exact = -F_0_real
print(f"\nPrincipal value = -{F_0_real} = {-F_0_real}")
print(f"Numerical = {float(pv_exact)}")

# Wait, this gives a negative value. Let me reconsider the signs...