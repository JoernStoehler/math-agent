#!/usr/bin/env python3
import math

# Generate Fibonacci sequence as defined in the problem
f = [1, 1]
for i in range(2, 30):
    f.append(f[i-1] + f[i-2])

# Check that consecutive Fibonacci numbers are coprime
print("Checking gcd(f_n, f_{n+1}) = 1:")
all_coprime = True
for n in range(0, 20):
    g = math.gcd(f[n], f[n+1])
    print(f"n={n}: gcd(f_{n}, f_{{{n+1}}}) = gcd({f[n]}, {f[n+1]}) = {g}")
    if g != 1:
        all_coprime = False

print(f"\nAll consecutive Fibonacci numbers coprime: {all_coprime}")

# The proof idea: 
# If d divides both f_n and f_{n+1}, then d divides f_{n+1} - f_n = f_{n-1}
# Continuing this argument, d must divide all previous Fibonacci numbers
# Eventually d must divide f_1 = 1, so d = 1

print("\n\nProof sketch:")
print("If d | f_n and d | f_{n+1}, then:")
print("d | (f_{n+1} - f_n) = f_{n-1}")
print("So d divides f_{n-1}, f_n, f_{n+1}")
print("Continuing: d | (f_n - f_{n-1}) = f_{n-2}")
print("By induction downward, d must divide f_1 = 1")
print("Therefore d = 1")