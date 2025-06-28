#!/usr/bin/env python3

# Standard Fibonacci: F_0 = 0, F_1 = 1, F_{n+1} = F_n + F_{n-1}
# But the problem states: f_0 = f_1 = 1, f_{n+1} = f_n + f_{n-1}

# Let's check both sequences
print("Standard Fibonacci (F_0 = 0, F_1 = 1):")
F = [0, 1]
for i in range(2, 21):
    F.append(F[i-1] + F[i-2])
for i in range(10):
    print(f"F_{i} = {F[i]}")

print("\nProblem's Fibonacci (f_0 = f_1 = 1):")
f = [1, 1]
for i in range(2, 21):
    f.append(f[i-1] + f[i-2])
for i in range(10):
    print(f"f_{i} = {f[i]}")

# For the problem's sequence, let's check the identity again
# The identity f_{m+n} = f_m * F_{n+1} + f_{m-1} * F_n works for standard Fibonacci
# But we need to adapt it for our sequence

print("\n\nLet me check a known result:")
print("For standard Fibonacci: F_{2n} = F_n * (2*F_{n+1} - F_n) = F_n * L_n")
print("where L_n are Lucas numbers")

# Actually, let's think differently. Maybe the statement is that f_n divides f_{2n}
# Let me check the greatest common divisor property first
import math

print("\n\nChecking GCD properties:")
print("GCD(F_m, F_n) = F_{GCD(m,n)} for standard Fibonacci")

# For the problem sequence, let's see if f_n always divides f_{kn}
print("\n\nChecking if f_n divides f_{kn} for various k:")
for n in range(2, 8):
    print(f"\nFor n={n} (f_{n} = {f[n]}):")
    for k in range(1, 8):
        if k*n < len(f):
            divisible = f[k*n] % f[n] == 0
            if divisible:
                print(f"  f_{n} = {f[n]} divides f_{{{k*n}}} = {f[k*n]} (quotient = {f[k*n] // f[n]})")

# Hmm, maybe the problem meant something else. Let me check if there's a pattern
print("\n\nLet me examine f_{2n} more carefully:")
for n in range(1, 10):
    if 2*n < len(f):
        print(f"n={n}: f_{n} = {f[n]}, f_{{{2*n}}} = {f[2*n]}, f_{{{2*n}}}/f_{n} = {f[2*n]/f[n]:.2f}")