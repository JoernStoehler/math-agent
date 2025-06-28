# Draft Solution for Inertia Tensor Exercise

## Part (a): Show that ⟨v, Θv⟩ is the moment of inertia

For |v| = 1, we need to show that ⟨v, Θv⟩ is the moment of inertia about the line through the origin in direction v.

The moment of inertia about an axis in direction v is:
I = ∫ d²(x) dμ(x)

where d(x) is the perpendicular distance from point x to the axis.

For a unit vector v and a point x, the perpendicular distance is:
d(x) = |x × v| = |x|²|v|² - ⟨x,v⟩² = |x|² - ⟨x,v⟩²

So the moment of inertia is:
I = ∫ (|x|² - ⟨x,v⟩²) dμ(x)

Now let's compute ⟨v, Θv⟩:
⟨v, Θv⟩ = ⟨v, ∫(|x|²v - ⟨x,v⟩x) dμ(x)⟩
        = ∫ ⟨v, |x|²v - ⟨x,v⟩x⟩ dμ(x)
        = ∫ (|x|²⟨v,v⟩ - ⟨x,v⟩⟨v,x⟩) dμ(x)
        = ∫ (|x|² - ⟨x,v⟩²) dμ(x)

This equals I!

## Part (b): Show Θ is symmetric and positive semidefinite

### Symmetry:
We need to show ⟨u, Θv⟩ = ⟨Θu, v⟩ for all u,v ∈ ℝ³.

⟨u, Θv⟩ = ⟨u, ∫(|x|²v - ⟨x,v⟩x) dμ(x)⟩
        = ∫ (|x|²⟨u,v⟩ - ⟨x,v⟩⟨u,x⟩) dμ(x)

⟨Θu, v⟩ = ⟨∫(|x|²u - ⟨x,u⟩x) dμ(x), v⟩
        = ∫ (|x|²⟨u,v⟩ - ⟨x,u⟩⟨x,v⟩) dμ(x)

Since ⟨x,v⟩⟨u,x⟩ = ⟨x,u⟩⟨x,v⟩, we have ⟨u, Θv⟩ = ⟨Θu, v⟩.

### Positive semidefiniteness:
From part (a), for any v with |v| = 1:
⟨v, Θv⟩ = ∫ (|x|² - ⟨x,v⟩²) dμ(x) ≥ 0

since |x|² - ⟨x,v⟩² ≥ 0 by Cauchy-Schwarz.

For general v ≠ 0:
⟨v, Θv⟩ = |v|² ⟨v/|v|, Θ(v/|v|)⟩ ≥ 0

### Positive definiteness:
⟨v, Θv⟩ = 0 ⟺ ∫ (|x|² - ⟨x,v⟩²) dμ(x) = 0
⟺ |x|² - ⟨x,v⟩² = 0 μ-a.e.
⟺ |x||v| = |⟨x,v⟩| μ-a.e.
⟺ x and v are parallel μ-a.e.

So Θ is positive definite unless all mass is concentrated along a line through the origin.

## Part (c): Show λ₃ ≤ λ₁ + λ₂

We can write Θ in matrix form:
Θᵢⱼ = ∫ (|x|²δᵢⱼ - xᵢxⱼ) dμ(x)

This gives:
Θ = ∫ (|x|²I - xx^T) dμ(x)

where I is the 3×3 identity matrix and xx^T is the outer product.

The trace is:
tr(Θ) = ∫ (3|x|² - |x|²) dμ(x) = 2∫ |x|² dμ(x)

So λ₁ + λ₂ + λ₃ = 2∫ |x|² dμ(x).

For any symmetric matrix A = |x|²I - xx^T:
- The eigenvalues are |x|², |x|², 0 (with eigenvector x)
- Or if x = 0, the eigenvalues are 0, 0, 0

Since Θ is the integral of such matrices, and eigenvalues of a sum are bounded by sums of eigenvalues, we need a more careful argument...

Actually, let's use that for any symmetric matrix:
λ₃ ≤ λ₁ + λ₂ is equivalent to λ₃ ≤ tr(Θ)/2

Since tr(Θ) = λ₁ + λ₂ + λ₃, we need λ₃ ≤ (λ₁ + λ₂ + λ₃)/2, which gives λ₃ ≤ λ₁ + λ₂.