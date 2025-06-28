#!/usr/bin/env python3

# Calculate Fibonacci numbers
def fibonacci(n):
    if n == 0 or n == 1:
        return 1
    fib = [1, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Generate Fibonacci numbers
fib = fibonacci(30)

# Known identity: f_{m+n} = f_m * f_{n+1} + f_{m-1} * f_n
# Let's check f_{2n} = f_n * f_{n+1} + f_{n-1} * f_n = f_n * (f_{n+1} + f_{n-1})

print("Checking identity: f_{2n} = f_n * (f_{n+1} + f_{n-1})")
for n in range(1, 15):
    if 2*n < len(fib) and n-1 >= 0:
        lhs = fib[2*n]
        rhs = fib[n] * (fib[n+1] + fib[n-1])
        print(f"n={n}: f_{{{2*n}}} = {lhs}, f_{n} * (f_{{{n+1}}} + f_{{{n-1}}}) = {fib[n]} * ({fib[n+1]} + {fib[n-1]}) = {rhs}")
        print(f"  Identity holds: {lhs == rhs}")

# Actually, let's check if we can express f_{2n} in terms of f_n
print("\n\nLooking for a formula for f_{2n} in terms of f_n:")
print("Let's check: f_{2n} = f_n * L_n where L_n is the n-th Lucas number")
# Lucas numbers: L_0 = 2, L_1 = 1, L_{n+1} = L_n + L_{n-1}
lucas = [2, 1]
for i in range(2, 21):
    lucas.append(lucas[i-1] + lucas[i-2])

print("\nLucas numbers:")
for i in range(10):
    print(f"L_{i} = {lucas[i]}")

print("\nChecking if f_{2n} = f_n * L_n:")
for n in range(1, 11):
    if 2*n < len(fib):
        print(f"n={n}: f_{{{2*n}}} = {fib[2*n]}, f_{n} * L_{n} = {fib[n]} * {lucas[n]} = {fib[n] * lucas[n]}")
        print(f"  Equal: {fib[2*n] == fib[n] * lucas[n]}")