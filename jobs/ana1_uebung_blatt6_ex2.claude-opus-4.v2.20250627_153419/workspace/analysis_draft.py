import numpy as np
import matplotlib.pyplot as plt

# Series (a): sum(2^n * n! / n^n)
# Using Stirling's approximation: n! ~ sqrt(2*pi*n) * (n/e)^n
# So 2^n * n! / n^n ~ 2^n * sqrt(2*pi*n) * (n/e)^n / n^n = 2^n * sqrt(2*pi*n) / e^n

# Let's compute the ratio test for series (a)
def ratio_test_a(n):
    # a_n = 2^n * n! / n^n
    # a_{n+1} = 2^(n+1) * (n+1)! / (n+1)^(n+1)
    # ratio = a_{n+1} / a_n
    # = [2^(n+1) * (n+1)! / (n+1)^(n+1)] / [2^n * n! / n^n]
    # = 2 * (n+1) * n^n / (n+1)^(n+1)
    # = 2 * (n+1) * n^n / [(n+1) * (n+1)^n]
    # = 2 * n^n / (n+1)^n
    # = 2 * (n/(n+1))^n
    # = 2 * (1 - 1/(n+1))^n
    # As n -> inf, this approaches 2/e < 1
    ratio = 2 * (n/(n+1))**n
    return ratio

# Series (b): sum(3^n * n! / n^n)
def ratio_test_b(n):
    # Similar to (a), but with 3 instead of 2
    # ratio approaches 3/e > 1
    ratio = 3 * (n/(n+1))**n
    return ratio

# Let's verify the limits
n_values = np.arange(1, 100)
ratios_a = [ratio_test_a(n) for n in n_values]
ratios_b = [ratio_test_b(n) for n in n_values]

print("Series (a): 2^n * n! / n^n")
print(f"Ratio test limit: {ratios_a[-1]:.6f}")
print(f"2/e = {2/np.e:.6f}")
print(f"Converges: {2/np.e < 1}")

print("\nSeries (b): 3^n * n! / n^n")
print(f"Ratio test limit: {ratios_b[-1]:.6f}")
print(f"3/e = {3/np.e:.6f}")
print(f"Converges: {3/np.e < 1}")

# Series (c): sum((1 + (-1)^n * n) / n^2)
# This can be split into sum(1/n^2) + sum((-1)^n * n / n^2) = sum(1/n^2) + sum((-1)^n / n)
print("\nSeries (c): (1 + (-1)^n * n) / n^2")
print("Split into: sum(1/n^2) + sum((-1)^n / n)")
print("sum(1/n^2) converges (p-series with p=2>1)")
print("sum((-1)^n / n) converges (alternating harmonic series)")
print("Therefore, the original series converges")

# Series (d): sum(x^n / (1 + x^(2n))) for x in R
print("\nSeries (d): x^n / (1 + x^(2n))")
print("Need to consider different cases for x:")
print("- |x| < 1: x^n / (1 + x^(2n)) ~ x^n (geometric series, converges)")
print("- |x| = 1: Need special analysis")
print("- |x| > 1: x^n / (1 + x^(2n)) ~ x^n / x^(2n) = 1/x^n (converges)")