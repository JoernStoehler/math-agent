#!/usr/bin/env python3

# Generate Fibonacci
f = [1, 1]
for i in range(2, 50):
    f.append(f[i-1] + f[i-2])

# Known property: gcd(f_m, f_n) = f_{gcd(m,n)}
# This would mean f_n | f_m if and only if n | m

import math

print("Testing the property: f_n | f_m if and only if n | m")
print("\nChecking for small values:")

for n in range(2, 10):
    print(f"\nFor n={n}:")
    divisible_indices = []
    for m in range(1, 30):
        if m < len(f) and f[m] % f[n] == 0:
            divisible_indices.append(m)
    
    print(f"  f_{n} = {f[n]} divides f_m at indices m = {divisible_indices[:10]}...")
    
    # Check if these are multiples of n
    multiples_of_n = [k*n for k in range(1, 11) if k*n < len(f)]
    print(f"  Multiples of {n}: {multiples_of_n[:10]}...")
    
    # Check if they match
    match = all(idx % n == 0 for idx in divisible_indices if idx > 0)
    print(f"  All divisible indices are multiples of n: {match}")

# So the correct statement should be: f_n | f_{kn} for all k
# Not specifically f_n | f_{2n}

print("\n\nActually, let me double-check the specific claim f_n | f_{2n}:")
for n in range(1, 15):
    if 2*n < len(f):
        divisible = f[2*n] % f[n] == 0
        print(f"n={n}: f_{n} = {f[n]}, f_{{{2*n}}} = {f[2*n]}, divisible: {divisible}")

# Wait! f_1 = 1 divides everything. Let me check with the standard relation
print("\n\nMaybe there's a confusion with indices. Let me be very careful:")
print("Given: f_0 = 1, f_1 = 1, f_{n+1} = f_n + f_{n-1}")
print("This is shifted from standard Fibonacci by 1 index")
print("\nIn standard Fibonacci (F_0=0, F_1=1), we have F_n | F_{kn}")
print("Our sequence: f_n = F_{n+1}")

print("\n\nSo maybe the statement should be interpreted differently?")
print("Let me check if the pattern works with a shift...")