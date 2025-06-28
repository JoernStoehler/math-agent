#!/usr/bin/env python3

# The known identity for Fibonacci numbers is:
# f_{m+n} = f_m * f_{n+1} + f_{m-1} * f_n  (when m >= 1)
# OR more generally:
# f_{m+n} = f_{m-1} * f_n + f_m * f_{n+1}

def fibonacci(n):
    if n == 0 or n == 1:
        return 1
    fib = [1, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])
    return fib

fib = fibonacci(30)

# Let's verify the identity first
print("Verifying f_{m+n} = f_{m-1} * f_n + f_m * f_{n+1}:")
for m in range(1, 5):
    for n in range(1, 5):
        if m+n < len(fib) and m-1 >= 0:
            lhs = fib[m+n]
            rhs = fib[m-1] * fib[n] + fib[m] * fib[n+1]
            print(f"m={m}, n={n}: f_{{{m+n}}} = {lhs}, f_{{{m-1}}}*f_{n} + f_{m}*f_{{{n+1}}} = {fib[m-1]}*{fib[n]} + {fib[m]}*{fib[n+1]} = {rhs}, Equal: {lhs == rhs}")

# Now let's apply this with m = n to get f_{2n}
print("\n\nApplying with m = n to get f_{2n}:")
print("f_{2n} = f_{n-1} * f_n + f_n * f_{n+1} = f_n * (f_{n-1} + f_{n+1})")

for n in range(1, 10):
    if 2*n < len(fib) and n-1 >= 0:
        f_2n = fib[2*n]
        formula = fib[n-1] * fib[n] + fib[n] * fib[n+1]
        factored = fib[n] * (fib[n-1] + fib[n+1])
        print(f"\nn={n}:")
        print(f"  f_{{{2*n}}} = {f_2n}")
        print(f"  f_{{{n-1}}}*f_{n} + f_{n}*f_{{{n+1}}} = {fib[n-1]}*{fib[n]} + {fib[n]}*{fib[n+1]} = {formula}")
        print(f"  f_{n} * (f_{{{n-1}}} + f_{{{n+1}}}) = {fib[n]} * ({fib[n-1]} + {fib[n+1]}) = {factored}")
        print(f"  Equal: {f_2n == formula}")
        
        # Check divisibility
        print(f"  Is f_{{{2*n}}} divisible by f_{n}? {f_2n % fib[n] == 0}")
        if f_2n % fib[n] == 0:
            print(f"  f_{{{2*n}}} / f_{n} = {f_2n // fib[n]}")