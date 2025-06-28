import sympy as sp

# Define the variable
x = sp.Symbol('x')

# Define the integrand
integrand = sp.exp(x) * sp.sin(x)

# My proposed antiderivative
my_antiderivative = sp.Rational(1,2) * sp.exp(x) * (sp.sin(x) - sp.cos(x))

# Differentiate to check
derivative = sp.diff(my_antiderivative, x)

# Simplify
derivative_simplified = sp.simplify(derivative)

print("Integrand:", integrand)
print("My antiderivative:", my_antiderivative)
print("Derivative of my antiderivative:", derivative)
print("Simplified derivative:", derivative_simplified)
print("Are they equal?", sp.simplify(derivative_simplified - integrand) == 0)

# Also compute the integral directly using SymPy
sympy_integral = sp.integrate(integrand, x)
print("\nSymPy's integral:", sympy_integral)
print("Simplified SymPy integral:", sp.simplify(sympy_integral))