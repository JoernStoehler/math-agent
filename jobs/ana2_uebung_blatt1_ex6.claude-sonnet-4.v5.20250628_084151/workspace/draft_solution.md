# Draft Solution for ζ(2) using Integral Comparison Criterion

## Problem Analysis
We need to calculate ζ(2) = Σ(n=1 to ∞) 1/n² with accuracy to 2 decimal places.

## Integral Comparison Criterion
For a decreasing positive function f(x), we have:
∫[n to ∞] f(x)dx ≤ Σ(k=n to ∞) f(k) ≤ f(n) + ∫[n to ∞] f(x)dx

For f(x) = 1/x², we have:
- ∫[n to ∞] 1/x² dx = [-1/x][n to ∞] = 1/n
- The series remainder: Rn = Σ(k=n+1 to ∞) 1/k²

Therefore:
1/(n+1) ≤ Rn ≤ 1/n

## Strategy
1. Calculate partial sum Sn = Σ(k=1 to n) 1/k²
2. Use bounds: Sn + 1/(n+1) ≤ ζ(2) ≤ Sn + 1/n
3. Find n such that 1/n - 1/(n+1) < 0.01 for 2 decimal place accuracy

## Calculation
For the bounds to differ by less than 0.01:
1/n - 1/(n+1) < 0.01
1/n - 1/(n+1) = (n+1-n)/(n(n+1)) = 1/(n(n+1)) < 0.01
n(n+1) > 100
n² + n - 100 > 0

Solving: n > (-1 + √401)/2 ≈ 9.5
So we need n ≥ 10.

Let me calculate S₁₀ = Σ(k=1 to 10) 1/k²