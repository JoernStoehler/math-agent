# Draft Calculations for Power Sets

## Power Set Definition
The power set P(M) of a set M is the set of all subsets of M, including the empty set and M itself.
For a set with n elements, the power set has 2^n elements.

## M₁ = {0, 1, 2, 3}
|M₁| = 4, so |P(M₁)| = 2^4 = 16 elements

P(M₁) = {
  ∅,
  {0}, {1}, {2}, {3},
  {0,1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3},
  {0,1,2}, {0,1,3}, {0,2,3}, {1,2,3},
  {0,1,2,3}
}

## M₂ = {a, b, c}
|M₂| = 3, so |P(M₂)| = 2^3 = 8 elements

P(M₂) = {
  ∅,
  {a}, {b}, {c},
  {a,b}, {a,c}, {b,c},
  {a,b,c}
}

## M₃ = {∅, λ, z}
|M₃| = 3 (note: ∅ is an element here, not the empty set), so |P(M₃)| = 2^3 = 8 elements

P(M₃) = {
  ∅,
  {∅}, {λ}, {z},
  {∅,λ}, {∅,z}, {λ,z},
  {∅,λ,z}
}

Note: In M₃, the symbol ∅ is an element of the set, not the empty set itself. The empty subset of M₃ is still denoted as ∅ in the power set.