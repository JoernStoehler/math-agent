import sympy as sp

x = sp.Symbol('x')

print("Verifying Part (b) step by step")
print("=" * 50)

# Original function
f_b = x/(x**3 + x**2 - x - 1)

# Factor denominator manually
denom = x**3 + x**2 - x - 1
print(f"Denominator: {denom}")

# Check factorization by grouping
grouped = x**2*(x + 1) - 1*(x + 1)
print(f"Grouping: x^2(x+1) - 1(x+1) = {sp.expand(grouped)}")
factored = (x**2 - 1)*(x + 1)
print(f"Factor out (x+1): (x^2-1)(x+1) = {sp.expand(factored)}")
factored2 = (x-1)*(x+1)*(x+1)
print(f"Further factor: (x-1)(x+1)^2 = {sp.expand(factored2)}")

# Set up partial fractions
A, B, C = sp.symbols('A B C')
pf_form = A/(x-1) + B/(x+1) + C/(x+1)**2

print(f"\nPartial fraction form: A/(x-1) + B/(x+1) + C/(x+1)^2")

# Clear denominators
numerator_pf = A*(x+1)**2 + B*(x-1)*(x+1) + C*(x-1)
print(f"After clearing denominators: x = {sp.expand(numerator_pf)}")

# Solve for A, B, C by substitution
# x = 1: 1 = A*4
A_val = sp.S(1)/4
print(f"At x=1: 1 = 4A, so A = {A_val}")

# x = -1: -1 = C*(-2)
C_val = sp.S(1)/2
print(f"At x=-1: -1 = -2C, so C = {C_val}")

# Coefficient of x^2: 0 = A + B
B_val = -A_val
print(f"Coefficient of x^2: 0 = A + B, so B = {B_val}")

# Verify
pf_result = A_val/(x-1) + B_val/(x+1) + C_val/(x+1)**2
print(f"\nPartial fraction decomposition: {pf_result}")

# Integrate
integral = sp.integrate(pf_result, x)
print(f"\nIntegral: {integral} + C")

# Double-check by differentiating
derivative = sp.diff(integral, x)
simplified = sp.simplify(derivative)
print(f"\nVerification - derivative of integral: {simplified}")
print(f"Original function: {f_b}")
print(f"Are they equal? {sp.simplify(simplified - f_b) == 0}")