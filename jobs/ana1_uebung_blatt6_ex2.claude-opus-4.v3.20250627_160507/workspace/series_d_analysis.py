import numpy as np
import matplotlib.pyplot as plt

# Analyze the behavior of the series term for different values of x
def term(n, x):
    if x == 0 and n == 0:
        return 0  # 0^0 / (1 + 0^0) = 0/2 = 0
    return x**n / (1 + x**(2*n))

# Test different values of x
x_values = [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]

for x in x_values:
    print(f"\nx = {x}:")
    terms = [term(n, x) for n in range(20)]
    print(f"First 10 terms: {[round(t, 6) for t in terms[:10]]}")
    print(f"Sum of first 20 terms: {sum(terms):.6f}")
    
    # Check if terms go to zero
    if abs(x) < 1:
        print(f"Term 100: {term(100, x):.2e}")
        if abs(x) < 0.5:
            print(f"Term 1000: {term(1000, x):.2e}")
    elif abs(x) > 1:
        # For |x| > 1, x^n/(1+x^{2n}) ≈ x^n/x^{2n} = x^{-n}
        print(f"Term 100 ≈ {x**(-100):.2e}")
        print(f"Term 1000 ≈ {x**(-1000):.2e}")

# Special analysis for |x| = 1
print("\n\nSpecial case x = 1:")
partial_sums = []
for N in [10, 100, 1000, 10000]:
    s = sum(1/(1+1) for n in range(N))
    partial_sums.append(s)
    print(f"Sum of first {N} terms: {s}")

print("\n\nSpecial case x = -1:")
partial_sums = []
for N in [10, 20, 30, 40]:
    s = sum((-1)**n / (1 + (-1)**(2*n)) for n in range(N))
    partial_sums.append(s)
    print(f"Sum of first {N} terms: {s}")