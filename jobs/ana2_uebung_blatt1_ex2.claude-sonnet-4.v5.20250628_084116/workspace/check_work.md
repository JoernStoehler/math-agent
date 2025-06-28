# Verification of Solutions

## (a) ∫x sin(x) dx
- Used u = x, v' = sin(x)
- Got u' = 1, v = -cos(x)
- Result: sin(b) - sin(a) - b cos(b) + a cos(a) ✓

## (b) ∫x² log(x) dx
- Used u = log(x), v' = x²
- Got u' = 1/x, v = x³/3
- Result looks correct ✓

## (c) ∫x^n e^x dx
- Used recursion formula
- Need to verify the final formula more carefully
- The formula with alternating signs looks correct

## (d) ∫sin(x)cos(x) dx
- Method 1: Used identity sin(x)cos(x) = (1/2)sin(2x) ✓
- Method 2: Integration by parts leads to correct result ✓
- Both methods give equivalent results

## (e) ∫e^x sin(x) dx
- Applied integration by parts twice
- Got a linear equation for the integral
- Result: (1/2)e^x(sin(x) - cos(x)) + C
- Wait, I think there's an error. Let me recalculate.

## (f) ∫arctan(x) dx
- Used u = arctan(x), v' = 1
- The substitution for ∫x/(1+x²) dx is correct ✓
- Result looks correct ✓

Let me fix the error in (e).