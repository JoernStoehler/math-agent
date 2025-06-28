# Draft Solution

## Problem Understanding
We need to prove that the shortest path between two points x,y ∈ ℝⁿ is a straight line.

Specifically:
1. Any rectifiable curve f:[a,b]→ℝⁿ with f(a)=x and f(b)=y has length ≥ ||x-y||
2. Equality holds iff f is a monotone parametrization of the line from x to y

## Key Concepts
- Rectifiable curve: has finite length
- Length of a curve: L(f) = sup{∑ᵢ ||f(tᵢ₊₁) - f(tᵢ)|| : a = t₀ < t₁ < ... < tₙ = b}
- For continuously differentiable curves: L(f) = ∫ₐᵇ ||f'(t)|| dt

## Proof Strategy
1. Use the definition of curve length
2. Apply triangle inequality
3. Show lower bound ||x-y||
4. Characterize when equality holds

## Proof

### Part 1: Lower bound
For any partition a = t₀ < t₁ < ... < tₙ = b:

∑ᵢ₌₀ⁿ⁻¹ ||f(tᵢ₊₁) - f(tᵢ)|| ≥ ||∑ᵢ₌₀ⁿ⁻¹ (f(tᵢ₊₁) - f(tᵢ))|| (triangle inequality)
                                = ||f(b) - f(a)||
                                = ||y - x||

Taking supremum over all partitions: L(f) ≥ ||y - x||

### Part 2: Equality condition
Equality in triangle inequality holds iff all vectors point in same direction.

For continuously differentiable f:
L(f) = ∫ₐᵇ ||f'(t)|| dt

If f(t) = x + φ(t)(y-x) with φ:[a,b]→[0,1] monotone increasing:
- f'(t) = φ'(t)(y-x)
- ||f'(t)|| = |φ'(t)| ||y-x|| = φ'(t)||y-x|| (since φ monotone increasing)
- L(f) = ∫ₐᵇ φ'(t)||y-x|| dt = ||y-x|| ∫ₐᵇ φ'(t) dt = ||y-x||(φ(b)-φ(a)) = ||y-x||

Conversely, if L(f) = ||y-x||, then equality must hold in triangle inequality throughout.