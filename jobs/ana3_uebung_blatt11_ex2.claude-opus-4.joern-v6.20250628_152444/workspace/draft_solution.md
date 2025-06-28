# Draft Solution

## Part (a)
We need to show that if Φ : U → V is a diffeomorphism between open sets U, V ⊆ ℝⁿ and U is path-connected, then Φ is either orientation-preserving (det(DΦₓ) > 0 for all x ∈ U) or orientation-reversing (det(DΦₓ) < 0 for all x ∈ U).

Key idea: The determinant of the Jacobian matrix DΦₓ is continuous and never zero (since Φ is a diffeomorphism). By path-connectedness, the sign of det(DΦₓ) must be constant.

Proof:
1. Since Φ is a diffeomorphism, DΦₓ is invertible for all x ∈ U, hence det(DΦₓ) ≠ 0 for all x ∈ U.
2. The function f : U → ℝ\{0} defined by f(x) = det(DΦₓ) is continuous (as the determinant is a continuous function of matrix entries).
3. Since U is path-connected and f is continuous with f(U) ⊆ ℝ\{0}, the image f(U) must be path-connected in ℝ\{0}.
4. But ℝ\{0} = (-∞,0) ∪ (0,∞) is not path-connected! So f(U) must be contained entirely in either (-∞,0) or (0,∞).
5. Therefore, either det(DΦₓ) > 0 for all x ∈ U (orientation-preserving) or det(DΦₓ) < 0 for all x ∈ U (orientation-reversing).

## Part (b)
We need to construct a diffeomorphism Φ : U → U where U = B₁ ∪ B₂ is the disjoint union of two open balls, such that Φ is neither orientation-preserving nor orientation-reversing.

Key idea: Define Φ to be orientation-preserving on B₁ and orientation-reversing on B₂.

Construction:
Let B₁ = B((-2,0,...,0), 1) and B₂ = B((2,0,...,0), 1) be two disjoint open balls in ℝⁿ.

Define Φ : U → U by:
- On B₁: Φ(x) = x (identity map)
- On B₂: Φ(x₁, x₂, ..., xₙ) = (4 - x₁, x₂, ..., xₙ) (reflection about the hyperplane x₁ = 2)

This is a diffeomorphism because:
1. Φ is smooth on each ball
2. Φ is bijective (identity on B₁, reflection on B₂ which maps B₂ to itself)
3. The inverse is also smooth

The Jacobian:
- On B₁: DΦₓ = I (identity matrix), so det(DΦₓ) = 1 > 0
- On B₂: DΦₓ = diag(-1, 1, ..., 1), so det(DΦₓ) = -1 < 0

Therefore, Φ is orientation-preserving on B₁ and orientation-reversing on B₂, making it neither globally orientation-preserving nor globally orientation-reversing.