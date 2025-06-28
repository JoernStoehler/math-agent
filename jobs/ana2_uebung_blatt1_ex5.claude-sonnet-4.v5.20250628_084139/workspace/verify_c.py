import sympy as sp

x = sp.Symbol('x')

print("Verifying Part (c) step by step")
print("=" * 50)

# Original function
f_c = x/(x**3 - x**2 + x - 1)

# Factor denominator manually
denom = x**3 - x**2 + x - 1
print(f"Denominator: {denom}")

# Check factorization by grouping
grouped = x**2*(x - 1) + 1*(x - 1)
print(f"Grouping: x^2(x-1) + 1(x-1) = {sp.expand(grouped)}")
factored = (x**2 + 1)*(x - 1)
print(f"Factor out (x-1): (x^2+1)(x-1) = {sp.expand(factored)}")

# Set up partial fractions
# Since x^2+1 is irreducible over reals, we need form (Ax+B)/(x^2+1) + C/(x-1)
A, B, C = sp.symbols('A B C')
pf_form = (A*x + B)/(x**2 + 1) + C/(x - 1)

print(f"\nPartial fraction form: (Ax+B)/(x^2+1) + C/(x-1)")

# Clear denominators: x = (Ax+B)(x-1) + C(x^2+1)
numerator_pf = (A*x + B)*(x - 1) + C*(x**2 + 1)
expanded = sp.expand(numerator_pf)
print(f"After clearing denominators: x = {expanded}")

# Coefficient matching
# x^2 coefficient: 0 = A + C
# x coefficient: 1 = -A + B
# constant: 0 = -B + C

# From equations:
C_val = sp.S(1)/2  # From substituting x=1: 1 = 2C
A_val = -C_val  # From x^2 coefficient
B_val = 1 + A_val  # From x coefficient

print(f"\nAt x=1: 1 = C*2, so C = {C_val}")
print(f"From x^2 coefficient: 0 = A + C, so A = {A_val}")
print(f"From x coefficient: 1 = -A + B, so B = {B_val}")

# Verify constant term
print(f"Check constant term: 0 = -B + C = -{B_val} + {C_val} = {-B_val + C_val}")

# Construct result
pf_result = (A_val*x + B_val)/(x**2 + 1) + C_val/(x - 1)
print(f"\nPartial fraction decomposition: {pf_result}")

# Simplify first fraction
first_frac = (A_val*x + B_val)/(x**2 + 1)
simplified_first = sp.simplify(first_frac)
print(f"First fraction simplified: {simplified_first}")

# Integrate
integral = sp.integrate(pf_result, x)
print(f"\nIntegral: {integral} + C")

# Double-check by differentiating
derivative = sp.diff(integral, x)
simplified = sp.simplify(derivative)
print(f"\nVerification - derivative of integral: {simplified}")
print(f"Original function: {f_c}")
print(f"Are they equal? {sp.simplify(simplified - f_c) == 0}")