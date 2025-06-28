# Draft Solution

## Part (a)
We need to show that if Φ: U → V is a diffeomorphism with U path-connected, then Φ is either orientation-preserving or orientation-reversing.

Key ideas:
- A diffeomorphism Φ is orientation-preserving at x if det(DΦ(x)) > 0
- A diffeomorphism Φ is orientation-reversing at x if det(DΦ(x)) < 0
- Since Φ is a diffeomorphism, DΦ(x) is invertible everywhere, so det(DΦ(x)) ≠ 0
- The function x ↦ det(DΦ(x)) is continuous
- Since U is path-connected and det(DΦ) is continuous and never zero, by the intermediate value theorem, det(DΦ) must have constant sign

## Part (b)
We need to construct a diffeomorphism Φ: U → U where U = B₁ ∪ B₂ (disjoint union of two open balls) that is neither orientation-preserving nor orientation-reversing.

Key idea:
- Define Φ to be the identity on B₁ (orientation-preserving)
- Define Φ to be a reflection on B₂ (orientation-reversing)
- Since B₁ and B₂ are disjoint, we can define Φ piecewise