import math

# Calculate partial sums
def partial_sum(n):
    return sum(1/k**2 for k in range(1, n+1))

# Find the right n for 2 decimal place accuracy
n = 1
while True:
    diff = 1/n - 1/(n+1)
    if diff < 0.01:
        print(f"Need n ≥ {n} for 2 decimal place accuracy")
        print(f"Difference at n={n}: {diff:.6f}")
        break
    n += 1

# Calculate bounds for different values of n
for n in [10, 20, 30, 40, 50]:
    S_n = partial_sum(n)
    lower_bound = S_n + 1/(n+1)
    upper_bound = S_n + 1/n
    print(f"\nn = {n}:")
    print(f"S_{n} = {S_n:.6f}")
    print(f"Lower bound: {lower_bound:.6f}")
    print(f"Upper bound: {upper_bound:.6f}")
    print(f"Difference: {upper_bound - lower_bound:.6f}")
    print(f"Average: {(lower_bound + upper_bound)/2:.6f}")

# The actual value of ζ(2) = π²/6
actual = math.pi**2 / 6
print(f"\n\nActual value of ζ(2) = π²/6 = {actual:.10f}")

# Let's see what n gives us exactly 2 decimal place accuracy
n = 10
while True:
    S_n = partial_sum(n)
    lower = S_n + 1/(n+1)
    upper = S_n + 1/n
    diff = upper - lower
    if diff < 0.005:  # For rounding to 2 decimal places
        print(f"\nFor exact 2 decimal place accuracy after rounding:")
        print(f"n = {n}, difference = {diff:.6f}")
        print(f"Bounds: [{lower:.6f}, {upper:.6f}]")
        print(f"Both round to: {round(lower, 2)}")
        break
    n += 1