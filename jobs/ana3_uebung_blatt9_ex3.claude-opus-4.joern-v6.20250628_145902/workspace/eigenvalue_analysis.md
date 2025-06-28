# Better proof for part (c)

The matrix representation of Θ in components is:
Θᵢⱼ = ∫ (|x|²δᵢⱼ - xᵢxⱼ) dμ(x)

This gives the matrix:
Θ = ∫ [(y² + z²)    -xy         -xz    ]
     [-xy          (x² + z²)    -yz    ] dμ
     [-xz          -yz       (x² + y²) ]

where x = (x,y,z).

Key observation: For any point mass at position x, the contribution to Θ is:
Θₓ = |x|²I - xx^T

This matrix has:
- Eigenvalue 0 with eigenvector x (since (|x|²I - xx^T)x = |x|²x - |x|²x = 0)
- Eigenvalue |x|² with multiplicity 2 (in the plane orthogonal to x)

Now, for the full tensor Θ = ∫ Θₓ dμ(x), we need to show λ₃ ≤ λ₁ + λ₂.

Since tr(Θ) = λ₁ + λ₂ + λ₃ and we computed:
tr(Θ) = ∫ ((y² + z²) + (x² + z²) + (x² + y²)) dμ
      = ∫ 2(x² + y² + z²) dμ
      = 2∫ |x|² dμ

So λ₁ + λ₂ + λ₃ = 2∫ |x|² dμ.

For any eigenvalue λᵢ and corresponding unit eigenvector vᵢ:
λᵢ = ⟨vᵢ, Θvᵢ⟩ = ∫ (|x|² - ⟨x,vᵢ⟩²) dμ(x) ≤ ∫ |x|² dμ(x)

Therefore: λ₃ ≤ ∫ |x|² dμ = (λ₁ + λ₂ + λ₃)/2

This gives: 2λ₃ ≤ λ₁ + λ₂ + λ₃, hence λ₃ ≤ λ₁ + λ₂.