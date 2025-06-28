#!/usr/bin/env python3

# Calculate Fibonacci numbers to verify
def fibonacci(n):
    if n == 0 or n == 1:
        return 1
    fib = [1, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Generate first 20 Fibonacci numbers
fib_seq = fibonacci(20)
print("Fibonacci sequence (starting with f_0 = 1, f_1 = 1):")
for i, f in enumerate(fib_seq):
    print(f"f_{i} = {f}")

# Check divisibility for part (b)
print("\nChecking divisibility f_n | f_{2n}:")
for n in range(1, 11):
    if 2*n < len(fib_seq):
        divisible = fib_seq[2*n] % fib_seq[n] == 0
        print(f"n={n}: f_{n} = {fib_seq[n]}, f_{2*n} = {fib_seq[2*n]}, divisible: {divisible}")

# Check gcd for part (c)
import math
print("\nChecking gcd(f_n, f_{n+1}) = 1:")
for n in range(0, 15):
    if n+1 < len(fib_seq):
        g = math.gcd(fib_seq[n], fib_seq[n+1])
        print(f"n={n}: gcd(f_{n}, f_{n+1}) = gcd({fib_seq[n]}, {fib_seq[n+1]}) = {g}")