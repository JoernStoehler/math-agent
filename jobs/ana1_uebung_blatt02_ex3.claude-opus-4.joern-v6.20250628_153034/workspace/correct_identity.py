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

# Check the correct identity: f_{2n} = f_n * f_{n+1} + f_{n-1} * f_n = f_n * (f_{n+1} + f_{n-1})
# But wait, by definition f_{n+1} = f_n + f_{n-1}, so f_{n+1} + f_{n-1} = f_n + 2*f_{n-1}

print("For reference, first few Fibonacci numbers:")
for i in range(10):
    print(f"f_{i} = {fib[i]}")

print("\nActually, let's use the known identity:")
print("f_{2n} = f_n * L_n where L_n is a specific sequence")
print("\nBut wait, let me check the correct formula:")
print("Known: f_{n+m} = f_n * f_{m+1} + f_{n-1} * f_m")
print("\nSetting m = n: f_{2n} = f_n * f_{n+1} + f_{n-1} * f_n")

for n in range(2, 10):
    lhs = fib[2*n]
    rhs = fib[n] * fib[n+1] + fib[n-1] * fib[n]
    print(f"n={n}: f_{{{2*n}}} = {lhs}, f_{n}*f_{{{n+1}}} + f_{{{n-1}}}*f_{n} = {fib[n]}*{fib[n+1]} + {fib[n-1]}*{fib[n]} = {rhs}")
    print(f"  Equal: {lhs == rhs}")
    
    # Factor out f_n
    factor = fib[n+1] + fib[n-1]
    print(f"  f_{{{2*n}}} = f_{n} * (f_{{{n+1}}} + f_{{{n-1}}}) = {fib[n]} * {factor} = {fib[n] * factor}")
    print(f"  So f_{n} divides f_{{{2*n}}}: {lhs % fib[n] == 0}")
    print()