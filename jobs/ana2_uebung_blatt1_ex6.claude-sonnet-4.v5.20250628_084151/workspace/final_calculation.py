import math
from fractions import Fraction

# For accuracy to 2 decimal places, we need |ζ(2) - estimate| < 0.005
# This means the bounds should be within 0.01 of each other

def exact_partial_sum(n):
    return sum(Fraction(1, k**2) for k in range(1, n+1))

# Find n such that upper - lower < 0.01
print("Finding n such that upper bound - lower bound < 0.01")
print("(This ensures 2 decimal place accuracy)\n")

for n in [5, 10, 15, 20]:
    S_n = exact_partial_sum(n)
    lower = S_n + Fraction(1, n+1)
    upper = S_n + Fraction(1, n)
    
    diff = float(upper - lower)
    
    print(f"n = {n}:")
    print(f"  S_{n} = {float(S_n):.6f}")
    print(f"  Lower bound: {float(lower):.6f}")
    print(f"  Upper bound: {float(upper):.6f}")
    print(f"  Difference: {diff:.6f}")
    
    if diff < 0.01:
        print(f"  ✓ Difference < 0.01, so n = {n} is sufficient")
        optimal_n = n
        break
    else:
        print(f"  ✗ Difference > 0.01, need larger n")

# Now let's use n = 10 for our calculation
n = 10
print(f"\n\nDetailed calculation with n = {n}:")

# Calculate S_10 term by term
print("\nCalculating S_10 = Σ(k=1 to 10) 1/k²:")
S_10 = Fraction(0)
for k in range(1, 11):
    term = Fraction(1, k**2)
    S_10 += term
    print(f"  1/{k}² = {term} = {float(term):.8f}")

print(f"\nS_10 = {S_10} = {float(S_10):.8f}")

# Calculate bounds
lower = S_10 + Fraction(1, 11)
upper = S_10 + Fraction(1, 10)

print(f"\nBounds:")
print(f"  Lower: S_10 + 1/11 = {float(lower):.8f}")
print(f"  Upper: S_10 + 1/10 = {float(upper):.8f}")
print(f"  Difference: {float(upper - lower):.8f} < 0.01 ✓")

# The estimate
estimate = (float(lower) + float(upper)) / 2
print(f"\nEstimate: ζ(2) ≈ {estimate:.2f}")

# Compare with actual value
actual = math.pi**2 / 6
print(f"\nActual value: ζ(2) = π²/6 = {actual:.8f}")
print(f"Our estimate rounded to 2 decimal places: {estimate:.2f}")
print(f"Actual value rounded to 2 decimal places: {round(actual, 2)}")
print(f"Error: |{actual:.8f} - {estimate:.8f}| = {abs(actual - estimate):.8f} < 0.005 ✓")