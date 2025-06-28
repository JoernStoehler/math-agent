import math
from fractions import Fraction

# Calculate partial sum using fractions for exact computation
def exact_partial_sum(n):
    return sum(Fraction(1, k**2) for k in range(1, n+1))

# Find n such that bounds round to same 2 decimal places
print("Finding n for 2 decimal place accuracy...")
print("(Bounds must round to the same value)")

found = False
for n in range(10, 100):
    S_n = exact_partial_sum(n)
    lower = S_n + Fraction(1, n+1)
    upper = S_n + Fraction(1, n)
    
    lower_float = float(lower)
    upper_float = float(upper)
    
    # Check if they round to same 2 decimal places
    lower_rounded = round(lower_float, 2)
    upper_rounded = round(upper_float, 2)
    
    if n <= 30 or n % 10 == 0:  # Show some intermediate values
        print(f"\nn = {n}:")
        print(f"  Lower bound: {lower_float:.8f} → {lower_rounded}")
        print(f"  Upper bound: {upper_float:.8f} → {upper_rounded}")
    
    if lower_rounded == upper_rounded and not found:
        print(f"\n✓ Found! n = {n}")
        print(f"  Both bounds round to {lower_rounded}")
        found = True
        optimal_n = n
        optimal_value = lower_rounded
        
        # Calculate the exact partial sum
        print(f"\nCalculating S_{n} = 1/1² + 1/2² + ... + 1/{n}²")
        
        # Show first few terms explicitly
        print("\nFirst few terms:")
        for k in range(1, min(11, n+1)):
            print(f"  1/{k}² = {Fraction(1, k**2)} ≈ {float(Fraction(1, k**2)):.8f}")
        
        print(f"\nS_{n} = {float(S_n):.8f}")
        print(f"Lower bound: S_{n} + 1/{n+1} = {lower_float:.8f}")
        print(f"Upper bound: S_{n} + 1/{n} = {upper_float:.8f}")
        print(f"\nζ(2) ≈ {optimal_value}")
        break

if not found:
    print("\nNeed even larger n!")