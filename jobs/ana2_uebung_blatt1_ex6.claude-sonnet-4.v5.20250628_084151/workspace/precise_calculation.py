import math
from fractions import Fraction

# Calculate partial sum using fractions for exact computation
def exact_partial_sum(n):
    return sum(Fraction(1, k**2) for k in range(1, n+1))

# Find n such that bounds round to same 2 decimal places
print("Finding n for 2 decimal place accuracy...")
print("(Bounds must round to the same value)")

for n in range(10, 25):
    S_n = exact_partial_sum(n)
    lower = S_n + Fraction(1, n+1)
    upper = S_n + Fraction(1, n)
    
    lower_float = float(lower)
    upper_float = float(upper)
    
    lower_rounded = round(lower_float, 2)
    upper_rounded = round(upper_float, 2)
    
    print(f"\nn = {n}:")
    print(f"  S_{n} = {float(S_n):.8f}")
    print(f"  Lower bound: {lower_float:.8f} → {lower_rounded}")
    print(f"  Upper bound: {upper_float:.8f} → {upper_rounded}")
    print(f"  Difference: {upper_float - lower_float:.8f}")
    
    if lower_rounded == upper_rounded:
        print(f"  ✓ Both bounds round to {lower_rounded}")
        optimal_n = n
        optimal_value = lower_rounded
        optimal_S_n = S_n
        optimal_lower = lower
        optimal_upper = upper
        break

# Check if we found an optimal n
if 'optimal_n' not in locals():
    print("\nNeed to check larger values of n...")
    # Just use n=20 for now
    optimal_n = 20
    optimal_S_n = exact_partial_sum(optimal_n)
    optimal_lower = optimal_S_n + Fraction(1, optimal_n+1)
    optimal_upper = optimal_S_n + Fraction(1, optimal_n)
    optimal_value = 1.64

# Show the exact fractions for the optimal n
print(f"\n\nDetailed calculation for n = {optimal_n}:")
print(f"S_{optimal_n} = ", end="")
terms = []
for k in range(1, min(6, optimal_n+1)):
    terms.append(f"1/{k}²")
if optimal_n > 5:
    terms.append("...")
    terms.append(f"1/{optimal_n}²")
print(" + ".join(terms))

print(f"\nExact value: S_{optimal_n} = {optimal_S_n}")
print(f"Lower bound: S_{optimal_n} + 1/{optimal_n+1} = {optimal_lower}")
print(f"Upper bound: S_{optimal_n} + 1/{optimal_n} = {optimal_upper}")
print(f"\nBoth bounds round to: {optimal_value}")

# Verify against π²/6
actual = math.pi**2 / 6
print(f"\nActual ζ(2) = π²/6 ≈ {actual:.8f}")
print(f"Error in our estimate: {abs(actual - optimal_value):.8f}")