import numpy as np
import sympy as sp

# Define symbolic variables
u, v, r, R = sp.symbols('u v r R', real=True)

# Define the parametrization
f = sp.Matrix([
    (R + r*sp.cos(v))*sp.cos(u),
    (R + r*sp.cos(v))*sp.sin(u),
    r*sp.sin(v)
])

# Compute partial derivatives
f_u = f.diff(u)
f_v = f.diff(v)

print("∂f/∂u =")
print(f_u)
print("\n∂f/∂v =")
print(f_v)

# Compute cross product
cross_product = f_u.cross(f_v)
print("\n∂f/∂u × ∂f/∂v =")
print(cross_product)

# Simplify
cross_product_simplified = sp.simplify(cross_product)
print("\nSimplified:")
print(cross_product_simplified)

# Compute magnitude
magnitude = sp.sqrt(cross_product.dot(cross_product))
magnitude_simplified = sp.simplify(magnitude)
print("\n|∂f/∂u × ∂f/∂v| =")
print(magnitude_simplified)

# Unit normal
unit_normal = cross_product / magnitude_simplified
unit_normal_simplified = sp.simplify(unit_normal)
print("\nUnit normal field:")
print(unit_normal_simplified)