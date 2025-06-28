#!/usr/bin/env python3

# Calculate Fibonacci numbers
def fibonacci(n):
    if n == 0 or n == 1:
        return 1
    fib = [1, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

# Generate first 30 Fibonacci numbers
fib_seq = fibonacci(30)

# Let's look for patterns in divisibility
print("Looking for patterns where f_n divides f_m:")
print("Checking if f_n divides f_{kn} for various k:")

for n in range(1, 11):
    print(f"\nFor n={n} (f_{n} = {fib_seq[n]}):")
    divisors = []
    for k in range(1, 6):
        if k*n < len(fib_seq):
            if fib_seq[k*n] % fib_seq[n] == 0:
                divisors.append(k)
                print(f"  f_{n} divides f_{{{k}*{n}}} = f_{k*n} = {fib_seq[k*n]}")
    if divisors:
        print(f"  Divisible at multiples: {divisors}")

# Let's specifically check the claim again
print("\n\nSpecific check for f_n | f_{2n}:")
for n in range(1, 15):
    if 2*n < len(fib_seq):
        print(f"n={n}: {fib_seq[n]} | {fib_seq[2*n]} ? {fib_seq[2*n] % fib_seq[n] == 0}")